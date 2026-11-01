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
import android.widget.CheckBox
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

/** Bounded Afrikaans wording through live consumers; no installed-layout claim. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], shadows = [CommonsPngFailureShadow::class])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class AfrikaansPriorityWordingTest {
    private lateinit var beforeResources: Resources
    private lateinit var beforeLocale: Locale
    private lateinit var afrikaans: Context

    @Before fun useAfrikaans() {
        beforeResources = PaintApplication.currentResources
        beforeLocale = Locale.getDefault()
        val app = RuntimeEnvironment.getApplication() as Context
        afrikaans = app.createConfigurationContext(Configuration(app.resources.configuration).apply {
            setLocale(Locale.forLanguageTag("af"))
        })
        PaintApplication.currentResources = afrikaans.resources
        Locale.setDefault(Locale.US)
        CommonsPngFailureShadow.resetFailure()
    }

    @After fun restoreResources() {
        CommonsPngFailureShadow.resetFailure()
        PaintApplication.currentResources = beforeResources
        Locale.setDefault(beforeLocale)
    }

    @Test fun actualDimensionSummaryHandlesSingularAndGroupedCounts() {
        val controls = DimensionControls(afrikaans, ImageDimensions(1, 1), locked = false)
        val result = controls.findViewWithTag<TextView>("size_result")
        assertEquals("1 × 1 px · Aantal piksels: 1 (0,00 MP)", result.text.toString())
        controls.setDimensions(ImageDimensions(2, 1))
        assertEquals("2 × 1 px · Aantal piksels: 2 (0,00 MP)", result.text.toString())
        controls.setDimensions(ImageDimensions(100, 100))
        assertEquals("100 × 100 px · Aantal piksels: " + String.format(Locale.forLanguageTag("af"), "%,d", 10000L) + " (0,01 MP)", result.text.toString())
        assertFalse(result.text.toString().contains("1 piksels"))
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
            val expected = afrikaans.getString(R.string.language20_translation_note)
            val all = textViews(shown.window!!.decorView).map { it.text.toString() }
            assertTrue(all.contains(expected))
            assertFalse(all.any { it.contains("bevat al AN Paint se") })
            assertEquals(afrikaans.getString(R.string.ui_cancel), shown.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
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

    @Test fun actualLosslessDialogsKeepCompleteExplanationAcrossTogglesAndCancel() {
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        var confirmed = 0
        var cancelled = 0
        try {
            for (format in listOf(ImageFormat.JPEG_XL, ImageFormat.WEBP, ImageFormat.AVIF)) {
                val dialog = SaveOptionsDialog(activity, ExportOptions(format),
                    confirm = { confirmed++ }, cancel = { cancelled++ }).show()
                try {
                    shadowOf(Looper.getMainLooper()).idle()
                    val view = dialog.window!!.decorView
                    val checkbox = view.findViewWithTag<CheckBox>("export_lossless")
                    val description = view.findViewWithTag<TextView>("export_description")
                    val quality = view.findViewWithTag<NumericSlider>("export_quality")
                    assertEquals(format.label + " sonder verlies", checkbox.text.toString())
                    assertEquals(View.VISIBLE, checkbox.visibility)
                    repeat(2) {
                        assertTrue(checkbox.isChecked)
                        assertEquals(View.GONE, quality.visibility)
                        assertEquals("Hoër kwaliteit lewer gewoonlik ’n groter lêer. Kompressie sonder verlies behou elke kleurwaarde.", description.text.toString())
                        checkbox.performClick()
                        assertFalse(checkbox.isChecked)
                        assertEquals(View.VISIBLE, quality.visibility)
                        assertEquals("Hoër kwaliteit lewer gewoonlik ’n groter lêer. Kompressie sonder verlies behou elke kleurwaarde.", description.text.toString())
                        checkbox.performClick()
                    }
                    dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
                    shadowOf(Looper.getMainLooper()).idle()
                    assertFalse(dialog.isShowing)
                    assertEquals(0, confirmed)
                } finally {
                    dialog.dismiss()
                }
            }
            assertEquals(3, cancelled)
        } finally {
            controller.pause().stop().destroy()
        }
    }

    @Test fun compiledSharingWarningPreservesCompletedSaveAndErrorArgument() {
        // Resource-format contract only; this does not exercise an Android share provider.
        val detail = "provider detail: % / ’"
        assertEquals(String.format(Locale.forLanguageTag("af"), afrikaans.getString(R.string.ui_the_image_was_saved_but_android_could_not), detail),
            afrikaans.getString(R.string.ui_the_image_was_saved_but_android_could_not, detail))
    }

    @Test fun failedPngAndDerivedEncodersReportIncompleteEncodingAndKeepSourcePixels() {
        val directory = File(afrikaans.cacheDir, "afrikaans-encoder-${System.nanoTime()}").apply { mkdirs() }
        val source = Bitmap.createBitmap(2, 2, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.MAGENTA) }
        try {
            for (format in listOf(ImageFormat.PNG, ImageFormat.BASE64, ImageFormat.ICO)) {
                val file = File(directory, "output.${format.extension}").apply { writeText("previous") }
                CommonsPngFailureShadow.reject = true
                val error = assertThrows(IOException::class.java) {
                    ImageExporter.encode(source, file, ExportOptions(format), 64L * 1024 * 1024)
                }
                assertEquals(afrikaans.getString(R.string.ui_the_encoder_did_not_finish), error.message)
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
