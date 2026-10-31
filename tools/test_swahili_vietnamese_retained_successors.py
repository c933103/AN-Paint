"""Current drawing and magnifier consumers, not historical successor approval."""
import unittest
import translation_catalogues as catalogues


class SwahiliVietnameseRetainedSuccessorsTest(unittest.TestCase):
    def test_return_to_drawing_consumer_does_not_recreate_content(self):
        source=(catalogues.ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt').read_text()
        self.assertIn('button(ui(R.string.ui_draw_again), "navigate_draw") { chooseTool(drawingTool) }',source)
        self.assertEqual('Rudi kuchora',catalogues.read_strings(catalogues.catalogue_paths()['sw'])['ui_draw_again'])

    def test_magnifier_label_remains_shared_between_cursor_and_active_preview(self):
        source=(catalogues.ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt').read_text()
        self.assertIn('tag="cursor_magnifier_enabled";text=ui(R.string.ui_show_magnified_drawing_preview)',source)
        self.assertIn('toggle(ui(R.string.ui_show_magnified_drawing_preview),paintCanvas.activeMagnifier,"magnifier_enabled")',source)
        self.assertEqual('Hiện bản xem trước phóng đại của bản vẽ',catalogues.read_strings(catalogues.catalogue_paths()['vi'])['ui_show_magnified_drawing_preview'])
