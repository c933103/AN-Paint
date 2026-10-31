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
class PersianHebrewUrduPriorityWordingTest {
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
    private fun forEachLocale(tags: List<String> = listOf("fa","he","ur"),check: (String,Activity)->Unit) {
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
            for(count in listOf(20,0,1,2,20)) {
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
            for(edge in edges.keys) root.findViewWithTag<EditText>("crop_$edge").setText("2")
            assertFalse(applied);assertTrue(images.all {it.crop==Rect(0,0,24,16)})
            assertEquals(expected(tag,"ui_reset_crop"),root.findViewWithTag<TextView>("crop_reset").text.toString())
            root.findViewWithTag<View>("crop_reset").performClick();idle()
            for(edge in edges.keys) assertEquals("$tag reset $edge",0.0,
                root.findViewWithTag<EditText>("crop_$edge").text.toString().toDouble(),0.0)
            assertEquals(Rect(0,0,24,16),root.findViewWithTag<CropPreview>("crop_preview").crop!!.rect)
            assertFalse(applied);assertTrue(images.all {it.crop==Rect(0,0,24,16)})
            assertEquals(cropText(tag,20),root.findViewWithTag<TextView>("crop_status").text.toString())
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();idle()
            assertFalse(applied);assertFalse(dialog.isShowing)
            assertTrue(images.all {it.crop==Rect(0,0,24,16)})
        } finally {dialog.dismiss()}
    }

    @Test fun dimensionControlsKeepFullCountAndComposedUnitsAcrossUnitAndSizeChanges() = forEachLocale { tag,activity ->
        val controls=DimensionControls(activity,ImageDimensions(40,25),locked=false)
        val result=controls.findViewWithTag<TextView>("size_result")
        for(size in listOf(ImageDimensions(1,1),ImageDimensions(2,1),ImageDimensions(40,25),ImageDimensions(2000,1000))) {
            controls.setDimensions(size)
            assertEquals(formatted(tag,"ui_d_d_px_d_pixels_2f_mp",size.width,size.height,size.pixels,size.pixels/1_000_000.0),result.text.toString())
        }
        for(percent in listOf(false,true,false)) {
            controls.findViewWithTag<View>(if(percent) "size_percent" else "size_pixels").performClick()
            assertEquals(expected(tag,if(percent) "ui_percent" else "ui_pixels"),
                controls.findViewWithTag<TextView>(if(percent) "size_percent" else "size_pixels").text.toString())
            val unit=expected(tag,if(percent) "ui_percent_fd8671" else "ui_pixels_6ec9c2")
            assertEquals(formatted(tag,"ui_width_in",unit),controls.widthInput.contentDescription.toString())
            assertEquals(formatted(tag,"ui_height_in",unit),controls.heightInput.contentDescription.toString())
            assertEquals(ImageDimensions(2000,1000),controls.dimensions)
        }
        controls.widthInput.setText("")
        assertNull(controls.dimensions)
        assertEquals(expected(tag,"ui_enter_positive_dimensions_that_resolve_to_at_least"),result.text.toString())
    }

    @Test fun canvasDialogKeepsTopLeftAndUndoRestoresEitherIndependentlyClippedEdge() {
        fun descendants(view: View): List<View> = listOf(view) + if(view is android.view.ViewGroup)
            (0 until view.childCount).flatMap {descendants(view.getChildAt(it))} else emptyList()
        for(tag in listOf("fa","he","ur")) {
            AppLanguage.select(RuntimeEnvironment.getApplication(),tag)
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);val activity=controller.get()
            try {
                controller.setup();awaitEditorStartup(activity);Locale.setDefault(Locale.US)
                activity.document.newImage(4,3)
                val original=IntArray(12) { 0xff000000.toInt() or ((it+1)*0x010101) }
                activity.document.bitmap.setPixels(original,0,4,0,0,4,3)
                val priorTolerance=activity.document.tolerance
                EditorTestNavigation.click(activity,"tool_FILL")
                val tolerance=descendants(activity.window.decorView).filterIsInstance<NumericSlider>()
                    .single {it.name==expected(tag,"ui_tolerance")}
                assertEquals(expected(tag,"ui_tolerance"),tolerance.slider.contentDescription.toString())
                assertEquals(priorTolerance,activity.document.tolerance,0f)
                for(limit in listOf(0,10)) {
                    tolerance.slider.progress=limit-tolerance.minimum;idle()
                    assertEquals(limit.toFloat(),activity.document.tolerance,0f)
                    val sample=android.graphics.Bitmap.createBitmap(3,1,android.graphics.Bitmap.Config.ARGB_8888)
                    try {
                        val black=0xff000000.toInt();val near=0xff060800.toInt();val far=0xff070800.toInt()
                        sample.setPixels(intArrayOf(black,near,far),0,3,0,0,3,1)
                        ScanlineFill.fill(sample,0,0,android.graphics.Color.RED,activity.document.tolerance)
                        assertEquals(android.graphics.Color.RED,sample.getPixel(0,0))
                        assertEquals(if(limit==10) android.graphics.Color.RED else near,sample.getPixel(1,0))
                        assertEquals(far,sample.getPixel(2,0))
                    } finally {sample.recycle()}
                }
                val unchanged=IntArray(12);activity.document.bitmap.getPixels(unchanged,0,4,0,0,4,3)
                assertArrayEquals(original,unchanged)
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

    @Test fun canonicalPickerTagsStayRtlAndHebrewLegacyResourcesDoNotCreateAnIwOption() = forEachLocale { tag,activity ->
        assertTrue(AppLanguage.tags(activity).containsAll(listOf("fa","fa-IR","he","ur")))
        assertFalse(AppLanguage.tags(activity).contains("iw"))
        assertThrows(IllegalArgumentException::class.java) {AppLanguage.select(activity,"iw")}
        assertEquals(tag,AppLanguage.selectedTag(activity))
        assertEquals(tag,AppLanguage.locale(activity).toLanguageTag())
        assertEquals(tag,AppLanguage.resourceLocale(AppLanguage.locale(activity)).toLanguageTag())
        assertEquals(View.LAYOUT_DIRECTION_RTL,activity.resources.configuration.layoutDirection)
        assertEquals(expected(tag,"save20_file_format"),activity.getString(R.string.save20_file_format))
        if(tag=="he") {
            val config=android.content.res.Configuration(activity.resources.configuration)
            config.setLocale(Locale.forLanguageTag("iw"))
            assertEquals("he",config.locales[0].toLanguageTag())
            assertEquals(expected(tag,"save20_file_format"),activity.createConfigurationContext(config).getString(R.string.save20_file_format))
        }
    }

    @Test fun keepEditingCancelsRepeatedActualReplacementWithoutSavingDiscardingOrLaunching() {
        for(tag in listOf("fa","he","ur")) {
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

}
