"""Offline semantic regression tests. Run: python -m unittest discover -s tests -v"""
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import shutil
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import validate
import build_site_data
import build_exports
import map_csv

V35_COMMIT = '88c2ee5409d7c41ffe91ee6c2e2c0eb6059a2590'
V36_COMMIT = 'd7f722845fef1ef178cf3ff8768f55e504092678'
V37_COMMIT = 'a1630b40ba030b85e05113f2e04ba960d2404ef9'
INTEGRATION_BASE = 'a1fc07a6dd24b595ba1e99df8edb25fe49e00199'


def v35_bytes(path):
    # Full local Git history is required; never fetch during offline tests.
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{V35_COMMIT}:{path}'])


def v36_bytes(path):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{V36_COMMIT}:{path}'])


def v37_bytes(path):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{V37_COMMIT}:{path}'])


def record_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


class RepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.places = validate.load('data/places.json')
        cls.by_id = {p['id']: p for p in cls.places}
        cls.sync = validate.load('data/map/sync-state.json')
        cls.operation = validate.load('data/map/verified-import-history.json')['completedAppendOperations'][0]
        cls.append_ids = cls.operation['placeIds']
        cls.original_append = cls.operation['originalArtifact']

    def test_kmz_privacy_scan_inspects_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / 'test.kmz'
            with zipfile.ZipFile(package, 'w') as archive:
                archive.writestr('doc.kml', '<kml>public place</kml>')
            self.assertEqual(validate.privacy_scan(root), 1)
            with zipfile.ZipFile(package, 'w') as archive:
                archive.writestr('doc.kml', '<kml>' + '/Users/' + 'private/files/' + '</kml>')
            with self.assertRaises(ValueError):
                validate.privacy_scan(root)
            with zipfile.ZipFile(package, 'w') as archive:
                archive.writestr('../doc.kml', '<kml/>')
            with self.assertRaises(ValueError):
                validate.privacy_scan(root)

    def test_full_validation(self):
        self.assertEqual(validate.validate()['status'], 'passed')

    def test_v35_original_snapshot_hashes(self):
        history = validate.load('data/history/verification-history.json')
        expected = {x['logicalId']: x['sha256'] for x in history['evidenceArtifacts']}
        known = {'places':'8c3610ebaa812141ec2f40ae89a0e3289c2200f69cd2974aea2fd03088248ee6', 'photos':'43fbae7d08a8e48ce33fa4a89d72657eeb692c2f23fa7cac4b2d1e3149228475', 'research':'dfa26a5594c36b9dd56f4d9befc63991ab0896f50b3d084427048c4a268dc523'}
        for name in ('places', 'photos', 'research'):
            self.assertEqual(expected[f'site-{name}-v35'], known[name])
            self.assertEqual(hashlib.sha256(v35_bytes(f'data/{name}.json')).hexdigest(), known[name])

    def test_v36_historical_snapshot_hashes(self):
        expected = {'places.json':'5ac13d79e8c646f8b2fa58ae1256cca50f1df69ffe29eb8dce3afef7c35583db', 'photos.json':'43fbae7d08a8e48ce33fa4a89d72657eeb692c2f23fa7cac4b2d1e3149228475', 'research.json':'476f6660390ab7f87615236ddddf912575ceddfea67f36eb111cb8f5d934c17e'}
        change = validate.load('data/history/batch18-change-record.json')
        self.assertEqual(change['canonicalInputHashes'], expected)
        for name, digest in expected.items():
            self.assertEqual(hashlib.sha256(v36_bytes('data/'+name)).hexdigest(), digest)

    def test_historical_append_content_exact(self):
        with (ROOT / self.sync['appendFile']['path']).open(encoding='utf-8-sig', newline='') as handle:
            rows = list(csv.DictReader(handle))
        historical_sync = json.loads(v35_bytes('data/map/sync-state.json'))
        self.assertEqual([r['Record ID'] for r in rows], historical_sync['pendingAppendPlaceIds'])
        self.assertEqual([r['Record ID'] for r in rows], self.append_ids[:35])
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
        self.assertEqual(len(unknown), 518)
        self.assertTrue(all(p['radial_distance_km'] is None for p in unknown))
        pending_points = [i for i in self.append_ids if self.by_id[i]['coordinates'] is not None]
        self.assertEqual(set(pending_points), {'culture-hongjuseong-history', 'culture-jeungpyeong-folk-museum'})

    def test_batch18_exact_scope_and_preservation(self):
        historical_places = json.loads(v36_bytes('data/places.json'))
        historical_by_id = {p['id']: p for p in historical_places}
        historical_sync = json.loads(v36_bytes('data/map/sync-state.json'))
        before = json.loads(v35_bytes('data/places.json'))
        before_by_id = {p['id']: p for p in before}
        change = validate.load('data/history/batch18-change-record.json')
        added = change['newPlaceIds']
        edited = {p['id']: p for p in change['existingChanges']}
        self.assertEqual([p['id'] for p in historical_places[:642]], [p['id'] for p in before])
        self.assertEqual([p['id'] for p in historical_places[642:]], added)
        self.assertEqual(historical_places[:311], before[:311])
        self.assertEqual(sum(historical_by_id[p['id']] == p for p in before), 639)
        self.assertEqual(sum(len(p['sources']) for p in before), 956)
        for old in before:
            after = historical_by_id[old['id']]
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
            place = historical_by_id[item['id']]
            self.assertEqual(record_hash(place), item['sha256'])
            self.assertIsNone(place['coordinates'])
            self.assertIsNone(place['radial_distance_km'])
        self.assertEqual(len(historical_places), 645)
        self.assertEqual(sum(len(p['sources']) for p in historical_places), 960)
        self.assertEqual(sum(p['coordinates'] is not None for p in historical_places), 130)
        self.assertEqual(len(historical_sync['pendingAppendPlaceIds']), 38)
        group = historical_sync['existingUpdateGroups'][-1]
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
            self.assertEqual(validate.load('data/history/map-status-v37-before-append41.json')[field], old_research['map'][field])

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

    def test_v37_historical_snapshot_hashes(self):
        change = validate.load('data/history/batch19-change-record.json')
        expected = {'places.json':'a599f6e6cbe8bb59e2f545664b56a6a57dea29983b05b9dbeb6dc42004de347c', 'photos.json':'43fbae7d08a8e48ce33fa4a89d72657eeb692c2f23fa7cac4b2d1e3149228475', 'research.json':'fbbe5b133bdfdfcca25c49fabc21bf0ae0e1db09fdc6475256ec119484a46e7a'}
        self.assertEqual(change['canonicalInputHashes'], expected)
        for name, digest in expected.items():
            self.assertEqual(hashlib.sha256(v37_bytes('data/'+name)).hexdigest(), digest)
            if name != 'research.json':
                self.assertEqual(validate.digest(ROOT/'data'/name), digest)

    def test_batch19_exact_scope_and_preservation(self):
        before = json.loads(v36_bytes('data/places.json'))
        change = validate.load('data/history/batch19-change-record.json')
        edited = {p['id']:p for p in change['existingChanges']}
        self.assertEqual(len(self.places), 648)
        self.assertEqual(sum(len(p['sources']) for p in self.places), 970)
        self.assertEqual(sum(p['coordinates'] is not None for p in self.places), 130)
        self.assertEqual(self.places[:311], before[:311])
        self.assertEqual([p['id'] for p in self.places[:645]], [p['id'] for p in before])
        self.assertEqual([p['id'] for p in self.places[645:]], change['newPlaceIds'])
        self.assertEqual(sum(self.by_id[p['id']] == p for p in before), 643)
        self.assertEqual(sum(len(p['sources']) for p in before), 960)
        self.assertEqual(set(edited), {'gocamping-6865', 'gocamping-2022'})
        for old in before:
            after = self.by_id[old['id']]
            self.assertEqual(after['sources'][:len(old['sources'])], old['sources'])
            for field in ('name_en', 'name_ko', 'description', 'checked', 'map_type', 'coordinates', 'radial_distance_km'):
                self.assertEqual(after[field], old[field])
            if old['id'] not in edited:
                self.assertEqual(after, old)
                continue
            item = edited[old['id']]
            self.assertEqual(record_hash(old), item['beforeRecordSHA256'])
            self.assertEqual(record_hash(after), item['afterRecordSHA256'])
            self.assertEqual({key for key in set(old)|set(after) if old.get(key) != after.get(key)}, set(item['changedFields']))
            self.assertEqual(len(after['sources']), len(old['sources'])+1)
            self.assertIsNone(after['coordinates'])
            self.assertIsNone(after['radial_distance_km'])
            self.assertFalse(item['liveMapApplied'])
            for lang in validate.LANGUAGES:
                self.assertTrue(after['notes'][lang].startswith(old['notes'][lang]))
        for item in change['newPlaceRecordHashes']:
            place = self.by_id[item['id']]
            self.assertEqual(record_hash(place), item['sha256'])
            self.assertIsNone(place['coordinates'])
            self.assertIsNone(place['radial_distance_km'])
        self.assertEqual(len(json.loads(v37_bytes('data/map/sync-state.json'))['pendingAppendPlaceIds']), 41)
        self.assertEqual(self.sync['pendingAppendPlaceIds'], [])
        self.assertEqual(set(self.sync['existingUpdateGroups'][-1]['explicitPlaceIds']), set(edited))
        self.assertFalse(set(edited) & set(self.append_ids))
        self.assertEqual(self.sync['existingUpdateGroups'][-1]['addressUpdateStatus'], 'canonical_only_not_applied_to_live_map')

    def test_batch19_address_and_dated_maintenance_scope(self):
        before = {p['id']:p for p in json.loads(v36_bytes('data/places.json'))}
        wangsong = self.by_id['gocamping-6865']
        self.assertEqual(wangsong['address'], '경기도 의왕시 왕송못동로 295 (월암동, 왕송호수캠핑장 매표소)')
        for lang in validate.LANGUAGES:
            suffix = wangsong['notes'][lang][len(before[wangsong['id']]['notes'][lang]):]
            self.assertIn('571', suffix)
            self.assertIn('295', suffix)
        hwarang = self.by_id['gocamping-2022']
        self.assertEqual(hwarang['address'], before[hwarang['id']]['address'])
        en = hwarang['notes']['en']
        self.assertIn('2026-11-09–13', en)
        self.assertIn('does not state a full-site closure', en)
        self.assertNotIn('2026-10-19', en)
        self.assertNotIn('rear-gate', en)

    def test_v36_history_and_append38_remain_immutable(self):
        for path in ('data/history/batch18-change-record.json', 'data/history/batch18-existing-audit.json', 'data/history/batch18-new-places-audit.json', 'data/history/batch18-new-places-evidence.json', 'data/history/batch18-new-places-holds.json', 'data/history/site-deployment-v36.json', 'exports/map-append38-v36.csv'):
            self.assertEqual((ROOT/path).read_bytes(), v36_bytes(path), path)
        old_sync = json.loads(v36_bytes('data/map/sync-state.json'))
        self.assertEqual(self.sync['archivedAppendFiles'][0], old_sync['currentAppendFile'])
        self.assertEqual(self.sync['appendAttemptHistory'][0], old_sync['lastAppendAttempt'])
        self.assertEqual(self.sync['appendFile'], old_sync['appendFile'])
        self.assertEqual(self.append_ids[:38], old_sync['pendingAppendPlaceIds'])
        old_places = json.loads(v36_bytes('data/places.json'))
        self.assertEqual(map_csv.csv_bytes(map_csv.format_places(old_places, old_sync['pendingAppendPlaceIds']), include_bom=True), v36_bytes('exports/map-append38-v36.csv'))
        history = validate.load('data/history/verification-history.json')
        old_history = json.loads(v36_bytes('data/history/verification-history.json'))
        self.assertEqual(history['events'][:len(old_history['events'])], old_history['events'])
        for field in ('evidenceArtifacts', 'additionalPreservedSourceChange', 'excludedFailedEdits', 'historyLimits'):
            self.assertEqual(history[field], old_history[field])
        research = validate.load('data/research.json')
        old_research = json.loads(v36_bytes('data/research.json'))
        for field in ('changes', 'held_candidates', 'open_questions'):
            self.assertEqual(research[field][:len(old_research[field])], old_research[field])
        for field in ('verified_utc', 'verification_scope', 'confirmed_data_rows', 'positioned_markers', 'unlocated_rows', 'legend_reorganization'):
            self.assertEqual(validate.load('data/history/map-status-v37-before-append41.json')[field], old_research['map'][field])

    def test_batch19_public_evidence_and_no_private_artifacts(self):
        change = validate.load('data/history/batch19-change-record.json')
        self.assertEqual(len(change['publicEvidenceArtifacts']), 4)
        for artifact in change['publicEvidenceArtifacts']:
            self.assertEqual(validate.digest(ROOT/artifact['path']), artifact['sha256'])
        for name in ('batch19-existing-patches.json', 'batch19-independent-qa.json', 'batch19-private-action-ledger.json', 'batch19-private-source-snapshots.json'):
            self.assertEqual(list(ROOT.rglob(name)), [])
        self.assertEqual(validate.load('data/metadata.json')['lastPublishedSiteRelease'], 'v37')
        self.assertEqual(validate.load('data/metadata.json')['releaseStatus'], 'canonical_prepared_not_site_deployed')
        self.assertEqual(validate.load('data/history/verification-history.json')['currentSiteRelease'], 'v37')

    def test_latest_append_receipt_supersedes_preserved_failure(self):
        failure = self.sync['appendAttemptHistory'][-1]
        self.assertEqual(failure, json.loads(v37_bytes('data/map/sync-state.json'))['lastAppendAttempt'])
        self.assertEqual((failure['rows'], failure['status'], failure['confirmedWrites'], failure['uncertainWrites']), (38, 'failed_before_upload', 0, 0))
        self.assertFalse(failure['currentFreshInventoryVerified'])
        attempt = self.sync['lastAppendAttempt']
        self.assertEqual((attempt['rows'], attempt['status'], attempt['successfulOperations'], attempt['duplicateAppends']), (41, 'saved_reloaded_verified', 1, 0))
        self.assertIsNone(attempt['exactAppendSaveAtUtc'])
        self.assertFalse(attempt['nativeIdsExposed'])
        self.assertEqual((self.sync['confirmedNativeRows'], self.sync['positionedMarkers'], self.sync['unresolvedRows']), (648, 641, 7))
        self.assertIsNone(self.sync['currentAppendFile'])
        self.assertEqual(self.sync['pendingAppendPlaceIds'], [])
        self.assertEqual(self.sync['pendingCohorts'], [])
        self.assertEqual(self.sync['currentAppendStatus'], 'no_pending_rows_do_not_upload')
        self.assertEqual(self.sync['archivedAppendFiles'][-1], self.original_append)

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

    def test_site_build_is_explicit_public_projection_and_deterministic(self):
        from build_category_presentation import public_projection, generate, public_research
        before = {name:(ROOT/'data'/name).read_bytes() for name in ('places.json','photos.json','research.json','metadata.json')}
        archive, public, policy = public_projection(ROOT)
        self.assertEqual(len(archive), 648)
        self.assertEqual(len(public), 646)
        self.assertEqual({p['id'] for p in archive} - {p['id'] for p in public}, set(policy['excludedPlaceIds']))
        self.assertTrue(all(p in archive for p in public))
        with tempfile.TemporaryDirectory() as temp:
            first, second = Path(temp)/'one', Path(temp)/'two'
            a = build_site_data.build(first)
            b = build_site_data.build(second)
            self.assertEqual(a, b)
            self.assertFalse(a['deployed'])
            self.assertEqual(json.loads((first/'places.json').read_text()), public)
            self.assertEqual(json.loads((first/'research.json').read_text()), public_research(ROOT, public))
            presentation = json.loads((first/'category-presentation.json').read_text())
            self.assertEqual(presentation, generate(ROOT))
            self.assertEqual([g['count'] for g in presentation['groups']], [127,140,185,74,120])
            self.assertEqual(len(presentation['assignments']), 646)
            self.assertEqual((first/'photos.json').read_bytes(), before['photos.json'])
            for name in ('places.json','photos.json','research.json','category-presentation.json','canonical-input-manifest.json'):
                self.assertEqual((first/name).read_bytes(), (second/name).read_bytes())
                for excluded in policy['excludedPlaceIds']:
                    self.assertNotIn(excluded, (first/name).read_text())
        for name, raw in before.items():
            self.assertEqual((ROOT/'data'/name).read_bytes(), raw)

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
        rows = map_csv.format_places(self.places, self.append_ids)
        actual = map_csv.csv_bytes(rows)
        historical = (ROOT/self.original_append['path']).read_bytes()
        self.assertTrue(historical.startswith(b'\xef\xbb\xbf'))
        self.assertEqual(actual, historical[3:])
        self.assertEqual(map_csv.csv_bytes(rows, include_bom=True), historical)
        self.assertEqual(hashlib.sha256(historical).hexdigest(), self.original_append['sha256'])
        self.assertEqual(len(rows), 41)
        old_ids = json.loads(v35_bytes('data/map/sync-state.json'))['pendingAppendPlaceIds']
        self.assertEqual(map_csv.csv_bytes(map_csv.format_places(self.places, old_ids), include_bom=True), (ROOT/self.sync['appendFile']['path']).read_bytes())

    def test_csv_header_is_exact_and_bom_free_with_plain_utf8_reader(self):
        rows = map_csv.format_places(self.places, self.append_ids)
        actual = map_csv.csv_bytes(rows)
        header = (','.join('"' + field + '"' for field in map_csv.FIELDS) + '\r\n').encode('ascii')
        self.assertTrue(actual.startswith(header))
        self.assertFalse(actual.startswith(b'\xef\xbb\xbf'))
        reader = csv.DictReader(io.StringIO(actual.decode('utf-8'), newline=''), strict=True)
        self.assertEqual(reader.fieldnames, map_csv.FIELDS)
        self.assertEqual(len(reader.fieldnames), 10)
        self.assertFalse({'Latitude', 'Longitude', 'Source audit'} & set(reader.fieldnames))
        self.assertTrue(actual.endswith(b'\r\n'))

    def test_csv_all_cells_roundtrip_without_field_loss(self):
        rows = map_csv.format_places(self.places, self.append_ids)
        for row in rows:
            self.assertEqual(set(row), set(map_csv.FIELDS))
        actual = list(csv.DictReader(io.StringIO(map_csv.csv_bytes(rows).decode('utf-8'), newline=''), strict=True))
        self.assertEqual(actual, rows)
        self.assertEqual([row['Record ID'] for row in actual], self.append_ids)
        self.assertEqual(sum(len(row) for row in actual), 410)
        with (ROOT/self.original_append['path']).open(encoding='utf-8-sig', newline='') as handle:
            self.assertEqual(actual, list(csv.DictReader(handle, strict=True)))

    def test_csv_five_language_descriptions_and_notes_preserved(self):
        rows = map_csv.format_places(self.places, self.append_ids)
        parsed = list(csv.DictReader(io.StringIO(map_csv.csv_bytes(rows).decode('utf-8'), newline=''), strict=True))
        self.assertEqual(map_csv.LANGUAGES, ('en', 'ko', 'ja', 'zh', 'es'))
        for row in parsed:
            place = self.by_id[row['Record ID']]
            expected = '\n\n'.join(lang.upper() + ': ' + place['description'][lang] + '\n' + place['notes'][lang] for lang in map_csv.LANGUAGES)
            self.assertEqual(row['Description'], expected)

    def test_csv_unicode_quotes_delimiters_and_embedded_bom_roundtrip(self):
        samples = ('English café', '한국어 설명', '日本語の説明', '中文说明', 'Español: información')
        rows = [{field: field + ': ' + sample + ', "quoted"\nLF\rCR\r\nCRLF\ufeffembedded'
                 for field in map_csv.FIELDS} for sample in samples]
        plain = map_csv.csv_bytes(rows)
        legacy = map_csv.csv_bytes(rows, include_bom=True)
        self.assertEqual(legacy, b'\xef\xbb\xbf' + plain)
        self.assertEqual(list(csv.DictReader(io.StringIO(plain.decode('utf-8'), newline=''), strict=True)), rows)
        self.assertEqual(list(csv.DictReader(io.StringIO(legacy.decode('utf-8-sig'), newline=''), strict=True)), rows)
        self.assertEqual(plain.count(b'\xef\xbb\xbf'), len(rows) * len(map_csv.FIELDS))

    def test_csv_empty_input_and_missing_cell(self):
        expected = (','.join('"' + field + '"' for field in map_csv.FIELDS) + '\r\n').encode('ascii')
        self.assertEqual(map_csv.csv_bytes([]), expected)
        self.assertEqual(map_csv.csv_bytes([], include_bom=True), b'\xef\xbb\xbf' + expected)
        with self.assertRaises(KeyError):
            map_csv.csv_bytes([{'Name': 'Incomplete'}])

    def test_immutable_csv_artifact_hashes(self):
        expected = {
            'map-append35-v35.csv': '33371ddb3efb701bae199a6486d2d7b71c5a3a06c823f631bec2e47358b2c2c4',
            'map-append38-v36.csv': 'b7a882ae9944c99b548adb39e00c6330be2b728e2892c07c6163d030d3e82213',
            'map-append41-v37.csv': 'e5cc66e6d8db9288eff5cb771fc0178aa102b62e67220ef6c902202877fb1dbc',
        }
        for name, digest in expected.items():
            self.assertEqual(hashlib.sha256((ROOT/'exports'/name).read_bytes()).hexdigest(), digest)

    def test_successful_evidence_preserves_exact_column_names(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)/'repo'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('build', '.git', '__pycache__'))
            artifact = root/self.operation['successfulArtifact']['path']
            original = artifact.read_bytes()
            self.assertFalse(original.startswith(b'\xef\xbb\xbf'))
            self.assertEqual(validate.validate(root)['status'], 'passed')
            artifact.write_bytes(b'"\xef\xbb\xbfName"' + original[len(b'"Name"'):])
            with self.assertRaisesRegex(ValueError, 'Successful compatibility CSV must remove only BOM'):
                validate.validate(root)

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
            self.assertEqual(a['csvEncoding'], 'utf-8')
            self.assertFalse(a['csvByteOrderMark'])
            self.assertEqual(a['appendRows'], 0)
            self.assertFalse(a['importable'])
            self.assertFalse(a['uploadAuthorized'])
            self.assertEqual(a['appendStatus'], 'no_pending_rows_do_not_upload')
            self.assertFalse((first/'map-append-current.csv').exists())
            self.assertFalse((first/'map-append-current.rows.json').exists())
            self.assertFalse(any('map-append-current' in item['path'] for item in a['outputs']))
            for item in a['outputs']:
                self.assertEqual((first/item['path']).read_bytes(), (second/item['path']).read_bytes())
            points = json.loads((first/'source-points-reference.geojson').read_text())
            self.assertFalse(points['nativeMapGeometry'])
            self.assertEqual(len(points['features']),130)
            self.assertEqual(points['unknownCoordinatesOmitted'],518)
            for feature in points['features']:
                place = self.by_id[feature['id']]
                self.assertEqual(feature['geometry']['coordinates'],[place['coordinates']['lng'],place['coordinates']['lat']])
            historical = json.loads((first/'historical-reconstruction607.json').read_text())
            self.assertTrue(historical['notForImport'])
            self.assertFalse(historical['nativeGeometryIncluded'])
            self.assertEqual(len(historical['records']),607)

    def test_zero_pending_export_removes_stale_import_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            (out/'map-append-current.csv').write_bytes((ROOT/self.original_append['path']).read_bytes())
            (out/'map-append-current.rows.json').write_text('[{"stale": true}]')
            result = build_exports.build(out)
            self.assertEqual(result['appendRows'], 0)
            self.assertFalse(result['importable'])
            self.assertFalse((out/'map-append-current.csv').exists())
            self.assertFalse((out/'map-append-current.rows.json').exists())

    def test_verified_rows_cannot_be_requeued_or_reimported(self):
        for mutation in ('requeue', 'repeat_operation'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)/'repo'
                shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('build', '.git', '__pycache__'))
                if mutation == 'requeue':
                    path = root/'data/map/sync-state.json'
                    data = json.loads(path.read_text())
                    data['pendingAppendPlaceIds'] = self.append_ids
                    expected = 'Pending IDs duplicate imported cohort'
                else:
                    path = root/'data/map/verified-import-history.json'
                    data = json.loads(path.read_text())
                    data['completedAppendOperations'].append(copy.deepcopy(data['completedAppendOperations'][0]))
                    expected = 'Repeated verified append IDs'
                path.write_text(json.dumps(data, ensure_ascii=False))
                with self.assertRaisesRegex(ValueError, expected):
                    validate.validate(root)

    def test_v38_status_only_preserves_all_v37_content_and_queues(self):
        for path in ('data/places.json', 'data/photos.json', 'data/map/baseline607.json', 'data/map/identity-index.json', 'data/map/geometry-evidence.json', 'data/map/unresolved6.json', 'data/map/pending-field-edits692.json', 'data/history/applied-field-changes213.json', 'data/history/original-source-audits296.json', 'exports/map-append35-v35.csv', 'exports/map-append38-v36.csv', 'exports/map-append41-v37.csv'):
            self.assertEqual((ROOT/path).read_bytes(), v37_bytes(path), path)
        old_sync = json.loads(v37_bytes('data/map/sync-state.json'))
        for field in ('existingUpdateGroups', 'cleanup', 'pendingFieldEditCount', 'appliedFieldChangeCount', 'pendingCivilianAddressNormalizationIds'):
            self.assertEqual(self.sync[field], old_sync[field])
        original_cohorts = [{k:v for k,v in c.items() if k not in ('status','sourceReleaseStatus')} for c in old_sync['pendingCohorts']]
        completed_cohorts = [{k:v for k,v in c.items() if k not in ('status','priorStatus','historicalSourceReleaseStatus','verifiedAtUtc','receipt')} for c in self.operation['cohorts']]
        self.assertEqual(completed_cohorts, original_cohorts)
        self.assertEqual(validate.load('data/history/map-status-v37-before-append41.json'), json.loads(v37_bytes('data/research.json'))['map'])
        old_history = json.loads(v37_bytes('data/history/verification-history.json'))
        self.assertEqual(validate.load('data/history/verification-history.json')['events'][:len(old_history['events'])], old_history['events'])
        self.assertEqual((ROOT/'data/history/site-deployment-v37.json').read_bytes(), subprocess.check_output(['git','-C',str(ROOT),'show',INTEGRATION_BASE+':data/history/site-deployment-v37.json']))
        self.assertEqual(validate.load('data/metadata.json')['snapshotRelease'], 'v38')
        self.assertEqual(validate.load('data/metadata.json')['lastPublishedSiteRelease'], 'v37')

    def test_successful_fixture_exact_410_cells_and_receipt_limits(self):
        receipt = validate.load(self.operation['receipt'])
        successful = (ROOT/self.operation['successfulArtifact']['path']).read_bytes()
        original = (ROOT/self.original_append['path']).read_bytes()
        self.assertEqual(successful, original[3:])
        self.assertEqual(len(successful), 151463)
        self.assertEqual(hashlib.sha256(successful).hexdigest(), 'c15497cc633be24e5449350d39fe4153c32332eec1e9cd16fd99e93c65044aa4')
        reader = csv.DictReader(io.StringIO(successful.decode('utf-8'), newline=''), strict=True)
        rows = list(reader)
        self.assertEqual(reader.fieldnames, map_csv.FIELDS)
        self.assertEqual(rows, map_csv.format_places(self.places, self.append_ids))
        self.assertEqual(sum(len(row) for row in rows), 410)
        preservation = receipt['preservation']
        self.assertEqual((preservation['explicitPointGeometriesCompared'], preservation['existingAddressLocatorsCompared']), (100, 501))
        self.assertFalse(preservation['full601NumericalGeometryPreservationVerified'])
        self.assertFalse(preservation['nativeIdsFreshlyVerified'])
        self.assertEqual(preservation['newNativeIds'], [])
        self.assertEqual(receipt['schema']['existingTitleColumn'], 'U+FEFF + Name')
        self.assertTrue(receipt['schema']['extraNameColumnRetained'])
        self.assertEqual(receipt['append']['newDisplayTitlesRepaired'], 41)
        self.assertEqual(receipt['schema']['deletedColumns'], 0)
        self.assertEqual(receipt['legendConsolidation']['categoryWrites'], 0)
        self.assertEqual(receipt['timestamps']['descriptionReloadVerifiedAtUtc'], '2026-10-27T07:45:51.523Z')
        unresolved = validate.load('data/map/unresolved7.json')
        self.assertEqual(unresolved[-1]['siteRecordId'], 'redbutton-ansan')
        self.assertIsNone(unresolved[-1]['nativeId'])

    def test_category_contract_is_proposal_only(self):
        plan = validate.load('data/map/coarse-category-plan.json')
        self.assertEqual(plan['status'], 'proposed_not_applied')
        self.assertEqual([g['count'] for g in plan['taxonomy']['groups']], [127, 140, 185, 74, 120, 2])
        self.assertEqual(sum(p['nativeId'] is not None for p in plan['places']), 296)
        self.assertEqual(plan['validation']['mapChangesPerformed'], 0)
        self.assertEqual([p['id'] for p in plan['places']], [p['id'] for p in self.places])
        research = validate.load('data/research.json')
        self.assertEqual(research['map']['category_consolidation']['category_writes'], 0)
        self.assertEqual(research['release_added_places'], 0)
        self.assertEqual(research['map']['legend_reorganization']['target_single_purpose_layers'], 6)
        self.assertEqual(research['map']['legend_reorganization']['target_status'], 'proposed_not_applied')
        self.assertEqual(validate.load('data/history/map-status-v37-before-append41.json')['legend_reorganization']['target_single_purpose_layers'], 8)

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
