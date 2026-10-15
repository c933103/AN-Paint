"""Negative checks for the source-identity and complete-review gates."""
import copy
import unittest
from validate_merged_assembly_reconciliation import (
    HERE, FRENCH_PAIRS, CROP_PAIRS, read, check_identity_scope,
    check_successor_scope,
)


class ScopeGates(unittest.TestCase):
    def setUp(self):
        self.identities = read(HERE / 'source-identities.json')
        self.counts = read(HERE / 'entry-review-counts.json')
        self.receipts = {(x['tag'], x['key']): x for x in
                         read(HERE / 'entry-review-receipts.json')['receipts']}

    def test_complete_manifest(self):
        self.assertEqual(check_identity_scope(self.identities, self.counts), 182)

    def test_removed_identity(self):
        # Select an unreviewed locale, so active-pair hashes cannot mask the gap.
        target = next(x['catalogue_path'] for x in self.counts['languages']
                      if x['reviewed_current'] == 0 and x['present'] > 0)
        self.identities['current_source_files'] = [x for x in self.identities['current_source_files']
                                                   if x['path'] != target]
        with self.assertRaises(ValueError):
            check_identity_scope(self.identities, self.counts)

    def test_duplicate_identity(self):
        items = self.identities['current_source_files']
        items[-1] = copy.deepcopy(items[0])
        with self.assertRaises(ValueError):
            check_identity_scope(self.identities, self.counts)

    def test_substituted_identity_same_count(self):
        self.identities['current_source_files'][-1]['path'] = 'unrelated.xml'
        with self.assertRaises(ValueError):
            check_identity_scope(self.identities, self.counts)

    def test_uncovered_catalogue(self):
        self.counts['languages'][0]['catalogue_path'] = 'uncovered.xml'
        with self.assertRaises(ValueError):
            check_identity_scope(self.identities, self.counts)

    def test_all_complete_successors(self):
        for pair in sorted(FRENCH_PAIRS | CROP_PAIRS):
            with self.subTest(pair=pair):
                check_successor_scope(self.receipts[pair], pair)

    def test_every_successor_rejects_partial_or_missing_metadata(self):
        mutations = {
            'review_scope': 'delta_only',
            'disposition': 'accepted_linguistic_only',
            'source': 'https://example.invalid/unrelated',
            'independent_review_source': 'https://example.invalid/unrelated',
            'reviewed_source_revision': 'wrong',
            'merged_revision': 'wrong',
            'correction_applied': False,
        }
        for pair in sorted(FRENCH_PAIRS | CROP_PAIRS):
            for field, bad in mutations.items():
                for missing in (False, True):
                    with self.subTest(pair=pair, field=field, missing=missing):
                        item = copy.deepcopy(self.receipts[pair])
                        if missing:
                            item.pop(field, None)
                        else:
                            item[field] = bad
                        with self.assertRaises(ValueError):
                            check_successor_scope(item, pair)


if __name__ == '__main__':
    unittest.main()
