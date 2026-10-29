/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.res.Resources
import android.graphics.Bitmap
import android.graphics.Rect
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
import org.robolectric.RuntimeEnvironment
import org.robolectric.RobolectricTestRunner
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.util.ReflectionHelpers
import org.robolectric.util.ReflectionHelpers.ClassParameter
import java.io.File
import java.util.Locale
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

/** Six corrections, actual bounded consumers; not whole-language or layout certification. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class OrdinaryPriorityFollowthroughTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    private val fixture by lazy { OrdinaryPriorityExpectations.fixture() }
    private fun row(tag: String,key: String)=OrdinaryPriorityExpectations.row(fixture,tag,key)
    private fun expected(tag: String,key: String)=row(tag,"string/$key").getString("display")
    private fun formatted(tag: String,key: String,vararg args: Any)=String.format(Locale.forLanguageTag(tag),expected(tag,key),*args)
    private fun idle()=shadowOf(Looper.getMainLooper()).idle()
    @Before fun remember() {
        previousResources=PaintApplication.currentResources;previousLocale=Locale.getDefault()
        previousTag=AppLanguage.selectedTag(RuntimeEnvironment.getApplication())
    }
    @After fun restore() {
        AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
        PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
    }
    private fun inLocale(tag: String,run: (Activity)->Unit) {
        val controller=Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity=controller.setup().get()
        try {
            AppLanguage.select(activity,tag);AppLanguage.refresh(activity);Locale.setDefault(Locale.US)
            assertEquals(tag,AppLanguage.selectedTag(activity));run(activity)
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss();idle()
            controller.pause().stop().destroy()
        }
    }
    private fun texts(view: View): List<String> = when(view) {
        is ViewGroup -> (0 until view.childCount).flatMap { texts(view.getChildAt(it)) }
        is TextView -> listOf(view.text.toString())
        else -> emptyList()
    }
    @Test fun completeCompiledValuesAndBothPluralBranchesMatchFiniteReview() {
        for(tag in listOf("es-419","eo","en-001"))inLocale(tag) { activity ->
            val rows=fixture.getJSONObject("locales").getJSONObject(tag)
            for(identity in rows.keys()) {
                val (kind,key)=identity.split('/',limit=2);val value=row(tag,identity)
                val id=activity.resources.getIdentifier(key,kind,activity.packageName);assertNotEquals(identity,0,id)
                if(kind=="string")assertEquals(identity,value.getString("display"),activity.getString(id))
                else for(count in listOf(1,2)) {
                    val text=value.getJSONObject("display").getString(if (count == 1) "one" else "other")
                    assertEquals(text,activity.resources.getQuantityString(id,count))
                    assertEquals(String.format(Locale.forLanguageTag(tag),text,24,16,count),uiQuantity(activity.resources,id,count,24,16,count))
                }
            }
        }
    }
    @Test fun onePixelAndLargerDimensionsUseCountNeutralActualControls()=inLocale("es-419") { activity ->
        val controls=DimensionControls(activity,ImageDimensions(40,25),locked=false)
        for(size in listOf(ImageDimensions(1,1),ImageDimensions(2,1),ImageDimensions(2000,1000))) {
            controls.setDimensions(size)
            assertEquals(size,controls.dimensions)
            assertEquals(formatted("es-419","ui_d_d_px_d_pixels_2f_mp",size.width,size.height,size.pixels,size.pixels/1_000_000.0),
                controls.findViewWithTag<TextView>("size_result").text.toString())
        }
    }
    @Test fun residentAndEditingPressureCanRejectImportEvenWhenNativeFootprintFits()=inLocale("en-001") { activity ->
        val mib=1024L*1024;val budget=8*mib
        val policy=ImageMemoryPolicy.calculate(512*mib,0,(budget+32*mib)*3,0,true)
        assertEquals(budget,policy.workingBytes)
        val native=ImportMemoryRequirements(2*mib);val resident=2*mib
        val source=ImageDimensions(1600,1200);val smallest=ImportPlan.create(source,ImageDimensions(1,1))
        assertTrue(2*mib<budget);assertTrue(native.hasNativeWork)
        assertTrue(native.estimatedBytes(smallest,resident)>budget)
        assertFalse(native.accepts(policy,smallest,resident));assertNull(native.suggestResize(source,policy,resident))
        var resized=false;var cancelled=0
        val dialog=ImageResizeDialog(activity,source,resident,{policy},resize={resized=true},cancel={cancelled++},memoryRequirements=native).show()
        try {
            idle();val root=dialog.window!!.decorView
            val copy=formatted("en-001","ui_copy_decoded_image_at_this_size_estimated_loading",ImageDimensions(1,1).describe(),memoryLabel(4.0),memoryLabel(native.estimatedBytes(smallest,resident)))
            assertEquals(copy+"\n"+expected("en-001","ui_no_resize_fits_decoder_memory"),root.findViewWithTag<TextView>("resize_estimate").text.toString())
            assertFalse(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();assertFalse(resized);assertTrue(dialog.isShowing)
            dialog.cancel();idle();assertEquals(1,cancelled);assertEquals(ImageDimensions(1600,1200),source)
        } finally {dialog.dismiss();idle()}
    }
    @Test fun assemblyMinimumCanFailFromResidentPressureWithoutChangingItsDocument() {
        AppLanguage.select(RuntimeEnvironment.getApplication(),"en-001")
        val controller=Robolectric.buildActivity(AssemblyActivity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme);val activity=controller.setup().get()
        AppLanguage.refresh(activity)
        val source=File.createTempFile("ordinary-floor-",".png",activity.cacheDir)
        val bitmap=Bitmap.createBitmap(1,1,Bitmap.Config.ARGB_8888)
        try {
            source.outputStream().use {assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))}
            val sourceBytes=source.readBytes();val before=activity.assembly.images.toList();val layout=activity.assembly.layout()
            val budget=ImageMemoryPolicy.forDevice(activity).workingBytes;assertTrue(budget>0)
            val imported=ImportedImage(source,"tiny.png")
            assertTrue(imported.estimatedBytes(ImportPlan.create(ImageDimensions(1,1),ImageDimensions(1,1)),0)<budget)
            val image=AssemblyImage("tiny",source,"tiny.png",null,ImageDimensions(1,1),position=ImagePosition(0,0))
            val renderer=AssemblyRenderer(activity,listOf(image),mapOf("tiny" to Rect(0,0,1,1)),budget/4+1024*1024)
            assertFalse(renderer.fits(ImageDimensions(1,1)));assertNull(renderer.suggested())
            ReflectionHelpers.callInstanceMethod<Unit>(activity,"outputSizeDialog",ClassParameter.from(AssemblyRenderer::class.java,renderer),
                ClassParameter.from(Boolean::class.javaPrimitiveType!!,false),ClassParameter.from(ImageDimensions::class.java,null))
            idle();val dialog=checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
            assertEquals(expected("en-001","ui_assembly_source_memory_floor"),activity.lastError)
            assertTrue(texts(dialog.window!!.decorView).contains(expected("en-001","ui_assembly_source_memory_floor")))
            assertNull(dialog.window!!.decorView.findViewWithTag<View>("assembly_size_width"))
            assertEquals(before,activity.assembly.images);assertEquals(layout,activity.assembly.layout());assertArrayEquals(sourceBytes,source.readBytes())
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss();bitmap.recycle();source.delete()
            controller.pause().stop().destroy();idle()
        }
    }
    @Test fun actualOneAndTwoPageChooserKeepsRangeNavigationAndCancellation() {
        for(tag in listOf("es-419","eo"))inLocale(tag) { activity ->
            val worker=Executors.newSingleThreadExecutor();var selected=0;var cancelled=0;var failure: Throwable?=null
            var selection: ImportSelection?=null
            try {
                for(kind in listOf("PDF","TIFF"))for(count in listOf(1,2)) {
                    selection=ImportSelection(activity,worker,{0L},{selected++},{cancelled++},{failure=it})
                    // Real chooser isolated from native decoding; start() count1 route is separately source-bound.
                    ReflectionHelpers.setField(selection,"name","example.$kind")
                    ReflectionHelpers.callInstanceMethod<Unit>(selection,"showPages",ClassParameter.from(String::class.java,kind),ClassParameter.from(Int::class.javaPrimitiveType!!,count))
                    idle();val dialog=checkNotNull(ShadowAlertDialog.getLatestAlertDialog());val root=dialog.window!!.decorView
                    assertTrue(texts(root).contains(formatted(tag,"formats22_page_description",kind,"example.$kind",count)))
                    assertEquals(expected(tag,"formats22_select_page"),shadowOf(dialog).title.toString())
                    assertEquals(expected(tag,"formats22_open_page"),dialog.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                    val previous=root.findViewWithTag<View>("import_previous_page");val next=root.findViewWithTag<View>("import_next_page")
                    assertEquals(expected(tag,"formats22_previous_page"),previous.contentDescription)
                    assertEquals(expected(tag,"formats22_next_page"),next.contentDescription)
                    assertFalse(previous.isEnabled);assertEquals(count>1,next.isEnabled)
                    val field=root.findViewWithTag<EditText>("import_page_number");assertEquals(expected(tag,"formats22_page_number"),field.contentDescription)
                    field.setText((count+1).toString());idle();assertFalse(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
                    assertEquals(formatted(tag,"formats22_page_range",count),root.findViewWithTag<TextView>("import_page_status").text.toString())
                    field.setText(count.toString());idle();assertTrue(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
                    dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();idle();assertFalse(dialog.isShowing)
                }
                assertEquals(0,selected);assertEquals(4,cancelled);assertNull(failure)
            } finally {selection?.dispose();worker.shutdownNow();assertTrue(worker.awaitTermination(10,TimeUnit.SECONDS))}
        }
    }
    @Test fun realCropSelectionShowsConditionalAttachedImageWarningInBothQuantities()=inLocale("es-419") { activity ->
        val images=listOf("one","two").map {AssemblyImage(it,File(activity.cacheDir,"$it.image"),it,null,ImageDimensions(24,16))}
        var applied=false;val dialog=ImageCropDialog(activity,images,{null}) {applied=true}.show()
        try {
            idle();val root=dialog.window!!.decorView;val status=root.findViewWithTag<TextView>("crop_status")
            val display=row("es-419","plurals/ui_crop_preview_images").getJSONObject("display")
            fun check(count: Int) {assertEquals(String.format(Locale.forLanguageTag("es-419"),display.getString(if (count == 1) "one" else "other"),24,16,count),status.text.toString())}
            check(2);root.findViewWithTag<CheckBox>("crop_include_two").performClick();idle();check(1)
            root.findViewWithTag<View>("crop_none").performClick();dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();idle()
            assertFalse(applied);assertTrue(dialog.isShowing);assertEquals(expected("es-419","ui_choose_at_least_one_image"),status.text.toString())
            root.findViewWithTag<View>("crop_all").performClick();idle();check(2)
            assertEquals(listOf(Rect(0,0,24,16),Rect(0,0,24,16)),images.map {it.crop})
        } finally {dialog.dismiss();idle()}
    }
    @Test fun croppingOnlyMovesAttachedImagesWhenTheirParentEdgeChanges()=inLocale("es-419") { activity ->
        val directory=File(activity.cacheDir,"ordinary-crop-model").apply {mkdirs()}
        val assembly=ImageAssembly(directory)
        val originals=listOf("parent","child","independent").map { id ->
            val file=File(directory,"$id.image").apply {writeBytes(byteArrayOf(1,2,3))}
            AssemblyImage(id,file,id,null,ImageDimensions(24,16))
        }
        try {
            assembly.add(originals);assembly.place("parent",Attachment(null,null))
            assembly.place("child",Attachment("parent",SnapEdge.RIGHT));assembly.position("independent",100,100)
            val before=assembly.layout();assertEquals(24,before.getValue("child").left)
            assembly.crop("parent",Rect(0,0,12,16))
            assertEquals(12,assembly.layout().getValue("child").left)
            assertEquals(before.getValue("independent"),assembly.layout().getValue("independent"))
            assertEquals(Attachment("parent",SnapEdge.RIGHT),assembly.image("child").attachment)
            assembly.undo();assertEquals(before,assembly.layout())
            // Trimming only the parent's height does not move its right-attached child.
            assembly.crop("parent",Rect(0,0,24,8))
            assertEquals(before.getValue("child"),assembly.layout().getValue("child"))
            assertEquals(before.getValue("independent"),assembly.layout().getValue("independent"))
            originals.forEach {assertArrayEquals(byteArrayOf(1,2,3),it.file.readBytes())}
        } finally {directory.deleteRecursively()}
    }
    @Test fun coordinatedFixtureTargetDisplayAndHistoryChangesCannotAlterTheOracle() {
        for(tag in fixture.getJSONObject("locales").keys())for(key in fixture.getJSONObject("locales").getJSONObject(tag).keys()) {
            for(field in listOf("target","display","source","previous","scope","changed")) {
                val data=JSONObject(fixture.toString());data.getJSONObject("locales").getJSONObject(tag).getJSONObject(key).put(field,"forged")
                assertThrows(AssertionError::class.java) {OrdinaryPriorityExpectations.row(data,tag,key)}
            }
            val missing=JSONObject(fixture.toString());missing.getJSONObject("locales").getJSONObject(tag).getJSONObject(key).remove("previous")
            assertThrows(AssertionError::class.java) {OrdinaryPriorityExpectations.row(missing,tag,key)}
        }
    }
}
