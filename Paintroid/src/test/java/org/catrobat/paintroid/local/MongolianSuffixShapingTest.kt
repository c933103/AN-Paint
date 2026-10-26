/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.text.Layout
import android.text.StaticLayout
import android.text.TextPaint
import org.catrobat.paintroid.classic.GlyphOrientation
import org.catrobat.paintroid.classic.TextDirection
import org.catrobat.paintroid.classic.VerticalText
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.util.Locale
import kotlin.math.ceil
import kotlin.math.floor

/** Native ink oracle: Noto's visible NNBSP diagnostic is a real glyph, not missing coverage. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class MongolianSuffixShapingTest {
    private fun paint()=TextPaint(Paint.ANTI_ALIAS_FLAG).apply {
        typeface=VerticalText.uiTypeface(RuntimeEnvironment.getApplication(),Locale.forLanguageTag("mn-Mong"))
        textSize=80f;color=Color.BLACK
    }
    @Suppress("DEPRECATION")
    private fun nativeLayout(text: String,paint: TextPaint)=StaticLayout(text,paint,
        ceil(Layout.getDesiredWidth(text,paint).coerceAtLeast(1f)).toInt()+2,
        Layout.Alignment.ALIGN_NORMAL,1f,0f,false)
    private fun bitmap()=Bitmap.createBitmap(240,2000,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.WHITE)}
    // Independent native layouts and rotations; deliberately does not call VerticalText's run builder.
    private fun reference(parts: List<String>,paint: TextPaint)=bitmap().apply {
        val canvas=Canvas(this);var y=0f
        for(part in parts) {
            val layout=nativeLayout(part,paint)
            canvas.save();canvas.translate((paint.fontSpacing+layout.height)/2,y)
            canvas.rotate(90f);layout.draw(canvas);canvas.restore();y+=layout.width
        }
    }
    private fun actual(text: String,paint: TextPaint,orientation: GlyphOrientation)=bitmap().apply {
        VerticalText.draw(Canvas(this),text,paint,TextDirection.VERTICAL_LR,orientation)
    }
    private fun inkAt(layout: StaticLayout,index: Int): Int {
        val bitmap=Bitmap.createBitmap(layout.width,layout.height,Bitmap.Config.ARGB_8888)
        try {
            bitmap.eraseColor(Color.WHITE);layout.draw(Canvas(bitmap))
            val start=ceil(layout.getPrimaryHorizontal(index)).toInt()+1
            val end=floor(layout.getPrimaryHorizontal(index+1)).toInt()-1
            var ink=0
            for(y in 0 until bitmap.height) for(x in start until end)
                if(x in 0 until bitmap.width && bitmap.getPixel(x,y)!=Color.WHITE) ink++
            return ink
        } finally {bitmap.recycle()}
    }
    @Test fun latinToMongolianBoundaryHasBlankSeparatorAndExactSuffixInk() {
        val paint=paint()
        for(prefix in listOf("Commons","URL","PNG","Cafe\u0301")) for(suffix in listOf("ᠤᠨ","ᡳ","ᠤ\u180bᠨ")) {
            val joined="\u202f$suffix";val text=prefix+joined
            // Native negative control reproduces the actual dotted-box N defect.
            assertTrue("Unsplit Latin/Common run must expose diagnostic ink",inkAt(nativeLayout(text,paint),prefix.length)>20)
            assertEquals("Mongolian suffix run must leave NNBSP blank",0,inkAt(nativeLayout(joined,paint),0))
            val expected=reference(listOf(prefix,joined),paint)
            val old=reference(listOf(text),paint)
            try {
                assertFalse("The pixel oracle must reject the pre-fix marker",expected.sameAs(old))
                for(orientation in listOf(GlyphOrientation.MIXED,GlyphOrientation.SIDEWAYS)) {
                    val image=actual(text,paint,orientation)
                    try {assertTrue("$prefix/$suffix/$orientation: complete shaped ink",expected.sameAs(image))}
                    finally {image.recycle()}
                }
                val substituted=actual(text.replace('\u202f',' '),paint,GlyphOrientation.MIXED)
                try {assertFalse("Ordinary space must not replace the suffix boundary",expected.sameAs(substituted))}
                finally {substituted.recycle()}
            } finally {expected.recycle();old.recycle()}
            assertEquals(text,VerticalText.wrapLabel(text,paint,1f,TextDirection.VERTICAL_LR))
        }
    }
    @Test fun mongolianRootsRetainTheirUnsplitNativeShaping() {
        val paint=paint()
        for(text in listOf("ᠵᠢᠷᠤᠭ\u202fᠤᠨ","ᠪᡳᡨᡥᡝ\u202fᡳ","ᠯᠢᠼᠧᠨ᠋ᠽ\u202fᠦᠨ","ᠨ\u180b\u202fᠤᠨ")) {
            val expected=reference(listOf(text),paint)
            val image=actual(text,paint,GlyphOrientation.MIXED)
            try {assertTrue("Do not split a Mongolian root from its suffix",expected.sameAs(image))}
            finally {expected.recycle();image.recycle()}
        }
    }
    @Test fun emptyNewlineAndMixedCjkDrawingKeepTheirNativeOrientation() {
        val paint=paint()
        val empty=actual("",paint,GlyphOrientation.SIDEWAYS);val blank=bitmap()
        try {assertTrue(blank.sameAs(empty))} finally {empty.recycle();blank.recycle()}
        val columns=bitmap();val actualColumns=actual("A\nB",paint,GlyphOrientation.MIXED)
        try {
            val canvas=Canvas(columns)
            for((index,text) in listOf("A","B").withIndex()) {
                val layout=nativeLayout(text,paint)
                canvas.save();canvas.translate(index*paint.fontSpacing+(paint.fontSpacing+layout.height)/2,0f)
                canvas.rotate(90f);layout.draw(canvas);canvas.restore()
            }
            assertTrue("Newlines remain separate columns",columns.sameAs(actualColumns))
        } finally {columns.recycle();actualColumns.recycle()}
        val mixed=bitmap();val actualMixed=actual("漢A",paint,GlyphOrientation.MIXED)
        try {
            val canvas=Canvas(mixed);val han=nativeLayout("漢",paint);val latin=nativeLayout("A",paint)
            canvas.save();canvas.translate((paint.fontSpacing-han.width)/2,(paint.fontSpacing-han.height)/2)
            han.draw(canvas);canvas.restore()
            canvas.save();canvas.translate((paint.fontSpacing+latin.height)/2,paint.fontSpacing)
            canvas.rotate(90f);latin.draw(canvas);canvas.restore()
            assertTrue("CJK stays upright beside sideways Latin",mixed.sameAs(actualMixed))
        } finally {mixed.recycle();actualMixed.recycle()}
    }
}
