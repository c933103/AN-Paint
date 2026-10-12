/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.LocaleManager
import android.content.Intent
import android.content.pm.ActivityInfo
import android.content.res.Configuration
import android.content.res.Resources
import android.graphics.Rect
import android.hardware.display.DisplayManager
import android.os.Handler
import android.os.Looper
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
import android.widget.TextView
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
import java.util.Collections
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
            for(tag in if(Build.VERSION.SDK_INT>=35) listOf("fr","mn-Mong","ar") else listOf("fr","mn-Mong")) {
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
                                if(Build.VERSION.SDK_INT>=35) recordStatusGlyphWidthFlags(gallery,tag,orientation)
                                android.util.Log.i("GalleryViewportDeviceTest",JSONObject().put("locale",tag).put("font_scale",2)
                                    .put("orientation",orientation).put("root_width",root.width).put("root_height",root.height)
                                    .put("controls_height",controls.height).put("browser_width",web.width).put("browser_height",web.height)
                                    .put("browser_visible",visible.toString()).put("required_reserve",reserve)
                                    .put("query_lines",search.layout.lineCount).put("search_ime_options",editorInfo.imeOptions)
                                    .put("search_input_type",editorInfo.inputType)
                                    .put("provider","real installed WebView; verified rejecting proxy; local HTML").toString())
                            }
                            if(Build.VERSION.SDK_INT>=35 && tag=="ar" && landscape) checkInstalledArabicStatusInk(gallery)
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

    /** Installed-device observation; no compatibility flags or core settings are changed. */
    @androidx.annotation.RequiresApi(35)
    private fun recordStatusGlyphWidthFlags(gallery: MediaGalleryActivity,tag: String,orientation: Int) {
        val view=gallery.window.decorView.findViewWithTag<android.widget.TextView>("gallery_status")
        val layout=requireNotNull(view.layout)
        val plain=android.widget.TextView(gallery)
        val vertical=tag=="mn-Mong"
        assertEquals(35,context.applicationInfo.targetSdkVersion)
        assertEquals(view.useBoundsForWidth,layout.useBoundsForWidth)
        if(vertical) {
            assertEquals("Vertical status retains the platform default",plain.useBoundsForWidth,view.useBoundsForWidth)
        } else {
            assertTrue("Installed horizontal status reserves glyph bounds",view.useBoundsForWidth)
            assertFalse(view.shiftDrawingOffsetForStartOverhang)
            assertFalse(layout.shiftDrawingOffsetForStartOverhang)
        }
        val report=JSONObject().put("locale",tag).put("font_scale",gallery.resources.configuration.fontScale)
            .put("orientation",orientation).put("target_sdk",context.applicationInfo.targetSdkVersion)
            .put("default_textview_use_bounds_for_width",plain.useBoundsForWidth)
            .put("status_use_bounds_for_width",view.useBoundsForWidth).put("layout_use_bounds_for_width",layout.useBoundsForWidth)
            .put("shift_drawing_offset_for_start_overhang",view.shiftDrawingOffsetForStartOverhang)
            .put("layout_shift_drawing_offset_for_start_overhang",layout.shiftDrawingOffsetForStartOverhang)
            .put("status_width",view.width).put("layout_width",layout.width).put("line_count",layout.lineCount)
            .put("compound_padding_left",view.compoundPaddingLeft).put("compound_padding_right",view.compoundPaddingRight)
            .put("baseline",view.baseline).put("layout_first_baseline",layout.getLineBaseline(0))
            .put("vertical_route",vertical).put("message",view.text.toString())
        if(!vertical) {
            assertEquals(view.width-view.compoundPaddingLeft-view.compoundPaddingRight,layout.width)
            report.put("glyph_bounds",android.graphics.RectF(layout.computeDrawingBoundingBox()).toString())
        }
        android.util.Log.i("GalleryStatusGlyphBounds",report.toString())
    }

    @androidx.annotation.RequiresApi(35)
    private fun checkInstalledArabicStatusInk(gallery: MediaGalleryActivity) {
        val allResults=android.os.Bundle()
        val failures=mutableListOf<String>()
        val source=InstrumentationRegistry.getArguments().getString("anpaint_source_tests_sha256")
        assertTrue("Installed evidence must bind to the runner's exact source inventory",source?.matches(Regex("[0-9a-f]{64}"))==true)
        for(insert in listOf(false,true)) {
            val route=if(insert) "insert" else "copy"
            val message=onMain {
                val reason=gallery.getString(R.string.commons_metadata_query_failed)
                gallery.getString(if(insert) R.string.ui_could_not_load_gallery_image else R.string.commons_credit_copy_failed_reason,reason)
                    .also {MediaGalleryActivity::class.java.getDeclaredMethod("showStatus",String::class.java)
                        .apply {isAccessible=true}.invoke(gallery,it)}
            }
            await("installed Arabic M04 $route layout") {onMain {
                val root=gallery.window.decorView;val view=root.findViewWithTag<TextView>("gallery_status")
                !root.isLayoutRequested && !view.isLayoutRequested && view.layout?.text?.toString()==message
            }}
            instrumentation.waitForIdleSync()
            onMain {
                val root=gallery.window.decorView
                val view=root.findViewWithTag<TextView>("gallery_status")
                assertEquals("ar",gallery.resources.configuration.locales[0].language)
                assertEquals(2f,gallery.resources.configuration.fontScale,0f)
                assertEquals(Configuration.ORIENTATION_LANDSCAPE,gallery.resources.configuration.orientation)
                assertEquals(message,view.text.toString());assertEquals(message,view.createAccessibilityNodeInfo().text.toString())
                capturePaintedInk(view).use {frame ->
                    fun png(bitmap: android.graphics.Bitmap): JSONObject {
                        val bytes=java.io.ByteArrayOutputStream().use {out ->
                            check(bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG,100,out));out.toByteArray()
                        }
                        return JSONObject().put("width",bitmap.width).put("height",bitmap.height).put("bytes",bytes.size)
                            .put("sha256",java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") {"%02x".format(it)})
                            .put("base64",android.util.Base64.encodeToString(bytes,android.util.Base64.NO_WRAP))
                    }
                    val report=paintedInkReport(frame).put("schema",1).put("route",route).put("locale","ar")
                        .put("evidence_kind","Installed API35 native software raster of injected actual status text; not network-route or hardware screenshot proof")
                        .put("source_tests_sha256",source).put("font_scale",2).put("api",Build.VERSION.SDK_INT)
                        .put("target_sdk",context.applicationInfo.targetSdkVersion).put("fingerprint",Build.FINGERPRINT)
                        .put("density",gallery.resources.displayMetrics.density).put("density_dpi",gallery.resources.displayMetrics.densityDpi)
                        .put("root_width",root.width).put("root_height",root.height).put("orientation",Configuration.ORIENTATION_LANDSCAPE)
                        .put("default_textview_use_bounds_for_width",TextView(gallery).useBoundsForWidth)
                        .put("message",message).put("accessibility_text",view.createAccessibilityNodeInfo().text.toString())
                        .put("complete_layout_text",view.layout.text.toString())
                        .put("actual_png",png(frame.actual)).put("reference_png",png(frame.reference))
                    val encoded=report.toString()
                    check(encoded.toByteArray(Charsets.UTF_8).size<=128*1024) {"Bounded installed ink record exceeded"}
                    val key="anpaint_m04_glyph_bounds_$route"
                    check(!allResults.containsKey(key));allResults.putString(key,encoded)
                    val parcel=android.os.Parcel.obtain()
                    try {parcel.writeBundle(allResults);check(parcel.dataSize()<=512*1024) {"Bounded installed ink Bundle exceeded"}}
                    finally {parcel.recycle()}
                    // Extra final-result data cannot create a test start or passing test result.
                    instrumentation.addResults(android.os.Bundle().apply {putString(key,encoded)})
                    try {assertPaintedInk(frame,"installed Arabic $route")}
                    catch(failure: AssertionError) {failures.add("$route: ${failure.message}")}
                }
            }
        }
        assertEquals(2,allResults.size())
        assertTrue("Installed Arabic ink failures: ${failures.joinToString()}",failures.isEmpty())
    }

    @androidx.annotation.RequiresApi(35)
    private data class PaintedInkFrame(
        val actual: android.graphics.Bitmap,val reference: android.graphics.Bitmap,
        val referencePixels: IntArray,val referenceBox: android.graphics.Rect,
        val originX: Int,val originY: Int,val contentWidth: Int,val glyphBounds: android.graphics.RectF,
        val viewBoundsWidth: Boolean,val layoutBoundsWidth: Boolean,val shiftedStart: Boolean,val leadingInset: Int,
        val inkPixels: Int,val inkLeft: Int,val inkRight: Int,val edgePixels: Int,
        val horizontalOverflow: Int,val outsideView: Int,val missingInk: Int,val differentPixels: Int
    ): java.io.Closeable {
        override fun close() {actual.recycle();reference.recycle()}
    }

    /** API35, plain horizontal status only. Unsupported drawing features fail closed. */
    @androidx.annotation.RequiresApi(35)
    private fun capturePaintedInk(view: TextView,translationX: Int=0,
        clipLeft: Int=0,clipRight: Int=view.width,expectedBoundsWidth: Boolean=true): PaintedInkFrame {
        val layout=requireNotNull(view.layout)
        assertEquals("Installed oracle is explicitly the horizontal Arabic profile","ar",view.resources.configuration.locales[0].language)
        assertEquals("gallery_status",view.tag)
        assertEquals("Reference must contain the complete actual text",view.text.toString(),layout.text.toString())
        assertTrue(view.text.isNotEmpty());assertTrue(layout.lineCount>0)
        var covered=0
        for(line in 0 until layout.lineCount) {
            assertEquals("Contiguous UTF-16 line coverage",covered,layout.getLineStart(line))
            assertEquals("No ellipsis in the complete reference",0,layout.getEllipsisCount(line))
            val end=layout.getLineEnd(line);assertTrue(end>=covered);covered=end
        }
        assertEquals(view.text.length,covered)
        val spanned=view.text as? android.text.Spanned
        val spans=spanned?.getSpans(0,view.text.length,Any::class.java).orEmpty()
        assertTrue("Only one measured geometry-only paragraph margin is supported",spans.size<=1)
        var leadingInset=0
        for(span in spans) {
            assertEquals(android.text.style.LeadingMarginSpan.Standard::class.java,span.javaClass)
            assertEquals(0,spanned!!.getSpanStart(span));assertEquals(view.text.length,spanned.getSpanEnd(span))
            assertEquals(android.text.Spanned.SPAN_EXCLUSIVE_EXCLUSIVE,spanned.getSpanFlags(span))
            val margin=span as android.text.style.LeadingMarginSpan.Standard
            leadingInset=margin.getLeadingMargin(true)
            assertTrue(leadingInset>0 && leadingInset<=kotlin.math.ceil(view.paint.textSize*2f).toInt())
            assertEquals(leadingInset,margin.getLeadingMargin(false))
        }
        assertEquals(android.text.Layout.Alignment.ALIGN_NORMAL,layout.alignment)
        assertEquals("Explicitly bound width-mode for this observation",expectedBoundsWidth,view.useBoundsForWidth)
        assertEquals("View and native Layout must agree on bounds-based width",view.useBoundsForWidth,layout.useBoundsForWidth)
        assertFalse("Shifted-overhang views need a separately reviewed origin",view.shiftDrawingOffsetForStartOverhang)
        assertFalse("Shifted-overhang layouts need a separately reviewed origin",layout.shiftDrawingOffsetForStartOverhang)
        assertNull(view.background);assertNull(view.foreground)
        assertTrue(view.compoundDrawables.all {it==null});assertNull(view.transformationMethod)
        assertEquals(-1,view.selectionStart);assertEquals(-1,view.selectionEnd)
        assertEquals(android.view.Gravity.TOP,view.gravity and android.view.Gravity.VERTICAL_GRAVITY_MASK)
        assertEquals(0,view.scrollX);assertEquals(0,view.scrollY)
        assertEquals(0f,view.rotation,0f);assertEquals(0f,view.rotationX,0f);assertEquals(0f,view.rotationY,0f)
        assertEquals(0f,view.translationX,0f);assertEquals(0f,view.translationY,0f)
        assertEquals(1f,view.scaleX,0f);assertEquals(1f,view.scaleY,0f);assertEquals(1f,view.alpha,0f)
        assertEquals(android.graphics.Paint.Style.FILL,view.paint.style)
        assertNull(view.paint.shader);assertNull(view.paint.colorFilter);assertNull(view.paint.maskFilter);assertNull(view.paint.pathEffect)
        assertFalse(view.paint.isUnderlineText);assertFalse(view.paint.isStrikeThruText);assertFalse(view.paint.isFakeBoldText)
        assertEquals(0f,view.paint.textSkewX,0f);assertEquals(0,view.paint.baselineShift)
        assertEquals(0f,view.shadowRadius,0f)
        val originX=view.compoundPaddingLeft
        val originY=view.baseline-layout.getLineBaseline(0)
        assertEquals("TOP baseline must identify the real draw origin",view.extendedPaddingTop,originY)
        val contentWidth=view.width-view.compoundPaddingLeft-view.compoundPaddingRight
        assertEquals("Native layout width must be the actual text clip width",contentWidth,layout.width)
        fun boundedBitmap(width: Int,height: Int): android.graphics.Bitmap {
            assertTrue("Positive, bounded native raster allocation",width>0 && height>0 && width.toLong()*height<=16_000_000L)
            return android.graphics.Bitmap.createBitmap(width,height,android.graphics.Bitmap.Config.ARGB_8888)
        }
        val actual=boundedBitmap(view.width,view.height)
        var reference: android.graphics.Bitmap?=null
        try {
            // The actual view retains its own native clip. No view/paint/text property is changed.
            val actualCanvas=android.graphics.Canvas(actual)
            actualCanvas.clipRect(clipLeft,0,clipRight,view.height)
            actualCanvas.translate(translationX.toFloat(),0f);view.draw(actualCanvas)
            // API35 derives this box from actual glyphs, including marks outside line metrics.
            // The union prevents a wholly displaced glyph from disappearing beyond a fixed margin.
            val bounds=android.graphics.RectF(layout.computeDrawingBoundingBox()).apply {offset(translationX.toFloat(),0f)}
            // API35 glyph bounds omit paragraph margins. The exact allowed span can
            // move any paragraph by at most this measured inset in either direction.
            val xs=mutableListOf(0f,layout.width.toFloat(),bounds.left-leadingInset,bounds.right+leadingInset)
            val ys=mutableListOf(0f,layout.height.toFloat(),bounds.top,bounds.bottom)
            for(line in 0 until layout.lineCount) {
                xs.add(layout.getLineLeft(line)+translationX);xs.add(layout.getLineRight(line)+translationX)
                ys.add(layout.getLineTop(line).toFloat());ys.add(layout.getLineBottom(line).toFloat())
            }
            assertTrue("Finite native glyph and line geometry",(xs+ys).all {it.isFinite() && kotlin.math.abs(it)<100_000f})
            assertTrue(bounds.left<=bounds.right && bounds.top<=bounds.bottom)
            // Two pixels are allocation guard only, never a containment or comparison tolerance.
            val box=android.graphics.Rect(kotlin.math.floor(xs.minOrNull()!!).toInt()-2,
                kotlin.math.floor(ys.minOrNull()!!).toInt()-2,kotlin.math.ceil(xs.maxOrNull()!!).toInt()+2,
                kotlin.math.ceil(ys.maxOrNull()!!).toInt()+2)
            val complete=boundedBitmap(box.width(),box.height());reference=complete
            val canvas=android.graphics.Canvas(complete)
            canvas.translate((translationX-box.left).toFloat(),(-box.top).toFloat());layout.draw(canvas)
            val expectedPixels=IntArray(complete.width*complete.height)
            complete.getPixels(expectedPixels,0,complete.width,0,0,complete.width,complete.height)
            val actualPixels=IntArray(actual.width*actual.height)
            actual.getPixels(actualPixels,0,actual.width,0,0,actual.width,actual.height)
            var ink=0;var left=Int.MAX_VALUE;var right=Int.MIN_VALUE;var edges=0
            var overflow=0;var outside=0;var missing=0;var different=0
            for(y in 0 until complete.height) for(x in 0 until complete.width) {
                val pixel=expectedPixels[y*complete.width+x]
                if((pixel ushr 24)==0) continue
                ink++;val localX=box.left+x;val localY=box.top+y
                left=minOf(left,localX);right=maxOf(right,localX+1)
                if(x==0 || y==0 || x==complete.width-1 || y==complete.height-1) edges++
                if(localX<0 || localX>=contentWidth) overflow++
                val vx=originX+localX;val vy=originY+localY
                if(vx !in 0 until actual.width || vy !in 0 until actual.height) {outside++;missing++}
                else if((actualPixels[vy*actual.width+vx] ushr 24)==0) missing++
            }
            // Compare the WHOLE actual view against the independent full reference. The
            // expected reference is never obtained by cropping the already-clipped actual view.
            for(y in 0 until actual.height) for(x in 0 until actual.width) {
                val rx=x-originX-box.left;val ry=y-originY-box.top
                val expected=if(rx in 0 until complete.width && ry in 0 until complete.height)
                    expectedPixels[ry*complete.width+rx] else 0
                if(actualPixels[y*actual.width+x]!=expected) different++
            }
            return PaintedInkFrame(actual,complete,expectedPixels,box,originX,originY,contentWidth,bounds,
                view.useBoundsForWidth,layout.useBoundsForWidth,layout.shiftDrawingOffsetForStartOverhang,leadingInset,ink,left,right,edges,overflow,outside,missing,different)
        } catch(failure: Throwable) {actual.recycle();reference?.recycle();throw failure}
    }

    @androidx.annotation.RequiresApi(35)
    private fun assertPaintedInk(frame: PaintedInkFrame,label: String) {
        assertTrue("$label complete reference must contain native ink",frame.inkPixels>0)
        assertEquals("$label reference raster must not touch allocation boundary",0,frame.edgePixels)
        assertEquals("$label horizontal painted-ink overflow",0,frame.horizontalOverflow)
        assertEquals("$label full reference ink lies outside the actual view",0,frame.outsideView)
        assertEquals("$label clipped expected ink",0,frame.missingInk)
        assertEquals("$label exact full-reference/actual-view ARGB mismatch",0,frame.differentPixels)
    }

    @androidx.annotation.RequiresApi(35)
    private fun paintedInkReport(frame: PaintedInkFrame)=org.json.JSONObject()
        .put("reference_source","Complete native Layout with API35 actual-glyph bounds; never an actual-view crop")
        .put("reference_box",frame.referenceBox.toShortString()).put("glyph_bounds",frame.glyphBounds.toString())
        .put("origin_x",frame.originX).put("origin_y",frame.originY).put("content_width",frame.contentWidth)
        .put("view_use_bounds_for_width",frame.viewBoundsWidth).put("layout_use_bounds_for_width",frame.layoutBoundsWidth)
        .put("shift_drawing_offset_for_start_overhang",frame.shiftedStart).put("measured_leading_inset_px",frame.leadingInset)
        .put("ink_pixels",frame.inkPixels).put("ink_left",frame.inkLeft).put("ink_right_exclusive",frame.inkRight)
        .put("allocation_edge_pixels",frame.edgePixels).put("horizontal_overflow_pixels",frame.horizontalOverflow)
        .put("outside_view_pixels",frame.outsideView).put("missing_expected_ink_pixels",frame.missingInk)
        .put("different_argb_pixels",frame.differentPixels).put("alpha_cutoff",0).put("position_tolerance_px",0)
        .put("color_tolerance",0)


    private fun selectLanguage(tag: String) {
        onMain {
            context.getSharedPreferences("app-language",0).edit().putString("language-tag",tag)
                .putBoolean("platform-initialized",true).commit()
            if(Build.VERSION.SDK_INT>=33) context.getSystemService(LocaleManager::class.java).applicationLocales=LocaleList.forLanguageTags(tag)
        }
        instrumentation.waitForIdleSync()
    }
    /** Reuse the same bounded, verified system transition in installed dialog checks. */
    internal fun transitionFontScale(scale: Float)=setFontScale(scale)

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
                legacyFontShell("settings put system font_scale $scale",deadline)
            }
            awaitUntil("real system font scale $scale",deadline,::matches)
            if(Build.VERSION.SDK_INT>=34) {
                // ATMS can distribute the new configuration before its queued
                // Settings write-back executes on DisplayThread. Flush that queue
                // before another transition can overwrite the pending snapshot.
                assertEquals("System configuration write-back barrier succeeded",0,
                    fontShell("am wait-for-broadcast-barrier --flush-broadcast-loopers",deadline))
            } else {
                awaitLegacyDisplayThread(deadline)
            }
            instrumentation.waitForIdleSync()
            assertTrue("Font transition exceeded its original 10s deadline",SystemClock.uptimeMillis()<deadline)
            assertTrue("Font setting and real resources must still agree after the barrier",matches())
        } finally {android.util.Log.i("GalleryViewportDeviceTest","font transition after: ${state()}")}
    }

    /**
     * API30-33 lack the shell looper-flush command. AOSP's ATMS configuration
     * persistence and DisplayManager display-event delivery share DisplayThread.
     * Register before creating a fresh private display, then require that exact
     * ID's added callback, release it, then require its removed callback. Under
     * normal FIFO delivery with no intervening synchronization barrier, this
     * covers the earlier configuration message and its pending font snapshot.
     * DMS messages are async and can bypass ordinary ATMS messages behind a
     * synchronization barrier. This is NOT a portable queue-drain guarantee;
     * exact-device verification and the real font/layout oracles remain required.
     * There is no Surface, mirroring, presentation, capture or app window.
     */
    private fun awaitLegacyDisplayThread(deadline: Long) {
        val manager=context.getSystemService(DisplayManager::class.java)
        val added=Collections.synchronizedSet(mutableSetOf<Int>())
        val removed=Collections.synchronizedSet(mutableSetOf<Int>())
        val listener=object: DisplayManager.DisplayListener {
            override fun onDisplayAdded(displayId: Int) {added.add(displayId)}
            override fun onDisplayChanged(displayId: Int) {}
            override fun onDisplayRemoved(displayId: Int) {removed.add(displayId)}
        }
        manager.registerDisplayListener(listener,Handler(Looper.getMainLooper()))
        try {
            assertTrue("No time remains for legacy display barrier",SystemClock.uptimeMillis()<deadline)
            val display=manager.createVirtualDisplay("ANPaint font synchronization",1,1,160,null,
                DisplayManager.VIRTUAL_DISPLAY_FLAG_OWN_CONTENT_ONLY)
            assertNotNull("Private display is required for the legacy font barrier",display)
            try {
                val id=display!!.display.displayId
                awaitUntil("DisplayThread added font barrier display $id",deadline) {added.contains(id)}
                display.release()
                awaitUntil("DisplayThread removed font barrier display $id",deadline) {removed.contains(id)}
                android.util.Log.i("GalleryViewportDeviceTest",JSONObject().put("font_display_barrier",id)
                    .put("remaining_ms",deadline-SystemClock.uptimeMillis()).toString())
            } finally {display!!.release()} // release() is idempotent, including after a failed wait.
        } finally {manager.unregisterDisplayListener(listener)}
    }

    /** Public read-only shell pipe on API30-33, bounded by the same deadline. */
    private fun legacyFontShell(command: String,deadline: Long) {
        val remaining=deadline-SystemClock.uptimeMillis()
        assertTrue("No time remains for legacy font shell",remaining>0)
        val seconds=String.format(Locale.ROOT,"%.3f",remaining/1000.0)
        val pipe=instrumentation.uiAutomation.executeShellCommand("timeout -s KILL ${seconds}s $command")
        val reader=Executors.newSingleThreadExecutor()
        try {
            val output=reader.submit<String> {
                ParcelFileDescriptor.AutoCloseInputStream(pipe).bufferedReader().use {it.readText()}
            }
            val readRemaining=deadline-SystemClock.uptimeMillis()
            assertTrue("No time remains to read legacy font shell",readRemaining>0)
            android.util.Log.i("GalleryViewportDeviceTest",JSONObject().put("legacy_font_shell",command)
                .put("stdout",output.get(readRemaining,TimeUnit.MILLISECONDS)).toString())
            assertTrue("Legacy font shell exceeded shared 10s deadline",SystemClock.uptimeMillis()<deadline)
        } finally {
            try {pipe.close()} catch(_: java.io.IOException) {}
            reader.shutdownNow()
        }
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
