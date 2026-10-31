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

    @Test fun nativeWorkingMemoryFloorKeepsCancelAndRejectsAnImpossibleCopy() = forEachLocale { tag,activity ->
        val mib=1024L*1024
        val policy=ImageMemoryPolicy.calculate(256*mib,0,0,0,false)
        var accepted=false;var cancelled=0
        val shown=ImageResizeDialog(activity,ImageDimensions(2000,1000),0,{policy},
            resize={accepted=true},cancel={cancelled++},memoryRequirements=ImportMemoryRequirements(1024*mib)).show()
        try {
            shadowOf(Looper.getMainLooper()).idle();val root=shown.window!!.decorView
            assertTrue(root.findViewWithTag<TextView>("resize_estimate").text.toString().contains(expected(tag,"ui_no_resize_fits_decoder_memory")))
            assertEquals(expected(tag,"ui_codec_resize_memory_floor"),root.findViewWithTag<TextView>("resize_explanation").text.toString())
            assertFalse(shown.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
            assertEquals(expected(tag,"ui_resize_and_load"),shown.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
            shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertFalse(accepted);assertEquals(1,cancelled)
        } finally {shown.dismiss()}
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
    @Test fun gifDescriptionAndCheckboxProduceTheSelectedDitherRequest() = forEachLocale { tag,activity ->
        for(enabled in listOf(false,true,false)) {
            var request: SaveRequest?=null;var canceled=false
            val dialog=SaveOptionsDialog(activity,ExportOptions(ImageFormat.GIF,dither=!enabled),
                confirm={request=it},cancel={canceled=true},initialFilename="fixture.gif").show()
            try {
                idle();val root=dialog.window!!.decorView
                val checkbox=root.findViewWithTag<CheckBox>("export_dither")
                assertEquals(View.VISIBLE,checkbox.visibility);assertEquals(expected(tag,"save20_dither"),checkbox.text.toString())
                assertEquals(expected(tag,"save20_gif_description"),root.findViewWithTag<TextView>("export_description").text.toString())
                assertEquals(!enabled,checkbox.isChecked);checkbox.performClick();assertEquals(enabled,checkbox.isChecked)
                dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();idle()
                assertEquals(ImageFormat.GIF,request!!.options.format);assertEquals(enabled,request!!.options.dither)
                assertEquals("fixture.gif",request!!.fileName);assertFalse(canceled);assertFalse(dialog.isShowing)
            } finally {dialog.dismiss()}
        }
    }

    @Test fun completedImageReplacementFailureKeepsDestinationInputAndTemporaryCleanup() = forEachLocale { tag,activity ->
        val folder=File(activity.cacheDir,"$tag-destination-${System.nanoTime()}").apply {mkdirs()}
        val bytes=Base64.getDecoder().decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j4Z0AAAAASUVORK5CYII=")
        val encoded="data:image/png;base64,"+Base64.getEncoder().encodeToString(bytes)
        val input=File(folder,"input.txt").apply {writeText(encoded)}
        val blocked=File(folder,"destination.png").apply {mkdirs()}
        val sentinel=File(blocked,"keep.txt").apply {writeText("existing destination")}
        try {
            val error=assertThrows(IOException::class.java) {TextImageCodec.decodeToFile(input,blocked,4096)}
            assertEquals(expected(tag,"save20_destination_error"),error.message)
            assertEquals("existing destination",sentinel.readText());assertEquals(encoded,input.readText())
            assertEquals(setOf("input.txt","destination.png"),folder.listFiles()!!.map {it.name}.toSet())
            val completed=File(folder,"completed.png");TextImageCodec.decodeToFile(input,completed,4096)
            assertArrayEquals(bytes,completed.readBytes());assertEquals(encoded,input.readText())
        } finally {folder.deleteRecursively()}
    }

    @Test fun canvasDialogKeepsTopLeftAndUndoRestoresEitherIndependentlyClippedEdge() {
        fun descendants(view: View): List<View> = listOf(view) + if(view is android.view.ViewGroup)
            (0 until view.childCount).flatMap {descendants(view.getChildAt(it))} else emptyList()
        for(tag in listOf("be","sq")) {
            AppLanguage.select(RuntimeEnvironment.getApplication(),tag)
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);val activity=controller.get()
            try {
                controller.setup();awaitEditorStartup(activity);Locale.setDefault(Locale.US)
                activity.document.newImage(4,3)
                val original=IntArray(12) { 0xff000000.toInt() or ((it+1)*0x010101) }
                activity.document.bitmap.setPixels(original,0,4,0,0,4,3)
                EditorTestNavigation.click(activity,"tool_WATERCOLOR")
                val strengthSlider=activity.window.decorView.findViewWithTag<SeekBar>("watercolor_strength")
                val strength=strengthSlider.parent as NumericSlider
                assertSame(strengthSlider,strength.slider)
                assertEquals(expected(tag,"ui_strength"),strength.name)
                assertEquals(expected(tag,"ui_strength"),strength.slider.contentDescription.toString())
                strength.slider.progress=37-strength.minimum;idle()
                assertEquals(37,activity.document.watercolorStrength)
                for(size in listOf(ImageDimensions(2,3),ImageDimensions(4,1))) {
                    EditorTestNavigation.named(activity,"Edit",expected(tag,"ui_canvas_size"))
                    val dialog=checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
                    val views=descendants(dialog.window!!.decorView)
                    assertEquals(expected(tag,"ui_canvas_size_30460e"),shadowOf(dialog).title.toString())
                    assertTrue(views.filterIsInstance<TextView>().any {it.text.toString()==expected(tag,"ui_keeps_pixels_at_the_top_left_smaller_canvas")})
                    views.filterIsInstance<DimensionControls>().single().setDimensions(size)
                    assertEquals(expected(tag,"ui_apply"),dialog.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                    dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();idle()
                    assertFalse(dialog.isShowing)
                    assertEquals(size.width,activity.document.bitmap.width);assertEquals(size.height,activity.document.bitmap.height)
                    for(y in 0 until size.height) for(x in 0 until size.width)
                        assertEquals("$tag top-left retained pixel $x,$y",original[y*4+x],activity.document.bitmap.getPixel(x,y))
                    EditorTestNavigation.click(activity,"undo")
                    assertEquals(4,activity.document.bitmap.width);assertEquals(3,activity.document.bitmap.height)
                    val restored=IntArray(12);activity.document.bitmap.getPixels(restored,0,4,0,0,4,3)
                    assertArrayEquals(original,restored)
                }
            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
                controller.pause().stop().destroy();AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
                PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
            }
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
