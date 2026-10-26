"""Five Afrikaans full-value regressions; semantics are documented separately."""
from copy import deepcopy
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues

KEYS = {
    'ui_the_encoder_did_not_finish',
    'ui_the_image_was_saved_but_android_could_not',
    'ui_higher_quality_usually_makes_a_larger_file_lossless',
    'language20_translation_note',
    'ui_d_d_px_d_pixels_2f_mp',
}
OLD = {
    'ui_the_encoder_did_not_finish': 'Die enkodeerder het nie voltooi nie.',
    'ui_the_image_was_saved_but_android_could_not': 'Die beeld is gestoor, maar Android kon deel nie oopmaak nie: %1$s',
    'ui_higher_quality_usually_makes_a_larger_file_lossless': 'Hoër kwaliteit lewer gewoonlik ’n groter lêer. Lossless behou elke kleurwaarde.',
    'language20_translation_note': 'Hierdie taalweergawe bevat al AN Paint se vertaalbare koppelvlakteks.',
    'ui_d_d_px_d_pixels_2f_mp': '%1$d × %2$d px · %3$,d piksels (%4$.2f MP)',
}


class AfrikaansPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture('afrikaans_priority_current_wording.json'), KEYS, {'default', 'af'})
        cls.xml = {tag: (catalogues.RES / path / 'strings.xml').read_text()
                   for tag, path in [('default', 'values'), ('af', 'values-b+af')]}
        cls.strings = {n.get('name'): ''.join(n.itertext())
                       for n in ET.fromstring(cls.xml['af']) if n.tag == 'string'}

    def test_complete_values_attributes_format_and_paragraphs(self):
        for key, values in self.data['values'].items():
            for tag, expected in values.items():
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, expected, self.data['constraints'][key])

    def test_missing_key_locale_constraint_and_empty_value_fail_closed(self):
        for key in KEYS:
            for mutation in ('key', 'locale', 'constraint', 'empty'):
                changed = deepcopy(self.data)
                if mutation == 'key': del changed['values'][key]
                elif mutation == 'locale': del changed['values'][key]['af']
                elif mutation == 'constraint': del changed['constraints'][key]
                else: changed['values'][key]['af'] = ''
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_wording_shape(changed, KEYS, {'default', 'af'})

    def test_old_values_and_structural_corruption_fail_closed(self):
        for key in KEYS:
            for mutation in ('old', 'missing', 'duplicate', 'truncated', 'markup', 'format-flag'):
                root = ET.fromstring(self.xml['af'])
                node = root.find(f"./string[@name='{key}']")
                if mutation == 'old': node.text = OLD[key]
                elif mutation == 'missing': root.remove(node)
                elif mutation == 'duplicate': root.append(deepcopy(node))
                elif mutation == 'truncated': node.text = node.text[:-1]
                elif mutation == 'markup': ET.SubElement(node, 'b').text, node.text = node.text, None
                else: node.set('formatted', 'false')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key,
                                   self.data['values'][key]['af'], self.data['constraints'][key])

    def test_encoder_failure_is_bound_to_failed_compression(self):
        classic = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        for filename in ('ImageExporter.kt', 'TextImageCodec.kt', 'IcoCodec.kt'):
            with self.subTest(filename=filename):
                source = (classic / filename).read_text()
                self.assertIn('compress(', source)
                self.assertIn('throw IOException(ui(R.string.ui_the_encoder_did_not_finish))', source)

    def test_live_lossless_checkbox_and_explanation_use_same_term(self):
        self.assertEqual('%1$s sonder verlies', self.strings['ui_lossless_format'])
        self.assertIn('Kompressie sonder verlies behou elke kleurwaarde.',
                      self.strings['ui_higher_quality_usually_makes_a_larger_file_lossless'])
        source = (catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/SaveOptionsDialog.kt').read_text()
        self.assertIn('losslessBox.text=ui(R.string.ui_lossless_format,format.label)', source)
        self.assertIn('R.string.ui_higher_quality_usually_makes_a_larger_file_lossless', source)

    def test_sharing_warning_preserves_saved_state_and_error_slot(self):
        value = self.strings['ui_the_image_was_saved_but_android_could_not']
        self.assertTrue(value.startswith('Die beeld is gestoor, maar Android kon nie '))
        self.assertTrue(value.endswith('deelopsies oopmaak nie: %1$s'))
        self.assertEqual({'%1$s': 1}, catalogues.placeholders(value))
        source = (catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt').read_text()
        body = source.split('private fun shareSavedImage(', 1)[1].split('private fun exportSourceTo(', 1)[0]
        self.assertIn('startActivity(Intent.createChooser(send,ui(R.string.ui_share_saved_image)))', body)
        self.assertIn('message(ui(R.string.ui_the_image_was_saved_but_android_could_not, error.message))', body)

    def test_current_catalogue_units_aliases_and_open_context_remain(self):
        self.assertEqual([], catalogues.validate_catalogue('af', require_complete=True))
        self.assertEqual('@string/ui_save', self.strings['ui_save_a5d0d9'])
        self.assertEqual('Stoor', self.strings['ui_save'])
        self.assertEqual(('Piksels', 'Persent'), (self.strings['ui_pixels'], self.strings['ui_percent']))
        self.assertEqual('Die konsep word gestoor. Probeer oor ’n oomblik weer.',
                         self.strings['ui_the_draft_is_saving_try_again_shortly'])
        self.assertEqual('Voorgrond %1$s, agtergrond %2$s. Kleurpalet %3$s.',
                         self.strings['ui_foreground_background_colour_palette'])
        self.assertEqual('Hoof', self.strings['ui_main23'])


if __name__ == '__main__':
    unittest.main()
