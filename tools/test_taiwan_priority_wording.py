"""Bounded Taiwan wording and source-consumer contracts, not installed UI evidence."""
from copy import deepcopy
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues
# The two memory translations remain pending review against the corrected source.
from memory_warning_source_review import current_source_expectation
from test_assembly_help_pr8 import code_locations, kotlin_block

KEYS = {
    'formats22_ascii_description', 'save20_gif_description',
    'ui_a_separate_recovery_copy_has_been_kept_use', 'ui_discard',
    'ui_recovery_copy_exported_extract_canvas_png_from_the', 'ui_save_a5d0d9',
    'ui_save_your_changes', 'language20_translation_note', 'ui_bg',
    'ui_choose_a_smaller_size', 'ui_crop_preview_drag_an_edge_or_corner_drag',
    'ui_draw_again', 'ui_drawing_canvas_pinch_and_move_two_fingers_to',
    'ui_enter_all_four_trim_amounts', 'ui_fg', 'ui_hex_rrggbb',
    'ui_no_resize_fits_decoder_memory', 'ui_not_enough_memory_to_finish_opening_this_image',
}
TAGS = {'default', 'zh-TW'}
CLASSIC = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
RECOVERY = 'ui_a_separate_recovery_copy_has_been_kept_use'
EXPORTED = 'ui_recovery_copy_exported_extract_canvas_png_from_the'
NOTE = 'language20_translation_note'


class TaiwanPriorityWordingTests(unittest.TestCase):
    def test_gif_dithering_description_names_the_actual_checkbox(self):
        self.assertEqual('遞色', self.strings['save20_dither'])
        self.assertIn(self.strings['save20_dither'], self.strings['save20_gif_description'])
        self.assertNotIn('抖色', self.strings['save20_gif_description'])
        dialog = (CLASSIC / 'SaveOptionsDialog.kt').read_text(encoding='utf-8')
        self.assertIn('text=ui(R.string.save20_dither)', dialog)
        self.assertIn('ImageFormat.GIF -> R.string.save20_gif_description', dialog)

    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture('taiwan_priority_current_wording.json'), KEYS, TAGS)
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in [('default', 'values'), ('zh-TW', 'values-zh-rTW')]}
        cls.strings = {n.get('name'): n.text or '' for n in ET.fromstring(cls.xml['zh-TW']) if n.tag == 'string'}
        cls.activity = (CLASSIC / 'ClassicPaintActivity.kt').read_text(encoding='utf-8')

    def test_all_eighteen_complete_values_attributes_arguments_and_paragraphs(self):
        for key, values in self.data['values'].items():
            self.assertEqual(TAGS, set(self.data['constraints'][key]))
            for tag, expected in values.items():
                constraints = self.data['constraints'][key][tag]
                self.assertEqual({'attributes', 'formatted', 'placeholders', 'escaped_newline_count'}, set(constraints))
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, current_source_expectation(key, tag, expected), constraints)
                    self.assertEqual(catalogues.placeholders(values['default']), catalogues.placeholders(expected))
                    self.assertEqual(values['default'].count(r'\n'), expected.count(r'\n'))
        self.assertEqual([], catalogues.validate_catalogue('zh-TW', require_complete=True))

    def test_fixture_cannot_omit_a_key_locale_constraint_or_full_text(self):
        for key in KEYS:
            for mutation in ('key', 'locale', 'constraint', 'empty'):
                changed = deepcopy(self.data)
                if mutation == 'key': del changed['values'][key]
                elif mutation == 'locale': del changed['values'][key]['zh-TW']
                elif mutation == 'constraint': del changed['constraints'][key]
                else: changed['values'][key]['zh-TW'] = ''
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_wording_shape(changed, KEYS, TAGS)

    def test_missing_duplicate_truncation_markup_attributes_and_wrong_type_fail(self):
        for key in KEYS:
            for mutation in ('missing', 'duplicate', 'truncate', 'markup', 'attributes', 'type'):
                root = ET.fromstring(self.xml['zh-TW']); node = root.find(f"./string[@name='{key}']")
                if mutation == 'missing': root.remove(node)
                elif mutation == 'duplicate': root.append(deepcopy(node))
                elif mutation == 'truncate': node.text = node.text[:-1]
                elif mutation == 'markup': ET.SubElement(node, 'b').text, node.text = node.text, None
                elif mutation == 'attributes': node.set('translatable', 'false')
                else: node.tag = 'plurals'
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key,
                                   self.data['values'][key]['zh-TW'], self.data['constraints'][key]['zh-TW'])

    def test_unexpected_format_arguments_invalid_escapes_and_paragraph_loss_fail(self):
        for key in KEYS:
            for suffix in (' %2$s', " '"):
                changed = self.data['values'][key]['zh-TW'] + suffix
                root = ET.fromstring(self.xml['zh-TW']); root.find(f"./string[@name='{key}']").text = changed
                with self.subTest(key=key, suffix=suffix), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, changed, self.data['constraints'][key]['zh-TW'])
        root = ET.fromstring(self.xml['zh-TW'])
        changed = self.strings[NOTE].replace(r'\n\n', ' ')
        root.find(f"./string[@name='{NOTE}']").text = changed
        with self.assertRaisesRegex(ValueError, 'escaped newlines differ'):
            require_string(ET.tostring(root, encoding='unicode'), NOTE, changed, self.data['constraints'][NOTE]['zh-TW'])

    def test_picker_restores_heading_maintenance_and_both_english_fallback_cases(self):
        value = self.strings[NOTE]
        self.assertEqual('應用程式語言', value.split(r'\n\n')[0])
        self.assertIn('翻譯內容會在 AN Paint 的語言資源中維護。', value)
        self.assertIn('新增或尚未翻譯的文字會以英文顯示。', value)
        self.assertNotIn('所有可翻譯的介面文字', value)
        picker = (CLASSIC / 'AppLanguage.kt').read_text()
        self.assertTrue(code_locations(picker, 'text = ui(R.string.' + NOTE + ')'))

    def test_save_ellipsis_and_generic_discard_keep_their_distinct_contexts(self):
        s = self.strings
        self.assertEqual(('儲存', '儲存…', '要儲存變更嗎？', '捨棄', '捨棄變更'),
                         tuple(s[k] for k in ('ui_save', 'ui_save_a5d0d9', 'ui_save_your_changes', 'ui_discard', 'ui_discard_changes23')))
        block = kotlin_block(self.activity, 'private fun confirmReplacement(action: () -> Unit) {')
        self.assertTrue(code_locations(block, '.setPositiveButton(ui(R.string.ui_save_a5d0d9)) { _, _ -> afterSave = action; requestSave(false) }'))
        self.assertTrue(code_locations(block, '.setNeutralButton(ui(R.string.ui_discard_changes23)) { _, _ -> action() }'))

    def test_recovery_keeps_exact_route_archive_image_and_retained_data(self):
        s = self.strings
        route = '「' + s['ui_menu_file'] + '」>「' + s['ui_export_recovery_copy'].rstrip('…') + '」'
        self.assertIn(route, s[RECOVERY])
        self.assertEqual(1, s[RECOVERY].count('%1$s'))
        self.assertIn('請從 ZIP 中解壓縮 canvas.png，再載入這張圖片。', s[RECOVERY])
        self.assertIn('「' + s['ui_menu_file'] + '」>「' + s['ui_load_image'].rstrip('…') + '」', s[EXPORTED])
        self.assertTrue(s[EXPORTED].endswith('ZIP 也包含草稿設定及任何浮動選取範圍。'))
        recovery = (CLASSIC / 'EditorDraftRecovery.kt').read_text()
        self.assertTrue(code_locations(recovery, 'recoveryNotice=ui(R.string.' + RECOVERY + ',reason)'))
        self.assertTrue(code_locations(self.activity, 'message(ui(R.string.' + EXPORTED + '))'))

    def test_visible_swatch_and_hex_terms_keep_foreground_background_roles(self):
        self.assertEqual(('前景', '背景', '十六進位 #RRGGBB'),
                         tuple(self.strings[k] for k in ('ui_fg', 'ui_bg', 'ui_hex_rrggbb')))
        colour = (CLASSIC / 'ColourStatusButton.kt').read_text()
        self.assertEqual(2, len(code_locations(colour, 'listOf(foreground to ui(R.string.ui_fg),backgroundColour to ui(R.string.ui_bg))')))
        self.assertTrue(code_locations(colour, 'foregroundTarget.contentDescription=ui(R.string.ui_foreground_edit_colour,hex(foreground))'))
        self.assertTrue(code_locations(colour, 'backgroundTarget.contentDescription=ui(R.string.ui_background_edit_colour,hex(backgroundColour))'))

    def test_navigation_resumes_drawing_and_canvas_teaches_distinct_gestures(self):
        self.assertEqual('繼續繪圖', self.strings['ui_draw_again'])
        self.assertTrue(code_locations(self.activity, 'options.addView(button(ui(R.string.ui_draw_again), "navigate_draw") { chooseTool(drawingTool) }'))
        hint = self.strings['ui_drawing_canvas_pinch_and_move_two_fingers_to']
        self.assertIn('用兩指捏合或張開可縮放，移動兩指可平移。', hint)
        self.assertIn('「移動與縮放」模式也可用單指平移。', hint)
        canvas = (CLASSIC / 'PaintCanvas.kt').read_text()
        self.assertTrue(code_locations(canvas, 'contentDescription = ui(R.string.ui_drawing_canvas_pinch_and_move_two_fingers_to)'))

    def test_no_resize_warning_keeps_native_budget_failure_and_recovery_action(self):
        warning = self.strings['ui_no_resize_fits_decoder_memory']
        self.assertEqual('即使使用最小的輸出尺寸，此圖片的解碼器工作緩衝區仍會超出目前的記憶體上限。請取消並使用較小的來源圖片。', warning)
        resize = (CLASSIC / 'ImageResizeDialog.kt').read_text()
        self.assertTrue(code_locations(resize, 'val cannotResize=memoryRequirements.hasNativeWork && !memoryRequirements.accepts(current,ImportPlan.create(source,ImageDimensions(1,1)),residentPixels)'))
        self.assertTrue(code_locations(resize, 'else if(cannotResize) "\\n"+ui(R.string.ui_no_resize_fits_decoder_memory)'))

    def test_dormant_holds_and_prior_sampled_memory_value_remain_distinct(self):
        expected = {'ui_foreground_background_colour_palette': '前景色 %1$s，背景色 %2$s。%3$s 調色盤。',
                    'ui_main23': '主要',
                    'ui_sampled_resize_memory_explanation': '估算包括目前畫布及剪貼簿、取樣解碼及編輯緩衝區。實際記憶體用量會有所不同。較小的副本會損失細節。原始檔案不會改變。'}
        for key, value in expected.items():
            self.assertNotIn(key, KEYS)
            self.assertEqual(value, self.strings[key])
        # The two held resources remain dormant, not newly accepted live messages.
        for key in ('ui_foreground_background_colour_palette', 'ui_main23', 'ui_discard'):
            for path in CLASSIC.glob('*.kt'):
                self.assertFalse(code_locations(path.read_text(), 'R.string.' + key + ')'), (path.name, key))


if __name__ == '__main__':
    unittest.main()
