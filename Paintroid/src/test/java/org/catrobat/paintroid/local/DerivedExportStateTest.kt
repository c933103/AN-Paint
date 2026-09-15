/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.graphics.BitmapFactory
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.os.Looper
import android.view.View
import android.widget.CheckBox
import android.widget.Spinner
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.IcoCodec
import org.catrobat.paintroid.classic.ImageFormat
import org.catrobat.paintroid.classic.NumericSlider
import org.catrobat.paintroid.classic.TextImageCodec
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
import java.io.File

/** Real encoders and picker results exercise the unsaved-work guard through Back > Save. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class DerivedExportStateTest {
    private lateinit var controller: ActivityController<ClassicPaintActivity>
    private lateinit var activity: ClassicPaintActivity
    private fun idle() = shadowOf(Looper.getMainLooper()).idle()
    private fun awaitIo() {
        val deadline = System.nanoTime() + 10_000_000_000
        while (activity.busy && System.nanoTime() < deadline) { idle(); Thread.sleep(10) }
        idle()
        assertFalse("Image I/O did not finish", activity.busy)
        assertNull(activity.lastIoError)
    }
    @Before fun start() {
        val context = RuntimeEnvironment.getApplication() as Context
        context.filesDir.listFiles()?.filter { it.name.startsWith("classic-") }?.forEach { it.delete() }
        listOf("classic-ui", "export").forEach { context.getSharedPreferences(it, 0).edit().clear().commit() }
        create()
    }
    private fun create(state: Bundle? = null) {
        controller = Robolectric.buildActivity(ClassicPaintActivity::class.java)
        activity = controller.create(state).start().resume().visible().get()
        activity.document.newImage(320, 160)
        activity.document.bitmap.eraseColor(Color.BLACK)
        activity.document.bitmap.setPixel(319, 159, Color.MAGENTA)
        activity.document.edited()
        idle()
    }
    private fun close() {
        ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
        controller.pause().stop()
        awaitIo()
        controller.destroy()
    }
    @After fun stop() = close()
    private fun menu(label: String) { EditorTestNavigation.named(activity,"File",label) }
    private fun options(format: ImageFormat): AlertDialog {
        menu(activity.getString(if(!format.isDerivedExport) R.string.save20_title else R.string.ui_export_as23))
        val dialog = checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
        EditorTestNavigation.format(dialog.window!!.decorView.findViewWithTag<Spinner>("export_format"),format); idle()
        return dialog
    }
    private fun rememberOptions(dialog: AlertDialog) {
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle()
        val launch = checkNotNull(shadowOf(activity).nextStartedActivityForResult)
        shadowOf(activity).nextStartedActivity
        activity.onActivityResult(launch.requestCode, Activity.RESULT_CANCELED, null); idle()
    }
    private fun writePickerResult(file: File) {
        EditorTestNavigation.chooseLocationIfShown()
        val launch = checkNotNull(shadowOf(activity).nextStartedActivityForResult)
        assertEquals(Intent.ACTION_CREATE_DOCUMENT, launch.intent.action)
        shadowOf(activity).nextStartedActivity
        activity.onActivityResult(launch.requestCode, Activity.RESULT_OK, Intent().setData(Uri.fromFile(file)))
        awaitIo()
        assertTrue("The export must really have been written", file.length() > 0)
    }
    private fun title() = activity.window.decorView.findViewWithTag<TextView>("document_title").text.toString()

    private fun derivedExportKeepsDrawing(format: ImageFormat) {
        val dialog = options(format)
        if (format == ImageFormat.ICO) {
            dialog.window!!.decorView.findViewWithTag<Spinner>("export_ico_size").setSelection(2); idle()
        } else if(format==ImageFormat.ASCII_ART) {
            dialog.window!!.decorView.findViewWithTag<NumericSlider>("export_ascii_columns").slider.progress = 0
        }
        rememberOptions(dialog)
        val bitmap = activity.document.bitmap
        val original = IntArray(bitmap.width * bitmap.height)
        bitmap.getPixels(original, 0, bitmap.width, 0, 0, bitmap.width, bitmap.height)
        val originalTitle = title()
        assertTrue(activity.document.dirty)
        val exporting=options(format)
        exporting.getButton(AlertDialog.BUTTON_POSITIVE).performClick();idle()
        val file = File.createTempFile("derived-state-", format.extension, activity.cacheDir)
        try {
            writePickerResult(file)
            if (format == ImageFormat.ICO) {
                assertTrue(IcoCodec.isIco(file)); assertEquals(32, IcoCodec.dimensions(file).width)
            } else if(format==ImageFormat.BASE64) {
                assertTrue(TextImageCodec.inspect(file))
                TextImageCodec.decodeToFile(file,file,1024*1024)
                val decoded=checkNotNull(BitmapFactory.decodeFile(file.path))
                try {
                    assertEquals(320,decoded.width);assertEquals(160,decoded.height)
                    val recovered=IntArray(original.size);decoded.getPixels(recovered,0,320,0,0,320,160)
                    assertArrayEquals(original,recovered)
                } finally {decoded.recycle()}
            } else {
                val lines = file.readLines()
                assertEquals(10, lines.size); assertTrue(lines.all { it.length == 40 })
            }
            assertFalse("Export must not finish the activity with the full drawing unsaved", activity.isFinishing)
            assertTrue(activity.document.dirty)
            assertSame(bitmap, activity.document.bitmap)
            val actual = IntArray(original.size)
            bitmap.getPixels(actual, 0, 320, 0, 0, 320, 160)
            assertArrayEquals(original, actual)
            assertEquals(originalTitle, title())
            val pending = ClassicPaintActivity::class.java.getDeclaredField("afterSave").apply { isAccessible = true }
            assertNull("The blocked replacement must not run during a later save", pending.get(activity))
        } finally { file.delete() }
    }

    @Test fun icoExportKeepsFullResolutionDrawingAndBlocksPendingClose() = derivedExportKeepsDrawing(ImageFormat.ICO)
    @Test fun asciiExportKeepsOriginalDrawingAndBlocksPendingClose() = derivedExportKeepsDrawing(ImageFormat.ASCII_ART)

    @Test fun base64ExportKeepsOriginalDrawingAndWritesRecoverableImage() = derivedExportKeepsDrawing(ImageFormat.BASE64)

    @Test fun savedAsciiOptionsDriveRealExportAfterActivityRecreationAndIconSizeRemainsAvailable() {
        val dialog = options(ImageFormat.ICO)
        dialog.window!!.decorView.findViewWithTag<Spinner>("export_ico_size").setSelection(3); idle()
        EditorTestNavigation.format(dialog.window!!.decorView.findViewWithTag<Spinner>("export_format"),ImageFormat.ASCII_ART); idle()
        dialog.window!!.decorView.findViewWithTag<NumericSlider>("export_ascii_columns").slider.progress = 80
        dialog.window!!.decorView.findViewWithTag<CheckBox>("export_ascii_invert").isChecked = true
        rememberOptions(dialog)
        val state = Bundle()
        controller.saveInstanceState(state)
        close(); create(state)
        activity.document.bitmap.eraseColor(Color.BLACK); activity.document.edited()
        menu(activity.getString(R.string.ui_export_as23))
        val file = File.createTempFile("restored-ascii-", ".txt", activity.cacheDir)
        try {
            writePickerResult(file)
            val lines = file.readLines()
            assertEquals(30, lines.size)
            assertTrue("Restored width and inversion must affect the exported bytes", lines.all { it == " ".repeat(120) })
            val reopened = options(ImageFormat.ICO)
            assertEquals("48 × 48", reopened.window!!.decorView.findViewWithTag<Spinner>("export_ico_size").selectedItem.toString())
            reopened.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
        } finally { file.delete() }
    }
}
