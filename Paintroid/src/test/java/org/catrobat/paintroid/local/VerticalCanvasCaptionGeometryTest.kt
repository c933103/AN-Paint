package org.catrobat.paintroid.local

import android.graphics.*
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

/** Native helper geometry tests; actual View/resource integration is covered separately. */
@RunWith(RobolectricTestRunner::class)
@Config(manifest=Config.NONE,sdk=[30,35])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@Suppress("DEPRECATION")
class VerticalCanvasCaptionGeometryTest {
    private fun image()=Bitmap.createBitmap(240,320,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.WHITE)}
    @Test fun copiesAlignmentAndMatchesSharedRendererWithoutMovingTheCanvas() {
        for(direction in listOf(TextDirection.VERTICAL_LR,TextDirection.VERTICAL_RL)) {
            val paint=Paint(Paint.ANTI_ALIAS_FLAG).apply {color=Color.BLACK;textSize=24f;textAlign=Paint.Align.CENTER}
            val copy=Paint(paint).apply {textAlign=Paint.Align.LEFT}
            val value="A\nBC✅"
            val caption=VerticalCanvasCaption(value,paint,180f,direction)
            val expected=image();val actual=image()
            try {
                val canvas=Canvas(actual);val before=Matrix(canvas.matrix)
                caption.draw(canvas,30f,40f)
                assertEquals(before,canvas.matrix)
                val reference=Canvas(expected);reference.translate(30f,40f)
                VerticalText.draw(reference,VerticalText.wrapLabel(value,copy,180f,direction),copy,direction,GlyphOrientation.MIXED)
                assertTrue(actual.sameAs(expected))
                assertEquals(Paint.Align.CENTER,paint.textAlign)
                assertEquals(24f,paint.textSize,0f)
            } finally {expected.recycle();actual.recycle()}
        }
    }
    @Test fun placementUsesBothSidesAndContainsFittingBoxes() {
        val paint=Paint().apply {textSize=18f}
        val viewport=RectF(4f,4f,200f,300f)
        for(direction in listOf(TextDirection.VERTICAL_LR,TextDirection.VERTICAL_RL)) {
            val caption=VerticalCanvasCaption("AB",paint,200f,direction)
            for(grip in listOf(PointF(100f,150f),PointF(4f,4f),PointF(199f,299f))) {
                val origin=caption.beside(grip,viewport,10f)
                assertTrue(origin.x>=viewport.left);assertTrue(origin.x+caption.width<=viewport.right)
                assertTrue(origin.y>=viewport.top);assertTrue(origin.y+caption.height<=viewport.bottom)
                if(grip.x==100f) assertEquals(if(direction==TextDirection.VERTICAL_LR) 110f else 90f-caption.width,origin.x,0f)
            }
            val tiny=caption.beside(PointF(0f,0f),RectF(4f,4f,2f,2f),10f)
            assertTrue(tiny.x.isFinite());assertTrue(tiny.y.isFinite())
        }
    }
    @Test fun fittingCaptionsAvoidTheSelectionAndImpossibleCasesKeepTheBoundedFallback() {
        val paint=Paint().apply {textSize=14f}
        val viewport=RectF(4f,4f,236f,316f)
        val grip=PointF(120f,140f)
        val selection=RectF(50f,160f,200f,250f)
        for(direction in listOf(TextDirection.VERTICAL_LR,TextDirection.VERTICAL_RL)) {
            val caption=VerticalCanvasCaption("Rotate slowly",paint,300f,direction)
            val original=caption.beside(grip,viewport,10f)
            fun box(point: PointF)=RectF(point.x,point.y,point.x+caption.width,point.y+caption.height)
            assertTrue("Fixture must exercise an original outline overlap",RectF.intersects(box(original),selection))
            val origin=caption.beside(grip,viewport,10f,selection)
            assertTrue(viewport.contains(box(origin)))
            assertFalse(RectF.intersects(box(origin),selection))
            assertFalse(RectF.intersects(box(origin),RectF(110f,130f,130f,150f)))
            // An obstacle covering the whole viewport admits no outside caption.
            assertEquals(original,caption.beside(grip,viewport,10f,RectF(viewport)))
        }
    }

    @Test fun screenPixelCaptionSurvivesCounterScalingAtOneBillionthZoom() {
        val paint=Paint(Paint.ANTI_ALIAS_FLAG).apply {color=Color.BLACK;textSize=14f}
        for(direction in listOf(TextDirection.VERTICAL_LR,TextDirection.VERTICAL_RL)) {
            val caption=VerticalCanvasCaption("Rotate",paint,260f,direction)
            val reference=image()
            try {
                caption.draw(Canvas(reference),100f,100f)
                for(zoom in listOf(1e-9f,.125f,1f,8f,32f)) {
                    val actual=image()
                    try {
                        val canvas=Canvas(actual)
                        canvas.scale(zoom,zoom)
                        canvas.translate(80f/zoom,90f/zoom)
                        canvas.scale(1/zoom,1/zoom)
                        caption.draw(canvas,20f,10f)
                        assertTrue("direction=$direction zoom=$zoom",actual.sameAs(reference))
                    } finally {actual.recycle()}
                }
            } finally {reference.recycle()}
        }
    }
}
