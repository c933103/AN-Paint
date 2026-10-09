/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Typeface
import android.text.Layout
import android.text.SpannableString
import android.text.Spanned
import android.text.StaticLayout
import android.text.TextPaint
import android.text.style.ForegroundColorSpan
import android.text.style.MetricAffectingSpan
import android.text.style.StyleSpan
import android.view.View
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.util.Locale

/** API26/27 catch use of the API28-only TypefaceSpan constructor. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[26,27,30,35])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class LocaleTooltipTest {
    private val context get()=RuntimeEnvironment.getApplication()
    private lateinit var previous: Locale
    @Before fun remember() {previous=Locale.getDefault()}
    @After fun restore() {Locale.setDefault(previous)}
    private fun select(tag: String) {Locale.setDefault(Locale.forLanguageTag(tag))}
    private fun spans(text: CharSequence)= (text as? Spanned)?.getSpans(0,text.length,MetricAffectingSpan::class.java).orEmpty()
    private fun paint(style: Int)=TextPaint(Paint.ANTI_ALIAS_FLAG).apply {
        typeface=Typeface.create(Typeface.SERIF,style);textSize=31f;color=Color.MAGENTA
        textScaleX=1.2f;textSkewX=-.1f;isFakeBoldText=true;letterSpacing=.04f
    }

    @Test fun bundledFacePreservesPaintStyleInBothMeasurementAndDrawing() {
        for((tag,text) in listOf("vi-Hani" to "𡨸喃", "wuu-Hans" to "𠲎")) {
            select(tag)
            val formatted=LocaleTooltip.format(context,text)!!
            assertEquals(text,formatted.toString())
            val span=spans(formatted).single()
            for(style in listOf(Typeface.NORMAL,Typeface.BOLD,Typeface.ITALIC,Typeface.BOLD_ITALIC)) {
                val measure=paint(style);val draw=paint(style)
                span.updateMeasureState(measure);span.updateDrawState(draw)
                val face=Typeface.create(LocaleTypography.typeface(context),style)
                for(actual in listOf(measure,draw)) {
                    assertSame(face,actual.typeface);assertEquals(style,actual.typeface.style)
                    assertEquals(31f,actual.textSize,0f);assertEquals(Color.MAGENTA,actual.color)
                    assertEquals(1.2f,actual.textScaleX,0f);assertEquals(-.1f,actual.textSkewX,0f)
                    assertTrue(actual.isFakeBoldText);assertEquals(.04f,actual.letterSpacing,0f)
                }
                assertEquals(measure.measureText(text),draw.measureText(text),0f)
                assertEquals(measure.fontMetricsInt.ascent,draw.fontMetricsInt.ascent)
                assertTrue(draw.hasGlyph(text.takeLast(if(tag=="wuu-Hans") 2 else 1)))
            }
        }
    }

    @Test fun nativeLayoutMeasuresAndDrawsExactlyLikeTheExplicitFace() {
        for((tag,text) in listOf("vi-Hani" to "𡨸喃 𥻂𦻳", "wuu-Hans" to "𠲎 𠲎")) {
            select(tag)
            for(style in listOf(Typeface.NORMAL,Typeface.BOLD_ITALIC)) {
                val formatted=LocaleTooltip.format(context,text)!!
                val expected=paint(style).apply {typeface=Typeface.create(LocaleTypography.typeface(context),style)}
                assertEquals(Layout.getDesiredWidth(text,expected),Layout.getDesiredWidth(formatted,paint(style)),.001f)
                fun render(value: CharSequence,p: TextPaint): Bitmap {
                    val layout=StaticLayout.Builder.obtain(value,0,value.length,p,256).setAlignment(Layout.Alignment.ALIGN_NORMAL).build()
                    return Bitmap.createBitmap(300,150,Bitmap.Config.ARGB_8888).also {layout.draw(Canvas(it))}
                }
                val actual=render(formatted,paint(style));val reference=render(text,expected)
                try {assertTrue("$tag/$style native pixels",actual.sameAs(reference))}
                finally {actual.recycle();reference.recycle()}
            }
        }
    }

    @Test fun formattingCopiesExistingSpansAndRefreshesWithoutStackingOrChangingText() {
        select("vi-Hani")
        val bold=StyleSpan(Typeface.BOLD);val colour=ForegroundColorSpan(Color.RED)
        val original=SpannableString("𡨸喃 label").apply {
            setSpan(bold,0,length,Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)
            setSpan(colour,0,2,Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)
        }
        var formatted=LocaleTooltip.format(context,original)!!
        repeat(4) {formatted=LocaleTooltip.format(context,formatted)!!}
        assertEquals(original.toString(),formatted.toString())
        assertEquals(1,spans(original).size);assertEquals(2,spans(formatted).size)
        val result=formatted as Spanned
        assertEquals(0,result.getSpanStart(bold));assertEquals(original.length,result.getSpanEnd(bold))
        assertEquals(2,result.getSpanEnd(colour));assertSame(colour,result.getSpans(0,2,ForegroundColorSpan::class.java).single())
        select("wuu-Hans")
        formatted=LocaleTooltip.format(context,formatted)!!
        val p=paint(Typeface.NORMAL);spans(formatted).forEach {it.updateMeasureState(p)}
        assertSame(Typeface.create(LocaleTypography.typeface(context),Typeface.BOLD),p.typeface)
        for(tag in listOf("en-001","ar","mn-Mong","mnc-Mong","lzh-Hant","en-XV","qaa-Zsye-XV")) {
            select(tag)
            val cleared=LocaleTooltip.format(context,formatted)!!
            assertEquals(original.toString(),cleared.toString())
            assertEquals(listOf(bold),spans(cleared).toList())
            assertSame(original,LocaleTooltip.format(context,original))
        }
        assertNull(LocaleTooltip.format(context,null));assertSame("",LocaleTooltip.format(context,""))
    }

    @Test fun allPickerLocalesKeepNativeTextAndOnlyHorizontalBundledFacesAreAdded() {
        val tags=context.resources.getStringArray(R.array.app_language_tags)
        assertEquals(140,tags.size)
        val previousResources=PaintApplication.currentResources
        try { for(tag in tags) {
            select(tag)
            val config=android.content.res.Configuration(context.resources.configuration).apply {setLocale(Locale.getDefault())}
            val localized=context.createConfigurationContext(config)
            PaintApplication.currentResources=localized.resources
            val view=View(localized).apply {contentDescription="accessible label"}
            val original=SpannableString("$tag tooltip")
            LocaleTooltip.set(view,original)
            assertEquals(original.toString(),view.tooltipText.toString())
            assertEquals("accessible label",view.contentDescription)
            val count=if(tag in setOf("vi-Hani","wuu-Hans")) 1 else 0
            assertEquals(tag,count,spans(view.tooltipText).size)
            if(count==0) assertSame(tag,original,view.tooltipText)
            val category=ToolCategoryButton(localized,ToolCategory.BRUSH,PaintTool.PENCIL,true)
            for(control in listOf(ToolButton(localized,PaintTool.PENCIL),ActionButton(localized,EditIcon.UNDO),category)) {
                assertEquals(tag,control.contentDescription.toString(),control.tooltipText.toString())
                assertEquals(tag,count,spans(control.tooltipText).size)
            }
            category.expanded=true;category.selectedTool=PaintTool.WATERCOLOR;category.refresh()
            assertEquals(category.contentDescription.toString(),category.tooltipText.toString())
            assertTrue(category.tooltipText.toString().contains(PaintTool.WATERCOLOR.label))
            assertEquals(tag,count,spans(category.tooltipText).size)
            LocaleTooltip.set(view,null);assertNull(view.tooltipText)
            LocaleTooltip.set(view,original);LocaleTooltip.set(view,"");assertNull(view.tooltipText)
        } } finally {PaintApplication.currentResources=previousResources}
    }
}
