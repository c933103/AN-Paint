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

}
