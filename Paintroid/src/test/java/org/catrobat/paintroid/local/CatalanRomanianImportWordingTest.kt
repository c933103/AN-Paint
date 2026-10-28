/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.res.Resources
import android.os.Looper
import android.view.View
import android.widget.CheckBox
import android.widget.EditText
import android.widget.Spinner
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
import java.io.File
import java.util.Locale

/** Bounded compiled wording and real format-panel behavior, not whole-locale acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class CatalanRomanianImportWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    private val fixture by lazy {
        JSONObject(File("../tools/fixtures/current_localization/catalan_romanian_import_wording.json").readText())
    }

    // The new reviewed values use simple Android quote wrapping. Inherited strings
    // can contain Android escapes and are preserved by separate source contracts.
    private fun expected(tag: String, key: String) = SkSlCaPriorityExpectations.current(tag,key,
        fixture.getJSONObject("values").getJSONObject(key).getString(tag)).removeSurrounding("\"")

    @Before fun rememberLanguage() {
        previousResources = PaintApplication.currentResources
        previousLocale = Locale.getDefault()
        previousTag = AppLanguage.selectedTag(RuntimeEnvironment.getApplication())
    }

    @After fun restoreLanguage() {
        AppLanguage.select(RuntimeEnvironment.getApplication(), previousTag)
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
    }

    private fun forEachLocale(check: (String, Activity) -> Unit) {
        for (tag in listOf("ca", "ro")) {
            val controller = Robolectric.buildActivity(Activity::class.java)
            val activity = controller.get()
            activity.setTheme(R.style.ClassicPaintTheme)
            controller.setup()
            try {
                AppLanguage.select(activity, tag)
                AppLanguage.refresh(activity)
                assertEquals(tag, AppLanguage.selectedTag(activity))
                check(tag, activity)
            } finally {
                AppLanguage.select(activity, previousTag)
                AppLanguage.refresh(activity)
                controller.pause().stop().destroy()
                PaintApplication.currentResources = previousResources
                Locale.setDefault(previousLocale)
            }
        }
    }

    @Test fun all13CompiledValuesPerLocaleKeepFormatArgumentsAndUnreviewedFallbacks() = forEachLocale { tag, activity ->
        val values = fixture.getJSONObject("values")
        assertEquals(13, values.length())
        assertEquals(137, fixture.getJSONObject("preserved_values").getJSONObject(tag).length())
        for (key in values.keys()) {
            val id = activity.resources.getIdentifier(key, "string", activity.packageName)
            assertNotEquals("$tag/$key", 0, id)
            assertEquals("$tag/$key", expected(tag, key), activity.getString(id))
        }
        val format = "GIF 100%"
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "formats22_animation_unknown"), format),
            ui(R.string.formats22_animation_unknown, format))
        assertEquals(String.format(Locale.forLanguageTag(tag),SkSlCaPriorityExpectations.display(tag,"formats22_at_least_frames"),2), ui(R.string.formats22_at_least_frames, 2))
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "formats22_animation_message"), format, String.format(Locale.forLanguageTag(tag),SkSlCaPriorityExpectations.display(tag,"formats22_at_least_frames"),2)),
            ui(R.string.formats22_animation_message, format, String.format(Locale.forLanguageTag(tag),SkSlCaPriorityExpectations.display(tag,"formats22_at_least_frames"),2)))
        // Explicit Catalan and Romanian priority successors preserve the held fallbacks below.
        assertEquals(SkSlCaPriorityExpectations.display(tag,"save20_file_format"), ui(R.string.save20_file_format))
        assertEquals(SkSlCaPriorityExpectations.display(tag,"ui_choose_location"), ui(R.string.ui_choose_location))
        assertEquals(if (tag == "ca") "Desa" else "Salvează", ui(R.string.ui_save))
        assertEquals(if (tag == "ca") "Anomena i desa…" else "Salvează ca…", ui(R.string.save20_title))
        assertEquals(if (tag == "ca") SkSlCaPriorityExpectations.display("ca","ui_save_your_changes") else "Salvaţi modificările?", ui(R.string.ui_save_your_changes))
        assertEquals(if (tag == "ca") "Art ASCII" else "Artă ASCII", ui(R.string.formats22_ascii_label))
        assertEquals("PNG exported. Your full drawing still has unsaved changes; save a full image copy before replacing it.",
            ui(R.string.formats22_derived_exported, "PNG"))
        assertEquals("Save as PNG", ui(R.string.ui_save_as, "PNG"))
        assertEquals("Save as JPEG…", ui(R.string.ui_save_as_jpeg))
        assertEquals("Save as JPEG XL…", ui(R.string.ui_save_as_jpeg_xl))
        assertEquals("Save as PNG…", ui(R.string.ui_save_as_png))
    }

    @Test fun realFormatPanelUpdatesDescriptionsRejectsInvalidNamesAndCancelsRepeatedly() = forEachLocale { tag, activity ->
        repeat(2) { attempt ->
            var confirmations = 0
            var cancellations = 0
            // Production Share exposes all formats; both flags are also set by the real File-menu action.
            val dialog = SaveOptionsDialog(activity, ExportOptions(format = ImageFormat.GIF), share = true,
                confirm = { confirmations++ }, cancel = { cancellations++ },
                initialFilename = "drawing 100%.png", export = true).show()
            try {
                val root = dialog.window!!.decorView
                val spinner = checkNotNull(root.findViewWithTag<Spinner>("export_format"))
                val explanation = checkNotNull(root.findViewWithTag<FlowTextView>("export_description"))
                val quality = checkNotNull(root.findViewWithTag<NumericSlider>("export_quality"))
                val lossless = checkNotNull(root.findViewWithTag<CheckBox>("export_lossless"))
                val dither = checkNotNull(root.findViewWithTag<CheckBox>("export_dither"))
                val filename = checkNotNull(root.findViewWithTag<EditText>("export_filename"))
                assertEquals(SkSlCaPriorityExpectations.display(tag,"save20_file_format"), spinner.contentDescription.toString())
                assertEquals(SkSlCaPriorityExpectations.display(tag,"ui_choose_location"), dialog.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals(if (tag == "ca") "Cancel·la" else "Anulează",
                    dialog.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
                fun select(format: ImageFormat, key: String) {
                    spinner.setSelection(ImageFormat.values().indexOf(format))
                    shadowOf(Looper.getMainLooper()).idle()
                    assertEquals(format.label, spinner.selectedItem.toString())
                    assertEquals(expected(tag, key), explanation.text.toString())
                    assertEquals(View.VISIBLE, explanation.visibility)
                }
                select(ImageFormat.GIF, "save20_gif_description")
                assertEquals(View.VISIBLE, dither.visibility)
                assertEquals(View.GONE, quality.visibility)
                select(ImageFormat.JPEG, "save20_lossy_quality_description")
                assertEquals(View.GONE, dither.visibility)
                assertEquals(View.GONE, lossless.visibility)
                assertEquals(View.VISIBLE, quality.visibility)
                select(ImageFormat.WEBP, "ui_higher_quality_usually_makes_a_larger_file_lossless")
                assertEquals(View.VISIBLE, lossless.visibility)
                assertTrue(lossless.isChecked)
                assertEquals(View.GONE, quality.visibility)
                lossless.performClick()
                shadowOf(Looper.getMainLooper()).idle()
                assertFalse(lossless.isChecked)
                assertEquals(View.VISIBLE, quality.visibility)
                assertEquals(expected(tag, "ui_higher_quality_usually_makes_a_larger_file_lossless"), explanation.text.toString())
                select(ImageFormat.ASCII_ART, "formats22_ascii_description")
                assertEquals(View.VISIBLE, root.findViewWithTag<View>("export_ascii_controls").visibility)
                assertEquals(View.GONE, quality.visibility)
                filename.setText("folder/bad-name.txt")
                repeat(2) {
                    dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
                    shadowOf(Looper.getMainLooper()).idle()
                    assertEquals(expected(tag, "save20_invalid_name"), filename.error.toString())
                    assertTrue(dialog.isShowing)
                    assertEquals(0, confirmations)
                    assertEquals(0, cancellations)
                }
                if (attempt == 0) dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick() else dialog.cancel()
                shadowOf(Looper.getMainLooper()).idle()
                assertFalse(dialog.isShowing)
                assertEquals(0, confirmations)
                assertEquals(1, cancellations)
            } finally { dialog.dismiss() }
        }
    }
}
