"""Exact composed-source contracts; host checks do not establish Android acceptance."""
import hashlib
import itertools
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import commons_metadata_m02_scope as m02
import commons_metadata_m03_scope as m03
import commons_metadata_m04_scope as m04
import hungarian_attribution_c05_scope as c05
from commons_metadata_composition_scope import COMBINED_HELPER
from commons_metadata_m04_composition_scope import (scope, FIXTURE, before_composed_m04,
    before_m04_composed_production, as_standalone_m04, as_standalone_m04_bytes, reverse)
from commons_metadata_m04_font_scope import before_m04_font
from commons_metadata_m04_diagnostic_scope import before_diagnostic

ROOT = Path(__file__).resolve().parents[1]
JAVA = 'Paintroid/src/main/java/org/catrobat/paintroid/classic/'
QUERY_BRANCH = '        else if(error is CommonsAttribution.QueryFailureException) ui(R.string.commons_metadata_query_failed)\n'


def digest(content):
    return hashlib.sha256(content).hexdigest()


class CommonsMetadataM04CompositionContracts(unittest.TestCase):
    def test_exact_source_inputs_and_accepted_value_file_remain_bound(self):
        data = scope()
        self.assertEqual('71f4d288669858e7975ec4c094b7f47a9a1ff145', data['pr52_commit'])
        self.assertEqual('815e265af5387111dcdaef66efac5d2091bbb56d', data['pr52_tree'])
        self.assertEqual('045004bb23ef762f1731982f7a0152fef0fc5507', data['m04_commit'])
        self.assertEqual('892e09280be9d668862ae5efada0ada163cc6bdb', data['m04_tree'])
        values = ROOT / 'verification/commons-metadata-m04-2026-10-12/linguistic-review/successor-recovered/accepted-and-proposed-values-v4.json'
        self.assertEqual(data['accepted_values_sha256'], digest(values.read_bytes()))
        for row in data['immutable_m04_inputs']:
            self.assertEqual(row['sha256'], digest((ROOT / row['path']).read_bytes()), row['path'])

    def test_every_pr52_leaf_is_preserved_exactly_or_has_an_explicit_reversible_delta(self):
        data = scope()
        rows = data['inherited_unchanged_paths'] + data['pr52_overlaps'] + data['binary_overlaps']
        self.assertEqual(1805, len(rows))
        self.assertEqual(1805, len({row['path'] for row in rows}))
        for row in data['inherited_unchanged_paths']:
            self.assertEqual(row['sha256'], digest((ROOT / row['path']).read_bytes()), row['path'])
        for row in data['pr52_overlaps']:
            content = (ROOT / row['path']).read_bytes()
            self.assertEqual(row['after_sha256'], digest(before_diagnostic(row['path'], content)), row['path'])
            self.assertEqual(row['before_sha256'], digest(before_composed_m04(row['path'], content)), row['path'])
        self.assertEqual(1, len(data['binary_overlaps']))
        row = data['binary_overlaps'][0]
        content = (ROOT / row['path']).read_bytes()
        self.assertEqual('Paintroid/src/main/assets/fonts/anpaintnomui.ttf', row['path'])
        self.assertEqual(row['after_sha256'], digest(content))
        self.assertEqual(row['before_sha256'], digest(before_m04_font(content)))

    def test_all_24_resource_reversal_orders_restore_original_pre_m02_m03_m04_c05_endpoints(self):
        reversals = (m02.before_m02_catalogue, m03.before_m03_catalogue,
                     m04.before_m04_catalogue, c05.before_c05)
        for row in m02.fixture()['entries']:
            path = row['path']; original = (ROOT / path).read_text()
            for key in ('commons_metadata_http_error', 'commons_metadata_response_too_large', 'commons_metadata_query_failed'):
                self.assertEqual(1, original.count(f'name="{key}"'))
            for order in itertools.permutations(reversals):
                restored = original
                for reverse in order:
                    restored = reverse(path, restored)
                self.assertEqual(row['before_sha256'], digest(restored.encode()), path)

    def test_original_m04_catalogue_production_and_prior_test_endpoints_are_preserved(self):
        for fixture in (m04.catalogue_fixture, m04.production_fixture, m04.test_fixture):
            for row in fixture()['entries']:
                text = as_standalone_m04(row['path'], (ROOT / row['path']).read_text())
                self.assertEqual(row['after_sha256'], digest(text.encode()), row['path'])
        for row in scope()['m04_overlaps']:
            self.assertEqual(row['before_sha256'], digest(as_standalone_m04_bytes(row['path'], (ROOT / row['path']).read_bytes())))

    def test_live_production_has_one_three_type_mapper_and_unchanged_pr52_callbacks(self):
        path = JAVA + 'MediaGalleryActivity.kt'; gallery = (ROOT / path).read_text()
        helper = COMBINED_HELPER.replace('        else error.message\n', QUERY_BRANCH + '        else error.message\n')
        self.assertEqual(1, gallery.count(helper))
        self.assertEqual(1, gallery.count('private fun commonsMetadataReason('))
        self.assertEqual(2, gallery.count('commonsMetadataReason(error)'))
        self.assertEqual(2, gallery.count('runOnUiThread {if(!isFinishing && !isDestroyed) {\n                    val reason='))
        self.assertNotIn('error.message==', gallery); self.assertNotIn('error.message ==', gallery)
        self.assertEqual(1, before_m04_composed_production(path, gallery).count(COMBINED_HELPER))
        producer = (ROOT / JAVA / 'CommonsAttribution.kt').read_text()
        for value in ('class QueryFailureException: IOException()', 'if (root.has("error")) throw QueryFailureException()',
                      'if (status != 200) throw HttpException(status)',
                      'if (bytes.size().toLong() + count > MAX_RESPONSE) throw ResponseLimitException()'):
            self.assertEqual(1, producer.count(value))
        self.assertNotIn('Commons metadata query failed', producer)

    def test_exact_projections_reject_changed_missing_duplicated_or_unrelated_source(self):
        for row in scope()['pr52_overlaps']:
            path = row['path']; content = (ROOT / path).read_bytes()
            with self.subTest(path=path), self.assertRaises(AssertionError):
                before_composed_m04(path, content + b'\n// unrelated\n')
            for edit in row['edits']:
                for bad in ('', edit['after'] * 2, edit['before']):
                    with self.subTest(path=path, mutation=bad[:30]), self.assertRaises(AssertionError):
                        reverse(path, before_diagnostic(path, content).replace(edit['after'].encode(), bad.encode(), 1),
                                scope()['pr52_overlaps'])
        for row in scope()['m04_overlaps']:
            content = (ROOT / row['path']).read_bytes()
            with self.assertRaises(AssertionError): as_standalone_m04_bytes(row['path'], content + b' ')

    def test_fragment_reversal_never_removes_corrupted_m04_production(self):
        for row in scope()['pr52_overlaps']:
            if row['kind'] != 'production': continue
            path = row['path']; text = (ROOT / path).read_text()
            for edit in row['edits']:
                for bad in ('', edit['after'] * 2, edit['before']):
                    with self.assertRaises(AssertionError):
                        before_m04_composed_production(path, text.replace(edit['after'], bad, 1))
            self.assertNotEqual(row['before_sha256'], digest(before_m04_composed_production(path, text + '\n// unrelated\n').encode()))

    def test_fixture_corruption_and_scope_expansion_fail_without_python_asserts(self):
        original_read = Path.read_bytes
        for kind in ('missing', 'duplicate', 'changed', 'expanded'):
            data = scope()
            if kind == 'missing': data['pr52_overlaps'].pop()
            if kind == 'duplicate': data['pr52_overlaps'].append(data['pr52_overlaps'][0])
            if kind == 'changed': data['m04_overlaps'][0]['after_sha256'] = '0' * 64
            if kind == 'expanded': data['pr52_overlaps'].append({'path': 'unrelated'})
            raw = json.dumps(data).encode()
            def read_bytes(path):
                return raw if path == FIXTURE else original_read(path)
            with patch.object(Path, 'read_bytes', read_bytes), self.assertRaises(AssertionError): scope()

    def test_new_flow_http_oracle_is_typed_and_every_other_original_m04_assertion_restores(self):
        path = 'Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt'
        content = (ROOT / path).read_bytes()
        self.assertIn(b'catch(error: CommonsAttribution.HttpException) {assertEquals(503,error.status);assertNull(error.message)}', content)
        restored = as_standalone_m04_bytes(path, content)
        self.assertIn(b'assertFalse(error is CommonsAttribution.QueryFailureException);assertEquals("Commons metadata: HTTP 503",error.message)', restored)
        row = next(row for row in scope()['m04_overlaps'] if row['path'] == path)
        self.assertEqual(1, len(row['edits']))
        self.assertEqual(row['before_sha256'], digest(restored))


if __name__ == '__main__': unittest.main()
