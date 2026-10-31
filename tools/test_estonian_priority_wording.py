"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

class EstonianPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml = {tag: (catalogues.RES / path / 'strings.xml').read_text() for tag, path in [('default', 'values'), ('et', 'values-b+et')]}
        cls.strings = {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(cls.xml['et']) if n.tag == 'string'}

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

    def test_save_alias_and_foreground_background_roles_stay_distinct(self):
        self.assertEqual('@string/ui_save', self.strings['ui_save_a5d0d9'])
        self.assertNotEqual(self.strings['ui_fg'], self.strings['ui_bg'])

if __name__ == '__main__': unittest.main()
