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
import android.widget.EditText
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
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

/** Complete Traditional Chinese assembly Help and real consumers; not whole-language acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], shadows = [PixelRegionDecoderShadow::class], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class TraditionalChineseAssemblyHelpTest {
    private val context get() = RuntimeEnvironment.getApplication() as Context
    private val tags = listOf("zh-HK", "zh-TW")
    private fun expected(tag: String) = javaClass.getResourceAsStream("/traditional-chinese-assembly-help/$tag.txt")!!
        .bufferedReader(Charsets.UTF_8).use { it.readText() }.removeSuffix("\n")
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
            // Selecting LocaleManager in Robolectric does not dispatch the app callback.
            // Bind the selected UI resources before onCreate builds toolbar labels.
            PaintApplication.currentResources = AppLanguage.wrap(context).resources
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

    @Test fun compiledResourcesPreserveBothCompleteTraditionalChineseEntries() {
        for (tag in tags) withLanguage(tag) { activity ->
            assertEquals(expected(tag), activity.getString(R.string.ui_add_up_to_20_images_with_android_s))
            assertEquals(8, expected(tag).split("\n\n").size)
        }
    }

    @Test @Config(fontScale = 1f)
    fun actualHelpToolbarDisplaysEveryLineAndReopensInPortrait() = checkHelp(1f)

    @Test @Config(fontScale = 2f, qualifiers = "w640dp-h320dp-land-xhdpi")
    fun actualHelpToolbarDisplaysEveryLineAndReopensAtLargeTextInShortLandscape() = checkHelp(2f)

    private fun checkHelp(fontScale: Float) {
        for (tag in tags) withLanguage(tag) { activity ->
            assertEquals(fontScale, activity.resources.configuration.fontScale, 0f)
            repeat(2) {
                click(activity, "assembly_help")
                val dialog = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
                assertTrue(dialog.isShowing)
                val message = dialog.findViewById<TextView>(android.R.id.message)
                assertEquals(expected(tag), message.text.toString())
                val node = message.createAccessibilityNodeInfo()
                assertEquals(expected(tag), node.text.toString())
                node.recycle()
                revealEveryLine(message)
                val done = dialog.getButton(AlertDialog.BUTTON_POSITIVE)
                revealEveryLine(done)
                assertTrue(done.performClick())
                idle()
                assertFalse(dialog.isShowing)
                assertTrue(activity.assembly.images.isEmpty())
            }
        }
    }

    /** Actual native TextView lines and scrolling ancestors, without resizing the dialog. */
    private fun revealEveryLine(view: TextView) {
        val layout = requireNotNull(view.layout)
        val text = view.transformationMethod?.getTransformation(view.text, view)?.toString()
            ?: view.text.toString()
        assertTrue(layout.lineCount > 0)
        assertEquals(text.length, layout.getLineEnd(layout.lineCount - 1))
        assertTrue(layout.height <= view.height - view.totalPaddingTop - view.totalPaddingBottom)
        for (line in 0 until layout.lineCount) {
            assertEquals("Ellipsized line $line", 0, layout.getEllipsisCount(line))
            assertTrue("Horizontal clip on line $line", layout.getLineLeft(line) >= 0f &&
                layout.getLineRight(line) <= layout.width.toFloat())
            val lineRect = Rect(view.totalPaddingLeft, view.totalPaddingTop + layout.getLineTop(line),
                view.width - view.totalPaddingRight, view.totalPaddingTop + layout.getLineBottom(line))
            view.requestRectangleOnScreen(Rect(lineRect), true)
            idle()
            val visible = Rect()
            assertTrue("Line $line invisible", view.getLocalVisibleRect(visible))
            assertTrue("Line $line clipped: $lineRect in $visible", visible.contains(lineRect))
        }
        // Return to the beginning too, after visiting the complete final paragraph.
        val first = Rect(view.totalPaddingLeft, view.totalPaddingTop,
            view.width - view.totalPaddingRight, view.totalPaddingTop + layout.getLineBottom(0))
        view.requestRectangleOnScreen(Rect(first), true)
        idle()
        val visible = Rect()
        assertTrue(view.getLocalVisibleRect(visible))
        assertTrue(visible.contains(first))
    }

    @Test fun hongKongExactPositionAndUnplaceMatchHelp() =
        checkExactPositionAndUnplace("zh-HK", "精確位置", "X 和 Y 必須是 0 至 2147483647 之間的整數。")

    @Test fun taiwanExactPositionAndUnplaceMatchHelp() =
        checkExactPositionAndUnplace("zh-TW", "精確位置", "X 和 Y 必須是 0 到 2147483647 之間的整數。")

    private fun checkExactPositionAndUnplace(
        tag: String, positionLabel: String, invalidMessage: String
    ) = withLanguage(tag) { activity ->
        assertEquals(positionLabel,
            activity.window.decorView.findViewWithTag<TextView>("assembly_position").text.toString())
        assertTrue(expected(tag).contains("「$positionLabel」"))
        assertEquals("取消放置",
            activity.window.decorView.findViewWithTag<TextView>("assembly_unplace").text.toString())
        val images = (0 until 3).map { index ->
            val file = File(activity.assembly.directory, "assembly-help-$index.png")
            val bitmap = Bitmap.createBitmap(24, 16, Bitmap.Config.ARGB_8888)
            bitmap.eraseColor(Color.RED)
            file.outputStream().use { assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it)) }
            bitmap.recycle()
            AssemblyImage("assembly-help-$index", file, "Image $index", null, ImageDimensions(24, 16))
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
            val dialog = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            assertTrue(dialog.isShowing)
            assertEquals(positionLabel, shadowOf(dialog).title.toString())
            val root = dialog.window!!.decorView
            assertEquals("X 座標（距左邊緣的像素數）",
                root.findViewWithTag<EditText>("assembly_position_x").contentDescription.toString())
            assertEquals("Y 座標（距上邊緣的像素數）",
                root.findViewWithTag<EditText>("assembly_position_y").contentDescription.toString())
            return dialog
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
        for ((x, y) in listOf("-1" to "0", "0" to "-1", "1.5" to "0", "0" to "1.5", "2147483648" to "0", "0" to "")) {
            coordinates(invalid, x, y)
            invalid.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle()
            assertTrue("$x,$y", invalid.isShowing)
            assertEquals(invalidMessage,
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

}
