"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

class IndonesianPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml = {tag: (catalogues.RES / path / 'strings.xml').read_text() for tag, path in [('default', 'values'), ('id', 'values-in')]}
        cls.strings = {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(cls.xml['id']) if n.tag == 'string'}

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

    def test_save_alias_and_foreground_background_roles_stay_distinct(self):
        self.assertEqual('@string/ui_save', self.strings['ui_save_a5d0d9'])
        self.assertNotEqual(self.strings['ui_fg'], self.strings['ui_bg'])

if __name__ == '__main__': unittest.main()
