#!/usr/bin/env python3
"""Offline, dependency-free canonical data and preservation checks."""
import argparse
import collections
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import sys
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
        text = path.read_text(encoding='utf-8-sig')
        for pattern in patterns:
            ensure(not re.search(pattern, text, re.I), f'Privacy review required: {path.relative_to(root)}')
        checked += 1
    return checked

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
    imported = joins['receiptBackedImportedPlaceIds']
    queue = sync['pendingAppendPlaceIds']
    ensure(len(imported) == len(set(imported)) == 607, 'Imported cohort IDs')
    ensure(len(queue) == len(set(queue)) and not set(queue) & set(imported), 'Pending IDs duplicate imported cohort')
    ensure(set(imported) | set(queue) == set(ids), 'Imported + pending does not cover canonical places')
    ensure(sync['siteTotal'] == len(places), 'Sync site count drift')
    ensure(research['map']['expected_total'] == len(places) and research['map']['remaining_map_uploads'] == len(queue), 'Research pending-map count drift')
    ensure(sync['confirmedNativeRows'] == 607 and sync['positionedMarkers'] + sync['unresolvedRows'] == 607, 'Receipt-backed map counts')
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
    if current:
        from map_csv import format_places, csv_bytes
        candidate = root / current['path']
        ensure(current['path'] != archive['path'], 'Current export must not overwrite historical append')
        ensure(candidate.read_bytes() == csv_bytes(format_places(places, queue)), 'Current append differs from canonical queue')
        ensure(digest(candidate) == current['sha256'] and candidate.stat().st_size == current['bytes'], 'Current append hash/size drift')
        ensure(current['rows'] == len(queue), 'Current append row count drift')
        ensure(current['coordinateColumns'] == 0 and current['sourceAuditColumn'] is False, 'Unsafe current append metadata')
    for group in sync['existingUpdateGroups']:
        ensure(set(group['explicitPlaceIds']).issubset(ids), 'Unknown existing correction ID')
    geometry = load('data/map/geometry-evidence.json', root)
    ensure(geometry['completeNativeGeometryBackup'] is False, 'Unproven geometry backup claim')
    ensure(len(geometry['importedCoordinateText']) == 100 and len(geometry['displayCoordinateComparisons']) == 47, 'Geometry evidence counts')
    return {'status': 'passed', 'places': len(places), 'sourceReferences': sum(statuses.values()), 'sourceStatuses': dict(statuses), 'coordinatePoints': point_count, 'unmeasured': len(places)-point_count, 'nativeBaseline':len(baseline),'originalAuditValues': len(original), 'pendingAppend':len(queue), 'photoAssets':len(assets), 'photoAssetBytesVerified': asset_root is not None, 'privacyFilesScanned': privacy_scan(root), 'networkRequests':0}

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
