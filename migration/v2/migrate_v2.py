#!/usr/bin/env python3
"""DRAFT v1 -> v2 migration (offline only). Never touches Google My Maps or GitHub.

Usage: python3 migrate_v2.py REPO_DIR OUT_DIR [--sample N] [--final] [--kml BASELINE.kml] [--cols8]
  --cols8 forces the 8-column projection; it is also chosen automatically when rows > 1,800.
Outputs:
  places.v2.json             canonical records (rich, all languages separated)
  mymaps/<layer>.csv         lean, uniform My Maps import files (one per layer)
  migration-report.json      counts, cell budget, id coverage, warnings
The CSV is a projection: canonical truth stays in places.v2.json.
"""
import csv, json, re, sys, hashlib
from pathlib import Path

LANGS = ('en', 'ko', 'ja', 'zh', 'es')
LAYERS = {
    'food_drink': 'Food & Drink / 음식·카페',
    'nature_camping': 'Nature & Camping / 자연·캠핑',
    'activities_wellness': 'Activities & Wellness / 체험·휴식',
    'shopping': 'Shopping / 쇼핑',
    'culture_sights': 'Culture & Sights / 문화·관광',
}
# Uniform My Maps columns (11). 20,000-cell map budget => <=1,818 rows at 11 cols.
CSV_FIELDS = ['Name', 'Address', 'Latitude', 'Longitude', 'Type', 'Region',
              'Guide', 'Practical', 'Video', 'Sources', 'Record ID']
SIDO = ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시',
        '세종특별자치시', '경기도', '강원특별자치도', '충청북도', '충청남도', '전북특별자치도',
        '전라남도', '경상북도', '경상남도', '제주특별자치도']
SIDO_ALIAS = {'서울': '서울특별시', '부산': '부산광역시', '대구': '대구광역시', '인천': '인천광역시',
              '광주': '광주광역시', '대전': '대전광역시', '울산': '울산광역시', '세종': '세종특별자치시',
              '경기': '경기도', '강원도': '강원특별자치도', '강원': '강원특별자치도', '충북': '충청북도',
              '충남': '충청남도', '전라북도': '전북특별자치도', '전북': '전북특별자치도', '전남': '전라남도',
              '경북': '경상북도', '경남': '경상남도', '제주도': '제주특별자치도', '제주': '제주특별자치도'}


EN_SIDO = {'seoul': '서울특별시', 'busan': '부산광역시', 'daegu': '대구광역시', 'incheon': '인천광역시',
           'gwangju': '광주광역시', 'daejeon': '대전광역시', 'ulsan': '울산광역시', 'sejong': '세종특별자치시',
           'gyeonggi': '경기도', 'gangwon': '강원특별자치도', 'chungcheongbuk': '충청북도', 'chungbuk': '충청북도',
           'chungcheongnam': '충청남도', 'chungnam': '충청남도', 'jeollabuk': '전북특별자치도', 'jeonbuk': '전북특별자치도',
           'jeollanam': '전라남도', 'jeonnam': '전라남도', 'gyeongsangbuk': '경상북도', 'gyeongbuk': '경상북도',
           'gyeongsangnam': '경상남도', 'gyeongnam': '경상남도', 'jeju': '제주특별자치도'}
# English city -> (sido, sigungu) for addresses like "Camp Humphreys, ..., Pyeongtaek, South Korea"
EN_CITY = {'pyeongtaek': ('경기도', '평택시'), 'osan': ('경기도', '오산시'), 'daegu': ('대구광역시', None),
           'seoul': ('서울특별시', None), 'cheonan': ('충청남도', '천안시'), 'asan': ('충청남도', '아산시')}
EN_SGG = {'chungju-si': '충주시', 'pyeongtaek-si': '평택시', 'osan-si': '오산시', 'cheonan-si': '천안시'}
SINGLE_SIDO = {'세종특별자치시'}  # no sigungu tier


def region(addr, addr_en=None, area=None):
    """Return (sido, sigungu, method). sigungu keeps 2-tier names, e.g. '수원시 팔달구', '청주시 상당구'."""
    toks = re.sub(r'[,()]', ' ', addr or '').split()
    for i, t in enumerate(toks[:3]):
        sido = t if t in SIDO else SIDO_ALIAS.get(t)
        if not sido:
            continue
        rest = toks[i + 1:]
        if sido in SINGLE_SIDO or not rest:
            return sido, None, 'ko_address'
        sgg = None
        if re.search(r'(시|군|구)$', rest[0]):
            sgg = rest[0]
            if sgg.endswith('시') and len(rest) > 1 and re.search(r'(구)$', rest[1]):
                sgg += ' ' + rest[1]
        return sido, sgg, 'ko_address'
    blob = ' '.join(x for x in (addr, addr_en, area) if x).lower()
    for k, v in EN_SIDO.items():
        if re.search(r'\b' + k, blob):
            m = re.search(r'([a-z]+)-(si|gun|gu)\b', blob)
            sg = EN_SGG.get(m.group(0)) if m else None
            return v, sg, 'en_text' + ('' if sg or not m else f'(sgg_unparsed:{m.group(0)})')
    for k, (sd, sg) in EN_CITY.items():
        if re.search(r'\b' + k + r'\b', blob):
            return sd, sg, 'en_city'
    return None, None, 'unparsed'


def flag(value):
    """Tri-state flag: True / False / None(unknown). Never infer from silence."""
    if value in (True, False):
        return value
    return None


def to_v2(p, layer, videos):
    sido, sgg, rmethod = region(p.get('address'), p.get('address_en'), p.get('area'))
    c = p.get('coordinates')
    return {
        'id': p['id'],
        'schema_version': 2,
        'layer': layer,
        'type': p.get('kind') or p.get('category'),
        'legacy_category': p.get('category'),
        'name': {'en': p.get('name_en'), 'ko': p.get('name_ko')},
        'address': {'ko': p.get('address'), 'en': p.get('address_en')},
        'region': {'sido': sido, 'sigungu': sgg, 'legacy_area': p.get('area'), 'method': rmethod},
        'location': {
            'lat': c['lat'] if c else None, 'lng': c['lng'] if c else None,
            'source': p.get('coordinate_quality') or ('address_geocoded_by_mymaps' if not c else 'unknown'),
            'point_kind': 'venue' if c else None,  # venue | entrance | parking | area_centroid
            'entrance_verified': False,
            'provenance_note': p.get('coordinate_provenance') or p.get('coordinate_status'),
            'source_url': p.get('coordinate_source_url'),
        },
        'description': {l: (p.get('description') or {}).get(l) for l in LANGS},
        'notes': {l: (p.get('notes') or {}).get(l) for l in LANGS},
        'practical': {   # tri-state; only set from facility-specific evidence
            'tax_refund': None,
            'foreign_card': flag(p.get('foreign_card_payment')) if isinstance(p.get('foreign_card_payment'), bool) else None,
            'english_support': flag(p.get('english_service_verified')),
            'passport_booking': None,
            'reservation_required': None,
            'evidence': [],
        },
        'external_ids': {'kto_contentid': None, 'kto_contenttypeid': None, 'gocamping_id': None},
        'videos': videos.get(p['id'], []),
        'sources': p.get('sources', []),
        'status': {
            'operation': p.get('operation_status') or 'unverified',
            'last_verified': p.get('checked'),
            'publish': 'public',
        },
        'legacy': {k: v for k, v in p.items() if k not in {
            'id', 'name_en', 'name_ko', 'address', 'address_en', 'description', 'notes',
            'sources', 'checked', 'coordinates'}},  # nothing dropped
    }



def short(text, n):
    text = ' '.join((text or '').split())
    return text if len(text) <= n else text[:n - 1].rstrip() + '…'


CSV_FIELDS_8 = ['Name', 'Address', 'Latitude', 'Longitude', 'Guide', 'Video', 'Sources', 'Record ID']
CELL_BUDGET, ROW_SOFT_LIMIT = 20000, 1800


def to_csv_row(r, use_coords, fields):
    d, n = r['description'], r['notes']
    guide = '\n'.join(f"{l.upper()}: {d.get(l)}" for l in LANGS if d.get(l))
    pr = r['practical']
    labels = {'tax_refund': 'Tax refund', 'foreign_card': 'Foreign cards',
              'english_support': 'English', 'passport_booking': 'Passport booking'}
    practical = ' · '.join(f"{v}: {'Yes' if pr[k] else 'No'}" for k, v in labels.items() if pr[k] is not None)
    practical = (practical + '\n' if practical else '') + f"EN: {n.get('en') or ''}\nKO: {n.get('ko') or ''}"
    vids = '\n'.join(f"{'★Official' if v['official'] else 'Review'} · {v['channel']}: {v['url']}" for v in r['videos'][:2])
    srcs = '\n'.join(s['url'] for s in r['sources'][:3] if isinstance(s, dict) and s.get('url'))
    loc = r['location']
    reg = ' '.join(x for x in (r['region']['sido'], r['region']['sigungu']) if x)
    row = {
        'Name': f"{r['name']['en']} | {r['name']['ko']}",
        'Address': r['address']['ko'] or r['address']['en'] or '',
        'Latitude': f"{loc['lat']:.6f}" if use_coords else '',
        'Longitude': f"{loc['lng']:.6f}" if use_coords else '',
        'Type': r['type'] or '', 'Region': reg,
        'Guide': guide, 'Practical': practical, 'Video': vids,
        'Sources': (srcs + '\n' if srcs else '') + f"Checked {r['status']['last_verified']}",
        'Record ID': r['id'],
    }
    if fields is CSV_FIELDS_8:  # fold Type/Region into Guide header so nothing user-facing is lost
        row['Guide'] = f"[{row['Type']} · {reg}]\n" + guide
    return {k: row[k] for k in fields}


def kml_baseline(path):
    import xml.etree.ElementTree as ET
    K = '{http://www.opengis.net/kml/2.2}'
    out = {}
    for f in ET.parse(path).getroot().iter(K + 'Folder'):
        name = f.find(K + 'name').text
        for p in f.findall(K + 'Placemark'):
            rid = next(((d.find(K + 'value').text or '').strip() for d in p.iter(K + 'Data') if d.get('name') == 'Record ID'), None)
            out[rid] = {'layer_title': name, 'point': p.find('.//' + K + 'Point') is not None}
    return out


def main():
    repo, out = Path(sys.argv[1]), Path(sys.argv[2])
    sample = int(sys.argv[sys.argv.index('--sample') + 1]) if '--sample' in sys.argv else None
    places = json.loads((repo / 'data/places.json').read_text())
    plan = json.loads((repo / 'data/map/coarse-category-plan.json').read_text())
    excl = json.loads((repo / 'data/map/public-exclusions.json').read_text())
    layer_of = {p['id']: p['presentationGroup'] for p in plan['places']}
    vf = Path(__file__).with_name('videos.json')
    videos = json.loads(vf.read_text()) if vf.exists() else {}
    # Daegu 41 records live in staged history files until places.json is consolidated.
    CAT = {'dining': 'food_drink', 'food': 'food_drink', 'cafe': 'food_drink', 'camping': 'nature_camping',
           'scenery': 'nature_camping', 'activity': 'activities_wellness', 'activities': 'activities_wellness',
           'family': 'activities_wellness', 'shopping': 'shopping', 'culture': 'culture_sights',
           'temple': 'culture_sights', 'landmarks': 'culture_sights'}
    for f in sorted((repo / 'data/history').glob('daegu-places-staged-*.json')):
        d = json.loads(f.read_text())
        lst = d if isinstance(d, list) else next(v for v in d.values() if isinstance(v, list) and v and isinstance(v[0], dict) and 'id' in v[0])
        for p in lst:
            t = p.get('map_layer_target') or ''
            layer_of[p['id']] = next((k for k in LAYERS if k == t or LAYERS[k] == t), None) or CAT.get(p['id'].split('-')[0])
            places.append(p)
    v2, warn = [], []
    for p in places:
        lay = layer_of.get(p['id'])
        if lay not in LAYERS:
            warn.append({'id': p['id'], 'reason': f'non-public layer {lay}'}); continue
        v2.append(to_v2(p, lay, videos))
    if sample:
        pick, seen = [], set()
        for r in v2:  # spread sample over layers, prefer ones with coords/videos
            if (r['videos'] or len([x for x in pick if not x['videos']]) < sample - 4 and len([x for x in pick if x['layer'] == r['layer']]) < 2) and r['id'] not in seen:
                pick.append(r); seen.add(r['id'])
            if len(pick) >= sample: break
        v2 = pick
    final = '--final' in sys.argv
    base = kml_baseline(sys.argv[sys.argv.index('--kml') + 1]) if '--kml' in sys.argv else None
    total = len(v2)
    force8 = '--cols8' in sys.argv
    fields = CSV_FIELDS_8 if (force8 or total > ROW_SOFT_LIMIT) else CSV_FIELDS
    out.mkdir(parents=True, exist_ok=True)
    (out / 'places.v2.json').write_text(json.dumps(v2, ensure_ascii=False, indent=1))
    d = out / ('final' if final else 'mymaps'); d.mkdir(exist_ok=True)
    manifest = {'columns': fields, 'column_count': len(fields), 'projection': '8col' if fields is CSV_FIELDS_8 else '11col',
                'coordinate_rule': 'coords file = rows that render as KML Points on the live baseline (if --kml) else rows with repo coordinates',
                'files': [], 'layers': {}}
    warn_extra = []
    for lay, title in LAYERS.items():
        recs = [r for r in v2 if r['layer'] == lay]
        def has_xy(r):
            if r['location']['lat'] is None:
                return False
            return base[r['id']]['point'] if base and r['id'] in base else True
        groups = {'coords': [r for r in recs if has_xy(r)], 'address': [r for r in recs if not has_xy(r)]}
        manifest['layers'][lay] = {'title': title, 'rows': len(recs)}
        for kind, rs in groups.items():
            if not rs:
                continue
            fn = f'{lay}.{kind}.csv'
            rows = [to_csv_row(r, kind == 'coords', fields) for r in rs]
            for r in rows:
                if not r['Address'] and kind == 'address':
                    warn_extra.append({'id': r['Record ID'], 'reason': 'address-only row without address'})
            with open(d / fn, 'w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
            manifest['files'].append({
                'file': fn, 'layer': lay, 'layer_title': title, 'kind': kind, 'rows': len(rows),
                'cells': len(rows) * len(fields),
                'location_columns': ['Latitude', 'Longitude'] if kind == 'coords' else ['Address'],
                'sha256': hashlib.sha256((d / fn).read_bytes()).hexdigest(),
                'ids': [r['Record ID'] for r in rows]})
    cells = total * len(fields)
    region_methods = {}
    for r in v2:
        region_methods[r['region']['method']] = region_methods.get(r['region']['method'], 0) + 1
    report = {'total_rows': total, 'columns': len(fields), 'cells': cells, 'cell_budget': CELL_BUDGET,
              'cell_use_pct': round(100 * cells / CELL_BUDGET, 1), 'max_rows_at_this_width': CELL_BUDGET // len(fields),
              'rows_per_layer': {k: v['rows'] for k, v in manifest['layers'].items()},
              'unique_ids': len({r['id'] for r in v2}) == total,
              'region_methods': region_methods,
              'region_missing_sigungu': [r['id'] for r in v2 if r['region']['sido'] and not r['region']['sigungu'] and r['region']['sido'] != '세종특별자치시'],
              'region_unparsed': [r['id'] for r in v2 if not r['region']['sido']],
              'videos_attached': {r['id']: len(r['videos']) for r in v2 if r['videos']},
              'warnings': warn + warn_extra}
    if base is not None:
        ids = {r['id'] for r in v2}
        bids = set(base)
        layer_mismatch = [r['id'] for r in v2 if r['id'] in base and base[r['id']]['layer_title'] != LAYERS[r['layer']]]
        report['baseline_check'] = {'baseline_rows': len(bids), 'migrated_rows': len(ids),
                                    'missing_from_migration': sorted(bids - ids), 'extra_in_migration': sorted(ids - bids),
                                    'layer_mismatch': layer_mismatch, 'id_set_equal': ids == bids}
    assert cells <= CELL_BUDGET, 'over My Maps cell budget'
    assert all(v['rows'] <= 2000 for v in manifest['layers'].values()), 'layer >2000 rows'
    manifest['report'] = report
    (d / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    (out / 'migration-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(json.dumps({k: report[k] for k in ('total_rows', 'columns', 'cells', 'cell_use_pct', 'rows_per_layer', 'region_methods')}, ensure_ascii=False))
    print('baseline', json.dumps(report.get('baseline_check', {}), ensure_ascii=False)[:800])


if __name__ == '__main__':
    main()
