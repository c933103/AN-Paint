/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.ContextWrapper
import android.content.res.Resources
import android.os.Looper
import android.view.View
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
class SoraniUyghurTatarPriorityWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    private fun ckbUgTtBoundFixture(tag: String): JSONObject {
        val expected=mapOf("ckb" to "a708e9f78a84386a601e1b68d55ac4057cb5a450e7f72577a00b375bd3b0806f", "ug" to "4110353522a52589ea13e1ecc8b471e9fc00e4ce9063812a7708966defa5982c", "tt-Cyrl" to "59878042f6e7bdd383ac5211921f2e5ecd8648059fb1ac0171583130febfcd22")
        val bytes=File("../tools/fixtures/current_localization/sorani_uyghur_tatar_priority_wording/$tag.json").readBytes()
        val digest=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete canonical fixture $tag",expected.getValue(tag),digest)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun ckbUgTtSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) ckbUgTtSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) ckbUgTtSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private val fixture by lazy {
        JSONObject().apply {
            for(tag in listOf("ckb","ug","tt-Cyrl")) put(tag,ckbUgTtBoundFixture(tag))
        }
    }
    private fun row(tag: String, key: String): JSONObject {
        val locale = fixture.getJSONObject(tag)
        return locale.getJSONObject("values").optJSONObject(key)
            ?: locale.getJSONObject("context").getJSONObject(key)
    }
    private fun expected(tag: String, key: String) = row(tag,key).getString("display")
    private fun formatted(tag: String, key: String, vararg args: Any) =
        String.format(Locale.forLanguageTag(tag),expected(tag,key),*args)

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
    private fun forEachLocale(tags: List<String> = listOf("ckb","ug","tt-Cyrl"), check: (String,Activity)->Unit) =
        PriorityWordingExpectations.forEachLocale(
            tags, previousResources, previousLocale, previousTag, check)

    @Test fun everyAcceptedAndHeldCompiledValueKeepsExactIndependentDisplayAndArguments() = forEachLocale { tag,activity ->
        val values=fixture.getJSONObject(tag).getJSONObject("values")
        val pattern=Regex("%(\\d+)\\$[-#+ 0,(<]*(?:\\d+)?(?:\\.\\d+)?([sdf])")
        val context=fixture.getJSONObject(tag).getJSONObject("context")
        val allKeys=(values.keys().asSequence()+context.keys().asSequence()).toSet()
        for(key in allKeys) {
            if(row(tag,key).getString("type")!="string")continue
            val id=activity.resources.getIdentifier(key,"string",activity.packageName)
            assertNotEquals("$tag/$key",0,id)
            val text=expected(tag,key)
            assertEquals("$tag/$key",text,activity.getString(id))
            val tokens=pattern.findAll(text).toList()
            if(tokens.isNotEmpty()) {
                val args=Array<Any>(tokens.maxOf { it.groupValues[1].toInt() }) { "argument 100%" }
                for(token in tokens) args[token.groupValues[1].toInt()-1]=when(token.groupValues[2]) {
                    "d"->21001L;"f"->12.75;else->"argument 100%"
                }
                assertEquals("$tag/$key arguments",String.format(Locale.forLanguageTag(tag),text,*args),ui(id,*args))
            }
        }
        val held=fixture.getJSONObject(tag).getJSONObject("held_display")
        for(key in held.keys()) {
            val entry=held.getJSONObject(key)
            assertEquals("string",entry.getString("type"))
            val id=activity.resources.getIdentifier(key,"string",activity.packageName)
            assertNotEquals("Held $tag/$key",0,id)
            assertEquals("Held current or English fallback $tag/$key",PriorityWordingExpectations.residual(tag,key,entry.getString("display")),activity.getString(id))
        }
        run {
            assertEquals(PriorityWordingExpectations.residual(tag,"ui_foreground_background_colour_palette","Foreground %1\$s, background %2\$s. %3\$s colour palette."),
                activity.getString(R.string.ui_foreground_background_colour_palette))
            assertEquals(PriorityWordingExpectations.residual(tag,"ui_foreground_background_colour_palette","Foreground foreground 100%, background background 100%. palette 100% colour palette.","foreground 100%","background 100%","palette 100%"),
                ui(R.string.ui_foreground_background_colour_palette,"foreground 100%","background 100%","palette 100%"))
            assertEquals(PriorityWordingExpectations.residual(tag,"ui_save_as_png","Save as PNG…"),ui(R.string.ui_save_as_png))
            run {
                assertEquals(PriorityWordingExpectations.residual(tag,"ui_fg","FG"),ui(R.string.ui_fg))
                assertEquals(PriorityWordingExpectations.residual(tag,"ui_bg","BG"),ui(R.string.ui_bg))
            }
        }
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
            val unit=expected(tag,if(percent) "ui_percent_fd8671" else "ui_pixels_6ec9c2")
            assertEquals(formatted(tag,"ui_width_in",unit),controls.widthInput.contentDescription.toString())
            assertEquals(formatted(tag,"ui_height_in",unit),controls.heightInput.contentDescription.toString())
            assertEquals(ImageDimensions(2000,1000),controls.dimensions)
        }
        controls.widthInput.setText("")
        assertNull(controls.dimensions)
        assertEquals(expected(tag,"ui_enter_positive_dimensions_that_resolve_to_at_least"),result.text.toString())
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

    @Test fun nativeWorkingMemoryFloorKeepsCancelAndRejectsAnImpossibleCopy() = forEachLocale() { tag,activity ->
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

    @Test fun memoryAdmissionStopsBeforeAllocationWithAllFourArguments() = forEachLocale { tag,_ ->
        val mib=1024L*1024;val policy=ImageMemoryPolicy.calculate(256*mib,0,96*mib,0,false)
        assertEquals(0L,policy.maxPixels())
        val error=assertThrows(ImageSizeException::class.java) {policy.check(1000,2000)}
        assertEquals(formatted(tag,"ui_d_d_pixels_2f_mp_exceeds_the_current",1000,2000,2.0,0.0),error.message)
    }

    @Test fun failedDraftRecoveryKeepsExactBytesBeforeClaimingPreservation() = forEachLocale { tag,activity ->
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
    @Test fun gifDitherDescriptionAndCheckboxStayPairedWithoutSavingOnCancel() = forEachLocale { tag,activity ->
        var saved=false;var cancelled=0
        val shown=SaveOptionsDialog(activity,ExportOptions(format=ImageFormat.GIF,dither=true),
            confirm={saved=true},cancel={cancelled++}).show()
        try {
            shadowOf(Looper.getMainLooper()).idle();val root=shown.window!!.decorView
            val dither=root.findViewWithTag<CheckBox>("export_dither")
            val description=root.findViewWithTag<TextView>("export_description")
            val formats=ImageFormat.values().filter { !it.isDerivedExport }
            val spinner=root.findViewWithTag<Spinner>("export_format")
            assertEquals(expected(tag,"save20_file_format"),spinner.contentDescription.toString())
            assertEquals(expected(tag,"save20_dither"),dither.text.toString())
            assertEquals(expected(tag,"save20_gif_description"),description.text.toString())
            assertEquals(View.VISIBLE,dither.visibility);assertTrue(dither.isChecked)
            dither.performClick();assertFalse(dither.isChecked)
            spinner.setSelection(formats.indexOf(ImageFormat.PNG));shadowOf(Looper.getMainLooper()).idle()
            assertEquals(View.GONE,dither.visibility)
            spinner.setSelection(formats.indexOf(ImageFormat.GIF));shadowOf(Looper.getMainLooper()).idle()
            assertEquals(View.VISIBLE,dither.visibility);assertFalse(dither.isChecked)
            assertEquals(expected(tag,"save20_gif_description"),description.text.toString())
            shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertFalse(saved);assertEquals(1,cancelled);assertFalse(shown.isShowing)
        } finally {shown.dismiss()}
    }


    @Test fun compiledCropPluralUsesCompleteReviewedQuantityForOneTwoAndMany() = forEachLocale { tag,activity ->
        val row=fixture.getJSONObject(tag).getJSONObject("values").getJSONObject("ui_crop_preview_images")
        val values=row.getJSONObject("display")
        for(count in listOf(0,1,2,21001)) {
            // CKB/UG exact CLDR48 one/other; TT has no explicit CLDR48 rule.
            // TT other-only count-neutral text is verified without asserting ICU dispatch.
            val quantity=if(tag!="tt-Cyrl" && count==1) "one" else "other"
            if(tag!="tt-Cyrl") assertEquals("Runtime ICU cardinal category $tag/$count",quantity,
                android.icu.text.PluralRules.forLocale(Locale.forLanguageTag(tag)).select(count.toDouble()))
            // Equal count-neutral forms verify complete compiled text, not which XML child supplied it.
            val text=values.getString(quantity)
            assertEquals(String.format(Locale.forLanguageTag(tag),text,24,16,count),
                uiQuantity(activity.resources,R.plurals.ui_crop_preview_images,count,24,16,count))
        }
    }
}
