"""Offline semantic regression tests. Run: python -m unittest discover -s tests -v"""
import copy
import csv
import hashlib
import json
from pathlib import Path
import sys
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import validate
import build_site_data
import build_exports
import map_csv


class RepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.places = validate.load('data/places.json')
        cls.by_id = {p['id']: p for p in cls.places}
        cls.sync = validate.load('data/map/sync-state.json')

    def test_full_validation(self):
        self.assertEqual(validate.validate()['status'], 'passed')

    def test_v35_original_snapshot_hashes(self):
        history = validate.load('data/history/verification-history.json')
        expected = {x['logicalId']: x['sha256'] for x in history['evidenceArtifacts']}
        # This v35 migration regression intentionally fails after a new data release;
        # retain the historical hashes and replace this test with a new snapshot comparison.
        for name in ('places', 'photos', 'research'):
            self.assertEqual(validate.digest(ROOT / f'data/{name}.json'), expected[f'site-{name}-v35'])

    def test_historical_append_content_exact(self):
        with (ROOT / self.sync['appendFile']['path']).open(encoding='utf-8-sig', newline='') as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual([r['Record ID'] for r in rows], self.sync['pendingAppendPlaceIds'])
        self.assertEqual(sum(len(r['Sources'].splitlines()) for r in rows), 79)
        for row in rows:
            place = self.by_id[row['Record ID']]
            self.assertEqual(row['Address'], place['address'])
            self.assertEqual(row['Name'], place['name_en'] + ' | ' + place['name_ko'])
            expected_sources = list(dict.fromkeys([s['url'] for s in place['sources']] + ([place['operator_url']] if place.get('operator_url') else [])))
            self.assertEqual(row['Sources'].splitlines(), expected_sources)
            self.assertEqual(row['Description'], '\n\n'.join(lang.upper()+': '+place['description'][lang]+'\n'+place['notes'][lang] for lang in validate.LANGUAGES))
            self.assertNotIn('Source audit', row)
            self.assertNotIn('Latitude', row)
            self.assertNotIn('Longitude', row)

    def test_unknown_locations_stay_unknown(self):
        unknown = [p for p in self.places if p['coordinates'] is None]
        self.assertEqual(len(unknown), 515)
        self.assertTrue(all(p['radial_distance_km'] is None for p in unknown))
        pending_points = [i for i in self.sync['pendingAppendPlaceIds'] if self.by_id[i]['coordinates'] is not None]
        self.assertEqual(set(pending_points), {'culture-hongjuseong-history', 'culture-jeungpyeong-folk-museum'})

    def test_original_audit_hashes_and_join(self):
        originals = validate.load('data/history/original-source-audits296.json')
        baseline = {p['nativeId']:p for p in validate.load('data/map/baseline607.json')['records']}
        for item in originals:
            self.assertEqual(hashlib.sha256(item['originalSourceAudit'].encode('utf-8')).hexdigest(), item['valueUtf8SHA256'])
            self.assertEqual(item['recordId'], baseline[item['nativeId']]['siteRecordId'])
            self.assertEqual(item['originalSourceAudit'], baseline[item['nativeId']]['baselineFields']['Source audit'])

    def test_no_guessed_native_joins(self):
        joins = validate.load('data/map/identity-index.json')
        joined = {x['nativeId'] for x in joins['explicitNativeJoins']}
        unknown = set(joins['nativeJoinsNotEstablished'])
        self.assertEqual(len(joined), 296)
        self.assertEqual(len(unknown), 311)
        self.assertFalse(joined & unknown)

    def test_geometry_claim_is_explicitly_incomplete(self):
        geometry = validate.load('data/map/geometry-evidence.json')
        self.assertFalse(geometry['completeNativeGeometryBackup'])
        self.assertEqual(geometry['historicalKml']['historicalKmlCoordinateElements'], 0)
        self.assertFalse(geometry['historicalKml']['historicalKmlBytesMatchReceipt'])

    def test_site_build_is_exact_and_deterministic(self):
        with tempfile.TemporaryDirectory() as temp:
            first, second = Path(temp)/'one', Path(temp)/'two'
            a = build_site_data.build(first)
            b = build_site_data.build(second)
            self.assertEqual(a, b)
            self.assertFalse(a['deployed'])
            for name in ('places.json', 'photos.json', 'research.json'):
                self.assertEqual((first/name).read_bytes(), (ROOT/'data'/name).read_bytes())
                self.assertEqual((first/name).read_bytes(), (second/name).read_bytes())

    def test_site_build_rejects_canonical_or_live_like_destination(self):
        with self.assertRaises(ValueError):
            build_site_data.build(ROOT/'data')
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            (out/'index.html').write_text('existing site')
            with self.assertRaises(ValueError):
                build_site_data.build(out)
            self.assertEqual((out/'index.html').read_text(), 'existing site')

    def test_csv_generator_exact_bytes(self):
        rows = map_csv.format_places(self.places, self.sync['pendingAppendPlaceIds'])
        actual = map_csv.csv_bytes(rows)
        self.assertEqual(actual, (ROOT/self.sync['appendFile']['path']).read_bytes())
        self.assertEqual(hashlib.sha256(actual).hexdigest(), self.sync['appendFile']['sha256'])

    def test_csv_formatter_rejects_duplicate_and_missing_ids(self):
        with self.assertRaises(ValueError):
            map_csv.format_places(self.places, ['gocamping-3397','gocamping-3397'])
        with self.assertRaises(KeyError):
            map_csv.format_places(self.places, ['not-a-real-place'])

    def test_exports_are_deterministic_and_not_native_geometry(self):
        with tempfile.TemporaryDirectory() as temp:
            first, second = Path(temp)/'one', Path(temp)/'two'
            a, b = build_exports.build(first), build_exports.build(second)
            self.assertEqual(a, b)
            self.assertFalse(a['uploaded'])
            for item in a['outputs']:
                self.assertEqual((first/item['path']).read_bytes(), (second/item['path']).read_bytes())
            points = json.loads((first/'source-points-reference.geojson').read_text())
            self.assertFalse(points['nativeMapGeometry'])
            self.assertEqual(len(points['features']),127)
            self.assertEqual(points['unknownCoordinatesOmitted'],515)
            for feature in points['features']:
                place = self.by_id[feature['id']]
                self.assertEqual(feature['geometry']['coordinates'],[place['coordinates']['lng'],place['coordinates']['lat']])
            historical = json.loads((first/'historical-reconstruction607.json').read_text())
            self.assertTrue(historical['notForImport'])
            self.assertFalse(historical['nativeGeometryIncluded'])
            self.assertEqual(len(historical['records']),607)

    def test_site_manifest_does_not_attribute_dirty_data_to_head(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)/'repo'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('build','.git','__pycache__'))
            subprocess.run(['git','init','-q',str(root)],check=True)
            subprocess.run(['git','-C',str(root),'add','.'],check=True)
            subprocess.run(['git','-C',str(root),'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Fixture'],check=True)
            clean = build_site_data.build(Path(temp)/'clean', root)
            self.assertIsNotNone(clean['canonicalCommit'])
            self.assertFalse(clean['canonicalWorkingTreeDirty'])
            source = root/'data/photos.json'
            source.write_bytes(source.read_bytes()+b'\n')
            dirty = build_site_data.build(Path(temp)/'dirty', root)
            self.assertTrue(dirty['canonicalWorkingTreeDirty'])
            self.assertIsNone(dirty['canonicalCommit'])
            self.assertEqual(dirty['canonicalHead'],clean['canonicalCommit'])

    def test_public_url_checker_rejects_credentials(self):
        for value in ['https://name:password@example.org/', 'https://example.org/?' + 'access_token' + '=test-value', 'http://localhost/']:
            with self.assertRaises(ValueError):
                validate.public_url(value)
        validate.public_url('https://example.org/home/pages/location.php?id=20')


if __name__ == '__main__':
    unittest.main()
