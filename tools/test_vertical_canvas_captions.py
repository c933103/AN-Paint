"""Source propagation guards; native view rendering is covered by Robolectric tests."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
JAVA = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'


class VerticalCanvasCaptionSourceTest(unittest.TestCase):
    def test_measurement_uses_a_left_aligned_copy_and_actual_wrapped_bounds(self):
        text = (JAVA / 'VerticalCanvasCaption.kt').read_text()
        for required in (
            'Paint(source).apply {textAlign=Paint.Align.LEFT}',
            'require(direction!=TextDirection.HORIZONTAL)',
            'VerticalText.wrapLabel(text,paint,availableHeight.coerceAtLeast(paint.fontSpacing),direction)',
            'VerticalText.bounds(label,paint,direction,GlyphOrientation.MIXED,1f)',
            'VerticalText.draw(canvas,label,paint,direction,GlyphOrientation.MIXED)',
        ):
            self.assertIn(required, text)
        self.assertNotIn('/zoom', text)

    def test_empty_assembly_instruction_routes_before_the_document_transform(self):
        text = (JAVA / 'AssemblyCanvas.kt').read_text()
        body = text.split('if (layout.isEmpty() && selectedId == null)', 1)[1].split('return', 1)[0]
        self.assertIn('typeface = VerticalText.uiTypeface(context)', body)
        self.assertIn('if(direction==TextDirection.HORIZONTAL)', body)
        self.assertIn('canvas.drawText(ui(R.string.ui_add_images_then_drag_a_thumbnail_here),width/2f,height/2f,p)', body)
        self.assertIn('VerticalCanvasCaption(ui(R.string.ui_add_images_then_drag_a_thumbnail_here),p,height-32*density,direction)', body)
        self.assertIn('caption.draw(canvas,(width-caption.width)/2,(height-caption.height)/2)', body)
        self.assertNotIn('canvas.scale(', body)

    def test_rotation_preserves_the_horizontal_call_and_measures_vertical_text_in_pixels(self):
        text = (JAVA / 'PaintCanvas.kt').read_text()
        body = text.split('private fun drawSelectionHandles', 1)[1].split('s.geometry.resizeHandles()', 1)[0]
        horizontal, vertical = body.split('if(direction==TextDirection.HORIZONTAL)', 1)[1].split('} else {', 1)
        self.assertIn('textSize=11*resources.displayMetrics.scaledDensity/zoom', horizontal)
        self.assertIn('canvas.drawText(ui(R.string.ui_rotate),grip.x+10*d,grip.y+4*d,text)', horizontal)
        self.assertIn('textSize=11*resources.displayMetrics.scaledDensity;', vertical)
        self.assertNotIn('textSize=11*resources.displayMetrics.scaledDensity/zoom', vertical)
        self.assertIn('typeface=VerticalText.uiTypeface(context)', vertical)
        self.assertIn('val viewport=RectF(rulerInset,rulerInset,width-bar,height-bar)', vertical)
        self.assertIn('val screen=toScreen(grip.x,grip.y)', vertical)
        self.assertIn('val selection=s.geometry.bounds()', vertical)
        self.assertIn('val origin=caption.beside(screen,viewport,10*pixels,avoid)', vertical)
        self.assertIn('canvas.save();canvas.translate(grip.x,grip.y);canvas.scale(1/zoom,1/zoom)', vertical)
        self.assertIn('caption.draw(canvas,origin.x-screen.x,origin.y-screen.y)', vertical)
        self.assertIn('canvas.restore()', vertical)

    def test_placement_tries_both_sides_without_moving_the_grip(self):
        text = (JAVA / 'VerticalCanvasCaption.kt').read_text()
        self.assertIn('if(direction==TextDirection.VERTICAL_LR) right else left', text)
        self.assertIn('fits(preferred) -> preferred', text)
        self.assertIn('fits(alternate) -> alternate', text)
        self.assertIn('width<=viewport.width()', text)
        self.assertIn('height<=viewport.height()', text)
        self.assertNotIn('grip.x=', text)
        self.assertNotIn('grip.y=', text)


if __name__ == '__main__':
    unittest.main()
