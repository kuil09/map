"""Synthetic additions only: no fixture is evidence of a real venue or live-map write."""
from collections import Counter
import copy
import csv
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import active_classification as active
import build_category_presentation as presentation
import build_exports
import build_site_data
import validate


def write(root, path, value):
    (root/path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def synthetic_place():
    return {
        'id':'fixture-national-addition', 'fixtureOnly':True,
        'name_en':'Synthetic national test venue', 'name_ko':'합성 시험 장소',
        'area':'Synthetic national area', 'category':'landmarks', 'setting':'mixed',
        'address':'Synthetic fixture address, not a real destination',
        'description':{lang:'Synthetic fixture only; not a real listing.' for lang in validate.LANGUAGES},
        'notes':{lang:'No live operations, entrance or route verified.' for lang in validate.LANGUAGES},
        'sources':[{'url':'https://example.invalid/synthetic-venue', 'quality':'fixture',
                    'audit':{'checked':'2000-01-01', 'scope':'synthetic_test_only',
                             'status':'unconfirmed', 'reason':'Synthetic input, not research evidence.'}}],
        'checked':'2000-01-01', 'map_type':'search', 'coordinates':None,
        'coordinate_status':'Unknown; no coordinate or entrance inferred.',
        'radial_distance_km':None, 'distance_reference_id':None,
        'distance_kind':'unmeasured', 'entrance_verification':'unverified', 'access':'public',
    }


def refresh_active_hashes(root):
    """Explicit fixture maintenance, not an automatic canonical updater."""
    places = validate.load('data/places.json', root)
    contract = validate.load(active.ACTIVE_PATH, root)
    contract['canonicalPlacesSha256'] = validate.digest(root/'data/places.json')
    by_id = {p['id']:p for p in places}
    for assignment in contract['assignments']:
        assignment['sourceRecordSha256'] = active.record_sha(by_id[assignment['id']])
    write(root, active.ACTIVE_PATH, contract)


def fixture(directory, measured=False, point_only=False):
    root = Path(directory)/'repo'
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('build','.git','__pycache__'))
    places = validate.load('data/places.json', root)
    addition = synthetic_place()
    research = validate.load('data/research.json', root)
    if measured or point_only:
        # Hypothetical sourced fixture point >200 km away; never a real canonical record.
        addition.update(coordinates={'lat':33.0,'lng':127.0}, distance_kind='straight_line',
                        coordinate_source_url=addition['sources'][0]['url'],
                        coordinate_provenance='Synthetic test fixture only; not real coordinate evidence.',
                        distance_reference_id=research['distance_audit']['reference']['id'],
                        distance_method=research['distance_audit']['method'])
        addition['sources'][0]['audit'].update(status='verified',scope='exact')
        if measured:
            addition['radial_distance_km'] = round(validate.haversine(
                research['distance_audit']['reference']['coordinates'], addition['coordinates']), 1)
        else:
            addition.update(distance_kind='unmeasured',distance_reference_id=None)
            addition.pop('distance_method')
    places.append(addition)
    write(root, 'data/places.json', places)
    write(root, active.ACTIVE_PATH, {
        'schemaVersion':'1.0', 'status':'active_classification', 'fixtureOnly':True,
        'canonicalRepository':'https://github.com/kuil09/map',
        'historicalPlanSha256':active.PLAN_SHA256,
        'canonicalPlacesSha256':validate.digest(root/'data/places.json'),
        'assignments':[{'id':addition['id'], 'sourceRecordSha256':active.record_sha(addition),
                        'sourceCategory':addition['category'], 'visitorPurpose':'culture_sights',
                        'presentationGroup':'culture_sights', 'nativeId':None}],
    })
    statuses = dict(Counter(s['audit']['status'] for p in places for s in p['sources']))
    points = sum(p['coordinates'] is not None for p in places)
    measured_count = sum(p['radial_distance_km'] is not None for p in places)
    metadata = validate.load('data/metadata.json', root)
    metadata.update(snapshotRelease='v39',lastPublishedSiteRelease='v38')
    metadata['counts'].update(places=len(places), sourceReferences=sum(statuses.values()),
                              sourceStatuses=statuses, coordinatePoints=points, unmeasured=len(places)-measured_count)
    write(root, 'data/metadata.json', metadata)
    research['places'] = len(places)
    research['source_audit'].update(places=len(places), source_references=sum(statuses.values()),
                                    source_reference_statuses=statuses)
    research['distance_audit'].update(checked_records=measured_count, unchecked_records=len(places)-measured_count)
    research['category_counts'] = dict(Counter(p['category'] for p in places))
    research['coverage'][addition['area']] = {addition['category']:1}
    research['coverage_gaps'][addition['area']] = []
    research['map'].update(expected_total=len(places), remaining_map_uploads=1)
    write(root, 'data/research.json', research)
    sync = validate.load('data/map/sync-state.json', root)
    sync.update(siteRelease='v39',lastPublishedSiteRelease='v38',siteTotal=len(places), pendingAppendPlaceIds=[addition['id']],
                pendingCohorts=[{'cohort':'synthetic_test_only', 'placeIds':[addition['id']]}],
                currentAppendFile=None, currentAppendStatus='pending_rows_not_authorized_for_upload')
    write(root, 'data/map/sync-state.json', sync)
    return root


class ActiveClassificationTests(unittest.TestCase):
    def test_current_counts_and_five_purposes_are_unchanged_without_overlay(self):
        self.assertFalse((ROOT/active.ACTIVE_PATH).exists())
        result = validate.validate()
        self.assertEqual((result['places'], result['pendingAppend'], result['confirmedMapRows']), (648,0,646))
        value = presentation.generate(ROOT)
        self.assertEqual(value['projection'], {'canonicalArchiveCount':648,'publicCount':646,'excludedCount':2})
        self.assertEqual([g['count'] for g in value['groups']], [127,140,185,74,120])
        self.assertEqual(len(value['assignments']), 646)

    def test_addition_builds_without_rewriting_history_or_claiming_map_import(self):
        with tempfile.TemporaryDirectory() as directory:
            root = fixture(directory)
            result = validate.validate(root)
            self.assertEqual((result['places'], result['pendingAppend'], result['historicallyImportedLogicalRows']), (649,1,648))
            self.assertEqual((result['confirmedMapRows'], result['positionedMapRows'], result['unresolvedMapRows']), (646,639,7))
            output = Path(directory)/'site'
            manifest = build_site_data.build(output, root)
            self.assertEqual(manifest['projection'], {'canonicalArchivePlaces':649,'publicPlaces':647,
                                                     'excludedPlaces':2,'policyPath':active.POLICY_PATH})
            self.assertFalse(manifest['deployed'])
            self.assertEqual(manifest['snapshotRelease'],'v39')
            public = json.loads((output/'places.json').read_text())
            self.assertEqual(len(public),647)
            self.assertIsNone(public[-1]['coordinates'])
            self.assertIsNone(public[-1]['radial_distance_km'])
            self.assertEqual(public[-1]['sources'], synthetic_place()['sources'])
            research = json.loads((output/'research.json').read_text())
            self.assertEqual(research['places'],647)
            self.assertEqual(research['provenance']['canonicalArchivePlaces'],649)
            self.assertEqual(tuple(research['map'][k] for k in ('confirmed_data_rows','positioned_markers','unlocated_rows')), (646,639,7))
            categories = json.loads((output/'category-presentation.json').read_text())
            self.assertEqual({g['id'] for g in categories['groups']}, active.PUBLIC_PURPOSES)
            self.assertEqual([g['count'] for g in categories['groups']], [127,140,185,74,121])
            self.assertEqual(len(categories['assignments']),647)
            self.assertEqual(categories['source']['canonicalArchivePlacesSha256'],validate.digest(root/'data/places.json'))
            self.assertEqual(categories['source']['activeContractSha256'],validate.digest(root/active.ACTIVE_PATH))
            self.assertFalse(categories['source']['mapVerifiedByGenerator'])
            self.assertFalse(categories['source']['deployedByGenerator'])
            export = Path(directory)/'exports'
            export_manifest = build_exports.build(export,root)
            self.assertEqual(export_manifest['appendRows'],1)
            self.assertFalse(export_manifest['uploaded'])
            self.assertFalse(export_manifest['uploadAuthorized'])
            with (export/'map-append-current.csv').open(encoding='utf-8',newline='') as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual([r['Record ID'] for r in rows],['fixture-national-addition'])
            for path in list((ROOT/'data/history').rglob('*')) + list((ROOT/'exports').rglob('*')):
                if path.is_file():
                    relative = path.relative_to(ROOT)
                    self.assertEqual((root/relative).read_bytes(),path.read_bytes(),str(relative))
            for path in (active.PLAN_PATH, active.POLICY_PATH, 'data/map/verified-import-history.json',
                         'data/map/identity-index.json','data/map/baseline607.json',
                         'data/map/unresolved6.json','data/map/unresolved7.json'):
                self.assertEqual((root/path).read_bytes(),(ROOT/path).read_bytes(),path)
            self.assertEqual(validate.load('data/places.json',root)[:648],validate.load('data/places.json'))

    def test_overlay_rejects_missing_duplicate_historical_stale_and_sixth_purpose(self):
        mutations = (
            ('missing',lambda a:a.update(assignments=[]),'purpose assignments'),
            ('duplicate',lambda a:a['assignments'].append(copy.deepcopy(a['assignments'][0])),'Duplicate active'),
            ('historical_collision',lambda a:a['assignments'][0].update(id=validate.load('data/places.json')[0]['id']),'collide'),
            ('stale_record',lambda a:a['assignments'][0].update(sourceRecordSha256='0'*64),'stale active source record'),
            ('stale_file',lambda a:a.update(canonicalPlacesSha256='0'*64),'canonical places hash'),
            ('sixth_purpose',lambda a:a['assignments'][0].update(visitorPurpose='restricted_access'),'unknown public purpose'),
            ('restricted_group',lambda a:a['assignments'][0].update(presentationGroup='restricted_access'),'non-public presentation'),
            ('native_id',lambda a:a['assignments'][0].update(nativeId='invented-native-id'),'unverified new native ID'),
        )
        for label, mutate, message in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                root = fixture(directory)
                contract = validate.load(active.ACTIVE_PATH, root)
                mutate(contract)
                write(root,active.ACTIVE_PATH,contract)
                with self.assertRaisesRegex(ValueError,message):
                    validate.validate(root)
        with tempfile.TemporaryDirectory() as directory:
            root = fixture(directory)
            (root/active.ACTIVE_PATH).unlink()
            with self.assertRaisesRegex(ValueError,'require active classification'):
                validate.validate(root)

    def test_restricted_unknown_access_and_unsupported_entrance_claims_fail_closed(self):
        for field, value, error in (
            ('access','restricted','Unapproved restricted-access'),
            ('access','unknown','explicit public access'),
            ('entrance_verification','verified','unsupported entrance verification'),
            ('distance_kind','driving','explicitly unmeasured'),
        ):
            with self.subTest(field=field,value=value), tempfile.TemporaryDirectory() as directory:
                root = fixture(directory)
                places = validate.load('data/places.json',root)
                places[-1][field] = value
                write(root,'data/places.json',places)
                refresh_active_hashes(root)
                with self.assertRaisesRegex(ValueError,error):
                    validate.validate(root)

    def test_national_fixture_over_200_km_is_not_subject_to_radius_cap(self):
        with tempfile.TemporaryDirectory() as directory:
            root = fixture(directory,measured=True)
            addition = validate.load('data/places.json',root)[-1]
            self.assertGreater(addition['radial_distance_km'],200)
            self.assertEqual(addition['distance_kind'],'straight_line')
            self.assertEqual(addition['entrance_verification'],'unverified')
            self.assertEqual(validate.validate(root)['places'],649)
            self.assertEqual(presentation.generate(root)['projection']['publicCount'],647)

    def test_sourced_general_point_can_remain_distance_unmeasured(self):
        with tempfile.TemporaryDirectory() as directory:
            root = fixture(directory,point_only=True)
            result = validate.validate(root)
            self.assertEqual((result['places'],result['coordinatePoints'],result['unmeasured']), (649,131,519))
            metadata = validate.load('data/metadata.json',root)
            research = validate.load('data/research.json',root)
            self.assertEqual(metadata['counts']['coordinatePoints'],131)
            self.assertEqual(metadata['counts']['unmeasured'],519)
            self.assertEqual(research['distance_audit']['checked_records'],130)
            self.assertEqual(research['distance_audit']['unchecked_records'],519)
            output = Path(directory)/'site'
            build_site_data.build(output,root)
            record = json.loads((output/'places.json').read_text())[-1]
            self.assertEqual(record['coordinates'],{'lat':33.0,'lng':127.0})
            self.assertIsNone(record['radial_distance_km'])
            self.assertIsNone(record['distance_reference_id'])
            self.assertEqual(record['distance_kind'],'unmeasured')
            self.assertEqual(record['entrance_verification'],'unverified')
            export = Path(directory)/'export'
            build_exports.build(export,root)
            points = json.loads((export/'source-points-reference.geojson').read_text())
            self.assertEqual(points['features'][-1]['id'],record['id'])
            self.assertIsNone(points['features'][-1]['properties']['radial_distance_km'])
            self.assertEqual(result['confirmedMapRows'],646)

    def test_general_point_still_requires_verified_exact_provenance(self):
        mutations = (
            ('unconfirmed',lambda p:p['sources'][0]['audit'].update(status='unconfirmed'),'verified exact evidence'),
            ('brand',lambda p:p['sources'][0]['audit'].update(scope='brand'),'verified exact evidence'),
            ('missing_provenance',lambda p:p.pop('coordinate_provenance'),'missing coordinate_provenance'),
            ('wrong_source',lambda p:p.update(coordinate_source_url='https://example.invalid/other'),'coordinate source missing'),
        )
        for label, mutate, error in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                root = fixture(directory,point_only=True)
                places = validate.load('data/places.json',root)
                mutate(places[-1])
                write(root,'data/places.json',places)
                refresh_active_hashes(root)
                if label == 'unconfirmed':
                    metadata = validate.load('data/metadata.json',root)
                    research = validate.load('data/research.json',root)
                    statuses = dict(Counter(s['audit']['status'] for p in places for s in p['sources']))
                    metadata['counts']['sourceStatuses'] = statuses
                    research['source_audit']['source_reference_statuses'] = statuses
                    write(root,'data/metadata.json',metadata)
                    write(root,'data/research.json',research)
                with self.assertRaisesRegex(ValueError,error):
                    validate.validate(root)

    def test_measured_distance_never_accepts_missing_coordinates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = fixture(directory,measured=True)
            places = validate.load('data/places.json',root)
            places[-1]['coordinates'] = None
            write(root,'data/places.json',places)
            refresh_active_hashes(root)
            with self.assertRaisesRegex(ValueError,'measured distance requires coordinates'):
                validate.validate(root)

    def test_historical_coordinate_distance_pairing_remains_strict(self):
        with tempfile.TemporaryDirectory() as directory:
            root = fixture(directory)
            places = validate.load('data/places.json',root)
            next(p for p in places[:648] if p['coordinates'])['radial_distance_km'] = None
            write(root,'data/places.json',places)
            refresh_active_hashes(root)
            with self.assertRaisesRegex(ValueError,'unknown coordinate/distance mismatch'):
                validate.validate(root)

    def test_original_record_order_and_immutable_contracts_cannot_be_rewritten(self):
        for label in ('record','order','plan','policy'):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                root = fixture(directory)
                if label in ('record','order'):
                    places = validate.load('data/places.json',root)
                    if label == 'record':
                        places[0]['name_en'] += ' changed'
                    else:
                        places[0],places[1] = places[1],places[0]
                    write(root,'data/places.json',places)
                    refresh_active_hashes(root)
                else:
                    path = active.PLAN_PATH if label == 'plan' else active.POLICY_PATH
                    (root/path).write_bytes((root/path).read_bytes()+b'\n')
                with self.assertRaisesRegex(ValueError,'Historical'):
                    validate.validate(root)

    def test_imported_or_duplicate_ids_cannot_be_queued_again(self):
        imported = validate.load('data/map/identity-index.json')['receiptBackedImportedPlaceIds'][0]
        for ids in ([imported], ['activity-humphreys-downtown-lanes'],
                    ['fixture-national-addition','fixture-national-addition']):
            with self.subTest(ids=ids), tempfile.TemporaryDirectory() as directory:
                root = fixture(directory)
                sync = validate.load('data/map/sync-state.json',root)
                sync['pendingAppendPlaceIds'] = ids
                write(root,'data/map/sync-state.json',sync)
                with self.assertRaisesRegex(ValueError,'Pending IDs duplicate imported cohort'):
                    validate.validate(root)

    def test_new_prepared_snapshot_must_name_latest_successful_publication(self):
        for last, prepared, error in (
            ('v37','v39','latest successful receipt'),
            ('v39','v40','latest successful receipt'),
            ('v38','v38','newer than last published'),
        ):
            with self.subTest(last=last,prepared=prepared), tempfile.TemporaryDirectory() as directory:
                root = fixture(directory)
                metadata = validate.load('data/metadata.json',root)
                sync = validate.load('data/map/sync-state.json',root)
                metadata.update(snapshotRelease=prepared,lastPublishedSiteRelease=last)
                sync.update(siteRelease=prepared,lastPublishedSiteRelease=last)
                write(root,'data/metadata.json',metadata)
                write(root,'data/map/sync-state.json',sync)
                with self.assertRaisesRegex(ValueError,error):
                    validate.validate(root)

    def test_publication_labels_are_derived_not_fixed_to_v38(self):
        with tempfile.TemporaryDirectory() as directory:
            root = fixture(directory)
            receipt = validate.load('data/history/site-deployment-v38.json',root)
            receipt.update(release='v39',publishedAtUtc='2100-01-01T00:00:00Z')
            # Local synthetic receipt only; this does not claim a real deployment.
            write(root,'data/history/site-deployment-v39.json',receipt)
            metadata = validate.load('data/metadata.json',root)
            sync = validate.load('data/map/sync-state.json',root)
            metadata.update(snapshotRelease='v40',lastPublishedSiteRelease='v39')
            sync.update(siteRelease='v40',lastPublishedSiteRelease='v39')
            write(root,'data/metadata.json',metadata)
            write(root,'data/map/sync-state.json',sync)
            self.assertEqual(validate.validate(root)['places'],649)

    def test_failed_future_deployment_is_not_publication_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = fixture(directory)
            failed = validate.load('data/history/site-deployment-v38.json',root)
            failed.update(release='v40',status='failed',publishedAtUtc='2100-01-01T00:00:00Z')
            write(root,'data/history/site-deployment-v40.json',failed)
            self.assertEqual(validate.validate(root)['places'],649)

    def test_rejects_missing_source_provenance_and_unbound_coordinate_source(self):
        for measured in (False,True):
            with self.subTest(measured=measured), tempfile.TemporaryDirectory() as directory:
                root = fixture(directory,measured=measured)
                places = validate.load('data/places.json',root)
                if measured:
                    places[-1]['coordinate_source_url'] = 'https://example.invalid/not-in-sources'
                else:
                    places[-1]['sources'] = []
                write(root,'data/places.json',places)
                refresh_active_hashes(root)
                with self.assertRaisesRegex(ValueError,'coordinate source missing|no sources'):
                    validate.validate(root)


if __name__ == '__main__':
    unittest.main()
