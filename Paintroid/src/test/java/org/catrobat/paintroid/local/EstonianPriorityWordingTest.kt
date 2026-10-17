/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.RadioButton
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import java.util.Locale

/** Bounded real-consumer checks, not native-speaker or installed-layout acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class EstonianPriorityWordingTest {
    private lateinit var beforeResources: Resources
    private lateinit var beforeLocale: Locale
    private lateinit var estonian: Context

    @Before fun useEstonian() {
        beforeResources = PaintApplication.currentResources
        beforeLocale = Locale.getDefault()
        val app = RuntimeEnvironment.getApplication() as Context
        estonian = app.createConfigurationContext(Configuration(app.resources.configuration).apply {
            setLocale(Locale.forLanguageTag("et"))
        })
        PaintApplication.currentResources = estonian.resources
        // Numeric punctuation must follow the resource locale, not the process locale.
        Locale.setDefault(Locale.US)
    }

    @After fun restoreResources() {
        PaintApplication.currentResources = beforeResources
        Locale.setDefault(beforeLocale)
    }

    @Test fun liveDimensionsComposeAllFourLabelsAcrossRepeatedUnitSwitches() {
        val controls = DimensionControls(estonian, ImageDimensions(24, 16), locked = false)
        val pixels = controls.findViewWithTag<RadioButton>("size_pixels")
        val percent = controls.findViewWithTag<RadioButton>("size_percent")
        assertEquals("Pikslid", pixels.text.toString())
        assertEquals("Protsent", percent.text.toString())
        repeat(2) {
            assertEquals("Laius pikslites", controls.widthInput.contentDescription.toString())
            assertEquals("Kõrgus pikslites", controls.heightInput.contentDescription.toString())
            assertEquals("24", controls.widthInput.text.toString())
            assertEquals("16", controls.heightInput.text.toString())
            percent.performClick()
            assertEquals("Laius protsentides", controls.widthInput.contentDescription.toString())
            assertEquals("Kõrgus protsentides", controls.heightInput.contentDescription.toString())
            assertEquals("100", controls.widthInput.text.toString())
            assertEquals("100", controls.heightInput.text.toString())
            pixels.performClick()
        }
        assertEquals(ImageDimensions(24, 16), controls.dimensions)
    }

    @Test fun livePixelSummaryIsCountNeutralForOneAndSeveralPixels() {
        val controls = DimensionControls(estonian, ImageDimensions(1, 1), locked = false)
        val result = controls.findViewWithTag<TextView>("size_result")
        for ((size, expected) in listOf(
            ImageDimensions(1, 1) to "1 × 1 px · Pikslite arv: 1 (0,00 MP)",
            ImageDimensions(1, 2) to "1 × 2 px · Pikslite arv: 2 (0,00 MP)",
            ImageDimensions(2, 2) to "2 × 2 px · Pikslite arv: 4 (0,00 MP)"
        )) {
            controls.setDimensions(size)
            assertEquals(expected, result.text.toString())
        }
        controls.setDimensions(ImageDimensions(100, 100))
        assertEquals("100 × 100 px · Pikslite arv: 10\u00a0000 (0,01 MP)", result.text.toString())
    }

    @Test fun actualPickerShowsCompleteTitleAndFallbackGuidanceWithoutChangingSelection() {
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        var dialog: AlertDialog? = null
        try {
            val selected = AppLanguage.selectedTag(activity)
            val expected = "Rakenduse keel\n\nTõlkeid hallatakse AN Painti keeleressurssides. Uus või tõlkimata tekst kuvatakse inglise keeles."
            var selectionChanged = false
            val shown = AppLanguage.showPicker(activity) { selectionChanged = true }
            dialog = shown
            fun texts(view: View): List<String> =
                (if (view is TextView) listOf(view.text.toString()) else emptyList()) +
                    (if (view is ViewGroup) (0 until view.childCount).flatMap { texts(view.getChildAt(it)) } else emptyList())
            assertEquals(expected, ui(R.string.language20_translation_note))
            assertTrue(texts(shown.window!!.decorView).contains(expected))
            shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
            shadowOf(Looper.getMainLooper()).idle()
            assertFalse(shown.isShowing)
            assertFalse(selectionChanged)
            assertEquals(selected, AppLanguage.selectedTag(activity))
        } finally {
            dialog?.dismiss()
            controller.pause().stop().destroy()
        }
    }

    @Test fun compiledExportWarningNamesTheActualSaveCommands() {
        assertEquals("Salvesta", ui(R.string.ui_save))
        assertEquals("Salvesta nimega…", ui(R.string.save20_title))
        assertEquals("Salvesta", ui(R.string.ui_save_a5d0d9))
        assertEquals("Eksport loodi. Enne jätkamist salvesta praegune pilt käsuga Salvesta või Salvesta nimega.",
            ui(R.string.ui_export_did_not_save23))
    }
}
