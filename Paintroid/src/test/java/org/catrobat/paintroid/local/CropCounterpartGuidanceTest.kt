/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.app.LocaleManager
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Color
import android.os.Looper
import android.view.View
import android.widget.CheckBox
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
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import java.io.File
import java.util.Locale

/** Bounded crop wording and real Help/toolbar consumers; not whole-Help acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], shadows = [PixelRegionDecoderShadow::class], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CropCounterpartGuidanceTest {
    private val context get() = RuntimeEnvironment.getApplication() as Context
    private val expected = JSONObject(javaClass.getResourceAsStream("/crop-counterparts/expected.json")!!
        .bufferedReader(Charsets.UTF_8).use { it.readText() }).getJSONObject("locales")
    private val tags = listOf("de", "es-ES", "it", "pt-PT")
    private fun idle() = shadowOf(Looper.getMainLooper()).idle()

    private fun withLanguage(tag: String, check: (AssemblyActivity) -> Unit) {
        val preferences = context.getSharedPreferences("app-language", Context.MODE_PRIVATE)
        val previousTag = preferences.getString("language-tag", null)
        val previousInitialized = if (preferences.contains("platform-initialized"))
            preferences.getBoolean("platform-initialized", false) else null
        val previousResources = PaintApplication.currentResources
        val previousLocale = Locale.getDefault()
        val manager = context.getSystemService(LocaleManager::class.java)!!
        val previousPlatform = manager.applicationLocales
        var controller: ActivityController<AssemblyActivity>? = null
        try {
            File(context.filesDir, "image-assembly").deleteRecursively()
            AppLanguage.select(context, tag)
            val started = Robolectric.buildActivity(AssemblyActivity::class.java)
            controller = started
            val activity = started.setup().get()
            AppLanguage.refresh(activity)
            idle()
            assertEquals(tag, AppLanguage.selectedTag(activity))
            assertEquals(Locale.forLanguageTag(tag), activity.resources.configuration.locales[0])
            check(activity)
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
            controller?.let { if (!it.get().isDestroyed) it.pause().stop().destroy() }
            idle()
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

    private fun click(activity: AssemblyActivity, tag: String) {
        assertTrue(tag, activity.window.decorView.findViewWithTag<View>(tag).performClick())
        idle()
    }

    private fun template(tag: String, count: Int): String = expected.getJSONObject(tag)
        .getJSONObject("crop").getString(if (count == 1) "one" else "other")

    private fun formatted(activity: AssemblyActivity, tag: String, count: Int, height: Int = 16) =
        String.format(activity.resources.configuration.locales[0], template(tag, count), 24, height, count)

    @Test fun compiledResourcesPreserveEveryCompleteHelpAndQuantityValue() {
        for (tag in tags) withLanguage(tag) { activity ->
            assertEquals(tag, expected.getJSONObject(tag).getString("help"),
                activity.getString(R.string.ui_add_up_to_20_images_with_android_s))
            // All four have one/other XML forms. Values outside the app's 20-image
            // cap also guard resource routing; actual interaction is bounded below.
            for (count in listOf(0, 1, 2, 3, 20, 21, 101)) {
                assertEquals(tag + "/" + count, template(tag, count),
                    activity.resources.getQuantityText(R.plurals.ui_crop_preview_images, count).toString())
                assertEquals(tag + "/" + count, formatted(activity, tag, count),
                    activity.resources.getQuantityString(R.plurals.ui_crop_preview_images, count, 24, 16, count))
            }
        }
    }

    @Test fun actualHelpButtonDisplaysTheCompleteSevenParagraphEntry() {
        for (tag in tags) withLanguage(tag) { activity ->
            click(activity, "assembly_help")
            val dialog = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            assertTrue(dialog.isShowing)
            val shown = dialog.findViewById<TextView>(android.R.id.message).text.toString()
            assertEquals(tag, expected.getJSONObject(tag).getString("help"), shown)
            assertEquals(7, shown.split("\n\n").size)
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            idle()
            assertFalse(dialog.isShowing)
            assertTrue(activity.assembly.images.isEmpty())
        }
    }

    @Test fun actualBatchCropToolbarKeepsWholeWarningsAcrossSelectionTrimResetAndCancel() {
        for (tag in tags) withLanguage(tag) { activity ->
            val images = (0 until 2).map { index ->
                val file = File(activity.assembly.directory, "crop-counterpart-$index.png")
                val bitmap = Bitmap.createBitmap(24, 16, Bitmap.Config.ARGB_8888)
                bitmap.eraseColor(if (index == 0) Color.RED else Color.BLUE)
                file.outputStream().use { assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it)) }
                bitmap.recycle()
                AssemblyImage("crop-counterpart-$index", file, "Image $index", null, ImageDimensions(24, 16))
            }
            activity.assembly.add(images)
            val deadline = System.nanoTime() + 15_000_000_000L
            while (activity.busy && System.nanoTime() < deadline) { idle(); Thread.sleep(10) }
            idle()
            assertFalse(activity.lastError, activity.busy)
            assertNull("Synthetic previews must decode successfully", activity.lastError)
            // Both images are placed, and one is attached to the other. Preview
            // warnings describe possible effects without applying any mutation.
            activity.assembly.place(images[0].id, Attachment(null, null))
            activity.assembly.place(images[1].id, Attachment(images[0].id, SnapEdge.RIGHT))
            val before = activity.assembly.images
            val beforeLayout = activity.assembly.layout()
            val saved = File(activity.assembly.directory, "project.json").readBytes()
            val originals = images.map { it.file.readBytes() }
            click(activity, "assembly_batch_crop")
            val dialog = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            val root = dialog.window!!.decorView
            val status = root.findViewWithTag<TextView>("crop_status")
            fun check(count: Int, height: Int = 16) {
                idle()
                assertEquals(tag + "/" + count, formatted(activity, tag, count, height), status.text.toString())
            }
            check(2)
            root.findViewWithTag<View>("crop_none").performClick(); check(0)
            root.findViewWithTag<CheckBox>("crop_include_" + images[0].id).isChecked = true; check(1)
            root.findViewWithTag<View>("crop_all").performClick(); check(2)
            root.findViewWithTag<EditText>("crop_top").setText("4"); check(2, 12)
            root.findViewWithTag<View>("crop_reset").performClick(); check(2)
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
            assertFalse(dialog.isShowing)
            assertEquals(before, activity.assembly.images)
            assertEquals(beforeLayout, activity.assembly.layout())
            assertArrayEquals(saved, File(activity.assembly.directory, "project.json").readBytes())
            images.forEachIndexed { index, image -> assertArrayEquals(originals[index], image.file.readBytes()) }
            // Reopening uses the same current complete message, with no retained draft.
            click(activity, "assembly_batch_crop")
            val reopened = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            assertEquals(formatted(activity, tag, 2),
                reopened.window!!.decorView.findViewWithTag<TextView>("crop_status").text.toString())
            reopened.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
            assertEquals(before, activity.assembly.images)
        }
    }
}
