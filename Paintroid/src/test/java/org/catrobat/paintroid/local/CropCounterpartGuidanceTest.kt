/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.app.LocaleManager
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Rect
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

    @Test fun actualHelpButtonDisplaysTheCompleteCurrentEntry() {
        for (tag in tags) withLanguage(tag) { activity ->
            click(activity, "assembly_help")
            val dialog = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            assertTrue(dialog.isShowing)
            val shown = dialog.findViewById<TextView>(android.R.id.message).text.toString()
            assertEquals(tag, expected.getJSONObject(tag).getString("help"), shown)
            assertEquals(if (tag == "de") 8 else 7, shown.split("\n\n").size)
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            idle()
            assertFalse(dialog.isShowing)
            assertTrue(activity.assembly.images.isEmpty())
        }
    }

    @Test fun germanExactPositionToolbarMatchesHelpAndUnplaceOnlySometimesClosesAGap() = withLanguage("de") { activity ->
        assertEquals("Exakte Position",
            activity.window.decorView.findViewWithTag<TextView>("assembly_position").text.toString())
        val images = (0 until 3).map { index ->
            val file = File(activity.assembly.directory, "german-help-$index.png")
            val bitmap = Bitmap.createBitmap(24, 16, Bitmap.Config.ARGB_8888)
            bitmap.eraseColor(Color.RED)
            file.outputStream().use { assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it)) }
            bitmap.recycle()
            AssemblyImage("german-help-$index", file, "Image $index", null, ImageDimensions(24, 16))
        }
        activity.assembly.add(images)
        val deadline = System.nanoTime() + 15_000_000_000L
        while (activity.busy && System.nanoTime() < deadline) { idle(); Thread.sleep(10) }
        idle()
        assertFalse(activity.lastError, activity.busy)
        assertNull(activity.lastError)
        val first = images[0].id; val child = images[1].id; val last = images[2].id
        fun openPosition(id: String): AlertDialog {
            click(activity, "assembly_item_$id"); click(activity, "assembly_position")
            return ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        }
        fun coordinates(dialog: AlertDialog, x: String, y: String) {
            dialog.window!!.decorView.findViewWithTag<EditText>("assembly_position_x").setText(x)
            dialog.window!!.decorView.findViewWithTag<EditText>("assembly_position_y").setText(y)
        }
        fun position(id: String, x: String, y: String) {
            val dialog = openPosition(id)
            coordinates(dialog, x, y)
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle()
            assertFalse(dialog.isShowing)
        }
        // Exact placement of even the first image is not restricted to the origin.
        position(first, "5", "7")
        assertEquals(Rect(5, 7, 29, 23), activity.assembly.layout()[first])
        activity.assembly.place(child, Attachment(first, SnapEdge.RIGHT))
        activity.assembly.place(last, Attachment(child, SnapEdge.RIGHT)); idle()
        val attached = activity.assembly.layout()
        val saved = File(activity.assembly.directory, "project.json").readBytes()
        val invalid = openPosition(first)
        for ((x, y) in listOf("-1" to "0", "0" to "-1", "1,5" to "0", "0" to "1,5")) {
            coordinates(invalid, x, y)
            invalid.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle()
            assertTrue("$x,$y", invalid.isShowing)
            assertEquals("X und Y müssen ganze Zahlen von 0 bis 2147483647 sein.",
                invalid.window!!.decorView.findViewWithTag<TextView>("assembly_position_error").text.toString())
            assertEquals(attached, activity.assembly.layout())
            assertArrayEquals(saved, File(activity.assembly.directory, "project.json").readBytes())
        }
        coordinates(invalid, "30", "8")
        invalid.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
        assertFalse(invalid.isShowing)
        assertEquals(attached, activity.assembly.layout())
        assertArrayEquals(saved, File(activity.assembly.directory, "project.json").readBytes())
        // Zero is valid; moving the selected anchor preserves every other rectangle.
        position(first, "0", "0")
        assertEquals(attached.toMutableMap().apply { put(first, Rect(0, 0, 24, 16)) }, activity.assembly.layout())
        position(first, "30", "8")
        val moved = attached.toMutableMap().apply { put(first, Rect(30, 8, 54, 24)) }
        assertEquals(moved, activity.assembly.layout())
        assertTrue(Rect.intersects(moved.getValue(first), moved.getValue(child)))
        // An absolute placement leaves a gap when unplaced; the others stay put.
        click(activity, "assembly_unplace")
        assertEquals(moved.filterKeys { it != first }, activity.assembly.layout())
        assertEquals(3, activity.assembly.images.size)
        assertFalse(activity.assembly.image(first).isPlaced)
        // Snapping starts at the origin, rejects overlap, and can close a gap.
        images.forEach { activity.assembly.unplace(it.id) }
        activity.assembly.place(first, Attachment(null, null))
        activity.assembly.place(child, Attachment(first, SnapEdge.RIGHT))
        activity.assembly.place(last, Attachment(child, SnapEdge.RIGHT)); idle()
        val snapped = activity.assembly.layout()
        assertEquals(Rect(0, 0, 24, 16), snapped[first])
        assertThrows(IllegalArgumentException::class.java) {
            activity.assembly.place(last, Attachment(first, SnapEdge.RIGHT))
        }
        assertEquals(snapped, activity.assembly.layout())
        click(activity, "assembly_item_$child"); click(activity, "assembly_unplace")
        assertEquals(Rect(24, 0, 48, 16), activity.assembly.layout()[last])
        assertEquals(2, activity.assembly.layout().size)
        click(activity, "assembly_undo"); assertEquals(snapped, activity.assembly.layout())
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
