"""Current Swedish catalogue coverage and complete critical-message regressions.

These tests are not a linguistic certificate. Unused ambiguous legacy keys and
source-correction dependencies stay explicit rather than being counted accepted.
"""
from copy import deepcopy
import unittest
import xml.etree.ElementTree as ET
import current_localization_contracts as contracts
import translation_catalogues as catalogues


def identities(xml):
    return {(e.tag, e.get('name')) for e in ET.fromstring(xml)
            if e.get('translatable') != 'false'}


class SwedishExtendedWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = contracts.fixture('swedish_extended_wording.json')
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text()
                   for tag, folder in [('default', 'values'), ('sv', 'values-sv')]}
        cls.strings = catalogues.read_strings(catalogues.RES / 'values-sv/strings.xml')

    def test_every_current_identity_exists_except_named_source_holds(self):
        source, target = (identities(self.xml[t]) for t in ('default', 'sv'))
        held = {('string', k) for k in self.data['held_missing']}
        self.assertEqual(held, source - target)
        self.assertFalse(target - source)
        self.assertEqual(['ui_main23'], self.data['present_held'])
        self.assertEqual('Huvud', self.strings['ui_main23'])
        self.assertEqual([], catalogues.validate_catalogue('sv'))

    def test_complete_critical_values_and_format_contracts(self):
        contracts.require_wording_shape(self.data, set(self.data['values']), {'default', 'sv'})
        for key, values in self.data['values'].items():
            for tag, expected in values.items():
                with self.subTest(key=key, tag=tag):
                    contracts.require_string(self.xml[tag], key, expected, self.data['constraints'][key])

    def test_missing_full_message_fragment_markup_and_format_mutations_fail(self):
        for key, values in self.data['values'].items():
            node = ET.fromstring(self.xml['sv']).find(f"./string[@name='{key}']")
            for mutation in ('missing', 'duplicate', 'fragment', 'markup', 'format'):
                root = ET.Element('resources'); changed = deepcopy(node)
                if mutation != 'missing': root.append(changed)
                if mutation == 'duplicate': root.append(deepcopy(changed))
                elif mutation == 'fragment': changed.text = changed.text[:-1]
                elif mutation == 'markup': ET.SubElement(changed, 'b').text, changed.text = changed.text, None
                elif mutation == 'format': changed.set('formatted', 'true' if changed.get('formatted') == 'false' else 'false')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    contracts.require_string(ET.tostring(root, encoding='unicode'), key, values['sv'], self.data['constraints'][key])

    def test_crop_singular_plural_keep_full_conditional_movement_warning(self):
        entry = self.data['plural']
        for tag in ('default', 'sv'):
            nodes = ET.fromstring(self.xml[tag]).findall(f"./plurals[@name='{entry['key']}']")
            self.assertEqual(1, len(nodes))
            items = nodes[0].findall('item')
            self.assertEqual(['one', 'other'], [n.get('quantity') for n in items])
            self.assertEqual(entry[tag], {n.get('quantity'): n.text for n in items})
            for node in items:
                self.assertEqual({'%1$d': 1, '%2$d': 1, '%3$d': 1}, catalogues.placeholders(node.text))
        for value in entry['sv'].values():
            self.assertIn('kan bilder som är fästa vid dem flyttas.', value)
            self.assertEqual(1, value.count('\\n'))
        self.assertIn('%3$d bild.', entry['sv']['one'])
        self.assertIn('%3$d bilder.', entry['sv']['other'])

    def test_active_help_navigation_matches_actual_controls(self):
        s = {k: v.strip('"') for k, v in self.strings.items()}
        help_text = s['ui_help23']
        for key in ('ui_menu_view', 'ui_navigate', 'ui_draw26', 'ui_drawing23', 'ui_category_selection',
                    'ui_category_insert', 'ui_swap23', 'ui_reset_bw23', 'ui_use_colour', 'ui_add_colour26',
                    'ui_advanced', 'ui_pixel_grid33', 'ui_cursor_drawing32', 'ui_about_credits23', 'commons_blank_maps'):
            self.assertIn(s[key], help_text, key)
        navigation = f"{s['ui_menu_file']} → {s['ui_about_credits23']} → {s['ui_image_credits']}"
        for key in ('gallery_description', 'ui_irasutoya_help34', 'ui_openclipart_help34'):
            self.assertIn(navigation, s[key])
            self.assertIn(s['gallery_use_image'], s[key])
        self.assertIn(s['gallery_copy_credit'], s['gallery_description'])
        self.assertEqual('@string/ui_cursor_help31', s['ui_cursor_help29'])

    def test_behavioural_distinctions_are_not_flattened(self):
        s = self.strings
        self.assertEqual('Färghjul', s['ui_wheel'])
        self.assertEqual('Överkant', s['ui_top'])
        self.assertEqual('Rund', s['ui_round'])
        self.assertIn('Jämna ut frihandsdrag', s['ui_smooth_freehand_strokes'])
        self.assertIn('Överlappning är tillåten här.', s['ui_assembly_position_help'])
        self.assertIn('Övriga bilder behåller sina nuvarande positioner.', s['ui_assembly_position_help'])
        self.assertIn('Bilder som importerats senare ritas ovanpå.', s['ui_assembly_position_help'])
        self.assertIn('Beskärningar och storlekar förblir oförändrade.', s['ui_assembly_position_help'])
        self.assertIn('Bilden importerades inte.', s['gallery_image_component_unavailable'])
        self.assertIn('kan minska filstorleken utan att ändra bildpunkterna', s['formats22_tiff_description'])
        self.assertIn('antiAlias=false; strokeDashArray=none; background=#FFFFFF.', s['commons_import_svg_changes'])
        self.assertIn('background=#FFFFFF', s['commons_import_raster_changes'])

    def test_assembly_help_preserves_separate_modes_and_actual_control_labels(self):
        s = {k: v.strip('"') for k, v in self.strings.items()}
        value = s['ui_add_up_to_20_images_with_android_s']
        paragraphs = value.split(r'\n\n')
        self.assertEqual(8, len(paragraphs))
        self.assertIn('Vid fästning börjar den första bilden i origo och överlappningar avvisas.', paragraphs[2])
        self.assertIn('räknat från noll', paragraphs[3])
        self.assertIn('Övriga bilder behåller sina positioner och överlappningar är tillåtna.', paragraphs[3])
        self.assertIn('kan flyttas för att fylla luckan', paragraphs[5])
        for key in ('ui_assembly_exact_position', 'ui_crop_image', 'ui_batch_crop', 'ui_reset_crop',
                    'ui_same_width', 'ui_same_height', 'ui_smallest', 'ui_largest',
                    'ui_restore_original_sizes', 'ui_unplace', 'ui_remove', 'ui_show_all',
                    'ui_save_png', 'ui_edit_in_paint', 'ui_menu_file', 'ui_about_credits23'):
            self.assertIn(s[key], value, key)

    def test_curve_hint_describes_early_completion_not_an_attachment(self):
        hint = self.strings['ui_drag_a_line_then_drag_twice_to_set']
        self.assertIn(self.strings['ui_finish_curve'], hint)
        self.assertIn('slutföra kurvan innan båda böjarna har ställts in.', hint)
        self.assertNotIn('fästa', hint)


if __name__ == '__main__':
    unittest.main()
