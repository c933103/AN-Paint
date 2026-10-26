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
import java.io.File
import java.util.Locale

/** Twenty bounded reviewed values and real dialog consumers, not whole-locale acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class CatalanRomanianSaveWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private val fixture by lazy {
        JSONObject(File("../tools/fixtures/current_localization/catalan_romanian_save_wording.json").readText())
    }

    // Only these ten newly reviewed strings are simple quote-wrapped values.
    // Inherited Catalan values can contain Android escapes and are not decoded this way.
    private fun expected(tag: String, key: String) = fixture.getJSONObject("values")
        .getJSONObject(key).getString(tag).removeSurrounding("\"")

    @Before fun rememberResources() {
        previousResources = PaintApplication.currentResources
        previousLocale = Locale.getDefault()
    }

    @After fun restoreResources() {
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
    }

    private fun forEachLocale(check: (String, Context) -> Unit) {
        val app = RuntimeEnvironment.getApplication() as Context
        for (tag in listOf("ca", "ro")) {
            val context = app.createConfigurationContext(Configuration(app.resources.configuration).apply {
                setLocale(AppLanguage.resourceLocale(Locale.forLanguageTag(tag)))
            })
            try {
                PaintApplication.currentResources = context.resources
                Locale.setDefault(Locale.US)
                check(tag, context)
            } finally {
                PaintApplication.currentResources = previousResources
                Locale.setDefault(previousLocale)
            }
        }
    }

    @Test fun allTenCompiledValuesAndSingleSubstitutionsPreserveActualNeighborLabels() = forEachLocale { tag, context ->
        val values = fixture.getJSONObject("values")
        assertEquals(10, values.length())
        for (key in values.keys()) {
            val id = context.resources.getIdentifier(key, "string", context.packageName)
            assertNotEquals("$tag/$key", 0, id)
            assertEquals("$tag/$key", expected(tag, key), context.getString(id))
        }
        val filename = "drawing 100%.png"
        val detail = "provider 50% unavailable"
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "ui_saved"), filename),
            ui(R.string.ui_saved, filename))
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "ui_the_image_was_saved_but_android_could_not"), detail),
            ui(R.string.ui_the_image_was_saved_but_android_could_not, detail))
        assertEquals(if (tag == "ca") "Desa" else "Salvează", ui(R.string.ui_save))
        assertEquals(ui(R.string.ui_save), ui(R.string.ui_save_a5d0d9))
        assertEquals(if (tag == "ca") "Anomena i desa…" else "Salvează ca…", ui(R.string.save20_title))
        assertEquals(if (tag == "ca") "Exporta com a…" else "Exportă ca…", ui(R.string.ui_export_as23))
        assertEquals(if (tag == "ca") "Save changes?" else "Salvaţi modificările?", ui(R.string.ui_save_your_changes))
        assertEquals(expected(tag, "ui_save_and_share_41edb4") + "…", ui(R.string.ui_save_and_share))
        // Existing mixed-language/fallback values are context, not newly reviewed translations.
        assertEquals("Image format", ui(R.string.save20_file_format))
        assertEquals("Choose location…", ui(R.string.ui_choose_location))
        assertEquals("Share saved image", ui(R.string.ui_share_saved_image))
        assertEquals("Base64 text", ui(R.string.formats22_base64_label))
        assertEquals(if (tag == "ca") "Art ASCII" else "Artă ASCII", ui(R.string.formats22_ascii_label))
    }

    @Test fun actualSaveExportAndSharePanelsKeepTheirDistinctWholeMessagesAndRepeatedCancel() = forEachLocale { tag, _ ->
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        var dialog: AlertDialog? = null
        try {
            fun texts(view: View): List<String> =
                (if (view is TextView) listOf(view.text.toString()) else emptyList()) +
                    (if (view is ViewGroup) (0 until view.childCount).flatMap { texts(view.getChildAt(it)) } else emptyList())
            val save = expected(tag, "ui_save_explanation23")
            val export = expected(tag, "ui_export_explanation23")
            val share = expected(tag, "ui_share_explanation34")
            // Real File-menu Share sets both flags; its copy/share prose must take precedence.
            val modes = listOf(Triple(false, false, save), Triple(false, true, export), Triple(true, true, share))
            for ((sharing, exporting, message) in modes) repeat(2) {
                var confirmed = false
                var cancelled = 0
                val shown = SaveOptionsDialog(activity, ExportOptions(), share = sharing,
                    confirm = { confirmed = true }, cancel = { cancelled++ }, export = exporting).show()
                dialog = shown
                val displayed = texts(shown.window!!.decorView)
                assertTrue(displayed.contains(message))
                for (other in listOf(save, export, share).filter { it != message }) assertFalse(displayed.contains(other))
                assertEquals(if (sharing) expected(tag, "ui_save_and_share_41edb4")
                    else ui(if (exporting) R.string.ui_export_as23 else R.string.save20_title), shadowOf(shown).title.toString())
                assertTrue(displayed.contains("Image format"))
                assertEquals("Choose location…", shown.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals(if (tag == "ca") "Cancel·la" else "Anulează", shown.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
                shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
                shadowOf(Looper.getMainLooper()).idle()
                assertFalse(shown.isShowing)
                assertFalse(confirmed)
                assertEquals(1, cancelled)
            }
        } finally {
            dialog?.dismiss()
            controller.pause().stop().destroy()
        }
    }
}
