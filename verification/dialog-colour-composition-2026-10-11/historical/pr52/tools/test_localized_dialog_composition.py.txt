"""Exact PR49/C05/M02 composition; no runtime or linguistic acceptance implied."""
import hashlib
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import hungarian_attribution_c05_scope as c05
import commons_metadata_m02_scope as m02
import test_commons_copy_credit_errors as c04
from app_instrumentation_matrix import app_partition, PHASE_TIMEOUTS
from run_android_instrumentation import declared_tests

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tools/fixtures/localized_dialog_composition_scope.json'
FIXTURE_SHA256 = 'ba102b66c8fe729af855398961144225172985524b3873d121bc184d5f7e7f22'


def digest(content):
    return hashlib.sha256(content).hexdigest()


def composition_scope():
    raw = FIXTURE.read_bytes()
    if digest(raw) != FIXTURE_SHA256:
        raise AssertionError('The exact accepted producer union changed')
    return json.loads(raw)


class LocalizedDialogCompositionContracts(unittest.TestCase):
    def test_all_247_nonconflicting_producer_paths_keep_exact_bytes(self):
        rows = composition_scope()['inherited_unchanged_paths']
        self.assertEqual(247, len(rows))
        self.assertEqual(247, len({row['path'] for row in rows}))
        for row in rows:
            with self.subTest(path=row['path'], producer=row['producer']):
                self.assertEqual(row['sha256'], digest((ROOT / row['path']).read_bytes()))

    def test_all_116_jvm_and_installed_source_files_preserve_every_original_method_and_assertion(self):
        rows = composition_scope()['all_kotlin_test_sources']
        paths = {str(path.relative_to(ROOT)) for module in ('Paintroid', 'app')
                 for folder in ('test', 'androidTest')
                 for path in (ROOT / module / 'src' / folder).rglob('*.kt')}
        self.assertEqual(116, len(rows))
        self.assertEqual(paths, {row['path'] for row in rows})
        for row in rows:
            with self.subTest(path=row['path']):
                self.assertEqual(row['sha256'], digest((ROOT / row['path']).read_bytes()))

    def test_exact_sdk_aware_phase_union_and_all_original_deadlines_survive(self):
        self.assertEqual({'ordinary': 180, 'gallery-draft': 90, 'dialog': 300,
                          'vertical-english-manchu': 180,
                          'vertical-literary-chinese-emoji': 180, 'seed': 60, 'verify': 60},
                         PHASE_TIMEOUTS)
        app = ROOT / 'app/src/androidTest'
        for sdk, ordinary, native, completed in ((30, 15, 73, 22), (35, 16, 74, 30)):
            with self.subTest(sdk=sdk):
                methods = declared_tests(app, sdk_level=sdk)
                parts = app_partition(methods, sdk)
                counts = {'ordinary': ordinary, 'gallery-draft': 3,
                          'vertical-english-manchu': 2, 'vertical-literary-chinese-emoji': 2}
                if sdk == 35:
                    counts.update(dialog=5, seed=1, verify=1)
                self.assertEqual(counts, {name: len(items) for name, items in parts.items()})
                self.assertEqual(completed, len(set.union(*parts.values())))
                self.assertEqual(completed, sum(map(len, parts.values())))
                self.assertEqual(native, len(declared_tests(ROOT / 'Paintroid/src/androidTest', sdk_level=sdk)))
        self.assertEqual(6, len(declared_tests(app) - declared_tests(app, sdk_level=30)))

    def test_hungarian_is_exactly_17_replacements_and_one_independent_m02_addition(self):
        scope = c05.scope()
        self.assertEqual(17, len(scope['entries']))
        row = next(row for row in m02.fixture()['entries'] if row['path'] == c05.PATH)
        text = (ROOT / c05.PATH).read_text()
        self.assertEqual(1, text.count(row['line']))
        c05_only = m02.before_m02_catalogue(c05.PATH, text)
        self.assertEqual(scope['after_sha256'], c05.digest(c05_only))
        base = c05.before_c05(c05.PATH, c05_only)
        self.assertEqual(scope['before_sha256'], c05.digest(base))
        self.assertEqual(row['before_sha256'], c05.digest(base))
        actual = {node.attrib['name']: node for node in ET.fromstring(text).findall('string')}
        original = {node.attrib['name']: node for node in ET.fromstring(base).findall('string')}
        self.assertEqual({'commons_metadata_http_error'}, actual.keys() - original.keys())
        self.assertEqual(set(), original.keys() - actual.keys())
        self.assertEqual({row['key'] for row in scope['entries']},
                         {key for key in original if (original[key].attrib, original[key].text) !=
                          (actual[key].attrib, actual[key].text)})

    def test_resource_reversals_commute_for_every_m02_catalogue_and_restore_pinned_endpoints(self):
        for row in m02.fixture()['entries']:
            path = row['path']
            text = (ROOT / path).read_text()
            with self.subTest(path=path):
                first = c05.before_c05(path, m02.before_m02_catalogue(path, text))
                second = m02.before_m02_catalogue(path, c05.before_c05(path, text))
                self.assertEqual(first, second)
                self.assertEqual(row['before_sha256'], c05.digest(first))

    def test_whole_file_c04_guard_still_rejects_m02_and_unrelated_hungarian_corruption(self):
        path = c05.PATH
        original = (ROOT / path).read_text()
        m02_row = next(row for row in m02.fixture()['entries'] if row['path'] == path)
        old = next(row for row in json.loads((c04.EVIDENCE / 'source-scope.json').read_text())['catalogues']
                   if row['path'] == path)
        def verify(text):
            self.assertEqual(old['before_sha256'], c05.digest(c04.catalogue_before_copy_credit_and_f01(path, text)))
        verify(original)
        for mutation in ('', m02_row['line'] * 2, m02_row['line'].replace('HTTP ', 'HTTPX ')):
            with self.subTest(mutation=mutation), self.assertRaises(AssertionError):
                verify(original.replace(m02_row['line'], mutation, 1))
        with self.assertRaises(AssertionError):
            verify(original.replace('</resources>', '<!-- unapproved -->\n</resources>'))

    def test_disjoint_about_and_m02_source_reversals_commute_and_restore_original_c04_hashes(self):
        title = json.loads((ROOT / 'verification/localized-dialog-layout-2026-10-11/minimal-successor/about-title-scope.json').read_text())
        def before_dialog(path, content):
            if path != title['path']:
                return content
            self.assertEqual(title['after_sha256'], digest(content))
            self.assertEqual(1, content.count(title['after_fragment'].encode()))
            self.assertEqual(0, content.count(title['before_fragment'].encode()))
            restored = content.replace(title['after_fragment'].encode(), title['before_fragment'].encode(), 1)
            self.assertEqual(title['before_sha256'], digest(restored))
            return restored
        for row in json.loads((c04.EVIDENCE / 'source-scope.json').read_text())['unchanged_semantics_files']:
            path = row['path']
            content = (ROOT / path).read_bytes()
            with self.subTest(path=path):
                first = before_dialog(path, m02.before_m02_producer(path, content))
                second = m02.before_m02_producer(path, before_dialog(path, content))
                self.assertEqual(first, second)
                self.assertEqual(row['sha256'], digest(first))


if __name__ == '__main__':
    unittest.main()
