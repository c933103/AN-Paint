"""Current locale semantics; historical approval snapshots live in immutable source history."""
import json
import re
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
        self.assertEqual(
            'Pikselleri sol üst köşeye hizalı olarak korur. '
            'Daha küçük tuval boyutları sağ/alt kenarın dışındaki pikselleri atar; Geri Al bunları geri getirir.',
            self.strings['tr'][CANVAS])
        self.assertRegex(self.activity, r'if \(!fresh\).*if \(stretch\).*else ui\(R\.string\.' + CANVAS)
        document = (CLASSIC / 'PaintDocument.kt').read_text(encoding='utf-8')
        resize = re.search(r'fun resize\(w: Int, h: Int, stretch: Boolean\) \{(.*?)\n    \}', document, re.S)
        self.assertIsNotNone(resize)
        self.assertRegex(resize.group(1), r'else canvas\.drawBitmap\(bitmap, 0f, 0f, copyPaint\)\s*replace\(next, true\)')

    def test_recovery_names_actual_file_menu_command_and_keeps_archive_contents(self):
        strings = self.strings['tr']
        command = strings['ui_load_image'].rstrip('…')
        self.assertEqual('Görüntü aç', command)
        self.assertEqual('Dosya', strings['ui_menu_file'])
        self.assertEqual(
            r"Kurtarma kopyası dışa aktarıldı. ZIP\'ten canvas.png dosyasını çıkarın ve "
            + strings['ui_menu_file'] + ' > ' + command +
            ' ile açın. ZIP ayrıca taslak ayarlarını ve varsa yüzen seçimi içerir.', strings[RECOVERY])
        self.assertRegex(self.activity, r'"File"->\(listOf[\s\S]*?ui\(R\.string\.ui_load_image\) to \{confirmReplacement \{launchOpen\(false\)\}\}')
        self.assertIn('message(ui(R.string.' + RECOVERY + '))', self.activity)

    def test_language_note_keeps_both_fallback_cases_and_two_newlines(self):
        self.assertEqual(
            r"Uygulama dili\n\nÇeviriler AN Paint\'in dil kaynaklarında tutulur. "
            'Yeni veya çevrilmemiş metinler İngilizce olarak gösterilir.', self.strings['tr'][NOTE])
        self.assertEqual(2, self.strings['tr'][NOTE].count('\\n'))
        picker = (CLASSIC / 'AppLanguage.kt').read_text(encoding='utf-8')
        self.assertIn('text = ui(R.string.' + NOTE + ')', picker)

    def test_zoom_direction_and_two_finger_pan_match_source_span_and_focus_changes(self):
        self.assertEqual(
            'Çizim tuvali. Yakınlaştırmak için iki parmağınızı birbirinden uzaklaştırın, '
            'uzaklaştırmak için birbirine yaklaştırın. Kaydırmak için iki parmağınızı birlikte sürükleyin. '
            'Gezinme modunda tek parmakla da kaydırabilirsiniz.', self.strings['tr'][GESTURE])
        self.assertIn('contentDescription=ui(R.string.' + GESTURE + ')', re.sub(r'\s+', '', self.canvas))
        self.assertIn('R.string.' + GESTURE, self.activity)
        self.assertIn('if (event.pointerCount > 1)', self.canvas)
        self.assertIn('zoomAt(zoom*span/pinchSpan,pinchFocus.x,pinchFocus.y)', self.canvas)
        self.assertIn('panX+=focus.x-pinchFocus.x;panY+=focus.y-pinchFocus.y', self.canvas)

    def test_p3_navigate_companion_retains_zoom_out_and_one_finger_pan(self):
        self.assertEqual(
            'Yakınlaştırmak için iki parmağınızı birbirinden uzaklaştırın; '
            'uzaklaştırmak için birbirine yaklaştırın. Kaydırmak için sürükleyin.',
            self.strings['tr'][NAVIGATE])
        self.assertRegex(self.activity, r'PaintTool\.ZOOM -> \{\s*options\.addView\(label\(ui\(R\.string\.' + NAVIGATE)
        self.assertIn('panning = tool == PaintTool.ZOOM', self.canvas)
        self.assertRegex(self.canvas, r'if \(panning\) \{\s*fitMode=false;panX \+= event.x - screenPrevious.x; panY \+= event.y - screenPrevious.y')
        priorities = json.loads((catalogues.ROOT / 'translations/string-importance.json').read_text())
        tier = {key: group['id'] for group in priorities['tiers'] for key in group['keys']}
        self.assertEqual('P3', tier['string/' + NAVIGATE])
        for key in PRIORITY_KEYS:
            self.assertIn(tier['string/' + key], {'P0', 'P1'}, key)

    def test_invalid_selection_uses_contour_terminology_for_serialized_paths(self):
        self.assertEqual('Kontur', self.strings['tr']['ui_outline'])
        self.assertEqual('Geçersiz seçim konturu.', self.strings['tr'][OUTLINE])
        source = (CLASSIC / 'SelectionOutline.kt').read_text(encoding='utf-8')
        self.assertRegex(source, r'fun read\(contours: JSONArray\?\): Path\?')
        self.assertIn('require(contours.length()<=128) { ui(R.string.' + OUTLINE + ') }', source)

    def test_memory_warning_keeps_both_causes_copy_target_and_original(self):
        self.assertEqual(
            'Tam görüntü ve çalışma arabellekleri geçerli güvenli sınırı aşıyor veya Android bunlar için bellek ayıramadı. '
            'Düzenlemek için bir kopyayı yeniden boyutlandırın. Özgün dosyanız değişmeden kalır.',
            self.strings['tr'][MEMORY])
        dialog = (CLASSIC / 'ImageResizeDialog.kt').read_text(encoding='utf-8')
        self.assertIn('label(ui(R.string.' + MEMORY + '), "resize_reason")', dialog)
        for cause in ('ImageSizeException', 'OutOfMemoryError'):
            self.assertRegex(self.activity, r'catch \(_: ' + cause + r'\) \{[^}]*askToResize\(source,import,target,asEdit,credits,whiteBacking\)')

    def test_swap_explicitly_exchanges_colours_and_preserves_legacy_context_limit(self):
        self.assertEqual('Renklerin yerini değiştir', self.strings['tr'][SWAP])
        self.assertEqual('Ön plan ile arka plan renklerinin yerini değiştir', self.strings['tr'][LEGACY_SWAP])
        self.assertRegex(self.activity, r'ui\(R\.string\.' + SWAP + r'\).*val old=document\.foreground;document\.foreground=document\.background;document\.background=old')

if __name__ == '__main__':
    unittest.main()
