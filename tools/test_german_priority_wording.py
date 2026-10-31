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
        source = (ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt').read_text()
        self.assertIn('listOf(ui(R.string.ui_pixels), ui(R.string.ui_percent))', source)
        for key in ('ui_width_in', 'ui_height_in'):
            self.assertIn('ui(R.string.' + key + ', if (percent) ui(R.string.ui_percent_fd8671) '
                          'else ui(R.string.ui_pixels_6ec9c2))', source)

    def test_foreground_background_abbreviations_remain_distinct_two_character_labels(self):
        self.assertEqual(('VG', 'HG'), (self.values['ui_fg'], self.values['ui_bg']))
        self.assertEqual([2, 2], [len(self.values[key]) for key in ('ui_fg', 'ui_bg')])

    def test_safety_and_accessibility_clauses_are_retained_in_full(self):
        clauses = {
            'formats22_animation_unknown': [
                'AN Paint öffnet nur ein Standbild und erhält keine Animation.',
            ],
            'ui_d_d_pixels_2f_mp_exceeds_the_current': [
                'AN Paint hält das vollständige Bild im Speicher und reserviert Platz für Transformationen und Auswahlen.',
                'Der verfügbare Speicher bestimmt dieses Limit.',
                'Der Vorgang wurde gestoppt, bevor die übergroße Bitmap angelegt wurde.',
                'Es wurde keine automatische Größenänderung vorgenommen.',
            ],
            'ui_no_resize_fits_decoder_memory': [
                'Brechen Sie ab und verwenden Sie ein kleineres Quellbild.',
            ],
            'ui_recovery_copy_exported_extract_canvas_png_from_the': [
                'canvas.png', 'ZIP-Datei', 'öffnen Sie dieses Bild über Datei > Bild laden',
                'Die ZIP-Datei enthält auch Entwurfseinstellungen und eine eventuell schwebende Auswahl.',
            ],
            'ui_share_explanation34': [
                'Das bisherige Speicherziel bleibt unverändert.',
            ],
            'ui_drawing_canvas_pinch_and_move_two_fingers_to': [
                'zwei Finger auseinander oder zusammen',
                'Im Navigationsmodus können Sie die Ansicht auch mit einem Finger verschieben.',
            ],
        }
        for key, required in clauses.items():
            for clause in required:
                with self.subTest(key=key, clause=clause):
                    self.assertIn(clause, self.values[key])

if __name__ == '__main__':
    unittest.main()
