/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.graphics.Rect
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.CheckBox
import android.widget.EditText
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONObject
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
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.util.ReflectionHelpers
import org.robolectric.util.ReflectionHelpers.ClassParameter
import java.io.File
import java.io.IOException
import java.util.Locale
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

/** Real UI consumers and compiled resources; not installed-device or native-fluency evidence. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "sv-rSE-w412dp-h900dp-port-xhdpi")
class SwedishExtendedWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var swedish: Context
    private val fixture by lazy {
        JSONObject(File("../tools/fixtures/current_localization/swedish_extended_wording.json").readText())
    }

    @Before fun swedishResources() {
        previousResources = PaintApplication.currentResources
        val context = RuntimeEnvironment.getApplication() as Context
        swedish = context.createConfigurationContext(Configuration(context.resources.configuration).apply {
            setLocale(Locale.forLanguageTag("sv"))
        })
        PaintApplication.currentResources = swedish.resources
    }
    @After fun restoreResources() {
        ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
        PaintApplication.currentResources = previousResources
    }
    private fun idle() = shadowOf(Looper.getMainLooper()).idle()
    private fun expected(key: String) = fixture.getJSONObject("values").getJSONObject(key).getString("sv")
        .removeSurrounding("\"").replace("\\n", "\n").replace("\\'", "'")
    private fun texts(view: View): List<String> =
        (if (view is TextView) listOf(view.text.toString()) else emptyList()) +
            (if (view is ViewGroup) (0 until view.childCount).flatMap { texts(view.getChildAt(it)) } else emptyList())

    @Test fun completeCriticalMessagesResolveWithoutDefaultEnglishFallback() {
        val values = fixture.getJSONObject("values")
        for (key in values.keys()) {
            val id = swedish.resources.getIdentifier(key, "string", swedish.packageName)
            assertNotEquals(key, 0, id)
            assertEquals(key, expected(key), swedish.getString(id))
        }
        assertEquals(swedish.getString(R.string.ui_cursor_help31), swedish.getString(R.string.ui_cursor_help29))
        val plural = fixture.getJSONObject("plural").getJSONObject("sv")
        for (count in listOf(0, 1, 2, 20, 21, 101)) {
            val template = plural.getString(if (count == 1) "one" else "other").replace("\\n", "\n")
            assertEquals(template, swedish.resources.getQuantityText(R.plurals.ui_crop_preview_images, count).toString())
            assertEquals(String.format(Locale.forLanguageTag("sv"), template, 24, 16, count),
                swedish.resources.getQuantityString(R.plurals.ui_crop_preview_images, count, 24, 16, count))
        }
    }

    @Test fun allTwelveCommonsFailuresUseTheActualDispatcherAndKeepProviderDetailVerbatim() {
        val gallery = MediaGalleryActivity()
        val cases = listOf(
            CommonsAttribution.HttpException(503) to "Commons-metadata: HTTP 503",
            CommonsAttribution.ResponseLimitException() to expected("commons_metadata_response_too_large"),
            CommonsAttribution.QueryFailureException() to expected("commons_metadata_query_failed"),
            CommonsImportFailure.NotFilePage() to expected("commons_metadata_not_file_page"),
            CommonsImportFailure.AmbiguousFile() to expected("commons_metadata_ambiguous_file"),
            CommonsImportFailure.MetadataUnavailable() to expected("commons_metadata_unavailable"),
            CommonsImportFailure.MetadataOriginalMismatch() to expected("commons_metadata_original_mismatch"),
            CommonsImportFailure.InvalidAttributionPage() to expected("commons_metadata_invalid_page"),
            CommonsImportFailure.FieldTooLarge() to expected("commons_metadata_field_too_large"),
            CommonsImportFailure.CacheFailed() to expected("commons_metadata_cache_failed"),
            CommonsImportFailure.DownloadOriginalMismatch() to expected("commons_download_original_mismatch"),
            CommonsImportFailure.PngEncodeFailed() to expected("commons_svg_png_encode_failed")
        )
        assertEquals(12, cases.size)
        fun reason(error: Exception): String? = ReflectionHelpers.callInstanceMethod(gallery, "commonsMetadataReason",
            ClassParameter.from(Exception::class.java, error))
        for ((error, wording) in cases) {
            assertEquals(wording, reason(error))
            assertEquals("Bildens erkännande kunde inte kopieras: $wording",
                ui(R.string.commons_credit_copy_failed_reason, reason(error)!!))
        }
        val provider = "  Provider 50%: %1\$s · détails\nTry again.  "
        assertEquals(provider, reason(IOException(provider)))
        assertEquals("Bildens erkännande kunde inte kopieras: $provider",
            ui(R.string.commons_credit_copy_failed_reason, reason(IOException(provider))!!))
        assertNull(reason(IOException()))
    }

    @Test fun cropSelectionChangesQuantityAndCancelNeverAppliesThePreview() {
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        var applied = 0
        val images = (1..2).map { AssemblyImage("sv-$it", File(activity.cacheDir, "sv-$it.image"),
            "Bild $it", null, ImageDimensions(24, 16)) }
        try {
            repeat(2) {
                val dialog = ImageCropDialog(activity, images, { null }, { applied++ }).show()
                val status = dialog.window!!.decorView.findViewWithTag<TextView>("crop_status")
                fun full(count: Int) = "Förhandsvisning: 24 × 16 px\nVerkställ för $count ${if (count == 1) "bild" else "bilder"}. " +
                    "Om placerade bilder beskärs kan bilder som är fästa vid dem flyttas."
                assertEquals(full(2), status.text.toString())
                val second = dialog.window!!.decorView.findViewWithTag<CheckBox>("crop_include_sv-2")
                second.isChecked = false; idle()
                assertEquals(full(1), status.text.toString())
                assertEquals("Beskärning från Överkant i bildpunkter",
                    dialog.window!!.decorView.findViewWithTag<EditText>("crop_top").contentDescription.toString())
                dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
                assertFalse(dialog.isShowing); assertEquals(0, applied)
                assertTrue(images.all { it.crop == Rect(0, 0, 24, 16) })
            }
        } finally { controller.pause().stop().destroy() }
    }

    @Test fun exactPositionValidatesLocalizedInputAndOnlyMovesTheSelectedImage() {
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        val directory = File(activity.cacheDir, "swedish-position").apply { deleteRecursively(); mkdirs() }
        try {
            val assembly = ImageAssembly(directory)
            val first = AssemblyImage("first", File(directory, "first.image").apply { writeBytes(byteArrayOf(1)) },
                "Första", null, ImageDimensions(24, 16))
            val second = AssemblyImage("second", File(directory, "second.image").apply { writeBytes(byteArrayOf(2)) },
                "Andra", null, ImageDimensions(24, 16))
            assembly.add(listOf(first, second)); assembly.position(first.id, 0, 0); assembly.position(second.id, 24, 0)
            val before = assembly.layout(); val saved = File(directory, "project.json").readBytes()
            val dialog = AssemblyPositionDialog(activity, assembly, first.id).show()
            assertEquals("Exakt position", shadowOf(dialog).title.toString())
            assertTrue(texts(dialog.window!!.decorView).contains(expected("ui_assembly_position_help")))
            val x = dialog.window!!.decorView.findViewWithTag<EditText>("assembly_position_x")
            val y = dialog.window!!.decorView.findViewWithTag<EditText>("assembly_position_y")
            assertEquals(expected("ui_assembly_target_x"), x.contentDescription.toString())
            assertEquals(expected("ui_assembly_target_y"), y.contentDescription.toString())
            for (invalid in listOf("-1", "1,5", "2147483648", "")) {
                x.setText(invalid); dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle()
                assertTrue(dialog.isShowing)
                assertEquals(expected("ui_assembly_position_nonnegative"),
                    dialog.window!!.decorView.findViewWithTag<TextView>("assembly_position_error").text.toString())
                assertEquals(before, assembly.layout()); assertArrayEquals(saved, File(directory, "project.json").readBytes())
            }
            x.setText("24"); y.setText("0")
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
            assertEquals(before, assembly.layout())
            val accepted = AssemblyPositionDialog(activity, assembly, first.id).show()
            accepted.window!!.decorView.findViewWithTag<EditText>("assembly_position_x").setText("24")
            accepted.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle()
            assertFalse(accepted.isShowing)
            assertEquals(Rect(24, 0, 48, 16), assembly.layout()[first.id])
            assertEquals(before[second.id], assembly.layout()[second.id])
            assertEquals(first.crop, assembly.image(first.id).crop)
        } finally { controller.pause().stop().destroy(); directory.deleteRecursively() }
    }

    @Test fun pageChooserUsesSwedishControlsAndRangeErrorsWithoutSelectingOnCancel() {
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        val worker = Executors.newSingleThreadExecutor()
        var selected = 0; var cancelled = 0; var failure: Throwable? = null
        var selection: ImportSelection? = null
        try {
            for (kind in listOf("PDF", "TIFF")) {
                selection = ImportSelection(activity, worker, { 0L }, { selected++ }, { cancelled++ }, { failure = it })
                // Isolate the real chooser from decoding/network; no staged file is supplied.
                ReflectionHelpers.setField(selection, "name", "karta.$kind")
                ReflectionHelpers.callInstanceMethod<Unit>(selection, "showPages",
                    ClassParameter.from(String::class.java, kind), ClassParameter.from(Int::class.javaPrimitiveType!!, 3))
                val dialog = checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
                assertEquals("Välj en sida", shadowOf(dialog).title.toString())
                assertTrue(texts(dialog.window!!.decorView).contains("$kind · karta.$kind\nAntal sidor: 3. Välj en sida att redigera som bild."))
                assertEquals("Öppna sida", dialog.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals("Föregående sida", dialog.window!!.decorView.findViewWithTag<View>("import_previous_page").contentDescription)
                assertEquals("Nästa sida", dialog.window!!.decorView.findViewWithTag<View>("import_next_page").contentDescription)
                val field = dialog.window!!.decorView.findViewWithTag<EditText>("import_page_number")
                assertEquals("Sidnummer", field.contentDescription)
                for (invalid in listOf("0", "4", "")) {
                    field.setText(invalid); idle()
                    assertEquals("Ange ett sidnummer från 1 till 3.",
                        dialog.window!!.decorView.findViewWithTag<TextView>("import_page_status").text.toString())
                    assertFalse(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
                }
                field.setText("2"); idle()
                assertTrue(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
                dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
                assertFalse(dialog.isShowing); assertEquals(0, selected); assertNull(failure)
            }
            assertEquals(2, cancelled)
        } finally {
            selection?.dispose(); worker.shutdownNow()
            try { assertTrue(worker.awaitTermination(10, TimeUnit.SECONDS)) }
            finally { controller.pause().stop().destroy() }
        }
    }
}
