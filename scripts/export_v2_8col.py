#!/usr/bin/env python3
"""Generate 8-column export CSVs from places.v2.json"""
import csv
import json
from pathlib import Path

places = json.loads(Path('data/v2/places.v2.json').read_text(encoding='utf-8'))
print(f"Total places: {len(places)}")

by_layer = {}
for p in places:
    by_layer.setdefault(p['layer'], []).append(p)

OUT = ['이름', '주소', 'Type', 'Guide', 'Details', 'Video', 'Sources', 'Record ID']
LANGS = ('en', 'ko', 'ja', 'zh', 'es')

def format_row(p):
    # Name
    name = f"{p['name'].get('en','')} | {p['name'].get('ko','')}"
    
    # Guide (5 languages)
    desc = p['description']
    guide = '\n'.join(f"{l.upper()}: {desc[l]}" for l in LANGS if desc.get(l))
    
    # Details: Only user-facing notes and practical info
    # Internal notes (region lines, reference coordinates, check dates, 
    # process notes, source notes) should stay in JSON metadata, not popups
    parts = []
    
    # Practical info
    pr = p['practical']
    labels = {'tax_refund': 'Tax refund', 'foreign_card': 'Foreign cards',
              'english_support': 'English', 'passport_booking': 'Passport booking'}
    flags = ' · '.join(f"{v}: {'Yes' if pr[k] else 'No'}" for k, v in labels.items() if pr[k] is not None)
    if flags:
        parts.append(flags)
    
    # User-facing notes only (no internal metadata)
    notes = p['notes']
    if notes.get('en'):
        parts.append(f"EN: {notes['en']}")
    if notes.get('ko'):
        parts.append(f"KO: {notes['ko']}")
    
    details = '\n'.join(parts)
    
    # Videos
    videos = '\n'.join(f"{'★Official' if v.get('official') else 'Video'} · {v.get('channel','')}: {v.get('url','')}" 
                       for v in p.get('videos', []) if v.get('url'))
    
    # Sources (URLs only, no check dates in popup)
    sources = '\n'.join([s.get('url','') for s in p.get('sources',[])[:3] if isinstance(s, dict) and s.get('url')])
    
    return {
        '이름': name,
        '주소': p['address'].get('ko', ''),
        'Type': p.get('type', ''),
        'Guide': guide,
        'Details': details,
        'Video': videos,
        'Sources': sources,
        'Record ID': p['id']
    }

base = Path('data/v2/exports/')
stats = {}
for layer, lplaces in sorted(by_layer.items()):
    csv_file = base / f'{layer}.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, OUT)
        writer.writeheader()
        writer.writerows([format_row(p) for p in lplaces])
    print(f"✓ {csv_file.name}: {len(lplaces)} rows")
    stats[layer] = {
        'rows': len(lplaces),
        'maxcell': max(len(str(v)) for r in [format_row(p) for p in lplaces] for v in r.values())
    }

# Update manifest
manifest = {
    'columns': OUT,
    'column_count': len(OUT),
    'layers': {l: {'title': {'food_drink': 'Food & Drink', 'nature_camping': 'Nature & Camping',
                             'activities_wellness': 'Activities & Wellness', 'shopping': 'Shopping',
                             'culture_sights': 'Culture & Sights'}[l], 'rows': len(by_layer[l])} 
               for l in sorted(by_layer.keys())},
    'total_rows': len(places),
    'total_cells': len(places) * len(OUT),
    'notes': 'Migrated to 8-column format on 2026-10-28. Details column combines Region, reference coordinates, and Practical information.'
}
Path('data/v2/exports/manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding='utf-8')

total_cells = len(places) * len(OUT)
print(f"\n✓ Total: {len(places)} places")
print(f"✓ Cells: {total_cells:,} / 20,000 ({100 * total_cells / 20000:.1f}%)")
print(f"✓ Row capacity: {20000 / len(OUT):.0f} rows")
print(json.dumps(stats, indent=1))
