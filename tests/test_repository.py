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

V35_COMMIT = '88c2ee5409d7c41ffe91ee6c2e2c0eb6059a2590'


def v35_bytes(path):
    # Full local Git history is required; never fetch during offline tests.
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{V35_COMMIT}:{path}'])


def record_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


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
        known = {'places':'8c3610ebaa812141ec2f40ae89a0e3289c2200f69cd2974aea2fd03088248ee6', 'photos':'43fbae7d08a8e48ce33fa4a89d72657eeb692c2f23fa7cac4b2d1e3149228475', 'research':'dfa26a5594c36b9dd56f4d9befc63991ab0896f50b3d084427048c4a268dc523'}
        for name in ('places', 'photos', 'research'):
            self.assertEqual(expected[f'site-{name}-v35'], known[name])
            self.assertEqual(hashlib.sha256(v35_bytes(f'data/{name}.json')).hexdigest(), known[name])

    def test_v36_current_snapshot_hashes(self):
        expected = {'places.json':'5ac13d79e8c646f8b2fa58ae1256cca50f1df69ffe29eb8dce3afef7c35583db', 'photos.json':'43fbae7d08a8e48ce33fa4a89d72657eeb692c2f23fa7cac4b2d1e3149228475', 'research.json':'476f6660390ab7f87615236ddddf912575ceddfea67f36eb111cb8f5d934c17e'}
        change = validate.load('data/history/batch18-change-record.json')
        self.assertEqual(change['canonicalInputHashes'], expected)
        for name, digest in expected.items():
            self.assertEqual(validate.digest(ROOT/'data'/name), digest)

    def test_historical_append_content_exact(self):
        with (ROOT / self.sync['appendFile']['path']).open(encoding='utf-8-sig', newline='') as handle:
            rows = list(csv.DictReader(handle))
        historical_sync = json.loads(v35_bytes('data/map/sync-state.json'))
        self.assertEqual([r['Record ID'] for r in rows], historical_sync['pendingAppendPlaceIds'])
        self.assertEqual([r['Record ID'] for r in rows], self.sync['pendingAppendPlaceIds'][:35])
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

    def test_batch18_exact_scope_and_preservation(self):
        before = json.loads(v35_bytes('data/places.json'))
        before_by_id = {p['id']: p for p in before}
        change = validate.load('data/history/batch18-change-record.json')
        added = change['newPlaceIds']
        edited = {p['id']: p for p in change['existingChanges']}
        self.assertEqual([p['id'] for p in self.places[:642]], [p['id'] for p in before])
        self.assertEqual([p['id'] for p in self.places[642:]], added)
        self.assertEqual(self.places[:311], before[:311])
        self.assertEqual(sum(self.by_id[p['id']] == p for p in before), 639)
        self.assertEqual(sum(len(p['sources']) for p in before), 956)
        for old in before:
            after = self.by_id[old['id']]
            self.assertEqual(after['sources'], old['sources'])
            for field in ('name_en', 'name_ko', 'address', 'description', 'checked', 'map_type'):
                self.assertEqual(after[field], old[field])
            if old['id'] not in edited:
                self.assertEqual(after, old)
                continue
            item = edited[old['id']]
            self.assertEqual(record_hash(old), item['beforeRecordSHA256'])
            self.assertEqual(record_hash(after), item['afterRecordSHA256'])
            changed = {key for key in set(old) | set(after) if old.get(key) != after.get(key)}
            self.assertEqual(changed, set(item['changedFields']))
            self.assertIsNone(old['coordinates'])
            self.assertEqual(after['coordinates'], item['after']['coordinates'])
            self.assertEqual(after['coordinate_source_url'], item['sourceURL'])
            self.assertIn(item['sourceURL'], [s['url'] for s in old['sources']])
            for lang in validate.LANGUAGES:
                self.assertTrue(after['notes'][lang].startswith(old['notes'][lang]))
        for item in change['newPlaceRecordHashes']:
            place = self.by_id[item['id']]
            self.assertEqual(record_hash(place), item['sha256'])
            self.assertIsNone(place['coordinates'])
            self.assertIsNone(place['radial_distance_km'])
        self.assertEqual(len(self.places), 645)
        self.assertEqual(sum(len(p['sources']) for p in self.places), 960)
        self.assertEqual(sum(p['coordinates'] is not None for p in self.places), 130)
        self.assertEqual(len(self.sync['pendingAppendPlaceIds']), 38)
        group = self.sync['existingUpdateGroups'][-1]
        self.assertEqual(set(group['explicitPlaceIds']), set(edited))
        self.assertEqual(group['coordinateUpdateStatus'], 'staged_not_applied_to_live_map')
        self.assertFalse(set(edited) & set(added))

    def test_historical_artifacts_and_event_prefix_unchanged(self):
        for path in ('data/photos.json', 'data/map/baseline607.json', 'data/map/geometry-evidence.json', 'data/map/identity-index.json', 'data/map/pending-field-edits692.json', 'data/map/unresolved6.json', 'data/history/original-source-audits296.json', 'data/history/applied-field-changes213.json', 'exports/map-append35-v35.csv'):
            self.assertEqual((ROOT/path).read_bytes(), v35_bytes(path), path)
        old = json.loads(v35_bytes('data/history/verification-history.json'))
        current = validate.load('data/history/verification-history.json')
        self.assertEqual(current['events'][:len(old['events'])], old['events'])
        self.assertEqual(current['evidenceArtifacts'], old['evidenceArtifacts'])
        self.assertEqual(current['additionalPreservedSourceChange'], old['additionalPreservedSourceChange'])
        old_research = json.loads(v35_bytes('data/research.json'))
        research = validate.load('data/research.json')
        for field in ('changes', 'held_candidates', 'open_questions'):
            self.assertEqual(research[field][:len(old_research[field])], old_research[field])
        for field in ('verified_utc', 'verification_scope', 'confirmed_data_rows', 'positioned_markers', 'unlocated_rows', 'legend_reorganization'):
            self.assertEqual(research['map'][field], old_research['map'][field])

    def test_batch18_public_evidence_exact_and_private_material_absent(self):
        change = validate.load('data/history/batch18-change-record.json')
        for artifact in change['publicEvidenceArtifacts']:
            self.assertEqual(validate.digest(ROOT/artifact['path']), artifact['sha256'])
        forbidden = ('batch18-existing-patches.json', 'batch18-independent-qa.json', 'batch18-private-action-ledger.json')
        for name in forbidden:
            self.assertEqual(list(ROOT.rglob(name)), [])
        holds = validate.load('data/history/batch18-new-places-holds.json')
        self.assertEqual(len(holds), 4)
        self.assertEqual(validate.load('data/metadata.json')['releaseStatus'], 'canonical_prepared_not_site_deployed')

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
        self.assertEqual(actual, (ROOT/self.sync['currentAppendFile']['path']).read_bytes())
        self.assertEqual(hashlib.sha256(actual).hexdigest(), self.sync['currentAppendFile']['sha256'])
        self.assertEqual(len(rows), 38)
        old_ids = json.loads(v35_bytes('data/map/sync-state.json'))['pendingAppendPlaceIds']
        self.assertEqual(map_csv.csv_bytes(map_csv.format_places(self.places, old_ids)), (ROOT/self.sync['appendFile']['path']).read_bytes())

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
            self.assertEqual(len(points['features']),130)
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
