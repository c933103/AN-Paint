"""Bounded Esperanto wording and source contracts, not fluency or device acceptance."""
from copy import deepcopy
import json
import re
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues

FIXTURE = 'esperanto_priority_current_wording.json'
COUNT = 'ui_d_d_px_d_pixels_2f_mp'
KEYS = {'ui_trim_amounts_must_be_zero_or_greater', 'ui_reset_crop', 'ui_trim_amounts_must_fit_inside_each_image_use', 'ui_the_crop_must_contain_at_least_one_pixel', 'ui_could_not_apply_the_crop', 'ui_trim_expand_canvas_by_touch', 'ui_d_d_px_d_pixels_2f_mp', 'ui_apply_crop', 'ui_crop', 'ui_the_crop_must_stay_inside_the_image', 'ui_choose_a_smaller_output_copy_the_source_images', 'ui_enter_a_trim_amount_for_every_edge', 'ui_the_trim_would_remove_the_entire_image', 'ui_crop_must_stay_inside_the_canvas', 'ui_enter_all_four_trim_amounts', 'ui_crop_preview_drag_an_edge_or_corner_drag'}
TAGS = {'default', 'eo'}
CLASSIC = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'


class EsperantoPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture(FIXTURE), KEYS, TAGS)
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in {'default': 'values', 'eo': 'values-b+eo'}.items()}
        cls.strings = {tag: {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(xml)
                            if n.tag == 'string'} for tag, xml in cls.xml.items()}
        cls.activity = (CLASSIC / 'ClassicPaintActivity.kt').read_text(encoding='utf-8')

    def test_complete_bilingual_values_attributes_newlines_and_typed_arguments(self):
        for key in KEYS:
            self.assertEqual(TAGS, set(self.data['constraints'][key]))
            for tag, expected in self.data['values'][key].items():
                constraints = self.data['constraints'][key][tag]
                self.assertEqual({'attributes', 'formatted', 'placeholders', 'escaped_newline_count'}, set(constraints))
                self.assertEqual(catalogues.placeholders(self.data['values'][key]['default']),
                                 catalogues.placeholders(expected))
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, expected, constraints)

    def test_fixture_requires_all_keys_locales_text_and_constraints(self):
        for key in KEYS:
            for mutation in ('key', 'locale', 'empty', 'constraint'):
                changed = deepcopy(self.data)
                if mutation == 'key': del changed['values'][key]
                elif mutation == 'locale': del changed['values'][key]['eo']
                elif mutation == 'empty': changed['values'][key]['eo'] = ''
                else: del changed['constraints'][key]
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_wording_shape(changed, KEYS, TAGS)

    def test_missing_duplicate_truncated_or_retyped_resource_is_rejected(self):
        for key in KEYS:
            expected = self.data['values'][key]['eo']
            constraints = self.data['constraints'][key]['eo']
            for mutation in ('missing', 'duplicate', 'truncated', 'format', 'markup'):
                root = ET.fromstring(self.xml['eo'])
                node = root.find(f"./string[@name='{key}']")
                if mutation == 'missing': root.remove(node)
                elif mutation == 'duplicate': root.append(deepcopy(node))
                elif mutation == 'truncated': node.text = node.text[:-1]
                elif mutation == 'format': node.set('formatted', 'false' if node.get('formatted') != 'false' else 'true')
                else: ET.SubElement(node, 'b').text, node.text = node.text, None
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, expected, constraints)

    def test_syntax_or_argument_changes_cannot_hide_behind_matching_expected_text(self):
        for key in KEYS:
            for suffix in (' %9$d', " '"):
                root = ET.fromstring(self.xml['eo'])
                node = root.find(f"./string[@name='{key}']")
                node.text += suffix
                with self.subTest(key=key, suffix=suffix), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, node.text,
                                   self.data['constraints'][key]['eo'])

    def test_complete_catalogue_and_android_syntax(self):
        self.assertEqual([], catalogues.validate_catalogue('eo', require_complete=True))
        for tag, xml in self.xml.items():
            root = ET.fromstring(xml)
            identities = [(n.tag, n.get('name')) for n in root]
            self.assertEqual(len(identities), len(set(identities)))
            for node in root.findall('string'):
                text = ''.join(node.itertext())
                with self.subTest(tag=tag, key=node.get('name')):
                    self.assertEqual([], catalogues.android_string_errors(text))
                    self.assertEqual([], catalogues.format_string_errors(text, node.get('formatted') != 'false'))

    def test_pixel_count_is_count_neutral_with_unchanged_numeric_contract(self):
        self.assertEqual('%1$d × %2$d px · Nombro de bilderoj: %3$,d (%4$.2f MP)', self.strings['eo'][COUNT])
        source = (CLASSIC / 'ImageImport.kt').read_text(encoding='utf-8')
        self.assertIn('width > 0 && height > 0', source)
        self.assertIn('val pixels: Long get() = width.toLong() * height', source)
        self.assertIn('ui(R.string.' + COUNT + ', width, height, pixels, pixels / 1_000_000.0)', source)

    def test_crop_spelling_matches_existing_crop_commands(self):
        self.assertEqual('Stuci bildon', self.strings['eo']['ui_crop_image'])
        self.assertEqual('Stuci al elekto', self.strings['eo']['ui_crop_to_selection'])
        for key in KEYS - {COUNT}:
            self.assertIn('stuc', self.strings['eo'][key].lower())
            self.assertNotIn('stuĉ', self.strings['eo'][key].lower())

    def test_every_change_remains_in_priority_scope(self):
        importance = json.loads((catalogues.ROOT / 'translations/string-importance.json').read_text())
        priorities = {key: tier['id'] for tier in importance['tiers'] for key in tier['keys']}
        for key in KEYS:
            self.assertIn(priorities['string/' + key], {'P0', 'P1'})


if __name__ == '__main__':
    unittest.main()
