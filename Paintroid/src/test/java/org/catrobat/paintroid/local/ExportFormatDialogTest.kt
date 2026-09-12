/* AN Paint, 2026-09-12. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.os.Looper
import android.view.View
import android.widget.CheckBox
import android.widget.EditText
import android.widget.Spinner
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.ExportOptions
import org.catrobat.paintroid.classic.ImageFormat
import org.catrobat.paintroid.classic.NumericSlider
import org.catrobat.paintroid.classic.SaveOptionsDialog
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
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
import org.robolectric.shadows.ShadowPopupMenu

/** Checks UI choices and the resulting Android document-picker contract. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ExportFormatDialogTest {
    private lateinit var controller: ActivityController<ClassicPaintActivity>
    private lateinit var activity: ClassicPaintActivity
    private fun idle() = shadowOf(Looper.getMainLooper()).idle()
    @Before fun start() {
        val context = RuntimeEnvironment.getApplication() as Context
        context.filesDir.listFiles()?.filter { it.name.startsWith("classic-") }?.forEach { it.delete() }
        listOf("classic-ui", "export").forEach { context.getSharedPreferences(it, 0).edit().clear().commit() }
        create()
    }
    private fun create(state: Bundle? = null) {
        controller = Robolectric.buildActivity(ClassicPaintActivity::class.java)
        activity = controller.create(state).start().resume().visible().get()
        activity.document.newImage(64, 48)
        idle()
    }
    private fun close() {
        controller.pause().stop()
        val until = System.nanoTime() + 10_000_000_000
        while (activity.busy && System.nanoTime() < until) { idle(); Thread.sleep(10) }
        assertFalse(activity.busy)
        controller.destroy()
    }
    @After fun stop() = close()
    private fun menu(label: String) {
        assertTrue(activity.window.decorView.findViewWithTag<View>("menu_File").performClick())
        idle()
        val menu = ShadowPopupMenu.getLatestPopupMenu().menu
        val item = (0 until menu.size()).map { menu.getItem(it) }.single { it.title.toString() == label }
        assertTrue(menu.performIdentifierAction(item.itemId, 0))
        idle()
    }
    private fun AlertDialog.confirm() { getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle() }
    private fun AlertDialog.lossless() = window!!.decorView.findViewWithTag<CheckBox>("export_lossless")
    private fun AlertDialog.quality() = window!!.decorView.findViewWithTag<NumericSlider>("export_quality")
    private fun AlertDialog.format() = window!!.decorView.findViewWithTag<Spinner>("export_format")

    @Test fun everyFileSaveCommandOpensThePickerWithItsActualMimeTypeAndFileExtension() {
        val formats = listOf(
            Triple("PNG", "image/png", ".png"), Triple("JPEG", "image/jpeg", ".jpg"),
            Triple("JPEG XL", "image/jxl", ".jxl"), Triple("WebP", "image/webp", ".webp"),
            Triple("HEIC", "image/heic", ".heic"), Triple("AVIF", "image/avif", ".avif")
        )
        for ((label, mime, extension) in formats) {
            menu("Save as $label…")
            if (label != "PNG") (ShadowAlertDialog.getLatestAlertDialog() as AlertDialog).confirm()
            val launch = shadowOf(activity).nextStartedActivityForResult
            assertNotNull(label, launch)
            assertEquals(label, Intent.ACTION_CREATE_DOCUMENT, launch.intent.action)
            assertEquals(label, mime, launch.intent.type)
            assertTrue(label, launch.intent.getStringExtra(Intent.EXTRA_TITLE)!!.endsWith(extension))
            assertTrue(launch.intent.hasCategory(Intent.CATEGORY_OPENABLE))
            // Cancelling the picker must not start encoding or sharing.
            shadowOf(activity).nextStartedActivity
            activity.onActivityResult(launch.requestCode, Activity.RESULT_CANCELED, null)
            idle()
            assertFalse(activity.busy)
            assertNull(shadowOf(activity).nextStartedActivity)
        }
    }

    @Test fun losslessFormatsToggleQualityAndRetainTheChosenLossyQuality() {
        for (format in listOf(ImageFormat.JPEG_XL, ImageFormat.WEBP, ImageFormat.AVIF)) {
            var selected: ExportOptions? = null
            val dialog = SaveOptionsDialog(activity, ExportOptions(format, 83, true),
                confirm = { selected = it }, cancel = { fail("Unexpected cancellation") }).show()
            idle()
            assertEquals(View.VISIBLE, dialog.lossless().visibility)
            assertTrue(dialog.lossless().isChecked)
            assertEquals(View.GONE, dialog.quality().visibility)
            dialog.lossless().performClick()
            assertEquals(View.VISIBLE, dialog.quality().visibility)
            dialog.quality().slider.progress = 26
            dialog.lossless().performClick()
            assertEquals(View.GONE, dialog.quality().visibility)
            dialog.lossless().performClick()
            assertEquals(26, dialog.quality().slider.progress)
            dialog.confirm()
            assertEquals(ExportOptions(format, 27, false), selected)
            val losslessDialog = SaveOptionsDialog(activity, selected!!,
                confirm = { selected = it }, cancel = { fail("Unexpected cancellation") }).show()
            idle()
            losslessDialog.lossless().performClick()
            assertEquals(View.GONE, losslessDialog.quality().visibility)
            losslessDialog.confirm()
            assertEquals(ExportOptions(format, 27, true), selected)
        }
    }

    @Test fun changingFromLosslessWebpToHeicShowsNumericQualityAndNeverClaimsLosslessHeic() {
        var selected: ExportOptions? = null
        val dialog = SaveOptionsDialog(activity, ExportOptions(ImageFormat.WEBP, 95, true), true,
            confirm = { selected = it }, cancel = { fail("Unexpected cancellation") }).show()
        idle()
        dialog.format().setSelection(ImageFormat.HEIC.ordinal)
        idle()
        assertEquals(View.GONE, dialog.lossless().visibility)
        assertEquals(View.VISIBLE, dialog.quality().visibility)
        assertTrue(dialog.quality().number.performClick())
        // Dialog dispatches OnShow through the main looper. Let the numeric
        // validator replace the default positive listener before the next tap.
        idle()
        val numberDialog = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        val number = numberDialog.window!!.decorView.findViewWithTag<EditText>("numeric_input")
        number.setText("101")
        numberDialog.confirm()
        assertTrue(numberDialog.isShowing)
        assertNotNull(number.error)
        number.setText("38")
        numberDialog.confirm()
        assertFalse(numberDialog.isShowing)
        dialog.confirm()
        assertEquals(ExportOptions(ImageFormat.HEIC, 38, false), selected)
    }

    @Test fun pngHidesQualityAndJpegKeepsItWithoutOfferingLossless() {
        var selected: ExportOptions? = null
        val dialog = SaveOptionsDialog(activity, ExportOptions(ImageFormat.JPEG, 74, true), true,
            confirm = { selected = it }, cancel = { fail("Unexpected cancellation") }).show()
        idle()
        assertEquals(View.GONE, dialog.lossless().visibility)
        assertEquals(View.VISIBLE, dialog.quality().visibility)
        dialog.format().setSelection(ImageFormat.PNG.ordinal)
        idle()
        assertEquals(View.GONE, dialog.lossless().visibility)
        assertEquals(View.GONE, dialog.quality().visibility)
        dialog.format().setSelection(ImageFormat.JPEG.ordinal)
        idle()
        assertEquals(73, dialog.quality().slider.progress)
        dialog.confirm()
        assertEquals(ExportOptions(ImageFormat.JPEG, 74, false), selected)
    }

    @Test fun originalSavedFormatNumbersStillOpenTheCorrespondingShareDialogChoice() {
        // These are the original local.16 saved-state values, deliberately not
        // derived from current enum ordinals. New formats must be appended.
        for ((savedNumber, label) in listOf(0 to "PNG", 1 to "JPEG", 2 to "JPEG XL")) {
            close()
            create(Bundle().apply { putInt("export_format", savedNumber) })
            menu("Save and share…")
            val dialog = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            assertEquals(label, dialog.format().selectedItem.toString())
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
            idle()
            assertNull(shadowOf(activity).nextStartedActivityForResult)
        }
    }
}
