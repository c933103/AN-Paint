"""Current locale semantics; historical approval snapshots live in immutable source history."""
from pathlib import Path
import unittest
import translation_catalogues as catalogues

ROOT = Path(__file__).resolve().parents[1]

class GermanPriorityWording(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = catalogues.catalogue_paths()['de']
        cls.values = catalogues.read_strings(cls.path)

    def test_pixel_unit_is_declined_only_in_width_and_height_descriptions(self):
        self.assertEqual('Pixel', self.values['ui_pixels'])
        self.assertEqual('Pixeln', self.values['ui_pixels_6ec9c2'])
        for key, label in (('ui_width_in', 'Breite'), ('ui_height_in', 'Höhe')):
            template = self.values[key]
            self.assertEqual(label + ' in %1$s', template)
            self.assertEqual(label + ' in Pixeln', template.replace('%1$s', self.values['ui_pixels_6ec9c2']))
            self.assertEqual(label + ' in Prozent', template.replace('%1$s', self.values['ui_percent_fd8671']))
        # Static consumer binding, not an assertion of Android runtime behavior.

    def test_foreground_background_abbreviations_remain_distinct_two_character_labels(self):
        self.assertEqual(('VG', 'HG'), (self.values['ui_fg'], self.values['ui_bg']))
        self.assertEqual([2, 2], [len(self.values[key]) for key in ('ui_fg', 'ui_bg')])

    def test_warning_modalities_and_recovery_ownership_remain_explicit(self):
        s = self.values
        self.assertIn('keine automatische Größenänderung', s['ui_d_d_pixels_2f_mp_exceeds_the_current'])
        self.assertIn('kleineres Quellbild', s['ui_no_resize_fits_decoder_memory'])
        self.assertIn('keine Animation', s['formats22_animation_unknown'])
        recovery = s['ui_recovery_copy_exported_extract_canvas_png_from_the']
        for boundary in ('canvas.png', 'ZIP', 'Entwurfseinstellungen', 'eventuell schwebende Auswahl'):
            self.assertIn(boundary, recovery)
        self.assertIn('Speicherziel bleibt unverändert', s['ui_share_explanation34'])

if __name__ == '__main__':
    unittest.main()
