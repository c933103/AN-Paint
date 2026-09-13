/* AN Paint, 2026-09-12. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Canvas
import java.io.File
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
    private fun menu(label: String) { EditorTestNavigation.named(activity,"File",label) }
    private fun AlertDialog.confirm() { getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle() }
    private fun AlertDialog.lossless() = window!!.decorView.findViewWithTag<CheckBox>("export_lossless")
    private fun AlertDialog.quality() = window!!.decorView.findViewWithTag<NumericSlider>("export_quality")
    private fun AlertDialog.format() = window!!.decorView.findViewWithTag<Spinner>("export_format")

    @Test fun oneFileSaveAsPanelChoosesEveryFormatAndUsesTheEditedName() {
        val save=ImageFormat.values().filter {it.canSaveLosslessly}
        val export=ImageFormat.values().filter {it.supportsQuality || it in listOf(ImageFormat.GIF,ImageFormat.ICO,ImageFormat.ASCII_ART)}
        assertEquals(ImageFormat.values().toSet(),(save+export).toSet())
        for((title,formats) in listOf("Save as…" to save,"Export as…" to export)) for(format in formats) {
            menu(title)
            val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            assertEquals(formats.map {it.label},(0 until dialog.format().count).map {dialog.format().getItemAtPosition(it).toString()})
            dialog.window!!.decorView.findViewWithTag<EditText>("export_filename").setText("日曜日 sketch.jpeg")
            EditorTestNavigation.format(dialog.format(),format);dialog.confirm()
            val launch=shadowOf(activity).nextStartedActivityForResult
            assertNotNull(format.label,launch);assertEquals(Intent.ACTION_CREATE_DOCUMENT,launch.intent.action)
            assertEquals(format.mime,launch.intent.type)
            assertEquals("日曜日 sketch"+format.extension,launch.intent.getStringExtra(Intent.EXTRA_TITLE))
            assertTrue(launch.intent.hasCategory(Intent.CATEGORY_OPENABLE))
            shadowOf(activity).nextStartedActivity
            activity.onActivityResult(launch.requestCode,Activity.RESULT_CANCELED,null);idle()
            assertFalse(activity.busy);assertNull(shadowOf(activity).nextStartedActivity)
        }
    }

    @Test fun invalidNamesStayInPanelAndCancellingDoesNotStartThePicker() {
        menu("Save as…")
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        val name=dialog.window!!.decorView.findViewWithTag<EditText>("export_filename")
        for (invalid in listOf("", ".png", "../outside", "folder\\file", "..")) {
            name.setText(invalid);dialog.confirm()
            assertTrue(dialog.isShowing);assertNotNull(name.error)
            assertNull(shadowOf(activity).nextStartedActivityForResult)
        }
        dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();idle()
        assertNull(shadowOf(activity).nextStartedActivityForResult)
        assertFalse(activity.busy)
    }

    @Test fun cancellingDestinationKeepsFloatingSelectionAndPlainSaveUsesLastChosenFormat() {
        val image=Bitmap.createBitmap(7,5,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.RED)}
        try {activity.document.paste(image)} finally {image.recycle()}
        val selection=activity.document.selection
        menu("Export as…")
        var dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        EditorTestNavigation.format(dialog.format(),ImageFormat.GIF);dialog.confirm()
        val launch=shadowOf(activity).nextStartedActivityForResult;shadowOf(activity).nextStartedActivity
        activity.onActivityResult(launch.requestCode,Activity.RESULT_CANCELED,null);idle()
        assertSame(selection,activity.document.selection);assertTrue(selection!!.floating)
        menu(activity.getString(org.catrobat.paintroid.R.string.ui_save))
        dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        assertEquals("PNG",dialog.format().selectedItem.toString())
        dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();idle()
        assertSame(selection,activity.document.selection);assertNull(shadowOf(activity).nextStartedActivityForResult)
    }

    @Test fun bmpHasNoQualityAndGifOffersDitheringInsteadOfFakeLosslessControls() {
        var chosen: ExportOptions?=null
        val bmp=SaveOptionsDialog(activity,ExportOptions(ImageFormat.BMP),confirm={},cancel={}).show();idle()
        assertEquals(View.GONE,bmp.quality().visibility);assertEquals(View.GONE,bmp.lossless().visibility);bmp.dismiss()
        val dialog=SaveOptionsDialog(activity,ExportOptions(ImageFormat.GIF),confirm={chosen=it.options},cancel={},export=true).show();idle()
        val dither=dialog.window!!.decorView.findViewWithTag<CheckBox>("export_dither")
        assertEquals(View.VISIBLE,dither.visibility);assertTrue(dither.isChecked)
        assertEquals(View.GONE,dialog.lossless().visibility);assertEquals(View.GONE,dialog.quality().visibility)
        dither.performClick();dialog.confirm();assertEquals(ExportOptions(ImageFormat.GIF,95,false,false),chosen)
    }

    @Test fun losslessFormatsToggleQualityAndRetainTheChosenLossyQuality() {
        for(format in listOf(ImageFormat.JPEG_XL,ImageFormat.WEBP,ImageFormat.AVIF)) {
            var chosen: ExportOptions?=null
            val save=SaveOptionsDialog(activity,ExportOptions(format,83,false),confirm={chosen=it.options},cancel={}).show();idle()
            assertEquals(View.GONE,save.lossless().visibility);assertEquals(View.GONE,save.quality().visibility)
            save.confirm();assertEquals(ExportOptions(format,83,true),chosen)
            val export=SaveOptionsDialog(activity,ExportOptions(format,83,true),confirm={chosen=it.options},cancel={},export=true).show();idle()
            assertEquals(View.GONE,export.lossless().visibility);assertEquals(View.VISIBLE,export.quality().visibility)
            export.quality().slider.progress=26;export.confirm();assertEquals(ExportOptions(format,27,false),chosen)
        }
    }

    @Test fun tiffCompressionPersistsAcrossDialogChoicesAndDibHasNoLossyControls() {
        menu("Save as…")
        var dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        EditorTestNavigation.format(dialog.format(),ImageFormat.TIFF);idle()
        val compression=dialog.window!!.decorView.findViewWithTag<CheckBox>("export_tiff_compressed")
        assertEquals(View.VISIBLE,compression.visibility);assertTrue(compression.isChecked)
        assertEquals(View.GONE,dialog.lossless().visibility);assertEquals(View.GONE,dialog.quality().visibility)
        compression.performClick()
        EditorTestNavigation.format(dialog.format(),ImageFormat.DIB);idle()
        assertEquals(View.GONE,compression.visibility)
        assertEquals(View.GONE,dialog.lossless().visibility);assertEquals(View.GONE,dialog.quality().visibility)
        EditorTestNavigation.format(dialog.format(),ImageFormat.TIFF);idle()
        assertFalse(compression.isChecked)
        dialog.window!!.decorView.findViewWithTag<EditText>("export_filename").setText("scan.TIFF")
        dialog.confirm()
        var launch=shadowOf(activity).nextStartedActivityForResult
        assertEquals("image/tiff",launch.intent.type)
        assertEquals("scan.tif",launch.intent.getStringExtra(Intent.EXTRA_TITLE))
        shadowOf(activity).nextStartedActivity
        activity.onActivityResult(launch.requestCode,Activity.RESULT_CANCELED,null);idle()
        menu("Save as…")
        dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        EditorTestNavigation.format(dialog.format(),ImageFormat.TIFF)
        assertFalse(dialog.window!!.decorView.findViewWithTag<CheckBox>("export_tiff_compressed").isChecked)
        EditorTestNavigation.format(dialog.format(),ImageFormat.DIB);idle();dialog.confirm()
        launch=shadowOf(activity).nextStartedActivityForResult
        assertEquals("image/x-dib",launch.intent.type)
        assertTrue(launch.intent.getStringExtra(Intent.EXTRA_TITLE)!!.endsWith(".dib"))
        shadowOf(activity).nextStartedActivity
        activity.onActivityResult(launch.requestCode,Activity.RESULT_CANCELED,null);idle()
    }

    @Test fun iconAndAsciiOptionsAreSpecificToTheirFormatAndSurviveReopening() {
        menu("Export as…")
        var dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        EditorTestNavigation.format(dialog.format(),ImageFormat.ICO);idle()
        val icon=dialog.window!!.decorView.findViewWithTag<Spinner>("export_ico_size")
        val iconControls=dialog.window!!.decorView.findViewWithTag<View>("export_ico_controls")
        val asciiControls=dialog.window!!.decorView.findViewWithTag<View>("export_ascii_controls")
        assertEquals(View.VISIBLE,iconControls.visibility);assertEquals(View.GONE,asciiControls.visibility)
        assertEquals(View.GONE,dialog.quality().visibility);icon.setSelection(3);idle()
        EditorTestNavigation.format(dialog.format(),ImageFormat.ASCII_ART);idle()
        assertEquals(View.GONE,iconControls.visibility);assertEquals(View.VISIBLE,asciiControls.visibility)
        val columns=dialog.window!!.decorView.findViewWithTag<NumericSlider>("export_ascii_columns")
        columns.slider.progress=80
        dialog.window!!.decorView.findViewWithTag<CheckBox>("export_ascii_invert").performClick()
        EditorTestNavigation.format(dialog.format(),ImageFormat.JPEG);idle()
        assertEquals(View.GONE,asciiControls.visibility);assertEquals(View.VISIBLE,dialog.quality().visibility)
        dialog.window!!.decorView.findViewWithTag<EditText>("export_filename").setText("Drawing.TXT")
        dialog.confirm()
        val launch=shadowOf(activity).nextStartedActivityForResult
        assertEquals("image/jpeg",launch.intent.type);assertEquals("Drawing.jpg",launch.intent.getStringExtra(Intent.EXTRA_TITLE))
        shadowOf(activity).nextStartedActivity
        activity.onActivityResult(launch.requestCode,Activity.RESULT_CANCELED,null);idle()
        menu("Export as…");dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        EditorTestNavigation.format(dialog.format(),ImageFormat.ICO);idle()
        assertEquals("48 × 48",dialog.window!!.decorView.findViewWithTag<Spinner>("export_ico_size").selectedItem.toString())
        EditorTestNavigation.format(dialog.format(),ImageFormat.ASCII_ART);idle()
        assertEquals(80,dialog.window!!.decorView.findViewWithTag<NumericSlider>("export_ascii_columns").slider.progress)
        assertTrue(dialog.window!!.decorView.findViewWithTag<CheckBox>("export_ascii_invert").isChecked)
        dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();idle()
    }

    @Test fun changingFromLosslessWebpToHeicShowsNumericQualityAndNeverClaimsLosslessHeic() {
        var selected: ExportOptions? = null
        val dialog = SaveOptionsDialog(activity, ExportOptions(ImageFormat.WEBP, 95, true), true,
            confirm = { selected = it.options }, cancel = { fail("Unexpected cancellation") },export=true).show()
        idle()
        EditorTestNavigation.format(dialog.format(),ImageFormat.HEIC)
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
            confirm = { selected = it.options }, cancel = { fail("Unexpected cancellation") },export=true).show()
        idle()
        assertEquals(View.GONE, dialog.lossless().visibility)
        assertEquals(View.VISIBLE, dialog.quality().visibility)
        EditorTestNavigation.format(dialog.format(),ImageFormat.PNG)
        idle()
        assertEquals(View.GONE, dialog.lossless().visibility)
        assertEquals(View.GONE, dialog.quality().visibility)
        EditorTestNavigation.format(dialog.format(),ImageFormat.JPEG)
        idle()
        assertEquals(73, dialog.quality().slider.progress)
        dialog.confirm()
        assertEquals(ExportOptions(ImageFormat.JPEG, 74, false), selected)
    }

    @Test fun portraitSavePanelKeepsFileAndFormatControlsVisible() { renderSavePanel("save-as-portrait.png",760,1640) }

    @Test @Config(qualifiers="w900dp-h412dp-land-xhdpi")
    fun landscapeSavePanelKeepsItsDestinationButtonBelowTheScrollingFields() { renderSavePanel("save-as-landscape.png",1100,680) }

    private fun renderSavePanel(name: String,width: Int,height: Int) {
        val dialog=SaveOptionsDialog(activity,ExportOptions(ImageFormat.JPEG,91,false),
            confirm={},cancel={},initialFilename="Sunday sketch.jpg",export=true).show();idle()
        val view=dialog.window!!.decorView
        view.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.AT_MOST))
        view.layout(0,0,view.measuredWidth,view.measuredHeight)
        val button=dialog.getButton(AlertDialog.BUTTON_POSITIVE)
        assertTrue(button.isShown)
        val bounds=android.graphics.Rect();assertTrue(button.getGlobalVisibleRect(bounds));assertTrue(bounds.height()>0)
        assertTrue(dialog.format().isShown)
        assertTrue(view.findViewWithTag<EditText>("export_filename").isShown)
        val bitmap=Bitmap.createBitmap(view.width,view.height,Bitmap.Config.ARGB_8888)
        try {
            view.draw(Canvas(bitmap))
            val file=File("build/reports/classic-preview",name);file.parentFile.mkdirs()
            file.outputStream().use {assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))}
        } finally {bitmap.recycle();dialog.dismiss()}
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
