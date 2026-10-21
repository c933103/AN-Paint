"""Complete Latvian wording contracts; real composition is exercised by Robolectric."""
from copy import deepcopy
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues

KEYS = {'ui_expand_tool_category', 'formats22_animation_message', 'ui_width_in', 'ui_height_in', 'ui_pixels_6ec9c2', 'ui_percent_fd8671', 'ui_d_d_px_d_pixels_2f_mp', 'ui_colour_palette_tap_for_foreground_hold_for_background', 'ui_colour_tap_foreground_hold_background', 'language20_translation_note', 'ui_collapse_tool_category'}
OLD = {'formats22_animation_message': 'Šis %1$s satur %2$s kadrus. AN Paint rediģē nekustīgus attēlus un nesaglabā animāciju.', 'language20_translation_note': 'Šajā valodas versijā ir viss AN Paint tulkojamais saskarnes teksts.', 'ui_d_d_px_d_pixels_2f_mp': '%1$d × %2$d px · %3$,d pikseļi (%4$.2f MP)', 'ui_width_in': 'Platums %1$s vienībās', 'ui_height_in': 'Augstums %1$s vienībās', 'ui_pixels_6ec9c2': 'pikseļi', 'ui_percent_fd8671': 'procenti', 'ui_collapse_tool_category': '%1$s: atlasīts %2$s. Sakļaut rīkus un opcijas', 'ui_expand_tool_category': '%1$s: atlasīts %2$s. Izvērst rīkus un opcijas', 'ui_colour_palette_tap_for_foreground_hold_for_background': 'Krāsu palete. Pieskarieties priekšplānam; turiet nospiestu fonam. Ritiniet, lai skatītu vairāk krāsu.', 'ui_colour_tap_foreground_hold_background': 'Krāsa #%1$s. Pieskarieties priekšplānam, turiet nospiestu fonam.'}

class LatvianPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture('latvian_priority_current_wording.json'), KEYS, {'default', 'lv'})
        cls.xml = {tag: (catalogues.RES / path / 'strings.xml').read_text() for tag, path in [('default', 'values'), ('lv', 'values-b+lv')]}
        cls.strings = {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(cls.xml['lv']) if n.tag == 'string'}

    def test_complete_values_attributes_placeholders_and_newlines(self):
        for key, values in self.data['values'].items():
            for tag, expected in values.items():
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, expected, self.data['constraints'][key])

    def test_missing_keys_locales_and_constraints_fail_closed(self):
        for key in KEYS:
            for mutation in ('key', 'locale', 'constraint', 'empty'):
                changed = deepcopy(self.data)
                if mutation == 'key': del changed['values'][key]
                elif mutation == 'locale': del changed['values'][key]['lv']
                elif mutation == 'constraint': del changed['constraints'][key]
                else: changed['values'][key]['lv'] = ''
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_wording_shape(changed, KEYS, {'default', 'lv'})

    def test_old_full_values_and_structural_mutations_are_rejected(self):
        for key in KEYS:
            for mutation in ('old', 'missing', 'duplicate', 'truncated', 'markup', 'format-flag'):
                root = ET.fromstring(self.xml['lv']); node = root.find(f"./string[@name='{key}']")
                if mutation == 'old': node.text = OLD[key]
                elif mutation == 'missing': root.remove(node)
                elif mutation == 'duplicate': root.append(deepcopy(node))
                elif mutation == 'truncated': node.text = node.text[:-1]
                elif mutation == 'markup': ET.SubElement(node, 'b').text, node.text = node.text, None
                else: node.set('formatted', 'false')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, self.data['values'][key]['lv'], self.data['constraints'][key])

    def test_all_four_accessible_compositions_and_standalone_labels(self):
        self.assertEqual(('Pikseļi', 'Procenti'), (self.strings['ui_pixels'], self.strings['ui_percent']))
        for dimension, unit, expected in [
                ('ui_width_in', 'ui_pixels_6ec9c2', 'Platums pikseļos'),
                ('ui_height_in', 'ui_pixels_6ec9c2', 'Augstums pikseļos'),
                ('ui_width_in', 'ui_percent_fd8671', 'Platums procentos'),
                ('ui_height_in', 'ui_percent_fd8671', 'Augstums procentos')]:
            self.assertEqual(expected, self.strings[dimension].replace('%1$s', self.strings[unit]))
        self.assertEqual(('Platums (%1$s)', 'Augstums (%1$s)'), (self.strings['ui_width'], self.strings['ui_height']))

    def test_consumer_shapes_keep_selected_names_and_argument_contracts(self):
        classic = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        self.assertIn('text = ui(R.string.language20_translation_note)', (classic / 'AppLanguage.kt').read_text())
        self.assertIn('ui(R.string.ui_d_d_px_d_pixels_2f_mp, width, height, pixels, pixels / 1_000_000.0)', (classic / 'ImageImport.kt').read_text())
        dimensions = (classic / 'DimensionControls.kt').read_text()
        for dimension in ('width', 'height'):
            self.assertIn(f'{dimension}Input.contentDescription = ui(R.string.ui_{dimension}_in, if (percent) ui(R.string.ui_percent_fd8671) else ui(R.string.ui_pixels_6ec9c2))', dimensions)
        self.assertIn('ui(category.labelId),selectedTool.label)', (classic / 'ToolCategoryButton.kt').read_text())
        self.assertIn('ui(R.string.formats22_animation_message,info.format,frames)', (classic / 'ImportSelection.kt').read_text())

    def test_complete_category_sentences_support_both_tool_genders(self):
        for category, tool, expected_prefix in [('Zīmēšana', 'Zīmulis', 'Zīmēšana. Atlasītais rīks: Zīmulis.'), ('Zīmēšana', 'Ota', 'Zīmēšana. Atlasītais rīks: Ota.'), ('Atlase', 'Brīvformas atlase', 'Atlase. Atlasītais rīks: Brīvformas atlase.')]:
            for key, action in [('ui_expand_tool_category', 'Izvērst'), ('ui_collapse_tool_category', 'Sakļaut')]:
                self.assertEqual(expected_prefix + f' {action} rīkus un opcijas', self.strings[key].replace('%1$s',category).replace('%2$s',tool))

    def test_complete_catalogue_and_unmodified_terminology_holds(self):
        self.assertEqual([], catalogues.validate_catalogue('lv', require_complete=True))
        self.assertEqual('@string/ui_save', self.strings['ui_save_a5d0d9'])
        self.assertEqual(('PR', 'F'), (self.strings['ui_fg'], self.strings['ui_bg']))
        self.assertEqual('Kodētājs nepabeidza darbu.', self.strings['ui_the_encoder_did_not_finish'])
        self.assertIn('Diterēšana', self.strings['save20_gif_description'])
        self.assertIn('paraugu dekodēšanu', self.strings['ui_sampled_resize_memory_explanation'])
        self.assertIn('avota flīzes', self.strings['ui_codec_resize_memory_floor'])

if __name__ == '__main__': unittest.main()
