"""Optimization-safe negative controls for this exact review checkpoint."""
import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from validate_merged_assembly_reconciliation import (
    HERE, FRENCH_PAIRS, CROP_PAIRS, CURRENT_PAIRS, COHORT, HELP_KEY, CROP_KEY,
    FIXTURE, read, check_identity_scope, check_successor_scope,
    check_current_review_scope, check_review_artifacts, normalized_review_pairs,
    check_pairs, check_history, check_tables, values,
)


class ScopeGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_identities = read(HERE / 'source-identities.json')
        cls.base_counts = read(HERE / 'entry-review-counts.json')
        cls.base_receipts = read(HERE / 'entry-review-receipts.json')
        cls.base_fixture = read(HERE / FIXTURE)
        if cls.base_receipts['source_revision'] != 'e53b2e6aaaa9ac231cfdd38485e28ee9d638e870':
            from validate_position_reconciliation import historical_receipts
            cls.base_receipts = historical_receipts(cls.base_receipts)
            previous = cls.base_identities['previous_resource_manifest_at_position_merge']
            cls.base_identities = {**cls.base_identities, **previous}

    def setUp(self):
        self.identities = copy.deepcopy(self.base_identities)
        self.counts = copy.deepcopy(self.base_counts)
        self.receipts = copy.deepcopy(self.base_receipts)
        self.fixture = copy.deepcopy(self.base_fixture)
        self.pairs = {(x['tag'], x['key']): x for x in self.receipts['receipts']}
        self.complete = {(x['tag'], x['key']): x for x in self.fixture['complete_pairs']}

    def test_complete_manifest(self):
        self.assertEqual(check_identity_scope(self.identities, self.counts), 182)

    def test_removed_unreviewed_catalogue_identity(self):
        target = next(x['catalogue_path'] for x in self.counts['languages'] if x['reviewed_current'] == 0 and x['present'] > 0)
        self.identities['current_source_files'] = [x for x in self.identities['current_source_files'] if x['path'] != target]
        with self.assertRaises(ValueError):
            check_identity_scope(self.identities, self.counts)

    def test_duplicate_identity(self):
        self.identities['current_source_files'][-1] = copy.deepcopy(self.identities['current_source_files'][0])
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

    def test_all_seven_historical_complete_successors(self):
        for pair in sorted(FRENCH_PAIRS | CROP_PAIRS):
            with self.subTest(pair=pair):
                check_successor_scope(self.pairs[pair], pair)

    def test_historical_metadata_gates_not_relaxed(self):
        mutations = {
            'review_scope': 'delta_only', 'disposition': 'accepted_linguistic_only',
            'source': 'https://example.invalid/unrelated', 'independent_review_source': 'https://example.invalid/unrelated',
            'reviewed_source_revision': 'wrong', 'merged_revision': 'wrong', 'correction_applied': False,
        }
        for pair in sorted(FRENCH_PAIRS | CROP_PAIRS):
            for field, bad in mutations.items():
                for missing in (False, True):
                    with self.subTest(pair=pair, field=field, missing=missing):
                        item = copy.deepcopy(self.pairs[pair])
                        if missing:
                            item.pop(field, None)
                        else:
                            item[field] = bad
                        with self.assertRaises(ValueError):
                            check_successor_scope(item, pair)

    def test_three_complete_current_successors(self):
        for pair in sorted(CURRENT_PAIRS):
            check_current_review_scope(self.pairs[pair], pair, self.complete[pair], self.fixture['review_bindings'][pair[0]])

    def test_every_current_metadata_field_required_and_exact(self):
        mutations = {
            'cohort': 'unknown', 'state': 'needs_rereview', 'disposition': 'accepted_linguistic_only',
            'review_scope': 'delta_only', 'review_kind': 'hash_only', 'review_decision': 'pending',
            'reviewed_source_revision': 'wrong', 'merged_revision': 'wrong',
            'correction_applied': True, 'localized_value_unchanged': False,
            'source_pair_status': 'current_english_changed_since_complete_review',
            'source': 'https://example.invalid/unrelated', 'independent_review_source': 'https://example.invalid/unrelated',
            'complete_review_report_sha256': 'wrong', 'complete_review_report_path': 'wrong', 'review_id': 'wrong',
        }
        for pair in sorted(CURRENT_PAIRS):
            for field, bad in mutations.items():
                for missing in (False, True):
                    with self.subTest(pair=pair, field=field, missing=missing):
                        item = copy.deepcopy(self.pairs[pair])
                        if missing:
                            item.pop(field, None)
                        else:
                            item[field] = bad
                        with self.assertRaises(ValueError):
                            check_current_review_scope(item, pair, self.complete[pair], self.fixture['review_bindings'][pair[0]])

    def test_current_cannot_keep_open_finding_or_stale_metadata(self):
        for pair in sorted(CURRENT_PAIRS):
            for field, bad in [('finding_status', 'open'), ('source_pair_review_note', 'still stale')]:
                item = dict(self.pairs[pair], **{field: bad})
                with self.assertRaises(ValueError):
                    check_current_review_scope(item, pair, self.complete[pair], self.fixture['review_bindings'][pair[0]])

    def test_current_requires_final_complete_pair_proof(self):
        for pair in sorted(CURRENT_PAIRS):
            for field, bad in [('decision', 'pending'), ('complete_value_review', False), ('review_id', 'wrong'), ('review_evidence', 'wrong'), ('reviewed_source_revision', 'wrong')]:
                complete = dict(self.complete[pair], **{field: bad})
                with self.assertRaises(ValueError):
                    check_current_review_scope(self.pairs[pair], pair, complete, self.fixture['review_bindings'][pair[0]])

    def test_exact_final_artifacts(self):
        check_review_artifacts(HERE, self.fixture)

    def test_unfinal_missing_or_wrong_artifact_bindings(self):
        for tag in ('ja', 'zh-HK'):
            for field, bad in [('final', False), ('sha256', 'wrong'), ('durable_receipt', 'https://example.invalid'), ('review_id', 'wrong'), ('reviewed_source_revision', 'wrong'), ('path', '../escape.json')]:
                fixture = copy.deepcopy(self.fixture)
                fixture['review_bindings'][tag][field] = bad
                with self.assertRaises(ValueError):
                    check_review_artifacts(HERE, fixture)

    def test_report_content_must_match_accepted_full_value(self):
        self.fixture['complete_pairs'][0]['english'] += ' altered'
        with self.assertRaises(ValueError):
            check_review_artifacts(HERE, self.fixture)

    def test_japanese_all_clauses_required(self):
        report = read(HERE / self.fixture['review_bindings']['ja']['path'])
        report['clause_dispositions'].pop()
        with self.assertRaises(ValueError):
            normalized_review_pairs('ja', report)

    def test_japanese_partial_or_unaccepted_clause_rejected(self):
        report = read(HERE / self.fixture['review_bindings']['ja']['path'])
        for field, value in [('review_scope', 'delta_only'), ('decision', 'pending')]:
            modified = dict(report, **{field: value})
            with self.assertRaises(ValueError):
                normalized_review_pairs('ja', modified)
        report['clause_dispositions'][0]['disposition'] = 'needs_correction'
        with self.assertRaises(ValueError):
            normalized_review_pairs('ja', report)

    def test_hk_every_help_paragraph_required(self):
        report = read(HERE / self.fixture['review_bindings']['zh-HK']['path'])
        help_row = next(x for x in report['rows'] if x['key'] == HELP_KEY)
        help_row['paragraph_reviews'].pop()
        with self.assertRaises(ValueError):
            normalized_review_pairs('zh-HK', report)

    def test_hk_full_paragraph_text_required(self):
        report = read(HERE / self.fixture['review_bindings']['zh-HK']['path'])
        help_row = next(x for x in report['rows'] if x['key'] == HELP_KEY)
        help_row['paragraph_reviews'][0]['localized'] = 'only a term'
        with self.assertRaises(ValueError):
            normalized_review_pairs('zh-HK', report)

    def test_hk_both_source_and_all_target_plural_forms_required(self):
        original = read(HERE / self.fixture['review_bindings']['zh-HK']['path'])
        for field in ('source_form_reviews', 'target_form_reviews'):
            report = copy.deepcopy(original)
            plural = next(x for x in report['rows'] if x['key'] == CROP_KEY)
            plural[field].pop()
            with self.assertRaises(ValueError):
                normalized_review_pairs('zh-HK', report)

    def test_hk_plural_full_form_text_required(self):
        report = read(HERE / self.fixture['review_bindings']['zh-HK']['path'])
        plural = next(x for x in report['rows'] if x['key'] == CROP_KEY)
        plural['target_form_reviews'][0]['full_value'] += ' altered'
        with self.assertRaises(ValueError):
            normalized_review_pairs('zh-HK', report)

    def test_historical_preservation(self):
        check_history(self.receipts, self.fixture)

    def test_prior_history_and_partial_tampering_rejected(self):
        for field in ('superseded_receipts', 'partial_reviews'):
            receipts = copy.deepcopy(self.receipts)
            receipts[field][0]['source'] = 'altered'
            with self.assertRaises(ValueError):
                check_history(receipts, self.fixture)

    def test_added_predecessor_must_be_exact(self):
        self.receipts['superseded_receipts'][-1]['reviewed_english_sha256'] = 'lost'
        with self.assertRaises(ValueError):
            check_history(self.receipts, self.fixture)

    def test_all_four_paused_records_preserved(self):
        for tag in ('ms', 'id', 'ja', 'zh-HK'):
            receipts = copy.deepcopy(self.receipts)
            item = next(x for x in receipts['receipts'] if (x['tag'], x['key']) == (tag, 'string/ui_rendering_images'))
            item['state'] = 'reviewed_current'
            with self.assertRaises(ValueError):
                check_history(receipts, self.fixture)

    def test_unrelated_active_receipt_and_cohort_unchanged(self):
        receipts = copy.deepcopy(self.receipts)
        receipts['receipts'][0]['confidence'] = 'changed'
        with self.assertRaises(ValueError):
            check_history(receipts, self.fixture)
        receipts = copy.deepcopy(self.receipts)
        old_key = next(k for k in receipts['cohorts'] if k != COHORT)
        receipts['cohorts'][old_key]['scope'] = 'changed'
        with self.assertRaises(ValueError):
            check_history(receipts, self.fixture)

    def test_new_fixture_requires_exact_three_distinct_pairs(self):
        historical = read(HERE / 'fr-assembly-merged-reconciliation-20261015.json')['complete_french_pairs']
        historical += read(HERE / 'four-crop-merged-reconciliation-20261015.json')['complete_crop_pairs']
        # All active hashes are satisfied by exact values loaded from the source
        # through a test-only fixture map, so this isolates pair-set validation.
        source = Path(os.environ['AN_PAINT_SOURCE']) if os.environ.get('AN_PAINT_SOURCE') else None
        if source is None or not source.exists():
            self.skipTest('Full-source mutation check requires supplied source checkout')
        english = values(source / 'Paintroid/src/main/res/values/strings.xml')
        cats = {row['tag']: values(source / row['catalogue_path']) for row in self.counts['languages']}
        self.fixture['complete_pairs'][2] = copy.deepcopy(self.fixture['complete_pairs'][1])
        with self.assertRaises(ValueError):
            check_pairs(self.receipts, historical, self.fixture, english, cats)

    def test_bad_active_hash_rejected(self):
        historical = read(HERE / 'fr-assembly-merged-reconciliation-20261015.json')['complete_french_pairs']
        historical += read(HERE / 'four-crop-merged-reconciliation-20261015.json')['complete_crop_pairs']
        source = Path(os.environ['AN_PAINT_SOURCE']) if os.environ.get('AN_PAINT_SOURCE') else None
        if source is None or not source.exists():
            self.skipTest('Full-source mutation check requires supplied source checkout')
        english = values(source / 'Paintroid/src/main/res/values/strings.xml')
        cats = {row['tag']: values(source / row['catalogue_path']) for row in self.counts['languages']}
        self.receipts['receipts'][0]['current_localized_sha256'] = 'bad'
        with self.assertRaises(ValueError):
            check_pairs(self.receipts, historical, self.fixture, english, cats)

    def test_all_171_table_rows_and_exact_counts(self):
        self.counts = read(HERE / 'entry-review-counts.json')
        self.assertGreaterEqual(check_tables(HERE, self.counts), 1)
        self.counts['languages'][0]['reviewed_current'] += 1
        with self.assertRaises(ValueError):
            check_tables(HERE, self.counts)

    def test_duplicate_plural_quantity_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'strings.xml'
            path.write_text('<resources><plurals name="x"><item quantity="other">a</item><item quantity="other">b</item></plurals></resources>')
            with self.assertRaises(ValueError):
                values(path)


if __name__ == '__main__':
    unittest.main()
