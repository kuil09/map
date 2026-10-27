#!/usr/bin/env python3
"""Offline, dependency-free canonical data and preservation checks."""
import argparse
import collections
import csv
import hashlib
import json
import math
import io
from pathlib import Path
import re
import sys
import zipfile
from urllib.parse import urlsplit, parse_qsl

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ('en', 'ko', 'ja', 'zh', 'es')

def load(relative, root=ROOT):
    return json.loads((root / relative).read_text(encoding='utf-8'))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def ensure(condition, message):
    if not condition:
        raise ValueError(message)

def public_url(value):
    parsed = urlsplit(value)
    ensure(parsed.scheme in ('http', 'https') and parsed.hostname, 'Invalid public URL')
    ensure(not parsed.username and not parsed.password, 'Credentials in URL')
    host = parsed.hostname.lower()
    ensure(host not in ('localhost', '127.0.0.1', '0.0.0.0', '::1'), 'Local URL')
    private_query = {'access_token', 'auth_token', 'token', 'signature', 'sig', 'x-amz-signature', 'x-goog-signature'}
    ensure(not any(k.lower() in private_query for k, _ in parse_qsl(parsed.query)), 'Signed/credential URL')

def haversine(origin, destination):
    a, b = math.radians(origin['lat']), math.radians(destination['lat'])
    dlat = b - a
    dlng = math.radians(destination['lng'] - origin['lng'])
    h = math.sin(dlat / 2) ** 2 + math.cos(a) * math.cos(b) * math.sin(dlng / 2) ** 2
    return 6371.0088 * 2 * math.asin(min(1, math.sqrt(h)))

def privacy_scan(root=ROOT):
    # Public website path segments such as /home/pages/ are not filesystem paths.
    patterns = [
        r'/(?:workspace|Users)/[A-Za-z0-9_.-]+/',
        r'/home/(?:agent|oai|ubuntu)/',
        r'(?:gh[pousr]_[A-Za-z0-9]{24,}|github_pat_[A-Za-z0-9_]{30,}|sk-(?:proj-)?[A-Za-z0-9_-]{24,})',
        r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        r'https://chatgpt\.com/(?:c|g)/[A-Za-z0-9_-]+',
        r'Sentinel_[0-9a-f]{20,}',
        r'\bturn[0-9]+(?:search|view|fetch)[0-9]+\b',
        r'[?&](?:X-Amz-Signature|X-Goog-Signature|access_token|auth_token)=[^&\s]+',
        r'[;?&](?:jsessionid|sessionid|session_id)=[^&\s]+',
    ]
    checked = 0
    for path in sorted(root.rglob('*')):
        if not path.is_file() or any(part in ('.git', 'build', '__pycache__') for part in path.relative_to(root).parts):
            continue
        if path.suffix.lower() == '.kmz':
            with zipfile.ZipFile(path) as archive:
                members = archive.infolist()
                ensure(members and sum(m.file_size for m in members) <= 10_000_000, 'Unexpected KMZ size')
                texts = []
                for member in members:
                    parts = Path(member.filename).parts
                    ensure(not Path(member.filename).is_absolute() and '..' not in parts, 'Unsafe KMZ member path')
                    ensure(not member.flag_bits & 1, 'Encrypted KMZ member')
                    raw = archive.read(member)
                    if member.filename.endswith('.kml'):
                        decoded = raw.decode('utf-8-sig')
                    else:
                        ensure(re.fullmatch(r'images/icon-\d+\.png', member.filename) and raw.startswith(b'\x89PNG\r\n\x1a\n'), 'Unexpected KMZ member')
                        decoded = raw.decode('latin-1')
                    texts.append(member.filename + '\n' + decoded)
                text = '\n'.join(texts)
        else:
            text = path.read_text(encoding='utf-8-sig')
        for pattern in patterns:
            ensure(not re.search(pattern, text, re.I), f'Privacy review required: {path.relative_to(root)}')
        checked += 1
    return checked

def current_map_membership(root, sync, receipt, imported):
    """Expected current logical cohort; a row count is not a fresh native-ID audit."""
    if receipt.get('operation') != 'restore_after_layer_deletion':
        return set(imported)
    policy = load('data/map/public-exclusions.json', root)
    ensure(policy['status'] == 'authorized_public_exclusion', 'Public exclusion is not authorized')
    ensure(digest(root / 'data/places.json') == policy['sourcePlacesSha256'], 'Public exclusion source hash drift')
    excluded = policy['excludedPlaceIds']
    ensure(len(excluded) == len(set(excluded)) == 2 and set(excluded) <= set(imported), 'Public exclusion identity drift')
    ensure(receipt['excludedPlaceIds'] == excluded, 'Restore exclusions differ from explicit policy')
    ensure(receipt['canonicalArchiveCount'] == policy['canonicalArchiveCount'] == len(imported) == 648, 'Restore changed logical archive')
    ensure(receipt['publicExclusionPolicySHA256'] == digest(root / 'data/map/public-exclusions.json'), 'Restore exclusion evidence hash drift')
    ensure(sync['mapReceiptSHA256'] == digest(root / sync['mapReceipt']), 'Current map receipt hash drift')
    ensure(receipt['status'] in ('partial', 'verified') and receipt['savedReloadedCountsVerified'] is True and receipt['verifiedAtUtc'], 'Restore counts lack saved/reloaded evidence')
    ensure(sync['mapVerifiedAtUtc'] == receipt['verifiedAtUtc'], 'Restore verification timestamp drift')
    expected = set(imported) - set(excluded)
    ensure(len(expected) == policy['publicCount'] == receipt['counts']['rows'] == 646, 'Restore public membership count drift')
    # An optional complete fresh Record-ID readback is checked, never inferred from totals.
    identity = receipt['identityCoverage']
    if identity['allCurrentRecordIdsFreshlyVerified']:
        observed = identity['verifiedPlaceIds']
        ensure(len(observed) == len(set(observed)) and set(observed) == expected, 'Restore fresh Record-ID membership drift')
    else:
        ensure(identity['verifiedPlaceIds'] == [], 'Unverified current IDs must not be advertised as observed')
    ensure(identity['nativeIdsPreserved'] is False, 'Restore must not claim old native IDs preserved')
    ensure(receipt['preservation']['fullNumericalGeometryPreservationVerified'] is False, 'Restore must not claim exact numerical geometry preservation')
    return expected

def validate(root=ROOT, asset_root=None):
    places = load('data/places.json', root)
    photos = load('data/photos.json', root)
    research = load('data/research.json', root)
    metadata = load('data/metadata.json', root)
    counts = metadata['counts']
    schema = load('schemas/places.schema.json', root)
    required = schema['items']['required']
    ids = [p['id'] for p in places]
    ensure(len(ids) == len(set(ids)), 'Duplicate place ID')
    ensure(len(places) == counts['places'] == research['places'], 'Place count drift')
    statuses = collections.Counter()
    point_count = 0
    for p in places:
        label = p.get('id', '<missing>')
        ensure(all(k in p for k in required), f'{label}: required field missing')
        ensure(re.fullmatch(r'[a-z0-9][a-z0-9_-]*', label), f'{label}: invalid ID')
        ensure(p['name_en'] and p['name_ko'] and p['address'], f'{label}: missing identity/address')
        ensure(p['category'] in schema['items']['properties']['category']['enum'], f'{label}: category')
        ensure(p['setting'] in ('indoor', 'outdoor', 'mixed'), f'{label}: setting')
        for field in ('description', 'notes'):
            ensure(all(isinstance(p[field].get(lang), str) and p[field][lang] for lang in LANGUAGES), f'{label}: {field} languages')
        ensure(p['sources'], f'{label}: no sources')
        for source in p['sources']:
            public_url(source['url'])
            audit = source['audit']
            ensure(audit['status'] in ('verified', 'unconfirmed', 'blocked'), f'{label}: source status')
            ensure(audit.get('checked') and audit.get('scope'), f'{label}: source scope/date')
            if audit.get('final_url'):
                public_url(audit['final_url'])
            statuses[audit['status']] += 1
        point = p['coordinates']
        distance = p['radial_distance_km']
        ensure((point is None) == (distance is None), f'{label}: unknown coordinate/distance mismatch')
        if point is not None:
            ensure(set(point) == {'lat', 'lng'}, f'{label}: point fields')
            ensure(-90 <= point['lat'] <= 90 and -180 <= point['lng'] <= 180, f'{label}: point range')
            ensure(math.isfinite(distance) and distance >= 0, f'{label}: distance range')
            for key in ('coordinate_provenance', 'coordinate_source_url', 'distance_reference_id', 'distance_method'):
                ensure(p.get(key), f'{label}: missing {key}')
            ensure(p['coordinate_source_url'] in [s['url'] for s in p['sources']], f'{label}: coordinate source missing')
            reference = research['distance_audit']['reference']
            ensure(p['distance_reference_id'] == reference['id'], f'{label}: distance reference')
            expected = haversine(reference['coordinates'], point)
            ensure(abs(distance - expected) <= 0.11, f'{label}: distance calculation')
            point_count += 1
    ensure(dict(statuses) == counts['sourceStatuses'], 'Source status counts drift')
    ensure(sum(statuses.values()) == counts['sourceReferences'], 'Source reference count drift')
    ensure(point_count == counts['coordinatePoints'], 'Coordinate count drift')
    ensure(len(places) - point_count == counts['unmeasured'], 'Unmeasured count drift')
    ensure(research['source_audit']['source_reference_statuses'] == dict(statuses), 'Research status summary drift')
    ensure(research['source_audit']['source_references'] == sum(statuses.values()), 'Research source count drift')
    ensure(research['distance_audit']['checked_records'] == point_count and research['distance_audit']['unchecked_records'] == len(places) - point_count, 'Research distance count drift')
    ensure(research['category_counts'] == dict(collections.Counter(p['category'] for p in places)), 'Research category count drift')
    for area, categories in research['coverage'].items():
        expected = collections.Counter(p['category'] for p in places if p['area'] == area)
        ensure(all(count == expected[category] for category, count in categories.items()), f'{area}: coverage count drift')
        ensure(research['coverage_gaps'][area] == [category for category, count in categories.items() if not count], f'{area}: coverage gaps drift')
    ensure(len(photos) == counts['photos'], 'Photo count drift')
    ensure(len({p['id'] for p in photos}) == len(photos), 'Duplicate photo ID')
    assets = []
    for photo in photos:
        for key in ('author', 'license', 'license_url', 'source_url', 'modifications', 'caption'):
            ensure(photo.get(key), f"{photo['id']}: missing photo attribution {key}")
        for key in ('license_url', 'source_url', 'original_url'):
            public_url(photo[key])
        ensure(set(photo['place_ids']).issubset(ids), f"{photo['id']}: unknown photo place link")
        for asset in photo['assets']:
            path = Path(asset['path'])
            ensure(not path.is_absolute() and '..' not in path.parts and path.parts[0] == 'photos', 'Unsafe asset path')
            ensure(re.fullmatch('[a-f0-9]{64}', asset['sha256']) and asset['bytes'] > 0, 'Invalid asset hash/size')
            if asset_root is not None:
                local = Path(asset_root) / path
                ensure(local.is_file(), f'Missing photo asset: {path}')
                ensure(local.stat().st_size == asset['bytes'] and digest(local) == asset['sha256'], f'Photo hash mismatch: {path}')
            assets.append(asset)
    ensure(len(assets) == counts['photoAssets'], 'Asset count drift')
    ensure(sum(a['bytes'] for a in assets) == counts['photoAssetBytes'], 'Asset byte count drift')
    ensure(len({a['path'] for a in assets}) == len(assets), 'Duplicate asset path')
    baseline = load('data/map/baseline607.json', root)['records']
    native_ids = {x['nativeId'] for x in baseline}
    ensure(len(baseline) == len(native_ids) == 607, 'Native historical identity mismatch')
    joins = load('data/map/identity-index.json', root)
    ensure(len(joins['explicitNativeJoins']) == 296 and len(joins['nativeJoinsNotEstablished']) == 311, 'Identity join coverage')
    ensure({x['nativeId'] for x in joins['explicitNativeJoins']} | set(joins['nativeJoinsNotEstablished']) == native_ids, 'Identity coverage')
    ensure({x['placeId'] for x in joins['explicitNativeJoins']}.issubset(ids), 'Unknown joined place')
    original = load('data/history/original-source-audits296.json', root)
    ensure(len(original) == 296 and len({x['nativeId'] for x in original}) == 296, 'Original audit coverage')
    for x in original:
        ensure(x['nativeId'] in native_ids, 'Audit native identity missing')
        ensure(hashlib.sha256(x['originalSourceAudit'].encode('utf-8')).hexdigest() == x['valueUtf8SHA256'], 'Original audit modified')
    applied = load('data/history/applied-field-changes213.json', root)
    pending = load('data/map/pending-field-edits692.json', root)
    ensure(len(applied) == 213 and len(pending) == 692, 'Historical cleanup counts')
    applied_keys = {(x['nativeId'], x['field']) for x in applied}
    pending_keys = {(x['nativeId'], x['field']) for x in pending}
    ensure(len(applied_keys) == 213 and len(pending_keys) == 692, 'Duplicate cleanup key')
    ensure(not (applied_keys & pending_keys), 'Applied key repeated in pending')
    ensure(all(x['nativeId'] in native_ids for x in applied + pending), 'Cleanup native identity missing')
    unresolved = load('data/map/unresolved6.json', root)
    ensure(len(unresolved) == 6 and all(x['nativeId'] in native_ids for x in unresolved), 'Unresolved coverage')
    sync = load('data/map/sync-state.json', root)
    historical_imported = joins['receiptBackedImportedPlaceIds']
    ensure(len(historical_imported) == len(set(historical_imported)) == 607, 'Historical imported cohort IDs')
    verified_history = load(sync['verifiedImportHistory'], root)
    operations = verified_history['completedAppendOperations']
    imported = list(historical_imported)
    for operation in operations:
        receipt_path = root / operation['receipt']
        receipt = load(operation['receipt'], root)
        ensure(digest(receipt_path) == operation['receiptSHA256'], 'Verified receipt hash drift')
        new_ids = operation['placeIds']
        ensure(new_ids == receipt['append']['recordIds'], 'Verified imported membership drift')
        ensure(len(new_ids) == len(set(new_ids)) == operation['rows'] == receipt['append']['rows'] == 41, 'Verified append row count')
        ensure(not set(new_ids) & set(imported), 'Repeated verified append IDs')
        ensure(operation['successfulOperations'] == receipt['append']['successfulOperations'] == 1 and operation['duplicateAppends'] == receipt['append']['duplicateAppends'] == 0, 'Repeat append operation')
        ensure(operation['nativeIds'] == [] and operation['nativeIdsExposed'] is False, 'Invented new native IDs')
        ensure(operation['exactAppendSaveAtUtc'] is None and receipt['timestamps']['exactOriginalAppendSaveAtUtc'] is None, 'Invented exact append timestamp')
        ensure([i for cohort in operation['cohorts'] for i in cohort['placeIds']] == new_ids, 'Verified cohort membership drift')
        ensure(all(c['status'] == 'imported_saved_reloaded_verified' for c in operation['cohorts']), 'Unverified imported cohort')
        original_artifact = operation['originalArtifact']
        successful = operation['successfulArtifact']
        original_bytes = (root / original_artifact['path']).read_bytes()
        successful_bytes = (root / successful['path']).read_bytes()
        ensure(original_bytes.startswith(b'\xef\xbb\xbf') and successful_bytes == original_bytes[3:], 'Successful compatibility CSV must remove only BOM')
        ensure(digest(root / original_artifact['path']) == original_artifact['sha256'] == receipt['append']['originalCsvSHA256'], 'Original append evidence drift')
        ensure(digest(root / successful['path']) == successful['sha256'] == receipt['append']['compatibilityCsv']['sha256'], 'Successful CSV hash drift')
        ensure(len(successful_bytes) == successful['bytes'] == receipt['append']['compatibilityCsv']['bytes'], 'Successful CSV size drift')
        from map_csv import FIELDS
        parsed = csv.DictReader(io.StringIO(successful_bytes.decode('utf-8'), newline=''), strict=True)
        rows = list(parsed)
        ensure(parsed.fieldnames == FIELDS == receipt['append']['compatibilityCsv']['headers'], 'Successful CSV exact header drift')
        ensure([r['Record ID'] for r in rows] == new_ids and sum(len(r) for r in rows) == 410, 'Successful CSV 410-cell membership drift')
        ensure(successful['notForImport'] is True, 'Historical successful CSV is not an upload candidate')
        imported.extend(new_ids)
    ensure(len(operations) == 1 and len(imported) == 648, 'Verified import history coverage')
    receipt = load(sync['mapReceipt'], root)
    current_membership = current_map_membership(root, sync, receipt, imported)
    current_unresolved = load(sync['currentUnresolvedFile'], root)
    ensure(len(current_unresolved) == 7 and [x['siteRecordId'] for x in current_unresolved] == [x['recordId'] for x in receipt['unresolved']], 'Current unresolved identity drift')
    ensure([x['name'] for x in current_unresolved] == [x['name'] for x in receipt['unresolved']], 'Current unresolved name drift')
    ensure(all(x['nativeId'] is None for x in current_unresolved), 'Unverified fresh unresolved native ID')
    if receipt.get('operation') == 'restore_after_layer_deletion':
        historical_unresolved = load('data/map/unresolved7.json', root)
        retained = {x['siteRecordId'] for x in historical_unresolved} & current_membership
        expected_unresolved = retained | {'activity-ds-billiards-paengseong'}
        ensure({x['siteRecordId'] for x in current_unresolved} == expected_unresolved and len(expected_unresolved) == 7, 'Restore unresolved public membership drift')
        ensure(sync['currentUnresolvedFile'] not in ('data/map/unresolved6.json', 'data/map/unresolved7.json'), 'Restore must not overwrite historical unresolved evidence')
        ensure(set(('data/map/unresolved6.json', 'data/map/unresolved7.json')) <= set(sync['historicalUnresolvedFiles']), 'Restore historical unresolved references missing')
    else:
        ensure([x['siteRecordId'] for x in current_unresolved[:6]] == [x['siteRecordId'] for x in unresolved], 'Original six unresolved not preserved')
    queue = sync['pendingAppendPlaceIds']
    ensure(len(imported) == len(set(imported)) == 648, 'Imported cohort IDs')
    ensure(len(queue) == len(set(queue)) and not set(queue) & set(imported), 'Pending IDs duplicate imported cohort')
    ensure(set(imported) | set(queue) == set(ids), 'Imported + pending does not cover canonical places')
    ensure(sync['siteTotal'] == len(places), 'Sync site count drift')
    ensure(research['map']['expected_total'] == len(places) and research['map']['remaining_map_uploads'] == len(queue), 'Research pending-map count drift')
    ensure(sync['confirmedNativeRows'] == receipt['counts']['rows'] == len(current_membership) and sync['positionedMarkers'] == receipt['counts']['positioned'] == len(current_membership) - 7 and sync['unresolvedRows'] == receipt['counts']['unresolved'] == 7, 'Receipt-backed map counts')
    ensure(sync['positionedMarkers'] + sync['unresolvedRows'] == sync['confirmedNativeRows'], 'Positioned/unresolved count sum')
    ensure(research['map']['confirmed_data_rows'] == research['map']['total_verified_rows'] == sync['confirmedNativeRows'] and research['map']['positioned_markers'] == sync['positionedMarkers'] and research['map']['unlocated_rows'] == research['map']['error_rows'] == sync['unresolvedRows'], 'Research verified map counts drift')
    ensure(sync['pendingCohorts'] == [] and queue == [], 'Completed 41 rows must not be queued for repeated upload')
    ensure(sync['lastPublishedSiteRelease'] == metadata['lastPublishedSiteRelease'] == load('data/history/site-deployment-v37.json', root)['siteRelease'] == 'v37', 'Published Site receipt mismatch')
    ensure(metadata['snapshotRelease'] == sync['siteRelease'] == 'v38' and metadata['releaseStatus'] == sync['siteReleaseStatus'] == 'canonical_prepared_not_site_deployed', 'Prepared v38 must not claim publication')
    archive = sync['appendFile']
    archived_csv = root / archive['path']
    ensure(digest(archived_csv) == archive['sha256'] and archived_csv.stat().st_size == archive['bytes'], 'Historical append CSV hash')
    with archived_csv.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        csv_rows = list(reader)
        ensure(len(reader.fieldnames) == 10 and 'Source audit' not in reader.fieldnames and 'Latitude' not in reader.fieldnames and 'Longitude' not in reader.fieldnames, 'Unsafe archived import fields')
    ensure(len(csv_rows) == archive['rows'] == 35, 'Historical append row count')
    ensure(len({x['Record ID'] for x in csv_rows}) == 35, 'Duplicate archived append ID')
    for row in csv_rows:
        ensure(row['Record ID'] in ids, 'Archived append unknown ID')
        ensure(row['Category'][0].isascii() and row['Category'][0].isalpha(), 'Category must be English-first')
        for value in row.values():
            ensure(not value.lstrip().startswith(('=', '+', '-', '@')), 'Spreadsheet formula-like cell')
    current = sync.get('currentAppendFile')
    archived_paths = {archive['path']}
    for prior in sync.get('archivedAppendFiles', []):
        path = root / prior['path']
        ensure(prior['path'] not in archived_paths, 'Duplicate historical append artifact')
        archived_paths.add(prior['path'])
        ensure(path.stat().st_size == prior['bytes'] and digest(path) == prior['sha256'], 'Preserved append artifact hash/size drift')
        with path.open(encoding='utf-8-sig', newline='') as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            ensure(len(reader.fieldnames) == 10 and not {'Latitude', 'Longitude', 'Source audit'} & set(reader.fieldnames), 'Unsafe preserved append fields')
        ensure(len(rows) == prior['rows'] and len({row['Record ID'] for row in rows}) == len(rows), 'Preserved append row count/identity drift')
        ensure(all(row['Record ID'] in ids for row in rows), 'Preserved append unknown ID')
    if current:
        from map_csv import format_places, csv_bytes
        candidate = root / current['path']
        ensure(current['path'] not in archived_paths, 'Current export must not overwrite historical append')
        candidate_bytes = candidate.read_bytes()
        ensure(queue and candidate_bytes == csv_bytes(format_places(places, queue), include_bom=candidate_bytes.startswith(b'\xef\xbb\xbf')), 'Current append differs from canonical queue')
        ensure(digest(candidate) == current['sha256'] and candidate.stat().st_size == current['bytes'], 'Current append hash/size drift')
        ensure(current['rows'] == len(queue), 'Current append row count drift')
        ensure(current['coordinateColumns'] == 0 and current['sourceAuditColumn'] is False, 'Unsafe current append metadata')
    ensure(current is None and sync['currentAppendStatus'] == 'no_pending_rows_do_not_upload', 'Empty queue cannot advertise an append artifact')
    for group in sync['existingUpdateGroups']:
        ensure(set(group['explicitPlaceIds']).issubset(ids), 'Unknown existing correction ID')
    geometry = load('data/map/geometry-evidence.json', root)
    ensure(geometry['completeNativeGeometryBackup'] is False, 'Unproven geometry backup claim')
    ensure(len(geometry['importedCoordinateText']) == 100 and len(geometry['displayCoordinateComparisons']) == 47, 'Geometry evidence counts')
    plan = load('data/map/coarse-category-plan.json', root)
    ensure(plan['status'] == 'proposed_not_applied' and plan['validation']['mapChangesPerformed'] == 0, 'Category proposal must not claim application')
    ensure([p['id'] for p in plan['places']] == ids, 'Category proposal canonical coverage')
    plan_counts = collections.Counter(p['presentationGroup'] for p in plan['places'])
    ensure(dict(plan_counts) == {g['id']:g['count'] for g in plan['taxonomy']['groups']}, 'Category proposal counts drift')
    known_joins = {x['placeId']:x['nativeId'] for x in joins['explicitNativeJoins']}
    for p, planned in zip(places, plan['places']):
        ensure(all(planned[k] == p[k] for k in ('id', 'name_en', 'name_ko', 'address')), 'Category proposal protected field drift')
        ensure(planned['sourceCategory'] == p['category'], 'Category proposal changed canonical category')
        ensure(planned['nativeId'] == known_joins.get(p['id']), 'Category proposal guessed native join')
        canonical_hash = hashlib.sha256(json.dumps(p, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        ensure(planned['sourceRecordSha256'] == canonical_hash, 'Category proposal source record drift')
    for item in plan['sourceFiles']:
        ensure(digest(root / item['path']) == item['sha256'], 'Category proposal source hash drift')
    return {'status': 'passed', 'places': len(places), 'sourceReferences': sum(statuses.values()), 'sourceStatuses': dict(statuses), 'coordinatePoints': point_count, 'unmeasured': len(places)-point_count, 'nativeBaseline':len(baseline),'originalAuditValues': len(original), 'pendingAppend':len(queue), 'historicallyImportedLogicalRows':len(imported), 'expectedCurrentLogicalRows':len(current_membership), 'confirmedMapRows':sync['confirmedNativeRows'], 'positionedMapRows':sync['positionedMarkers'], 'unresolvedMapRows':len(current_unresolved), 'verifiedImportedRows':sum(x['rows'] for x in operations), 'proposedCategoryGroups':len(plan_counts), 'photoAssets':len(assets), 'photoAssetBytesVerified': asset_root is not None, 'privacyFilesScanned': privacy_scan(root), 'networkRequests':0}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--asset-root', type=Path)
    args = parser.parse_args()
    try:
        result = validate(asset_root=args.asset_root)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
