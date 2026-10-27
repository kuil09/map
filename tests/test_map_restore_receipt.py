"""Synthetic receipt tests: fixtures are NOT observations of the live map."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import validate
from build_category_presentation import public_research, public_projection

BASE = '57584da2f67ed41b4bab677d979317d3ccef9c2e'
RECEIPT_PATH = 'data/history/map-restore-current-receipt.json'
UNRESOLVED_PATH = 'data/map/unresolved-after-restore.json'


def write(root, path, value):
    (root/path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def install_synthetic_receipt(root):
    """Exercise the new contract without claiming real save time or fresh IDs."""
    policy = validate.load('data/map/public-exclusions.json', root)
    unresolved = [copy.deepcopy(r) for r in validate.load('data/map/unresolved7.json', root)
                  if r['siteRecordId'] not in policy['excludedPlaceIds']]
    unresolved.append({'siteRecordId':'activity-ds-billiards-paengseong',
                       'name':'DS Billiards Paengseong | DS Billiards 팽성점',
                       'nativeId':None})
    receipt = {
        'schemaVersion':'1.0', 'fixtureOnly':True,
        'operation':'restore_after_layer_deletion', 'status':'partial',
        'mapId':'1-wHgIPUvxP4PS6YwuxBsMp8luu_amrk',
        'verifiedAtUtc':'2000-01-01T00:00:00Z',
        'savedReloadedCountsVerified':True,
        'canonicalArchiveCount':648,
        'publicExclusionPolicySHA256':validate.digest(root/'data/map/public-exclusions.json'),
        'excludedPlaceIds':policy['excludedPlaceIds'],
        'counts':{'rows':646,'positioned':639,'unresolved':7,'layers':5},
        'unresolved':[{'recordId':r['siteRecordId'],'name':r['name']} for r in unresolved],
        'identityCoverage':{'allCurrentRecordIdsFreshlyVerified':False,'verifiedPlaceIds':[],
                            'nativeIdsPreserved':False},
        'preservation':{'fullNumericalGeometryPreservationVerified':False},
    }
    write(root, RECEIPT_PATH, receipt)
    write(root, UNRESOLVED_PATH, unresolved)
    sync = validate.load('data/map/sync-state.json', root)
    sync.update({'confirmedNativeRows':646,'positionedMarkers':639,'unresolvedRows':7,
                 'mapReceipt':RECEIPT_PATH,'mapReceiptSHA256':validate.digest(root/RECEIPT_PATH),
                 'mapVerifiedAtUtc':receipt['verifiedAtUtc'],'currentUnresolvedFile':UNRESOLVED_PATH,
                 'historicalUnresolvedFiles':['data/map/unresolved6.json','data/map/unresolved7.json']})
    write(root, 'data/map/sync-state.json', sync)
    research = validate.load('data/research.json', root)
    research['map'].update({'confirmed_data_rows':646,'total_verified_rows':646,
                            'positioned_markers':639,'unlocated_rows':7,'error_rows':7})
    write(root, 'data/research.json', research)
    return receipt, sync


class RestoreReceiptTests(unittest.TestCase):
    def fixture(self, directory):
        root = Path(directory)/'repo'
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('build','.git','__pycache__'))
        install_synthetic_receipt(root)
        return root

    def test_partial_restore_counts_do_not_rewrite_archive_or_claim_id_audit(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self.fixture(temp)
            result = validate.validate(root)
            self.assertEqual((result['historicallyImportedLogicalRows'], result['expectedCurrentLogicalRows'], result['confirmedMapRows'], result['positionedMapRows'], result['unresolvedMapRows']), (648,646,646,639,7))
            archive, public, _ = public_projection(root)
            output = public_research(root, public)
            self.assertEqual(len(archive),648)
            self.assertEqual(output['map']['restoration_status'],'partial')
            self.assertFalse(output['map']['all_current_record_ids_freshly_verified'])
            self.assertEqual(output['map']['confirmed_data_rows'],646)
            for path in ('data/places.json','data/map/unresolved6.json','data/map/unresolved7.json',
                         'data/history/map-append41-verified-receipt.json','data/map/verified-import-history.json',
                         'data/map/coarse-category-plan.json'):
                self.assertEqual((root/path).read_bytes(), (ROOT/path).read_bytes(), path)

    def test_public_totals_come_from_receipt_not_stale_research_scalar(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self.fixture(temp)
            research = validate.load('data/research.json', root)
            research['map'].update({'confirmed_data_rows':999,'positioned_markers':998,'unlocated_rows':1})
            write(root, 'data/research.json', research)
            _, public, _ = public_projection(root)
            output = public_research(root, public)
            self.assertEqual(tuple(output['map'][k] for k in ('confirmed_data_rows','positioned_markers','unlocated_rows')), (646,639,7))
            with self.assertRaisesRegex(ValueError,'Research verified map counts drift'):
                validate.validate(root)

    def test_restore_rejects_unsupported_claims_and_policy_drift(self):
        mutations = (
            ('excluded', lambda r: r['excludedPlaceIds'].pop(), 'Restore exclusions differ'),
            ('geometry', lambda r: r['preservation'].update(fullNumericalGeometryPreservationVerified=True), 'exact numerical geometry'),
            ('native_ids', lambda r: r['identityCoverage'].update(nativeIdsPreserved=True), 'old native IDs'),
            ('unverified_ids', lambda r: r['identityCoverage'].update(verifiedPlaceIds=['activity-ds-billiards-paengseong']), 'Unverified current IDs'),
            ('incomplete_id_readback', lambda r: r['identityCoverage'].update(allCurrentRecordIdsFreshlyVerified=True), 'fresh Record-ID membership'),
            ('not_reloaded', lambda r: r.update(savedReloadedCountsVerified=False), 'saved/reloaded evidence'),
        )
        for label, mutate, error in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                root = self.fixture(temp)
                receipt = validate.load(RECEIPT_PATH, root)
                mutate(receipt)
                write(root, RECEIPT_PATH, receipt)
                sync = validate.load('data/map/sync-state.json', root)
                sync['mapReceiptSHA256'] = validate.digest(root/RECEIPT_PATH)
                write(root, 'data/map/sync-state.json', sync)
                with self.assertRaisesRegex(ValueError,error):
                    validate.validate(root)

    def test_excluded_archived_rows_cannot_be_requeued(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self.fixture(temp)
            sync = validate.load('data/map/sync-state.json', root)
            sync['pendingAppendPlaceIds'] = ['activity-humphreys-downtown-lanes']
            write(root, 'data/map/sync-state.json', sync)
            with self.assertRaisesRegex(ValueError,'Pending IDs duplicate imported cohort'):
                validate.validate(root)

    def test_original_append_and_six_group_proposal_stay_immutable(self):
        for path in ('data/history/map-append41-verified-receipt.json',
                     'data/map/verified-import-history.json','data/map/coarse-category-plan.json',
                     'data/map/unresolved7.json','data/map/public-exclusions.json'):
            old = subprocess.check_output(['git','-C',str(ROOT),'show',f'{BASE}:{path}'])
            self.assertEqual((ROOT/path).read_bytes(),old,path)


if __name__ == '__main__':
    unittest.main()
