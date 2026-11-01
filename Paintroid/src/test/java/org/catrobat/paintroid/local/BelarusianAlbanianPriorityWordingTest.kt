/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import java.util.concurrent.TimeUnit
import java.util.concurrent.Executors
import java.io.ByteArrayOutputStream
import android.content.ContextWrapper
import android.content.Context
import android.app.AlertDialog
import android.content.res.Resources
import android.graphics.Rect
import android.os.Looper
import android.view.View
import android.widget.CheckBox
import android.widget.SeekBar
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
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import java.io.File
import java.io.IOException
import java.util.Base64
import java.util.Locale

/** Compiled complete values and production consumers, not device or native-reader certification. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class BelarusianAlbanianPriorityWordingTest {
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
    private fun forEachLocale(tags: List<String> = listOf("be","sq"),check: (String,Activity)->Unit) {
        for(tag in tags) {
            val controller=Robolectric.buildActivity(Activity::class.java)
            val activity=controller.get();activity.setTheme(R.style.ClassicPaintTheme);controller.setup()
            try {
                AppLanguage.select(activity,tag);AppLanguage.refresh(activity)
                assertEquals(tag,AppLanguage.selectedTag(activity));Locale.setDefault(Locale.US)
                check(tag,activity)
            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
                AppLanguage.select(activity,previousTag);AppLanguage.refresh(activity)
                controller.pause().stop().destroy()
                PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
            }
        }
    }

    @Test fun realCropDialogSelectionCountsAllEdgesAndRepeatedUnitsStayAtomic() = forEachLocale { tag,activity ->
        val images=(0 until 20).map { AssemblyImage("fixture-$it",File(activity.cacheDir,"fixture-$it.image"),"Image $it",null,ImageDimensions(24,16)) }
        var applied=false
        val dialog=ImageCropDialog(activity,images,{null}) {applied=true}.show()
        try {
            idle();val root=dialog.window!!.decorView
            assertEquals(expected(tag,"ui_image_shown_in_crop_preview"),root.findViewWithTag<View>("crop_preview_image").contentDescription.toString())
            assertEquals(expected(tag,"ui_all"),root.findViewWithTag<TextView>("crop_all").text.toString())
            assertEquals(expected(tag,"ui_none"),root.findViewWithTag<TextView>("crop_none").text.toString())
            for(count in listOf(20,0,1,2,3,6,7,10,11,12,19,20)) {
                if(count==0 || count==20) root.findViewWithTag<View>(if(count==0) "crop_none" else "crop_all").performClick()
                else images.forEachIndexed { index,image -> root.findViewWithTag<CheckBox>("crop_include_${image.id}").isChecked=index<count }
                idle();assertEquals(cropText(tag,count),root.findViewWithTag<TextView>("crop_status").text.toString())
            }
            val edges=mapOf("left" to "ui_left","top" to "ui_top","right" to "ui_right","bottom" to "ui_bottom")
            for(percent in listOf(false,true,false)) {
                root.findViewWithTag<View>(if(percent) "crop_percent" else "crop_pixels").performClick()
                for((edge,key) in edges) assertEquals(formatted(tag,if(percent) "ui_trim_in_percent" else "ui_trim_in_pixels",expected(tag,key)),
                    root.findViewWithTag<EditText>("crop_$edge").contentDescription.toString())
                assertEquals(cropText(tag,20),root.findViewWithTag<TextView>("crop_status").text.toString())
            }
            root.findViewWithTag<EditText>("crop_left").setText("2");idle()
            assertEquals(cropText(tag,20,22),root.findViewWithTag<TextView>("crop_status").text.toString())
            root.findViewWithTag<View>("crop_reset").performClick();idle()
            assertEquals(cropText(tag,20),root.findViewWithTag<TextView>("crop_status").text.toString())
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();idle()
            assertFalse(applied);assertFalse(dialog.isShowing)
            assertTrue(images.all {it.crop==Rect(0,0,24,16)})
        } finally {dialog.dismiss()}
    }

    @Test fun zeroBudgetRejectsSingleAndManyPixelsBeforeAllocation() = forEachLocale { tag,_ ->
        val mib=1024L*1024
        val policy=ImageMemoryPolicy.calculate(256*mib,0,96*mib,0,false)
        assertEquals(0L,policy.maxPixels())
        for(size in listOf(ImageDimensions(1,1),ImageDimensions(2,1),ImageDimensions(2000,1000))) {
            val error=assertThrows(ImageSizeException::class.java) {policy.check(size.width,size.height)}
            assertEquals(formatted(tag,"ui_d_d_pixels_2f_mp_exceeds_the_current",size.width,size.height,size.pixels/1_000_000.0,0.0),error.message)
        }
    }

    @Test fun losslessCheckboxAndQualityPercentageControlKeepTheActualSaveRequest() = forEachLocale { tag,activity ->
        var request:SaveRequest?=null;var canceled=false
        val dialog=SaveOptionsDialog(activity,ExportOptions(ImageFormat.WEBP,quality=67,lossless=false),
            confirm={request=it},cancel={canceled=true},initialFilename="fixture.webp").show()
        try {
            idle();val root=dialog.window!!.decorView
            val lossless=root.findViewWithTag<CheckBox>("export_lossless")
            val quality=root.findViewWithTag<NumericSlider>("export_quality")
            assertEquals(formatted(tag,"ui_lossless_format",ImageFormat.WEBP.label),lossless.text.toString())
            assertEquals(expected(tag,"ui_quality"),quality.name)
            assertEquals(expected(tag,"ui_quality"),quality.slider.contentDescription.toString())
            quality.slider.progress=42-quality.minimum;idle()
            for(enabled in listOf(true,false)) {
                lossless.performClick();idle();assertEquals(enabled,lossless.isChecked)
                assertEquals(if(enabled) View.GONE else View.VISIBLE,quality.visibility)
            }
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();idle()
            assertNotNull(request);assertEquals(ImageFormat.WEBP,request!!.options.format)
            assertEquals(42,request!!.options.quality);assertFalse(request!!.options.lossless)
            assertFalse(canceled);assertFalse(dialog.isShowing)
        } finally {dialog.dismiss()}
    }
}
