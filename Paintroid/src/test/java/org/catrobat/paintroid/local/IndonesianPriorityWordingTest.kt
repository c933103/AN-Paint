/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

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
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File
import java.io.IOException
import java.util.Locale

/** Complete Indonesian strings exercised through real composition and encoding consumers. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], shadows = [CommonsPngFailureShadow::class])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class IndonesianPriorityWordingTest {
    private lateinit var beforeResources: Resources
    private lateinit var beforeLocale: Locale
    private lateinit var indonesian: Context

    @Before fun useIndonesian() {
        beforeResources = PaintApplication.currentResources
        beforeLocale = Locale.getDefault()
        val app = RuntimeEnvironment.getApplication() as Context
        indonesian = app.createConfigurationContext(Configuration(app.resources.configuration).apply {
            setLocale(Locale.forLanguageTag("id"))
        })
        PaintApplication.currentResources = indonesian.resources
        Locale.setDefault(Locale.US)
        CommonsPngFailureShadow.resetFailure()
    }

    @After fun restoreResources() {
        CommonsPngFailureShadow.resetFailure()
        PaintApplication.currentResources = beforeResources
        Locale.setDefault(beforeLocale)
    }

    @Test fun liveDimensionDescriptionsUseLowercaseUnitsAcrossRepeatedSwitches() {
        val controls = DimensionControls(indonesian, ImageDimensions(24, 16), locked = false)
        val pixels = controls.findViewWithTag<RadioButton>("size_pixels")
        val percent = controls.findViewWithTag<RadioButton>("size_percent")
        assertEquals("Piksel", pixels.text.toString())
        repeat(2) {
            assertEquals("Lebar dalam piksel", controls.widthInput.contentDescription.toString())
            assertEquals("Tinggi dalam piksel", controls.heightInput.contentDescription.toString())
            percent.performClick()
            assertEquals("Lebar dalam persen", controls.widthInput.contentDescription.toString())
            assertEquals("Tinggi dalam persen", controls.heightInput.contentDescription.toString())
            pixels.performClick()
        }
        assertEquals(ImageDimensions(24, 16), controls.dimensions)
    }

    @Test fun failedPngAndDerivedEncodersReportIncompleteEncodingAndKeepSourcePixels() {
        val directory = File(indonesian.cacheDir, "indonesian-encoder-${System.nanoTime()}").apply { mkdirs() }
        val source = Bitmap.createBitmap(2, 2, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.MAGENTA) }
        try {
            for (format in listOf(ImageFormat.PNG, ImageFormat.BASE64, ImageFormat.ICO)) {
                val file = File(directory, "output.${format.extension}").apply { writeText("previous") }
                CommonsPngFailureShadow.reject = true
                val error = assertThrows(IOException::class.java) {
                    ImageExporter.encode(source, file, ExportOptions(format), 64L * 1024 * 1024)
                }
                assertEquals("Enkoder tidak menyelesaikan pengodean.", error.message)
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
