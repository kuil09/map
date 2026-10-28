"""Test export quality - no BOM, proper encoding"""
import unittest
from pathlib import Path


class TestExportQuality(unittest.TestCase):
    """Test export CSV quality standards"""
    
    def test_exports_have_no_bom(self):
        """Exports must be UTF-8 without BOM"""
        export_dir = Path('data/v2/exports')
        csv_files = list(export_dir.glob('*.csv'))
        self.assertTrue(len(csv_files) > 0, "No CSV files found in exports")
        
        for csv_file in csv_files:
            with open(csv_file, 'rb') as f:
                first_bytes = f.read(3)
                self.assertNotEqual(
                    first_bytes, 
                    b'\xef\xbb\xbf',
                    f"{csv_file.name} has UTF-8 BOM (EF BB BF), must be BOM-free"
                )
    
    def test_exports_are_utf8(self):
        """Exports must be valid UTF-8"""
        export_dir = Path('data/v2/exports')
        for csv_file in export_dir.glob('*.csv'):
            with open(csv_file, 'r', encoding='utf-8') as f:
                # If this doesn't raise, it's valid UTF-8
                content = f.read()
                self.assertIsInstance(content, str)


if __name__ == '__main__':
    unittest.main()
