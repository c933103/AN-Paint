/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.graphics.*
import android.view.MotionEvent
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RuntimeEnvironment
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30],qualifiers="en-rUS-w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CursorDrawingTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private fun board(): PaintCanvas {
        val document=PaintDocument().apply {newImage(100,100);strokeWidth=8f;foreground=Color.RED}
        return PaintCanvas(context,document).apply {layout(0,0,824,1000);fit();setCursorMode(true)}
    }
    private fun touch(board: PaintCanvas,action: Int,x: Float,y: Float) {
        val e=MotionEvent.obtain(0,20,action,x,y,0);board.onTouchEvent(e);e.recycle()
    }
    private fun tap(board: PaintCanvas) {touch(board,MotionEvent.ACTION_DOWN,100f,500f);touch(board,MotionEvent.ACTION_UP,100f,500f)}
    private fun pixels(board: PaintCanvas)=IntArray(10000).also {board.document.bitmap.getPixels(it,0,100,0,0,100,100)}

    @Test fun enablingCursorOnlyPositionsUntilDrawingIsExplicitlyStarted() {
        val board=board();val doc=board.document;val original=pixels(board)
        assertFalse(board.cursorDrawing);assertFalse(doc.canUndo)
        tap(board);assertArrayEquals(original,pixels(board));assertFalse(doc.canUndo)
        board.setCursorDrawing(true)
        tap(board);assertTrue(board.cursorDrawing);assertTrue(doc.canUndo)
        assertTrue(pixels(board).any {it==Color.RED});val dot=pixels(board)
        board.setCursorDrawing(false)
        tap(board);assertFalse(board.cursorDrawing);assertArrayEquals(dot,pixels(board))
        doc.undo();assertArrayEquals(original,pixels(board));assertFalse(doc.canUndo)
    }

    @Test fun movingAndTappingNeverToggleInkAndCancelRollsBack() {
        val board=board();val original=pixels(board);board.setCursorDrawing(false)
        touch(board,MotionEvent.ACTION_DOWN,100f,500f)
        // Repositioning, including touch jitter, must never enable ink.
        repeat(12) {touch(board,MotionEvent.ACTION_MOVE,if(it%2==0) 106f else 100f,500f)}
        touch(board,MotionEvent.ACTION_UP,100f,500f)
        assertFalse(board.cursorDrawing);assertArrayEquals(original,pixels(board));assertFalse(board.document.canUndo)
        board.setCursorDrawing(true);tap(board);val dot=pixels(board);val position=board.draftState().getDouble("cursor_x")
        touch(board,MotionEvent.ACTION_DOWN,100f,500f);touch(board,MotionEvent.ACTION_MOVE,150f,500f)
        assertFalse(dot.contentEquals(pixels(board)))
        touch(board,MotionEvent.ACTION_CANCEL,150f,500f)
        assertArrayEquals(dot,pixels(board));assertEquals(position,board.draftState().getDouble("cursor_x"),0.0)
    }

    @Test fun strokesShorterThanTouchSlopSurviveLiftForEveryCursorBrush() {
        for(tool in listOf(PaintTool.BRUSH,PaintTool.PENCIL,PaintTool.WATERCOLOR,PaintTool.ERASER)) {
            val board=board();board.selectTool(tool);board.setCursorDrawing(true);board.zoomAt(1f)
            board.document.strokeWidth=1f;board.pencilSize=1f
            board.document.bitmap.eraseColor(Color.BLUE)
            val original=pixels(board)
            touch(board,MotionEvent.ACTION_DOWN,100f,500f)
            touch(board,MotionEvent.ACTION_MOVE,103f,500f)
            touch(board,MotionEvent.ACTION_UP,103f,500f)
            assertTrue("$tool must retain a short line, not cancel it as a tap",pixels(board).count {it!=Color.BLUE}>=3)
            assertTrue(board.cursorDrawing);assertTrue(board.document.canUndo)
            board.document.undo();assertArrayEquals(original,pixels(board));assertFalse(board.document.canUndo)
        }
    }

    @Test fun circleAndSquareCursorOutlinesFollowTheActualBrushCapAndWidth() {
        val overlay=PaintroidCursorOverlay()
        fun render(cap: Paint.Cap,width: Float): Bitmap {
            val image=Bitmap.createBitmap(200,200,Bitmap.Config.ARGB_8888);image.eraseColor(Color.WHITE)
            overlay.draw(Canvas(image),PointF(100f,100f),Paint().apply {strokeCap=cap;strokeWidth=width;color=Color.RED},1f,1f,true)
            return image
        }
        val round=render(Paint.Cap.ROUND,20f);val square=render(Paint.Cap.SQUARE,20f)
        assertEquals(Color.WHITE,round.getPixel(116,116));assertNotEquals(Color.WHITE,square.getPixel(116,116))
        val large=render(Paint.Cap.ROUND,60f)
        assertNotEquals(Color.WHITE,large.getPixel(126,126));assertEquals(Color.WHITE,round.getPixel(126,126))
        listOf(round,square,large).forEach {it.recycle()}
    }

    @Test fun fittedImagesKeepAVisibleMarkerWithoutInflatingTheBrushFootprint() {
        fun markerWidth(zoom: Float,visibility: Float): Int {
            val image=Bitmap.createBitmap(400,400,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.WHITE)}
            val canvas=Canvas(image);canvas.translate(200f,200f);canvas.scale(zoom,zoom)
            PaintroidCursorOverlay().draw(canvas,PointF(0f,0f),Paint().apply {strokeCap=Paint.Cap.SQUARE;strokeWidth=2f},zoom,1f,false,visibility)
            val touched=(0 until 400).filter {image.getPixel(it,200)!=Color.WHITE}
            // The marker surrounds the actual one-pixel half-width; its centre stays clear.
            if(zoom>=1f) assertEquals(Color.WHITE,image.getPixel(200,200))
            image.recycle();return touched.last()-touched.first()+1
        }
        val normal=markerWidth(1f,1f)
        assertTrue(normal>90)
        assertEquals(normal.toDouble(),markerWidth(.1f,1f).toDouble(),3.0)
        assertEquals(normal.toDouble(),markerWidth(.5f,1f).toDouble(),3.0)
        assertTrue(markerWidth(.1f,1.5f)>normal*1.4)
    }

    @Test fun magnifierSamplesCursorInsteadOfFingerAndItsPreferenceSurvivesDraftRestore() {
        val board=board();board.document.bitmap.eraseColor(Color.BLUE)
        val state=board.draftState();val x=state.getDouble("cursor_x").toFloat();val y=state.getDouble("cursor_y").toFloat()
        Canvas(board.document.bitmap).drawRect(x-2,y-2,x+2,y+2,Paint().apply {color=Color.RED})
        touch(board,MotionEvent.ACTION_DOWN,700f,700f)
        val image=Bitmap.createBitmap(board.width,board.height,Bitmap.Config.ARGB_8888)
        board.draw(Canvas(image))
        // The unobstructed upper-left circular lens is 120 dp wide, inset 8 dp.
        assertEquals(Color.RED,image.getPixel(136,136))
        assertNotEquals(Color.RED,image.getPixel(17,17))
        val file=java.io.File("build/reports/classic-preview/cursor-magnifier.png");file.parentFile.mkdirs()
        file.outputStream().use {image.compress(Bitmap.CompressFormat.PNG,100,it)};image.recycle()
        touch(board,MotionEvent.ACTION_CANCEL,700f,700f)
        board.cursorMagnifier=false;board.cursorMarkerScale=1.5f;board.setCursorDrawing(true)
        val restored=board();restored.restoreDraft(board.draftState())
        assertFalse(restored.cursorMagnifier);assertTrue(restored.cursorMode);assertFalse(restored.cursorDrawing)
        assertEquals(1.5f,restored.cursorMarkerScale,0f)
        board.setCursorDrawing(false);restored.restoreDraft(board.draftState());assertFalse(restored.cursorDrawing)
        val legacy=board.draftState().apply {remove("cursor_drawing")}
        restored.restoreDraft(legacy);assertFalse(restored.cursorDrawing)
    }
}
