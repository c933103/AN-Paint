/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.graphics.Bitmap
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
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import java.io.File
import java.util.Locale

/** Ten bounded reviewed values and real consumers, not installed/native-language acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class UkrainianSaveWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private val fixture by lazy {
        JSONObject(File("../tools/fixtures/current_localization/ukrainian_save_wording.json").readText())
    }

    // Decode only these ten simple quote-wrapped values, not inherited Android escapes.
    private fun expected(tag: String, key: String) = PriorityWordingExpectations.current(tag,key,
        fixture.getJSONObject("values").getJSONObject(key).getString(tag)).removeSurrounding("\"")

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
        for (tag in listOf("uk")) {
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
        assertEquals("Зберегти", ui(R.string.ui_save))
        assertEquals(ui(R.string.ui_save), ui(R.string.ui_save_a5d0d9))
        assertEquals("Файл", ui(R.string.ui_menu_file))
        assertEquals("Скасувати", ui(R.string.ui_cancel))
        assertEquals("Зберегти як…", ui(R.string.save20_title))
        assertEquals("Експортувати як…", ui(R.string.ui_export_as23))
        assertEquals("Зберегти зміни?", ui(R.string.ui_save_your_changes))
        assertEquals(expected(tag, "ui_save_and_share_41edb4") + "…", ui(R.string.ui_save_and_share))
        // Explicitly reviewed successors replace these neighbors; unrelated P2 context stays exact.
        assertEquals(PriorityWordingExpectations.display("uk","save20_file_format"), ui(R.string.save20_file_format))
        assertEquals(PriorityWordingExpectations.display("uk","ui_choose_location"), ui(R.string.ui_choose_location))
        assertEquals(PriorityWordingExpectations.display("uk","ui_share_saved_image"), ui(R.string.ui_share_saved_image))
        assertEquals("Base64 text", ui(R.string.formats22_base64_label))
        assertEquals("Рисунки у ASCII", ui(R.string.formats22_ascii_label))
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
                assertTrue(displayed.contains(PriorityWordingExpectations.display("uk","save20_file_format")))
                assertEquals(PriorityWordingExpectations.display("uk","ui_choose_location"), shown.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals("Скасувати", shown.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
                if (it == 0) shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick() else shown.cancel()
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

    @Test fun actualDirtyImagePromptIsNotExportCompletionAndRepeatedCancelPreservesTheDrawing() {
        val app = RuntimeEnvironment.getApplication() as Context
        val oldTag = AppLanguage.selectedTag(app)
        for (name in listOf("classic-recovery.png", "classic-autosave.zip", "classic-autosave.zip.bak"))
            File(app.filesDir, name).delete()
        app.getSharedPreferences("classic-ui", Context.MODE_PRIVATE).edit().clear().commit()
        val controller = Robolectric.buildActivity(ClassicPaintActivity::class.java)
        val activity = controller.setup().get()
        var snapshot: Bitmap? = null
        try {
            awaitEditorStartup(activity)
            AppLanguage.select(activity, "uk")
            AppLanguage.refresh(activity)
            activity.document.newImage(32, 24)
            activity.document.invert()
            activity.paintCanvas.fit()
            val document = activity.document
            snapshot = document.bitmap.copy(Bitmap.Config.ARGB_8888, false)
            val history = document.historySnapshot()
            val unsaved = expected("uk", "ui_your_current_image_has_unsaved_changes")
            val exported = expected("uk", "ui_export_did_not_save23")
            assertNotEquals(unsaved, exported)
            repeat(2) {
                EditorTestNavigation.command(activity, "File", 0)
                val shown = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
                assertEquals("Зберегти зміни?", shadowOf(shown).title.toString())
                val body = shown.findViewById<TextView>(android.R.id.message).text.toString()
                assertEquals(unsaved, body)
                assertNotEquals(exported, body)
                assertEquals("Зберегти", shown.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals(PriorityWordingExpectations.display("uk","ui_keep_editing23"), shown.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
                assertTrue(shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick())
                EditorTestNavigation.idle()
                assertFalse(shown.isShowing)
                assertTrue(document.dirty)
                assertTrue(snapshot!!.sameAs(document.bitmap))
                assertEquals(history, document.historySnapshot())
                assertNull(shadowOf(activity).nextStartedActivityForResult)
            }
            // The clean document takes the real New route without the unsaved warning.
            document.markSaved()
            EditorTestNavigation.command(activity, "File", 0)
            val shown = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            assertNotNull(shown.window!!.decorView.findViewWithTag<View>("size_width"))
            assertNotEquals("Зберегти зміни?", shadowOf(shown).title.toString())
            shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
            EditorTestNavigation.idle()
            assertFalse(shown.isShowing)
            assertFalse(document.dirty)
            assertTrue(snapshot!!.sameAs(document.bitmap))
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
            controller.pause().stop()
            val deadline = System.nanoTime() + 10_000_000_000L
            while (activity.busy && System.nanoTime() < deadline) {
                shadowOf(Looper.getMainLooper()).idle()
                Thread.sleep(10)
            }
            controller.destroy()
            snapshot?.recycle()
            AppLanguage.select(app, oldTag)
        }
    }
}
