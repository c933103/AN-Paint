"""Bounded complete Swedish statements; actual consumers also have JVM tests."""
from copy import deepcopy
import json
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues

class SwedishPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = fixture('swedish_priority_current_wording.json')
        cls.keys = set(cls.data['values'])
        require_wording_shape(cls.data, cls.keys, {'default', 'sv'})
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text() for tag, folder in [('default', 'values'), ('sv', 'values-sv')]}
        cls.strings = {n.get('name'): n.text.strip('"') for n in ET.fromstring(cls.xml['sv']) if n.tag == 'string'}

    def test_complete_values_attributes_formats_and_newlines(self):
        for key, values in self.data['values'].items():
            for tag, expected in values.items():
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, expected, self.data['constraints'][key])
        self.assertEqual([], catalogues.validate_catalogue('sv'))

    def test_current_fixture_is_nonempty_and_has_all_safety_keys(self):
        self.assertGreater(len(self.keys), 100)
        manifest = json.loads((catalogues.ROOT / 'translations/string-importance.json').read_text())
        safety = next(t['keys'] for t in manifest['tiers'] if t['id'] == 'P0')
        self.assertTrue(all(k.removeprefix('string/') in self.strings for k in safety))
        self.assertIn('formats22_at_least_frames', self.keys)
        self.assertIn('ui_load_image', self.keys)

    def test_missing_empty_or_duplicate_value_and_markup_fail(self):
        for key in self.keys:
            for mutation in ('missing', 'duplicate', 'truncated', 'markup', 'format-flag'):
                root = ET.fromstring(self.xml['sv']); node = root.find(f"./string[@name='{key}']")
                if mutation == 'missing': root.remove(node)
                elif mutation == 'duplicate': root.append(deepcopy(node))
                elif mutation == 'truncated': node.text = node.text[:-1]
                elif mutation == 'markup': ET.SubElement(node, 'b').text, node.text = node.text, None
                else: node.set('formatted', 'true' if node.get('formatted') == 'false' else 'false')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, self.data['values'][key]['sv'], self.data['constraints'][key])

    def test_missing_fixture_locale_or_constraint_fails(self):
        for mutation in ('key', 'locale', 'constraint', 'empty'):
            changed = deepcopy(self.data); key = 'ui_keep_editing23'
            if mutation == 'key': del changed['values'][key]
            elif mutation == 'locale': del changed['values'][key]['sv']
            elif mutation == 'constraint': del changed['constraints'][key]
            else: changed['values'][key]['sv'] = ''
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                require_wording_shape(changed, self.keys, {'default', 'sv'})

    def test_actual_command_names_in_recovery_and_export_guidance(self):
        s = self.strings
        self.assertEqual(('Arkiv', 'Spara', 'Spara som…', 'Öppna bild…'), tuple(s[k] for k in ('ui_menu_file', 'ui_save', 'save20_title', 'ui_load_image')))
        for key in ('ui_a_separate_recovery_copy_has_been_kept_use', 'ui_autosave_is_paused_to_protect_that_draft_use'):
            self.assertIn(s['ui_export_recovery_copy'].removesuffix('…'), s[key])
        self.assertIn('Arkiv > Öppna bild', s['ui_recovery_copy_exported_extract_canvas_png_from_the'])
        self.assertIn('canvas.png', s['ui_recovery_copy_exported_extract_canvas_png_from_the'])
        self.assertIn('Spara eller Spara som', s['ui_export_did_not_save23'])
        self.assertIn('Filformat: PNG / JPEG', s['ui_autosave_is_paused_to_protect_that_draft_use'])

    def test_frame_counts_include_the_localized_lower_bound(self):
        for count in (2, 21, 101):
            exact = self.strings['formats22_animation_message'].replace('%1$s', 'GIF').replace('%2$s', str(count))
            lower = self.strings['formats22_at_least_frames'].replace('%1$d', str(count))
            inexact = self.strings['formats22_animation_message'].replace('%1$s', 'GIF').replace('%2$s', lower)
            self.assertIn(f'innehåller {count} bildrutor.', exact)
            self.assertIn(f'innehåller minst {count} bildrutor.', inexact)
            self.assertIn('bevarar inte animeringar.', exact)
        self.assertIn('om den innehåller flera bildrutor', self.strings['formats22_animation_unknown'])

    def test_fixed_tool_and_action_meanings_are_distinct(self):
        expected = {'ui_line': 'Linje', 'ui_watercolor': 'Akvarell', 'ui_outline': 'Kontur', 'ui_solid_fill': 'Enfärgad fyllning', 'ui_keep_editing23': 'Fortsätt redigera', 'ui_swap23': 'Byt plats på färgerna'}
        for key, value in expected.items(): self.assertEqual(value, self.strings[key])
        self.assertNotEqual(self.strings['ui_keep_editing23'], self.strings['ui_cancel'])
        self.assertIn('osparade ändringar', self.strings['ui_your_current_image_has_unsaved_changes'])

    def test_conditional_safety_and_retained_data_are_explicit(self):
        s = self.strings
        for key in ('ui_d_d_pixels_2f_mp_exceeds_the_current', 'ui_there_is_not_enough_memory_for_this_operation'):
            self.assertIn('Ingen automatisk storleksändring gjordes.', s[key])
        self.assertIn('Originalfilen förblir oförändrad.', s['ui_sampled_resize_memory_explanation'])
        self.assertIn('Bildmontaget är oförändrat.', s['ui_assembly_source_memory_floor'])
        self.assertIn('har behållits', s['ui_history_unavailable34'])
        self.assertIn('visas på engelska.', s['language20_translation_note'])

if __name__ == '__main__': unittest.main()
