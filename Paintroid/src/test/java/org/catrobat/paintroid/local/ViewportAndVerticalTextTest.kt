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
            Locale.setDefault(Locale.forLanguageTag("mn-Mong"));assertEquals(TextDirection.VERTICAL_LR,TextSettings().direction)
            val font=VerticalText.uiTypeface(RuntimeEnvironment.getApplication());assertNotNull(font)
            val paint=Paint().apply {typeface=font;textSize=40f};assertTrue(paint.hasGlyph("ᠮ"))
            val settings=TextSettings("ᠮᠣᠩᠭᠣᠯ",direction=TextDirection.VERTICAL_LR,glyphOrientation=GlyphOrientation.SIDEWAYS)
            assertEquals(settings,TextSettings.read(settings.json()))
            assertEquals(TextDirection.HORIZONTAL,TextSettings.read(JSONObject().put("text","Old draft")).direction)
        } finally {Locale.setDefault(old)}
    }
}
