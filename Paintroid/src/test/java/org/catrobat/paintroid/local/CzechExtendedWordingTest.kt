/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.app.LocaleManager
import android.content.Context
import android.content.SharedPreferences
import android.content.res.Resources
import android.graphics.Rect
import android.os.LocaleList
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.CheckBox
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
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.util.ReflectionHelpers
import org.robolectric.util.ReflectionHelpers.ClassParameter
import java.io.File
import java.io.IOException
import java.text.DecimalFormatSymbols
import java.util.Locale
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

/** Real UI consumers and compiled resources; not installed-device or native-fluency evidence. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "cs-rCZ-w412dp-h900dp-port-xhdpi")
class CzechExtendedWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var preferences: SharedPreferences
    private var previousTag: String? = null
    private var hadTag = false
    private var previousInitialized = false
    private var hadInitialized = false
    private var localeManager: LocaleManager? = null
    private var previousPlatformLocales: LocaleList? = null
    private lateinit var czech: Context

    @Before fun czechResources() {
        previousResources = PaintApplication.currentResources
        previousLocale = Locale.getDefault()
        val context = RuntimeEnvironment.getApplication() as Context
        preferences = context.getSharedPreferences("app-language", Context.MODE_PRIVATE)
        hadTag = preferences.contains("language-tag")
        previousTag = preferences.getString("language-tag", null)
        hadInitialized = preferences.contains("platform-initialized")
        previousInitialized = preferences.getBoolean("platform-initialized", false)
        localeManager = context.getSystemService(LocaleManager::class.java)
        previousPlatformLocales = localeManager?.applicationLocales
        // Select the real app language, not only a resource overlay: uiNumber
        // uses the process locale which AppLanguage.wrap/refresh also updates.
        AppLanguage.select(context, "cs")
        czech = AppLanguage.wrap(context)
        PaintApplication.currentResources = czech.resources
    }
    @After fun restoreResources() {
        ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
        idle()
        previousPlatformLocales?.let { localeManager?.applicationLocales = it }
        preferences.edit().apply {
            if (hadTag) putString("language-tag", previousTag) else remove("language-tag")
            if (hadInitialized) putBoolean("platform-initialized", previousInitialized) else remove("platform-initialized")
        }.commit()
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
    }
    private fun idle() = shadowOf(Looper.getMainLooper()).idle()
    private fun expected(key: String) = PriorityWordingExpectations.resourceText("cs",key)
    private fun texts(view: View): List<String> =
        (if (view is TextView) listOf(view.text.toString()) else emptyList()) +
            (if (view is ViewGroup) (0 until view.childCount).flatMap { texts(view.getChildAt(it)) } else emptyList())

    @Test fun dormantManualResolvesCzechParagraphsThroughTheSelectedResources() {
        // This key is not the active Help dialog. Check compiled selection and escapes,
        // not a second full-text approval mirror or a claim of installed layout coverage.
        val value = ui(R.string.ui_the_arrow_on_the_left_directly_below_the)
        val paragraphs = value.split("\n\n")
        assertEquals(10, paragraphs.size)
        assertTrue(paragraphs.first().startsWith("Vyberte kartu Zobrazení"))
        assertTrue(paragraphs[2].contains(czech.getString(R.string.ui_draw_again)))
        assertTrue(paragraphs[7].contains(czech.getString(R.string.commons_blank_maps)))
        assertTrue(paragraphs[8].contains("připojené obrázky se mohou posunout a vyplnit mezeru"))
        assertTrue(paragraphs.last().endsWith("Kopírovat vše, Další podmínky a Hotovo."))
        assertFalse(value.contains("\\n"))
    }

    @Test fun allTwelveCommonsFailuresUseTheActualDispatcherAndKeepProviderDetailVerbatim() {
        val gallery = MediaGalleryActivity()
        val cases = listOf(
            CommonsAttribution.HttpException(503) to "Metadata Commons: HTTP 503",
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
            assertEquals("Údaje o autorství obrázku se nepodařilo zkopírovat: $wording",
                ui(R.string.commons_credit_copy_failed_reason, reason(error)!!))
        }
        val provider = "  Provider 50%: %1\$s · détails\nTry again.  "
        assertEquals(provider, reason(IOException(provider)))
        assertEquals("Údaje o autorství obrázku se nepodařilo zkopírovat: $provider",
            ui(R.string.commons_credit_copy_failed_reason, reason(IOException(provider))!!))
        assertNull(reason(IOException()))
    }

    @Test fun cropSelectionChangesQuantityAndCancelNeverAppliesThePreview() {
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        var applied = 0
        val images = (1..5).map { AssemblyImage("cs-$it", File(activity.cacheDir, "cs-$it.image"),
            "Obrázek $it", null, ImageDimensions(24, 16)) }
        try {
            repeat(2) {
                val dialog = ImageCropDialog(activity, images, { null }, { applied++ }).show()
                val status = dialog.window!!.decorView.findViewWithTag<TextView>("crop_status")
                fun full(count: Int): String {
                    val noun = when (count) { 1 -> "obrázek"; in 2..4 -> "obrázky"; else -> "obrázků" }
                    return "Náhled: 24 × 16 px\nPoužít na $count $noun. " +
                        "Ořez umístěných obrázků může posunout obrázky, které jsou k nim připojené."
                }
                assertEquals(full(5), status.text.toString())
                for (unchecked in 5 downTo 2) {
                    dialog.window!!.decorView.findViewWithTag<CheckBox>("crop_include_cs-$unchecked").isChecked = false
                    idle(); assertEquals(full(unchecked - 1), status.text.toString())
                }
                assertEquals("Nahoře: ořez v pixelech",
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
        AppLanguage.refresh(activity)
        val directory = File(activity.cacheDir, "czech-position").apply { deleteRecursively(); mkdirs() }
        try {
            assertEquals("cs", AppLanguage.selectedTag(activity))
            assertEquals("cs", activity.resources.configuration.locales[0].language)
            assertEquals("cs", Locale.getDefault().language)
            assertEquals(1.5, checkNotNull(uiNumber("1,5")), 0.0)
            val assembly = ImageAssembly(directory)
            val first = AssemblyImage("first", File(directory, "first.image").apply { writeBytes(byteArrayOf(1)) },
                "První", null, ImageDimensions(24, 16))
            val second = AssemblyImage("second", File(directory, "second.image").apply { writeBytes(byteArrayOf(2)) },
                "Druhý", null, ImageDimensions(24, 16))
            assembly.add(listOf(first, second)); assembly.position(first.id, 0, 0); assembly.position(second.id, 24, 0)
            val before = assembly.layout(); val saved = File(directory, "project.json").readBytes()
            val dialog = AssemblyPositionDialog(activity, assembly, first.id).show()
            // Dialog.show queues OnShow; let it install the validation click
            // listener before sending input to the positive button.
            idle()
            assertEquals("Přesná poloha", shadowOf(dialog).title.toString())
            assertTrue(texts(dialog.window!!.decorView).contains(expected("ui_assembly_position_help")))
            val x = dialog.window!!.decorView.findViewWithTag<EditText>("assembly_position_x")
            val y = dialog.window!!.decorView.findViewWithTag<EditText>("assembly_position_y")
            assertEquals(expected("ui_assembly_target_x"), x.contentDescription.toString())
            assertEquals(expected("ui_assembly_target_y"), y.contentDescription.toString())
            // Exercise signs retained by the real Czech input filter. Arbitrary
            // non-native Unicode-minus filtering is a separate behavior, not this test's claim.
            val nativeMinus = DecimalFormatSymbols.getInstance(Locale.getDefault()).minusSign
            val invalidValues = setOf('-', nativeMinus).map { "${it}1" } +
                listOf("1,5", "1.5", "2147483648", "")
            for (field in listOf(x, y)) {
                for (invalid in invalidValues) {
                    x.setText("0"); y.setText("0")
                    field.setText(""); field.text.replace(0, 0, invalid)
                    assertEquals("Numeric syntax must reach validation unchanged", invalid, field.text.toString())
                    dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle()
                    assertTrue("${field.tag}=$invalid must leave the dialog open", dialog.isShowing)
                    assertEquals(expected("ui_assembly_position_nonnegative"),
                        dialog.window!!.decorView.findViewWithTag<TextView>("assembly_position_error").text.toString())
                    assertEquals(before, assembly.layout()); assertArrayEquals(saved, File(directory, "project.json").readBytes())
                }
            }
            x.setText("24"); y.setText("0")
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
            assertEquals(before, assembly.layout())
            val accepted = AssemblyPositionDialog(activity, assembly, first.id).show()
            idle()
            accepted.window!!.decorView.findViewWithTag<EditText>("assembly_position_x").setText("24")
            accepted.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle()
            assertFalse(accepted.isShowing)
            assertEquals(Rect(24, 0, 48, 16), assembly.layout()[first.id])
            assertEquals(before[second.id], assembly.layout()[second.id])
            assertEquals(first.crop, assembly.image(first.id).crop)
        } finally { controller.pause().stop().destroy(); directory.deleteRecursively() }
    }

    @Test fun pageChooserUsesCzechControlsAndRangeErrorsWithoutSelectingOnCancel() {
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
                ReflectionHelpers.setField(selection, "name", "mapa.$kind")
                ReflectionHelpers.callInstanceMethod<Unit>(selection, "showPages",
                    ClassParameter.from(String::class.java, kind), ClassParameter.from(Int::class.javaPrimitiveType!!, 3))
                val dialog = checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
                assertEquals("Vybrat stránku", shadowOf(dialog).title.toString())
                assertTrue(texts(dialog.window!!.decorView).contains("$kind · mapa.$kind\nPočet stránek: 3. Vyberte jednu stránku k úpravě jako obrázek."))
                assertEquals("Otevřít stránku", dialog.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals("Předchozí stránka", dialog.window!!.decorView.findViewWithTag<View>("import_previous_page").contentDescription)
                assertEquals("Další stránka", dialog.window!!.decorView.findViewWithTag<View>("import_next_page").contentDescription)
                val field = dialog.window!!.decorView.findViewWithTag<EditText>("import_page_number")
                assertEquals("Číslo stránky", field.contentDescription)
                for (invalid in listOf("0", "4", "")) {
                    field.setText(invalid); idle()
                    assertEquals("Zadejte číslo stránky od 1 do 3.",
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
