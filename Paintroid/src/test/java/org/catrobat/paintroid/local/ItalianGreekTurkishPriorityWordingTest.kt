/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.res.Resources
import android.graphics.Rect
import android.os.Looper
import android.view.View
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
class ItalianGreekTurkishPriorityWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    private val fixture by lazy {
        JSONObject(File("../tools/fixtures/current_localization/italian_greek_turkish_priority_wording.json").readText()).getJSONObject("locales")
    }
    private fun row(tag: String,identity: String): JSONObject {
        val locale=fixture.getJSONObject(tag)
        return locale.getJSONObject("values").optJSONObject(identity) ?: locale.getJSONObject("context").getJSONObject(identity)
    }
    private fun expected(tag: String,key: String)=row(tag,"string/$key").getString("display")
    private fun formatted(tag: String,key: String,vararg args: Any)=String.format(Locale.forLanguageTag(tag),expected(tag,key),*args)
    private fun cropTemplate(tag: String,count: Int)=row(tag,"plurals/ui_crop_preview_images").getJSONObject("display").getString(if(count==1) "one" else "other")
    private fun cropText(tag: String,count: Int,width: Int=24,height: Int=16)=String.format(Locale.forLanguageTag(tag),cropTemplate(tag,count),width,height,count)
    private fun idle()=shadowOf(Looper.getMainLooper()).idle()

    @Before fun rememberLanguage() {
        previousResources=PaintApplication.currentResources;previousLocale=Locale.getDefault()
        previousTag=AppLanguage.selectedTag(RuntimeEnvironment.getApplication())
    }
    @After fun restoreLanguage() {
        AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
        PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
    }
    private fun forEachLocale(tags: List<String> = listOf("it","el","tr"),check: (String,Activity)->Unit) {
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

    @Test fun allChangedCompiledStringsAndEveryReachablePluralKeepCompleteArguments() = forEachLocale { tag,activity ->
        val values=fixture.getJSONObject(tag).getJSONObject("values")
        for(identity in values.keys()) {
            val (kind,key)=identity.split('/')
            val id=activity.resources.getIdentifier(key,kind,activity.packageName)
            assertNotEquals("$tag/$identity",0,id)
            if(kind=="string") assertEquals("$tag/$identity",expected(tag,key),activity.getString(id))
            else for(count in 0..20) {
                assertEquals("$tag/$count",cropTemplate(tag,count),activity.resources.getQuantityText(id,count).toString())
                assertEquals(cropText(tag,count),activity.resources.getQuantityString(id,count,24,16,count))
            }
        }
    }

    @Test fun realCropDialogSelectionCountsAllEdgesAndRepeatedUnitsStayAtomic() = forEachLocale { tag,activity ->
        val images=(0 until 20).map { AssemblyImage("fixture-$it",File(activity.cacheDir,"fixture-$it.image"),"Image $it",null,ImageDimensions(24,16)) }
        var applied=false
        val dialog=ImageCropDialog(activity,images,{null}) {applied=true}.show()
        try {
            idle();val root=dialog.window!!.decorView
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
            root.findViewWithTag<View>("crop_reset").performClick();idle()
            assertEquals(cropText(tag,20),root.findViewWithTag<TextView>("crop_status").text.toString())
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();idle()
            assertFalse(applied);assertFalse(dialog.isShowing)
            assertTrue(images.all {it.crop==Rect(0,0,24,16)})
        } finally {dialog.dismiss()}
    }

    @Test fun actualAttachmentGeometryExplainsMayMoveRatherThanAlwaysMove() = forEachLocale(listOf("el","tr")) { _,activity ->
        val folder=File(activity.cacheDir,"conditional-crop-${System.nanoTime()}").apply {mkdirs()}
        try {
            val model=ImageAssembly(folder)
            val images=listOf("parent","child").map { AssemblyImage(it,File(folder,"$it.image").apply {writeText(it)},it,null,ImageDimensions(24,16)) }
            model.add(images);model.place("parent",Attachment(null,null));model.place("child",Attachment("parent",SnapEdge.RIGHT))
            val before=Rect(model.layout().getValue("child"))
            model.crop("parent",Rect(0,0,24,14))
            assertEquals("Height-only crop leaves right-attached child in place",before,model.layout().getValue("child"))
            model.undo();model.crop("parent",Rect(0,0,22,16))
            val moved=model.layout().getValue("child")
            assertEquals(before.left-2,moved.left);assertEquals(before.top,moved.top)
            model.undo();assertEquals(before,model.layout().getValue("child"))
        } finally {folder.deleteRecursively()}
    }

    @Test fun greekGifDescriptionAndCheckboxProduceTheSelectedDitherRequest() = forEachLocale(listOf("el")) { tag,activity ->
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

    @Test fun completedImageReplacementFailureKeepsDestinationInputAndTemporaryCleanup() = forEachLocale(listOf("el","tr")) { tag,activity ->
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

    @Test fun greekZeroBudgetRejectsOneAndManyPixelsWithCompleteSingularImageWarning() = forEachLocale(listOf("el")) { tag,_ ->
        val mib=1024L*1024;val policy=ImageMemoryPolicy.calculate(256*mib,0,0,0,false)
        assertEquals(0L,policy.maxPixels())
        for(size in listOf(ImageDimensions(1,1),ImageDimensions(2,1),ImageDimensions(2000,1000))) {
            val error=assertThrows(ImageSizeException::class.java) {policy.check(size.width,size.height)}
            assertEquals(formatted(tag,"ui_d_d_pixels_2f_mp_exceeds_the_current",size.width,size.height,size.pixels/1_000_000.0,0.0),error.message)
            assertTrue(error.message!!.startsWith("Μια εικόνα "));assertTrue(error.message!!.endsWith("Δεν εφαρμόστηκε αυτόματη αλλαγή μεγέθους."))
        }
    }

    @Test fun realEditorReturnsToPreviousDrawingToolAndSelectsSolidFillWithoutRedrawing() {
        for(tag in listOf("it","el","tr")) {
            AppLanguage.select(RuntimeEnvironment.getApplication(),tag)
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);val activity=controller.get()
            try {
                controller.setup();awaitEditorStartup(activity);Locale.setDefault(Locale.US)
                activity.document.newImage(5,7);val bitmap=activity.document.bitmap
                EditorTestNavigation.click(activity,"tool_BRUSH");EditorTestNavigation.click(activity,"tool_ZOOM")
                assertEquals(PaintTool.ZOOM,activity.paintCanvas.tool)
                val back=activity.window.decorView.findViewWithTag<TextView>("navigate_draw")
                assertEquals(expected(tag,"ui_draw_again"),back.text.toString());assertTrue(back.performClick());idle()
                assertEquals(PaintTool.BRUSH,activity.paintCanvas.tool);assertSame(bitmap,activity.document.bitmap)
                if(tag!="el") {
                    activity.document.shapeStyle=0
                    EditorTestNavigation.click(activity,"category_INSERT");EditorTestNavigation.click(activity,"tool_RECTANGLE")
                    val choice=activity.window.decorView.findViewWithTag<TextView>("tool_option")
                    assertTrue(choice.performClick());idle()
                    val dialog=checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
                    for((index,key) in listOf("ui_outline","ui_solid_fill","ui_fill_line").withIndex())
                        assertEquals(expected(tag,key),dialog.listView.adapter.getItem(index).toString())
                    assertTrue(dialog.listView.performItemClick(null,1,1L));idle()
                    assertEquals(1,activity.document.shapeStyle);assertEquals(expected(tag,"ui_solid_fill"),choice.text.toString())
                    assertSame(bitmap,activity.document.bitmap)
                }
                if(tag=="it") {
                    EditorTestNavigation.named(activity,"Edit",expected(tag,"ui_canvas_size"))
                    val dialog=checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
                    assertEquals(expected(tag,"ui_canvas_size_30460e"),shadowOf(dialog).title.toString())
                    dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();idle();assertSame(bitmap,activity.document.bitmap)
                }
            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
                controller.pause().stop().destroy();AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
                PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
            }
        }
    }
}
