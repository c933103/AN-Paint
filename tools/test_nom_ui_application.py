"""Source call-site guards, not device/glyph rendering tests."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
JAVA = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'


def source(name):
    return (JAVA / name).read_text()


class NomUiApplicationTest(unittest.TestCase):
    def test_assembly_empty_instruction_uses_ui_typeface(self):
        body = source('AssemblyCanvas.kt').split('if (layout.isEmpty() && selectedId == null)', 1)[1].split('return', 1)[0]
        self.assertIn('typeface = VerticalText.uiTypeface(context)', body)
        self.assertIn('R.string.ui_add_images_then_drag_a_thumbnail_here', body)

    def test_horizontal_colour_caption_uses_ui_typeface(self):
        body = source('ColourStatusButton.kt').split('val colourRight=', 1)[1]
        self.assertIn('Typeface.create(VerticalText.uiTypeface(context) ?: Typeface.DEFAULT,Typeface.BOLD)', body)
        self.assertIn('c.drawText(label', body)

    def test_selection_rotation_caption_uses_ui_typeface(self):
        body = source('PaintCanvas.kt').split('private fun drawSelectionHandles', 1)[1].split('s.geometry.resizeHandles()', 1)[0]
        self.assertIn('typeface=VerticalText.uiTypeface(context)', body)
        self.assertIn('R.string.ui_rotate', body)

    def test_known_app_toasts_pass_through_api21_font_binding(self):
        paths = ('AdvancedColourDialog.kt', 'AssemblyActivity.kt', 'ClassicPaintActivity.kt',
                 'GalleryCredits.kt', 'LegalInfo.kt', 'MediaGalleryActivity.kt')
        for name in paths:
            self.assertNotIn('Toast.makeText(', source(name), name)
            self.assertIn('LocaleTypography.toast(', source(name), name)
        helper = source('LocaleTypography.kt')
        self.assertIn('if(Build.VERSION.SDK_INT<30) toast.view?.let {install(it)}', helper)

    def test_explicit_drawing_font_boundaries_remain(self):
        self.assertIn('filterNot {it.optBoolean("ui_only")}', source('FontCatalog.kt'))
        self.assertIn('if(index!=0) return face(index,style)', source('FontCatalog.kt'))
        self.assertIn('tag!="text_content"', source('LocaleTypography.kt'))
        self.assertIn('tag?.startsWith("font_option_")!=true', source('LocaleTypography.kt'))


if __name__ == '__main__':
    unittest.main()
