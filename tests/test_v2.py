#!/usr/bin/env python3
"""Tests for v2 data structure."""
import json
import unittest
from pathlib import Path


class TestV2DataStructure(unittest.TestCase):
    """Test v2 places.json and export consistency."""
    
    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).parent.parent
        cls.places_path = cls.repo_root / 'data' / 'v2' / 'places.v2.json'
        cls.places = json.loads(cls.places_path.read_text(encoding='utf-8'))
    
    def test_total_places_count(self):
        """1,565 places total (1,414 + 151 Seoul/Incheon)."""
        self.assertEqual(len(self.places), 1565)
    
    def test_unique_ids(self):
        """All Record IDs are unique."""
        ids = [p['id'] for p in self.places]
        self.assertEqual(len(ids), len(set(ids)))
    
    def test_schema_version(self):
        """All places have schema_version 2."""
        for place in self.places:
            self.assertEqual(place.get('schema_version'), 2)
    
    def test_type_format(self):
        """All types are lowercase snake_case."""
        import re
        pattern = re.compile(r'^[a-z][a-z0-9_]*$')
        for place in self.places:
            ptype = place.get('type')
            if ptype:
                self.assertRegex(ptype, pattern,
                               f"{place['id']}: type '{ptype}' not lowercase_snake_case")
    
    def test_guide_content(self):
        """Every place has description content in at least one language."""
        for place in self.places:
            desc = place.get('description', {})
            has_content = any(desc.get(lang) for lang in ['en', 'ko', 'ja', 'zh', 'es'])
            self.assertTrue(has_content,
                          f"{place['id']}: no description in any language")
    
    def test_layer_distribution(self):
        """Layer distribution matches expected counts (updated 2026-10-28)."""
        expected = {
            'food_drink': 343,
            'nature_camping': 372,
            'activities_wellness': 314,
            'shopping': 166,
            'culture_sights': 370,
        }
        actual = {}
        for place in self.places:
            layer = place.get('layer')
            actual[layer] = actual.get(layer, 0) + 1
        
        self.assertEqual(actual, expected)
    
    def test_nongdari_address(self):
        """농다리캠핑장 uses lot address."""
        place = next(p for p in self.places if p['id'] == 'gocamping-101667')
        self.assertEqual(place['address']['ko'], '충청북도 진천군 문백면 평산리 543')
    
    def test_region_structure(self):
        """All places have region.sido."""
        for place in self.places:
            region = place.get('region', {})
            sido = region.get('sido')
            self.assertTrue(sido, f"{place['id']}: missing sido")


class TestV2ExportConsistency(unittest.TestCase):
    """Test CSV exports match places.v2.json."""
    
    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).parent.parent
        cls.places_path = cls.repo_root / 'data' / 'v2' / 'places.v2.json'
        cls.csv_dir = cls.repo_root / 'data' / 'v2' / 'exports'
        
        if cls.places_path.exists():
            cls.places = json.loads(cls.places_path.read_text(encoding='utf-8'))
            cls.places_by_id = {p['id']: p for p in cls.places}
        else:
            cls.places = []
            cls.places_by_id = {}
    
    def test_csv_files_exist(self):
        """All 5 layer CSV files exist."""
        if not self.csv_dir.exists():
            self.skipTest("CSV directory not found")
        
        for layer in ['food_drink', 'nature_camping', 'activities_wellness', 
                     'shopping', 'culture_sights']:
            csv_path = self.csv_dir / f'{layer}.csv'
            self.assertTrue(csv_path.exists(), f"{csv_path.name} not found")
    
    def test_csv_covers_all_ids(self):
        """CSVs cover all IDs from places.v2.json."""
        if not self.csv_dir.exists():
            self.skipTest("CSV directory not found")
        
        import csv
        csv_ids = set()
        
        for csv_file in self.csv_dir.glob('*.csv'):
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    record_id = row.get('Record ID', '').strip()
                    if record_id:
                        csv_ids.add(record_id)
        
        json_ids = set(self.places_by_id.keys())
        self.assertEqual(csv_ids, json_ids)


if __name__ == '__main__':
    unittest.main()
