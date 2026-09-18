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

    @Test fun touchesAwayFromTheCursorNeverToggleInkAndCancelRollsBack() {
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
        assertNotEquals(Color.WHITE,large.getPixel(125,125));assertEquals(Color.WHITE,round.getPixel(125,125))
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
        assertTrue("Main marker retains its compact size",normal in 60..79)
        assertEquals(normal.toDouble(),markerWidth(.1f,1f).toDouble(),3.0)
        assertEquals(normal.toDouble(),markerWidth(.5f,1f).toDouble(),3.0)
        assertTrue(markerWidth(.1f,1.5f)>normal*1.4)
    }

    @Test fun cursorOutlineDoesNotChangeTheBrushAndActiveStateIsVisible() {
        val board=board();board.setCursorMode(false)
        board.document.brushTip=2;board.setCursorMode(true)
        assertEquals("Cursor mode preserves the calligraphy brush",2,board.document.brushTip)
        fun rendered(drawing: Boolean,shape: Int): IntArray {
            val image=Bitmap.createBitmap(200,200,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.WHITE)}
            val brush=Paint().apply {strokeCap=Paint.Cap.ROUND;strokeWidth=20f;color=Color.RED}
            PaintroidCursorOverlay().draw(Canvas(image),PointF(100f,100f),brush,1f,1f,drawing,1f,if(shape==0) Paint.Cap.ROUND else Paint.Cap.SQUARE)
            assertEquals(Paint.Cap.ROUND,brush.strokeCap)
            return IntArray(40000).also {image.getPixels(it,0,200,0,0,200,200);image.recycle()}
        }
        val positioning=rendered(false,0);val active=rendered(true,0)
        assertFalse(positioning.contentEquals(active));assertTrue(active.any {it==Color.RED})
        assertFalse(active.contentEquals(rendered(true,1)))
    }

    @Test fun magnifierSamplesCursorInsteadOfFingerAndItsPreferenceSurvivesDraftRestore() {
        val board=board();board.document.bitmap.eraseColor(Color.BLUE)
        val state=board.draftState();val x=state.getDouble("cursor_x").toFloat();val y=state.getDouble("cursor_y").toFloat()
        Canvas(board.document.bitmap).drawRect(x-2,y-2,x+2,y+2,Paint().apply {color=Color.RED})
        touch(board,MotionEvent.ACTION_DOWN,700f,700f)
        val image=Bitmap.createBitmap(board.width,board.height,Bitmap.Config.ARGB_8888)
        board.draw(Canvas(image))
        // Preserve the 120 dp lens area; it samples the cursor, not the finger.
        assertEquals(RectF(16f,16f,256f,256f),board.magnifierBounds())
        assertEquals(Color.RED,image.getPixel(136,136))
        assertNotEquals(Color.RED,image.getPixel(17,17))
        val file=java.io.File("build/reports/classic-preview/cursor-magnifier.png");file.parentFile.mkdirs()
        file.outputStream().use {image.compress(Bitmap.CompressFormat.PNG,100,it)};image.recycle()
        touch(board,MotionEvent.ACTION_UP,700f,700f)
        assertTrue("Positioning preview remains visible after lifting the finger",board.magnifierVisible)
        val still=Bitmap.createBitmap(board.width,board.height,Bitmap.Config.ARGB_8888)
        board.draw(Canvas(still));assertEquals(Color.RED,still.getPixel(136,136));still.recycle()
        board.cursorMagnifier=false;board.cursorMarkerScale=1.5f;board.cursorShape=1;board.setCursorDrawing(true)
        val restored=board();restored.restoreDraft(board.draftState())
        assertFalse(restored.cursorMagnifier);assertTrue(restored.cursorMode);assertFalse(restored.cursorDrawing)
        assertEquals(1.5f,restored.cursorMarkerScale,0f);assertEquals(1,restored.cursorShape)
        board.setCursorDrawing(false);restored.restoreDraft(board.draftState());assertFalse(restored.cursorDrawing)
        val legacy=board.draftState().apply {remove("cursor_drawing")}
        restored.restoreDraft(legacy);assertFalse(restored.cursorDrawing)
    }

    @Test fun navigateMagnifierSamplesTheFingerAfterBothPanningAndClampedMovement() {
        // At 5x this 100 px image stays centred inside the viewport; at 12x it can pan.
        for(scale in listOf(5f,12f)) {
            val board=board();board.setCursorMode(false);board.selectTool(PaintTool.ZOOM);board.zoomAt(scale)
            board.document.bitmap.eraseColor(Color.BLUE)
            Canvas(board.document.bitmap).drawRect(45f,45f,55f,55f,Paint().apply {color=Color.RED})
            board.activeMagnifier=true
            var point=board.toScreen(50f,50f)
            touch(board,MotionEvent.ACTION_DOWN,point.x,point.y)
            val image=Bitmap.createBitmap(board.width,board.height,Bitmap.Config.ARGB_8888)
            fun assertLens(expected: Int) {
                board.draw(Canvas(image))
                assertEquals("$scale: lens samples the image under the finger",expected,image.getPixel(136,136))
            }
            try {
                assertLens(Color.RED)
                point=PointF(point.x+35,point.y+25)
                touch(board,MotionEvent.ACTION_MOVE,point.x,point.y)
                val sampled=board.toImage(point.x,point.y)
                if(scale==5f) {
                    assertEquals(57f,sampled.x,.001f);assertEquals(55f,sampled.y,.001f)
                    assertLens(Color.BLUE)
                } else {
                    assertEquals(50f,sampled.x,.001f);assertEquals(50f,sampled.y,.001f)
                    assertLens(Color.RED)
                }
                touch(board,MotionEvent.ACTION_UP,point.x,point.y)
                board.draw(Canvas(image));assertFalse(board.magnifierVisible);assertNotEquals(Color.RED,image.getPixel(136,136))
                assertFalse(board.document.canUndo)
            } finally {image.recycle();board.document.close()}
        }
    }

    @Test fun activeMagnifierSettingControlsTheCurrentDrawingMode() {
        val board=board()
        board.activeMagnifier=false;assertFalse(board.cursorMagnifier)
        board.activeMagnifier=true;assertTrue(board.cursorMagnifier)
        board.setCursorMode(false);board.activeMagnifier=true;assertTrue(board.magnifiedPreview)
        board.setCursorMode(true);assertTrue(board.activeMagnifier)
        board.document.close()
    }

    @Test fun lensEnlargesRenderedPixelsByTheSelectedScaleRegardlessOfBitmapDensity() {
        val board=board();board.setCursorMode(false);board.selectTool(PaintTool.ZOOM)
        board.activeMagnifier=true
        board.document.bitmap.eraseColor(Color.WHITE)
        Canvas(board.document.bitmap).drawRect(48f,48f,52f,52f,Paint().apply {color=Color.RED})
        val original=pixels(board)
        val image=Bitmap.createBitmap(board.width,board.height,Bitmap.Config.ARGB_8888)
        fun redWidth(centre: PointF): Int {
            val y=centre.y.toInt()
            return (centre.x.toInt()-50..centre.x.toInt()+50).count {image.getPixel(it,y)==Color.RED}
        }
        try {
            for(density in listOf(Bitmap.DENSITY_NONE,160,480)) {
                board.document.bitmap.density=density
                for(scale in listOf(.5f,1f,2f)) {
                    board.zoomAt(scale)
                    val point=board.toScreen(50f,50f)
                    touch(board,MotionEvent.ACTION_DOWN,point.x,point.y)
                    for(magnification in listOf(1f,2f,4f)) {
                        board.previewMagnification=magnification;board.draw(Canvas(image))
                        val lens=board.magnifierBounds()
                        val mainWidth=redWidth(point)
                        val lensWidth=redWidth(PointF(lens.centerX(),lens.centerY()))
                        assertEquals("Main pixels at density $density / zoom $scale",(4*scale).toInt(),mainWidth)
                        assertEquals("Lens pixels at density $density / zoom $scale / magnification $magnification",
                            (4*maxOf(scale,1f)*magnification).toInt(),lensWidth)
                        assertArrayEquals("Display must not change the drawing",original,pixels(board))
                    }
                    touch(board,MotionEvent.ACTION_UP,point.x,point.y)
                }
            }
        } finally {image.recycle();board.document.close()}
    }

    @Test fun lensEnlargesTheRenderedCursorOutlineTogetherWithTheCanvas() {
        val board=board();board.document.strokeWidth=2f
        val image=Bitmap.createBitmap(board.width,board.height,Bitmap.Config.ARGB_8888)
        // A diagonal crosses the outline without intersecting the crosshair arms.
        fun outlineExtent(centre: PointF): Int {
            val positions=(1..75).filter {offset ->
                val colour=image.getPixel(centre.x.toInt()+offset,centre.y.toInt()+offset)
                Color.red(colour)<150 && Color.green(colour)<150 && Color.blue(colour)<150
            }
            assertTrue("A visible outline must be rendered",positions.isNotEmpty())
            return positions.last()
        }
        try {
            for(shape in listOf(0,1)) for(scale in listOf(1f,2f)) {
                board.cursorShape=shape;board.zoomAt(scale)
                val state=board.draftState()
                val point=board.toScreen(state.getDouble("cursor_x").toFloat(),state.getDouble("cursor_y").toFloat())
                for(magnification in listOf(1f,2f,4f)) {
                    board.previewMagnification=magnification;board.draw(Canvas(image))
                    val lens=board.magnifierBounds()
                    val mainExtent=outlineExtent(point)
                    val lensExtent=outlineExtent(PointF(lens.centerX(),lens.centerY()))
                    assertEquals("Shape $shape at zoom $scale must enlarge with the lens",
                        mainExtent*magnification,lensExtent.toFloat(),magnification+1f)
                    assertFalse(board.document.canUndo)
                }
            }
        } finally {image.recycle();board.document.close()}
    }

    @Test fun tappingTheCursorTogglesInkWithoutPaintingAndDraggingItStillDraws() {
        val board=board();board.zoomAt(2f);board.document.strokeSmoothing=false
        val original=pixels(board)
        var notifications=0;board.onCursorDrawingToggled={notifications++}
        fun position(): PointF {
            val state=board.draftState()
            return board.toScreen(state.getDouble("cursor_x").toFloat(),state.getDouble("cursor_y").toFloat())
        }
        val start=position()
        touch(board,MotionEvent.ACTION_DOWN,start.x,start.y)
        touch(board,MotionEvent.ACTION_MOVE,start.x+2,start.y+1)
        touch(board,MotionEvent.ACTION_UP,start.x+2,start.y+1)
        assertTrue(board.cursorDrawing);assertEquals(1,notifications)
        assertArrayEquals(original,pixels(board));assertFalse(board.document.canUndo)
        touch(board,MotionEvent.ACTION_DOWN,start.x,start.y)
        touch(board,MotionEvent.ACTION_MOVE,start.x+40,start.y)
        touch(board,MotionEvent.ACTION_UP,start.x+40,start.y)
        assertTrue(board.cursorDrawing);assertEquals(1,notifications);assertTrue(board.document.canUndo)
        val line=pixels(board);assertTrue(line.count {it==Color.RED}>20)
        val end=position()
        touch(board,MotionEvent.ACTION_DOWN,end.x,end.y)
        touch(board,MotionEvent.ACTION_UP,end.x,end.y)
        assertFalse(board.cursorDrawing);assertEquals(2,notifications);assertArrayEquals(line,pixels(board))
        board.document.undo();assertArrayEquals(original,pixels(board));assertFalse(board.document.canUndo)
        board.document.close()
    }

    @Test fun cancelledCursorTapDoesNotEnableInkAndCancelledCursorDragRestoresTheImage() {
        val board=board();board.zoomAt(2f)
        val state=board.draftState();val x=state.getDouble("cursor_x").toFloat();val y=state.getDouble("cursor_y").toFloat()
        val point=board.toScreen(x,y);val original=pixels(board)
        touch(board,MotionEvent.ACTION_DOWN,point.x,point.y)
        touch(board,MotionEvent.ACTION_CANCEL,point.x,point.y)
        assertFalse(board.cursorDrawing);assertFalse(board.document.canUndo)
        board.setCursorDrawing(true)
        touch(board,MotionEvent.ACTION_DOWN,point.x,point.y)
        touch(board,MotionEvent.ACTION_MOVE,point.x+50,point.y)
        assertFalse(original.contentEquals(pixels(board)))
        touch(board,MotionEvent.ACTION_CANCEL,point.x+50,point.y)
        assertArrayEquals(original,pixels(board));assertFalse(board.document.canUndo)
        assertEquals(x.toDouble(),board.draftState().getDouble("cursor_x"),0.0)
        board.document.close()
    }

    @Test fun magnifierMovesOnlyToAvoidTheFingerAndKeepsItsCornerAfterLift() {
        val board=board()
        assertTrue(board.magnifierVisible)
        assertEquals(16f,board.magnifierBounds().left,0f)
        touch(board,MotionEvent.ACTION_DOWN,90f,90f)
        assertEquals(528f,board.magnifierBounds().left,0f)
        touch(board,MotionEvent.ACTION_MOVE,430f,250f)
        assertEquals("Crossing the screen centre must not move the lens",528f,board.magnifierBounds().left,0f)
        touch(board,MotionEvent.ACTION_UP,430f,250f)
        assertEquals(528f,board.magnifierBounds().left,0f)
        touch(board,MotionEvent.ACTION_DOWN,680f,90f)
        assertEquals(16f,board.magnifierBounds().left,0f)
        touch(board,MotionEvent.ACTION_CANCEL,680f,90f)
        board.activeMagnifier=false;assertFalse(board.magnifierVisible)
        board.document.close()
    }

    @Test fun aSecondFingerCancelsACursorTapAndPreviewReturnsAfterPinching() {
        val board=board();val point=board.toScreen(50f,50f)
        touch(board,MotionEvent.ACTION_DOWN,point.x,point.y)
        val properties=Array(2) {i ->MotionEvent.PointerProperties().apply {id=i;toolType=MotionEvent.TOOL_TYPE_FINGER}}
        val coordinates=Array(2) {i ->MotionEvent.PointerCoords().apply {x=point.x+i*100;y=point.y;pressure=1f;size=1f}}
        val event=MotionEvent.obtain(0,30,MotionEvent.ACTION_POINTER_DOWN or (1 shl MotionEvent.ACTION_POINTER_INDEX_SHIFT),
            2,properties,coordinates,0,0,1f,1f,0,0,android.view.InputDevice.SOURCE_TOUCHSCREEN,0)
        board.onTouchEvent(event);event.recycle()
        assertFalse(board.magnifierVisible)
        touch(board,MotionEvent.ACTION_UP,point.x,point.y)
        assertTrue(board.magnifierVisible);assertFalse(board.cursorDrawing);assertFalse(board.document.canUndo)
        board.document.close()
    }
}
