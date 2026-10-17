/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.content.res.Configuration
import android.graphics.Paint
import android.view.View
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.util.Locale

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class VerticalCaptionSafetyTest {
    private fun context(tag: String): Context {
        val base=RuntimeEnvironment.getApplication() as Context
        return base.createConfigurationContext(Configuration(base.resources.configuration).apply {setLocale(Locale.forLanguageTag(tag))})
    }
    private class Tile(context: Context): PanelToolButton(context) {
        fun visibleCaption()=caption()
    }
    private fun tile(context: Context,value: String): Tile = Tile(context).apply {
        text=value;contentDescription=value
        val unbounded=View.MeasureSpec.makeMeasureSpec(0,View.MeasureSpec.UNSPECIFIED)
        measure(unbounded,unbounded);layout(0,0,measuredWidth,measuredHeight)
    }
    private fun fits(tile: Tile,value: String): Boolean {
        val bounds=VerticalText.bounds(value,tile.paint,VerticalText.uiDirection(tile.context),GlyphOrientation.MIXED,1f)
        return bounds.width()<=tile.width-tile.paddingLeft-tile.paddingRight &&
            bounds.height()<=tile.height-tile.paddingTop-tile.paddingBottom
    }

    @Test fun longCombiningAndJoinedSequencesRemainCompleteSingleClusters() {
        val combining="a"+"\u0301".repeat(16383)
        val joined="a"+"\u200da".repeat(8191)
        val supplementary="👩🏽‍🎨"
        assertEquals(listOf(combining," ",joined," ",supplementary),VerticalText.clusters("$combining $joined $supplementary"))
    }

    @Test fun incrementalColumnsMatchWholeRunNativeMeasurement() {
        // Independently specified token boundaries include one complete joined
        // Mongolian suffix, adjacent sideways words, upright glyphs and emoji.
        val fixtures=listOf(
            listOf("AV"," ","office"," ","To"," ","again"),
            listOf("ᠵᠢᠷᠤᠭ\u202fᠤᠨ"," ","ᠪᠠᠶᠢᠷᠢᠯᠠᠯ\u202fᠢᠶᠠᠨ"),
            listOf("Commons\u202fᠤᠨ"," ","ᠮᠡᠳᠡᠭᠡ"),
            listOf("A"," ","\u202fᠤᠨ"," ","B"),
            listOf("漢","字","A"," ","B","✅","👩🏽‍🎨"))
        fun breakable(char: Char)=char.isWhitespace() && char !in "\u00a0\u2007\u202f"
        val paint=Paint().apply {textSize=32f;typeface=VerticalText.uiTypeface(context("mn-Mong"))}
        for(direction in listOf(TextDirection.VERTICAL_LR,TextDirection.VERTICAL_RL)) {
            for(height in listOf(1f,paint.fontSpacing*2,160f,100000f)) for(tokens in fixtures) {
                val expected=mutableListOf<String>();var column=""
                for(token in tokens) {
                    val proposed=column+token
                    val measured=VerticalText.bounds(proposed,paint,direction,GlyphOrientation.MIXED,1f).height()
                    if(column.any {!breakable(it)} && measured>height) {
                        expected.add(column.trim(::breakable));column=token.trimStart(::breakable)
                    }
                    else column=proposed
                }
                expected.add(column.trim(::breakable))
                assertEquals(expected.joinToString("\n"),VerticalText.wrapLabel(tokens.joinToString(""),paint,height,direction))
            }
        }
    }

    @Test fun ordinaryCaptionsKeepExhaustiveFittingAndTheirCompleteAccessibleText() {
        for(tag in listOf("lzh-Hant","mn-Mong","en-XV")) {
            for(value in listOf("Drawing","天地玄黃宇宙洪荒","Á 👩🏽‍🎨 🇲🇳","ᠵᠢᠷᠤᠭ\u202fᠤᠨ ᠪᠠᠶᠢᠷᠢᠯᠠᠯ")) {
                val button=tile(context(tag),value)
                val direction=VerticalText.uiDirection(button.context)
                val available=(button.height-button.paddingTop-button.paddingBottom).toFloat()
                val full=VerticalText.wrapLabel(value,button.paint,(button.columnHeightDp*button.resources.displayMetrics.density+.5f).toInt().toFloat(),direction)
                val clusters=VerticalText.clusters(value)
                val expected=if(fits(button,full)) full else (clusters.size-1 downTo 0).map {count ->
                    VerticalText.wrapLabel(clusters.take(count).joinToString("").trimEnd()+"…",button.paint,available,direction)
                }.firstOrNull {fits(button,it)} ?: ""
                assertEquals("$tag/$value",expected,button.visibleCaption())
                assertEquals(value,button.text.toString());assertEquals(value,button.contentDescription.toString())
            }
        }
    }

    @Test fun longCaptionFitsAndCachedResultChangesWithTextAndPaint() {
        val context=context("lzh-Hant")
        val full="天地".repeat(2048)
        val button=tile(context,full)
        val caption=button.visibleCaption()
        assertTrue(caption.endsWith("…"));assertTrue(fits(button,caption))
        assertSame("An unchanged draw reuses fitted text",caption,button.visibleCaption())
        assertEquals(full,button.text.toString());assertEquals(full,button.contentDescription.toString())
        button.paint.textSize*=1.8f
        val fresh=tile(context,full).apply {paint.textSize=button.paint.textSize}
        assertEquals("Font changes invalidate cached fitting",fresh.visibleCaption(),button.visibleCaption())
        button.text="漢"
        assertEquals(tile(context,"漢").apply {paint.textSize=button.paint.textSize}.visibleCaption(),button.visibleCaption())
        button.paint.textSize=button.height*4f
        assertEquals("Even the ellipsis cannot fit at this size","",button.visibleCaption())
    }
}
