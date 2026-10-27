#!/usr/bin/env python3
"""Deterministic offline exports. No upload, map mutation, geocoding or network."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from validate import ROOT, load, validate
from map_csv import format_places, csv_bytes


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def reconstruct(root=ROOT):
    records = copy.deepcopy(load('data/map/baseline607.json', root)['records'])
    by_id = {p['nativeId']: p for p in records}
    changes = load('data/history/applied-field-changes213.json', root)
    extra = load('data/history/verification-history.json', root)['additionalPreservedSourceChange']
    for change in changes + extra:
        by_id[change['nativeId']]['baselineFields'][change['field']] = change['after']
    return {'status':'DERIVED historical baseline plus 213 recorded successful field edits and one source-URL preservation change. Not a fresh readback, not a live import file.', 'notForImport':True, 'nativeGeometryIncluded':False, 'records':records}


def build(out, root=ROOT):
    out = Path(out).resolve()
    if out == root or any(out == root / d or root / d in out.parents for d in ('data','docs','scripts','tests','schemas','exports')):
        raise ValueError('Output must be staging, not canonical data or historical evidence.')
    if any((out / name).exists() for name in ('index.html','app.js','.git')):
        raise ValueError('Refusing an existing Site/document-root checkout.')
    validate(root)
    out.mkdir(parents=True, exist_ok=True)
    places = load('data/places.json', root)
    sync = load('data/map/sync-state.json', root)
    rows = format_places(places, sync['pendingAppendPlaceIds'])
    data = csv_bytes(rows)
    # A zero-row CSV is not an import candidate. Remove only our known stale
    # staging outputs so a previous nonempty export cannot be mistaken for work.
    if rows:
        (out / 'map-append-current.csv').write_bytes(data)
        write_json(out / 'map-append-current.rows.json', rows)
    else:
        for name in ('map-append-current.csv', 'map-append-current.rows.json'):
            (out / name).unlink(missing_ok=True)
    write_json(out / 'historical-reconstruction607.json', reconstruct(root))
    features = []
    for place in places:
        if place['coordinates'] is None:
            continue
        point = place['coordinates']
        features.append({'type':'Feature','id':place['id'],'geometry':{'type':'Point','coordinates':[point['lng'],point['lat']]},'properties':{'id':place['id'],'name_en':place['name_en'],'name_ko':place['name_ko'],'address':place['address'],'coordinate_source_url':place['coordinate_source_url'],'coordinate_provenance':place['coordinate_provenance'],'coordinate_status':place['coordinate_status'],'radial_distance_km':place['radial_distance_km'],'distance_reference_id':place['distance_reference_id'],'scope':'Published source reference point only; not native Google marker geometry or a verified entrance.'}})
    write_json(out / 'source-points-reference.geojson', {'type':'FeatureCollection','name':'Published source reference points — NOT a native map backup','nativeMapGeometry':False,'unknownCoordinatesOmitted':len(places)-len(features),'features':features})
    manifest = {'canonicalRepository':'https://github.com/kuil09/map','snapshotRelease':load('data/metadata.json', root)['snapshotRelease'],'inputs':{str(p):hashlib.sha256((root/p).read_bytes()).hexdigest() for p in ['data/places.json','data/map/sync-state.json','data/map/baseline607.json','data/history/applied-field-changes213.json','data/history/verification-history.json']},'appendRows':len(rows),'addressBasedImport':True,'coordinateColumns':0,'sourceAuditColumn':False,'uploaded':False,'outputs':[]}
    manifest['appendStatus'] = 'pending_rows_not_authorized_for_upload' if rows else 'no_pending_rows_do_not_upload'
    manifest['importable'] = bool(rows)
    manifest['uploadAuthorized'] = False
    manifest['csvEncoding'] = 'utf-8'
    manifest['csvByteOrderMark'] = False
    output_names = (['map-append-current.csv', 'map-append-current.rows.json'] if rows else []) + ['historical-reconstruction607.json', 'source-points-reference.geojson']
    for name in output_names:
        path = out / name
        manifest['outputs'].append({'path':name,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    write_json(out / 'export-manifest.json', manifest)
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.out), ensure_ascii=False, indent=2))
