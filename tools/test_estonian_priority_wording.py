"""Complete Estonian wording contracts; real composition is exercised by Robolectric."""
from copy import deepcopy
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues

KEYS = {'language20_translation_note', 'ui_export_did_not_save23', 'ui_d_d_px_d_pixels_2f_mp',
        'ui_width_in', 'ui_height_in', 'ui_pixels_6ec9c2', 'ui_percent_fd8671'}
OLD = {'language20_translation_note': 'See keeleversioon sisaldab kogu AN Painti tõlgitavat kasutajaliidese teksti.',
       'ui_export_did_not_save23': 'Eksport loodi. Enne jätkamist salvesta praegune pilt käsuga Salvesta või Salvesta kui.',
       'ui_d_d_px_d_pixels_2f_mp': '%1$d × %2$d px · %3$,d pikslit (%4$.2f MP)',
       'ui_width_in': 'Laius ühikus %1$s', 'ui_height_in': 'Kõrgus ühikus %1$s',
       'ui_pixels_6ec9c2': 'pikslit', 'ui_percent_fd8671': 'protsent'}

class EstonianPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture('estonian_priority_current_wording.json'), KEYS, {'default', 'et'})
        cls.xml = {tag: (catalogues.RES / path / 'strings.xml').read_text() for tag, path in [('default', 'values'), ('et', 'values-b+et')]}
        cls.strings = {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(cls.xml['et']) if n.tag == 'string'}

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
                elif mutation == 'locale': del changed['values'][key]['et']
                elif mutation == 'constraint': del changed['constraints'][key]
                else: changed['values'][key]['et'] = ''
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_wording_shape(changed, KEYS, {'default', 'et'})

    def test_old_full_values_and_structural_mutations_are_rejected(self):
        for key in KEYS:
            for mutation in ('old', 'missing', 'duplicate', 'truncated', 'markup', 'format-flag'):
                root = ET.fromstring(self.xml['et']); node = root.find(f"./string[@name='{key}']")
                if mutation == 'old': node.text = OLD[key]
                elif mutation == 'missing': root.remove(node)
                elif mutation == 'duplicate': root.append(deepcopy(node))
                elif mutation == 'truncated': node.text = node.text[:-1]
                elif mutation == 'markup': ET.SubElement(node, 'b').text, node.text = node.text, None
                else: node.set('formatted', 'false')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, self.data['values'][key]['et'], self.data['constraints'][key])

    def test_all_four_accessible_compositions_and_standalone_labels(self):
        self.assertEqual(('Pikslid', 'Protsent'), (self.strings['ui_pixels'], self.strings['ui_percent']))
        for dimension, unit, expected in [
                ('ui_width_in', 'ui_pixels_6ec9c2', 'Laius pikslites'),
                ('ui_height_in', 'ui_pixels_6ec9c2', 'Kõrgus pikslites'),
                ('ui_width_in', 'ui_percent_fd8671', 'Laius protsentides'),
                ('ui_height_in', 'ui_percent_fd8671', 'Kõrgus protsentides')]:
            self.assertEqual(expected, self.strings[dimension].replace('%1$s', self.strings[unit]))
        self.assertEqual(('Laius (%1$s)', 'Kõrgus (%1$s)'), (self.strings['ui_width'], self.strings['ui_height']))

    def test_export_guidance_uses_actual_save_commands_and_preserves_consumers(self):
        self.assertEqual(('Salvesta', 'Salvesta nimega…'), (self.strings['ui_save'], self.strings['save20_title']))
        self.assertIn('Salvesta või Salvesta nimega.', self.strings['ui_export_did_not_save23'])
        classic = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        activity = (classic / 'ClassicPaintActivity.kt').read_text()
        self.assertIn('ui(R.string.ui_export_did_not_save23)', activity)
        self.assertIn('text = ui(R.string.language20_translation_note)', (classic / 'AppLanguage.kt').read_text())
        self.assertIn('ui(R.string.ui_d_d_px_d_pixels_2f_mp, width, height, pixels, pixels / 1_000_000.0)', (classic / 'ImageImport.kt').read_text())
        dimensions = (classic / 'DimensionControls.kt').read_text()
        for dimension in ('width', 'height'):
            self.assertIn(f'{dimension}Input.contentDescription = ui(R.string.ui_{dimension}_in, if (percent) ui(R.string.ui_percent_fd8671) else ui(R.string.ui_pixels_6ec9c2))', dimensions)

    def test_complete_catalogue_and_explicit_holds_remain_unchanged(self):
        self.assertEqual([], catalogues.validate_catalogue('et', require_complete=True))
        self.assertEqual('@string/ui_save', self.strings['ui_save_a5d0d9'])
        self.assertEqual(('ES', 'TA'), (self.strings['ui_fg'], self.strings['ui_bg']))
        self.assertEqual('Mustandit salvestatakse. Proovi varsti uuesti.', self.strings['ui_the_draft_is_saving_try_again_shortly'])
        self.assertEqual('Kuueteistkümnend #RRGGBB', self.strings['ui_hex_rrggbb'])
        self.assertIn('Rasterdamine', self.strings['save20_gif_description'])
        self.assertIn('näidispõhist', self.strings['ui_sampled_resize_memory_explanation'])

if __name__ == '__main__': unittest.main()
