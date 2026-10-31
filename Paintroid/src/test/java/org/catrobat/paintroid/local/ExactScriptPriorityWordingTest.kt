/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.ActivityManager
import android.app.AlertDialog
import android.content.Context
import android.content.ContextWrapper
import android.content.res.Resources
import android.os.Looper
import android.view.View
import android.widget.CheckBox
import android.widget.EditText
import android.widget.SeekBar
import android.widget.TextView
import android.widget.Spinner
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
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
class ExactScriptPriorityWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    // Current compiled label checks control binding, not historical wording approval.
    private fun expected(tag: String,key: String)=PriorityWordingExpectations.resourceText(tag,key)
    private fun formatted(tag: String, key: String, vararg args: Any) =
        String.format(Locale.forLanguageTag(tag),expected(tag,key),*args)

    private fun idle()=shadowOf(Looper.getMainLooper()).idle()

    @Before fun rememberLanguage() {
        // Wording/menu checks need a fixed device budget, not transient host-JVM headroom.
        // Robolectric resets this system-service fixture after each test.
        val context = RuntimeEnvironment.getApplication() as Context
        val mib = 1024L * 1024
        shadowOf(context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager).setMemoryInfo(ActivityManager.MemoryInfo().apply {
            totalMem = 1024 * mib; availMem = 512 * mib; threshold = 128 * mib
        })
        previousResources = PaintApplication.currentResources
        previousLocale = Locale.getDefault()
        previousTag = AppLanguage.selectedTag(RuntimeEnvironment.getApplication())
    }
    @After fun restoreLanguage() {
        AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
    }
    private fun forEachLocale(tags: List<String> = listOf("tt-Latn","ain-Latn","mn-Mong"), visible: Boolean = false, check: (String,Activity)->Unit) {
        for(tag in tags) {
            val controller=Robolectric.buildActivity(Activity::class.java)
            val activity=controller.get();activity.setTheme(R.style.ClassicPaintTheme);controller.setup()
            try {
                AppLanguage.select(activity,tag);AppLanguage.refresh(activity)
                assertEquals(tag,AppLanguage.selectedTag(activity))
                // ui() must format using the selected resource locale, not the process default.
                Locale.setDefault(Locale.US)
                if(visible) controller.visible().windowFocusChanged(true)
                check(tag,activity)
            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
                AppLanguage.select(activity,previousTag);AppLanguage.refresh(activity)
                controller.pause().stop().destroy()
                PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
            }
        }
    }

    @Test fun dimensionControlsKeepFullCountAndComposedUnitsAcrossUnitAndSizeChanges() = forEachLocale { tag,activity ->
        val controls=DimensionControls(activity,ImageDimensions(40,25),locked=false)
        assertEquals(activity.getString(R.string.ui_pixels),controls.findViewWithTag<TextView>("size_pixels").text.toString())
        assertEquals(activity.getString(R.string.ui_percent),controls.findViewWithTag<TextView>("size_percent").text.toString())
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

    private fun requireCategoryCaptionAndTooltip(tag: String,button: ToolCategoryButton,caption: String,description: String) {
        val vertical=tag=="mn-Mong"
        assertEquals("Expected tooltip ownership $tag",vertical,VerticalText.uiVertical(button.context))
        assertEquals(caption,button.text.toString())
        assertEquals(description,button.contentDescription.toString())
        assertEquals(description,LocaleTooltip.logicalText(button).toString())
        if(vertical) assertNull("No duplicate native tooltip $tag",button.tooltipText)
        else assertEquals(description,button.tooltipText.toString())
        assertTrue("Category button attached $tag",button.isAttachedToWindow)
        val node=button.createAccessibilityNodeInfo()
        assertEquals(description,node.contentDescription.toString())
        assertEquals(description,node.tooltipText.toString())
    }

    @Test fun categoryAccessibilityTracksEveryActualToolAndExpansionState() = forEachLocale(visible=true) { tag,activity ->
        for(down in listOf(false,true)) for(category in ToolCategory.values()) {
            val button=ToolCategoryButton(activity,category,category.tools.first(),down)
            activity.setContentView(button);idle()
            for(tool in category.tools) for(expanded in listOf(false,true)) {
                button.selectedTool=tool;button.expanded=expanded;button.refresh()
                val description=formatted(tag,if(expanded) "ui_collapse_tool_category" else "ui_expand_tool_category",ui(category.labelId),tool.label)
                requireCategoryCaptionAndTooltip(tag,button,ui(category.labelId),description)
            }
        }
    }

    @Test fun categoryTooltipChecksRejectCaptionLogicalNativeAndAccessibilityCorruption() = forEachLocale(visible=true) { tag,activity ->
        val category=ToolCategory.BRUSH
        val caption=ui(category.labelId)
        val description=formatted(tag,"ui_expand_tool_category",caption,PaintTool.PENCIL.label)
        for(mutation in listOf("caption","description","logical","native","accessibility","detached")) {
            val button=ToolCategoryButton(activity,category,PaintTool.PENCIL,false)
            activity.setContentView(button);idle()
            requireCategoryCaptionAndTooltip(tag,button,caption,description)
            when(mutation) {
                "detached" -> (button.parent as android.view.ViewGroup).removeView(button)
                "caption" -> button.text="forged"
                "description" -> button.contentDescription="forged"
                "logical" -> {
                    LocaleTooltip.set(button,"forged")
                    if(tag!="mn-Mong") button.tooltipText=description
                }
                "native" -> button.tooltipText="forged"
                "accessibility" -> button.accessibilityDelegate=object: View.AccessibilityDelegate() {
                    override fun onInitializeAccessibilityNodeInfo(host: View,info: android.view.accessibility.AccessibilityNodeInfo) {
                        super.onInitializeAccessibilityNodeInfo(host,info)
                        info.tooltipText="forged"
                    }
                }
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) {
                requireCategoryCaptionAndTooltip(tag,button,caption,description)
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

    @Test fun canvasDialogKeepsTopLeftAndUndoRestoresEitherIndependentlyClippedEdge() {
        fun descendants(view: View): List<View> = listOf(view) + if(view is android.view.ViewGroup)
            (0 until view.childCount).flatMap {descendants(view.getChildAt(it))} else emptyList()
        for(tag in listOf("tt-Latn","ain-Latn","mn-Mong")) {
            AppLanguage.select(RuntimeEnvironment.getApplication(),tag)
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);val activity=controller.get()
            try {
                controller.setup();awaitEditorStartup(activity);Locale.setDefault(Locale.US)
                activity.document.newImage(4,3)
                val original=IntArray(12) { 0xff000000.toInt() or ((it+1)*0x010101) }
                activity.document.bitmap.setPixels(original,0,4,0,0,4,3)
                if(tag in listOf("tt-Latn","ain-Latn","mn-Mong")) {
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

    @Test fun realEditorReturnsToPreviousDrawingToolAndSelectsSolidFillWithoutRedrawing() {
        for(tag in listOf("tt-Latn","ain-Latn","mn-Mong")) {
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
                if(tag in listOf("tt-Latn","ain-Latn","mn-Mong")) {
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
        for(tag in listOf("tt-Latn","ain-Latn","mn-Mong")) {
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
    @Test fun imageAssemblyMenuUsesCurrentCompanionAndKeepsCurrentPixels() {
        for(tag in listOf("tt-Latn","ain-Latn","mn-Mong")) {
            AppLanguage.select(RuntimeEnvironment.getApplication(),tag)
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);val activity=controller.get()
            try {
                controller.setup();awaitEditorStartup(activity);Locale.setDefault(Locale.US)
                activity.document.newImage(5,7);val bitmap=activity.document.bitmap
                val resident=activity.document.residentPixels
                EditorTestNavigation.named(activity,"File",expected(tag,"ui_image_assembly"));idle()
                val request=checkNotNull(shadowOf(activity).nextStartedActivityForResult)
                assertEquals(AssemblyActivity::class.java.name,request.intent.component!!.className)
                assertEquals(resident,request.intent.getLongExtra("resident_pixels",-1L))
                assertSame(bitmap,activity.document.bitmap)
                assertEquals(5,activity.document.bitmap.width);assertEquals(7,activity.document.bitmap.height)
            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
                controller.pause().stop().destroy();AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
                PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
            }
        }
    }

}
