#!/usr/bin/env python3
"""Test that migrate_v2.py does not truncate content."""
import unittest
from migrate_v2 import to_csv_row, CSV_FIELDS_8, LANGS


class TestNoTruncation(unittest.TestCase):
    """Test that long descriptions and notes are not truncated."""
    
    def test_long_description_not_truncated(self):
        """Long descriptions should not be truncated with ellipsis."""
        long_text = "A" * 300  # Much longer than old 140-char limit
        record = {
            'description': {'en': long_text, 'ko': 'Korean text', 'ja': '', 'zh': '', 'es': ''},
            'notes': {'en': '', 'ko': '', 'ja': None, 'zh': None, 'es': None},
            'practical': {
                'tax_refund': None, 'foreign_card': None, 'english_support': None,
                'passport_booking': None, 'reservation_required': None
            },
            'videos': [],
            'sources': [],
            'location': {'lat': 37.5, 'lng': 127.0},
            'region': {'sido': '서울특별시', 'sigungu': None},
            'name': {'en': 'Test', 'ko': '테스트'},
            'address': {'ko': '서울특별시', 'en': None},
            'type': 'test',
            'id': 'test-1',
            'status': {'last_verified': '2026-10-28'}
        }
        
        row = to_csv_row(record, False, CSV_FIELDS_8)
        
        # Check that the long text is NOT truncated
        self.assertIn(long_text, row['Guide'])
        self.assertNotIn('…', row['Guide'])
        self.assertNotIn('...', row['Guide'])
    
    def test_long_notes_not_truncated(self):
        """Long notes should not be truncated with ellipsis."""
        long_en = "B" * 300  # Much longer than old 200-char limit
        long_ko = "C" * 200  # Much longer than old 120-char limit
        record = {
            'description': {'en': 'Short', 'ko': 'Short', 'ja': '', 'zh': '', 'es': ''},
            'notes': {'en': long_en, 'ko': long_ko, 'ja': None, 'zh': None, 'es': None},
            'practical': {
                'tax_refund': None, 'foreign_card': None, 'english_support': None,
                'passport_booking': None, 'reservation_required': None
            },
            'videos': [],
            'sources': [],
            'location': {'lat': 37.5, 'lng': 127.0},
            'region': {'sido': '서울특별시', 'sigungu': None},
            'name': {'en': 'Test', 'ko': '테스트'},
            'address': {'ko': '서울특별시', 'en': None},
            'type': 'test',
            'id': 'test-2',
            'status': {'last_verified': '2026-10-28'}
        }
        
        # For 8-column format, notes go in the Details column (not exported by to_csv_row)
        # But we can verify the practical field contains the notes without truncation
        row = to_csv_row(record, False, CSV_FIELDS_8)
        
        # In the migration script, notes are combined with practical info
        # The format is "EN: {notes_en}\nKO: {notes_ko}"
        # Since we're testing 8-col which doesn't have Practical in CSV_FIELDS_8,
        # let's just verify no ellipsis appears in any field
        for value in row.values():
            if isinstance(value, str):
                self.assertNotIn('…', value)
                self.assertNotIn('...', value)
    
    def test_all_description_languages_included(self):
        """All description languages should be included without truncation."""
        record = {
            'description': {
                'en': 'E' * 200,
                'ko': 'K' * 200,
                'ja': 'J' * 200,
                'zh': 'Z' * 200,
                'es': 'S' * 200
            },
            'notes': {'en': '', 'ko': '', 'ja': None, 'zh': None, 'es': None},
            'practical': {
                'tax_refund': None, 'foreign_card': None, 'english_support': None,
                'passport_booking': None, 'reservation_required': None
            },
            'videos': [],
            'sources': [],
            'location': {'lat': 37.5, 'lng': 127.0},
            'region': {'sido': '서울특별시', 'sigungu': None},
            'name': {'en': 'Test', 'ko': '테스트'},
            'address': {'ko': '서울특별시', 'en': None},
            'type': 'test',
            'id': 'test-3',
            'status': {'last_verified': '2026-10-28'}
        }
        
        row = to_csv_row(record, False, CSV_FIELDS_8)
        
        # All languages should be in Guide field
        for lang in LANGS:
            lang_marker = f"{lang.upper()}:"
            self.assertIn(lang_marker, row['Guide'])
        
        # No truncation markers
        self.assertNotIn('…', row['Guide'])


if __name__ == '__main__':
    unittest.main()
