"""Whole Swedish P1 messages, context distinctions and deliberately open fallback.

The independent review receipt is archived separately. These are current product
expectations, not a fluency certificate or a reconstruction of historical source.
"""
from copy import deepcopy
import json
import unittest
import xml.etree.ElementTree as ET

import current_localization_contracts as contracts
import translation_catalogues as catalogues
# Frozen pairs stay historical; exact current warning successors are separately receipt-bound.
from memory_warning_source_review import current_source_expectation

HELD = 'ui_foreground_background_colour_palette'
SOURCE_ONLY = {
    'ui_1_px', 'ui_actual_size_100', 'ui_collapse_colour_palette',
    'ui_expand_colour_palette', 'ui_heights', 'ui_hide_editor_controls',
    'ui_insert_image_into_canvas', 'ui_left_arrow_collapse', 'ui_new_colour',
    'ui_pinch_and_pan_mode', 'ui_reset_to_black_white', 'ui_show_editor_controls',
    'ui_tool_categories', 'ui_trim_expand_canvas_by_touch',
}


class SwedishRemainingP1WordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = contracts.fixture('swedish_remaining_p1_wording.json')
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text()
                   for tag, folder in [('default', 'values'), ('sv', 'values-sv')]}
        cls.strings = catalogues.read_strings(catalogues.RES / 'values-sv/strings.xml')

    def test_complete_reviewed_values_attributes_and_formats(self):
        keys = set(self.data['values'])
        self.assertEqual(148, len(keys))
        contracts.require_wording_shape(self.data, keys, {'default', 'sv'})
        for key, values in self.data['values'].items():
            for tag, expected in values.items():
                with self.subTest(key=key, tag=tag):
                    contracts.require_string(self.xml[tag], key, current_source_expectation(key, tag, expected), self.data['constraints'][key])
        self.assertEqual([], catalogues.validate_catalogue('sv'))

    def test_p1_gap_and_source_only_limits_remain_explicit(self):
        manifest = json.loads((catalogues.ROOT / 'translations/string-importance.json').read_text())
        p1 = {key.removeprefix('string/') for tier in manifest['tiers']
              if tier['id'] == 'P1' for key in tier['keys']}
        self.assertEqual(set(), p1 - self.strings.keys())
        self.assertTrue(set(self.data['values']) <= p1)
        self.assertEqual(SOURCE_ONLY, set(self.data['source_semantics_only']))
        self.assertEqual(14, len(self.data['source_semantics_only']))
        self.assertTrue(SOURCE_ONLY <= self.data['values'].keys())
        self.assertEqual(HELD, self.data['withheld']['key'])
        self.assertIn(HELD, self.strings)  # Current palette semantics are checked by SwedishExtendedWordingTests.
        contracts.require_string(self.xml['default'], HELD, self.data['withheld']['default'])
        previous = contracts.fixture('swedish_priority_current_wording.json')
        self.assertFalse(set(previous['values']) & set(self.data['values']))

    def test_every_message_rejects_missing_duplicate_fragment_or_markup(self):
        # Minimal resources keep these mutations independent of catalogue size.
        for key, values in self.data['values'].items():
            for tag, historical in values.items():
                expected = current_source_expectation(key, tag, historical)
                node = ET.fromstring(self.xml[tag]).find(f"./string[@name='{key}']")
                for mutation in ('missing', 'duplicate', 'fragment', 'markup', 'format-flag'):
                    root = ET.Element('resources'); changed = deepcopy(node)
                    if mutation != 'missing': root.append(changed)
                    if mutation == 'duplicate': root.append(deepcopy(changed))
                    elif mutation == 'fragment': changed.text = changed.text[:-1]
                    elif mutation == 'markup':
                        ET.SubElement(changed, 'b').text, changed.text = changed.text, None
                    elif mutation == 'format-flag':
                        changed.set('formatted', 'true' if changed.get('formatted') == 'false' else 'false')
                    with self.subTest(key=key, tag=tag, mutation=mutation), self.assertRaises(ValueError):
                        contracts.require_string(ET.tostring(root, encoding='unicode'), key, expected,
                                                 self.data['constraints'][key])

    def test_argument_indexes_types_precision_and_grouping_are_required(self):
        for key, values in self.data['values'].items():
            expected = values['sv']
            tokens = list(catalogues.FORMAT_TOKEN.finditer(expected))
            for token in tokens:
                for replacement in ('', '%99$s', '%1$d'):
                    changed = expected[:token.start()] + replacement + expected[token.end():]
                    if changed == expected: continue
                    root = ET.Element('resources')
                    ET.SubElement(root, 'string', self.data['constraints'][key]['attributes']).text = changed
                    with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                        contracts.require_string(ET.tostring(root, encoding='unicode'), key, expected,
                                                 self.data['constraints'][key])

    def test_actual_navigation_names_and_action_distinctions(self):
        s = {key: value.strip('"') for key, value in self.strings.items()}
        self.assertEqual(f"Kopiera ett område eller välj {s['ui_draw26']} → {s['ui_category_insert']} → {s['ui_other_images34']}.",
                         s['ui_paste_hint34'])
        self.assertIn(f"I läget {s['ui_navigate']}", s['ui_drawing_canvas_pinch_and_move_two_fingers_to'])
        self.assertEqual('Anpassa bilden till ritytan', s['ui_fit_selection34'])
        self.assertEqual('Fäst markeringen', s['ui_commit_selection'])
        self.assertEqual('Radera markeringen', s['ui_delete_selection'])
        self.assertNotEqual(s['ui_apply_crop'], s['ui_reset_crop'])
        self.assertEqual(('Alla', 'Inga'), (s['ui_all'], s['ui_none']))

    def test_no_automatic_resize_or_success_is_invented(self):
        s = self.strings
        for key, clause in {
            'colour_converter_unavailable': 'Bilden importerades inte.',
            'commons_svg_original_size_too_large': 'Ingen storleksändring gjordes.',
            'commons_svg_original_size_unavailable': 'Ingen storlek baserad på ritytan användes i stället.',
            'ui_the_full_image_and_working_buffers_exceed_the': 'Originalfilen förblir oförändrad.',
            'ui_choose_a_smaller_output_copy_the_source_images': 'Källbilderna och beskärningsinställningarna behålls i originalupplösningen.',
            'ui_codec_resize_memory_floor': 'Även en mindre utdatabild kan kräva mer minne',
            'ui_no_resize_fits_decoder_memory': 'Avbryt och använd en mindre källbild.',
        }.items():
            with self.subTest(key=key): self.assertIn(clause, s[key])
        self.assertIn('512 MiB', s['formats22_import_limit'])
        self.assertIn('bilddata som Base64-text', s['ui_this_file_is_not_a_supported_image_use'])
        self.assertNotIn('bildtext', s['ui_this_file_is_not_a_supported_image_use'])

    def test_palette_gestures_and_geometry_remain_distinct(self):
        s = self.strings
        for key in ('ui_colour_palette_tap_for_foreground_hold_for_background',
                    'ui_colour_tap_foreground_hold_background'):
            self.assertIn('Tryck för att välja förgrundsfärg.', s[key])
            self.assertIn('Tryck och håll för att välja bakgrundsfärg.', s[key])
        self.assertEqual('Beskärningsområdet måste ligga inom ritytan.', s['ui_crop_must_stay_inside_the_canvas'])
        self.assertEqual('Beskärningsområdet måste ligga inom bilden.', s['ui_the_crop_must_stay_inside_the_image'])
        self.assertIn('minst en bildpunkt', s['ui_the_crop_must_contain_at_least_one_pixel'])
        self.assertIn('noll eller större', s['ui_trim_amounts_must_be_zero_or_greater'])
        self.assertEqual(r'%1$.0f × %2$.0f px\n%3$.1f°', s['ui_0f_0f_px_1f'])


if __name__ == '__main__':
    unittest.main()
