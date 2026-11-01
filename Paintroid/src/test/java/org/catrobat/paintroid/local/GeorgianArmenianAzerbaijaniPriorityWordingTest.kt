/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.graphics.Bitmap
import android.app.Activity
import android.app.AlertDialog
import android.content.res.Resources
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.CheckBox
import android.widget.EditText
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
import org.robolectric.shadows.ShadowAlertDialog
import java.io.ByteArrayOutputStream
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import java.io.File
import java.io.IOException
import java.util.Base64
import java.util.Locale

/** Exact compiled resources and real consumers; not installed UI or native-reader certification. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class GeorgianArmenianAzerbaijaniPriorityWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    // Current compiled labels are the oracle for control binding, not approval history.
    private fun expected(tag: String, key: String) = PriorityWordingExpectations.resourceText(tag,key)
    private fun formatted(tag: String, key: String, vararg args: Any) =
        String.format(Locale.forLanguageTag(tag),expected(tag,key),*args)
    private fun cropText(tag: String,count: Int,width: Int=24,height: Int=16) =
        PriorityWordingExpectations.resources(tag).getQuantityString(R.plurals.ui_crop_preview_images,count,width,height,count)
    private fun idle() = shadowOf(Looper.getMainLooper()).idle()

    @Before fun rememberLanguage() {
        previousResources=PaintApplication.currentResources;previousLocale=Locale.getDefault()
        previousTag=AppLanguage.selectedTag(RuntimeEnvironment.getApplication())
    }
    @After fun restoreLanguage() {
        AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
        PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
    }
    private fun forEachLocale(tags: List<String> = listOf("ka","hy","az"),check: (String,Activity)->Unit) {
        for(tag in tags) {
            val controller=Robolectric.buildActivity(Activity::class.java)
            val activity=controller.get();activity.setTheme(R.style.ClassicPaintTheme);controller.setup()
            try {
                AppLanguage.select(activity,tag);AppLanguage.refresh(activity)
                assertEquals(tag,AppLanguage.selectedTag(activity))
                Locale.setDefault(Locale.US)
                check(tag,activity)
            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
                AppLanguage.select(activity,previousTag);AppLanguage.refresh(activity)
                controller.pause().stop().destroy()
                PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
            }
        }
    }
    private fun allText(view: View): List<String> {
        val result=mutableListOf<String>()
        if(view is TextView)result.add(view.text.toString())
        if(view is ViewGroup)for(i in 0 until view.childCount)result.addAll(allText(view.getChildAt(i)))
        return result
    }

    @Test fun actualDimensionControlsHandleOneTwoGroupedCountsAndRepeatedUnitChanges() = forEachLocale { tag,activity ->
        val controls=DimensionControls(activity,ImageDimensions(1,1),locked=false)
        val result=controls.findViewWithTag<TextView>("size_result")
        assertEquals(formatted(tag,"ui_d_d_px_d_pixels_2f_mp",1,1,1L,0.0),result.text.toString())
        controls.setDimensions(ImageDimensions(2,1))
        assertEquals(formatted(tag,"ui_d_d_px_d_pixels_2f_mp",2,1,2L,0.0),result.text.toString())
        for(size in listOf(ImageDimensions(40,25),ImageDimensions(2000,1000))) {
            controls.setDimensions(size)
            assertEquals(formatted(tag,"ui_d_d_px_d_pixels_2f_mp",size.width,size.height,size.pixels,size.pixels/1_000_000.0),result.text.toString())
        }
        for(percent in listOf(false,true,false)) {
            controls.findViewWithTag<View>(if(percent) "size_percent" else "size_pixels").performClick()
            val unit=expected(tag,if(percent) "ui_percent_fd8671" else "ui_pixels_6ec9c2")
            assertEquals(formatted(tag,"ui_width_in",unit),controls.widthInput.contentDescription.toString())
            assertEquals(formatted(tag,"ui_height_in",unit),controls.heightInput.contentDescription.toString())
            assertEquals(expected(tag,"ui_percent"),controls.findViewWithTag<TextView>("size_percent").text.toString())
            assertEquals(ImageDimensions(2000,1000),controls.dimensions)
        }
        controls.widthInput.setText("")
        assertNull(controls.dimensions)
        assertEquals(expected(tag,"ui_enter_positive_dimensions_that_resolve_to_at_least"),result.text.toString())
    }

    @Test fun completedDecodedImageCannotReplaceBlockedDestinationAndLeavesBothSourcesUntouched() = forEachLocale { tag,activity ->
        val folder=File(activity.cacheDir,"$tag-destination-${System.nanoTime()}").apply { mkdirs() }
        val bytes=Base64.getDecoder().decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j4Z0AAAAASUVORK5CYII=")
        val encoded="data:image/png;base64,"+Base64.getEncoder().encodeToString(bytes)
        val input=File(folder,"input.txt").apply { writeText(encoded) }
        // A nonempty directory cannot be atomically replaced by the completed image file.
        val blocked=File(folder,"destination.png").apply { mkdirs() }
        val sentinel=File(blocked,"keep.txt").apply { writeText("existing destination") }
        try {
            val failure=assertThrows(IOException::class.java) { TextImageCodec.decodeToFile(input,blocked,4096) }
            assertEquals(expected(tag,"save20_destination_error"),failure.message)
            assertEquals("existing destination",sentinel.readText())
            assertEquals(encoded,input.readText())
            assertEquals(setOf("input.txt","destination.png"),folder.listFiles()!!.map { it.name }.toSet())
            val completed=File(folder,"completed.png")
            TextImageCodec.decodeToFile(input,completed,4096)
            assertArrayEquals(bytes,completed.readBytes())
            assertEquals(encoded,input.readText())
        } finally { folder.deleteRecursively() }
    }

    @Test fun realExportAndLosslessDialogsKeepCompleteExplanationsAndCancelWithoutSaving() = forEachLocale() { tag,activity ->
        var confirmed=false;var canceled=0
        var dialog=SaveOptionsDialog(activity,ExportOptions(ImageFormat.ASCII_ART),
            confirm={confirmed=true},cancel={canceled++},export=true).show()
        try {
            shadowOf(Looper.getMainLooper()).idle()
            assertTrue(allText(dialog.window!!.decorView).contains(expected(tag,"ui_export_explanation23")))
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertFalse(dialog.isShowing);assertFalse(confirmed);assertEquals(1,canceled)
        } finally { dialog.dismiss() }
        dialog=SaveOptionsDialog(activity,ExportOptions(ImageFormat.WEBP),
            confirm={confirmed=true},cancel={canceled++}).show()
        try {
            shadowOf(Looper.getMainLooper()).idle()
            val root=dialog.window!!.decorView
            val lossless=root.findViewWithTag<CheckBox>("export_lossless")
            assertEquals(formatted(tag,"ui_lossless_format",ImageFormat.WEBP.label),lossless.text.toString())
            val quality=root.findViewWithTag<NumericSlider>("export_quality")
            assertEquals(expected(tag,"ui_quality"),quality.name)
            for(checked in listOf(false,true,false)) {
                lossless.isChecked=checked
                assertEquals(if(checked) View.GONE else View.VISIBLE,quality.visibility)
                assertEquals(expected(tag,"ui_higher_quality_usually_makes_a_larger_file_lossless"),root.findViewWithTag<TextView>("export_description").text.toString())
            }
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertFalse(dialog.isShowing);assertFalse(confirmed);assertEquals(2,canceled)
        } finally { dialog.dismiss() }
    }

    @Test fun actualDirtyImagePromptIsNotExportCompletionAndRepeatedCancelPreservesTheDrawing() {
      for(tag in listOf("ka","hy","az")) {
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
            AppLanguage.select(activity, tag)
            AppLanguage.refresh(activity)
            activity.document.newImage(32, 24)
            activity.document.invert()
            activity.paintCanvas.fit()
            val document = activity.document
            snapshot = document.bitmap.copy(Bitmap.Config.ARGB_8888, false)
            val history = document.historySnapshot()
            val unsaved = expected(tag, "ui_your_current_image_has_unsaved_changes")
            val exported = expected(tag, "ui_export_did_not_save23")
            assertNotEquals(unsaved, exported)
            repeat(2) {
                EditorTestNavigation.command(activity, "File", 0)
                val shown = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
                assertEquals(expected(tag,"ui_save_your_changes"), shadowOf(shown).title.toString())
                val body = shown.findViewById<TextView>(android.R.id.message).text.toString()
                assertEquals(unsaved, body)
                assertNotEquals(exported, body)
                assertEquals(expected(tag,"ui_save_a5d0d9"), shown.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals(expected(tag,"ui_keep_editing23"), shown.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
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
            assertNotEquals(expected(tag,"ui_save_your_changes"), shadowOf(shown).title.toString())
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

    @Test fun gifExplanationAndRetainedDitherControlStayTogetherAcrossRepeatedToggles() = forEachLocale { tag,activity ->
        var confirmed=false;var canceled=0
        val dialog=SaveOptionsDialog(activity,ExportOptions(ImageFormat.GIF),
            confirm={confirmed=true},cancel={canceled++}).show()
        try {
            shadowOf(Looper.getMainLooper()).idle()
            val root=dialog.window!!.decorView
            val dither=root.findViewWithTag<CheckBox>("export_dither")
            assertEquals(View.VISIBLE,dither.visibility)
            assertEquals(expected(tag,"save20_dither"),dither.text.toString())
            for(checked in listOf(false,true,false)) {
                dither.isChecked=checked
                assertEquals(expected(tag,"save20_gif_description"),root.findViewWithTag<TextView>("export_description").text.toString())
            }
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertFalse(confirmed);assertEquals(1,canceled);assertFalse(dialog.isShowing)
        } finally { dialog.dismiss() }
    }
}
