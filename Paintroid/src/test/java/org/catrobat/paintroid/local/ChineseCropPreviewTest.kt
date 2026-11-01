/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.app.LocaleManager
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Canvas
import android.graphics.Paint
import android.os.Looper
import android.view.View
import android.widget.CheckBox
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

/** Complete bounded Sinitic crop warnings through the real batch-crop toolbar. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], shadows = [PixelRegionDecoderShadow::class], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ChineseCropPreviewTest {
    private val context get() = RuntimeEnvironment.getApplication() as Context
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

    private fun formatted(activity: AssemblyActivity, count: Int, height: Int = 16) =
        activity.resources.getQuantityString(R.plurals.ui_crop_preview_images, count, 24, height, count)

    @Test fun taiwanWarningSurvivesActualBatchCropSelectionTrimResetCancelAndReopen() =
        checkActualBatchCrop("zh-TW")

    @Test fun chinaWarningSurvivesActualBatchCropSelectionTrimResetCancelAndReopen() =
        checkActualBatchCrop("zh-CN")

    @Test fun cantoneseHanWarningSeparatesSelectedCountFromPlacementAndKeepsDraftReadOnly() =
        checkActualBatchCrop("yue-Hant", withUnplaced = true)

    @Test fun cantoneseJyutpingWarningSeparatesSelectedCountFromPlacementAndKeepsDraftReadOnly() =
        checkActualBatchCrop("yue-Latn", withUnplaced = true)

    @Test fun literaryChineseWarningSeparatesSelectedCountFromPlacementAndKeepsDraftReadOnly() =
        checkActualBatchCrop("lzh-Hant", withUnplaced = true)

    @Test fun taiwaneseHanWarningKeepsPlacedAntecedentAndAlternateGraph() =
        checkActualBatchCrop("nan-Hant-TW", withUnplaced = true)

    @Test fun taiwanesePojWarningKeepsPlacedAntecedentAndCombiningDot() =
        checkActualBatchCrop("nan-Latn-TW", withUnplaced = true)

    private fun checkTaiwaneseGlyphs(status: TextView, tag: String) {
        val paint = Paint(status.paint).apply { color = Color.BLACK }
        // MOE alternate 怹/in retains the referent; API33 lacks preferred 𪜶.
        val sample = if (tag == "nan-Hant-TW") "怹" else "ô͘"
        sample.codePoints().forEach { point ->
            assertTrue("$tag actual status font covers U+${point.toString(16)}",
                paint.hasGlyph(String(Character.toChars(point))))
        }
        val missing = String(Character.toChars(0x10ffff))
        assertFalse(paint.hasGlyph(missing))
        fun raster(text: String): IntArray {
            val bitmap = Bitmap.createBitmap(192, 192, Bitmap.Config.ARGB_8888)
            try {
                Canvas(bitmap).drawText(text, 48f, 112f, paint)
                return IntArray(192 * 192).also { pixels ->
                    bitmap.getPixels(pixels, 0, 192, 0, 0, 192, 192)
                    assertTrue(text, pixels.any { Color.alpha(it) > 0 })
                    for (i in 0 until 192) {
                        assertEquals(text, 0, Color.alpha(pixels[i]))
                        assertEquals(text, 0, Color.alpha(pixels[191 * 192 + i]))
                        assertEquals(text, 0, Color.alpha(pixels[i * 192]))
                        assertEquals(text, 0, Color.alpha(pixels[i * 192 + 191]))
                    }
                }
            } finally { bitmap.recycle() }
        }
        val actual = raster(sample)
        assertFalse("$tag must not draw a missing-glyph box", actual.contentEquals(raster(missing)))
        if (tag == "nan-Latn-TW")
            assertFalse("POJ dot above right must contribute ink", actual.contentEquals(raster("ô")))
    }

    private fun checkActualBatchCrop(tag: String, withUnplaced: Boolean = false) = withLanguage(tag) { activity ->
        val total = if (withUnplaced) 3 else 2
        val initialCount = if (withUnplaced) 1 else total
        val images = (0 until total).map { index ->
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
        // Two images are placed, with a child attached to its parent. An optional
        // third image stays unplaced and is the initial selection: the displayed
        // count describes selected images, independently of placement. Preview
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
        if (tag == "lzh-Hant") assertNotNull(root.findViewWithTag<View>("vertical_dialog"))
        val status = root.findViewWithTag<TextView>("crop_status")
        if (tag.startsWith("nan-")) checkTaiwaneseGlyphs(status, tag)
        fun check(count: Int, height: Int = 16) {
            idle()
            val expected = formatted(activity, count, height)
            assertEquals(tag + "/" + count, expected, status.text.toString())
            if (tag.startsWith("nan-")) {
                val layout = status.layout
                assertNotNull("$tag native status layout", layout)
                assertEquals(expected.length, layout.getLineEnd(layout.lineCount - 1))
                for (line in 0 until layout.lineCount) assertEquals(0, layout.getEllipsisCount(line))
                assertTrue("$tag complete status height", layout.height <=
                    status.height - status.compoundPaddingTop - status.compoundPaddingBottom)
            }
            val accessibility = status.createAccessibilityNodeInfo()
            try { assertEquals(expected, accessibility.text.toString()) }
            finally { accessibility.recycle() }
        }
        check(initialCount)
        root.findViewWithTag<View>("crop_all").performClick(); check(total)
        root.findViewWithTag<View>("crop_none").performClick(); check(0)
        root.findViewWithTag<CheckBox>("crop_include_" + images[0].id).isChecked = true; check(1)
        root.findViewWithTag<View>("crop_all").performClick(); check(total)
        root.findViewWithTag<EditText>("crop_top").setText("4"); check(total, 12)
        root.findViewWithTag<View>("crop_reset").performClick(); check(total)
        dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
        assertFalse(dialog.isShowing)
        assertEquals(before, activity.assembly.images)
        assertEquals(beforeLayout, activity.assembly.layout())
        assertArrayEquals(saved, File(activity.assembly.directory, "project.json").readBytes())
        images.forEachIndexed { index, image -> assertArrayEquals(originals[index], image.file.readBytes()) }
        // Reopening uses the same current complete message, with no retained draft.
        click(activity, "assembly_batch_crop")
        val reopened = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        assertEquals(formatted(activity, initialCount),
            reopened.window!!.decorView.findViewWithTag<TextView>("crop_status").text.toString())
        reopened.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
        assertFalse(reopened.isShowing)
        assertEquals(before, activity.assembly.images)
        assertEquals(beforeLayout, activity.assembly.layout())
        assertArrayEquals(saved, File(activity.assembly.directory, "project.json").readBytes())
        images.forEachIndexed { index, image -> assertArrayEquals(originals[index], image.file.readBytes()) }
    }
}
