/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.ContextWrapper
import android.content.res.Resources
import android.graphics.Color
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
import java.io.IOException
import org.robolectric.shadows.ShadowToast
import org.robolectric.util.ReflectionHelpers
import org.robolectric.util.ReflectionHelpers.ClassParameter
import java.io.File
import java.util.Base64
import java.util.Locale
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

/** Bounded compiled-resource and actual-consumer checks, not installed UI/fluency certification. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class AfrikaansRetainedPriorityWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    private val fixture by lazy {
        JSONObject(File("../tools/fixtures/current_localization/afrikaans_retained_priority_wording.json").readText())
    }
    private fun expected(tag: String, key: String): String {
        val raw=fixture.getJSONObject("accepted").getString(key)
        if(raw.startsWith("@string/")) {
            require(tag=="af" && key=="ui_save_a5d0d9" && raw=="@string/ui_save")
            return expected(tag,"ui_save")
        }
        return decoded(raw)
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
    private fun forEachLocale(tags: List<String> = listOf("af"), check: (String,Activity)->Unit) {
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

    @Test fun everyAcceptedAfrikaansCompleteValueAndPresentHoldKeepsItsDistinctScope() = forEachLocale { tag,activity ->
        val locale=fixture
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
        val held=fixture.getJSONObject("held_present")
        for(key in held.keys()) {
            val id=activity.resources.getIdentifier(key,"string",activity.packageName)
            assertEquals(decoded(held.getJSONObject(key).getString("value")),activity.getString(id))
        }
    }

    @Test fun memoryAdmissionStopsBeforeAllocationWithAllFourArguments() = forEachLocale { tag,_ ->
        val mib=1024L*1024;val policy=ImageMemoryPolicy.calculate(256*mib,0,96*mib,0,false)
        assertEquals(0L,policy.maxPixels())
        for((width,height) in listOf(1 to 1,1000 to 2000)) {
            val error=assertThrows(ImageSizeException::class.java) {policy.check(width,height)}
            assertEquals(formatted(tag,"ui_d_d_pixels_2f_mp_exceeds_the_current",width,height,width.toLong()*height/1_000_000.0,0.0),error.message)
        }
    }

    @Test fun completeCropPluralAndAccessiblePreviewTrackActualSelectionCounts() = forEachLocale { tag,activity ->
        val images=(1..3).map {i->AssemblyImage("image$i",File(activity.cacheDir,"$tag-$i.image"),"$i.png",null,ImageDimensions(24,16))}
        var applied=false
        val shown=ImageCropDialog(activity,images,{null}) {applied=true}.show()
        try {
            val root=shown.window!!.decorView;shadowOf(Looper.getMainLooper()).idle()
            assertEquals(expected(tag,"ui_image_shown_in_crop_preview"),root.findViewWithTag<View>("crop_preview_image").contentDescription.toString())
            val values=fixture.getJSONObject("accepted").getJSONObject("ui_crop_preview_images")
            fun check(count: Int) {
                val quantity=if(values.has("one") && (count==1)) "one" else "other"
                val pattern=decoded(values.getString(quantity))
                val text=String.format(Locale.forLanguageTag(tag),pattern,24,16,count)
                assertEquals(text,root.findViewWithTag<TextView>("crop_status").text.toString())
                assertEquals(text,uiQuantity(activity.resources,R.plurals.ui_crop_preview_images,count,24,16,count))
            }
            check(3);root.findViewWithTag<View>("crop_none").performClick();check(0)
            root.findViewWithTag<CheckBox>("crop_include_image1").isChecked=true;check(1)
            root.findViewWithTag<CheckBox>("crop_include_image2").isChecked=true;check(2)
            shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertFalse(applied);assertFalse(shown.isShowing)
            images.forEach {assertEquals(android.graphics.Rect(0,0,24,16),it.crop)}
        } finally {shown.dismiss()}
    }

    private fun texts(view: View): List<String> = (if(view is TextView) listOf(view.text.toString()) else emptyList()) +
        (if(view is ViewGroup) (0 until view.childCount).flatMap {texts(view.getChildAt(it))} else emptyList())

    @Test fun failedAtomicDestinationReplacementKeepsTheExistingTargetAndSourceBitmap()=forEachLocale { tag,activity ->
        val directory=File(activity.cacheDir,"afrikaans-target-${System.nanoTime()}").apply {mkdirs()}
        val image=Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.MAGENTA)}
        try {
            for(format in listOf(ImageFormat.BMP,ImageFormat.DIB,ImageFormat.ICO,ImageFormat.BASE64)) {
                val target=File(directory,"target.${format.extension}").apply {mkdirs()}
                val old=File(target,"existing").apply {writeText("original destination")}
                val error=assertThrows(IOException::class.java) {ImageExporter.encode(image,target,ExportOptions(format),64L*1024*1024)}
                assertEquals(expected(tag,"save20_destination_error"),error.message)
                assertEquals("original destination",old.readText());assertEquals(listOf(target.name),directory.listFiles()!!.map {it.name})
                assertFalse(image.isRecycled);assertEquals(Color.MAGENTA,image.getPixel(0,0));target.deleteRecursively()
            }
        } finally {image.recycle();directory.deleteRecursively()}
    }

    @Test fun actualSampledResizeDialogKeepsFullMemoryAndUnchangedOriginalExplanationOnCancel()=forEachLocale { tag,activity ->
        val mib=1024L*1024;val policy=ImageMemoryPolicy.calculate(256*mib,0,96*mib,0,false)
        var resized=false;var cancelled=0
        val dialog=ImageResizeDialog(activity,ImageDimensions(2000,1000),0,{policy},resize={resized=true},cancel={cancelled++}).show()
        shadowOf(Looper.getMainLooper()).idle() // Deliver onShow before checking its refresh/listeners.
        try {
            val root=dialog.window!!.decorView
            assertEquals(expected(tag,"ui_sampled_resize_memory_explanation"),root.findViewWithTag<TextView>("resize_explanation").text.toString())
            assertFalse(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertEquals(1,cancelled);assertFalse(resized);assertFalse(dialog.isShowing)
        } finally {dialog.dismiss()}
    }

    @Test fun actualHexadecimalFieldUsesTheFullLabelAndCancelDoesNotCommitAColour()=forEachLocale { tag,activity ->
        var commits=0
        val dialog=AdvancedColourDialog(activity,Color.RED,false,initialMode=1) {commits++}.show()
        try {
            val field=dialog.window!!.decorView.findViewWithTag<EditText>("colour_hex")
            assertEquals(expected(tag,"ui_hex_rrggbb"),field.contentDescription.toString())
            assertTrue(texts(dialog.window!!.decorView).contains(expected(tag,"ui_hex_rrggbb")))
            field.setText("#12AB34");shadowOf(Looper.getMainLooper()).idle();assertEquals(0,commits)
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertEquals(0,commits);assertFalse(dialog.isShowing)
        } finally {dialog.dismiss()}
    }

    @Test fun actualCreditEditorPreservesBothSourcesAndDraftOnSaveAndSizeFailures()=forEachLocale { tag,activity ->
        val credits=listOf(ImageCredit("https://example.com/a.png","first source and licence"),ImageCredit("https://example.com/b.png","second source and licence"))
        val before=ImageCredit.write(credits).toString()
        for(oversized in listOf(false,true)) {
            var attempts=0
            val session=checkNotNull(GalleryCredits.showEditor(activity,credits) {_,_->
                attempts++;if(oversized) throw IllegalArgumentException("test metadata bound") else throw IOException("test storage failure")
            })
            val dialog=session.dialog
            shadowOf(Looper.getMainLooper()).idle() // Install the real Save handler before clicking it.
            try {
                val field=dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text")
                field.setText("edited attribution 100%")
                dialog.getButton(AlertDialog.BUTTON_NEUTRAL).performClick();shadowOf(Looper.getMainLooper()).idle()
                assertEquals(expected(tag,if(oversized)"gallery_credit_too_large" else "gallery_credit_could_not_save"),ShadowToast.getTextOfLatestToast())
                assertEquals(1,attempts);assertTrue(dialog.isShowing);assertEquals("edited attribution 100%",field.text.toString())
                assertEquals(before,ImageCredit.write(credits).toString());assertEquals("edited attribution 100%",session.snapshot().text)
            } finally {dialog.dismiss()}
        }
    }

    private fun editor(check: (ClassicPaintActivity)->Unit) {
        val app=RuntimeEnvironment.getApplication() as Context
        app.filesDir.listFiles()?.filter {it.name.startsWith("classic-") }?.forEach {it.delete()}
        app.getSharedPreferences("classic-ui",0).edit().clear().commit();AppLanguage.select(app,"af")
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);val activity=controller.setup().get()
        try {
            awaitEditorStartup(activity);shadowOf(Looper.getMainLooper()).idle();Locale.setDefault(Locale.US);check(activity)
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss();controller.pause().stop()
            val end=System.nanoTime()+15_000_000_000L
            while(activity.busy&&System.nanoTime()<end) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(10)}
            assertFalse(activity.busy);controller.destroy()
        }
    }

    @Test fun returnToDrawingAndSingleColourStyleUseActualControlsWithoutRedrawing()=editor { activity ->
        activity.document.newImage(24,16);EditorTestNavigation.click(activity,"tool_BRUSH")
        val before=activity.document.bitmap.copy(Bitmap.Config.ARGB_8888,false)
        val dirty=activity.document.dirty;val undo=activity.document.canUndo;val redo=activity.document.canRedo
        try {
            repeat(2) {
                EditorTestNavigation.click(activity,"tool_ZOOM")
                val button=activity.window.decorView.findViewWithTag<TextView>("navigate_draw")
                assertEquals(expected("af","ui_draw_again"),button.text.toString());button.performClick();shadowOf(Looper.getMainLooper()).idle()
                assertEquals(PaintTool.BRUSH,activity.paintCanvas.tool);assertTrue(before.sameAs(activity.document.bitmap))
                assertEquals(dirty,activity.document.dirty);assertEquals(undo,activity.document.canUndo);assertEquals(redo,activity.document.canRedo)
            }
            EditorTestNavigation.click(activity,"tool_RECTANGLE")
            val choice=activity.window.decorView.findViewWithTag<TextView>("tool_option")
            assertTrue(choice.performClick());shadowOf(Looper.getMainLooper()).idle()
            val options=checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
            assertEquals(expected("af","ui_solid_fill"),options.listView.adapter.getItem(1).toString())
            options.listView.performItemClick(null,1,1L);shadowOf(Looper.getMainLooper()).idle()
            assertEquals(1,activity.document.shapeStyle);assertEquals(expected("af","ui_solid_fill"),choice.text.toString())
            assertFalse(options.isShowing)
            assertTrue(before.sameAs(activity.document.bitmap));assertEquals(undo,activity.document.canUndo);assertEquals(redo,activity.document.canRedo)
        } finally {before.recycle()}
    }

    @Test fun actualCanvasAndScaleDialogsKeepDistinctHelpAndTopLeftPixelsThroughUndo()=editor { activity ->
        activity.document.newImage(24,16);activity.document.bitmap.setPixel(0,0,Color.MAGENTA);activity.document.bitmap.setPixel(11,7,Color.GREEN)
        activity.document.bitmap.setPixel(20,4,Color.BLUE);activity.document.bitmap.setPixel(4,12,Color.YELLOW)
        fun show(stretch: Boolean): AlertDialog {
            ReflectionHelpers.callInstanceMethod<Void>(activity,"dimensionsDialog",ClassParameter.from(Boolean::class.javaPrimitiveType!!,stretch),ClassParameter.from(Boolean::class.javaPrimitiveType!!,false))
            val dialog=checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
            shadowOf(Looper.getMainLooper()).idle() // Deliver the real Apply onShow handler.
            return dialog
        }
        for(stretch in listOf(true,false)) {
            val dialog=show(stretch)
            assertTrue(texts(dialog.window!!.decorView).contains(expected("af",if (stretch) "ui_scales_the_image_unlock_the_ratio_to_stretch" else "ui_keeps_pixels_at_the_top_left_smaller_canvas")))
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();assertEquals(24,activity.document.bitmap.width);assertEquals(16,activity.document.bitmap.height)
        }
        val before=activity.document.bitmap.copy(Bitmap.Config.ARGB_8888,false)
        try {
            for((width,height) in listOf(12 to 16,24 to 8)) {
                // Clip only one axis at a time: each cut removes a marked pixel.
                assertEquals(Color.BLUE,before.getPixel(20,4));assertEquals(Color.YELLOW,before.getPixel(4,12))
                val dialog=show(false);val root=dialog.window!!.decorView
                root.findViewWithTag<EditText>("size_width").setText(width.toString())
                root.findViewWithTag<EditText>("size_height").setText(height.toString())
                dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
                assertEquals(width,activity.document.bitmap.width);assertEquals(height,activity.document.bitmap.height)
                val surviving=Bitmap.createBitmap(before,0,0,width,height)
                try {assertTrue(surviving.sameAs(activity.document.bitmap))} finally {surviving.recycle()}
                if(width==12)assertEquals(Color.YELLOW,activity.document.bitmap.getPixel(4,12))
                else assertEquals(Color.BLUE,activity.document.bitmap.getPixel(20,4))
                ReflectionHelpers.callInstanceMethod<Void>(activity,"undoEdit");shadowOf(Looper.getMainLooper()).idle()
                assertEquals(24,activity.document.bitmap.width);assertEquals(16,activity.document.bitmap.height)
                assertTrue(before.sameAs(activity.document.bitmap))
                assertEquals(Color.BLUE,activity.document.bitmap.getPixel(20,4));assertEquals(Color.YELLOW,activity.document.bitmap.getPixel(4,12))
            }
        } finally {before.recycle()}

    }
}
