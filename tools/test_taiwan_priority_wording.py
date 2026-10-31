"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues
from test_assembly_help_pr8 import code_locations, kotlin_block

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
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in [('default', 'values'), ('zh-TW', 'values-zh-rTW')]}
        cls.strings = {n.get('name'): n.text or '' for n in ET.fromstring(cls.xml['zh-TW']) if n.tag == 'string'}
        cls.activity = (CLASSIC / 'ClassicPaintActivity.kt').read_text(encoding='utf-8')

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

    def test_no_resize_warning_keeps_current_limit_and_recovery_action(self):
        warning = self.strings['ui_no_resize_fits_decoder_memory']
        self.assertEqual('即使使用最小的輸出尺寸，也無法在目前的記憶體限制內載入此圖片進行編輯。請取消並使用較小的來源圖片。', warning)
        resize = (CLASSIC / 'ImageResizeDialog.kt').read_text()
        self.assertTrue(code_locations(resize, 'val cannotResize=memoryRequirements.hasNativeWork && !memoryRequirements.accepts(current,ImportPlan.create(source,ImageDimensions(1,1)),residentPixels)'))
        self.assertTrue(code_locations(resize, 'else if(cannotResize) "\\n"+ui(R.string.ui_no_resize_fits_decoder_memory)'))

if __name__ == '__main__':
    unittest.main()
