/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.Activity
import android.app.Instrumentation
import android.app.LocaleManager
import android.content.Intent
import android.content.pm.ActivityInfo
import android.content.res.Configuration
import android.graphics.Rect
import android.graphics.Color
import android.os.Build
import android.os.Handler
import android.os.LocaleList
import android.os.Looper
import android.os.SystemClock
import android.view.KeyEvent
import android.view.View
import android.view.ViewGroup
import android.view.inspector.WindowInspector
import android.widget.Button
import android.widget.EditText
import android.widget.HorizontalScrollView
import android.widget.ListView
import android.widget.ScrollView
import android.widget.Spinner
import android.widget.TextView
import androidx.lifecycle.Lifecycle
import androidx.test.core.app.ActivityScenario
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.SdkSuppress
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.runner.lifecycle.ActivityLifecycleCallback
import androidx.test.runner.lifecycle.ActivityLifecycleMonitorRegistry
import androidx.test.runner.lifecycle.Stage
import androidx.test.uiautomator.UiDevice
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.PaintTool
import org.catrobat.paintroid.classic.ToolCategoryButton
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.util.concurrent.CopyOnWriteArrayList
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicReference

/**
 * Installed Android input coverage, separate from the programmatic/Robolectric
 * layout checks. All ribbon, tool, dialog and format actions use screen taps or
 * swipes. Only initial fixture setup, orientation and picker viewport positioning
 * are programmatic. No clipboard, remote gallery, save destination or encoding is
 * involved. Screenshots show the emulator; they are not physical-device evidence.
 */
@RunWith(AndroidJUnit4::class)
@SdkSuppress(minSdkVersion=29)
class VerticalLocaleDeviceTest {
    private val instrumentation=InstrumentationRegistry.getInstrumentation()
    private val context get()=instrumentation.targetContext
    private val device get()=UiDevice.getInstance(instrumentation)
    private lateinit var scenario: ActivityScenario<ClassicPaintActivity>
    private lateinit var activity: ClassicPaintActivity
    private var originalLanguageTag=""
    private var originalOrientation=ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
    private var evidenceName="setup"
    private val externalRequests=CopyOnWriteArrayList<Intent>()
    private val monitor=object: Instrumentation.ActivityMonitor() {
        override fun onStartActivity(intent: Intent): Instrumentation.ActivityResult? {
            if(intent.action !in listOf(Intent.ACTION_CREATE_DOCUMENT,Intent.ACTION_OPEN_DOCUMENT,
                    Intent.ACTION_GET_CONTENT,Intent.ACTION_CHOOSER)) return null
            externalRequests.add(Intent(intent))
            return Instrumentation.ActivityResult(Activity.RESULT_CANCELED,null)
        }
    }
    private val lifecycleCallback=ActivityLifecycleCallback { observed,stage ->
        if(observed is ClassicPaintActivity && stage==Stage.CREATED) activity=observed
    }

    @Before fun launchInstalledApp() {
        assertEquals("paint.anpaint.android",context.packageName)
        originalLanguageTag=if(Build.VERSION.SDK_INT>=33)
            context.getSystemService(LocaleManager::class.java).applicationLocales.toLanguageTags()
        else context.getSharedPreferences("app-language",0).getString("language-tag","").orEmpty()
        instrumentation.runOnMainSync {
            ActivityLifecycleMonitorRegistry.getInstance().addLifecycleCallback(lifecycleCallback)
        }
        instrumentation.addMonitor(monitor)
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {it.delete()}
        listOf("classic-ui","recent-colours","export").forEach {
            context.getSharedPreferences(it,0).edit().clear().commit()
        }
        val launch=context.packageManager.getLaunchIntentForPackage(context.packageName)
        assertNotNull(launch)
        scenario=ActivityScenario.launch(launch!!)
        scenario.onActivity {activity=it;originalOrientation=it.requestedOrientation}
        awaitState("initial editor") {!activity.busy && activity.paintCanvas.width>0}
        onMain {
            activity.document.newImage(100,100)
            activity.document.bitmap.setPixel(4,7,Color.MAGENTA)
            activity.document.bitmap.setPixel(81,63,Color.CYAN)
            activity.document.markSaved();activity.paintCanvas.fit()
        }
        orient(false)
    }

    @After fun closeInstalledApp() {
        try {
            if(::scenario.isInitialized && ::activity.isInitialized && !activity.isDestroyed) {
                if(onMain {saveRoot()!=null || pickerList()!=null || formatList()!=null}) {
                    instrumentation.sendKeyDownUpSync(KeyEvent.KEYCODE_BACK)
                    instrumentation.waitForIdleSync()
                }
                onMain {activity.requestedOrientation=originalOrientation}
                instrumentation.waitForIdleSync()
                scenario.moveToState(Lifecycle.State.CREATED)
                awaitState("pending save before close") {!activity.busy}
                // Preserve EditorDeviceTest's completed-autosave teardown: avoid
                // the AndroidX EmptyActivity double-resume 45-second timeout.
                onMain {activity.finish()}
                awaitState("finished editor") {activity.isDestroyed}
                scenario.close()
            }
        } finally {
            instrumentation.removeMonitor(monitor)
            instrumentation.runOnMainSync {
                ActivityLifecycleMonitorRegistry.getInstance().removeLifecycleCallback(lifecycleCallback)
                context.getSharedPreferences("app-language",0).edit()
                    .putString("language-tag",originalLanguageTag).putBoolean("platform-initialized",true).commit()
                if(Build.VERSION.SDK_INT>=33) context.getSystemService(LocaleManager::class.java)
                    .applicationLocales=LocaleList.forLanguageTags(originalLanguageTag)
            }
            instrumentation.waitForIdleSync()
        }
    }

    @Test fun manchuPickerRibbonToolsAndJpegUseNativeInputInBothOrientations()=checkLocale("mnc-Mong",false)
    @Test fun literaryChinesePickerRibbonToolsAndJpegUseNativeInputInBothOrientations()=checkLocale("lzh-Hant",true)
    @Test fun verticalEnglishPickerRibbonToolsAndJpegUseNativeInputInBothOrientations()=checkLocale("en-XV",false)
    @Test fun verticalEmojiPickerRibbonToolsAndJpegUseNativeInputInBothOrientations()=checkLocale("qaa-Zsye-XV",true)

    private fun checkLocale(tag: String,rightToLeft: Boolean) {
        evidenceName=tag
        val started=SystemClock.uptimeMillis()
        try {
            chooseLanguage(tag)
            var overflowToolSwipes=0
            for(landscape in listOf(false,true)) {
                val orientation=if(landscape) "landscape" else "portrait"
                evidenceName="$tag-$orientation"
                orient(landscape)
                for(tab in listOf("View","Draw","File","Edit","Color")) {
                    selectTab(tab)
                    assertCanvas(tag)
                }
                selectTab("Draw")
                // Opening Insert must be a native category tap. Switch to Brush
                // first in the second orientation so Insert opens rather than
                // toggling a previously retained category closed.
                tap("Brush category") {root().findViewWithTag<View>("category_BRUSH")}
                tap("Insert category") {root().findViewWithTag<View>("category_INSERT")}
                awaitState("Insert category opened") {
                    root().findViewWithTag<ToolCategoryButton>("category_INSERT").expanded &&
                        root().findViewWithTag<View>("tool_ARROW").isShown
                }
                // Insert remembers the previous orientation's selected tool.
                // Establish a different real selection so the Arrow assertion
                // cannot pass merely because the injected tap missed its target.
                tap("Line tool precondition") {root().findViewWithTag<View>("tool_LINE")}
                awaitState("Line selected before Arrow") {activity.paintCanvas.tool==PaintTool.LINE}
                val swipes=tap("offscreen Arrow tool") {root().findViewWithTag<View>("tool_ARROW")}
                overflowToolSwipes+=swipes
                android.util.Log.i("VerticalLocaleDeviceTest","$evidenceName Arrow native_swipes=$swipes")
                awaitState("Arrow tool selected by native input") {activity.paintCanvas.tool==PaintTool.ARROW}
                assertCanvas(tag)
                screenshot("workspace")
                selectTab("File")
                // Check initial ribbon column order before moving it to Save as.
                assertInitialColumns(onMain {
                    root().findViewWithTag<View>("panel_File_commands").parent as HorizontalScrollView
                },rightToLeft,"File ribbon")
                openSave()
                assertInitialColumns(onMain {
                    saveRoot()!!.findViewWithTag<HorizontalScrollView>("vertical_dialog_columns")
                },rightToLeft,"Save dialog")
                screenshot("save-initial")
                tap("native format spinner") {saveRoot()!!.findViewWithTag<View>("export_format")}
                awaitState("native format popup") {formatList()!=null}
                screenshot("format-popup")
                tapJpeg()
                awaitState("JPEG selected") {
                    saveRoot()?.findViewWithTag<Spinner>("export_format")?.selectedItem?.toString()=="JPEG"
                }
                onMain {
                    val dialog=saveRoot()!!
                    assertTrue("JPEG updates the native filename",dialog.findViewWithTag<EditText>("export_filename").text.toString().endsWith(".jpg"))
                    assertEquals("JPEG exposes quality",View.VISIBLE,dialog.findViewWithTag<View>("export_quality").visibility)
                    assertEquals("JPEG has no lossless toggle",View.GONE,dialog.findViewWithTag<View>("export_lossless").visibility)
                }
                // Physically reveal the quality control too; visibility in an
                // offscreen column alone would not establish reachability.
                reveal("JPEG quality") {saveRoot()!!.findViewWithTag<View>("export_quality")}
                screenshot("jpeg-quality")
                tap("Cancel Save") {saveRoot()!!.findViewById<View>(android.R.id.button2)}
                awaitState("native Cancel dismissed Save") {saveRoot()==null}
                assertCanvas(tag)
                openSave()
                onMain {assertEquals("Cancelled format is not persisted","PNG",saveRoot()!!.findViewWithTag<Spinner>("export_format").selectedItem.toString())}
                instrumentation.sendKeyDownUpSync(KeyEvent.KEYCODE_BACK)
                awaitState("native Back dismissed reopened Save") {saveRoot()==null}
                assertCanvas(tag)
                assertTrue("Navigation and cancellation launch no external destination",externalRequests.isEmpty())
            }
            assertTrue("The locale matrix exercised a genuinely offscreen tool with native swipes",overflowToolSwipes>0)
        } catch(failure: Throwable) {
            try {screenshot("failure")} catch(captureFailure: Throwable) {failure.addSuppressed(captureFailure)}
            throw failure
        } finally {
            android.util.Log.i("VerticalLocaleDeviceTest","$tag duration_ms=${SystemClock.uptimeMillis()-started}")
        }
    }

    private fun orient(landscape: Boolean) {
        val expected=if(landscape) Configuration.ORIENTATION_LANDSCAPE else Configuration.ORIENTATION_PORTRAIT
        onMain {activity.requestedOrientation=if(landscape) ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE else ActivityInfo.SCREEN_ORIENTATION_PORTRAIT}
        awaitState("${if(landscape) "landscape" else "portrait"} workspace layout") {
            activity.resources.configuration.orientation==expected && root().width>0 &&
                (root().width>root().height)==landscape && activity.paintCanvas.width>0 && !activity.busy
        }
        instrumentation.waitForIdleSync()
    }

    private fun chooseLanguage(tag: String) {
        selectTab("View")
        tap("Languages command") {command("View",R.string.ui_languages23)}
        awaitState("native locale picker") {pickerList()!=null}
        val index=onMain {
            val tags=activity.resources.getStringArray(R.array.app_language_tags).toList()
            assertTrue("Exact locale is offered: $tag",tag in tags)
            (tags.indexOf(tag)+1).also {pickerList()!!.setSelection(it)}
        }
        awaitState("exact picker row laid out") {
            pickerList()?.let {list -> list.getChildAt(index-list.firstVisiblePosition)?.height?.let {it>0}}==true
        }
        tap("locale row $tag") {
            val list=pickerList()!!
            (list.getChildAt(index-list.firstVisiblePosition) as TextView).also {
                assertTrue("Exact picker row text",it.text.toString().endsWith("[$tag]"))
            }
        }
        awaitState("recreated $tag activity") {
            activity.resources.configuration.locales[0].toLanguageTag()==tag &&
                root().findViewWithTag<View>("vertical_status_rail")?.isShown==true && !activity.busy
        }
        onMain {assertEquals(tag,activity.getSharedPreferences("app-language",0).getString("language-tag",null))}
        assertCanvas(tag)
    }

    private fun selectTab(name: String) {
        tap("$name tab") {root().findViewWithTag<View>("menu_$name")}
        awaitState("$name panel selected") {
            val tag=when(name) {"Draw"->"primary_tools";"Color"->"colour_dock";else->"panel_${name}_commands"}
            root().findViewWithTag<View>("menu_$name").isSelected && root().findViewWithTag<View>(tag).isShown
        }
        onMain {
            for(other in listOf("View","Draw","File","Edit","Color"))
                assertEquals("Only requested tab selected",other==name,root().findViewWithTag<View>("menu_$other").isSelected)
        }
    }

    private fun openSave() {
        tap("Save as command") {command("File",R.string.save20_title)}
        awaitState("native vertical Save layout") {
            saveRoot()?.findViewWithTag<View>("vertical_save_form")?.height?.let {it>0}==true &&
                saveRoot()?.findViewWithTag<View>("vertical_dialog_columns")?.width?.let {it>0}==true
        }
        instrumentation.waitForIdleSync()
    }

    private fun assertInitialColumns(columns: HorizontalScrollView,rtl: Boolean,label: String)=onMain {
        val maximum=(columns.getChildAt(0).width-columns.width+columns.paddingLeft+columns.paddingRight).coerceAtLeast(0)
        assertTrue("$label has columns",columns.getChildAt(0).width>0)
        assertEquals("$label starts at the first ${if(rtl) "right" else "left"} reading column",if(rtl) maximum else 0,columns.scrollX)
    }

    private fun assertCanvas(tag: String)=onMain {
        assertEquals(tag,activity.resources.configuration.locales[0].toLanguageTag())
        assertTrue(root().findViewWithTag<View>("vertical_status_rail").isShown)
        assertTrue("Usable canvas width",activity.paintCanvas.width>=48*activity.resources.displayMetrics.density)
        assertTrue("Usable canvas height",activity.paintCanvas.height>=48*activity.resources.displayMetrics.density)
        assertEquals(100,activity.document.bitmap.width);assertEquals(100,activity.document.bitmap.height)
        assertEquals(Color.MAGENTA,activity.document.bitmap.getPixel(4,7))
        assertEquals(Color.CYAN,activity.document.bitmap.getPixel(81,63))
        assertNull(activity.lastIoError)
    }

    private fun root()=activity.window.decorView
    private fun saveRoot(): View?=WindowInspector.getGlobalWindowViews().lastOrNull {
        it.isShown && it.findViewWithTag<View>("export_filename")!=null
    }
    private fun pickerList(): ListView?=windowList {list ->
        list.count==activity.resources.getStringArray(R.array.app_language_tags).size+1
    }
    private fun formatList(): ListView?=windowList {list ->
        (0 until list.count).any {list.getItemAtPosition(it).toString()=="JPEG"}
    }
    private fun windowList(accept: (ListView)->Boolean): ListView? =
        WindowInspector.getGlobalWindowViews().asReversed().firstNotNullOfOrNull {window ->
            descend(window) {it is ListView && it.isShown && accept(it)} as? ListView
        }
    private fun command(group: String,stringId: Int): View = descend(root()) {
        it is Button && it.tag?.toString()?.startsWith("command_${group}_")==true &&
            it.text.toString()==activity.getString(stringId)
    } ?: throw AssertionError("Missing command $group/$stringId")
    private fun descend(view: View,predicate: (View)->Boolean): View? {
        if(predicate(view)) return view
        if(view is ViewGroup) for(i in 0 until view.childCount) descend(view.getChildAt(i),predicate)?.let {return it}
        return null
    }

    private fun tapJpeg() {
        repeat(8) {
            val row=onMain {formatList()?.let {list ->descend(list) {it is TextView && it.text.toString()=="JPEG"}}}
            if(row!=null && onMain {usableBounds(row)!=null}) {
                tap("native JPEG row") {row}
                return
            }
            val bounds=onMain {val list=formatList() ?: throw AssertionError("JPEG popup vanished");visibleBounds(list)}
            swipe(bounds,horizontal=false,direction=1)
        }
        throw AssertionError("JPEG row not reachable with native popup scrolling")
    }

    /** Return screen-space bounds, intersected with all parent clipping. */
    private fun visibleBounds(view: View): Rect {
        val bounds=Rect()
        if(!view.getGlobalVisibleRect(bounds)) return bounds
        val location=IntArray(2);view.rootView.getLocationOnScreen(location)
        bounds.offset(location[0],location[1]);return bounds
    }
    private fun rawBounds(view: View): Rect {
        val location=IntArray(2);view.getLocationOnScreen(location)
        return Rect(location[0],location[1],location[0]+view.width,location[1]+view.height)
    }
    private fun usableBounds(view: View): Rect? {
        if(!view.isShown || view.width==0 || view.height==0) return null
        val visible=visibleBounds(view);val raw=rawBounds(view)
        val minimum=(32*view.resources.displayMetrics.density).toInt()
        return visible.takeIf {it.width()>=minOf(view.width,minimum) && it.height()>=minOf(view.height,minimum) &&
            it.contains(raw.centerX(),raw.centerY())}
    }
    private fun tap(label: String,target: ()->View): Int {
        val swipes=reveal(label,target)
        val bounds=onMain {usableBounds(target()) ?: throw AssertionError("Target moved before tap: $label")}
        assertTrue("Native tap: $label",device.click(bounds.centerX(),bounds.centerY()))
        instrumentation.waitForIdleSync()
        return swipes
    }
    private data class Gesture(val bounds: Rect,val horizontal: Boolean,val direction: Int)
    private fun reveal(label: String,target: ()->View): Int {
        awaitState("ready for $label") {!activity.busy}
        repeat(24) {attempt ->
            instrumentation.waitForIdleSync()
            if(onMain {usableBounds(target())!=null}) return attempt
            val gesture=onMain {
                val view=target();assertTrue("Shown target: $label",view.isShown)
                val targetBounds=rawBounds(view)
                var parent: View?=view.parent as? View
                var next: Gesture?=null
                while(parent!=null && next==null) {
                    val candidate=parent
                    val bounds=visibleBounds(candidate)
                    if(!bounds.isEmpty) {
                        if(candidate is HorizontalScrollView) {
                            val direction=when {
                                targetBounds.centerX()<bounds.left -> -1
                                targetBounds.centerX()>=bounds.right -> 1
                                targetBounds.left<bounds.left -> -1
                                targetBounds.right>bounds.right -> 1
                                else -> 0
                            }
                            if(direction!=0 && candidate.canScrollHorizontally(direction)) next=Gesture(bounds,true,direction)
                        } else if(candidate is ScrollView || candidate is ListView) {
                            val direction=when {
                                targetBounds.centerY()<bounds.top -> -1
                                targetBounds.centerY()>=bounds.bottom -> 1
                                targetBounds.top<bounds.top -> -1
                                targetBounds.bottom>bounds.bottom -> 1
                                else -> 0
                            }
                            if(direction!=0 && candidate.canScrollVertically(direction)) next=Gesture(bounds,false,direction)
                        }
                    }
                    parent=candidate.parent as? View
                }
                next ?: throw AssertionError("No native scroll route to $label: raw=$targetBounds visible=${visibleBounds(view)}")
            }
            swipe(gesture.bounds,gesture.horizontal,gesture.direction)
        }
        throw AssertionError("Native scrolling did not reveal $label")
    }
    private fun swipe(bounds: Rect,horizontal: Boolean,direction: Int) {
        assertFalse("Visible swipe viewport",bounds.isEmpty)
        val low=if(horizontal) bounds.left+bounds.width()/5 else bounds.top+bounds.height()/5
        val high=if(horizontal) bounds.right-bounds.width()/5 else bounds.bottom-bounds.height()/5
        val start=if(direction>0) high else low;val end=if(direction>0) low else high
        assertTrue("Native overflow swipe",if(horizontal) device.swipe(start,bounds.centerY(),end,bounds.centerY(),16)
            else device.swipe(bounds.centerX(),start,bounds.centerX(),end,16))
    }

    private fun screenshot(suffix: String) {
        val directory=File(context.getExternalFilesDir(null),"vertical-locale-evidence")
        assertTrue("Screenshot directory",directory.isDirectory || directory.mkdirs())
        val file=File(directory,"$evidenceName-$suffix.png")
        assertTrue("Installed screenshot $file",device.takeScreenshot(file))
        assertTrue("Nonempty screenshot",file.length()>0)
    }
    private fun <T> onMain(action: ()->T): T {
        val result=AtomicReference<T>();val failure=AtomicReference<Throwable?>()
        instrumentation.runOnMainSync {try {result.set(action())} catch(error: Throwable) {failure.set(error)}}
        failure.get()?.let {throw it};return result.get()
    }
    private fun awaitState(description: String,condition: ()->Boolean) {
        val done=CountDownLatch(1);val error=AtomicReference<Throwable?>();val handler=Handler(Looper.getMainLooper())
        val until=SystemClock.uptimeMillis()+15000
        val check=object: Runnable {
            override fun run() {
                try {
                    if(condition()) {done.countDown();return}
                    if(SystemClock.uptimeMillis()<until) {handler.postDelayed(this,25);return}
                    error.set(AssertionError("Timed out: $description; last I/O error: ${activity.lastIoError}"))
                } catch(failure: Throwable) {error.set(failure)}
                done.countDown()
            }
        }
        handler.post(check)
        try {assertTrue("Timed out: $description",done.await(16,TimeUnit.SECONDS));error.get()?.let {throw it}}
        finally {handler.removeCallbacks(check)}
    }
}
