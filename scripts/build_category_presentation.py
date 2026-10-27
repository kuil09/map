#!/usr/bin/env python3
"""Derive public Site data from canonical archive, explicit exclusion and purpose plans.
Does not mutate canonical records, verify Google My Maps, or deploy.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

LANGUAGES = ('en', 'ko', 'ja', 'zh', 'es')
REQUIRED_COPY = ('moreFilters', 'originalType', 'purposeLabel')
def sha(data): return hashlib.sha256(data).hexdigest()
def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def record_sha(record): return sha(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
def public_projection(root):
    root = Path(root)
    source = root / 'data/places.json'
    archive = read(source)
    policy = read(root / 'data/map/public-exclusions.json')
    assert policy['schemaVersion'] == '1.0', 'Unknown public exclusion schema'
    assert sha(source.read_bytes()) == policy['sourcePlacesSha256'], 'Public exclusion source hash is stale'
    excluded = set(policy['excludedPlaceIds'])
    assert len(excluded) == len(policy['excludedPlaceIds']) == 2, 'Explicit exclusion requires two unique IDs'
    by_id = {p['id']: p for p in archive}
    assert len(archive) == len(by_id) == policy['canonicalArchiveCount'] == 648, 'Canonical archive identity count changed'
    assert excluded <= set(by_id), 'Unknown exclusion ID'
    assert {p['id'] for p in archive if p.get('access') == 'restricted'} == excluded, 'Public exclusion/access mismatch'
    public = [p for p in archive if p['id'] not in excluded]
    assert len(public) == policy['publicCount'] == 646, 'Public projection count mismatch'
    return archive, public, policy

def generate(root):
    root = Path(root)
    plan_path = root / 'data/map/coarse-category-plan.json'
    labels_path = root / 'data/map/coarse-category-labels.json'
    places_path = root / 'data/places.json'
    plan, labels = read(plan_path), read(labels_path)
    places, public, policy = public_projection(root)
    assert plan['schemaVersion'] == labels['schemaVersion'] == '1.0', 'Schema mismatch'
    expected_sha = next(s['sha256'] for s in plan['sourceFiles'] if s['path'] == 'data/places.json')
    assert sha(places_path.read_bytes()) == expected_sha, 'Contract places hash is stale'
    assert labels['languages'] == list(LANGUAGES), 'Required five languages'
    source_groups = plan['taxonomy']['groups']
    group_ids = {g['id'] for g in source_groups}
    assert len(group_ids) == len(source_groups) == 6 and 'restricted_access' in group_ids, 'Original archived plan must remain intact'
    public_groups = group_ids - {'restricted_access'}
    assert set(labels['labels']) == public_groups, 'Labels must cover only five public purposes'
    assert set(REQUIRED_COPY) == set(labels.get('copy', {})), 'Required public UI copy keys mismatch'
    for text in [*labels['labels'].values(), *labels['copy'].values()]:
        assert set(text) == set(LANGUAGES) and all(isinstance(v, str) and v.strip() for v in text.values()), 'Missing translation'
    by_id = {p['id']: p for p in places}
    plan_by = {p['id']: p for p in plan['places']}
    assert len(by_id) == len(places) == len(plan_by) == len(plan['places']), 'Duplicate ID or incomplete assignment'
    assert set(by_id) == set(plan_by), 'Identity set mismatch'
    assignments = []
    for p in places:
        assignment = plan_by[p['id']]
        assert record_sha(p) == assignment['sourceRecordSha256'], f"Stale source record {p['id']}"
        assert p['category'] == assignment['sourceCategory'], f"Stale semantic category {p['id']}"
        purpose, group = assignment['visitorPurpose'], assignment['presentationGroup']
        assert purpose in public_groups and group in group_ids, 'Unknown group'
        assert (p.get('access') == 'restricted') == (group == 'restricted_access'), f"Access override mismatch {p['id']}"
        assert group == purpose or group == 'restricted_access', 'Nonrestricted presentation must match purpose'
        assignments.append({'id': p['id'], 'purpose': purpose, 'presentationGroup': group})
    assert dict(Counter(p['presentationGroup'] for p in assignments)) == {g['id']: g['count'] for g in source_groups}, 'Presentation counts mismatch'
    assert dict(Counter(p['purpose'] for p in assignments)) == plan['taxonomy']['countsByUnderlyingPurpose'], 'Purpose counts mismatch'
    excluded = set(policy['excludedPlaceIds'])
    assignments = [a for a in assignments if a['id'] not in excluded]
    counts = dict(Counter(a['purpose'] for a in assignments))
    assert counts == {'food_drink':127,'nature_camping':140,'activities_wellness':185,'shopping':74,'culture_sights':120}, 'Public purpose count mismatch'
    groups = [{'id': g['id'], 'labels': labels['labels'][g['id']], 'mapLabel': g['label'], 'warningOnly': False, 'count': counts[g['id']]} for g in source_groups if g['id'] in public_groups]
    return {'schemaVersion': '1.0', 'source': {'canonicalRepository': plan['canonicalRepository'], 'contractPath': 'data/map/coarse-category-plan.json', 'contractStatus': plan['status'], 'contractSha256': sha(plan_path.read_bytes()), 'canonicalArchivePlacesSha256': expected_sha, 'labelsSha256': sha(labels_path.read_bytes()), 'exclusionPolicySha256': sha((root/'data/map/public-exclusions.json').read_bytes()), 'mapVerifiedByGenerator': False, 'deployedByGenerator': False}, 'projection': {'canonicalArchiveCount':len(places),'publicCount':len(public),'excludedCount':len(excluded)}, 'groups': groups, 'copy': labels['copy'], 'assignments': assignments}

def public_research(root, public):
    """Minimal public consumer, not a rewrite of canonical research/history metadata."""
    root = Path(root)
    source = read(root/'data/research.json')
    # Read factual totals from the selected receipt, never from directory size or stale scalars.
    sync = read(root/'data/map/sync-state.json')
    receipt_path = root/sync['mapReceipt']
    receipt = read(receipt_path)
    receipt_sha = sha(receipt_path.read_bytes())
    if receipt.get('operation') == 'restore_after_layer_deletion':
        assert receipt_sha == sync['mapReceiptSHA256'], 'Current map receipt hash drift'
        assert receipt['savedReloadedCountsVerified'] is True, 'Restore counts not verified'
        verified_at = receipt['verifiedAtUtc']
    else:
        verified_at = sync['mapVerifiedAtUtc']
    counts = receipt['counts']
    map_snapshot = {'map_id':receipt['mapId'], 'confirmed_data_rows':counts['rows'],
                    'positioned_markers':counts['positioned'], 'unlocated_rows':counts['unresolved'],
                    'verified_utc':verified_at, 'checked':verified_at[:10]}
    if receipt.get('operation') == 'restore_after_layer_deletion':
        map_snapshot['restoration_status'] = receipt['status']
        map_snapshot['all_current_record_ids_freshly_verified'] = receipt['identityCoverage']['allCurrentRecordIdsFreshlyVerified']
    coverage = {}
    for p in public:
        area = coverage.setdefault(p['area'], {})
        area[p['category']] = area.get(p['category'], 0) + 1
    return {'checked':source.get('checked'), 'status':'public_projection', 'places':len(public), 'languages':source.get('languages'), 'coverage':coverage, 'category_counts':dict(Counter(p['category'] for p in public)), 'source_audit':{'places':len(public),'source_reference_statuses':dict(Counter(s.get('audit',{}).get('status','unconfirmed') for p in public for s in p['sources']))}, 'map':map_snapshot, 'provenance':{'canonicalArchivePlaces':648,'excludedCount':2,'canonicalResearchSha256':sha((root/'data/research.json').read_bytes()),'mapReceipt':sync['mapReceipt'], 'mapReceiptSha256':receipt_sha, 'mapCounts':'Saved/reloaded row totals from the selected canonical map receipt; not inferred from public directory count and not a full native-ID or exact geometry audit. Historical evidence remains unchanged in the archive.'}}

def write_json(out, name, value):
    path = Path(out)/name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return {'file':path.name,'sha256':sha(path.read_bytes()),'bytes':path.stat().st_size}

def write(out, root): return write_json(out, 'category-presentation.json', generate(root))

def write_public(out, root):
    _, public, _ = public_projection(root)
    return [write_json(out, 'places.json', public), write_json(out, 'research.json', public_research(root, public))]
