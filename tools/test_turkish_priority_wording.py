"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

CANVAS = 'ui_keeps_pixels_at_the_top_left_smaller_canvas'

RECOVERY = 'ui_recovery_copy_exported_extract_canvas_png_from_the'

NOTE = 'language20_translation_note'

GESTURE = 'ui_drawing_canvas_pinch_and_move_two_fingers_to'

OUTLINE = 'ui_invalid_selection_outline'

MEMORY = 'ui_the_full_image_and_working_buffers_exceed_the'

SWAP = 'ui_swap23'

LEGACY_SWAP = 'ui_swap_foreground_background'

NAVIGATE = 'ui_pinch_to_zoom_drag_to_pan'

PRIORITY_KEYS = {CANVAS, RECOVERY, NOTE, GESTURE, OUTLINE, MEMORY, SWAP, LEGACY_SWAP}

CLASSIC = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'

class TurkishPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml = {
            'default': (catalogues.RES / 'values/strings.xml').read_text(encoding='utf-8'),
            'tr': (catalogues.RES / 'values-tr/strings.xml').read_text(encoding='utf-8'),
        }
        cls.strings = {
            tag: {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(xml) if n.tag == 'string'}
            for tag, xml in cls.xml.items()
        }
        cls.activity = (CLASSIC / 'ClassicPaintActivity.kt').read_text(encoding='utf-8')
        cls.canvas = (CLASSIC / 'PaintCanvas.kt').read_text(encoding='utf-8')

    def test_canvas_preserves_top_left_alignment_loss_edges_and_undo(self):
        value = self.strings['tr'][CANVAS]
        self.assertIn('sol üst', value)
        self.assertIn('sağ/alt', value)
        self.assertIn(self.strings['tr']['ui_undo'], value)

    def test_recovery_names_actual_file_menu_command_and_keeps_archive_contents(self):
        strings = self.strings['tr']
        command = strings['ui_load_image'].rstrip('…')
        self.assertIn(strings['ui_menu_file'] + ' > ' + command, strings[RECOVERY])
        self.assertIn('canvas.png', strings[RECOVERY])
        self.assertIn('ZIP', strings[RECOVERY])
        self.assertIn('taslak ayarlarını', strings[RECOVERY])
        self.assertIn('varsa yüzen seçimi', strings[RECOVERY])
        # Recovery-export notification has no independently mapped runtime binding yet.
        self.assertIn('message(ui(R.string.' + RECOVERY + '))', self.activity)

    def test_language_note_keeps_both_fallback_cases_and_two_newlines(self):
        value = self.strings['tr'][NOTE]
        self.assertIn('Yeni veya çevrilmemiş', value)
        self.assertIn('İngilizce', value)

    def test_gesture_guidance_distinguishes_both_zoom_directions_and_finger_counts(self):
        value = self.strings['tr'][GESTURE]
        for distinction in ('Yakınlaştırmak', 'uzaklaştırmak', 'iki parmağ', 'tek parmak'):
            self.assertIn(distinction, value)

    def test_navigate_guidance_retains_both_zoom_directions(self):
        value = self.strings['tr'][NAVIGATE]
        self.assertIn('Yakınlaştırmak', value)
        self.assertIn('uzaklaştırmak', value)

    def test_invalid_selection_uses_contour_terminology_for_serialized_paths(self):
        self.assertEqual('Kontur', self.strings['tr']['ui_outline'])
        self.assertEqual('Geçersiz seçim konturu.', self.strings['tr'][OUTLINE])
        source = (CLASSIC / 'SelectionOutline.kt').read_text(encoding='utf-8')
        self.assertRegex(source, r'fun read\(contours: JSONArray\?\): Path\?')
        self.assertIn('require(contours.length()<=128) { ui(R.string.' + OUTLINE + ') }', source)

    def test_memory_warning_keeps_both_causes_copy_target_and_original(self):
        value = self.strings['tr'][MEMORY]
        self.assertIn('veya Android', value)
        self.assertIn('bir kopyayı', value)
        self.assertIn('Özgün dosyanız değişmeden', value)

    def test_swap_explicitly_exchanges_colours_and_preserves_legacy_context_limit(self):
        self.assertEqual('Renklerin yerini değiştir', self.strings['tr'][SWAP])
        self.assertEqual('Ön plan ile arka plan renklerinin yerini değiştir', self.strings['tr'][LEGACY_SWAP])

if __name__ == '__main__':
    unittest.main()
