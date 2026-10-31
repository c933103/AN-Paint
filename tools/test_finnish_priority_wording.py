"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

class FinnishPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml = {tag: (catalogues.RES / path / 'strings.xml').read_text() for tag, path in [('default', 'values'), ('fi', 'values-fi')]}
        cls.strings = {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(cls.xml['fi']) if n.tag == 'string'}

    def test_encoder_failure_names_unfinished_operation(self):
        self.assertEqual('Kooderi ei suorittanut koodausta loppuun.', self.strings['ui_the_encoder_did_not_finish'])
        classic = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        for filename in ('ImageExporter.kt', 'TextImageCodec.kt', 'IcoCodec.kt'):
            with self.subTest(filename=filename):
                text = (classic / filename).read_text()
                self.assertIn('compress(', text)
                self.assertIn('throw IOException(ui(R.string.ui_the_encoder_did_not_finish))', text)

    def test_unit_compositions_and_standalone_labels(self):
        self.assertEqual(('Pikselit', 'Prosentti'), (self.strings['ui_pixels'], self.strings['ui_percent']))
        for key, noun in [('ui_width_in', 'Leveys'), ('ui_height_in', 'Korkeus')]:
            for unit, expected in [('ui_pixels_6ec9c2', 'pikseleinä'), ('ui_percent_fd8671', 'prosentteina')]:
                self.assertEqual(noun + ' ' + expected, self.strings[key].replace('%1$s', self.strings[unit]))
        self.assertEqual(('Leveys (%1$s)', 'Korkeus (%1$s)'), (self.strings['ui_width'], self.strings['ui_height']))

    def test_count_neutral_summary_and_truthful_fallback_note(self):
        self.assertEqual('%1$d × %2$d px · Pikselimäärä: %3$,d (%4$.2f MP)', self.strings['ui_d_d_px_d_pixels_2f_mp'])
        self.assertNotIn('sisältää kaikki', self.strings['language20_translation_note'])

    def test_save_alias_and_foreground_background_roles_stay_distinct(self):
        self.assertEqual('@string/ui_save', self.strings['ui_save_a5d0d9'])
        self.assertNotEqual(self.strings['ui_fg'], self.strings['ui_bg'])

if __name__ == '__main__': unittest.main()
