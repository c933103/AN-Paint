"""Bounded Indonesian full-value contracts; actual consumers have Robolectric tests."""
from copy import deepcopy
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues

KEYS = {'ui_the_encoder_did_not_finish', 'ui_pixels_6ec9c2'}

class IndonesianPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture('indonesian_priority_current_wording.json'), KEYS, {'default', 'id'})
        cls.xml = {tag: (catalogues.RES / path / 'strings.xml').read_text() for tag, path in [('default', 'values'), ('id', 'values-in')]}
        cls.strings = {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(cls.xml['id']) if n.tag == 'string'}

    def test_complete_values_attributes_and_syntax(self):
        for key, values in self.data['values'].items():
            for tag, expected in values.items():
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, expected, self.data['constraints'][key])

    def test_missing_keys_locales_and_constraints_fail_closed(self):
        for key in KEYS:
            for mutation in ('key', 'locale', 'constraint', 'empty'):
                changed = deepcopy(self.data)
                if mutation == 'key': del changed['values'][key]
                elif mutation == 'locale': del changed['values'][key]['id']
                elif mutation == 'constraint': del changed['constraints'][key]
                else: changed['values'][key]['id'] = ''
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_wording_shape(changed, KEYS, {'default', 'id'})

    def test_old_complete_values_and_structural_mutations_are_rejected(self):
        old = {'ui_the_encoder_did_not_finish': 'Enkoder tidak selesai.', 'ui_pixels_6ec9c2': 'Piksel'}
        for key in KEYS:
            for mutation in ('old', 'missing', 'duplicate', 'truncated', 'markup', 'format-flag'):
                root = ET.fromstring(self.xml['id']); node = root.find(f"./string[@name='{key}']")
                if mutation == 'old': node.text = old[key]
                elif mutation == 'missing': root.remove(node)
                elif mutation == 'duplicate': root.append(deepcopy(node))
                elif mutation == 'truncated': node.text = node.text[:-1]
                elif mutation == 'markup': ET.SubElement(node, 'b').text, node.text = node.text, None
                else: node.set('formatted', 'false')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, self.data['values'][key]['id'], self.data['constraints'][key])

    def test_encoder_failure_names_unfinished_operation(self):
        self.assertEqual('Enkoder tidak menyelesaikan pengodean.', self.strings['ui_the_encoder_did_not_finish'])
        classic = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        for filename in ('ImageExporter.kt', 'TextImageCodec.kt', 'IcoCodec.kt'):
            with self.subTest(filename=filename):
                text = (classic / filename).read_text()
                self.assertIn('compress(', text)
                self.assertIn('throw IOException(ui(R.string.ui_the_encoder_did_not_finish))', text)

    def test_pixel_units_compose_lowercase_and_standalone_label_stays_capitalized(self):
        self.assertEqual('Piksel', self.strings['ui_pixels'])
        self.assertEqual('piksel', self.strings['ui_pixels_6ec9c2'])
        for key, expected in [('ui_width_in', 'Lebar dalam piksel'), ('ui_height_in', 'Tinggi dalam piksel')]:
            self.assertEqual(expected, self.strings[key].replace('%1$s', self.strings['ui_pixels_6ec9c2']))

    def test_full_catalogue_and_reviewed_processing_wording_are_preserved(self):
        self.assertEqual([], catalogues.validate_catalogue('id', require_complete=True))
        self.assertEqual('Gambar yang telah diproses: %1$s / %2$s…', self.strings['ui_rendering_images'])
        self.assertEqual('@string/ui_save', self.strings['ui_save_a5d0d9'])
        self.assertEqual('Simpan', self.strings['ui_save'])
        self.assertEqual('Latar depan %1$s, latar belakang %2$s. Palet warna %3$s.', self.strings['ui_foreground_background_colour_palette'])
        self.assertEqual(('Depan', 'Latar'), (self.strings['ui_fg'], self.strings['ui_bg']))

if __name__ == '__main__': unittest.main()
