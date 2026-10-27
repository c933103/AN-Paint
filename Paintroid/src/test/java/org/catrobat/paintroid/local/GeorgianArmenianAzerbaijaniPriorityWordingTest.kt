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
    private fun kaHyAzBoundFixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/georgian_armenian_azerbaijani_priority_wording.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete finite KA/HY/AZ reviewed fixture", "6672b568ad8919285db2ed87ce13f2578a6f29a651a10c885d4ca5ac4dbd9247", actual)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun kaHyAzSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) kaHyAzSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) kaHyAzSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private val fixture by lazy { kaHyAzBoundFixture().getJSONObject("locales") }
    private fun row(tag: String, key: String): JSONObject {
        val locale=fixture.getJSONObject(tag)
        return locale.getJSONObject("values").optJSONObject(key)
            ?: locale.getJSONObject("retained").optJSONObject(key)
            ?: locale.getJSONObject("context").optJSONObject(key)
            ?: error("Missing exact expectation $tag/$key")
    }
    private fun expected(tag: String,key: String)=row(tag,key).getString("display")
    private fun formatted(tag: String,key: String,vararg args: Any)=String.format(Locale.forLanguageTag(tag),expected(tag,key),*args)

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

    @Test fun everyChangedCompiledValueKeepsCompleteUnicodeNewlinesAndPercentArguments() = forEachLocale { tag,activity ->
        val values=fixture.getJSONObject(tag).getJSONObject("values")
        val pattern=Regex("%(\\d+)\\$[-#+ 0,(<]*(?:\\d+)?(?:\\.\\d+)?([sdf])")
        for(key in values.keys()) {
            val id=activity.resources.getIdentifier(key,"string",activity.packageName)
            assertNotEquals("$tag/$key",0,id)
            val text=expected(tag,key)
            assertEquals("$tag/$key",text,activity.getString(id))
            val tokens=pattern.findAll(text).toList()
            if(tokens.isNotEmpty() && values.getJSONObject(key).getJSONObject("attributes").optString("formatted")!="false") {
                val args=Array<Any>(tokens.maxOf { it.groupValues[1].toInt() }) { "argument 100%" }
                for(token in tokens) args[token.groupValues[1].toInt()-1]=when(token.groupValues[2]) {
                    "d"->21001L;"f"->12.75;else->"argument 100%"
                }
                assertEquals("$tag/$key arguments",String.format(Locale.forLanguageTag(tag),text,*args),ui(id,*args))
            }
        }
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

    @Test fun zeroBudgetRejectsOneAndManyPixelsWithCompleteWarning() = forEachLocale() { tag,_ ->
        val mib=1024L*1024
        val policy=ImageMemoryPolicy.calculate(256*mib,0,0,0,false)
        assertEquals(0L,policy.maxPixels())
        for(size in listOf(ImageDimensions(1,1),ImageDimensions(2,1),ImageDimensions(2000,1000))) {
            val error=assertThrows(ImageSizeException::class.java) { policy.check(size.width,size.height) }
            assertEquals(formatted(tag,"ui_d_d_pixels_2f_mp_exceeds_the_current",size.width,size.height,size.pixels/1_000_000.0,0.0),error.message)
        }
    }

    @Test fun realAnimationWarningsHandleArbitraryAndLowerBoundCountsAndCancelWithoutImporting() = forEachLocale { tag,activity ->
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
    @Test fun categoryAccessibilityTracksEveryActualToolAndExpansionState() = forEachLocale { tag,activity ->
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
            val none=root.findViewWithTag<TextView>("crop_none")
            assertEquals(expected(tag,"ui_none"),none.text.toString());none.performClick()
            images.forEach { assertFalse(root.findViewWithTag<CheckBox>("crop_include_${it.id}").isChecked) }
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
