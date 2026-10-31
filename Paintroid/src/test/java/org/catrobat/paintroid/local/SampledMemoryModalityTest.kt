/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.app.LocaleManager
import android.content.Context
import android.os.Looper
import android.widget.EditText
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.shadows.ShadowAlertDialog
import java.util.Locale

/** Complete warning regressions and real consumers, not whole-message linguistic acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
class SampledMemoryModalityTest {
    private val context get() = RuntimeEnvironment.getApplication() as Context
    private val historicalExpected = JSONObject(javaClass.getResourceAsStream("/memory-modality/expected.json")!!
        .bufferedReader(Charsets.UTF_8).use { it.readText() }).getJSONObject("values")
    private val mib = 1024L * 1024
    private fun idle() = shadowOf(Looper.getMainLooper()).idle()
    private fun policy() = ImageMemoryPolicy.calculate(4L * 1024 * mib, 0, (128 * mib + 32 * mib) * 3, 0, true)

    private fun withLanguage(tag: String, check: (Activity) -> Unit) {
        val preferences = context.getSharedPreferences("app-language", Context.MODE_PRIVATE)
        val previousTag = preferences.getString("language-tag", null)
        val previousInitialized = if (preferences.contains("platform-initialized"))
            preferences.getBoolean("platform-initialized", false) else null
        val previousResources = PaintApplication.currentResources
        val previousLocale = Locale.getDefault()
        val manager = context.getSystemService(LocaleManager::class.java)!!
        val previousPlatform = manager.applicationLocales
        val controller = Robolectric.buildActivity(Activity::class.java)
        try {
            AppLanguage.select(context, tag)
            val activity = controller.setup().get()
            AppLanguage.refresh(activity)
            idle()
            assertEquals(tag, AppLanguage.selectedTag(activity))
            assertEquals(Locale.forLanguageTag(tag), activity.resources.configuration.locales[0])
            check(activity)
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
            idle()
            if (!controller.get().isDestroyed) controller.pause().stop().destroy()
            manager.applicationLocales = previousPlatform
            preferences.edit().apply {
                if (previousTag == null) remove("language-tag") else putString("language-tag", previousTag)
                if (previousInitialized == null) remove("platform-initialized")
                else putBoolean("platform-initialized", previousInitialized)
            }.commit()
            PaintApplication.currentResources = previousResources
            Locale.setDefault(previousLocale)
        }
    }

    private fun explanation(dialog: AlertDialog) =
        dialog.window!!.decorView.findViewWithTag<TextView>("resize_explanation").text.toString()

    @Test fun compiledCompleteValuesReachTheSampledDialogAcrossEditCancelAndReopen() {
        for (tag in listOf("bo", "jje")) withLanguage(tag) { activity ->
            val value = if (tag == "bo") activity.getString(R.string.ui_sampled_resize_memory_explanation) else historicalExpected.getString(tag)
            if (tag != "bo") assertEquals(tag, value, activity.getString(R.string.ui_sampled_resize_memory_explanation))
            var resized = 0
            var cancelled = 0
            repeat(2) { attempt ->
                val dialog = ImageResizeDialog(activity, ImageDimensions(4000, 3000), 0, { policy() },
                    resize = { resized++ }, cancel = { cancelled++ }).show()
                idle()
                assertTrue(dialog.isShowing)
                assertEquals(tag, value, explanation(dialog))
                val width = dialog.window!!.decorView.findViewWithTag<EditText>("resize_width")
                width.setText("0")
                assertFalse(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
                assertEquals(value, explanation(dialog))
                width.setText("400")
                assertTrue(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
                assertEquals(value, explanation(dialog))
                if (attempt == 0) dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
                else dialog.cancel()
                idle()
                assertFalse(dialog.isShowing)
                assertEquals(attempt + 1, cancelled)
                assertEquals(0, resized)
            }
        }
    }

    @Test fun nativeMemoryKeepsItsOwnFloorWarningAndBlocksImpossibleResize() {
        for (tag in listOf("bo", "jje")) withLanguage(tag) { activity ->
            var resized = false
            var cancelled = 0
            val source = ImageDimensions(40000, 40000)
            val native = ImportMemoryRequirements(source.pixels * 32 + 32 * mib + 4)
            val dialog = ImageResizeDialog(activity, source, 0, { policy() },
                resize = { resized = true }, cancel = { cancelled++ }, memoryRequirements = native).show()
            idle()
            assertEquals(activity.getString(R.string.ui_codec_resize_memory_floor), explanation(dialog))
            assertNotEquals(activity.getString(R.string.ui_sampled_resize_memory_explanation), explanation(dialog))
            assertFalse(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            idle()
            assertTrue(dialog.isShowing)
            assertFalse(resized)
            dialog.cancel()
            idle()
            assertEquals(1, cancelled)
        }
    }
}
