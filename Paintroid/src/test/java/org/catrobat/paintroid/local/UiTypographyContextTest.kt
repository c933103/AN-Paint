/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.content.res.Configuration
import android.graphics.Paint
import android.graphics.Typeface
import android.os.Build
import android.text.Spanned
import android.text.TextPaint
import android.text.style.MetricAffectingSpan
import android.widget.ArrayAdapter
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.Spinner
import android.widget.TextView
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.util.Locale

/** API21/24 establish binding with legacy fonts, not real glyph geometry.
 * API30/35 additionally exercise native glyph coverage; direction has its own
 * unchanged native geometry and lifecycle tests.
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[21,24,30,35],qualifiers="en-rUS")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class UiTypographyContextTest {
    private data class Profile(val tag: String,val asset: String,val sample: String)
    private val base get()=RuntimeEnvironment.getApplication() as Context
    private fun profiles(): List<Profile> = listOf(
        Profile("vi-Hani","fonts/anpaintnomui.ttf","𡨸喃 𮞶"),
        Profile("wuu-Hans","fonts/anpaintwuufallback.ttf","𠲎")
    )+AppLanguage.tags(base).filter {Locale.forLanguageTag(it).script=="Mong"}
        .map {Profile(it,"fonts/notosansmongolian.ttf","ᠮᠣᠩᠭᠣᠯ ᡤ")}
    private fun localized(tag: String)=base.createConfigurationContext(
        Configuration(base.resources.configuration).apply {setLocale(Locale.forLanguageTag(tag))})
    @Suppress("DEPRECATION")
    private fun resourceLocale(context: Context)=if(Build.VERSION.SDK_INT>=24)
        context.resources.configuration.locales[0] else context.resources.configuration.locale
    private fun withDefault(tag: String,check: ()->Unit) {
        val before=Locale.getDefault()
        try {Locale.setDefault(Locale.forLanguageTag(tag));check()}
        finally {Locale.setDefault(before)}
    }
    private fun requiredFace(profile: Profile,context: Context)=Typeface.createFromAsset(context.assets,profile.asset)
    private fun checkFace(profile: Profile,view: TextView) {
        assertEquals("Bundled asset for ${profile.tag}",requiredFace(profile,view.context),view.typeface)
        assertEquals(profile.sample,view.text.toString())
        // These binding-only views are detached; API21 needs an attached window for
        // a real accessibility node. Attached notification/dialog tests cover that path.
        if(Build.VERSION.SDK_INT>=26) {
            val paint=Paint(view.paint)
            profile.sample.codePoints().filter {it!=32}.forEach {point ->
                assertTrue("${profile.tag} U+${point.toString(16)}",paint.hasGlyph(String(Character.toChars(point))))
            }
        }
    }

    @Test fun freshControlsUseEveryApplicableResourceFontAfterDefaultReset() {
        val required=profiles()
        assertTrue(required.any {it.tag=="mn-Mong"})
        assertTrue(required.any {it.tag=="mnc-Mong"})
        for(profile in required) {
            val context=localized(profile.tag)
            withDefault("en-US") {
                assertEquals(profile.tag,resourceLocale(context).toLanguageTag())
                assertNotEquals(resourceLocale(context),Locale.getDefault())
                val expected=requiredFace(profile,context)
                assertEquals(expected,LocaleTypography.typeface(context))
                assertEquals(expected,VerticalText.uiTypeface(context))
                val button=FlowButton(context).apply {this.text=profile.sample}
                val label=FlowTextView(context).apply {this.text=profile.sample}
                listOf(button,label).forEach {checkFace(profile,it)}
                if(Locale.forLanguageTag(profile.tag).script=="Mong") {
                    val caption=TextView(context).apply {this.text=profile.sample}
                    VerticalUi.caption(caption)
                    checkFace(profile,caption)
                }
            }
        }
    }

    @Test fun installerCoversNewChildrenAndSpinnerWithoutReplacingExplicitDrawingFaces() {
        for(profile in profiles()) {
            val context=localized(profile.tag)
            withDefault("en-US") {
                val expected=requiredFace(profile,context)
                val root=LinearLayout(context)
                val label=TextView(context).apply {this.text=profile.sample}
                val field=EditText(context).apply {setText(profile.sample)}
                val bold=TextView(context).apply {typeface=Typeface.DEFAULT_BOLD}
                val explicit=EditText(context).apply {tag="text_content";typeface=Typeface.MONOSPACE}
                val preview=TextView(context).apply {tag="font_option_monospace";typeface=Typeface.MONOSPACE}
                listOf(label,field,bold,explicit,preview).forEach {root.addView(it)}
                LocaleTypography.install(root)
                checkFace(profile,label);checkFace(profile,field)
                assertEquals(Typeface.create(expected,Typeface.BOLD),bold.typeface)
                assertSame(Typeface.MONOSPACE,explicit.typeface);assertSame(Typeface.MONOSPACE,preview.typeface)
                val added=TextView(context).apply {this.text=profile.sample};root.addView(added)
                val spinner=Spinner(context).apply {
                    adapter=ArrayAdapter(context,android.R.layout.simple_spinner_dropdown_item,listOf("first",profile.sample))
                    setSelection(1)
                }
                root.addView(spinner);root.viewTreeObserver.dispatchOnGlobalLayout()
                checkFace(profile,added)
                assertEquals(1,spinner.selectedItemPosition)
                val row=spinner.adapter.getDropDownView(1,null,root) as TextView
                assertEquals(expected,row.typeface);assertEquals(profile.sample,row.text.toString())
                assertSame(Typeface.MONOSPACE,explicit.typeface);assertSame(Typeface.MONOSPACE,preview.typeface)
            }
        }
    }

    @Test fun englishResourcesDoNotInheritAnUnrelatedProcessBundledFace() {
        val context=localized("en-US")
        val normal=withEnglishDefaults(context)
        for(processTag in listOf("vi-Hani","wuu-Hans","mn-Mong")) withDefault(processTag) {
            assertEquals("en-US",resourceLocale(context).toLanguageTag())
            assertNotEquals(resourceLocale(context),Locale.getDefault())
            assertNull(LocaleTypography.typeface(context));assertNull(VerticalText.uiTypeface(context))
            assertEquals(normal.first,FlowButton(context).typeface)
            assertEquals(normal.second,FlowTextView(context).typeface)
            val root=LinearLayout(context)
            val label=TextView(context).apply {this.text="English label";typeface=Typeface.SERIF}
            root.addView(label);LocaleTypography.install(root);root.viewTreeObserver.dispatchOnGlobalLayout()
            assertSame(Typeface.SERIF,label.typeface)
            assertEquals("English label",label.text.toString())
        }
    }
    private fun withEnglishDefaults(context: Context): Pair<Typeface?,Typeface?> {
        var result: Pair<Typeface?,Typeface?>?=null
        withDefault("en-US") {result=FlowButton(context).typeface to FlowTextView(context).typeface}
        return result!!
    }

    @Test fun explicitLocaleAndPickerOverridesRemainIndependentOfContextAndProcess() {
        val context=localized("en-US")
        withDefault("lzh-Hant") {
            for(profile in profiles()) {
                val locale=Locale.forLanguageTag(profile.tag)
                val expected=requiredFace(profile,context)
                assertEquals(expected,LocaleTypography.typeface(context,locale))
                assertEquals(expected,VerticalText.uiTypeface(context,locale))
                if(locale.script!="Mong") {
                    val row=TextView(context).apply {this.text=profile.sample;contentDescription=profile.sample}
                    VerticalUi.languageChoice(row,locale)
                    checkFace(profile,row)
                    assertEquals(profile.sample,row.contentDescription.toString())
                }
            }
            assertNull(LocaleTypography.typeface(localized("vi-Hani"),Locale.US))
        }
    }

    @Test fun tooltipFontAndVerticalExclusionUseTheSameResourceLocale() {
        for(profile in profiles()) {
            val context=localized(profile.tag)
            val vertical=Locale.forLanguageTag(profile.tag).script=="Mong"
            withDefault(if(vertical) "vi-Hani" else "mn-Mong") {
                val formatted=LocaleTooltip.format(context,profile.sample)!!
                val spans=(formatted as? Spanned)?.getSpans(0,formatted.length,MetricAffectingSpan::class.java).orEmpty()
                assertEquals(profile.sample,formatted.toString())
                if(vertical) assertTrue(spans.isEmpty())
                else {
                    val paint=TextPaint();spans.single().updateMeasureState(paint)
                    assertEquals(requiredFace(profile,context),paint.typeface)
                }
            }
        }
    }
}
