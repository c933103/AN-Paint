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
class MoroccanArabicMongolianTokiPonaPriorityWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    private fun aryMnTokBoundFixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/moroccan_arabic_mongolian_toki_pona_priority_wording.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete finite ARY/MN/TOK reviewed fixture", "02b4dcb288d76cc53c7d50e2e91375cd6aecffbf9a404a3d0a61987e86197f62", actual)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun aryMnTokSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) aryMnTokSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) aryMnTokSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private val sourceFixture by lazy { aryMnTokBoundFixture() }
    private val fixture by lazy { sourceFixture.getJSONObject("locales") }
    private fun defaultSource(key: String): String =
        decoded(sourceFixture.getJSONObject("sources").getJSONObject(key).getString("source"))
    private fun expected(tag: String, key: String): String {
        val raw=fixture.getJSONObject(tag).getJSONObject("accepted").getString(key)
        if(raw.startsWith("@string/")) {
            require(tag=="mn-Cyrl-MN" && key=="ui_draw26" && raw=="@string/ui_drawing23") { "Only the exact retained MN Draw alias is reviewed" }
            return expected(tag,"ui_drawing23")
        }
        return PriorityWordingExpectations.successor(tag,key,decoded(raw))
    }
    private fun decoded(raw: String): String = Regex("""\\(.)""").replace(raw.removeSurrounding("\"")) { token ->
        when(token.groupValues[1]) { "n"->"\n"; "t"->"\t"; "r"->"\r"; else->token.groupValues[1] }
    }
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
    private fun forEachLocale(tags: List<String> = listOf("ary","mn-Cyrl-MN","tok"), check: (String,Activity)->Unit) {
        for(tag in tags) {
            val controller=Robolectric.buildActivity(Activity::class.java)
            val activity=controller.get();activity.setTheme(R.style.ClassicPaintTheme);controller.setup()
            try {
                AppLanguage.select(activity,tag);AppLanguage.refresh(activity)
                assertEquals(tag,AppLanguage.selectedTag(activity))
                // ui() must format using the selected resource locale, not the process default.
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

    @Test fun everyReviewedMoroccanArabicMongolianTokiPonaCompiledValueKeepsCompleteUnicodeNewlinesAndPercentArguments() = forEachLocale { tag,activity ->
        val locale=fixture.getJSONObject(tag)
        val values=locale.getJSONObject("accepted")
        val keys=values.keys().asSequence().filter { values.get(it) is String }.toList()
        val pattern=Regex("%(\\d+)\\$[-#+ 0,(<]*(?:\\d+)?(?:\\.\\d+)?([sdf])")
        for(key in keys) {
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
        // Exact ARY/TOK successors replace former fallback; existing MN holds remain unchanged.
        val held=locale.getJSONObject("held")
        for(key in held.keys().asSequence()) if(held.isNull(key)) {
            val id=activity.resources.getIdentifier(key,"string",activity.packageName)
            assertNotEquals("$tag held/$key",0,id)
            val text=PriorityWordingExpectations.residual(tag,key,defaultSource(key))
            assertEquals("$tag held/successor/$key",text,activity.getString(id))
            val tokens=pattern.findAll(text).toList()
            if(tokens.isNotEmpty()) {
                val args=Array<Any>(tokens.maxOf { it.groupValues[1].toInt() }) { "argument 100%" }
                assertEquals("$tag successor arguments/$key",String.format(Locale.forLanguageTag(tag),text,*args),ui(id,*args))
            }
        }
    }

    @Test fun reviewedPaletteDoesNotSubstituteAmericanEnglishRegionalWording() = forEachLocale(listOf("ary","tok")) { tag,activity ->
        val key="ui_foreground_background_colour_palette"
        val held=fixture.getJSONObject(tag).getJSONObject("held")
        assertTrue("$tag explicitly held",held.has(key))
        assertTrue("$tag explicitly held absent",held.isNull(key))
        val defaultText="Foreground %1\$s, background %2\$s. %3\$s colour palette."
        val americanText="Foreground %1\$s, background %2\$s. %3\$s color palette."
        assertEquals(defaultText,defaultSource(key))
        val american=activity.createConfigurationContext(android.content.res.Configuration(activity.resources.configuration).apply {
            setLocale(Locale.US)
        }).resources
        assertEquals(americanText,american.getString(R.string.ui_foreground_background_colour_palette))
        assertNotEquals(defaultText,americanText)
        assertEquals("$tag reviewed palette not US",PriorityWordingExpectations.residual(tag,key,defaultText),activity.getString(R.string.ui_foreground_background_colour_palette))
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
        for((width,height) in listOf(1 to 1,1000 to 2000)) {
            val error=assertThrows(ImageSizeException::class.java) {policy.check(width,height)}
            assertEquals(formatted(tag,"ui_d_d_pixels_2f_mp_exceeds_the_current",width,height,width.toLong()*height/1_000_000.0,0.0),error.message)
        }
    }

    @Test fun saveExportAndShareKeepDistinctCompleteMessagesAndRepeatedCancel() = forEachLocale { tag,activity ->
        fun texts(view: View): List<String> =
            (if(view is TextView) listOf(view.text.toString()) else emptyList())+
            (if(view is ViewGroup) (0 until view.childCount).flatMap {texts(view.getChildAt(it))} else emptyList())
        val save=expected(tag,"ui_save_explanation23")
        val export=expected(tag,"ui_export_explanation23")
        val share=expected(tag,"ui_share_explanation34")
        for((sharing,exporting,message) in listOf(Triple(false,false,save),Triple(false,true,export),Triple(true,true,share))) repeat(2) {
            var confirmed=false;var cancelled=0
            val shown=SaveOptionsDialog(activity,ExportOptions(),share=sharing,
                confirm={confirmed=true},cancel={cancelled++},export=exporting).show()
            try {
                val displayed=texts(shown.window!!.decorView)
                assertTrue(displayed.contains(message))
                listOf(save,export,share).filter {it!=message}.forEach {assertFalse(displayed.contains(it))}
                assertEquals(expected(tag,if(sharing) "ui_save_and_share_41edb4" else if(exporting) "ui_export_as23" else "save20_title"),shadowOf(shown).title.toString())
                assertTrue(displayed.contains(expected(tag,"save20_file_format")))
                assertTrue(displayed.contains(expected(tag,"save20_file_name")))
                assertEquals(expected(tag,"ui_choose_location"),shown.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals(expected(tag,"ui_cancel"),shown.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
                shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
                assertFalse(shown.isShowing);assertFalse(confirmed);assertEquals(1,cancelled)
            } finally {shown.dismiss()}
        }
    }

    @Test fun completeCropPluralAndAccessiblePreviewTrackActualSelectionCounts() = forEachLocale { tag,activity ->
        val images=(1..3).map {i->AssemblyImage("image$i",File(activity.cacheDir,"$tag-$i.image"),"$i.png",null,ImageDimensions(24,16))}
        var applied=false
        val shown=ImageCropDialog(activity,images,{null}) {applied=true}.show()
        try {
            val root=shown.window!!.decorView;shadowOf(Looper.getMainLooper()).idle()
            assertEquals(expected(tag,"ui_image_shown_in_crop_preview"),root.findViewWithTag<View>("crop_preview_image").contentDescription.toString())
            val values=fixture.getJSONObject(tag).getJSONObject("accepted").getJSONObject("ui_crop_preview_images")
            fun check(count: Int) {
                // MN integer one=1; ARY/TOK expected root-other fallback, not generic Arabic rules.
                val quantity=if(tag=="mn-Cyrl-MN" && count==1) "one" else "other"
                val pattern=decoded(values.getString(quantity))
                val text=String.format(Locale.forLanguageTag(tag),pattern,24,16,count)
                assertEquals(text,root.findViewWithTag<TextView>("crop_status").text.toString())
                assertEquals(text,uiQuantity(activity.resources,R.plurals.ui_crop_preview_images,count,24,16,count))
            }
            for(count in listOf(0,1,2,3,4,5,9,11,21,71,101,1_000_000)) {
                val quantity=if(tag=="mn-Cyrl-MN" && count==1) "one" else "other"
                val expected=String.format(Locale.forLanguageTag(tag),decoded(values.getString(quantity)),24,16,count)
                assertEquals(expected,uiQuantity(activity.resources,R.plurals.ui_crop_preview_images,count,24,16,count))
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
        for(tag in listOf("ary","mn-Cyrl-MN","tok")) {
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
