/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.graphics.Bitmap
import android.graphics.Color
import android.widget.RadioButton
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
import org.robolectric.annotation.GraphicsMode
import java.io.File
import java.io.IOException
import java.util.Locale

/** Complete Finnish strings exercised through real composition and encoding consumers. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], shadows = [CommonsPngFailureShadow::class])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class FinnishPriorityWordingTest {
    private lateinit var beforeResources: Resources
    private lateinit var beforeLocale: Locale
    private lateinit var finnish: Context

    @Before fun useFinnish() {
        beforeResources = PaintApplication.currentResources
        beforeLocale = Locale.getDefault()
        val app = RuntimeEnvironment.getApplication() as Context
        finnish = app.createConfigurationContext(Configuration(app.resources.configuration).apply {
            setLocale(Locale.forLanguageTag("fi"))
        })
        PaintApplication.currentResources = finnish.resources
        Locale.setDefault(Locale.US)
        CommonsPngFailureShadow.resetFailure()
    }

    @After fun restoreResources() {
        CommonsPngFailureShadow.resetFailure()
        PaintApplication.currentResources = beforeResources
        Locale.setDefault(beforeLocale)
    }

    @Test fun liveDimensionDescriptionsUseInflectedUnitsAcrossRepeatedSwitches() {
        val controls = DimensionControls(finnish, ImageDimensions(24, 16), locked = false)
        val pixels = controls.findViewWithTag<RadioButton>("size_pixels")
        val percent = controls.findViewWithTag<RadioButton>("size_percent")
        assertEquals("Pikselit", pixels.text.toString())
        assertEquals("Prosentti", percent.text.toString())
        repeat(2) {
            assertEquals("Leveys pikseleinä", controls.widthInput.contentDescription.toString())
            assertEquals("Korkeus pikseleinä", controls.heightInput.contentDescription.toString())
            percent.performClick()
            assertEquals("Leveys prosentteina", controls.widthInput.contentDescription.toString())
            assertEquals("Korkeus prosentteina", controls.heightInput.contentDescription.toString())
            pixels.performClick()
        }
        assertEquals(ImageDimensions(24, 16), controls.dimensions)
    }

    @Test fun actualDimensionSummaryHandlesSingularAndGroupedCounts() {
        val controls = DimensionControls(finnish, ImageDimensions(1, 1), locked = false)
        val result = controls.findViewWithTag<TextView>("size_result")
        assertEquals("1 × 1 px · Pikselimäärä: 1 (0,00 MP)", result.text.toString())
        controls.setDimensions(ImageDimensions(2, 1))
        assertEquals("2 × 1 px · Pikselimäärä: 2 (0,00 MP)", result.text.toString())
        controls.setDimensions(ImageDimensions(100, 100))
        assertEquals("100 × 100 px · Pikselimäärä: " + String.format(Locale.forLanguageTag("fi"), "%,d", 10000L) + " (0,01 MP)", result.text.toString())
        assertFalse(result.text.toString().contains("1 pikseliä"))
    }

    @Test fun actualLanguagePickerExplainsEnglishFallbackWithoutCompletenessClaim() {
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        var dialog: AlertDialog? = null
        try {
            val shown = AppLanguage.showPicker(activity) { }
            dialog = shown
            shadowOf(Looper.getMainLooper()).idle()
            val expected = "Sovelluksen kieli\n\nKäännöksiä ylläpidetään AN Paintin kieliresursseissa. Uusi tai kääntämätön teksti näkyy englanniksi."
            val all = textViews(shown.window!!.decorView).map { it.text.toString() }
            assertTrue(all.contains(expected))
            assertFalse(all.any { it.contains("sisältää kaikki AN Paintin") })
            assertEquals("Peruuta", shown.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
            shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
            shadowOf(Looper.getMainLooper()).idle()
            assertFalse(shown.isShowing)
        } finally {
            dialog?.dismiss()
            controller.pause().stop().destroy()
        }
    }

    private fun textViews(view: View): List<TextView> =
        (if (view is TextView) listOf(view) else emptyList()) +
            (if (view is ViewGroup) (0 until view.childCount).flatMap { textViews(view.getChildAt(it)) } else emptyList())

    @Test fun failedPngAndDerivedEncodersReportIncompleteEncodingAndKeepSourcePixels() {
        val directory = File(finnish.cacheDir, "finnish-encoder-${System.nanoTime()}").apply { mkdirs() }
        val source = Bitmap.createBitmap(2, 2, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.MAGENTA) }
        try {
            for (format in listOf(ImageFormat.PNG, ImageFormat.BASE64, ImageFormat.ICO)) {
                val file = File(directory, "output.${format.extension}").apply { writeText("previous") }
                CommonsPngFailureShadow.reject = true
                val error = assertThrows(IOException::class.java) {
                    ImageExporter.encode(source, file, ExportOptions(format), 64L * 1024 * 1024)
                }
                assertEquals("Kooderi ei suorittanut koodausta loppuun.", error.message)
                assertNotNull(CommonsPngFailureShadow.rejectedBitmap)
                assertFalse(source.isRecycled)
                assertEquals(Color.MAGENTA, source.getPixel(0, 0))
                if (format != ImageFormat.PNG) assertEquals("previous", file.readText())
                assertEquals(listOf(file.name), directory.listFiles()!!.map { it.name })
                file.delete()
                CommonsPngFailureShadow.resetFailure()
            }
            // A successful real PNG encode remains possible with the failure injection disabled.
            val png = File(directory, "success.png")
            ImageExporter.encode(source, png, ExportOptions(ImageFormat.PNG), 64L * 1024 * 1024)
            assertTrue(png.length() > 8)
            assertArrayEquals(byteArrayOf(-119, 80, 78, 71, 13, 10, 26, 10), png.readBytes().copyOf(8))
        } finally {
            source.recycle()
            directory.deleteRecursively()
        }
    }
}
