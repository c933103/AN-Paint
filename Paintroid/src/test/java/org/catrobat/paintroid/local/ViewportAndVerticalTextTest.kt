/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.*
import android.view.MotionEvent
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.json.JSONObject
import java.util.Locale

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ViewportAndVerticalTextTest {
    @Test fun rulersKeepPixelCoordinatesAndStayBoundedForLargeImagesAtEveryZoom() {
        for(zoom in listOf(.00001f,.25f,1f,8f,32f)) {
            val ticks=PixelRuler.ticks(-12f,zoom,24f,800f,100_000_000,64f)
            assertTrue(ticks.isNotEmpty());assertTrue(ticks.size<100)
            for(tick in ticks) {
                assertTrue(tick.position in 24f..800f)
                assertEquals(-12f+tick.pixel*zoom,tick.position,.001f)
            }
            val labels=ticks.filter {it.major}
            labels.zipWithNext().forEach {(a,b)->assertTrue(b.position-a.position>=63.9f)}
        }
    }
    @Test fun gridInsetsPreserveCentreThroughRotationDraftRestoreAndScrollbarDragging() {
        val doc=PaintDocument().apply {newImage(1600,1200)}
        val board=PaintCanvas(RuntimeEnvironment.getApplication(),doc)
        val bar=20*board.resources.displayMetrics.density
        fun centre(view: PaintCanvas)=view.toImage((view.width-bar+view.rulerInset)/2,(view.height-bar+view.rulerInset)/2)
        board.layout(0,0,800,600);board.zoomAt(2f)
        val before=centre(board);board.grid=true
        assertEquals(before.x,centre(board).x,.001f);assertEquals(before.y,centre(board).y,.001f)
        board.layout(0,0,500,900)
        assertEquals(before.x,centre(board).x,.001f);assertEquals(before.y,centre(board).y,.001f)
        val restored=PaintCanvas(RuntimeEnvironment.getApplication(),doc)
        restored.restoreDraft(board.draftState());restored.layout(0,0,1000,600)
        assertTrue(restored.grid);assertEquals(before.x,centre(restored).x,.001f);assertEquals(before.y,centre(restored).y,.001f)
        for((action,x) in listOf(MotionEvent.ACTION_DOWN to 500f,MotionEvent.ACTION_MOVE to 2000f,MotionEvent.ACTION_UP to 2000f)) {
            val event=MotionEvent.obtain(0,20,action,x,restored.height-2f,0);restored.dispatchTouchEvent(event);event.recycle()
        }
        val edge=restored.toScreen(1600f,0f)
        assertTrue(edge.x<restored.width-bar && edge.x>restored.width-bar-50*restored.resources.displayMetrics.density)
        assertFalse(doc.canUndo)
    }
    @Test fun rulerTouchesDoNotPaintAndCursorReportsPixelsDuringMovement() {
        val doc=PaintDocument().apply {newImage(500,400)}
        assertFalse(doc.paint(PaintTool.BRUSH).isAntiAlias)
        doc.antialiasing=true;assertTrue(doc.paint(PaintTool.BRUSH).isAntiAlias)
        val board=PaintCanvas(RuntimeEnvironment.getApplication(),doc)
        board.layout(0,0,800,600);board.grid=true;board.selectTool(PaintTool.BRUSH)
        fun touch(action: Int,x: Float,y: Float) {
            val event=MotionEvent.obtain(0,20,action,x,y,0);board.dispatchTouchEvent(event);event.recycle()
        }
        touch(MotionEvent.ACTION_DOWN,5f,100f);touch(MotionEvent.ACTION_MOVE,300f,300f);touch(MotionEvent.ACTION_UP,300f,300f)
        assertFalse(doc.canUndo)
        board.zoomAt(2f);board.setCursorMode(true);board.setCursorDrawing(false)
        val before=board.draftState();var readout="";board.onStatus={readout=board.zoomStatusLabel()}
        touch(MotionEvent.ACTION_DOWN,200f,200f);touch(MotionEvent.ACTION_MOVE,240f,260f)
        val moved=board.draftState()
        assertEquals(before.getDouble("cursor_x")+20,moved.getDouble("cursor_x"),.001)
        assertEquals(before.getDouble("cursor_y")+30,moved.getDouble("cursor_y"),.001)
        assertTrue(readout,readout.contains("x: ${moved.getDouble("cursor_x").toInt()}, y: ${moved.getDouble("cursor_y").toInt()}"))
        assertFalse(doc.canUndo)
        touch(MotionEvent.ACTION_CANCEL,240f,260f)
        assertEquals(before.getDouble("cursor_x"),board.draftState().getDouble("cursor_x"),0.0)
        board.setCursorMode(false);assertFalse(board.zoomStatusLabel().contains("x:"))
    }
    @Test fun canvasDisplayFiltersOnlyReducedPreviewsAndPreservesSourcePixels() {
        val doc=PaintDocument().apply {newImage(32,32)}
        for(y in 0 until 32) for(x in 0 until 32) doc.bitmap.setPixel(x,y,if((x+y)%2==0) Color.RED else Color.BLUE)
        val board=PaintCanvas(RuntimeEnvironment.getApplication(),doc)
        board.layout(0,0,800,600)
        val original=IntArray(32*32).also {doc.bitmap.getPixels(it,0,32,0,0,32,32)}
        for(zoom in listOf(.6f,1f,1.75f)) {
            board.zoomAt(zoom)
            val image=Bitmap.createBitmap(board.width,board.height,Bitmap.Config.ARGB_8888)
            try {
                board.draw(Canvas(image))
                val start=board.toScreen(4f,4f);val end=board.toScreen(28f,28f)
                var sampled=0;var blended=0
                for(y in start.y.toInt()+1 until end.y.toInt()-1) for(x in start.x.toInt()+1 until end.x.toInt()-1) {
                    val colour=image.getPixel(x,y)
                    if(zoom>=1f) assertTrue("$zoom: magnified pixels stay crisp at $x,$y",colour==Color.RED || colour==Color.BLUE)
                    else {
                        assertEquals(255,Color.alpha(colour));assertEquals(0,Color.green(colour))
                        if(Color.red(colour)>0 && Color.blue(colour)>0) blended++
                    }
                    sampled++
                }
                assertTrue(sampled>20)
                if(zoom<1f) assertTrue("Reduced previews must average neighbouring pixels",blended>20)
                val unchanged=IntArray(original.size).also {doc.bitmap.getPixels(it,0,32,0,0,32,32)}
                assertArrayEquals(original,unchanged)
            } finally {image.recycle()}
        }
    }
    @Test fun scrollbarEndpointsAndDraggingAreInverseForLargeAndExpandedCanvases() {
        for(axis in listOf(ViewportAxis(800f,0f,4000f,48f),ViewportAxis(360f,-120f,960f,24f),ViewportAxis(400f,0f,120f,24f))) {
            val thumb=axis.thumbSize(40f)
            for(fraction in listOf(0f,.1f,.5f,.9f,1f)) {
                val pan=axis.minimum+fraction*axis.range
                assertEquals(pan,axis.panForThumb(axis.thumbStart(pan,thumb),thumb),.001f)
            }
            assertEquals(axis.maximum,axis.panForThumb(-1000f,thumb),0f)
            assertEquals(axis.minimum,axis.panForThumb(10000f,thumb),0f)
        }
    }
    @Test fun resizedViewportKeepsImageCentreAndRestoredDraftUsesNewWindowSize() {
        val doc=PaintDocument().apply {newImage(1600,1200)}
        val board=PaintCanvas(RuntimeEnvironment.getApplication(),doc)
        board.layout(0,0,800,600);board.zoomAt(2f)
        val before=board.toImage((board.width-20*board.resources.displayMetrics.density)/2,(board.height-20*board.resources.displayMetrics.density)/2)
        board.layout(0,0,500,900)
        val after=board.toImage((board.width-20*board.resources.displayMetrics.density)/2,(board.height-20*board.resources.displayMetrics.density)/2)
        assertEquals(before.x,after.x,.001f);assertEquals(before.y,after.y,.001f)
        val restored=PaintCanvas(RuntimeEnvironment.getApplication(),doc)
        restored.restoreDraft(board.draftState());restored.layout(0,0,1100,450)
        val point=restored.toImage((restored.width-20*restored.resources.displayMetrics.density)/2,(restored.height-20*restored.resources.displayMetrics.density)/2)
        assertEquals(after.x,point.x,.001f);assertEquals(after.y,point.y,.001f)
    }
    @Test fun oldDraftWithOffscreenPanRefitsAndCursorModeStillAllowsScrollbarMovement() {
        val doc=PaintDocument().apply {newImage(1200,900)}
        val board=PaintCanvas(RuntimeEnvironment.getApplication(),doc)
        board.restoreDraft(JSONObject().put("zoom",2.0).put("pan_x",-90000).put("pan_y",90000));board.layout(0,0,800,600)
        val centre=board.toScreen(600f,450f)
        assertTrue(centre.x in 0f..800f);assertTrue(centre.y in 0f..600f)
        board.selectTool(PaintTool.BRUSH);board.setCursorMode(true);board.zoomAt(3f)
        val old=board.panX
        for((action,x) in listOf(MotionEvent.ACTION_DOWN to 10f,MotionEvent.ACTION_MOVE to 750f,MotionEvent.ACTION_UP to 750f)) {
            val event=MotionEvent.obtain(0,20,action,x,board.height-2f,0);board.dispatchTouchEvent(event);event.recycle()
        }
        assertTrue(board.panX<old);assertFalse(doc.canUndo);assertFalse(board.cursorDrawing)
    }
    @Test fun unicodeClustersPreserveCombiningCharactersAndEmojiSequences() {
        assertEquals(listOf("Á","👩🏽‍🎨","🇲🇳","𠀀"),VerticalText.clusters("Á👩🏽‍🎨🇲🇳𠀀"))
    }
    @Test fun verticalLatinModesAndColumnOrdersProduceDistinctEditablePixels() {
        val paint=Paint(Paint.ANTI_ALIAS_FLAG).apply {textSize=32f;color=Color.BLACK;typeface=Typeface.DEFAULT}
        val upright=VerticalText.bounds("ABC",paint,TextDirection.VERTICAL_LR,GlyphOrientation.UPRIGHT,1f)
        val sideways=VerticalText.bounds("ABC",paint,TextDirection.VERTICAL_LR,GlyphOrientation.SIDEWAYS,1f)
        assertTrue(upright.height()>sideways.height())
        fun render(direction: TextDirection): Bitmap {
            val image=Bitmap.createBitmap(180,240,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.WHITE)}
            VerticalText.draw(Canvas(image),"A\nBC",paint,direction,GlyphOrientation.UPRIGHT)
            return image
        }
        val lr=render(TextDirection.VERTICAL_LR);val rl=render(TextDirection.VERTICAL_RL)
        assertFalse(lr.sameAs(rl))
        val doc=PaintDocument().apply {newImage(240,240)}
        doc.text(100f,20f,"ABC\nDE",32f,Typeface.DEFAULT,false,direction=TextDirection.VERTICAL_RL,glyphOrientation=GlyphOrientation.UPRIGHT)
        assertTrue(doc.canUndo)
        val pixels=IntArray(240*240);doc.bitmap.getPixels(pixels,0,240,0,0,240,240)
        assertTrue(pixels.count {it!=Color.WHITE}>50);doc.undo();assertEquals(Color.WHITE,doc.bitmap.getPixel(100,20))
        lr.recycle();rl.recycle()
    }
    @Test fun verticalLocaleDefaultsAndSettingsSurviveSerialization() {
        val old=Locale.getDefault()
        try {
            Locale.setDefault(Locale.forLanguageTag("lzh-Hant"));assertEquals(TextDirection.VERTICAL_RL,TextSettings().direction)
            for(tag in listOf("mn-Mong","mnc-Mong")) {
                Locale.setDefault(Locale.forLanguageTag(tag))
                assertEquals(tag,TextDirection.VERTICAL_LR,VerticalText.uiDirection())
                assertEquals(tag,TextDirection.VERTICAL_LR,TextSettings().direction)
                val font=VerticalText.uiTypeface(RuntimeEnvironment.getApplication());assertNotNull(tag,font)
                val paint=Paint().apply {typeface=font;textSize=40f}
                assertTrue(tag,paint.hasGlyph(if(tag=="mnc-Mong") "ᡠ" else "ᠮ"))
            }
            Locale.setDefault(Locale.forLanguageTag("mn-Cyrl-MN"))
            assertEquals(TextDirection.HORIZONTAL,VerticalText.uiDirection())
            assertNull(VerticalText.uiTypeface(RuntimeEnvironment.getApplication()))
            val settings=TextSettings("ᠮᠣᠩᠭᠣᠯ",direction=TextDirection.VERTICAL_LR,glyphOrientation=GlyphOrientation.SIDEWAYS)
            assertEquals(settings,TextSettings.read(settings.json()))
            assertEquals(TextDirection.HORIZONTAL,TextSettings.read(JSONObject().put("text","Old draft")).direction)
        } finally {Locale.setDefault(old)}
    }
}
