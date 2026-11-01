/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.graphics.Paint
import org.catrobat.paintroid.classic.LocaleTypography
import org.robolectric.annotation.GraphicsMode
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.CommonsAttribution
import org.catrobat.paintroid.classic.ImageCredit
import org.catrobat.paintroid.classic.PaintApplication
import org.json.JSONArray
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.util.Locale

/** Resource selection and immutable persisted text, on pre/post-platform app-language APIs. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CommonsImportChangeTranslationTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val source="https://upload.wikimedia.org/wikipedia/commons/a/ab/Test_map.svg"
    private val page="https://commons.wikimedia.org/wiki/File:Test_map.svg"

    private fun withLanguage(tag: String,check: ()->Unit) {
        val previousTag=AppLanguage.selectedTag(context)
        val previousLocale=Locale.getDefault()
        val previousResources=PaintApplication.currentResources
        try {
            AppLanguage.select(context,tag)
            PaintApplication.currentResources=AppLanguage.wrap(context).resources
            check()
        } finally {
            AppLanguage.select(context,previousTag)
            PaintApplication.currentResources=previousResources
            Locale.setDefault(previousLocale)
        }
    }

    @Test fun selectedLocaleSuppliesWholeMessagesWithExactTechnicalLiterals() {
        for(tag in listOf("en-US","fr","ja")) withLanguage(tag) {
            val record=CommonsAttribution.parse(CommonsTestMetadata.response(source,page),source)
            val notes=PaintApplication.currentResources.getString(R.string.commons_import_svg_changes) to
                PaintApplication.currentResources.getString(R.string.commons_import_raster_changes)
            assertTrue(record.text(true).lines().contains(notes.first))
            assertTrue(record.copy(source=source.replace(".svg",".png")).text(true).lines().contains(notes.second))
            assertFalse(record.text(false).contains("AN Paint:"))
        }
    }

    @Test fun bundledScriptNotesKeepTechnicalParametersAndGlyphs() {
        val tags=listOf("vi-Hani","mn-Mong","mnc-Mong")
        for(tag in tags) withLanguage(tag) {
            val svg=PaintApplication.currentResources.getString(R.string.commons_import_svg_changes)
            val raster=PaintApplication.currentResources.getString(R.string.commons_import_raster_changes)
            assertTrue("$tag SVG conversion",svg.contains("SVG → PNG"))
            for(literal in listOf("antiAlias=false","strokeDashArray=none","background=#FFFFFF"))
                assertTrue("$tag $literal",svg.contains(literal))
            assertTrue("$tag raster background",raster.contains("background=#FFFFFF"))
            assertFalse(raster.contains("SVG → PNG"));assertFalse(raster.contains("antiAlias=false"))
            val paint=Paint().apply {typeface=LocaleTypography.typeface(context,Locale.forLanguageTag(tag))}
            (svg+raster).codePoints().filter {point ->
                point>0x7f && Character.getType(point)!=Character.FORMAT.toInt() &&
                    Character.getType(point)!=Character.NON_SPACING_MARK.toInt()
            }.distinct().forEach {point ->
                assertTrue("$tag missing U+${point.toString(16)}",paint.hasGlyph(String(Character.toChars(point))))
            }
        }
    }

    @Test fun absentUnscopedCatalogueUsesRealEnglishFallback() {
        // Compare the selected fallback with current source resources, not a frozen caption.
        val english=PriorityWordingExpectations.resources("en-GB")
        val englishSvg=english.getString(R.string.commons_import_svg_changes)
        val englishRaster=english.getString(R.string.commons_import_raster_changes)
        for(tag in listOf("am","bn","cy")) withLanguage(tag) {
            assertEquals(englishSvg,PaintApplication.currentResources.getString(R.string.commons_import_svg_changes))
            assertEquals(englishRaster,PaintApplication.currentResources.getString(R.string.commons_import_raster_changes))
            val record=CommonsAttribution.parse(CommonsTestMetadata.response(source,page),source)
            assertTrue(record.text(true).lines().contains(englishSvg))
            assertFalse(record.text(false).contains("AN Paint:"))
        }
    }

    @Test fun storedGeneratedAndUserEditedCreditsStayByteExactAcrossLanguageChanges() {
        val record=CommonsAttribution.parse(CommonsTestMetadata.response(source,page),source)
        var generated=""
        withLanguage("fr") {generated=record.text(true)}
        val userText="My attribution Ω · かな · 𠀀\nAN Paint: an intentional user-edited note."
        val credits=listOf(ImageCredit(source,generated),ImageCredit(source+"?edited",userText))
        val serialized=ImageCredit.write(credits).toString()
        for(tag in listOf("ja","ar","am","en-US")) withLanguage(tag) {
            val restored=ImageCredit.read(JSONArray(serialized))
            assertEquals(credits,restored)
            assertArrayEquals(generated.toByteArray(Charsets.UTF_8),restored[0].text.toByteArray(Charsets.UTF_8))
            assertArrayEquals(userText.toByteArray(Charsets.UTF_8),restored[1].text.toByteArray(Charsets.UTF_8))
            assertEquals(serialized,ImageCredit.write(restored).toString())
        }
    }
}
