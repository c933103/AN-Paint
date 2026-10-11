"""C05 source/successor contracts; matching wording is not linguistic approval."""
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from commons_metadata_m02_scope import before_m02_catalogue
import hungarian_attribution_c05_scope as c05
import test_commons_copy_credit_errors as c04
import translation_catalogues as catalogues

ROOT = Path(__file__).resolve().parents[1]
KEYS = ['gallery_copy_credit', 'gallery_description', 'gallery_edit_credits',
        'gallery_credit_copied', 'gallery_credit_saved', 'ui_image_credits',
        'ui_about_credits23', 'ui_credits_terms', 'ui_icons_fonts_artwork_credits',
        'ui_open_source_credits_and_notices', 'ui_gimp_translations31',
        'ui_catrobat_s_own_artwork_uses_cc_by_sa', 'ui_irasutoya_help34',
        'ui_openclipart_help34', 'ui_help23', 'ui_add_up_to_20_images_with_android_s',
        'ui_the_arrow_on_the_left_directly_below_the']


class HungarianAttributionC05Test(unittest.TestCase):
    def setUp(self):
        self.scope = c05.scope()
        self.text = (ROOT / c05.PATH).read_text()

    def test_exact_17_named_values_restore_the_entire_settled_base(self):
        self.assertEqual(KEYS, [r['key'] for r in self.scope['entries']])
        self.assertEqual([f'AN-W05-C05-HU-{n:02}' for n in range(1, 18)],
                         [r['id'] for r in self.scope['entries']])
        self.assertEqual(c05.PATH, self.scope['path'])
        self.assertEqual('691f8870649a1d21d1441f4e3d0e795660b23e9a', self.scope['source_commit'])
        # Remove only M02's separately pinned single addition before the
        # unchanged C05 whole-file endpoints; keep all 17 replacements required.
        c05_only = before_m02_catalogue(c05.PATH, self.text)
        self.assertEqual(self.scope['after_sha256'], c05.digest(c05_only))
        self.assertEqual(self.scope['before_sha256'], c05.digest(c05.before_c05(c05.PATH, c05_only)))

    def test_every_item_preserves_attributes_placeholders_newlines_and_legal_identifiers(self):
        for row in self.scope['entries']:
            with self.subTest(item=row['id']):
                a, b = ET.fromstring(row['before']), ET.fromstring(row['after'])
                self.assertEqual(a.attrib, b.attrib)
                self.assertEqual(0, len(a)); self.assertEqual(0, len(b))
                self.assertNotEqual(a.text, b.text)
                self.assertEqual(catalogues.placeholders(a.text), catalogues.placeholders(b.text))
                self.assertEqual(a.text.count('\\n'), b.text.count('\\n'))
                self.assertNotIn('jóváírás', b.text.lower())
                self.assertEqual([], catalogues.android_string_errors(b.text))
                self.assertEqual([], catalogues.format_string_errors(b.text, b.get('formatted') != 'false'))
                for literal in ('Catrobat', 'AGPL', 'CC BY-SA 4.0', 'CC0', 'Irasutoya', '21', 'Openclipart', 'Wikimedia Commons'):
                    self.assertEqual(a.text.count(literal), b.text.count(literal), literal)

    def test_changed_instruction_references_match_the_actual_new_labels(self):
        values = catalogues.read_strings(ROOT / c05.PATH)
        for key in ('gallery_description', 'ui_catrobat_s_own_artwork_uses_cc_by_sa',
                    'ui_irasutoya_help34', 'ui_openclipart_help34',
                    'ui_the_arrow_on_the_left_directly_below_the'):
            for label in ('ui_about_credits23', 'ui_image_credits'):
                self.assertIn(values[label], values[key], (key, label))
        for label in ('gallery_copy_credit', 'gallery_edit_credits'):
            self.assertIn(values[label], values['gallery_description'])
        self.assertIn(values['ui_credits_terms'], values['ui_the_arrow_on_the_left_directly_below_the'])
        self.assertIn(values['ui_about_credits23'], values['ui_help23'])
        self.assertIn(values['ui_about_credits23'], values['ui_add_up_to_20_images_with_android_s'])

    def _assert_c04(self, text):
        row = next(r for r in json.loads((c04.EVIDENCE / 'source-scope.json').read_text())['catalogues']
                   if r['path'] == c05.PATH)
        historical = c04.catalogue_before_copy_credit_and_f01(c05.PATH, text)
        self.assertEqual(row['before_sha256'], c05.digest(historical))

    def test_composed_historical_guard_rejects_each_reversion_deletion_and_duplication(self):
        self._assert_c04(self.text)
        for row in self.scope['entries']:
            for bad in (row['before'], '', row['after'] * 2):
                with self.subTest(item=row['id'], mutation=bad[:40]):
                    with self.assertRaises(AssertionError):
                        self._assert_c04(self.text.replace(row['after'], bad, 1))

    def test_unrelated_content_and_non_hungarian_catalogues_have_no_waiver(self):
        with self.assertRaises(AssertionError):
            self._assert_c04(self.text.replace('</resources>', '<!-- unrelated -->\n</resources>'))
        path = 'Paintroid/src/main/res/values-fr/strings.xml'
        original = (ROOT / path).read_text()
        self.assertEqual(original, c05.before_c05(path, original))
        self.assertEqual(original + 'bad', c05.before_c05(path, original + 'bad'))

    def test_changed_missing_duplicate_or_expanded_scope_is_rejected_even_under_python_O(self):
        original_read = Path.read_bytes
        for mutate in ('missing', 'duplicate', 'changed', 'expanded'):
            data = json.loads(json.dumps(self.scope))
            if mutate == 'missing': data['entries'].pop()
            if mutate == 'duplicate': data['entries'].append(data['entries'][0])
            if mutate == 'changed': data['entries'][0]['after'] += ' '
            if mutate == 'expanded': data['entries'].append({'key': 'unrelated'})
            raw = json.dumps(data).encode()
            def read_bytes(path):
                return raw if path == c05.FIXTURE else original_read(path)
            with self.subTest(mutation=mutate), patch.object(Path, 'read_bytes', read_bytes):
                with self.assertRaisesRegex(AssertionError, '17-entry C05 scope fixture changed'):
                    c05.before_c05(c05.PATH, self.text)

    def test_c03_two_transition_chain_and_seven_independent_negative_controls(self):
        data = json.loads((ROOT / 'verification/help-commons-provider-2026-10-09/translations.json').read_text())
        for tag, row in data['translations'].items():
            actual = catalogues.read_strings(ROOT / row['catalogue'])['ui_help23']
            historical = c05.historical_c03_help(tag, actual, row)
            self.assertEqual(row['after_help_sha256'], c05.digest(historical))
            self.assertEqual(row['before_help_sha256'],
                             c05.digest(historical.replace(row['after_segment'], row['before_segment'], 1)))
        row = data['translations']['hu']
        actual = catalogues.read_strings(ROOT / c05.PATH)['ui_help23']
        mutations = [actual + ' ', 'Changed. ' + actual,
                     actual.replace(row['caption'], '', 1), actual.replace('Openclipart', 'Changed', 1),
                     actual.replace(c05.NEW_ABOUT, c05.OLD_ABOUT, 1),
                     actual.replace(c05.NEW_ABOUT, c05.NEW_ABOUT * 2, 1)]
        for bad in mutations:
            with self.subTest(mutation=bad[:60]), self.assertRaises(AssertionError):
                c05.historical_c03_help('hu', bad, row)
        other = data['translations']['fr']
        bad = catalogues.read_strings(ROOT / other['catalogue'])['ui_help23'] + ' '
        self.assertNotEqual(other['after_help_sha256'], c05.digest(c05.historical_c03_help('fr', bad, other)))

    def test_android_tests_keep_existing_languages_and_add_hungarian_real_routes(self):
        tests = ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local'
        reach = (tests / 'GalleryControlReachabilityTest.kt').read_text()
        self.assertIn('listOf("hu","fr","hak-Latn-TW","ar","vi-Hani","bo","dz","mn-Mong","mnc-Mong","lzh-Hant")', reach)
        for name in ('portraitControlsAtNormalText', 'portraitControlsAtLargeText',
                     'narrowControlsAtLargeText', 'landscapeControlsAtLargeText'):
            self.assertIn('fun ' + name, reach)
        help_test = (tests / 'CommonsHelpProviderTranslationTest.kt').read_text()
        self.assertIn('listOf("hu","fr","ja","mn-Mong","vi-Hani","am")', help_test)
        actual = (tests / 'HungarianAttributionC05Test.kt').read_text()
        for contract in ('gallery_edit_credits', 'gallery_credit_copy', 'gallery_credit_save',
                         'gallery_credit_done', 'terms_text', 'terms_done', 'EditorTestNavigation.named',
                         'clipboard.primaryClip', 'Resources.getSystem().configuration.fontScale',
                         'list.setSelection(index)', 'list.performItemClick(row,index,index.toLong())',
                         'terms_copy', 'terms_more', 'requestRectangleOnScreen',
                         'text_fits_view', 'initial_fully_visible', 'ancestor_chain_before',
                         'fully_visible_after_rectangle_request', 'rectangle_reveal_is_not_native_input_acceptance'):
            self.assertIn(contract, actual)


if __name__ == '__main__':
    unittest.main()
