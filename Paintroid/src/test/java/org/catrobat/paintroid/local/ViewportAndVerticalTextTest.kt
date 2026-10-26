/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.res.Configuration
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
    @Test fun nonbreakingSpacesStayInsideWordsAcrossVerticalWraps() {
        val paint=Paint().apply {textSize=32f}
        for(space in listOf('\u202f','\u00a0','\u2007')) {
            assertTrue("The old isBlank branch incorrectly consumes this boundary",space.isWhitespace())
            val word="A${space}B"
            for(direction in listOf(TextDirection.VERTICAL_LR,TextDirection.VERTICAL_RL)) {
                assertEquals(word,VerticalText.wrapLabel(word,paint,10000f,direction))
                assertEquals("C\n$word\nD",VerticalText.wrapLabel("C $word D",paint,1f,direction))
                for(joined in listOf("漢${space}字","✅${space}A","A${space}✅","${space}漢","漢${space}")) {
                    assertEquals(joined,VerticalText.wrapLabel(joined,paint,1f,direction))
                    assertEquals("C\n$joined\nD",VerticalText.wrapLabel("C $joined D",paint,1f,direction))
                }
                assertEquals("漢${space}字\nA",VerticalText.wrapLabel("漢${space}字A",paint,1f,direction))
                assertEquals("A${space}✅\n字",VerticalText.wrapLabel("A${space}✅字",paint,1f,direction))
            }
        }
        assertEquals("A\nB",VerticalText.wrapLabel("A B",paint,1f,TextDirection.VERTICAL_LR))
        assertEquals("漢\n字",VerticalText.wrapLabel("漢字",paint,paint.fontSpacing,TextDirection.VERTICAL_RL))
        assertEquals("A B C",VerticalText.wrapLabel("A B C",paint,1f,TextDirection.HORIZONTAL))
    }
    @Test fun completeMongolianPositionValuesKeepEverySuffixWhenWrapped() {
        val base=RuntimeEnvironment.getApplication() as android.content.Context
        val locale=Locale.forLanguageTag("mn-Mong")
        val context=base.createConfigurationContext(Configuration(base.resources.configuration).apply {setLocale(locale)})
        val paint=Paint().apply {typeface=VerticalText.uiTypeface(context);textSize=32f}
        val keys=listOf(org.catrobat.paintroid.R.string.ui_assembly_exact_position,
            org.catrobat.paintroid.R.string.ui_assembly_target_x,org.catrobat.paintroid.R.string.ui_assembly_target_y,
            org.catrobat.paintroid.R.string.ui_assembly_position_help,org.catrobat.paintroid.R.string.ui_assembly_position_nonnegative,
            org.catrobat.paintroid.R.string.ui_assembly_unknown_image)
        for(key in keys) {
            val value=context.getString(key)
            assertTrue(value.any {it in '\u1820'..'\u1842'})
            assertEquals(value,VerticalText.wrapLabel(value,paint,100000f,TextDirection.VERTICAL_LR))
            val wrapped=VerticalText.wrapLabel(value,paint,1f,TextDirection.VERTICAL_LR)
            // Ordinary spaces may become column boundaries; NNBSP is part of
            // the same shaped word, even if that word exceeds the target height.
            assertEquals(value.split(' '),wrapped.split('\n'))
            assertEquals(value.count {it=='\u202f'},wrapped.count {it=='\u202f'})
        }
    }
    @Test fun replacingMongolianSuffixBoundaryChangesNativeInk() {
        val base=RuntimeEnvironment.getApplication() as android.content.Context
        val context=base.createConfigurationContext(Configuration(base.resources.configuration).apply {setLocale(Locale.forLanguageTag("mn-Mong"))})
        val paint=Paint(Paint.ANTI_ALIAS_FLAG).apply {typeface=VerticalText.uiTypeface(context);textSize=36f;color=Color.BLACK}
        val value="ᠵᠢᠷᠤᠭ ᠤᠨ ᠪᠠᠶᠢᠷᠢᠯᠠᠯ ᠢᠶᠠᠨ"
        fun render(text: String)=Bitmap.createBitmap(100,1200,Bitmap.Config.ARGB_8888).apply {
            eraseColor(Color.WHITE);VerticalText.draw(Canvas(this),text,paint,TextDirection.VERTICAL_LR,GlyphOrientation.MIXED)
        }
        val exact=render(value)
        val wrapped=render(VerticalText.wrapLabel(value,paint,100000f,TextDirection.VERTICAL_LR))
        val replaced=render(value.replace('\u202f',' '))
        try {
            assertTrue("Wrapping without a column break must preserve exact shaped ink",exact.sameAs(wrapped))
            assertFalse("ASCII substitution must be a meaningful native negative control",exact.sameAs(replaced))
        } finally {exact.recycle();wrapped.recycle();replaced.recycle()}
    }
    @Test fun verticalCaptionDisablesEllipsisWithoutRemovingMongolianSuffixes() {
        val base=RuntimeEnvironment.getApplication() as android.content.Context
        val context=base.createConfigurationContext(Configuration(base.resources.configuration).apply {setLocale(Locale.forLanguageTag("mn-Mong"))})
        val value=context.getString(org.catrobat.paintroid.R.string.ui_assembly_position_help)
        val view=android.widget.TextView(context).apply {text=value;setSingleLine(true);ellipsize=android.text.TextUtils.TruncateAt.END}
        VerticalUi.caption(view,32)
        val spec=android.view.View.MeasureSpec.makeMeasureSpec(4000,android.view.View.MeasureSpec.AT_MOST)
        view.measure(spec,spec);view.layout(0,0,view.measuredWidth,view.measuredHeight)
        assertEquals(value,view.text.toString());assertNull(view.ellipsize)
        assertEquals(Int.MAX_VALUE,view.maxLines)
        val text=view.text as android.text.Spanned
        val span=text.getSpans(0,text.length,android.text.style.ReplacementSpan::class.java).single()
        assertEquals(0,text.getSpanStart(span));assertEquals(value.length,text.getSpanEnd(span))
        for(line in 0 until view.layout.lineCount) assertEquals(0,view.layout.getEllipsisCount(line))
    }
    @Test fun mixedVerticalEmojiSymbolsSelectorsAndKeycapsStayUpright() {
        val paint=Paint().apply {textSize=32f}
        val box=VerticalText.bounds("✅⚙️1️⃣",paint,TextDirection.VERTICAL_RL,GlyphOrientation.MIXED,1f)
        assertEquals(3*paint.fontSpacing,box.height(),.01f)
        assertEquals(listOf("✅","⚙️","1️⃣"),VerticalText.clusters("✅⚙️1️⃣"))
    }
    @Test fun subdivisionFlagTagsStayTogetherWhenMeasuredAndWrappedVertically() {
        // England: BLACK FLAG, tag letters "gbeng", CANCEL TAG.
        val flag=buildString { listOf(0x1f3f4,0xe0067,0xe0062,0xe0065,0xe006e,0xe0067,0xe007f).forEach { appendCodePoint(it) } }
        val paint=Paint().apply {textSize=32f}
        assertEquals(listOf(flag,"✅"),VerticalText.clusters(flag+"✅"))
        for(direction in listOf(TextDirection.VERTICAL_RL,TextDirection.VERTICAL_LR)) {
            assertEquals(2*paint.fontSpacing,VerticalText.bounds(flag+"✅",paint,direction,GlyphOrientation.MIXED,1f).height(),.01f)
            assertEquals(flag+"\n✅",VerticalText.wrapLabel(flag+"✅",paint,paint.fontSpacing,direction))
        }
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
        fun localizedContext()=RuntimeEnvironment.getApplication().let {base ->
            base.createConfigurationContext(Configuration(base.resources.configuration).apply {setLocale(Locale.getDefault())})
        }
        try {
            Locale.setDefault(Locale.forLanguageTag("lzh-Hant"));assertEquals(TextDirection.VERTICAL_RL,TextSettings().direction)
            Locale.setDefault(Locale.forLanguageTag("mn-Mong"));assertEquals(TextDirection.VERTICAL_LR,TextSettings().direction)
            val font=VerticalText.uiTypeface(localizedContext());assertNotNull(font)
            val paint=Paint().apply {typeface=font;textSize=40f};assertTrue(paint.hasGlyph("ᠮ"))
            Locale.setDefault(Locale.forLanguageTag("mnc-Mong"));assertEquals(TextDirection.VERTICAL_LR,TextSettings().direction)
            assertSame(font,VerticalText.uiTypeface(localizedContext()))
            assertTrue(paint.hasGlyph("ᡤ"))
            assertEquals(TextDirection.VERTICAL_LR,VerticalText.uiDirection(Locale.forLanguageTag("en-XV")))
            assertEquals(TextDirection.VERTICAL_RL,VerticalText.uiDirection(Locale.forLanguageTag("qaa-Zsye-XV")))
            assertEquals(TextDirection.HORIZONTAL,VerticalText.uiDirection(Locale.forLanguageTag("en-US")))
            val settings=TextSettings("ᠮᠣᠩᠭᠣᠯ",direction=TextDirection.VERTICAL_LR,glyphOrientation=GlyphOrientation.SIDEWAYS)
            assertEquals(settings,TextSettings.read(settings.json()))
            assertEquals(TextDirection.HORIZONTAL,TextSettings.read(JSONObject().put("text","Old draft")).direction)
        } finally {Locale.setDefault(old)}
    }
}
