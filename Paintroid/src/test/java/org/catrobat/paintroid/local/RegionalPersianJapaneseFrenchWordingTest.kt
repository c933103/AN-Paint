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
class RegionalPersianJapaneseFrenchWordingTest {
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
    private fun forEachLocale(tags: List<String> = listOf("fa-IR","ja","fr"),check: (String,Activity)->Unit) {
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

    @Test fun frenchAllFourCropEdgesConvertWithoutApplyingUntilConfirmed() = forEachLocale(listOf("fr")) {tag,activity ->
        val image=AssemblyImage("crop",File(activity.cacheDir,"crop.image"),"Source",null,ImageDimensions(40,20))
        var applied:Map<String,Rect>?=null
        fun show()=ImageCropDialog(activity,listOf(image),{null}) {applied=it}.show()
        fun exercise(dialog:AlertDialog) {
            idle();val root=dialog.window!!.decorView
            val edges=listOf("left","top","right","bottom")
            for((i,edge) in edges.withIndex()) root.findViewWithTag<EditText>("crop_$edge").setText((i+1).toString())
            for(percent in listOf(false,true,false)) {
                root.findViewWithTag<View>(if(percent) "crop_percent" else "crop_pixels").performClick();idle()
                for(edge in edges) assertEquals(formatted(tag,if(percent) "ui_trim_in_percent" else "ui_trim_in_pixels",expected(tag,"ui_$edge")),root.findViewWithTag<EditText>("crop_$edge").contentDescription.toString())
                assertEquals(expected(tag,if(percent) "ui_percent" else "ui_pixels"),root.findViewWithTag<TextView>(if(percent) "crop_percent" else "crop_pixels").text.toString())
                assertEquals(Rect(1,2,37,16),root.findViewWithTag<CropPreview>("crop_preview").crop!!.rect)
                assertNull(applied);assertEquals(Rect(0,0,40,20),image.crop)
            }
        }
        val canceled=show();try {exercise(canceled);canceled.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();idle();assertNull(applied)}finally{canceled.dismiss()}
        val confirmed=show();try {exercise(confirmed);confirmed.getButton(AlertDialog.BUTTON_POSITIVE).performClick();idle();assertEquals(mapOf("crop" to Rect(1,2,37,16)),applied);assertEquals(Rect(0,0,40,20),image.crop)}finally{confirmed.dismiss()}
    }
    @Test fun regionalQualityUsesActualSliderAndPreservesThenUpdatesRequest() = forEachLocale(listOf("fa-IR")) {tag,activity ->
        for(change in listOf(false,true)) {
            var request:SaveRequest?=null
            val shown=SaveOptionsDialog(activity,ExportOptions(ImageFormat.JPEG,quality=73),confirm={request=it},cancel={},initialFilename="sample.jpg").show()
            try {
                idle();val slider=shown.window!!.decorView.findViewWithTag<NumericSlider>("export_quality")
                assertEquals(expected(tag,"ui_quality"),slider.name);assertEquals(expected(tag,"ui_quality"),slider.slider.contentDescription.toString())
                assertEquals(1,slider.minimum);assertEquals(100,slider.maximum);assertEquals(72,slider.slider.progress)
                if(change)slider.slider.progress=40
                shown.getButton(AlertDialog.BUTTON_POSITIVE).performClick();idle();assertEquals(if(change)41 else 73,request!!.options.quality)
            }finally{shown.dismiss()}
        }
    }

    @Test fun regionalFlipUndoAndAirbrushPerformTheirNamedOperations() {
        val tag="fa-IR";AppLanguage.select(RuntimeEnvironment.getApplication(),tag)
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);val activity=controller.get()
        try {
            controller.setup();awaitEditorStartup(activity)
            val doc=activity.document;val canvas=activity.paintCanvas
            doc.newImage(4,3)
            for(y in 0..2) for(x in 0..3) doc.bitmap.setPixel(x,y,android.graphics.Color.rgb(x*50,y*70,30+x+y))
            val before=doc.bitmap.copy(android.graphics.Bitmap.Config.ARGB_8888,false)
            try {
                EditorTestNavigation.named(activity,"Edit",expected(tag,"ui_flip_vertical"))
                assertEquals(4,doc.bitmap.width);assertEquals(3,doc.bitmap.height)
                for(y in 0..2) for(x in 0..3) assertEquals(before.getPixel(x,2-y),doc.bitmap.getPixel(x,y))
                assertEquals(expected(tag,"ui_undo"),activity.window.decorView.findViewWithTag<View>("undo").contentDescription.toString())
                EditorTestNavigation.click(activity,"undo");assertTrue(before.sameAs(doc.bitmap))
            } finally {before.recycle()}
            doc.newImage(96,96);canvas.fit();val empty=doc.bitmap.copy(android.graphics.Bitmap.Config.ARGB_8888,false)
            try {
                EditorTestNavigation.click(activity,"menu_Draw")
                val category=activity.window.decorView.findViewWithTag<ToolCategoryButton>("category_BRUSH")
                if(!category.expanded) EditorTestNavigation.click(activity,"category_BRUSH")
                val spray=activity.window.decorView.findViewWithTag<View>("tool_SPRAY")
                assertTrue(spray.isShown);assertEquals(expected(tag,"ui_airbrush"),spray.contentDescription.toString())
                EditorTestNavigation.click(activity,"tool_SPRAY");assertEquals(PaintTool.SPRAY,canvas.tool)
                assertEquals(expected(tag,"ui_airbrush"),PaintTool.SPRAY.label);assertTrue(empty.sameAs(doc.bitmap))
                for((action,point) in listOf(android.view.MotionEvent.ACTION_DOWN to 20f,android.view.MotionEvent.ACTION_MOVE to 35f,android.view.MotionEvent.ACTION_UP to 45f)) {
                    val screen=canvas.toScreen(point,point);val event=android.view.MotionEvent.obtain(0,10,action,screen.x,screen.y,0)
                    try {assertTrue(canvas.dispatchTouchEvent(event))}finally{event.recycle()}
                }
                idle();assertFalse(empty.sameAs(doc.bitmap));EditorTestNavigation.click(activity,"undo");assertTrue(empty.sameAs(doc.bitmap))
            }finally{empty.recycle()}
        }finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss();controller.pause().stop().destroy()
            AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag);PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
        }
    }
    @Test fun keepEditingCancelsRepeatedActualReplacementWithoutSavingDiscardingOrLaunching() {
        for(tag in listOf("fa-IR")) {
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
