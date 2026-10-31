"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

class LatvianPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml = {tag: (catalogues.RES / path / 'strings.xml').read_text() for tag, path in [('default', 'values'), ('lv', 'values-b+lv')]}
        cls.strings = {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(cls.xml['lv']) if n.tag == 'string'}

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

    def test_save_alias_and_foreground_background_roles_stay_distinct(self):
        self.assertEqual('@string/ui_save', self.strings['ui_save_a5d0d9'])
        self.assertNotEqual(self.strings['ui_fg'], self.strings['ui_bg'])

    def test_all_four_accessible_compositions_and_standalone_labels(self):
        self.assertEqual(('Pikseļi', 'Procenti'), (self.strings['ui_pixels'], self.strings['ui_percent']))
        for dimension, unit, expected in [
                ('ui_width_in', 'ui_pixels_6ec9c2', 'Platums pikseļos'),
                ('ui_height_in', 'ui_pixels_6ec9c2', 'Augstums pikseļos'),
                ('ui_width_in', 'ui_percent_fd8671', 'Platums procentos'),
                ('ui_height_in', 'ui_percent_fd8671', 'Augstums procentos')]:
            self.assertEqual(expected, self.strings[dimension].replace('%1$s', self.strings[unit]))
        self.assertEqual(('Platums (%1$s)', 'Augstums (%1$s)'), (self.strings['ui_width'], self.strings['ui_height']))

if __name__ == '__main__': unittest.main()
