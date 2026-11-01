/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.ContextWrapper
import android.content.res.Resources
import android.graphics.Bitmap
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.CheckBox
import android.widget.EditText
import android.widget.TextView
import android.widget.Spinner
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
import java.io.ByteArrayOutputStream
import java.io.File
import java.util.Base64
import java.util.Locale
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

/** Bounded compiled-resource and actual-consumer checks, not installed UI/fluency certification. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class NorthKoreanAustralianPriorityWordingTest {
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
        previousResources = PaintApplication.currentResources
        previousLocale = Locale.getDefault()
        previousTag = AppLanguage.selectedTag(RuntimeEnvironment.getApplication())
    }
    @After fun restoreLanguage() {
        AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
    }
    private fun forEachLocale(tags: List<String> = listOf("ko-KP","en-AU"), check: (String,Activity)->Unit) =
        PriorityWordingExpectations.forEachLocale(
            tags, previousResources, previousLocale, previousTag, check)

    @Test fun completeCropPluralAndAccessiblePreviewTrackActualSelectionCounts() = forEachLocale { tag,activity ->
        val images=(1..3).map {i->AssemblyImage("image$i",File(activity.cacheDir,"$tag-$i.image"),"$i.png",null,ImageDimensions(24,16))}
        var applied=false
        val shown=ImageCropDialog(activity,images,{null}) {applied=true}.show()
        try {
            val root=shown.window!!.decorView;shadowOf(Looper.getMainLooper()).idle()
            assertEquals(expected(tag,"ui_image_shown_in_crop_preview"),root.findViewWithTag<View>("crop_preview_image").contentDescription.toString())
            fun check(count: Int) {
                val text=activity.resources.getQuantityString(R.plurals.ui_crop_preview_images,count,24,16,count)
                assertEquals(text,root.findViewWithTag<TextView>("crop_status").text.toString())
            }
            check(3);root.findViewWithTag<View>("crop_none").performClick();check(0)
            root.findViewWithTag<CheckBox>("crop_include_image1").isChecked=true;check(1)
            root.findViewWithTag<CheckBox>("crop_include_image2").isChecked=true;check(2)
            shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertFalse(applied);assertFalse(shown.isShowing)
            images.forEach {assertEquals(android.graphics.Rect(0,0,24,16),it.crop)}
        } finally {shown.dismiss()}
    }

    @Test fun textAlignmentCaptionsCommitTheirActualLeftAndRightIndices() = forEachLocale { tag,activity ->
        for(index in listOf(0,2)) {
            var committed: TextSettings?=null
            val shown=TextStyleDialog(activity,TextSettings("Text 100%"),android.graphics.Color.BLACK,android.graphics.Color.WHITE) {value,_->committed=value;true}.show()
            try {
                val spinner=shown.window!!.decorView.findViewWithTag<Spinner>("text_alignment")
                assertEquals(expected(tag,"ui_text_alignment"),spinner.contentDescription.toString())
                assertEquals(expected(tag,"ui_left_aligned"),spinner.getItemAtPosition(0).toString())
                assertEquals(expected(tag,"ui_centred"),spinner.getItemAtPosition(1).toString())
                assertEquals(expected(tag,"ui_right_aligned"),spinner.getItemAtPosition(2).toString())
                spinner.setSelection(index);shadowOf(Looper.getMainLooper()).idle()
                shown.getButton(AlertDialog.BUTTON_POSITIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
                assertEquals(index,checkNotNull(committed).alignment);assertEquals("Text 100%",checkNotNull(committed).text)
            } finally {shown.dismiss()}
        }
    }

    @Test fun qualityLosslessAndDitherRemainCoherentAcrossRealFormatChangesAndCancel() = forEachLocale { tag,activity ->
        var confirmed=false;var cancelled=0
        val shown=SaveOptionsDialog(activity,ExportOptions(),share=false,confirm={confirmed=true},cancel={cancelled++}).show()
        try {
            val root=shown.window!!.decorView
            val selector=root.findViewWithTag<Spinner>("export_format")
            val quality=root.findViewWithTag<NumericSlider>("export_quality")
            val dither=root.findViewWithTag<CheckBox>("export_dither")
            val lossless=root.findViewWithTag<CheckBox>("export_lossless")
            val description=root.findViewWithTag<TextView>("export_description")
            assertEquals(expected(tag,"ui_quality"),quality.name)
            assertEquals(expected(tag,"ui_quality"),quality.slider.contentDescription.toString())
            EditorTestNavigation.format(selector,ImageFormat.GIF)
            assertEquals(View.VISIBLE,dither.visibility);assertEquals(expected(tag,"save20_dither"),dither.text.toString())
            assertEquals(expected(tag,"save20_gif_description"),description.text.toString())
            EditorTestNavigation.format(selector,ImageFormat.JPEG_XL)
            assertEquals(View.GONE,dither.visibility);assertEquals(formatted(tag,"ui_lossless_format","JPEG XL"),lossless.text.toString())
            assertEquals(expected(tag,"ui_higher_quality_usually_makes_a_larger_file_lossless"),description.text.toString())
            assertTrue(lossless.isChecked);lossless.performClick();shadowOf(Looper.getMainLooper()).idle()
            assertEquals(View.VISIBLE,quality.visibility)
            shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertFalse(confirmed);assertEquals(1,cancelled);assertFalse(shown.isShowing)
        } finally {shown.dismiss()}
    }
    private fun forEachEditor(check: (String,ClassicPaintActivity)->Unit) {
        for(tag in listOf("ko-KP","en-AU")) {
            val app=RuntimeEnvironment.getApplication() as Context
            app.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {it.delete()}
            app.getSharedPreferences("classic-ui",0).edit().clear().commit()
            AppLanguage.select(app,tag)
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java)
            val activity=controller.setup().get()
            try {
                awaitEditorStartup(activity);shadowOf(Looper.getMainLooper()).idle()
                activity.document.newImage(24,16)
                check(tag,activity)
            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss();controller.pause().stop()
                val end=System.nanoTime()+15_000_000_000L
                while(activity.busy && System.nanoTime()<end) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(10)}
                assertFalse(activity.busy);controller.destroy()
            }
        }
    }

    @Test fun returnToDrawingRestoresThePreviousToolWithoutRedrawing() = forEachEditor { tag,activity ->
        EditorTestNavigation.click(activity,"tool_BRUSH")
        val bitmap=activity.document.bitmap.copy(Bitmap.Config.ARGB_8888,false)
        val dirty=activity.document.dirty;val history=activity.document.historySnapshot()
        try {repeat(2) {
            EditorTestNavigation.click(activity,"tool_ZOOM")
            assertEquals(PaintTool.ZOOM,activity.paintCanvas.tool)
            val control=activity.window.decorView.findViewWithTag<TextView>("navigate_draw")
            assertEquals(expected(tag,"ui_draw_again"),control.text.toString())
            EditorTestNavigation.click(activity,"navigate_draw")
            assertEquals(PaintTool.BRUSH,activity.paintCanvas.tool);assertTrue(bitmap.sameAs(activity.document.bitmap))
            assertEquals(dirty,activity.document.dirty);assertEquals(history,activity.document.historySnapshot())
        }} finally {bitmap.recycle()}
    }

    @Test fun keepEditingCancelsActualReplacementAndPreservesDirtyPixelsAndHistory() = forEachEditor { tag,activity ->
        activity.document.invert();activity.paintCanvas.fit()
        val bitmap=activity.document.bitmap.copy(Bitmap.Config.ARGB_8888,false)
        val history=activity.document.historySnapshot()
        assertTrue(activity.document.dirty)
        try {repeat(2) {
            EditorTestNavigation.command(activity,"File",0)
            val shown=checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
            assertEquals(expected(tag,"ui_save_your_changes"),shadowOf(shown).title.toString())
            assertEquals(expected(tag,"ui_your_current_image_has_unsaved_changes"),shadowOf(shown).message.toString())
            assertEquals(expected(tag,"ui_save_a5d0d9"),shown.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
            assertEquals(expected(tag,"ui_discard_changes23"),shown.getButton(AlertDialog.BUTTON_NEUTRAL).text.toString())
            assertEquals(expected(tag,"ui_keep_editing23"),shown.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
            shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();EditorTestNavigation.idle()
            assertFalse(shown.isShowing);assertFalse(activity.isFinishing)
            assertTrue(activity.document.dirty);assertTrue(bitmap.sameAs(activity.document.bitmap))
            assertEquals(history,activity.document.historySnapshot())
            assertNull(shadowOf(activity).nextStartedActivityForResult)
        }} finally {bitmap.recycle()}
    }

    @Test fun swapColourCommandExchangesExactlyForegroundAndBackgroundWithoutEditingPixels() = forEachEditor { tag,activity ->
        val fg=android.graphics.Color.MAGENTA;val bg=android.graphics.Color.CYAN
        activity.document.foreground=fg;activity.document.background=bg
        val bitmap=activity.document.bitmap.copy(Bitmap.Config.ARGB_8888,false)
        val dirty=activity.document.dirty;val history=activity.document.historySnapshot()
        try {
            val control=activity.window.decorView.findViewWithTag<TextView>("swap_colours")
            assertEquals(expected(tag,"ui_swap23"),control.text.toString())
            EditorTestNavigation.click(activity,"swap_colours")
            assertEquals(bg,activity.document.foreground);assertEquals(fg,activity.document.background)
            EditorTestNavigation.click(activity,"swap_colours")
            assertEquals(fg,activity.document.foreground);assertEquals(bg,activity.document.background)
            assertTrue(bitmap.sameAs(activity.document.bitmap));assertEquals(dirty,activity.document.dirty)
            assertEquals(history,activity.document.historySnapshot())
        } finally {bitmap.recycle()}
    }

    @Test fun commitSelectionKeepsRealUndoRedoAndRestoresEveryPixel() = forEachEditor { tag,activity ->
        EditorTestNavigation.click(activity,"tool_SELECT")
        val before=activity.document.bitmap.copy(Bitmap.Config.ARGB_8888,false)
        val inserted=Bitmap.createBitmap(4,4,Bitmap.Config.ARGB_8888).apply {eraseColor(android.graphics.Color.MAGENTA)}
        var committed: Bitmap?=null
        try {
            assertTrue(activity.document.paste(inserted))
            assertNotNull(activity.document.selection);assertTrue(activity.document.canUndo)
            val apply=activity.window.decorView.findViewWithTag<TextView>("apply")
            assertEquals(expected(tag,"ui_commit_selection"),apply.text.toString())
            EditorTestNavigation.click(activity,"apply")
            assertNull(activity.document.selection);assertTrue(activity.document.canUndo)
            assertEquals(android.graphics.Color.MAGENTA,activity.document.bitmap.getPixel(1,1))
            committed=activity.document.bitmap.copy(Bitmap.Config.ARGB_8888,false)
            assertEquals(expected(tag,"ui_undo"),activity.window.decorView.findViewWithTag<View>("undo").contentDescription.toString())
            EditorTestNavigation.click(activity,"undo")
            assertTrue(before.sameAs(activity.document.bitmap));assertTrue(activity.document.canRedo)
            assertEquals(expected(tag,"ui_redo"),activity.window.decorView.findViewWithTag<View>("redo").contentDescription.toString())
            EditorTestNavigation.click(activity,"redo")
            assertTrue(checkNotNull(committed).sameAs(activity.document.bitmap));assertTrue(activity.document.canUndo)
        } finally {before.recycle();inserted.recycle();committed?.recycle()}
    }

}
