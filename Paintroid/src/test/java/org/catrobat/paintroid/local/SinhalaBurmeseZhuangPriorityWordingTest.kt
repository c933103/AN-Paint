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
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class SinhalaBurmeseZhuangPriorityWordingTest {
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
    private fun forEachLocale(tags: List<String> = listOf("si","my"), check: (String,Activity)->Unit) =
        PriorityWordingExpectations.forEachLocale(
            tags, previousResources, previousLocale, previousTag, check)

    @Test fun cropEdgeHintsAndNoneActionUseActualControlsWithoutApplyingInvalidSelection() = forEachLocale { tag,activity ->
        val images=listOf("one","two").map { id -> AssemblyImage(id,File(activity.cacheDir,"$id.image"),id,null,ImageDimensions(24,16)) }
        var applied=false
        val shown=ImageCropDialog(activity,images,{null}) { applied=true }.show()
        try {
            shadowOf(Looper.getMainLooper()).idle();val root=shown.window!!.decorView
            val edges=mapOf("left" to "ui_left","top" to "ui_top","right" to "ui_right","bottom" to "ui_bottom")
            for(percent in listOf(false,true,false)) {
                root.findViewWithTag<View>(if(percent) "crop_percent" else "crop_pixels").performClick()
                for((edge,key) in edges) assertEquals(formatted(tag,if(percent) "ui_trim_in_percent" else "ui_trim_in_pixels",expected(tag,key)),
                    root.findViewWithTag<EditText>("crop_$edge").contentDescription.toString())
            }
            for((edge,amount) in listOf("left" to 1,"top" to 2,"right" to 3,"bottom" to 4))
                root.findViewWithTag<EditText>("crop_$edge").setText(amount.toString())
            val reset=root.findViewWithTag<TextView>("crop_reset")
            assertEquals(expected(tag,"ui_reset_crop"),reset.text.toString());reset.performClick();idle()
            for(edge in edges.keys) assertEquals("0",root.findViewWithTag<EditText>("crop_$edge").text.toString())
            assertFalse(applied);images.forEach {assertEquals(android.graphics.Rect(0,0,24,16),it.crop)}
            fun cropStatus(count: Int) = activity.resources.getQuantityString(R.plurals.ui_crop_preview_images,count,24,16,count)
            assertEquals(cropStatus(2),root.findViewWithTag<TextView>("crop_status").text.toString())
            val none=root.findViewWithTag<TextView>("crop_none")
            assertEquals(expected(tag,"ui_none"),none.text.toString());none.performClick()
            images.forEach { assertFalse(root.findViewWithTag<CheckBox>("crop_include_${it.id}").isChecked) }
            assertEquals(cropStatus(0),root.findViewWithTag<TextView>("crop_status").text.toString())
            shown.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            assertFalse(applied);assertTrue(shown.isShowing)
            assertEquals(expected(tag,"ui_choose_at_least_one_image"),root.findViewWithTag<TextView>("crop_status").text.toString())
            root.findViewWithTag<View>("crop_all").performClick()
            images.forEach { assertTrue(root.findViewWithTag<CheckBox>("crop_include_${it.id}").isChecked) }
            shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertFalse(shown.isShowing);assertFalse(applied)
            images.forEach { assertEquals(android.graphics.Rect(0,0,24,16),it.crop) }
        } finally { shown.dismiss() }
    }

    @Test fun textAlignmentCaptionsCommitTheirActualLeftAndRightIndices() = forEachLocale { tag,activity ->
        for(index in listOf(0,2)) {
            var committed: TextSettings?=null
            val shown=TextStyleDialog(activity,TextSettings("Text 100%"),android.graphics.Color.BLACK,android.graphics.Color.WHITE) {value,_->committed=value;true}.show()
            try {
                val spinner=shown.window!!.decorView.findViewWithTag<Spinner>("text_alignment")
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
            assertEquals(ui(R.string.ui_quality),quality.name)
            assertEquals(ui(R.string.ui_quality),quality.slider.contentDescription.toString())
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

    @Test fun keepEditingCancelsRepeatedActualReplacementWithoutSavingDiscardingOrLaunching() {
        for(tag in listOf("si","my")) {
            AppLanguage.select(RuntimeEnvironment.getApplication(),tag)
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);val activity=controller.get()
            try {
                controller.setup();awaitEditorStartup(activity);Locale.setDefault(Locale.US)
                activity.document.newImage(4,3);activity.document.invert();activity.paintCanvas.fit()
                val bitmap=activity.document.bitmap.copy(android.graphics.Bitmap.Config.ARGB_8888,false)
                val history=activity.document.historySnapshot()
                try {repeat(2) {
                    assertTrue(activity.document.dirty)
                    EditorTestNavigation.command(activity,"File",0)
                    val shown=checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
                    assertEquals(expected(tag,"ui_save_your_changes"),shadowOf(shown).title.toString())
                    assertEquals(expected(tag,"ui_your_current_image_has_unsaved_changes"),shadowOf(shown).message.toString())
                    assertEquals(expected(tag,"ui_save_a5d0d9"),shown.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                    assertEquals(expected(tag,"ui_discard_changes23"),shown.getButton(AlertDialog.BUTTON_NEUTRAL).text.toString())
                    assertEquals(expected(tag,"ui_keep_editing23"),shown.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
                    shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();idle()
                    assertFalse(shown.isShowing);assertFalse(activity.isFinishing)
                    assertTrue(activity.document.dirty);assertTrue(bitmap.sameAs(activity.document.bitmap))
                    assertEquals(history,activity.document.historySnapshot())
                    assertNull(shadowOf(activity).nextStartedActivityForResult)
                }} finally {bitmap.recycle()}
            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
                controller.pause().stop().destroy();AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
                PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
            }
        }
    }

    @Test fun realFillThresholdAndInteriorShapeChoicePreserveDocumentAndForegroundAlpha() {
        fun descendants(view: View): List<View> = listOf(view) + if(view is ViewGroup)
            (0 until view.childCount).flatMap {descendants(view.getChildAt(it))} else emptyList()
        for(tag in listOf("si","my")) {
            AppLanguage.select(RuntimeEnvironment.getApplication(),tag)
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);val activity=controller.get()
            try {
                controller.setup();awaitEditorStartup(activity);Locale.setDefault(Locale.US)
                activity.document.newImage(4,3);val bitmap=activity.document.bitmap
                EditorTestNavigation.click(activity,"tool_FILL")
                val tolerance=descendants(activity.window.decorView).filterIsInstance<NumericSlider>().single {it.name==expected(tag,"ui_tolerance")}
                assertEquals(expected(tag,"ui_tolerance"),tolerance.slider.contentDescription.toString())
                for(limit in listOf(0,10)) {
                    tolerance.slider.progress=limit-tolerance.minimum;idle()
                    assertEquals(limit.toFloat(),activity.document.tolerance,0f)
                    val sample=Bitmap.createBitmap(3,1,Bitmap.Config.ARGB_8888)
                    try {
                        val near=0xff060800.toInt();val far=0xff070800.toInt()
                        sample.setPixels(intArrayOf(0xff000000.toInt(),near,far),0,3,0,0,3,1)
                        ScanlineFill.fill(sample,0,0,android.graphics.Color.RED,activity.document.tolerance)
                        assertEquals(android.graphics.Color.RED,sample.getPixel(0,0))
                        assertEquals(if(limit==10) android.graphics.Color.RED else near,sample.getPixel(1,0))
                        assertEquals(far,sample.getPixel(2,0))
                    } finally {sample.recycle()}
                }
                activity.document.shapeStyle=0;activity.document.foreground=0x80ff0000.toInt()
                assertEquals(0xffff0000.toInt(),activity.document.foreground) // foreground input is normalized opaque
                EditorTestNavigation.click(activity,"category_INSERT");EditorTestNavigation.click(activity,"tool_RECTANGLE")
                val choice=activity.window.decorView.findViewWithTag<TextView>("tool_option")
                choice.performClick();idle();val shown=checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
                assertEquals(expected(tag,"ui_solid_fill"),shown.listView.adapter.getItem(1).toString())
                assertTrue(shown.listView.performItemClick(null,1,1L));idle()
                assertEquals(1,activity.document.shapeStyle);assertEquals(expected(tag,"ui_solid_fill"),choice.text.toString());assertSame(bitmap,activity.document.bitmap)
                val rendered=Bitmap.createBitmap(4,4,Bitmap.Config.ARGB_8888)
                try {
                    val path=android.graphics.Path().apply {addRect(0f,0f,4f,4f,android.graphics.Path.Direction.CW)}
                    activity.document.drawShape(android.graphics.Canvas(rendered),PaintTool.RECTANGLE,path)
                    assertEquals(0xffff0000.toInt(),rendered.getPixel(2,2))
                    assertEquals(255,android.graphics.Color.alpha(rendered.getPixel(2,2)))
                    assertEquals(0xffff0000.toInt(),activity.document.foreground)
                } finally {rendered.recycle()}
            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss();controller.pause().stop().destroy()
                AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
                PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
            }
        }
    }

}
