/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.res.Resources
import android.os.Looper
import android.view.View
import android.widget.CheckBox
import android.widget.Spinner
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
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.util.Locale

/** F01: production resources and SaveOptionsDialog, without invoking an encoder. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class TiffDescriptionDialogTest {
    private lateinit var controller: ActivityController<Activity>
    private lateinit var activity: Activity
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    private lateinit var previousResources: Resources
    private var currentDialog: AlertDialog? = null
    private val requests = mutableListOf<SaveRequest>()
    private var cancellations = 0

    @Before fun start() {
        controller = Robolectric.buildActivity(Activity::class.java)
        activity = controller.setup().get()
        previousLocale = Locale.getDefault()
        previousTag = AppLanguage.selectedTag(activity)
        previousResources = PaintApplication.currentResources
    }

    @After fun stop() {
        currentDialog?.dismiss()
        idle()
        AppLanguage.select(activity, previousTag)
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
        if (!activity.isDestroyed) controller.pause().stop().destroy()
    }

    private fun idle() = shadowOf(Looper.getMainLooper()).idle()

    private fun open(tag: String, compressed: Boolean): AlertDialog {
        assertFalse(currentDialog?.isShowing == true)
        requests.clear(); cancellations = 0
        AppLanguage.select(activity, tag)
        AppLanguage.refresh(activity)
        assertEquals(tag, AppLanguage.selectedTag(activity))
        return SaveOptionsDialog(activity, ExportOptions(ImageFormat.TIFF, tiffCompressed = compressed),
            confirm = { requests += it }, cancel = { cancellations++ }, initialFilename = "scan.tif")
            .show().also { currentDialog = it; idle() }
    }

    private fun AlertDialog.compression(): CheckBox =
        window!!.decorView.findViewWithTag("export_tiff_compressed")

    private fun AlertDialog.description(): TextView =
        window!!.decorView.findViewWithTag("export_description")

    private fun AlertDialog.format(): Spinner =
        window!!.decorView.findViewWithTag("export_format")

    private fun assertTiff(dialog: AlertDialog, expected: String, compressed: Boolean) {
        assertTrue(dialog.isShowing)
        assertEquals("TIFF", dialog.format().selectedItem.toString())
        assertEquals(View.VISIBLE, dialog.description().visibility)
        assertEquals(expected, dialog.description().text.toString())
        assertEquals(View.VISIBLE, dialog.compression().visibility)
        assertEquals(compressed, dialog.compression().isChecked)
        assertTrue(requests.isEmpty())
        assertEquals(0, cancellations)
    }

    private fun confirm(dialog: AlertDialog, compressed: Boolean) {
        assertTrue(dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick())
        idle()
        assertFalse(dialog.isShowing)
        assertEquals(1, requests.size)
        assertEquals(ExportOptions(ImageFormat.TIFF, lossless = false, tiffCompressed = compressed), requests.single().options)
        assertEquals("scan.tif", requests.single().fileName)
        assertEquals(0, cancellations)
    }

    private fun expected(tag: String) = if (tag == "pt-BR") PORTUGUESE else ENGLISH

    @Test fun sevenEnglishVariantsUseQualifiedDescriptionForBothCompressionChoices() {
        for (tag in listOf("en-001", "en-AU", "en-CA", "en-GB", "en-IN", "en-SG", "en-US")) {
            for (compressed in listOf(false, true)) {
                val dialog = open(tag, compressed)
                assertTiff(dialog, ENGLISH, compressed)
                assertEquals("Lossless compression (Deflate)", dialog.compression().text.toString())
                confirm(dialog, compressed)
            }
        }
    }

    @Test fun brazilianPortugueseUsesQualifiedDescriptionForBothCompressionChoices() {
        for (compressed in listOf(false, true)) {
            val dialog = open("pt-BR", compressed)
            assertTiff(dialog, PORTUGUESE, compressed)
            assertEquals("Compressão sem perdas (Deflate)", dialog.compression().text.toString())
            confirm(dialog, compressed)
        }
    }

    @Test fun welshMissingDescriptionFallsBackToQualifiedEnglishForBothChoices() {
        for (compressed in listOf(false, true)) {
            val dialog = open("cy", compressed)
            assertTiff(dialog, ENGLISH, compressed)
            confirm(dialog, compressed)
        }
    }

    @Test fun verticalEnglishAndEmojiFixturesKeepTheQualifiedDescription() {
        for ((tag, text) in listOf("en-XV" to ENGLISH, "qaa-Zsye-XV" to "💾 $ENGLISH")) {
            for (compressed in listOf(false, true)) {
                val dialog = open(tag, compressed)
                assertNotNull(dialog.window!!.decorView.findViewWithTag<View>("vertical_save_form"))
                assertTiff(dialog, text, compressed)
                confirm(dialog, compressed)
            }
        }
    }

    @Test fun togglingCompressionKeepsTheDescriptionAndSubmitsTheChosenFlag() {
        for (tag in listOf("en-US", "pt-BR", "cy")) for (initial in listOf(false, true)) {
            val dialog = open(tag, initial)
            assertTiff(dialog, expected(tag), initial)
            dialog.compression().performClick(); idle()
            assertTiff(dialog, expected(tag), !initial)
            confirm(dialog, !initial)
        }
    }

    @Test fun switchingFormatsRestoresDescriptionAndRetainsCompressionChoice() {
        for (tag in listOf("en-GB", "pt-BR", "cy")) for (compressed in listOf(false, true)) {
            val dialog = open(tag, compressed)
            EditorTestNavigation.format(dialog.format(), ImageFormat.DIB)
            assertEquals(View.GONE, dialog.compression().visibility)
            assertEquals(ui(R.string.formats22_dib_description), dialog.description().text.toString())
            assertNotEquals(expected(tag), dialog.description().text.toString())
            EditorTestNavigation.format(dialog.format(), ImageFormat.TIFF)
            assertTiff(dialog, expected(tag), compressed)
            confirm(dialog, compressed)
        }
    }

    @Test fun buttonAndCancelEventNeverConfirmAnExportForEitherCompressionChoice() {
        for (tag in listOf("en-US", "pt-BR", "cy")) for (compressed in listOf(false, true)) {
            for (cancelEvent in listOf(false, true)) {
                val dialog = open(tag, compressed)
                assertTiff(dialog, expected(tag), compressed)
                if (cancelEvent) dialog.cancel()
                else assertTrue(dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick())
                idle()
                assertFalse(dialog.isShowing)
                assertTrue(requests.isEmpty())
                assertEquals(1, cancellations)
            }
        }
    }

    @Test fun cyrillicMongolianC023KeepsQualifiedDescriptionWhenTogglingAndConfirming() {
        for (initial in listOf(false, true)) {
            val dialog = open("mn-Cyrl-MN", initial)
            assertTiff(dialog, MONGOLIAN_C023, initial)
            assertEquals(MONGOLIAN_C023, ui(R.string.formats22_tiff_description))
            assertEquals("Алдагдалгүй шахалт (Deflate)", dialog.compression().text.toString())
            dialog.compression().performClick(); idle()
            assertTiff(dialog, MONGOLIAN_C023, !initial)
            confirm(dialog, !initial)
        }
    }

    @Test fun cyrillicMongolianC023RestoresDescriptionAfterFormatSwitchAndBothCancelRoutes() {
        for (compressed in listOf(false, true)) for (cancelEvent in listOf(false, true)) {
            val dialog = open("mn-Cyrl-MN", compressed)
            assertTiff(dialog, MONGOLIAN_C023, compressed)
            EditorTestNavigation.format(dialog.format(), ImageFormat.DIB)
            assertEquals(View.GONE, dialog.compression().visibility)
            assertEquals(ui(R.string.formats22_dib_description), dialog.description().text.toString())
            assertNotEquals(MONGOLIAN_C023, dialog.description().text.toString())
            EditorTestNavigation.format(dialog.format(), ImageFormat.TIFF)
            assertTiff(dialog, MONGOLIAN_C023, compressed)
            if (cancelEvent) dialog.cancel()
            else assertTrue(dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick())
            idle()
            assertFalse(dialog.isShowing)
            assertTrue(requests.isEmpty())
            assertEquals(1, cancellations)
        }
    }

    companion object {
        private const val MONGOLIAN_C023 = "Нэг RGB хуудсыг хадгална. Шахалт нь пикселийг өөрчлөхгүйгээр файлын хэмжээг багасгаж магадгүй; шахалтгүй TIFF хадгалахын тулд унтраана."
        private const val ENGLISH = "Saves one RGB page. Compression may reduce file size without changing " +
            "pixels; turn it off for uncompressed TIFF."
        private const val PORTUGUESE = "Salva uma página RGB. A compressão pode reduzir o tamanho do arquivo " +
            "sem alterar os pixels; desative-a para criar um TIFF sem compressão."
    }
}
