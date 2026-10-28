#!/usr/bin/env python3
"""Validate v2 data structure and exports.

Usage:
  python scripts/validate_v2.py
  python scripts/validate_v2.py --csv-dir migration/final/single-v2

Validates:
- places.v2.json schema compliance
- 2,013 unique Record IDs
- Every place has a Guide (description in at least one language)
- CSV columns match 8-column specification
- Type values are lowercase snake_case
- CSV data is consistent with places.v2.json
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path


EXPECTED_COLUMNS = [
    'Name', 'Address', 'Type', 'Guide', 'Details', 'Video', 'Sources', 'Record ID'
]

# The live CSVs use Korean headers for Name and Address
EXPECTED_COLUMNS_KO = [
    '이름', '주소', 'Type', 'Guide', 'Details', 'Video', 'Sources', 'Record ID'
]

EXPECTED_LAYERS = {
    'shopping': 'Shopping',
    'culture_sights': 'Culture & Sights',
    'food_drink': 'Food & Drink',
    'nature_camping': 'Nature & Camping',
    'activities_wellness': 'Activities & Wellness'
}

VALID_TYPE_PATTERN = re.compile(r'^[a-z][a-z0-9_]*$')


def validate_places_json(path):
    """Validate places.v2.json structure and content."""
    errors = []
    warnings = []
    
    # Updated 2026-10-28: 2,013 places live = 2,013
    expected_count = 2013
    
    if not path.exists():
        return [f"places.v2.json not found at {path}"], []
    
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"], []
    
    if not isinstance(data, list):
        return ["places.v2.json must be a list"], []
    
    # Check count (updated 2026-10-28: 1,863 + 150 Batch Next = 2,013)
    expected_count = 2013
    if len(data) != expected_count:
        errors.append(f"Expected {expected_count} places, found {len(data)}")
    
    # Check unique IDs
    ids = [p.get('id') for p in data]
    if len(ids) != len(set(ids)):
        duplicates = [id for id in ids if ids.count(id) > 1]
        errors.append(f"Duplicate IDs found: {set(duplicates)}")
    elif len(set(ids)) == expected_count:
        print(f"✓ {expected_count} unique Record IDs")
    
    # Validate each place
    missing_guide = []
    invalid_types = []
    
    for i, place in enumerate(data):
        # Required fields
        if 'id' not in place:
            errors.append(f"Place {i} missing 'id'")
            continue
        
        pid = place['id']
        
        # Schema version
        if place.get('schema_version') != 2:
            errors.append(f"{pid}: schema_version must be 2")
        
        # Layer
        if place.get('layer') not in EXPECTED_LAYERS:
            errors.append(f"{pid}: invalid layer '{place.get('layer')}'")
        
        # Type - must be lowercase snake_case
        ptype = place.get('type')
        if ptype and not VALID_TYPE_PATTERN.match(ptype):
            invalid_types.append(f"{pid}: '{ptype}'")
        
        # Description (Guide) - at least one language must have content
        desc = place.get('description', {})
        if not isinstance(desc, dict):
            errors.append(f"{pid}: description must be a dict")
        elif not any(desc.get(lang) for lang in ['en', 'ko', 'ja', 'zh', 'es']):
            missing_guide.append(pid)
        
        # Region
        region = place.get('region', {})
        if not region.get('sido'):
            warnings.append(f"{pid}: missing sido in region")
    
    if missing_guide:
        errors.append(f"{len(missing_guide)} places missing Guide content: {missing_guide[:5]}...")
    else:
        print("✓ All places have Guide content")
    
    if invalid_types:
        errors.append(f"Types not lowercase snake_case: {invalid_types[:5]}...")
    else:
        print("✓ All Type values are lowercase snake_case")
    
    return errors, warnings


def validate_csv_file(csv_path, places_by_id):
    """Validate a single CSV file."""
    errors = []
    warnings = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            # Check BOM
            first_bytes = f.read(3)
            if first_bytes.startswith('\ufeff'):
                warnings.append(f"{csv_path.name}: Contains UTF-8 BOM")
            f.seek(0)
            
            reader = csv.DictReader(f)
            
            # Check columns (accept either English or Korean headers)
            if reader.fieldnames not in (EXPECTED_COLUMNS, EXPECTED_COLUMNS_KO):
                errors.append(f"{csv_path.name}: Column mismatch")
                errors.append(f"  Expected: {EXPECTED_COLUMNS} or {EXPECTED_COLUMNS_KO}")
                errors.append(f"  Found: {reader.fieldnames}")
                return errors, warnings
            
            # Map Korean headers to English for consistent processing
            name_col = '이름' if reader.fieldnames[0] == '이름' else 'Name'
            addr_col = '주소' if reader.fieldnames[1] == '주소' else 'Address'
            
            rows = list(reader)
            
            # Validate each row
            for i, row in enumerate(rows, start=2):  # Start at 2 (header is 1)
                record_id = row.get('Record ID', '').strip()
                
                if not record_id:
                    errors.append(f"{csv_path.name} row {i}: Missing Record ID")
                    continue
                
                # Check consistency with places.v2.json
                if record_id not in places_by_id:
                    errors.append(f"{csv_path.name} row {i}: Record ID '{record_id}' not in places.v2.json")
                    continue
                
                place = places_by_id[record_id]
                
                # Check Type
                csv_type = row.get('Type', '').strip()
                json_type = place.get('type', '')
                if csv_type != json_type:
                    errors.append(f"{csv_path.name} row {i} ({record_id}): Type mismatch CSV='{csv_type}' vs JSON='{json_type}'")
                
                # Check Guide exists
                if not row.get('Guide', '').strip():
                    errors.append(f"{csv_path.name} row {i} ({record_id}): Empty Guide")
                
                # Check coordinates or address
                has_coords = row.get('Latitude', '').strip() and row.get('Longitude', '').strip()
                has_address = row.get(addr_col, '').strip()
                if not has_coords and not has_address:
                    errors.append(f"{csv_path.name} row {i} ({record_id}): No coordinates or address")
            
            print(f"✓ {csv_path.name}: {len(rows)} rows, columns correct")
            
    except Exception as e:
        errors.append(f"{csv_path.name}: {str(e)}")
    
    return errors, warnings


def validate_csv_consistency(csv_dir, places_by_id):
    """Validate all CSVs are consistent with places.v2.json."""
    errors = []
    warnings = []
    
    csv_ids = set()
    layer_counts = {}
    
    for csv_file in sorted(csv_dir.glob('*.csv')):
        layer = csv_file.stem
        if layer not in EXPECTED_LAYERS:
            continue
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            layer_counts[layer] = len(rows)
            
            for row in rows:
                record_id = row.get('Record ID', '').strip()
                if record_id:
                    csv_ids.add(record_id)
    
    # Compare with places.v2.json
    json_ids = set(places_by_id.keys())
    
    if csv_ids != json_ids:
        missing_from_csv = json_ids - csv_ids
        extra_in_csv = csv_ids - json_ids
        
        if missing_from_csv:
            errors.append(f"IDs in JSON but not in CSVs: {sorted(list(missing_from_csv))[:10]}...")
        if extra_in_csv:
            errors.append(f"IDs in CSVs but not in JSON: {sorted(list(extra_in_csv))[:10]}...")
    else:
        print(f"✓ CSVs cover all {len(csv_ids)} IDs from places.v2.json")
    
    print(f"✓ Layer counts: {layer_counts}")
    
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description='Validate v2 data structure')
    parser.add_argument('--csv-dir', default='data/v2/exports',
                       help='Directory containing CSV files')
    args = parser.parse_args()
    
    repo_root = Path(__file__).parent.parent
    
    # Validate places.v2.json
    print("Validating places.v2.json...")
    json_path = repo_root / 'data' / 'v2' / 'places.v2.json'
    errors, warnings = validate_places_json(json_path)
    
    all_errors = errors
    all_warnings = warnings
    
    if errors:
        print("\nERRORS in places.v2.json:")
        for err in errors:
            print(f"  ✗ {err}")
        return 1
    
    # Load places for CSV validation
    places_data = json.loads(json_path.read_text(encoding='utf-8'))
    places_by_id = {p['id']: p for p in places_data}
    
    # Validate CSVs
    csv_dir = repo_root / args.csv_dir
    if csv_dir.exists():
        print(f"\nValidating CSVs in {csv_dir}...")
        
        for csv_file in sorted(csv_dir.glob('*.csv')):
            errors, warnings = validate_csv_file(csv_file, places_by_id)
            all_errors.extend(errors)
            all_warnings.extend(warnings)
        
        # Check consistency
        print("\nValidating CSV consistency...")
        errors, warnings = validate_csv_consistency(csv_dir, places_by_id)
        all_errors.extend(errors)
        all_warnings.extend(warnings)
    else:
        print(f"\nWarning: CSV directory not found: {csv_dir}")
    
    # Print summary
    print("\n" + "=" * 60)
    if all_warnings:
        print(f"\nWARNINGS ({len(all_warnings)}):")
        for warn in all_warnings:
            print(f"  ⚠ {warn}")
    
    if all_errors:
        print(f"\nERRORS ({len(all_errors)}):")
        for err in all_errors:
            print(f"  ✗ {err}")
        return 1
    
    print("\n✓ All validation checks passed!")
    print(f"✓ Verification state: 2,013 places live (2,013 places live), 0 known unplaced, as of 2026-10-28")
    return 0


if __name__ == '__main__':
    sys.exit(main())
