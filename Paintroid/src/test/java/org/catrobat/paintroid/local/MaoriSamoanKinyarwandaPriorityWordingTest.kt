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
import android.widget.EditText
import android.widget.SeekBar
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
class MaoriSamoanKinyarwandaPriorityWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    private fun miSmRwBoundFixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/maori_samoan_kinyarwanda_priority_wording.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete finite MI/SM/RW reviewed fixture", "efaa8682d929a670acc3915e14941f9099513437df5874d2c16958e63182bc01", actual)
        return JSONObject(String(bytes,Charsets.UTF_8)).getJSONObject("locales")
    }

    private fun miSmRwSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) miSmRwSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) miSmRwSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private val fixture by lazy { miSmRwBoundFixture() }
    private fun row(tag: String,identity: String): JSONObject {
        val locale=fixture.getJSONObject(tag)
        return locale.getJSONObject("values").optJSONObject(identity) ?: locale.getJSONObject("context").getJSONObject(identity)
    }
    private fun expected(tag: String,key: String)=row(tag,"string/$key").getString("display")
    private fun formatted(tag: String,key: String,vararg args: Any)=String.format(Locale.forLanguageTag(tag),expected(tag,key),*args)
    // These bounded translations provide only other. Android falls back to other
    // for any missing quantity category; no native-language plural-dispatch claim.
    private fun cropQuantity(tag: String,count: Int):String {
        require(tag in listOf("mi","sm","rw"));require(count>=0)
        return "other"
    }
    private fun cropTemplate(tag: String,count: Int)=row(tag,"plurals/ui_crop_preview_images").getJSONObject("display").getString(cropQuantity(tag,count))
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
    private fun forEachLocale(tags: List<String> = listOf("mi","sm","rw"),check: (String,Activity)->Unit) {
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
        for(group in listOf("values","context")) {
        val values=fixture.getJSONObject(tag).getJSONObject(group)
        for(identity in values.keys()) {
            val (kind,key)=identity.split('/')
            val id=activity.resources.getIdentifier(key,kind,activity.packageName)
            assertNotEquals("$tag/$identity",0,id)
            if(kind=="string") {
                val text=expected(tag,key)
                assertEquals("$tag/$identity",text,activity.getString(id))
                val pattern=Regex("%(\\d+)\\$[-#+ 0,(<]*(?:\\d+)?(?:\\.\\d+)?([sdf])")
                val tokens=pattern.findAll(text).toList()
                if(tokens.isNotEmpty()) {
                    val args=Array<Any>(tokens.maxOf { it.groupValues[1].toInt() }) { "argument 100%" }
                    for(token in tokens) args[token.groupValues[1].toInt()-1]=when(token.groupValues[2]) {
                        "d"->21001L;"f"->12.75;else->"argument 100%"
                    }
                    assertEquals("$tag/$identity arguments",String.format(Locale.forLanguageTag(tag),text,*args),ui(id,*args))
                }
            }
            else for(count in 0..125) {
                assertEquals("$tag/$count",cropTemplate(tag,count),activity.resources.getQuantityText(id,count).toString())
                assertEquals(cropText(tag,count),activity.resources.getQuantityString(id,count,24,16,count))
            }
        }
        }
        // Historical absent holds resolve only to exact reviewed successors; RW gesture and SM stay fallback.
        val held=fixture.getJSONObject(tag).getJSONObject("held")
        val pattern=Regex("%(\\d+)\\$[-#+ 0,(<]*(?:\\d+)?(?:\\.\\d+)?([sdf])")
        for(identity in held.keys()) {
            val (kind,key)=identity.split('/');val row=held.getJSONObject(identity)
            assertEquals("string",kind);assertTrue(row.isNull("target"))
            val id=activity.resources.getIdentifier(key,"string",activity.packageName)
            assertNotEquals("$tag held/$key",0,id)
            val text=PriorityWordingExpectations.residual(tag,key,row.getString("source"))
            assertEquals("$tag held/successor/$key",text,activity.getString(id))
            val tokens=pattern.findAll(text).toList()
            if(tokens.isNotEmpty()) {
                val args=Array<Any>(tokens.maxOf { it.groupValues[1].toInt() }) { "argument 100%" }
                for(token in tokens) args[token.groupValues[1].toInt()-1]=when(token.groupValues[2]) {
                    "d"->21001L;"f"->12.75;else->"argument 100%"
                }
                assertEquals("$tag/$key successor arguments",String.format(Locale.forLanguageTag(tag),text,*args),ui(id,*args))
            }
        }
    }

    @Test fun realCropDialogSelectionCountsAllEdgesAndRepeatedUnitsStayAtomic() = forEachLocale(listOf("mi","sm","rw")) { tag,activity ->
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

    @Test fun dimensionControlsKeepFullCountAndComposedUnitsAcrossUnitAndSizeChanges() = forEachLocale(listOf("mi","sm","rw")) { tag,activity ->
        val controls=DimensionControls(activity,ImageDimensions(40,25),locked=false)
        val result=controls.findViewWithTag<TextView>("size_result")
        for(size in listOf(ImageDimensions(1,1),ImageDimensions(2,1),ImageDimensions(40,25),ImageDimensions(2000,1000))) {
            controls.setDimensions(size)
            assertEquals(formatted(tag,"ui_d_d_px_d_pixels_2f_mp",size.width,size.height,size.pixels,size.pixels/1_000_000.0),result.text.toString())
        }
        for(percent in listOf(false,true,false)) {
            controls.findViewWithTag<View>(if(percent) "size_percent" else "size_pixels").performClick()
            val unit=expected(tag,if(percent) "ui_percent_fd8671" else "ui_pixels_6ec9c2")
            assertEquals(formatted(tag,"ui_width_in",unit),controls.widthInput.contentDescription.toString())
            assertEquals(formatted(tag,"ui_height_in",unit),controls.heightInput.contentDescription.toString())
            assertEquals(ImageDimensions(2000,1000),controls.dimensions)
        }
        controls.widthInput.setText("")
        assertNull(controls.dimensions)
        assertEquals(expected(tag,"ui_enter_positive_dimensions_that_resolve_to_at_least"),result.text.toString())
    }

    @Test fun categoryAccessibilityTracksEveryActualToolAndExpansionState() = forEachLocale(listOf("mi","sm","rw")) { tag,activity ->
        for(down in listOf(false,true)) for(category in ToolCategory.values()) {
            val button=ToolCategoryButton(activity,category,category.tools.first(),down)
            for(tool in category.tools) for(expanded in listOf(false,true)) {
                button.selectedTool=tool;button.expanded=expanded;button.refresh()
                val description=formatted(tag,if(expanded) "ui_collapse_tool_category" else "ui_expand_tool_category",ui(category.labelId),tool.label)
                assertEquals(ui(category.labelId),button.text.toString())
                assertEquals(description,button.contentDescription.toString())
                assertEquals(description,button.tooltipText.toString())
            }
        }
    }

    @Test fun realAnimationWarningsHandleArbitraryAndLowerBoundCountsAndCancelWithoutImporting() = forEachLocale(listOf("mi","sm","rw")) { tag,activity ->
        val worker=Executors.newSingleThreadExecutor();var selection:ImportSelection?=null
        val files=mutableListOf<File>()
        try {
            for((count,exact) in listOf(2 to true,21 to true,21 to false)) {
                val bytes=ByteArrayOutputStream().apply {
                    write(Base64.getDecoder().decode("R0lGODlhAQABAIAAAAAAAP///w=="))
                    repeat(count) { write(Base64.getDecoder().decode("LAAAAAABAAEAAAICRAEA")) }
                    if(!exact) repeat(100_001) { write(byteArrayOf(0x21,0xfe.toByte(),1,0x78,0)) }
                    write(0x3b)
                }.toByteArray()
                val file=File.createTempFile("priority-animation-",".gif",activity.cacheDir).apply {writeBytes(bytes)};files.add(file)
                assertEquals(AnimationInfo("GIF",count,exact,false),AnimationInfo.inspect(file))
                var selected=0;var cancelled=0;var failure:Throwable?=null
                selection=ImportSelection(activity,worker,{0L},{selected++},{cancelled++},{failure=it})
                selection.start(file,"source.gif");worker.submit {}.get(10,TimeUnit.SECONDS);shadowOf(Looper.getMainLooper()).idle()
                assertNull(failure);val shown=checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
                val countText=if(exact) count.toString() else formatted(tag,"formats22_at_least_frames",count)
                assertEquals(formatted(tag,"formats22_animation_message","GIF",countText)+"\n\n"+expected(tag,"formats22_animation_still"),shadowOf(shown).message.toString())
                assertEquals(expected(tag,"formats22_animation_title"),shadowOf(shown).title.toString())
                assertEquals(expected(tag,"formats22_open_still"),shown.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertTrue(file.exists());assertEquals(0,selected)
                shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
                assertEquals(1,cancelled);assertEquals(0,selected);assertNull(failure);assertFalse(file.exists())
            }
        } finally {selection?.dispose();worker.shutdownNow();assertTrue(worker.awaitTermination(10,TimeUnit.SECONDS));files.forEach {it.delete()} }
    }

    @Test fun nativeWorkingMemoryFloorKeepsCancelAndRejectsAnImpossibleCopy() = forEachLocale(listOf("mi","sm","rw")) { tag,activity ->
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

    @Test fun failedDraftRecoveryKeepsExactBytesBeforeClaimingPreservation() = forEachLocale(listOf("mi","sm","rw")) { tag,activity ->
        val folder=File(activity.cacheDir,"priority-recovery-${System.nanoTime()}").apply {mkdirs()}
        val context=object:ContextWrapper(activity) {
            override fun getFilesDir():File=folder
            override fun getCacheDir():File=File(folder,"cache").apply {mkdirs()}
        }
        val store=AutosaveStore(folder);val original="deliberately not a ZIP draft".toByteArray();store.file.writeBytes(original)
        var recovered:RecoveredEditor?=null
        try {
            val result=recoverEditor(context,store).value;recovered=result
            assertFalse(result.restored);assertFalse(result.autosaveBlocked)
            assertEquals(expected(tag,"ui_previous_draft_kept_for_recovery"),result.draftStatus)
            assertEquals(formatted(tag,"ui_a_separate_recovery_copy_has_been_kept_use",expected(tag,"ui_the_previous_draft_could_not_be_restored")),result.recoveryNotice)
            assertArrayEquals(original,store.file.readBytes());assertEquals(1,store.recoveryCopies().size)
            assertArrayEquals(original,store.recoveryCopies().single().readBytes())
        } finally {recovered?.document?.close();folder.deleteRecursively()}
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
    @Test fun gifDescriptionAndCheckboxProduceTheSelectedDitherRequest() = forEachLocale(listOf("mi","sm","rw")) { tag,activity ->
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
        for(tag in listOf("mi","sm","rw")) {
            AppLanguage.select(RuntimeEnvironment.getApplication(),tag)
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);val activity=controller.get()
            try {
                controller.setup();awaitEditorStartup(activity);Locale.setDefault(Locale.US)
                activity.document.newImage(4,3)
                val original=IntArray(12) { 0xff000000.toInt() or ((it+1)*0x010101) }
                activity.document.bitmap.setPixels(original,0,4,0,0,4,3)
                if(tag in listOf("mi","sm","rw")) {
                EditorTestNavigation.click(activity,"tool_WATERCOLOR")
                val strengthSlider=activity.window.decorView.findViewWithTag<SeekBar>("watercolor_strength")
                val strength=strengthSlider.parent as NumericSlider
                assertSame(strengthSlider,strength.slider)
                assertEquals(expected(tag,"ui_strength"),strength.name)
                assertEquals(expected(tag,"ui_strength"),strength.slider.contentDescription.toString())
                strength.slider.progress=37-strength.minimum;idle()
                assertEquals(37,activity.document.watercolorStrength)
                }
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
    @Test fun losslessCheckboxAndQualityPercentageControlKeepTheActualSaveRequest() = forEachLocale(listOf("mi","sm","rw")) { tag,activity ->
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

    @Test fun realEditorReturnsToPreviousDrawingToolAndSelectsSolidFillWithoutRedrawing() {
        for(tag in listOf("mi","sm","rw")) {
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
                if(tag in listOf("mi","sm","rw")) {
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

            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
                controller.pause().stop().destroy();AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
                PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
            }
        }
    }

    @Test fun unlockedScalingCanShrinkAndEnlargeAxesIndependentlyAndUndo() {
        fun descendants(view: View): List<View> = listOf(view) + if(view is android.view.ViewGroup)
            (0 until view.childCount).flatMap {descendants(view.getChildAt(it))} else emptyList()
        for(tag in listOf("mi","sm","rw")) {
            AppLanguage.select(RuntimeEnvironment.getApplication(),tag)
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);val activity=controller.get()
            try {
                controller.setup();awaitEditorStartup(activity);Locale.setDefault(Locale.US)
                activity.document.newImage(8,6)
                for(size in listOf(ImageDimensions(4,9),ImageDimensions(12,3))) {
                    EditorTestNavigation.named(activity,"Edit",expected(tag,"ui_resize_image"))
                    val dialog=checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
                    val views=descendants(dialog.window!!.decorView)
                    assertEquals(expected(tag,"ui_resize_image_ab28be"),shadowOf(dialog).title.toString())
                    assertTrue(views.filterIsInstance<TextView>().any {it.text.toString()==expected(tag,"ui_scales_the_image_unlock_the_ratio_to_stretch")})
                    val controls=views.filterIsInstance<DimensionControls>().single()
                    assertTrue(controls.aspectLock.isChecked);controls.aspectLock.performClick();idle()
                    assertFalse(controls.aspectLock.isChecked)
                    controls.widthInput.setText(size.width.toString());controls.heightInput.setText(size.height.toString())
                    assertEquals(size,controls.dimensions)
                    dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();idle()
                    assertFalse(dialog.isShowing)
                    assertEquals(size.width,activity.document.bitmap.width);assertEquals(size.height,activity.document.bitmap.height)
                    EditorTestNavigation.click(activity,"undo")
                    assertEquals(8,activity.document.bitmap.width);assertEquals(6,activity.document.bitmap.height)
                }
            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
                controller.pause().stop().destroy();AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
                PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
            }
        }
    }
}
