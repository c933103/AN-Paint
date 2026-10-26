"""Bounded Turkish text/source contracts, not Android layout or fluency certification."""
from collections import Counter
from copy import deepcopy
import json
import re
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues

FIXTURE = 'turkish_priority_current_wording.json'
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
KEYS = PRIORITY_KEYS | {NAVIGATE}
TAGS = {'default', 'tr'}
CLASSIC = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'


class TurkishPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture(FIXTURE), KEYS, TAGS)
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

    def test_complete_bilingual_wording_attributes_and_typed_arguments(self):
        for key, values in self.data['values'].items():
            self.assertEqual(TAGS, set(self.data['constraints'][key]))
            self.assertEqual(Counter(), catalogues.placeholders(values['default']))
            for tag, expected in values.items():
                constraints = self.data['constraints'][key][tag]
                self.assertEqual({'attributes', 'placeholders', 'formatted'}, set(constraints))
                attributes = {'name': key}
                formatted = not (tag == 'tr' and key == SWAP)
                if not formatted:
                    attributes['formatted'] = 'false'
                self.assertEqual(attributes, constraints['attributes'])
                self.assertIs(formatted, constraints['formatted'])
                self.assertEqual({}, constraints['placeholders'])
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, expected, constraints)

    def test_fixture_requires_all_nine_keys_both_locales_and_constraints(self):
        for key in KEYS:
            for mutation in ('missing-key', 'missing-locale', 'empty-text', 'missing-constraint'):
                changed = deepcopy(self.data)
                if mutation == 'missing-key':
                    del changed['values'][key]
                elif mutation == 'missing-locale':
                    del changed['values'][key]['tr']
                elif mutation == 'empty-text':
                    changed['values'][key]['tr'] = ''
                else:
                    del changed['constraints'][key]
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_wording_shape(changed, KEYS, TAGS)

    def test_truncation_duplicates_missing_entries_attributes_and_markup_fail_closed(self):
        for key in KEYS:
            expected = self.data['values'][key]['tr']
            constraints = self.data['constraints'][key]['tr']
            for mutation in ('truncate', 'duplicate', 'missing', 'format-flag', 'markup'):
                root = ET.fromstring(self.xml['tr'])
                node = root.find(f"./string[@name='{key}']")
                if mutation == 'truncate':
                    node.text = node.text[:-1]
                elif mutation == 'duplicate':
                    root.append(deepcopy(node))
                elif mutation == 'missing':
                    root.remove(node)
                elif mutation == 'format-flag':
                    node.set('formatted', 'true' if node.get('formatted') == 'false' else 'false')
                else:
                    ET.SubElement(node, 'b').text, node.text = node.text, None
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, expected, constraints)

    def test_introduced_arguments_and_unescaped_apostrophes_are_rejected(self):
        for key in KEYS:
            value = self.data['values'][key]['tr']
            for changed in (value + ' %1$s', value + " '"):
                root = ET.fromstring(self.xml['tr'])
                root.find(f"./string[@name='{key}']").text = changed
                # Matching changed text cannot bypass Android syntax/argument checks.
                with self.subTest(key=key, changed=changed), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, changed,
                                   self.data['constraints'][key]['tr'])

    def test_complete_turkish_catalogue_and_android_syntax(self):
        self.assertEqual([], catalogues.validate_catalogue('tr', require_complete=True))
        for tag, xml in self.xml.items():
            root = ET.fromstring(xml)
            identities = [(n.tag, n.get('name')) for n in root]
            self.assertEqual(len(identities), len(set(identities)))
            for node in root.findall('string'):
                value = ''.join(node.itertext())
                with self.subTest(locale=tag, key=node.get('name')):
                    self.assertEqual([], catalogues.android_string_errors(value))
                    self.assertEqual([], catalogues.format_string_errors(value, node.get('formatted') != 'false'))

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
        # The legacy resource is a lexical correction only; this test claims no live consumer or width fit.

    def test_four_unresolved_values_and_previous_sampled_memory_credit_are_preserved(self):
        strings = self.strings['tr']
        self.assertEqual(('FG', 'BG', 'Ana'), tuple(strings[k] for k in ('ui_fg', 'ui_bg', 'ui_main23')))
        self.assertEqual('Ön plan %1$s, arka plan %2$s. %3$s renk paleti.',
                         strings['ui_foreground_background_colour_palette'])
        self.assertEqual(
            'Tahminler geçerli tuvali ve panoyu, örneklenmiş kod çözmeyi ve düzenleme arabelleklerini içerir. '
            'Gerçek bellek kullanımı değişebilir. Daha küçük bir kopya ayrıntı kaybeder. Özgün dosya değişmeden kalır.',
            strings['ui_sampled_resize_memory_explanation'])


if __name__ == '__main__':
    unittest.main()
