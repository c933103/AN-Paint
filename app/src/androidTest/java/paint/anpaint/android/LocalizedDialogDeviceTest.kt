/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.AlertDialog
import android.app.Activity
import android.app.Instrumentation
import android.app.LocaleManager
import android.content.ClipData
import android.content.ClipboardManager
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
import android.view.KeyEvent
import android.view.View
import android.view.ViewGroup
import android.view.WindowInsets
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
import androidx.test.uiautomator.By
import androidx.test.uiautomator.Until
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
class LocalizedDialogDeviceTest {
    private val instrumentation=InstrumentationRegistry.getInstrumentation()
    private val context get()=instrumentation.targetContext
    private val device get()=UiDevice.getInstance(instrumentation)
    @get:Rule val evidence=DialogEvidenceExportRule(instrumentation)
    private lateinit var activity: ClassicPaintActivity
    private var deadline=Long.MAX_VALUE

    @Test fun aboutThirdPartyNoticeRetainsRotationAndNativeFooterFlow()=noticeFlow(0)
    @Test fun aboutArtworkNoticeCompletesNativeFooterFlow()=noticeFlow(1)
    @Test fun aboutGimpTranslationNoticeCompletesNativeFooterFlow()=noticeFlow(2)

    // Each complete notice flow has its own unchanged 45-second interaction
    // interval. Keep the original per-notice assertions, not a filtered subset.
    private fun noticeFlow(index: Int)=fixture("fr",2f) {scenario ->
        val cases=listOf(
            Triple(R.string.ui_third_party_notices,R.string.ui_open_source_credits_and_notices,"legal/THIRD_PARTY_NOTICES.txt"),
            Triple(R.string.ui_icons_fonts_artwork_credits,R.string.ui_icons_fonts_artwork_credits,"legal/ASSET_CREDITS.txt"),
            Triple(R.string.ui_gimp_translations31,R.string.ui_gimp_translations31,"legal/GIMP_TRANSLATION_NOTICES.txt"))
        val entry=cases[index]
        // The former combined loop inherited landscape from index zero.
        if(index!=0) orient(true,scenario)
        openAbout()
        val menu=onMain {aboutList()}
        if(index==0) {
            val about=onMain {menu.rootView}
            evidence.capture("about-portrait")
            orient(true,scenario)
            onMain {assertSame("Retain the real About chooser across rotation",menu,aboutList())
                assertSame(about,menu.rootView)}
            revealText(onMain {about.findViewWithTag("dialog_title")})
            evidence.capture("about-landscape")
        }
        tapRow(menu,onMain {activity.getString(entry.first)})
        await("notice opened") {termsRoot()!=null}
        val root=onMain {termsRoot()!!}
        val expected=context.assets.open(entry.third).bufferedReader().use {it.readText()}
        fun assertNotice()=onMain {
            assertEquals(activity.getString(entry.second),root.findViewWithTag<TextView>("terms_title").text.toString())
            assertEquals("Actual menu callback loaded the bundled notice",expected,
                root.findViewWithTag<TextView>("terms_text").text.toString())
            assertTrue(root.findViewWithTag<View>("terms_scroll").height>0)
        }
        assertNotice()
        revealText(onMain {root.findViewWithTag("terms_title")})
        evidence.capture("notice-$index-initial")
        if(index==0) {
            orient(false,scenario)
            onMain {assertSame("Keep the same legal dialog after real rotation",root,termsRoot())}
            assertNotice();revealText(onMain {root.findViewWithTag("terms_title")})
            evidence.capture("notice-$index-portrait")
            orient(true,scenario)
            assertNotice();revealText(onMain {root.findViewWithTag("terms_title")})
        }
        onMain {activity.getSystemService(ClipboardManager::class.java)
            .setPrimaryClip(ClipData.newPlainText("Synthetic dialog test","copy has not run"))}
        dismissClipboardOverlay("notice-sentinel",waitForAppearance=true)
        onMain {
            assertSame("System preview dismissal retains the notice",root,termsRoot())
            assertEquals("Sentinel survives native preview dismissal","copy has not run",
                activity.getSystemService(ClipboardManager::class.java).primaryClip!!.getItemAt(0).text.toString())
        }
        tap("notice copy",onMain {root.findViewWithTag("terms_copy")})
        onMain {
            val clipboard=activity.getSystemService(ClipboardManager::class.java)
            assertEquals(expected,clipboard.primaryClip!!.getItemAt(0).text.toString())
        }
        dismissClipboardOverlay("notice-copy",waitForAppearance=true)
        onMain {
            assertSame("Copy preview dismissal retains the notice",root,termsRoot())
            assertEquals(expected,activity.getSystemService(ClipboardManager::class.java).primaryClip!!.getItemAt(0).text.toString())
        }
        tap("other terms",onMain {root.findViewWithTag("terms_more")})
        await("other terms opened") {topList()?.let {it!==menu && it.rootView.hasWindowFocus()}==true}
        val nested=onMain {topList()!!.rootView}
        nativeBack("notice-$index-nested",state={
            backWindowState(nested).put("notice_retained",termsRoot()===root)
                .put("notice_focused",root.hasWindowFocus())
        }) {!nested.isAttachedToWindow && termsRoot()===root && root.hasWindowFocus()}
        await("notice resumes after nested Back") {termsRoot()===root && root.hasWindowFocus()}
        assertNotice()
        tap("notice done",onMain {root.findViewWithTag("terms_done")})
        await("Done dismisses the notice") {termsRoot()==null}
        openAbout();tapRow(onMain {aboutList()},onMain {activity.getString(entry.first)})
        await("notice reopened") {termsRoot()?.hasWindowFocus()==true}
        val reopened=onMain {termsRoot()!!}
        nativeBack("notice-$index-close",state={
            backWindowState(reopened).put("notice_present",termsRoot()!=null)
                .put("editor_focused",activity.window.decorView.hasWindowFocus())
        }) {!reopened.isAttachedToWindow && termsRoot()==null && activity.window.decorView.hasWindowFocus()}
        await("Back returned to editor") {termsRoot()==null && activity.window.decorView.hasWindowFocus()}
    }

    @Test fun retainedCreditDialogKeepsDraftSelectionAndNativeListenersAcrossRotation()=fixture("hu",2f) {scenario ->
        var saved="Original fixture attribution";var calls=0;var dismissed=0
        val source="https://example.invalid/dialog-fixture.png"
        // GalleryCredits is internal to :Paintroid; reflection opens the real
        // editor with a capture-only fixture callback. No callback is invoked here.
        val credits=Class.forName("org.catrobat.paintroid.classic.GalleryCredits")
        val receiver=credits.getField("INSTANCE").get(null)
        val method=credits.methods.single {it.name=="showEditor" && it.parameterTypes.size==5}
        fun open(): AlertDialog=onMain {
            val onEdit: (String,String)->Unit={actual,value ->assertEquals(source,actual);saved=value;calls++}
            val onDismiss: ()->Unit={dismissed++}
            val session=checkNotNull(method.invoke(receiver,activity,listOf(ImageCredit(source,saved)),null,onEdit,onDismiss))
            session.javaClass.getMethod("getDialog").invoke(session) as AlertDialog
        }
        val dialog=open()
        try {
            await("credit field laid out") {dialog.window!!.decorView.findViewWithTag<View>("gallery_credit_text")?.width?.let {it>0}==true}
            val root=onMain {dialog.window!!.decorView}
            val field=onMain {root.findViewWithTag<EditText>("gallery_credit_text")}
            val draft="Unsaved rotation fixture 100% %1\$s\nCreator\nhttps://example.invalid/source?a=1&b=2"
            onMain {
                field.setText(draft);field.setSelection(3,8)
                activity.getSystemService(InputMethodManager::class.java).hideSoftInputFromWindow(field.windowToken,0)
            }
            for((index,landscape) in listOf(true,false).withIndex()) {
                orient(landscape,scenario)
                onMain {
                    assertTrue(dialog.isShowing);assertSame(root,dialog.window!!.decorView)
                    assertSame("Retain the actual EditText",field,root.findViewWithTag<EditText>("gallery_credit_text"))
                    assertEquals(draft,field.text.toString());assertEquals(3,field.selectionStart);assertEquals(8,field.selectionEnd)
                    assertEquals(index,calls);assertEquals(0,dismissed)
                    evidence.observe(JSONObject().put("kind","retained-credit-state").put("landscape",landscape)
                        .put("same_field",root.findViewWithTag<EditText>("gallery_credit_text")===field)
                        .put("synthetic_draft_matches",field.text.toString()==draft)
                        .put("selection_start",field.selectionStart).put("selection_end",field.selectionEnd)
                        .put("save_calls",calls).put("dismiss_calls",dismissed).put("geometry",geometry(field)))
                }
                revealText(onMain {descendants(root).filterIsInstance<TextView>().first {
                    it.text.toString()==activity.getString(R.string.ui_image_credits)
                }})
                evidence.capture("credit-${if(landscape) "landscape" else "portrait"}")
                tap("credit save",onMain {root.findViewWithTag("gallery_credit_save")})
                onMain {assertEquals(index+1,calls);assertEquals(draft,saved);assertTrue(dialog.isShowing)}
            }
            tap("credit copy",onMain {root.findViewWithTag("gallery_credit_copy")})
            onMain {
                assertEquals(3,calls);assertEquals(draft,saved)
                assertEquals(draft,activity.getSystemService(ClipboardManager::class.java).primaryClip!!.getItemAt(0).text.toString())
            }
            dismissClipboardOverlay("credit-copy",waitForAppearance=true)
            onMain {
                assertTrue("System preview dismissal retains the credit editor",dialog.isShowing)
                assertEquals(3,calls);assertEquals(0,dismissed)
                assertEquals(draft,activity.getSystemService(ClipboardManager::class.java).primaryClip!!.getItemAt(0).text.toString())
            }
            tap("credit done",onMain {root.findViewWithTag("gallery_credit_done")})
            await("Done invokes original listener and dismisses") {!dialog.isShowing}
            onMain {assertEquals(4,calls);assertEquals(1,dismissed)}
            val reopened=open()
            try {
                await("credit reopened") {reopened.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text")?.layout!=null}
                onMain {
                    val next=reopened.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text")
                    assertEquals(draft,next.text.toString());next.setText("Discard this synthetic draft")
                    activity.getSystemService(InputMethodManager::class.java).hideSoftInputFromWindow(next.windowToken,0)
                }
                instrumentation.waitForIdleSync()
                await("reopened credit window focused") {reopened.isShowing && reopened.window!!.decorView.hasWindowFocus()}
                nativeBack("credit-discard",state={
                    backWindowState(reopened.window!!.decorView).put("dialog_showing",reopened.isShowing)
                        .put("save_calls",calls).put("dismiss_calls",dismissed).put("saved_draft_unchanged",saved==draft)
                }) {!reopened.isShowing && !reopened.window!!.decorView.isAttachedToWindow &&
                    calls==4 && dismissed==2 && saved==draft}
                await("Back dismissed credit editor") {!reopened.isShowing}
                onMain {
                    assertEquals(4,calls);assertEquals(2,dismissed);assertEquals(draft,saved)
                    evidence.observe(JSONObject().put("kind","credit-listeners-complete").put("save_calls",calls)
                        .put("dismiss_calls",dismissed).put("back_discarded_synthetic_draft",saved==draft))
                }
            } finally {onMain {reopened.dismiss()}}
        } finally {onMain {dialog.dismiss()}}
    }

    /** This characterizes an unchanged-source limitation; it does not accept
     * colour usability. The original positive oracle is preserved verbatim in
     * verification/localized-dialog-layout-2026-10-11/colour-separate-scope/.
     * The untouched-baseline installed comparison reproduces this failure;
     * the positive corrective gate remains separate.
     */
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
            interaction {
                await("initial editor") {activity.startupReady && !activity.busy && activity.paintCanvas.width>0 && activity.window.decorView.hasWindowFocus()}
                onMain {
                    // Read only after this synthetic activity is foreground. Android
                    // can return null for a background clipboard read despite data.
                    assertTrue("Clipboard snapshot requires the fixture foreground",activity.window.decorView.hasWindowFocus())
                    originalClip=clipboard.primaryClip;clipboardSnapshotted=true
                    assertEquals(tag,activity.resources.configuration.locales[0].toLanguageTag())
                    assertEquals(scale,activity.resources.configuration.fontScale,0f)
                }
                dismissClipboardOverlay("fixture-ready")
                orient(false,launched)
                evidence.observe(JSONObject().put("kind","fixture").put("locale",tag).put("font_scale",scale)
                    .put("setup","real installed dialogs; synthetic editor data; native pointer actions"))
                block(launched)
                assertTrue("Dialog checks must not request any external activity",externalRequests.isEmpty())
            }
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
            cleanup {dismissClipboardOverlay("fixture-restored",waitForAppearance=clipboardSnapshotted && originalClip!=null)}
            cleanup {instrumentation.removeMonitor(external)}
            cleanup {onMain {ActivityLifecycleMonitorRegistry.getInstance().removeLifecycleCallback(lifecycle)}}
        }
        failure?.let {throw it}
    }

    /** Keep the existing interval: initial editor readiness through the complete
     * interaction block, before fixture restoration. A final successful action
     * can itself consume the remaining time, so checking only before awaits or
     * gestures is insufficient. Teardown is measured by the outer export rule.
     */
    private fun interaction(block: ()->Unit) {
        val started=SystemClock.uptimeMillis()
        deadline=started+45000
        evidence.observe(JSONObject().put("kind","interaction-start").put("started_uptime_ms",started)
            .put("deadline_uptime_ms",deadline).put("budget_ms",45000))
        var completed=false
        var ended=started
        try {block();completed=true} finally {
            ended=SystemClock.uptimeMillis()
            evidence.observe(JSONObject().put("kind","interaction-end").put("started_uptime_ms",started)
                .put("ended_uptime_ms",ended).put("deadline_uptime_ms",deadline).put("elapsed_ms",ended-started)
                .put("budget_ms",45000).put("block_completed",completed).put("within_deadline",ended<=deadline))
        }
        assertTrue("Entire dialog interaction exceeded its 45-second budget",ended<=deadline)
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

    /** Same native SystemUI dismissal used by EditorDeviceTest. Clipboard writes
     * create a separate input window: app-local visible bounds do not account
     * for that occlusion. Never disable previews, change settings or tap through
     * an overlay. Preserve the real clipboard and app callback assertions.
     */
    private fun dismissClipboardOverlay(phase: String,waitForAppearance: Boolean=false) {
        val until=minOf(deadline,SystemClock.uptimeMillis()+10000)
        fun remaining()=(until-SystemClock.uptimeMillis()).also {assertTrue("Clipboard dismissal deadline",it>0)}
        fun showing()=instrumentation.uiAutomation.windows.any {it.title?.toString()=="ClipboardOverlay"}
        val selector=By.res("com.android.systemui","clipboard_ui")
        val overlay=if(waitForAppearance) device.wait(Until.findObject(selector),minOf(1500L,remaining()))
            else device.findObject(selector)
        val windowShowing=showing()
        evidence.observe(JSONObject().put("kind","clipboard-overlay-before").put("phase",phase)
            .put("requested_appearance_wait",waitForAppearance).put("content_found",overlay!=null)
            .put("window_showing",windowShowing))
        if(overlay==null && !windowShowing) return
        val dismiss=overlay?.findObject(By.res("com.android.systemui","dismiss_button"))
        if(dismiss!=null) {
            val bounds=dismiss.visibleBounds
            assertFalse("System clipboard dismiss target is visible",bounds.isEmpty)
            evidence.observe(JSONObject().put("kind","clipboard-overlay-native-dismiss").put("phase",phase)
                .put("target",rect(bounds)).put("tap",JSONArray().put(bounds.centerX()).put(bounds.centerY())))
            assertTrue("Tap only the SystemUI clipboard dismiss control",device.click(bounds.centerX(),bounds.centerY()))
        }
        // If this SystemUI variant has no dismiss affordance, require its normal
        // timeout within the same bound; no extra tap may reset that timeout.
        assertTrue("Clipboard preview content disappears",device.wait(Until.gone(selector),remaining())==true)
        while(showing() && SystemClock.uptimeMillis()<until) SystemClock.sleep(25)
        assertFalse("Clipboard input window disappears",showing())
        evidence.observe(JSONObject().put("kind","clipboard-overlay-after").put("phase",phase)
            .put("content_gone",device.findObject(selector)==null).put("window_gone",!showing()))
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
        val start=Point(bounds.centerX(),if(direction>0) high else low)
        val end=Point(bounds.centerX(),start.y-if(direction>0) distance else -distance)
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
    private fun checkDeadline() {assertTrue("Dialog case exceeded its 45-second interaction budget",SystemClock.uptimeMillis()<deadline)}
    private fun await(label: String,condition: ()->Boolean) {
        val until=minOf(deadline,SystemClock.uptimeMillis()+8000)
        while(SystemClock.uptimeMillis()<until) {if(onMain(condition)) return;SystemClock.sleep(25)}
        throw AssertionError("Timed out: $label")
    }
    private fun <T> onMain(action: ()->T): T {
        if(Looper.myLooper()==Looper.getMainLooper()) return action()
        val value=AtomicReference<T>();val error=AtomicReference<Throwable?>()
        instrumentation.runOnMainSync {try {value.set(action())} catch(failure: Throwable) {error.set(failure)}}
        error.get()?.let {throw it};return value.get()
    }
}
