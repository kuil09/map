"""Append-only active purposes; historical classification and exclusions stay immutable.

An optional active-classification.json covers ONLY records after the original 648.
It is a canonical input, not a map-import receipt or publication authorization.
"""
import hashlib
import json
from pathlib import Path

PLAN_PATH = 'data/map/coarse-category-plan.json'
POLICY_PATH = 'data/map/public-exclusions.json'
ACTIVE_PATH = 'data/map/active-classification.json'
PLAN_SHA256 = 'e54f265fe6ae072cef5182c7bb7ce3a4286c4a39d3adb7daeca56296a7c7efb2'
POLICY_SHA256 = 'cd0d16e964518e43d8a8a343a93c1468dd0252712962a85f973eaf176474dadc'
PUBLIC_PURPOSES = {'food_drink', 'nature_camping', 'activities_wellness', 'shopping', 'culture_sights'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def record_sha(record):
    return sha(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_classification(root, places=None):
    """Validate unchanged historical prefix and an exact, hash-bound addition overlay."""
    root = Path(root)
    places_path = root/'data/places.json'
    places = read(places_path) if places is None else places
    require(sha((root/PLAN_PATH).read_bytes()) == PLAN_SHA256, 'Historical category plan is immutable')
    require(sha((root/POLICY_PATH).read_bytes()) == POLICY_SHA256, 'Historical exclusion policy is immutable')
    plan, policy = read(root/PLAN_PATH), read(root/POLICY_PATH)
    historical = plan['places']
    historic_ids = [p['id'] for p in historical]
    ids = [p['id'] for p in places]
    require(len(ids) == len(set(ids)), 'Duplicate place ID')
    require(ids[:len(historical)] == historic_ids, 'Historical place membership/order changed')
    for place, assignment in zip(places, historical):
        require(record_sha(place) == assignment['sourceRecordSha256'], f"Historical source record changed: {place['id']}")
    # Reconstruct only the unchanged historical prefix in its recorded encoding.
    # Never repoint the historical plan/policy to the larger current JSON file.
    historic_bytes = places_path.read_bytes() if len(places) == len(historical) else (
        json.dumps(places[:len(historical)], ensure_ascii=False, indent=2)+'\n').encode('utf-8')
    for item in plan['sourceFiles']:
        actual = sha(historic_bytes) if item['path'] == 'data/places.json' else sha((root/item['path']).read_bytes())
        require(actual == item['sha256'], 'Historical category source hash drift')
    require(sha(historic_bytes) == policy['sourcePlacesSha256'], 'Historical exclusion source hash drift')
    excluded = set(policy['excludedPlaceIds'])
    require({p['id'] for p in places if p.get('access') == 'restricted'} == excluded,
            'Unapproved restricted-access record or changed historical exclusion')
    additions = places[len(historical):]
    active_path = root/ACTIVE_PATH
    if not active_path.exists():
        require(not additions, 'New places require active classification')
        return plan, policy, []
    active = read(active_path)
    require(active.get('schemaVersion') == '1.0' and active.get('status') == 'active_classification', 'Unknown active classification schema/status')
    require(active.get('canonicalRepository') == plan['canonicalRepository'], 'Active canonical repository mismatch')
    require(active.get('historicalPlanSha256') == PLAN_SHA256, 'Active historical plan hash mismatch')
    require(active.get('canonicalPlacesSha256') == sha(places_path.read_bytes()), 'Active canonical places hash is stale')
    assignments = active['assignments']
    assignment_ids = [a['id'] for a in assignments]
    require(not set(assignment_ids) & set(historic_ids), 'Active IDs collide with historical classification')
    require(len(assignment_ids) == len(set(assignment_ids)), 'Duplicate active purpose assignment')
    require(assignment_ids == [p['id'] for p in additions], 'Missing, extra or reordered active purpose assignments')
    for place, assignment in zip(additions, assignments):
        ident = place['id']
        require(place.get('access') == 'public', f'{ident}: additions require explicit public access classification')
        require(assignment.get('sourceRecordSha256') == record_sha(place), f'{ident}: stale active source record hash')
        require(assignment.get('sourceCategory') == place['category'], f'{ident}: stale active semantic category')
        require(assignment.get('visitorPurpose') in PUBLIC_PURPOSES, f'{ident}: unknown public purpose')
        require(assignment.get('presentationGroup') == assignment['visitorPurpose'], f'{ident}: non-public presentation group')
        require(assignment.get('nativeId') is None, f'{ident}: unverified new native ID')
        # First additions are venue information, not independently verified entrances.
        require(place.get('entrance_verification') == 'unverified', f'{ident}: unsupported entrance verification')
        require('distance_reference_id' in place, f'{ident}: missing explicit distance reference')
        if place['radial_distance_km'] is None:
            require(place.get('distance_kind') == 'unmeasured' and place['distance_reference_id'] is None,
                    f'{ident}: unknown distance must remain explicitly unmeasured')
        else:
            require(place['coordinates'] is not None and place.get('distance_kind') == 'straight_line' and place['distance_reference_id'],
                    f'{ident}: measured distance must identify straight-line reference')
        if place['coordinates'] is not None:
            require(place.get('coordinate_provenance') and place.get('coordinate_source_url'),
                    f'{ident}: missing coordinate provenance/source')
            sources = [s for s in place['sources'] if s['url'] == place['coordinate_source_url']]
            require(sources and any(s.get('audit', {}).get('status') == 'verified' and
                                    s.get('audit', {}).get('scope') == 'exact' for s in sources),
                    f'{ident}: coordinate source requires verified exact evidence')
    return plan, policy, assignments
