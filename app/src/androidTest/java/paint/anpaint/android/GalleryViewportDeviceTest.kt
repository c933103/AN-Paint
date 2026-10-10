/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.LocaleManager
import android.content.Intent
import android.content.pm.ActivityInfo
import android.content.res.Configuration
import android.content.res.Resources
import android.graphics.Rect
import android.os.Build
import android.os.LocaleList
import android.os.ParcelFileDescriptor
import android.os.SystemClock
import android.provider.Settings
import android.view.View
import android.view.ViewGroup
import android.view.inputmethod.EditorInfo
import android.webkit.WebView
import android.widget.EditText
import androidx.test.core.app.ActivityScenario
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.SdkSuppress
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.runner.lifecycle.ActivityLifecycleCallback
import androidx.test.runner.lifecycle.ActivityLifecycleMonitorRegistry
import androidx.test.runner.lifecycle.Stage
import androidx.webkit.ProxyConfig
import androidx.webkit.ProxyController
import androidx.webkit.WebViewFeature
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.MediaGalleryActivity
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.util.Locale
import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executor
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicReference

/** Real Chromium sizing complements the host-only WebView MeasureSpec model.
 * All WebView traffic is rejected by a verified process-local proxy. No provider
 * content, image acquisition or navigation result is simulated as a layout pass. */
@RunWith(AndroidJUnit4::class)
@SdkSuppress(minSdkVersion=30)
class GalleryViewportDeviceTest {
    private val instrumentation=InstrumentationRegistry.getInstrumentation()
    private val context get()=instrumentation.targetContext

    @Test fun realBrowserKeepsItsViewportAtLargeTextAcrossGalleryRotation() {
        val oldScale=Settings.System.getFloat(context.contentResolver,Settings.System.FONT_SCALE,1f)
        val preferences=context.getSharedPreferences("app-language",0)
        val oldTag=if(Build.VERSION.SDK_INT>=33) context.getSystemService(LocaleManager::class.java).applicationLocales.toLanguageTags()
            else preferences.getString("language-tag","").orEmpty()
        val hadPreferenceTag=preferences.contains("language-tag")
        val oldPreferenceTag=preferences.getString("language-tag",null)
        val hadInitialization=preferences.contains("platform-initialized")
        val oldInitialization=preferences.getBoolean("platform-initialized",false)
        val oldLocale=Locale.getDefault()
        fun restorePreferenceSnapshot() {
            onMain {
                preferences.edit().apply {
                    if(hadPreferenceTag) putString("language-tag",oldPreferenceTag) else remove("language-tag")
                    if(hadInitialization) putBoolean("platform-initialized",oldInitialization) else remove("platform-initialized")
                }.commit()
                assertEquals(hadPreferenceTag,preferences.contains("language-tag"))
                assertEquals(oldPreferenceTag,preferences.getString("language-tag",null))
                assertEquals(hadInitialization,preferences.contains("platform-initialized"))
                assertEquals(oldInitialization,preferences.getBoolean("platform-initialized",false))
            }
        }
        val network=LocalRejectingProxy()
        val browsers=mutableListOf<WebView>()
        val galleries=mutableListOf<MediaGalleryActivity>()
        val lifecycle=ActivityLifecycleCallback {activity,stage ->
            if(activity is MediaGalleryActivity && stage==Stage.PRE_ON_CREATE) galleries.add(activity)
        }
        onMain {ActivityLifecycleMonitorRegistry.getInstance().addLifecycleCallback(lifecycle)}
        var probe: WebView?=null
        var applied=false
        try {
            onMain {assertTrue("A supported rejecting proxy is required",WebViewFeature.isFeatureSupported(WebViewFeature.PROXY_OVERRIDE))}
            val proxy=ProxyConfig.Builder().addProxyRule(network.rule()).removeImplicitRules().build()
            applied=true
            proxyChange {done ->ProxyController.getInstance().setProxyOverride(proxy,Executor {it.run()},done)}
            onMain {probe=WebView(context).also {it.loadUrl("https://gallery-viewport.invalid/preflight")}}
            await("verified rejecting proxy") {
                network.assertHealthy();network.requests().any {it.startsWith("CONNECT gallery-viewport.invalid:443 ")}
            }
            onMain {probe!!.stopLoading();probe!!.destroy();probe=null}
            for(tag in listOf("fr","mn-Mong")) {
                selectLanguage(tag)
                // A real system configuration transition also refreshes the
                // app-wide selected-language resources on pre-LocaleManager APIs.
                setFontScale(1f);setFontScale(2f)
                val activity=AtomicReference<MediaGalleryActivity>()
                val intent=Intent(context,MediaGalleryActivity::class.java).putExtra("gallery_provider","COMMONS")
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                ActivityScenario.launch<MediaGalleryActivity>(intent).use {scenario ->
                    scenario.onActivity {activity.set(it)}
                    val gallery=activity.get()
                    val web=onMain {
                        assertEquals(2f,gallery.resources.configuration.fontScale,0f)
                        assertEquals(tag,gallery.resources.configuration.locales[0].toLanguageTag())
                        assertEquals(gallery.getString(R.string.ui_copy_all),
                            gallery.window.decorView.findViewWithTag<android.widget.TextView>("gallery_copy_credits").text.toString())
                        val view=descendants(gallery.window.decorView).filterIsInstance<WebView>().single()
                        browsers.add(view)
                        view.loadDataWithBaseURL("https://gallery-viewport.invalid/local",
                            "<html><body style='margin:0;background:#287a65;color:white'>Local gallery viewport</body></html>","text/html","UTF-8",null)
                        val message=gallery.getString(R.string.ui_could_not_load_gallery_image,
                            gallery.getString(R.string.commons_svg_original_size_unavailable))
                        MediaGalleryActivity::class.java.getDeclaredMethod("showStatus",String::class.java)
                            .apply {isAccessible=true}.invoke(gallery,message)
                        view
                    }
                    val query="viewport query ".repeat(8)+"नदी 山"
                    val search=onMain {gallery.window.decorView.findViewWithTag<EditText>("gallery_search").also {it.setText(query)}}
                    try {
                        for(landscape in listOf(false,true)) {
                            val orientation=if(landscape) Configuration.ORIENTATION_LANDSCAPE else Configuration.ORIENTATION_PORTRAIT
                            onMain {gallery.requestedOrientation=if(landscape) ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE else ActivityInfo.SCREEN_ORIENTATION_PORTRAIT}
                            await("gallery layout $tag orientation=$orientation") {onMain {
                                val root=gallery.window.decorView
                                gallery.resources.configuration.orientation==orientation && root.width>0 && root.height>0 &&
                                    (root.width>root.height)==landscape && web.width>0 && web.height>0 && !root.isLayoutRequested
                            }}
                            instrumentation.waitForIdleSync()
                            scenario.onActivity {assertSame("Rotation must retain the same gallery",gallery,it)}
                            onMain {
                                val root=gallery.window.decorView
                                assertSame(web,descendants(root).filterIsInstance<WebView>().single())
                                assertSame(search,root.findViewWithTag<EditText>("gallery_search"))
                                assertEquals(query,search.text.toString())
                                assertTrue("Installed query must actually wrap",search.layout.lineCount>1)
                                val editorInfo=EditorInfo()
                                assertNotNull("Installed native search connection",search.onCreateInputConnection(editorInfo))
                                assertEquals(EditorInfo.IME_ACTION_SEARCH,editorInfo.imeOptions and EditorInfo.IME_MASK_ACTION)
                                assertEquals("Installed keyboard must retain Search",0,editorInfo.imeOptions and EditorInfo.IME_FLAG_NO_ENTER_ACTION)
                                assertEquals(2f,gallery.resources.configuration.fontScale,0f)
                                val visible=Rect();assertTrue("Real WebView must intersect the screen",web.getGlobalVisibleRect(visible))
                                assertEquals(web.width,visible.width());assertEquals(web.height,visible.height())
                                val parent=web.parent as View
                                val reserve=minOf((120*gallery.resources.displayMetrics.density+.5f).toInt(),(parent.height-parent.paddingTop-parent.paddingBottom)/3)
                                assertTrue("Real WebView must retain the declared usable area",web.height>=reserve)
                                val controls=root.findViewWithTag<View>("gallery_controls_scroll")
                                assertTrue("Browser must follow the controls without overlap",web.top>=controls.bottom)
                                android.util.Log.i("GalleryViewportDeviceTest",JSONObject().put("locale",tag).put("font_scale",2)
                                    .put("orientation",orientation).put("root_width",root.width).put("root_height",root.height)
                                    .put("controls_height",controls.height).put("browser_width",web.width).put("browser_height",web.height)
                                    .put("browser_visible",visible.toString()).put("required_reserve",reserve)
                                    .put("query_lines",search.layout.lineCount).put("search_ime_options",editorInfo.imeOptions)
                                    .put("search_input_type",editorInfo.inputType)
                                    .put("provider","real installed WebView; verified rejecting proxy; local HTML").toString())
                            }
                        }
                    } finally {onMain {gallery.requestedOrientation=ActivityInfo.SCREEN_ORIENTATION_PORTRAIT}}
                }
                instrumentation.waitForIdleSync()
            }
        } finally {
            // Track PRE_ON_CREATE too, so even a failed launch cannot leave an
            // unobserved gallery behind when the rejecting proxy is restored.
            try {
                try {
                    onMain {galleries.toList().filterNot {it.isDestroyed}.forEach {it.finish()}}
                    await("all gallery windows destroyed") {onMain {galleries.all {it.isDestroyed}}}
                } finally {
                    // Configuration callbacks can initialize migration preferences.
                    // Settle those first, then restore exact original key presence.
                    try {selectLanguage(oldTag)} finally {
                        try {setFontScale(oldScale)} finally {
                            Locale.setDefault(oldLocale);restorePreferenceSnapshot()
                        }
                    }
                }
            } finally {
                try {
                    onMain {
                        probe?.let {it.stopLoading();it.destroy()};probe=null
                        assertTrue("Destroy every gallery before proxy restoration",galleries.all {it.isDestroyed})
                        assertTrue("Detach every browser before proxy restoration",browsers.none {it.isAttachedToWindow})
                    }
                    instrumentation.waitForIdleSync()
                    if(applied) proxyChange {done ->ProxyController.getInstance().clearProxyOverride(Executor {it.run()},done)}
                } finally {
                    onMain {ActivityLifecycleMonitorRegistry.getInstance().removeLifecycleCallback(lifecycle)}
                    network.close()
                }
            }
        }
    }

    private fun selectLanguage(tag: String) {
        onMain {
            context.getSharedPreferences("app-language",0).edit().putString("language-tag",tag)
                .putBoolean("platform-initialized",true).commit()
            if(Build.VERSION.SDK_INT>=33) context.getSystemService(LocaleManager::class.java).applicationLocales=LocaleList.forLanguageTags(tag)
        }
        instrumentation.waitForIdleSync()
    }
    private fun setFontScale(scale: Float) {
        require(scale.isFinite() && scale>0f)
        val deadline=SystemClock.uptimeMillis()+10000
        fun state()=onMain {
            JSONObject().put("requested",scale)
                .put("setting",Settings.System.getFloat(context.contentResolver,Settings.System.FONT_SCALE,1f))
                .put("system_resources",Resources.getSystem().configuration.fontScale)
                .put("target_resources",context.resources.configuration.fontScale)
        }
        fun matches()=onMain {
            listOf(Settings.System.getFloat(context.contentResolver,Settings.System.FONT_SCALE,1f),
                Resources.getSystem().configuration.fontScale,context.resources.configuration.fontScale)
                .all {kotlin.math.abs(it-scale)<.001f}
        }
        android.util.Log.i("GalleryViewportDeviceTest","font transition before: ${state()}")
        try {
            if(Build.VERSION.SDK_INT>=34) {
                // Verify the actual target utility, including decimal duration and
                // hard-kill support, before relying on it for a system-server wait.
                if(!fontShellVerified) {
                    val probe=fontShell("timeout -s KILL 0.01s sleep 1",deadline)
                    assertEquals("Target timeout must accept decimal seconds and KILL",137,probe)
                    fontShellVerified=true
                }
                assertEquals("Real font setting write succeeded",0,
                    fontShell("settings put system font_scale $scale",deadline))
            } else {
                // API30-33 do not expose the system-looper flush command. This
                // retains the older real-setting check, not an equivalent barrier.
                android.util.Log.i("GalleryViewportDeviceTest","system-looper barrier unavailable on API${Build.VERSION.SDK_INT}; legacy synchronization only")
                ParcelFileDescriptor.AutoCloseInputStream(instrumentation.uiAutomation.executeShellCommand("settings put system font_scale $scale"))
                    .bufferedReader().use {android.util.Log.i("GalleryViewportDeviceTest","legacy font shell stdout: ${it.readText()}")}
            }
            awaitUntil("real system font scale $scale",deadline,::matches)
            if(Build.VERSION.SDK_INT>=34) {
                // ATMS can distribute the new configuration before its queued
                // Settings write-back executes on DisplayThread. Flush that queue
                // before another transition can overwrite the pending snapshot.
                assertEquals("System configuration write-back barrier succeeded",0,
                    fontShell("am wait-for-broadcast-barrier --flush-broadcast-loopers",deadline))
            }
            instrumentation.waitForIdleSync()
            assertTrue("Font transition exceeded its original 10s deadline",SystemClock.uptimeMillis()<deadline)
            assertTrue("Font setting and real resources must still agree after the barrier",matches())
        } finally {android.util.Log.i("GalleryViewportDeviceTest","font transition after: ${state()}")}
    }

    private var fontShellVerified=false

    /** API34+ has public stdin/stdout/stderr pipes; no Runtime.exec shell quoting. */
    @androidx.annotation.RequiresApi(34)
    private fun fontShell(command: String,deadline: Long): Int {
        val remaining=deadline-SystemClock.uptimeMillis()
        assertTrue("No time remains for font shell: $command",remaining>0)
        val seconds=String.format(Locale.ROOT,"%.3f",remaining/1000.0)
        android.util.Log.i("GalleryViewportDeviceTest",JSONObject().put("font_shell_start",command)
            .put("remaining_ms",remaining).toString())
        val pipes=instrumentation.uiAutomation.executeShellCommandRwe("sh")
        val readers=Executors.newFixedThreadPool(2)
        try {
            val output=readers.submit<String> {ParcelFileDescriptor.AutoCloseInputStream(pipes[0]).bufferedReader().use {it.readText()}}
            val error=readers.submit<String> {ParcelFileDescriptor.AutoCloseInputStream(pipes[2]).bufferedReader().use {it.readText()}}
            // Commands are fixed fixture strings plus a finite positive float.
            // Feeding stdin avoids assuming Runtime.exec interprets shell quotes.
            ParcelFileDescriptor.AutoCloseOutputStream(pipes[1]).bufferedWriter().use {
                it.write("timeout -s KILL ${seconds}s $command\nresult=$?\nprintf '\\nANPAINT_FONT_EXIT=%s\\n' \"${'$'}result\"\n")
            }
            fun remainingTime(): Long=(deadline-SystemClock.uptimeMillis()).also {
                assertTrue("Font shell exceeded the shared 10s deadline",it>0)
            }
            val stdout=output.get(remainingTime(),TimeUnit.MILLISECONDS)
            val stderr=error.get(remainingTime(),TimeUnit.MILLISECONDS)
            android.util.Log.i("GalleryViewportDeviceTest",JSONObject().put("font_shell",command)
                .put("stdout",stdout).put("stderr",stderr).put("remaining_ms",deadline-SystemClock.uptimeMillis()).toString())
            val exit=Regex("(?m)^ANPAINT_FONT_EXIT=([0-9]+)$").findAll(stdout).toList()
            assertEquals("Font shell must report one exit status",1,exit.size)
            assertTrue("Font shell exceeded the shared 10s deadline",SystemClock.uptimeMillis()<deadline)
            return exit.single().groupValues[1].toInt()
        } catch(failure: Throwable) {
            android.util.Log.e("GalleryViewportDeviceTest","Font shell failed within shared deadline: $command",failure)
            throw failure
        } finally {
            pipes.forEach {try {it.close()} catch(_: java.io.IOException) {}}
            readers.shutdownNow()
        }
    }
    private fun descendants(root: View): List<View> = listOf(root)+if(root is ViewGroup)
        (0 until root.childCount).flatMap {descendants(root.getChildAt(it))} else emptyList()
    private fun proxyChange(change: (Runnable)->Unit) {
        val done=CountDownLatch(1);onMain {change(Runnable {done.countDown()})}
        assertTrue("Proxy change completed",done.await(10,TimeUnit.SECONDS))
    }
    private fun <T> onMain(action: ()->T): T {
        val value=AtomicReference<T>();val error=AtomicReference<Throwable?>()
        instrumentation.runOnMainSync {try {value.set(action())} catch(failure: Throwable) {error.set(failure)}}
        error.get()?.let {throw it};return value.get()
    }
    private fun await(label: String,condition: ()->Boolean) {
        awaitUntil(label,SystemClock.uptimeMillis()+10000,condition)
    }
    private fun awaitUntil(label: String,deadline: Long,condition: ()->Boolean) {
        while(SystemClock.uptimeMillis()<deadline) {
            if(condition()) return
            SystemClock.sleep(25)
        }
        assertTrue("Timed out: $label",condition())
    }
}
