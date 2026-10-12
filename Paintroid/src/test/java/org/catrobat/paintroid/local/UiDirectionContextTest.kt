/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.content.Context
import android.content.res.Configuration
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.os.Looper
import android.util.DisplayMetrics
import android.graphics.Rect
import android.view.Display
import android.view.ContextThemeWrapper
import android.view.View
import android.widget.HorizontalScrollView
import android.widget.LinearLayout
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.LooperMode
import org.robolectric.android.controller.ActivityController
import org.robolectric.shadows.ShadowDisplayManager
import java.util.Locale
import java.util.concurrent.TimeUnit

/** The selected resource locale must survive an unrelated process-default reset.
 * Controlled JVM regression, complementary to the unchanged installed native-input cases.
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="en-rUS-w320dp-h640dp-port-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class UiDirectionContextTest {
    @Test fun literaryChineseUiStaysVerticalWhenProcessDefaultIsHorizontal()=checkMismatch("lzh-Hant",true,true)
    @Test fun manchuUiStaysVerticalWhenProcessDefaultIsHorizontal()=checkMismatch("mnc-Mong",true,false)
    @Test fun verticalEnglishUiStaysVerticalWhenProcessDefaultIsHorizontal()=checkMismatch("en-XV",true,false)
    @Test fun verticalEmojiUiStaysVerticalWhenProcessDefaultIsHorizontal()=checkMismatch("qaa-Zsye-XV",true,true)
    @Test fun horizontalUiStaysHorizontalWhenProcessDefaultIsVertical()=checkMismatch("en-US",false,false)

    private fun idle()=shadowOf(Looper.getMainLooper()).idle()
    private fun opposite(vertical: Boolean)=Locale.forLanguageTag(if(vertical) "en-US" else "lzh-Hant")
    private data class Frame(val width: Int,val height: Int,val pixels: IntArray)
    private fun frame(view: TextView): Frame {
        view.requestLayout()
        val spec=View.MeasureSpec.makeMeasureSpec(512,View.MeasureSpec.AT_MOST)
        view.measure(spec,spec);view.layout(0,0,view.measuredWidth,view.measuredHeight)
        val bitmap=Bitmap.createBitmap(view.width,view.height,Bitmap.Config.ARGB_8888)
        return try {
            view.draw(Canvas(bitmap))
            val pixels=IntArray(bitmap.width*bitmap.height)
            bitmap.getPixels(pixels,0,bitmap.width,0,0,bitmap.width,bitmap.height)
            Frame(bitmap.width,bitmap.height,pixels)
        } finally {bitmap.recycle()}
    }
    private fun widgets(context: Context)=listOf<TextView>(
        FlowButton(context).apply {background=null;columnHeightDp=96},
        FlowTextView(context).apply {columnHeightDp=96}
    ).onEach {it.text="Sample 95\nNative text";it.contentDescription=it.text}

    private fun checkMismatch(tag: String,vertical: Boolean,rtl: Boolean)=withEditor(tag) {controller ->
        val activity=controller.get()
        val views=widgets(activity)
        val host=LinearLayout(activity).apply {orientation=LinearLayout.HORIZONTAL}
        views.forEach {host.addView(it)}
        activity.setContentView(host)
        awaitUi("Attached widget host") {host.width>0 && views.all {it.isAttachedToWindow && it.width>0 && it.height>0}}
        val before=views.map(::frame)
        Locale.setDefault(opposite(vertical))
        assertEquals(tag,activity.resources.configuration.locales[0].toLanguageTag())
        assertNotEquals(Locale.getDefault(),activity.resources.configuration.locales[0])
        views.forEachIndexed {index,view ->
            val after=frame(view)
            assertEquals("Resource-bound width: $tag",before[index].width,after.width)
            assertEquals("Resource-bound height: $tag",before[index].height,after.height)
            assertArrayEquals("Same UI ink after an unrelated default reset: $tag",before[index].pixels,after.pixels)
            assertEquals("Native accessibility keeps the full text",view.text.toString(),view.createAccessibilityNodeInfo().text.toString())
            if(vertical) assertNull("Still the vertical renderer",view.layout)
            else assertNotNull("Still the native horizontal renderer",view.layout)
        }
        // Construct with the opposite process default already in force, then let
        // the real posted dialog mount run. Neither step may consult that default.
        checkSave(activity,vertical,rtl)
        // Separately change the default between content construction and mount.
        Locale.setDefault(Locale.forLanguageTag(tag))
        val dialog=SaveOptionsDialog(activity,ExportOptions(),confirm={},cancel={}).show()
        Locale.setDefault(opposite(vertical))
        try {idle();assertSave(dialog,vertical,rtl)} finally {dialog.dismiss();idle()}
    }

    private fun checkSave(activity: ClassicPaintActivity,vertical: Boolean,rtl: Boolean) {
        val dialog=SaveOptionsDialog(activity,ExportOptions(),confirm={},cancel={}).show()
        try {idle();assertSave(dialog,vertical,rtl)} finally {dialog.dismiss();idle()}
    }
    private fun assertSave(dialog: AlertDialog,vertical: Boolean,rtl: Boolean) {
        val root=dialog.window!!.decorView
        awaitUi("Completed native Save layout") {
            root.width>0 && root.height>0 && !root.isLayoutRequested &&
                (!vertical || root.findViewWithTag<View>("vertical_dialog_columns")?.width?.let {it>0}==true)
        }
        val form=root.findViewWithTag<View>("vertical_save_form")
        val columns=root.findViewWithTag<HorizontalScrollView>("vertical_dialog_columns")
        assertEquals("Save form matches its resource locale",vertical,form!=null)
        assertEquals("Deferred dialog shell matches the same locale",vertical,columns!=null)
        assertTrue(root.findViewWithTag<View>("export_filename").isShown)
        val slider=root.findViewWithTag<NumericSlider>("export_quality")
        assertEquals("Slider and its FlowButton use one direction",if(vertical) LinearLayout.HORIZONTAL else LinearLayout.VERTICAL,slider.orientation)
        if(vertical) {
            assertTrue("Laid-out vertical form",form!!.height>0)
            assertTrue("Laid-out vertical columns",columns!!.width>0)
            val maximum=(columns.getChildAt(0).width-columns.width+columns.paddingLeft+columns.paddingRight).coerceAtLeast(0)
            assertEquals("Native initial reading column",if(rtl) maximum else 0,columns.scrollX)
        }
        for(which in listOf(AlertDialog.BUTTON_POSITIVE,AlertDialog.BUTTON_NEGATIVE)) {
            val button=dialog.getButton(which)
            assertTrue("Real dialog action retained",button.isShown && button.text.isNotEmpty())
        }
    }

    @Test fun rotationAndRecreationPreserveSelectedDirectionDespiteLaterDefaultReset() {
        for((tag,vertical,rtl) in listOf(
                Triple("lzh-Hant",true,true),Triple("mnc-Mong",true,false),
                Triple("en-XV",true,false),Triple("qaa-Zsye-XV",true,true),Triple("en-US",false,false))) {
            withEditor(tag) {controller ->
                var activity=controller.get()
                activity.document.newImage(17,11)
                activity.document.bitmap.setPixel(3,4,Color.MAGENTA)
                activity.document.markSaved();activity.paintCanvas.fit()
                val document=activity.document
                val original=Configuration(activity.resources.configuration)
                for(landscape in listOf(true,false)) {
                    val changed=Configuration(original).apply {
                        orientation=if(landscape) Configuration.ORIENTATION_LANDSCAPE else Configuration.ORIENTATION_PORTRAIT
                        screenWidthDp=if(landscape) 640 else 320
                        screenHeightDp=if(landscape) 320 else 640
                    }
                    val metrics=DisplayMetrics().apply {
                        setTo(activity.resources.displayMetrics)
                        widthPixels=(changed.screenWidthDp*density+.5f).toInt()
                        heightPixels=(changed.screenHeightDp*density+.5f).toInt()
                    }
                    val changes=Configuration(activity.resources.configuration).diff(changed)
                    controller.configurationChange(changed,metrics,changes)
                    ShadowDisplayManager.changeDisplay(Display.DEFAULT_DISPLAY,
                        "+w${changed.screenWidthDp}dp-h${changed.screenHeightDp}dp-${if(landscape) "land" else "port"}")
                    controller.visible()
                    val decor=activity.window.decorView
                    awaitUi("Rotated editor window") {
                        decor.width>0 && decor.height>0 && (decor.width>decor.height)==landscape && !decor.isLayoutRequested
                    }
                    val visible=Rect();assertTrue(decor.getLocalVisibleRect(visible))
                    assertEquals("Display-backed root width",decor.width,visible.width())
                    assertEquals("Display-backed root height",decor.height,visible.height())
                    assertSame("Rotation retains the editor",activity,controller.get())
                    assertSame("Rotation retains the document",document,activity.document)
                    assertEquals(changed.orientation,activity.resources.configuration.orientation)
                    // Deliberately reset AFTER callback refresh, matching the race
                    // under investigation without relying on a scheduler accident.
                    Locale.setDefault(opposite(vertical))
                    assertWorkspaceAndSave(activity,tag,vertical,rtl)
                }
                // Flush the normal onStop save before the framework recreation;
                // do not substitute a new image after the replacement is created.
                controller.pause().stop();awaitNotBusy(activity)
                controller.recreate();activity=controller.get()
                controller.restart().resume().visible();awaitEditorStartup(activity)
                Locale.setDefault(opposite(vertical))
                assertEquals(17,activity.document.bitmap.width)
                assertEquals(11,activity.document.bitmap.height)
                assertEquals(Color.MAGENTA,activity.document.bitmap.getPixel(3,4))
                assertWorkspaceAndSave(activity,tag,vertical,rtl)
            }
        }
    }
    private fun assertWorkspaceAndSave(activity: ClassicPaintActivity,tag: String,vertical: Boolean,rtl: Boolean) {
        assertEquals(tag,AppLanguage.selectedTag(activity))
        assertEquals(tag,activity.resources.configuration.locales[0].toLanguageTag())
        assertEquals(opposite(vertical),Locale.getDefault())
        val root=activity.window.decorView
        assertEquals("Workspace scaffold follows resources",vertical,root.findViewWithTag<View>("vertical_status_rail")!=null)
        val file=root.findViewWithTag<TextView>("menu_File")
        file.requestLayout()
        awaitUi("Reflowed resource-bound ribbon") {file.width>0 && file.height>0 && !file.isLayoutRequested}
        if(vertical) assertNull("Retained vertical ribbon renderer",file.layout)
        else assertNotNull("Retained horizontal ribbon renderer",file.layout)
        checkSave(activity,vertical,rtl)
    }

    @Test @Config(sdk=[21,24]) @GraphicsMode(GraphicsMode.Mode.LEGACY)
    fun legacyResourceContextsDoNotNeedProcessDefaultOrApi24LocaleList() {
        val before=Locale.getDefault()
        val base=RuntimeEnvironment.getApplication() as Context
        try {
            val localized=base.createConfigurationContext(Configuration().apply {setLocale(Locale.forLanguageTag("lzh-Hant"))})
            val context=ContextThemeWrapper(localized,R.style.ClassicPaintTheme)
            Locale.setDefault(Locale.US)
            for(view in widgets(context)) {
                val spec=View.MeasureSpec.makeMeasureSpec(512,View.MeasureSpec.AT_MOST)
                view.measure(spec,spec);view.layout(0,0,view.measuredWidth,view.measuredHeight)
                assertTrue(view.width>0 && view.height>0)
                assertNull("Selected vertical context on legacy Android",view.layout)
            }
        } finally {Locale.setDefault(before)}
    }

    private fun awaitUi(label: String,ready: ()->Boolean) {
        val until=System.nanoTime()+TimeUnit.SECONDS.toNanos(3)
        while(!ready() && System.nanoTime()<until) {
            shadowOf(Looper.getMainLooper()).idleFor(16,TimeUnit.MILLISECONDS)
            if(!ready()) Thread.sleep(1)
        }
        assertTrue(label,ready())
    }
    private fun awaitNotBusy(activity: ClassicPaintActivity) {
        val until=System.nanoTime()+TimeUnit.SECONDS.toNanos(10)
        while(activity.busy && System.nanoTime()<until) {idle();Thread.sleep(5)}
        assertFalse("Normal editor I/O completed",activity.busy)
        assertNull(activity.lastAutosaveError)
    }
    private fun withEditor(tag: String,check: (ActivityController<ClassicPaintActivity>)->Unit) {
        val app=RuntimeEnvironment.getApplication() as Context
        val oldLocale=Locale.getDefault();val oldTag=AppLanguage.selectedTag(app)
        val oldResources=PaintApplication.currentResources
        app.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {it.delete()}
        app.getSharedPreferences("classic-ui",0).edit().clear().commit()
        AppLanguage.select(app,tag)
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        try {awaitEditorStartup(controller.get());check(controller)}
        finally {
            try {controller.pause().stop();awaitNotBusy(controller.get())}
            finally {
                try {controller.destroy()}
                finally {AppLanguage.select(app,oldTag);PaintApplication.currentResources=oldResources;Locale.setDefault(oldLocale)}
            }
        }
    }
}
