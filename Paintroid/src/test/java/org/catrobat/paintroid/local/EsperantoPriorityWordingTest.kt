/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.os.Looper
import android.widget.EditText
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
import java.io.File
import java.util.Locale

/** Bounded consumer checks, not native-speaker or installed-layout certification. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class EsperantoPriorityWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var esperanto: Context

    @Before fun useEsperantoResources() {
        previousResources = PaintApplication.currentResources
        previousLocale = Locale.getDefault()
        val application = RuntimeEnvironment.getApplication() as Context
        val configuration = Configuration(application.resources.configuration).apply {
            setLocale(Locale.forLanguageTag("eo"))
        }
        esperanto = application.createConfigurationContext(configuration)
        PaintApplication.currentResources = esperanto.resources
        // Resource locale must govern display even when process locale differs.
        Locale.setDefault(Locale.US)
    }

    @After fun restoreResources() {
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
    }

    @Test fun dimensionsUseCountNeutralLabelForOneAndMultiplePixels() {
        val controls = DimensionControls(esperanto, ImageDimensions(1, 1), locked = false)
        val result = controls.findViewWithTag<TextView>("size_result")
        assertEquals("1 × 1 px · Nombro de bilderoj: 1 (0,00 MP)", result.text.toString())
        controls.setDimensions(ImageDimensions(2, 1))
        assertEquals("2 × 1 px · Nombro de bilderoj: 2 (0,00 MP)", result.text.toString())
        controls.setDimensions(ImageDimensions(100, 100))
        assertTrue(result.text.toString().startsWith("100 × 100 px · Nombro de bilderoj: "))
        assertTrue(result.text.toString().endsWith(" (0,01 MP)"))
        assertFalse(result.text.toString().contains("1 bilderoj"))
    }

    @Test fun cropValidationReportsAttestedSpellingWithoutWeakeningBounds() {
        val size = ImageDimensions(24, 16)
        val cases = listOf(
            CropMargins(-1.0, 0.0, 0.0, 0.0, false) to "Stuckvantoj devas esti nul aŭ pli.",
            CropMargins(0.5, 0.0, 0.0, 0.0, false) to "Stuckvantoj devas konveni ene de ĉiu bildo; uzu tutajn bilderojn aŭ procentojn.",
            CropMargins(24.0, 0.0, 0.0, 0.0, false) to "La stuco forigus la tutan bildon."
        )
        for ((margins, expected) in cases) {
            val error = assertThrows(IllegalArgumentException::class.java) { margins.rect(size) }
            assertEquals(expected, error.message)
        }
        assertEquals(android.graphics.Rect(1, 2, 21, 12), CropMargins(1.0, 2.0, 3.0, 4.0, false).rect(size))
    }

    @Test fun cropDialogUsesCorrectedActionsAndRejectsIncompleteInput() {
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        var dialog: AlertDialog? = null
        try {
            val item = AssemblyImage("one", File(activity.cacheDir, "one.image"), "specimeno", null, ImageDimensions(24, 16))
            var applied = false
            val shown = ImageCropDialog(activity, listOf(item), { null }) { applied = true }.show()
            dialog = shown
            shadowOf(Looper.getMainLooper()).idle()
            val root = shown.window!!.decorView
            assertEquals("Stuci specimeno", shadowOf(shown).title.toString())
            assertEquals("Apliki stucon", shown.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
            assertEquals("Restarigi stucon", root.findViewWithTag<TextView>("crop_reset").text.toString())
            root.findViewWithTag<EditText>("crop_left").setText("")
            assertEquals("Enigu stuckvanton por ĉiu rando.", root.findViewWithTag<TextView>("crop_status").text.toString())
            shown.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            assertFalse(applied)
            assertTrue(shown.isShowing)
            assertEquals("Enigu ĉiujn kvar stuckvantojn.", root.findViewWithTag<TextView>("crop_status").text.toString())
            root.findViewWithTag<TextView>("crop_reset").performClick()
            shown.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            assertTrue(applied)
            assertFalse(shown.isShowing)
        } finally {
            dialog?.dismiss()
            controller.pause().stop().destroy()
        }
    }
}
