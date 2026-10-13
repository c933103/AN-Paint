/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.AlertDialog
import android.app.Activity
import android.app.Instrumentation
import android.app.LocaleManager
import android.content.ClipData
import android.content.ClipboardManager
import android.content.ComponentName
import android.content.Intent
import android.content.pm.ActivityInfo
import android.content.res.Configuration
import android.graphics.Point
import android.graphics.Rect
import android.os.Build
import android.os.LocaleList
import android.os.Looper
import android.os.SystemClock
import android.provider.Settings
import android.view.View
import android.view.KeyEvent
import android.view.WindowInsets
import android.view.accessibility.AccessibilityWindowInfo
import android.view.ViewGroup
import android.view.inspector.WindowInspector
import android.view.inputmethod.InputMethodManager
import android.widget.EditText
import android.widget.ListView
import android.widget.ScrollView
import android.widget.TextView
import androidx.test.core.app.ActivityScenario
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.SdkSuppress
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.runner.lifecycle.ActivityLifecycleCallback
import androidx.test.runner.lifecycle.ActivityLifecycleMonitorRegistry
import androidx.test.runner.lifecycle.Stage
import androidx.test.uiautomator.UiDevice
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AdvancedColourDialog
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.ImageCredit
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import java.util.Locale
import java.util.concurrent.atomic.AtomicReference
import java.util.concurrent.CopyOnWriteArrayList

/** API35 installed-emulator checks; no physical-device or linguistic acceptance.
 * The initial dialog/draft are explicit fixtures. Every menu row, footer, scroll
 * and Back assertion uses injected device input, never a production handler call.
 * No provider, image import, file destination or document edit is involved.
 */
@RunWith(AndroidJUnit4::class)
@SdkSuppress(minSdkVersion=35,maxSdkVersion=35)
class ColourViewportDeviceTest {
    private val instrumentation=InstrumentationRegistry.getInstrumentation()
    private val context get()=instrumentation.targetContext
    private val device get()=UiDevice.getInstance(instrumentation)
    @get:Rule val evidence=DialogEvidenceExportRule(instrumentation)
    private lateinit var activity: ClassicPaintActivity
    private var deadline=Long.MAX_VALUE

    @Test fun normalAdvancedColourKeepsFiniteViewportAndFixedControls()=fixture("en-US",1f) {scenario ->
        orient(true,scenario)
        var committed=0;var closed=0
        val dialog=onMain {AdvancedColourDialog(activity,android.graphics.Color.RED,false,
            closed={closed++},initialMode=1) {committed++}.show()}
        try {
            await("normal Advanced Colour laid out") {dialog.window!!.decorView.findViewWithTag<View>("colour_editor_scroll")?.height?.let {it>0}==true}
            val root=onMain {dialog.window!!.decorView}
            val inner=onMain {root.findViewWithTag<ScrollView>("colour_editor_scroll")}
            val fixed=onMain {listOf("colour_advanced_tab","custom_colours_panel","add_custom_colour").map {root.findViewWithTag<View>(it)}}
            val bounds=onMain {
                val holder=root.findViewWithTag<View>("colour_dialog_holder")
                assertTrue("Native colour holder has finite positive bounds",holder.width>0 && holder.height>0)
                assertTrue(inner.height>0);assertTrue("Internal colour content actually scrolls",inner.getChildAt(0).height>inner.height)
                assertTrue(holder.height<=activity.resources.displayMetrics.heightPixels)
                fixed.map {assertComplete(it);rawBounds(it)}
            }
            evidence.capture("colour-normal-before")
            val before=onMain {inner.scrollY}
            swipe(onMain {visibleBounds(inner)},1)
            settle(inner)
            onMain {
                assertTrue("Real gesture scrolls the internal colour viewport",inner.scrollY>before)
                assertEquals("Fixed controls must not move with colour content",bounds,fixed.map {assertComplete(it);rawBounds(it)})
                evidence.observe(JSONObject().put("kind","colour-finite-bounds").put("scale",1)
                    .put("inner",geometry(inner)).put("fixed",JSONArray(fixed.map {geometry(it)})))
            }
            evidence.capture("colour-normal-scrolled")
            tap("colour cancel",onMain {dialog.getButton(AlertDialog.BUTTON_NEGATIVE)})
            await("colour Cancel closes") {!dialog.isShowing}
            onMain {assertEquals(0,committed);assertEquals(1,closed)}
            // 2x short-landscape is intentionally outside this acceptance test.
            // Its baseline comparison remains a separately labelled diagnostic.
        } finally {onMain {dialog.dismiss()}}
    }

    @Test fun retainedColourStateSurvivesRotationImeCancelAndReopen()=fixture("en-US",1f) {scenario ->
        var commits=0;var closes=0;var selected=android.graphics.Color.RED;var preview=selected
        fun open(mode: Int): Pair<AdvancedColourDialog,AlertDialog> = onMain {
            val picker=AdvancedColourDialog(activity,android.graphics.Color.RED,false,
                preview={preview=it},closed={closes++},initialMode=mode) {selected=it;commits++}
            picker to picker.show()
        }
        var (picker,dialog)=open(2)
        try {
            await("portrait colour window") {dialog.window!!.decorView.hasWindowFocus() &&
                dialog.window!!.decorView.findViewWithTag<View>("colour_editor_scroll").height>0}
            val root=onMain {dialog.window!!.decorView}
            val field=onMain {root.findViewWithTag<EditText>("colour_hex")}
            val slots=onMain {(0 until 16).map {root.findViewWithTag<View>("custom_colour_$it")}}
            // An explicit synthetic draft, not a claim of keyboard transcription.
            onMain {field.setText("#13579B");field.setSelection(2,5)}
            fun retained()=onMain {
                assertSame(root,dialog.window!!.decorView)
                assertSame(field,root.findViewWithTag<View>("colour_hex"))
                assertEquals("#13579B",field.text.toString());assertNull(field.error)
                assertEquals(2,field.selectionStart);assertEquals(5,field.selectionEnd)
                assertEquals(0xff13579b.toInt(),picker.value.colour)
                assertTrue((root.findViewWithTag<View>("colour_surface") as org.catrobat.paintroid.classic.ColourSurface).wheel)
                assertEquals(slots,(0 until 16).map {root.findViewWithTag<View>("custom_colour_$it")})
                assertEquals(0,commits);assertEquals(0,closes)
            }
            for(landscape in listOf(true,false,true)) {
                orient(landscape,scenario);settle(root);retained()
                onMain {
                    assertTrue(root.findViewWithTag<View>("colour_editor_scroll").height>0)
                    slots.forEach {assertTrue("Saved slot retains a finite size",it.width>0 && it.height>0)}
                    if(!landscape) slots.forEach {assertComplete(it)}
                    for(tag in listOf("colour_mode_0","colour_mode_3","colour_advanced_tab",
                            "colour_mode_1","colour_mode_2","add_custom_colour")) {
                        val view=root.findViewWithTag<TextView>(tag)
                        intrinsic(view)
                        // Spectrum/Wheel may be inside the scrollable body;
                        // their full intrinsic captions must still fit their views.
                        if(tag !in listOf("colour_mode_1","colour_mode_2")) assertComplete(view)
                    }
                    assertComplete(root.findViewWithTag("custom_colours_panel"))
                }
                evidence.capture(if(landscape) "retained-landscape" else "retained-portrait")
            }
            val inner=onMain {root.findViewWithTag<ScrollView>("colour_editor_scroll")}
            val surface=onMain {root.findViewWithTag<View>("colour_surface")}
            reveal(surface) {
                val raw=rawBounds(surface);val density=surface.resources.displayMetrics.density
                Rect(raw.left,raw.top+(8*density).toInt(),raw.right,raw.top+(32*density).toInt())
            }
            val surfaceBounds=onMain {visibleBounds(surface)}
            assertTrue("A real visible colour surface remains available",surfaceBounds.width()>16 && surfaceBounds.height()>16)
            val beforeDrag=onMain {picker.value.colour to inner.scrollY}
            assertTrue("Native surface drag",device.swipe(surfaceBounds.left+surfaceBounds.width()/4,surfaceBounds.centerY(),
                surfaceBounds.right-surfaceBounds.width()/4,surfaceBounds.centerY(),16))
            instrumentation.waitForIdleSync()
            onMain {
                assertNotEquals("Dragging the actual colour surface still edits the value",beforeDrag.first,picker.value.colour)
                assertEquals("The surface retains its drag ownership",beforeDrag.second,inner.scrollY)
                assertEquals(0,commits);assertEquals(0,closes)
                val node=inner.createAccessibilityNodeInfo()
                try {
                    assertTrue("Native accessibility reports scrollable content",node.isScrollable)
                    assertTrue(node.actionList.any {it.id==android.view.accessibility.AccessibilityNodeInfo.ACTION_SCROLL_FORWARD})
                } finally {node.recycle()}
                evidence.observe(JSONObject().put("kind","colour-surface-native-drag")
                    .put("before_colour",beforeDrag.first).put("after_colour",picker.value.colour)
                    .put("scroll_before",beforeDrag.second).put("scroll_after",inner.scrollY))
            }
            evidence.capture("colour-surface-dragged")
            onMain {field.setText("#13579B");field.setSelection(2,5)}
            retained()
            // The last saved slot remains reachable by the existing horizontal
            // native scroll route; resizing does not replace any swatch object.
            val palette=onMain {descendants(root.findViewWithTag("custom_colours_panel"))
                .filterIsInstance<android.widget.HorizontalScrollView>().single()}
            var reached=false
            for(attempt in 0..8) {
                if(onMain {visibleBounds(slots.last()).contains(rawBounds(slots.last()))}) {reached=true;break}
                val bounds=onMain {visibleBounds(palette)}
                assertTrue(device.swipe(bounds.right-bounds.width()/5,bounds.centerY(),
                    bounds.left+bounds.width()/5,bounds.centerY(),16))
                settle(palette)
            }
            assertTrue("Last saved slot has a real native reachability route",reached);retained()
            tap("colour hex field",field)
            onMain {
                field.setSelection(2,5)
                activity.getSystemService(InputMethodManager::class.java).showSoftInput(field,InputMethodManager.SHOW_IMPLICIT)
            }
            awaitNativeImeWindow(true,root,field)
            nativeBack("hide colour IME",{
                backWindowState(root).put("dialog_showing",dialog.isShowing).put("value",field.text.toString())
                    .put("ime_inset_bottom",root.rootWindowInsets?.getInsets(WindowInsets.Type.ime())?.bottom ?: JSONObject.NULL)
                    .put("commit_callbacks",commits).put("closed_callbacks",closes)
            }) {
                dialog.isShowing && root.isAttachedToWindow && root.hasWindowFocus() &&
                    dialog.window!!.decorView===root && root.findViewWithTag<View>("colour_hex")===field &&
                    root.rootWindowInsets?.isVisible(WindowInsets.Type.ime())==false &&
                    root.rootWindowInsets?.getInsets(WindowInsets.Type.ime())?.bottom==0 &&
                    field.text.toString()=="#13579B" && picker.value.colour==0xff13579b.toInt() &&
                    field.selectionStart==2 && field.selectionEnd==5 && commits==0 && closes==0
            }
            awaitNativeImeWindow(false,root,field)
            settle(root);retained();evidence.capture("colour-ime-hidden-retained")
            tap("colour state cancel",onMain {dialog.getButton(AlertDialog.BUTTON_NEGATIVE)})
            await("state Cancel closes") {!dialog.isShowing}
            onMain {assertEquals(0,commits);assertEquals(1,closes);assertEquals(android.graphics.Color.RED,preview)}
            val reopened=open(1);picker=reopened.first;dialog=reopened.second
            await("reopened colour ready") {dialog.window!!.decorView.hasWindowFocus()}
            onMain {assertEquals("#FF0000",dialog.window!!.decorView.findViewWithTag<EditText>("colour_hex").text.toString())}
            val reopenedRoot=onMain {dialog.window!!.decorView}
            nativeBack("close reopened colour picker",{
                backWindowState(reopenedRoot).put("dialog_showing",dialog.isShowing)
                    .put("commit_callbacks",commits).put("closed_callbacks",closes)
                    .put("selected_colour",selected).put("preview_colour",preview)
            }) {
                !dialog.isShowing && !reopenedRoot.isAttachedToWindow && activity.window.decorView.hasWindowFocus() &&
                    commits==0 && closes==2 && selected==android.graphics.Color.RED && preview==android.graphics.Color.RED
            }
            onMain {assertEquals(0,commits);assertEquals(2,closes)}
            evidence.capture("colour-reopened-back-closed")
            val third=open(1);picker=third.first;dialog=third.second
            await("third colour ready") {dialog.window!!.decorView.hasWindowFocus()}
            val finalField=onMain {dialog.window!!.decorView.findViewWithTag<EditText>("colour_hex")}
            onMain {finalField.setText("#broken")}
            tap("invalid colour rejected",onMain {dialog.getButton(AlertDialog.BUTTON_POSITIVE)})
            onMain {assertTrue(dialog.isShowing);assertEquals(0,commits);assertNotNull(finalField.error)}
            onMain {finalField.setText("#2468AC")}
            tap("valid colour committed",onMain {dialog.getButton(AlertDialog.BUTTON_POSITIVE)})
            await("valid colour closes") {!dialog.isShowing}
            onMain {
                assertEquals(1,commits);assertEquals(3,closes);assertEquals(0xff2468ac.toInt(),selected)
                evidence.observe(JSONObject().put("kind","colour-retained-state-complete")
                    .put("commit_callbacks",commits).put("closed_callbacks",closes)
                    .put("selected",String.format(Locale.ROOT,"#%06X",selected and 0xffffff)))
            }
        } finally {onMain {dialog.dismiss()}}
    }

    @Test fun hungarianColourCaptionsFitPortraitAndLandscape()=fixture("hu",1f) {scenario ->
        var commits=0;var closes=0
        val dialog=onMain {AdvancedColourDialog(activity,android.graphics.Color.RED,false,
            closed={closes++},initialMode=1) {commits++}.show()}
        try {
            await("Hungarian colour ready") {dialog.window!!.decorView.hasWindowFocus()}
            val root=onMain {dialog.window!!.decorView}
            // Start with a real rotation, then return to portrait for both its
            // capture and native Cancel. Android dismisses its temporary clipboard
            // preview on orientation change; inspect the resulting pixels too.
            for(landscape in listOf(true,false)) {
                orient(landscape,scenario);settle(root)
                onMain {
                    val inner=root.findViewWithTag<ScrollView>("colour_editor_scroll")
                    assertTrue(inner.height>0 && inner.getChildAt(0).height>inner.height)
                    for(tag in listOf("colour_mode_0","colour_mode_3","colour_advanced_tab",
                            "colour_mode_1","colour_mode_2","add_custom_colour")) {
                        val view=root.findViewWithTag<TextView>(tag);intrinsic(view);assertComplete(view)
                    }
                    assertComplete(root.findViewWithTag("custom_colours_panel"))
                    assertEquals(0,commits);assertEquals(0,closes)
                    evidence.observe(JSONObject().put("kind","hungarian-colour-captions-fit")
                        .put("landscape",landscape).put("inner",geometry(inner))
                        .put("add",geometry(root.findViewWithTag("add_custom_colour"))))
                }
                evidence.capture(if(landscape) "hungarian-captions-landscape" else "hungarian-captions-portrait")
            }
            tap("Hungarian colour Cancel",onMain {dialog.getButton(AlertDialog.BUTTON_NEGATIVE)})
            await("Hungarian colour Cancel closes") {!dialog.isShowing && !root.isAttachedToWindow &&
                activity.window.decorView.hasWindowFocus() && commits==0 && closes==1}
        } finally {onMain {dialog.dismiss()}}
    }

    @Test fun largeEnglishColourCaptionsAndPreviewRemainReachable()=largeColourRail("en-US")
    @Test fun largeHungarianColourCaptionsAndPreviewRemainReachable()=largeColourRail("hu")

    private fun largeColourRail(tag: String)=fixture(tag,2f) {scenario ->
        orient(true,scenario)
        var commits=0;var closes=0
        val dialog=onMain {AdvancedColourDialog(activity,android.graphics.Color.RED,false,
            closed={closes++},initialMode=1) {commits++}.show()}
        try {
            await("large colour rail laid out") {dialog.window!!.decorView.hasWindowFocus() &&
                dialog.window!!.decorView.findViewWithTag<ScrollView>("colour_controls_scroll").height>0}
            val root=onMain {dialog.window!!.decorView}
            val controls=onMain {root.findViewWithTag<ScrollView>("colour_controls_scroll")}
            val editor=onMain {root.findViewWithTag<ScrollView>("colour_editor_scroll")}
            val add=onMain {root.findViewWithTag<TextView>("add_custom_colour")}
            val selected=onMain {root.findViewWithTag<TextView>("selected_colour_caption")}
            val sample=onMain {root.findViewWithTag<View>("new_colour_preview")}
            onMain {
                val display=activity.window.decorView
                assertEquals(640,display.width);assertEquals(320,display.height)
                assertEquals(1f,activity.resources.displayMetrics.density,0f)
                assertEquals(2f,activity.resources.configuration.fontScale,0f)
                assertComplete(editor);assertComplete(controls)
                assertTrue("Large-font rail width is applied: ${geometry(controls)}",controls.width>220)
                assertTrue("At least half the columns remain for editing",editor.width>=controls.width)
                assertTrue(editor.getChildAt(0).height>editor.height)
                assertTrue(add.height>=48*add.resources.displayMetrics.density)
                assertEquals(android.util.TypedValue.applyDimension(android.util.TypedValue.COMPLEX_UNIT_SP,
                    12f,add.resources.displayMetrics),add.textSize,0f)
                assertEquals(64,sample.width);assertEquals(24,sample.height)
            }
            evidence.capture("colour-large-initial")
            val editorOffset=onMain {editor.scrollY}
            // Every line must first fit the natural control, then be reachable
            // through native ancestor gestures. No requestRectangle/performClick.
            for(view in listOf(selected,add)) revealText(view)
            reveal(add) {rawBounds(add)}
            reveal(sample) {rawBounds(sample)}
            val overflow=onMain {controls.getChildAt(0).height>controls.height}
            onMain {
                assertComplete(add);assertComplete(selected);assertComplete(sample)
                if(overflow) assertTrue("Native input reaches the lower rail",controls.scrollY>0)
                if(tag=="hu") assertTrue("Long caption exercises overflow",overflow)
                assertEquals(editorOffset,editor.scrollY)
                evidence.observe(JSONObject().put("kind","colour-large-rail-reached")
                    .put("display",geometry(activity.window.decorView)).put("density",activity.resources.displayMetrics.density)
                    .put("font_scale",activity.resources.configuration.fontScale).put("text_size",add.textSize)
                    .put("expected_text_size",android.util.TypedValue.applyDimension(android.util.TypedValue.COMPLEX_UNIT_SP,
                        12f,add.resources.displayMetrics)).put("overflow",overflow)
                    .put("content_height",controls.getChildAt(0).height).put("viewport_height",controls.height)
                    .put("controls",geometry(controls)).put("editor",geometry(editor))
                    .put("editor_before",editorOffset).put("add",geometry(add))
                    .put("selected",geometry(selected)).put("sample",geometry(sample)))
            }
            evidence.capture("colour-large-preview-reached")
            val heading=onMain {root.findViewWithTag<TextView>("custom_colour_selection")}
            revealText(heading);reveal(heading) {rawBounds(heading)}
            onMain {
                assertComplete(heading);assertComplete(root.findViewWithTag("custom_colour_0"))
                assertEquals(editorOffset,editor.scrollY)
                evidence.observe(JSONObject().put("kind","colour-large-rail-top-reached")
                    .put("heading",geometry(heading)).put("slot",geometry(root.findViewWithTag("custom_colour_0")))
                    .put("controls",geometry(controls)))
            }
            evidence.capture("colour-large-top-reached")
            tap("large colour Cancel",onMain {dialog.getButton(AlertDialog.BUTTON_NEGATIVE)})
            await("large colour Cancel closes") {!dialog.isShowing && !root.isAttachedToWindow}
            onMain {
                assertEquals(0,commits);assertEquals(1,closes)
                evidence.observe(JSONObject().put("kind","colour-large-cancelled")
                    .put("commit_callbacks",commits).put("closed_callbacks",closes)
                    .put("dialog_attached",root.isAttachedToWindow).put("dialog_showing",dialog.isShowing))
            }
        } finally {onMain {dialog.dismiss()}}
    }

    private fun backWindowState(root: View): JSONObject {
        val focused=WindowInspector.getGlobalWindowViews().lastOrNull {it.hasWindowFocus()}
        val targetInsets=root.rootWindowInsets
        val focusedInsets=focused?.rootWindowInsets
        return JSONObject().put("target_attached",root.isAttachedToWindow)
            .put("target_showing",root.isShown && root.isAttachedToWindow).put("target_focused",root.hasWindowFocus())
            .put("target_insets_available",targetInsets!=null)
            .put("target_ime_visible",targetInsets?.isVisible(WindowInsets.Type.ime()) ?: JSONObject.NULL)
            .put("focused_app_window_present",focused!=null).put("focused_app_window_is_target",focused===root)
            .put("focused_app_window_is_editor",focused===activity.window.decorView)
            .put("focused_insets_available",focusedInsets!=null)
            .put("focused_app_window_ime_visible",focusedInsets?.isVisible(WindowInsets.Type.ime()) ?: JSONObject.NULL)
    }

    /** androidx.test.uiautomator:uiautomator:2.2.0 pressBack waits for a
     * TYPE_WINDOW_CONTENT_CHANGED event; its false result is not an injection
     * result. pressKeyCode instead reports the single native DOWN/UP pair.
     * Primary source: https://dl.google.com/dl/android/maven2/androidx/test/uiautomator/uiautomator/2.2.0/uiautomator-2.2.0-sources.jar
     * JAR SHA256: e1f438106ac0d26b80ecf4fd6ffe6d36f60e12bdcd6316903f802ed24d00be99.
     * App state/callbacks remain a separate oracle; never retry a Back action.
     */
    private fun nativeBack(label: String,state: ()->JSONObject,condition: ()->Boolean) {
        val before=onMain(state)
        evidence.observe(JSONObject().put("kind","native-back-before").put("label",label)
            .put("state",before).put("postcondition_met",onMain(condition)))
        assertTrue("Back target is attached, visible and focused",before.getBoolean("target_attached") &&
            before.getBoolean("target_showing") && before.getBoolean("target_focused"))
        assertFalse("Back must establish a new app outcome",onMain(condition))
        var injected: Boolean?=null
        var completed=false
        try {
            checkDeadline()
            injected=device.pressKeyCode(KeyEvent.KEYCODE_BACK)
            evidence.observe(JSONObject().put("kind","native-back-injected").put("label",label)
                .put("route","UiDevice.pressKeyCode(KEYCODE_BACK)").put("keycode",KeyEvent.KEYCODE_BACK)
                .put("injection_count",1).put("injected",injected).put("state",onMain(state)))
            assertTrue("Native Back DOWN/UP injection succeeded",injected==true)
            await("native Back outcome: $label",condition)
            completed=true
        } finally {
            // This runs inside the caller's try: its dismiss()/finish() cleanup
            // has not happened yet, including when injection or waiting fails.
            evidence.observe(JSONObject().put("kind","native-back-after").put("label",label)
                .put("injected",injected ?: JSONObject.NULL).put("completed",completed)
                .put("postcondition_met",onMain(condition)).put("state",onMain(state)))
        }
    }

    private fun fixture(tag: String,scale: Float,block: (ActivityScenario<ClassicPaintActivity>)->Unit) {
        assertEquals(35,Build.VERSION.SDK_INT)
        assertTrue("Run only on the declared emulator, not a personal device",
            Build.FINGERPRINT.contains("generic") || Build.MODEL.contains("sdk",ignoreCase=true) || Build.MODEL.contains("Emulator"))
        val preferences=context.getSharedPreferences("app-language",0)
        val snapshot=preferences.all.toMap()
        val oldLocale=Locale.getDefault()
        val oldTags=context.getSystemService(LocaleManager::class.java).applicationLocales.toLanguageTags()
        val oldScale=Settings.System.getFloat(context.contentResolver,Settings.System.FONT_SCALE,1f)
        val font=GalleryViewportDeviceTest()
        val activities=mutableListOf<ClassicPaintActivity>()
        val externalRequests=CopyOnWriteArrayList<Intent>()
        val external=object: Instrumentation.ActivityMonitor() {
            override fun onStartActivity(intent: Intent): Instrumentation.ActivityResult? {
                if(intent.action !in listOf(Intent.ACTION_VIEW,Intent.ACTION_CHOOSER,
                        Intent.ACTION_OPEN_DOCUMENT,Intent.ACTION_CREATE_DOCUMENT,Intent.ACTION_GET_CONTENT)) return null
                externalRequests.add(Intent(intent))
                return Instrumentation.ActivityResult(Activity.RESULT_CANCELED,null)
            }
        }
        val lifecycle=ActivityLifecycleCallback {seen,stage ->
            if(seen is ClassicPaintActivity && stage==Stage.PRE_ON_CREATE) activities.add(seen)
        }
        var scenario: ActivityScenario<ClassicPaintActivity>?=null
        var oldOrientation=ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
        var failure: Throwable?=null
        val clipboard=context.getSystemService(ClipboardManager::class.java)
        // This is synthetic emulator state; do not log the previous clipboard.
        var originalClip: ClipData?=null
        var clipboardSnapshotted=false
        onMain {ActivityLifecycleMonitorRegistry.getInstance().addLifecycleCallback(lifecycle)}
        instrumentation.addMonitor(external)
        try {
            onMain {
                preferences.edit().putString("language-tag",tag).putBoolean("platform-initialized",true).commit()
                context.getSystemService(LocaleManager::class.java).applicationLocales=LocaleList.forLanguageTags(tag)
            }
            instrumentation.waitForIdleSync()
            font.transitionFontScale(1f)
            if(scale!=1f) font.transitionFontScale(scale)
            val launch=checkNotNull(context.packageManager.getLaunchIntentForPackage(context.packageName))
            val launched=ActivityScenario.launch<ClassicPaintActivity>(launch);scenario=launched
            launched.onActivity {activity=it;oldOrientation=it.requestedOrientation}
            deadline=SystemClock.uptimeMillis()+45000
            await("initial editor") {activity.startupReady && !activity.busy && activity.paintCanvas.width>0 && activity.window.decorView.hasWindowFocus()}
            onMain {
                // Read only after this synthetic activity is foreground. Android
                // can return null for a background clipboard read despite data.
                assertTrue("Clipboard snapshot requires the fixture foreground",activity.window.decorView.hasWindowFocus())
                originalClip=clipboard.primaryClip;clipboardSnapshotted=true
                assertEquals(tag,activity.resources.configuration.locales[0].toLanguageTag())
                assertEquals(scale,activity.resources.configuration.fontScale,0f)
            }
            orient(false,launched)
            evidence.observe(JSONObject().put("kind","fixture").put("locale",tag).put("font_scale",scale)
                .put("setup","real installed dialogs; synthetic editor data; native pointer actions"))
            block(launched)
            assertTrue("Dialog checks must not request any external activity",externalRequests.isEmpty())
        } catch(error: Throwable) {
            failure=error
            try {evidence.capture("failure-before-restoration")} catch(capture: Throwable) {error.addSuppressed(capture)}
        } finally {
            // Every cleanup runs even when a previous one fails; keep the original
            // failing assertion and attach restoration errors instead of hiding it.
            deadline=Long.MAX_VALUE
            fun cleanup(action: ()->Unit) {try {action()} catch(error: Throwable) {
                if(failure==null) failure=error else failure!!.addSuppressed(error)
            }}
            cleanup {onMain {activities.filterNot {it.isDestroyed}.forEach {it.requestedOrientation=oldOrientation;it.finish()}}
                await("all fixture activities destroyed") {activities.all {it.isDestroyed}}}
            cleanup {scenario?.close()}
            cleanup {onMain {context.getSystemService(LocaleManager::class.java).applicationLocales=LocaleList.forLanguageTags(oldTags)}
                instrumentation.waitForIdleSync()}
            cleanup {font.transitionFontScale(oldScale)}
            cleanup {onMain {
                Locale.setDefault(oldLocale)
                preferences.edit().clear().apply {for((key,value) in snapshot) when(value) {
                    is String->putString(key,value);is Boolean->putBoolean(key,value);is Int->putInt(key,value)
                    is Long->putLong(key,value);is Float->putFloat(key,value)
                    is Set<*>->putStringSet(key,value.map {it as String}.toSet())
                    else->error("Unsupported language preference type")
                }}.commit()
                assertEquals(snapshot,preferences.all)
            }}
            cleanup {onMain {if(clipboardSnapshotted) {
                val previous=originalClip
                if(previous==null) clipboard.clearPrimaryClip() else clipboard.setPrimaryClip(previous)
            }}}
            cleanup {instrumentation.removeMonitor(external)}
            cleanup {onMain {ActivityLifecycleMonitorRegistry.getInstance().removeLifecycleCallback(lifecycle)}}
        }
        failure?.let {throw it}
    }

    private fun openAbout() {
        onMain {ClassicPaintActivity::class.java.getDeclaredMethod("showAboutOptions").apply {isAccessible=true}.invoke(activity)}
        await("actual About choices") {topList()?.let {list ->
            (0 until list.count).any {list.getItemAtPosition(it).toString()==activity.getString(R.string.ui_third_party_notices)}
        }==true}
        // The opt-in About heading is the repaired surface; inspect every line
        // through its real native scroll ancestors before selecting any row.
        revealText(onMain {aboutList().rootView.findViewWithTag("dialog_title")})
    }
    private fun aboutList()=checkNotNull(topList())
    private fun topList(): ListView?=WindowInspector.getGlobalWindowViews().asReversed()
        .firstNotNullOfOrNull {root ->descendants(root).filterIsInstance<ListView>().firstOrNull {it.isShown}}
    private fun termsRoot(): View?=WindowInspector.getGlobalWindowViews().lastOrNull {
        it.isShown && it.findViewWithTag<View>("terms_text")!=null
    }
    private fun tapRow(list: ListView,label: String) {
        repeat(10) {
            val row=onMain {descendants(list).filterIsInstance<TextView>().firstOrNull {it.text.toString()==label}}
            if(row!=null) {tap("About row: $label",row);return}
            onMain {assertTrue("About list can reach $label",list.canScrollVertically(1))}
            swipe(onMain {visibleBounds(list)},1);settle(list)
        }
        throw AssertionError("About row was not reached within ten gestures: $label")
    }
    private fun orient(landscape: Boolean,scenario: ActivityScenario<ClassicPaintActivity>) {
        val retained=activity
        onMain {activity.requestedOrientation=if(landscape) ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE else ActivityInfo.SCREEN_ORIENTATION_PORTRAIT}
        await("real ${if(landscape) "landscape" else "portrait"} dimensions") {
            val root=activity.window.decorView
            activity.resources.configuration.orientation==(if(landscape) Configuration.ORIENTATION_LANDSCAPE else Configuration.ORIENTATION_PORTRAIT) &&
                root.width>0 && root.height>0 && (root.width>root.height)==landscape && !root.isLayoutRequested
        }
        instrumentation.waitForIdleSync()
        scenario.onActivity {assertSame("Configuration is handled by the retained activity",retained,it)}
        evidence.observe(onMain {JSONObject().put("kind","orientation").put("landscape",landscape)
            .put("root",geometry(activity.window.decorView)).put("font_scale",activity.resources.configuration.fontScale)})
    }

    private fun intrinsic(view: TextView) {
        val layout=checkNotNull(view.layout)
        val transformed=view.transformationMethod?.getTransformation(view.text,view)?.toString() ?: view.text.toString()
        evidence.observe(JSONObject().put("kind","intrinsic-caption").put("tag",view.tag ?: "About-row")
            .put("lines",layout.lineCount).put("layout_height",layout.height)
            .put("available_text_height",view.height-view.totalPaddingTop-view.totalPaddingBottom)
            .put("text_padding",JSONArray().put(view.totalPaddingLeft).put(view.totalPaddingTop)
                .put(view.totalPaddingRight).put(view.totalPaddingBottom))
            .put("caption_length",transformed.length).put("layout_width",layout.width)
            .put("line_metrics",JSONArray((0 until layout.lineCount).map {line ->JSONObject()
                .put("end",layout.getLineEnd(line)).put("ellipsis",layout.getEllipsisCount(line))
                .put("left",layout.getLineLeft(line)).put("right",layout.getLineRight(line))}))
            .put("measurement_scope","native layout-line boxes and text padding; not pixel-level glyph proof")
            .put("geometry",geometry(view)))
        assertTrue(layout.lineCount>0);assertEquals("Full caption laid out",transformed.length,layout.getLineEnd(layout.lineCount-1))
        for(line in 0 until layout.lineCount) {
            assertEquals("Caption cannot ellipsize",0,layout.getEllipsisCount(line))
            assertTrue("Caption fits native width",layout.getLineLeft(line)>=-1 && layout.getLineRight(line)<=layout.width+1)
        }
        assertTrue("Caption fits intrinsic control height",layout.height<=view.height-view.totalPaddingTop-view.totalPaddingBottom)
    }
    private fun revealText(view: TextView) {
        settle(view);onMain {intrinsic(view)}
        val lines=onMain {view.layout.lineCount}
        for(line in 0 until lines) {
            reveal(view) {val raw=rawBounds(view);val layout=view.layout
                Rect(raw.left+view.totalPaddingLeft,raw.top+view.totalPaddingTop+layout.getLineTop(line),
                    raw.right-view.totalPaddingRight,raw.top+view.totalPaddingTop+layout.getLineBottom(line))}
            evidence.observe(onMain {JSONObject().put("kind","caption-line-reached").put("line",line)
                .put("tag",view.tag ?: "About-row").put("geometry",geometry(view))
                .put("line_rect",rect(rawBounds(view).let {raw ->Rect(raw.left+view.totalPaddingLeft,
                    raw.top+view.totalPaddingTop+view.layout.getLineTop(line),raw.right-view.totalPaddingRight,
                    raw.top+view.totalPaddingTop+view.layout.getLineBottom(line))}))})
        }
    }
    private fun tap(label: String,view: TextView) {
        revealText(view)
        val bounds=onMain {visibleBounds(view).also {assertTrue("Native tap target is enabled",view.isEnabled)
            assertTrue("Native tap target is nonempty",it.width()>0 && it.height()>0)}}
        evidence.observe(onMain {JSONObject().put("kind","pointer-before").put("label",label)
            .put("tap",JSONArray().put(bounds.centerX()).put(bounds.centerY())).put("geometry",geometry(view))})
        assertTrue("Injected native tap: $label",device.click(bounds.centerX(),bounds.centerY()))
        instrumentation.waitForIdleSync()
        evidence.observe(JSONObject().put("kind","pointer-injected").put("label",label))
    }
    private fun reveal(view: View,target: ()->Rect) {
        val seen=mutableSetOf<String>()
        repeat(12) {
            checkDeadline()
            if(onMain {visibleBounds(view).contains(target())}) return
            val route=onMain {
                val wanted=target();var parent=view.parent as? View
                var found: Triple<Rect,Int,Int>?=null
                while(parent!=null && found==null) {
                    val candidate=parent;val visible=visibleBounds(candidate)
                    if(candidate is ScrollView || candidate is ListView) {
                        val direction=when {wanted.top<visible.top -> -1;wanted.bottom>visible.bottom -> 1;else -> 0}
                        if(!visible.isEmpty && direction!=0 && candidate.canScrollVertically(direction)) {
                            val hidden=if(direction<0) visible.top-wanted.top else wanted.bottom-visible.bottom
                            found=Triple(visible,direction,hidden)
                        }
                    }
                    parent=candidate.parent as? View
                }
                evidence.observe(JSONObject().put("kind","reveal-before").put("target",rect(wanted)).put("geometry",geometry(view)))
                found ?: throw AssertionError("No native scroll route to full caption: ${geometry(view)} wanted=$wanted")
            }
            assertTrue("Native reveal must not loop",seen.add(onMain {geometry(view).toString()}))
            swipe(route.first,route.second,route.third);settle(view)
        }
        throw AssertionError("Caption not reached within native gesture bound")
    }
    private fun swipe(bounds: Rect,direction: Int,hidden: Int?=null) {
        checkDeadline();assertTrue("Scroll viewport has finite area",bounds.width()>8 && bounds.height()>16)
        val low=bounds.top+bounds.height()/5;val high=bounds.bottom-bounds.height()/5
        val slop=android.view.ViewConfiguration.get(context).scaledTouchSlop
        val distance=hidden?.let {(it+slop+2).coerceIn(1,high-low)} ?: (high-low)
        // Colour-surface drags intentionally belong to the colour editor.
        // Use the visible native scroll gutter for this ScrollView only.
        val x=onMain {
            val editor=WindowInspector.getGlobalWindowViews().asReversed().firstNotNullOfOrNull {
                it.findViewWithTag<ScrollView>("colour_editor_scroll")
            }?.takeIf {visibleBounds(it)==bounds}
            if(editor==null) bounds.centerX() else {
                val rtl=editor.layoutDirection==View.LAYOUT_DIRECTION_RTL
                val gutter=if(rtl) editor.paddingLeft else editor.paddingRight
                assertTrue("Visible scroll gutter has a finite touch width",gutter>=24*editor.resources.displayMetrics.density)
                val target=if(rtl) bounds.left+gutter/2 else bounds.right-gutter/2
                evidence.observe(JSONObject().put("kind","colour-native-scroll-route")
                    .put("viewport",rect(bounds)).put("gutter_pixels",gutter).put("x",target).put("rtl",rtl))
                target
            }
        }
        val start=Point(x,if(direction>0) high else low)
        val end=Point(x,start.y-if(direction>0) distance else -distance)
        assertTrue("Native scroll gesture",device.swipe(arrayOf(start,end,end,end),16))
        instrumentation.waitForIdleSync()
    }
    private fun settle(view: View) {
        var previous="";var changed=SystemClock.uptimeMillis()
        await("native layout settled") {
            val state="${rawBounds(view)}:${view.scrollX}:${view.scrollY}:${visibleBounds(view)}"
            if(state!=previous || view.isLayoutRequested) {previous=state;changed=SystemClock.uptimeMillis();false}
            else SystemClock.uptimeMillis()-changed>=100
        }
    }
    private fun assertComplete(view: View) {
        assertTrue("Shown, finite control",view.isShown && view.width>0 && view.height>0)
        assertTrue("Complete fixed control fits: ${geometry(view)}",visibleBounds(view).contains(rawBounds(view)))
    }
    private fun rawBounds(view: View): Rect {
        val p=IntArray(2);view.getLocationOnScreen(p);return Rect(p[0],p[1],p[0]+view.width,p[1]+view.height)
    }
    private fun visibleBounds(view: View): Rect {
        val result=Rect();if(!view.getGlobalVisibleRect(result)) return Rect()
        val root=IntArray(2);view.rootView.getLocationOnScreen(root);result.offset(root[0],root[1]);return result
    }
    private fun rect(value: Rect)=JSONArray().put(value.left).put(value.top).put(value.right).put(value.bottom)
    private fun geometry(view: View)=JSONObject().put("class",view.javaClass.name).put("tag",view.tag ?: JSONObject.NULL)
        .put("raw",rect(rawBounds(view))).put("visible",rect(visibleBounds(view)))
        .put("scroll_x",view.scrollX).put("scroll_y",view.scrollY).put("shown",view.isShown)
    private fun descendants(view: View): List<View> = listOf(view)+if(view is ViewGroup)
        (0 until view.childCount).flatMap {descendants(view.getChildAt(it))} else emptyList()
    private fun recordColourAllocation() {
        onMain {
            val root=WindowInspector.getGlobalWindowViews().last {it.findViewWithTag<View>("colour_dialog_holder")!=null}
            val holder=root.findViewWithTag<View>("colour_dialog_holder")
            val inner=root.findViewWithTag<ScrollView>("colour_editor_scroll")
            fun measured(view: View): JSONObject {
                val params=view.layoutParams
                return geometry(view).put("width",view.width).put("height",view.height)
                    .put("measured_width",view.measuredWidth).put("measured_height",view.measuredHeight)
                    .put("layout_width",params?.width ?: JSONObject.NULL).put("layout_height",params?.height ?: JSONObject.NULL)
                    .put("layout_weight",(params as? android.widget.LinearLayout.LayoutParams)?.weight ?: JSONObject.NULL)
                    .put("padding",JSONArray().put(view.paddingLeft).put(view.paddingTop).put(view.paddingRight).put(view.paddingBottom))
            }
            val display=activity.window.decorView
            val frame=Rect();root.getWindowVisibleDisplayFrame(frame)
            evidence.observe(JSONObject().put("kind","colour-pre-assert-allocation")
                .put("device_sdk",Build.VERSION.SDK_INT).put("font_scale",activity.resources.configuration.fontScale)
                .put("density",activity.resources.displayMetrics.density).put("visible_display_frame",rect(frame))
                .put("display",measured(display)).put("dialog",measured(root))
                .put("holder",measured(holder)).put("holder_parent",measured(holder.parent as View))
                .put("inner",measured(inner)).put("inner_content",measured(inner.getChildAt(0)))
                .put("native_panels",JSONArray(descendants(root).filter {it.id!=View.NO_ID &&
                    runCatching {it.resources.getResourceEntryName(it.id)}.getOrNull() in
                        listOf("topPanel","buttonPanel","customPanel","custom","parentPanel")}.map {measured(it)}))
                .put("fixed",JSONArray(listOf("colour_advanced_tab","custom_colours_panel","add_custom_colour")
                    .map {measured(root.findViewWithTag<View>(it))})))
            assertEquals("Original installed fixture width",640,display.width)
            assertEquals("Original installed fixture height",320,display.height)
            assertEquals("Original installed fixture density",1f,activity.resources.displayMetrics.density,0f)
            assertEquals("Original installed fixture font scale",1f,activity.resources.configuration.fontScale,0f)
        }
        evidence.capture("colour-pre-assert-allocation")
    }

    private fun awaitNativeImeWindow(showing: Boolean,root: View,field: EditText) {
        // AOSP InputMethodService leaves the app unchanged behind a fullscreen
        // extract editor; its dialog inset can be zero while the keyboard shows.
        // UiAutomator 2.2.0 already requests interactive-window retrieval. Observe
        // the configured native IME window, without changing input-mode flags.
        val imePackage=checkNotNull(ComponentName.unflattenFromString(
            Settings.Secure.getString(context.contentResolver,Settings.Secure.DEFAULT_INPUT_METHOD))).packageName
        val until=minOf(deadline,SystemClock.uptimeMillis()+8000)
        var previous="";var stableSince=SystemClock.uptimeMillis();var reached=false
        var last=JSONArray()
        try {
            while(SystemClock.uptimeMillis()<until) {
                val facts=instrumentation.uiAutomation.windows.mapNotNull {window ->
                    if(window.type!=AccessibilityWindowInfo.TYPE_INPUT_METHOD) return@mapNotNull null
                    val bounds=Rect();window.getBoundsInScreen(bounds)
                    val node=window.root;val nodeBounds=Rect();node?.getBoundsInScreen(nodeBounds)
                    val pkg=node?.packageName?.toString()
                    val visible=node?.isVisibleToUser==true && !bounds.isEmpty && !nodeBounds.isEmpty
                    JSONObject().put("id",window.id).put("type",window.type).put("bounds",rect(bounds))
                        .put("root_bounds",rect(nodeBounds)).put("package",pkg ?: JSONObject.NULL)
                        .put("root_visible",visible).put("root_children",node?.childCount ?: 0)
                        .put("configured_ime",pkg==imePackage)
                }
                last=JSONArray(facts)
                val visible=facts.filter {it.getBoolean("root_visible")}
                val matches=if(showing) visible.any {it.getBoolean("configured_ime") && it.getInt("root_children")>0}
                    else visible.isEmpty()
                val state=last.toString()
                if(!matches || state!=previous) {previous=state;stableSince=SystemClock.uptimeMillis()}
                else if(SystemClock.uptimeMillis()-stableSince>=250) {reached=true;break}
                SystemClock.sleep(25)
            }
            assertTrue("Actual configured IME window ${if(showing) "shown" else "hidden"} and stable",reached)
        } finally {
            evidence.observe(onMain {JSONObject().put("kind","colour-native-ime-window")
                .put("requested_visible",showing).put("condition_passed",reached).put("windows",last)
                .put("stable_window_ms",SystemClock.uptimeMillis()-stableSince)
                .put("ime_visible",root.rootWindowInsets?.isVisible(WindowInsets.Type.ime()) ?: JSONObject.NULL)
                .put("ime_inset_bottom",root.rootWindowInsets?.getInsets(WindowInsets.Type.ime())?.bottom ?: JSONObject.NULL)
                .put("fullscreen_ime",activity.getSystemService(InputMethodManager::class.java).isFullscreenMode)
                .put("dialog",geometry(root)).put("field",geometry(field)).put("value",field.text.toString())
                .put("note","Native window observation; inspect actual PNG; no simultaneous field/footer fit acceptance")})
            evidence.capture(if(reached) "colour-ime-${if(showing) "visible" else "hidden"}"
                else "colour-ime-wait-failed-before-dismiss")
        }
    }
    private fun recordEditorStartup(stage: String) {
        // Read-only diagnosis of the unchanged compound startup gate. Capture
        // before cleanup so a blank window is not mistaken for a colour failure.
        onMain {
            val root=activity.window.decorView
            val canvas=runCatching {activity.paintCanvas}.getOrNull()
            evidence.observe(JSONObject().put("kind","initial-editor-state").put("stage",stage)
                .put("startup_ready",activity.startupReady).put("busy",activity.busy)
                .put("canvas",canvas?.let {geometry(it)} ?: JSONObject.NULL)
                .put("activity_destroyed",activity.isDestroyed).put("activity_finishing",activity.isFinishing)
                .put("io_error_present",activity.lastIoError!=null).put("autosave_error_present",activity.lastAutosaveError!=null)
                .put("window_focus",root.hasWindowFocus()).put("root",geometry(root))
                .put("root_attached",root.isAttachedToWindow).put("descendant_count",descendants(root).size)
                .put("startup_view_present",root.findViewWithTag<View>("editor_startup")!=null)
                .put("font_scale",activity.resources.configuration.fontScale)
                .put("locale",activity.resources.configuration.locales[0].toLanguageTag())
                .put("orientation",activity.resources.configuration.orientation)
                .put("screen_width_dp",activity.resources.configuration.screenWidthDp)
                .put("screen_height_dp",activity.resources.configuration.screenHeightDp)
                .put("global_windows",JSONArray(WindowInspector.getGlobalWindowViews().map {
                    geometry(it).put("attached",it.isAttachedToWindow).put("window_focus",it.hasWindowFocus())
                })))
        }
    }
    private fun checkDeadline() {assertTrue("Dialog case exceeded its 45-second interaction budget",SystemClock.uptimeMillis()<deadline)}
    private fun await(label: String,condition: ()->Boolean) {
        if(label=="initial editor") recordEditorStartup("before-wait")
        val until=minOf(deadline,SystemClock.uptimeMillis()+8000)
        while(SystemClock.uptimeMillis()<until) {if(onMain(condition)) {
            if(label=="initial editor") recordEditorStartup("passed")
            if(label=="normal Advanced Colour laid out") recordColourAllocation()
            return
        };SystemClock.sleep(25)}
        if(label=="initial editor") recordEditorStartup("failed-before-cleanup")
        if(label=="normal Advanced Colour laid out") recordColourAllocation()
        throw AssertionError("Timed out: $label")
    }
    private fun <T> onMain(action: ()->T): T {
        if(Looper.myLooper()==Looper.getMainLooper()) return action()
        val value=AtomicReference<T>();val error=AtomicReference<Throwable?>()
        instrumentation.runOnMainSync {try {value.set(action())} catch(failure: Throwable) {error.set(failure)}}
        error.get()?.let {throw it};return value.get()
    }
}
