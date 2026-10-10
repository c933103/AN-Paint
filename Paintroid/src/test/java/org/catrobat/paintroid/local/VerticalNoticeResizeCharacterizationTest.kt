/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.LocaleManager
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Rect
import android.os.Build
import android.os.Looper
import android.os.SystemClock
import android.text.TextPaint
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.view.WindowInsets
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityManager
import android.widget.FrameLayout
import android.widget.TextView
import android.widget.Toast
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONArray
import org.json.JSONObject
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
import org.robolectric.shadow.api.Shadow
import org.robolectric.shadows.ShadowAccessibilityRecord
import org.robolectric.shadows.ShadowToast
import org.robolectric.util.ReflectionHelpers as Reflection
import java.io.File
import java.time.Duration
import java.util.Locale
import kotlin.math.ceil
import kotlin.math.floor
import kotlin.math.max
import kotlin.math.min

/**
 * Current compiled-resource characterization, NOT a vertical foreground implementation.
 * C02/C03 call the unchanged horizontal helper directly. C04 inserts a test-only
 * vertical drawing child. Production routes for all five profiles remain system toasts.
 * Host event requests are not a recording of TalkBack speech or installed-device events.
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35], qualifiers="en-rUS-w420dp-h680dp-port-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class VerticalNoticeResizeCharacterizationTest {
    class NoticeActivity: Activity() {
        override fun attachBaseContext(base: Context) {
            super.attachBaseContext(AppLanguage.wrap(base))
        }
    }

    private val tags=listOf("mn-Mong","mnc-Mong","lzh-Hant","en-XV","qaa-Zsye-XV")
    private val nullFaces=setOf("lzh-Hant","en-XV","qaa-Zsye-XV")
    private val joinedEmoji="😀‍😀‍😀‍😀‍😀‍😀.png"
    private val app get()=RuntimeEnvironment.getApplication() as Context
    private val output get()=File("build/reports/vertical-notice-resize").apply {mkdirs()}
    private fun settle(ms: Long=64)=shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(ms))
    private fun now()=SystemClock.uptimeMillis()
    private fun host(a: Activity)=a.findViewById<FrameLayout>(android.R.id.content)
    private fun notice(a: Activity)=host(a).findViewWithTag<FrameLayout>("locale_notification")
    private fun label(a: Activity)=host(a).findViewWithTag<TextView>("locale_notification_text")
    private fun combined(a: Activity)=a.getString(R.string.ui_cursor_pan_move32)+"\n"+a.getString(R.string.ui_cursor_tap_hint37)

    private fun expected(tag: String): JSONObject {
        val bytes=javaClass.getResourceAsStream("/vertical-notice-resize/expected-resources.json")
        assertNotNull("Compiled-resource oracle must be packaged in the test classpath",bytes)
        return bytes!!.bufferedReader().use {JSONObject(it.readText()).getJSONObject("locales").getJSONObject(tag)}
    }

    /** C01: compiled resources and actual message entry point, not an actual save/provider operation. */
    @Test fun compiledAppResourcesKeepFiveVerticalProfilesOnSystemToasts()=withLanguageState {
        report("routes") {rows->
            assertTrue(AppLanguage.tags(app).containsAll(tags))
            assertTrue(ExportNames.valid(joinedEmoji,ImageFormat.PNG))
            assertEquals(joinedEmoji,ExportNames.withExtension(joinedEmoji,ImageFormat.PNG))
            assertEquals(1,VerticalText.clusters(joinedEmoji.removeSuffix(".png")).size)
            for(tag in tags) withActivity(tag) {a->
                val oracle=expected(tag)
                assertEquals(oracle.getString("ui_cursor_pan_move32"),a.getString(R.string.ui_cursor_pan_move32))
                assertEquals(oracle.getString("ui_cursor_tap_hint37"),a.getString(R.string.ui_cursor_tap_hint37))
                assertEquals(oracle.getString("ui_saved"),a.getString(R.string.ui_saved))
                assertEquals(tag in nullFaces,LocaleTypography.typeface(a)==null)
                val expectedDirection=if(tag=="lzh-Hant" || tag=="qaa-Zsye-XV")
                    TextDirection.VERTICAL_RL else TextDirection.VERTICAL_LR
                assertEquals(expectedDirection,VerticalText.uiDirection())
                val cursor=combined(a)
                assertEquals(1,cursor.count {it=='\n'})
                val saved=a.getString(R.string.ui_saved,joinedEmoji)
                assertEquals(oracle.getString("ui_saved").replace("%1\$s",joinedEmoji),saved)
                for((kind,text) in listOf("combined" to cursor,"joined-emoji-save" to saved)) {
                    ShadowToast.reset()
                    LocaleTypography.showMessage(a,text,Toast.LENGTH_LONG)
                    settle()
                    assertNull("Vertical profile must not take the direct-helper diagnostic route",notice(a))
                    assertEquals(1,ShadowToast.shownToastCount())
                    assertEquals(text,ShadowToast.getTextOfLatestToast())
                    rows.put(baseRow(tag).put("kind",kind).put("text",text)
                        .put("route","system-toast").put("configured_face",LocaleTypography.asset() ?: JSONObject.NULL)
                        .put("direction",expectedDirection.name).put("resource_locale",a.resources.configuration.locales[0].toLanguageTag()))
                }
            }
            assertEquals(10,rows.length())
        }
    }

    /** C02: no vertical body or fallback switch is used in this test. */
    @Test fun unchangedHorizontalDirectHelperKeepsNodeTextAndDeadlineAcrossRepeatedGeometryChanges()=withLanguageState {
        report("transitions") {rows->
            var noFitRows=0
            for(tag in tags) for(edgeToEdge in listOf(false,true)) withActivity(tag,edgeToEdge) {a->
                withFullInsetsMode {
                    val manager=a.getSystemService(AccessibilityManager::class.java)
                    val oldTimeout=Reflection.getField<Int>(manager,"mNonInteractiveUiTimeout")
                    shadowOf(manager).setNonInteractiveUiTimeout(8000)
                    try {
                        val text=combined(a)
                        var touches=0
                        (host(a).getChildAt(0) as FrameLayout).addView(View(a).apply {
                            setOnTouchListener {_,_->touches++;true}
                        },FrameLayout.LayoutParams(-1,-1))
                        ShadowToast.reset()
                        val shownAt=now()
                        assertTrue(LocaleNotification.show(a,text,Toast.LENGTH_SHORT,
                            LocaleTypography.typeface(a) ?: TextView(a).typeface,null))
                        settle()
                        val n=notice(a);val body=label(a)
                        assertNotNull(n);assertNotNull(body)
                        val phases=listOf("initial","ime","restored","shrink180","shrink124","expand","same-layout")
                        for(phase in phases) {
                            when(phase) {
                                "ime" -> injectIme(a.window.decorView,320)
                                "restored" -> injectIme(a.window.decorView,0)
                                "shrink180" -> a.window.setLayout(420,180)
                                "shrink124" -> a.window.setLayout(420,124)
                                "expand","same-layout" -> a.window.setLayout(420,680)
                            }
                            settle()
                            if(phase=="ime") assertEquals(320,host(a).rootWindowInsets.getInsets(WindowInsets.Type.ime()).bottom)
                            if(phase=="restored") assertEquals(0,host(a).rootWindowInsets.getInsets(WindowInsets.Type.ime()).bottom)
                            if(phase.startsWith("shrink")) assertEquals(phase.removePrefix("shrink").toInt(),host(a).rootView.height)
                            assertSame(n,notice(a));assertSame(body,label(a))
                            assertLogicalText(body,text)
                            assertInsets(a,n)
                            assertEquals(0,ShadowToast.shownToastCount())
                            val fullHeight=body.layout.height+body.compoundPaddingTop+body.compoundPaddingBottom
                            assertEquals(text.length,body.layout.getLineEnd(body.layout.lineCount-1))
                            val geometryFits=fullHeight<=body.height
                            if(!geometryFits) noFitRows++
                            val id=tag+"-"+edgeToEdge+"-"+phase
                            val pixels=horizontalPixels(n,body,id,phase=="shrink124")
                            rows.put(baseRow(tag).put("phase",phase).put("edge_to_edge",edgeToEdge)
                                .put("at_ms",now()-shownAt).put("original_expiry_ms",8000)
                                .put("host_width",host(a).width).put("host_height",host(a).height)
                                .put("body_width",body.width).put("body_height",body.height)
                                .put("complete_horizontal_height",fullHeight).put("complete_layout_fits",geometryFits)
                                .put("last_line_end",body.layout.getLineEnd(body.layout.lineCount-1))
                                .put("notice_identity",System.identityHashCode(n)).put("node_identity",System.identityHashCode(body))
                                .put("logical_text",text).put("pixels",pixels))
                        }
                        assertFalse(n.isFocusable);assertFalse(body.isFocusable)
                        val touch=MotionEvent.obtain(now(),now(),MotionEvent.ACTION_DOWN,30f,20f,0)
                        try {assertTrue(host(a).dispatchTouchEvent(touch))} finally {touch.recycle()}
                        assertEquals(1,touches)
                        advanceTo(shownAt+7999);assertSame(n,notice(a))
                        advanceTo(shownAt+8001);assertNull(notice(a))
                        assertEquals(0,ShadowToast.shownToastCount())
                        // Existing replacement/detach tests remain the authoritative broader lifecycle controls.
                        rows.put(baseRow(tag).put("phase","expired").put("edge_to_edge",edgeToEdge)
                            .put("at_ms",now()-shownAt).put("original_expiry_ms",8000).put("toast_count",0))
                    } finally {shadowOf(manager).setNonInteractiveUiTimeout(oldTimeout)}
                }
            }
            assertEquals(80,rows.length())
            assertTrue("The bounded shrink matrix must exercise a complete horizontal no-fit case",noFitRows>0)
        }
    }

    /** C03: snapshot event requests before Android recycles them; never infer speech from event counts. */
    @Test fun accessibilityObserverSeesControlsAndSeparatesInitialContentFromGeometryEvents()=withLanguageState {
        report("events") {rows->
            for(tag in listOf("mn-Mong","lzh-Hant")) withActivity(tag) {a->
                val manager=a.getSystemService(AccessibilityManager::class.java)
                val wasEnabled=manager.isEnabled
                val oldTimeout=Reflection.getField<Int>(manager,"mNonInteractiveUiTimeout")
                shadowOf(manager).setEnabled(true)
                shadowOf(manager).setNonInteractiveUiTimeout(30000)
                val recorder=EventRecorder(rows,tag)
                host(a).accessibilityDelegate=recorder
                ShadowToast.reset()
                try {
                    recorder.phase="initial"
                    val text=combined(a)
                    assertTrue(LocaleNotification.show(a,text,Toast.LENGTH_LONG,
                        LocaleTypography.typeface(a) ?: TextView(a).typeface,null))
                    settle(300)
                    val n=notice(a);val body=label(a)
                    assertTrue(body.isAttachedToWindow);assertTrue(body.isShown)
                    assertLogicalText(body,text)

                    // Deliberate TEST control only: validates event type, payload and exact source identity.
                    recorder.phase="explicit-positive-control"
                    val marker="notice-observer-positive-"+tag
                    val first=recorder.events.size
                    body.announceForAccessibility(marker)
                    settle(300)
                    assertTrue("Observer must see an announcement from the actual node",
                        recorder.events.drop(first).any {it.type==AccessibilityEvent.TYPE_ANNOUNCEMENT &&
                            it.source===body && marker in it.text})

                    recorder.phase="quiet-control"
                    val quietStart=recorder.events.size
                    settle(300)
                    assertFalse(recorder.events.drop(quietStart).any {it.type==AccessibilityEvent.TYPE_ANNOUNCEMENT})

                    for(phase in listOf("same-layout","shrink","expand","same-text-assignment")) {
                        recorder.phase=phase
                        val before=recorder.events.size
                        if(phase=="same-text-assignment") body.text=text
                        else a.window.setLayout(420,if(phase=="shrink") 180 else 680)
                        settle(300)
                        assertSame(n,notice(a));assertSame(body,label(a));assertLogicalText(body,text)
                        assertEquals(0,ShadowToast.shownToastCount())
                        // Ordinary content-change events are recorded, not suppressed or assumed absent.
                        assertFalse("Geometry/same-text path must not request an explicit announcement",
                            recorder.events.drop(before).any {it.type==AccessibilityEvent.TYPE_ANNOUNCEMENT})
                    }

                    recorder.phase="changed-text-positive-control"
                    val changed=text+"\nobserver replacement"
                    val beforeChange=recorder.events.size
                    body.text=changed
                    settle(500)
                    assertLogicalText(body,changed)
                    assertTrue("A working observer must see a genuine TextView content mutation",
                        recorder.events.drop(beforeChange).any {it.source===body &&
                            (it.type==AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED ||
                                it.type==AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED &&
                                it.changes and AccessibilityEvent.CONTENT_CHANGE_TYPE_TEXT != 0)})
                    rows.put(baseRow(tag).put("record_kind","observer-controls")
                        .put("explicit_announcement_observed",true).put("real_text_mutation_observed",true)
                        .put("event_count",recorder.events.size).put("toast_count",ShadowToast.shownToastCount()))
                } finally {
                    host(a).accessibilityDelegate=null
                    shadowOf(manager).setEnabled(wasEnabled)
                    shadowOf(manager).setNonInteractiveUiTimeout(oldTimeout)
                }
            }
            assertTrue(rows.length()>2)
        }
    }

    /** C04: shared renderer, independently clipped native reference, actual Notice parent. */
    @Test fun currentRendererNominalFitIsNotAnInkContainmentOracle()=withLanguageState {
        report("ink") {rows->
            var clippedCounterexamples=0;var ordinaryControls=0
            for(tag in tags) withActivity(tag) {a->
                for((kind,name) in listOf("unsupported-zwj" to joinedEmoji,
                    "ordinary-emoji" to "𠲎🖌️绘画.png","joined-word" to "ᠮᠣᠩᠭᠣᠯ.png")) {
                    assertTrue(ExportNames.valid(name,ImageFormat.PNG))
                    assertEquals(name,ExportNames.withExtension(name,ImageFormat.PNG))
                    val text=a.getString(R.string.ui_saved,name)
                    ShadowToast.reset()
                    LocaleTypography.showMessage(a,text,Toast.LENGTH_SHORT)
                    assertNull(notice(a));assertEquals(1,ShadowToast.shownToastCount())
                    ShadowToast.reset()
                    // Test-only bypass. Null-configured faces use the actual TextView default face.
                    assertTrue(LocaleNotification.show(a,text,Toast.LENGTH_LONG,
                        LocaleTypography.typeface(a) ?: TextView(a).typeface,null))
                    settle()
                    val n=notice(a);val original=label(a)
                    assertLogicalText(original,text)
                    val margins=FrameLayout.LayoutParams(original.layoutParams as FrameLayout.LayoutParams)
                    val safeW=n.width-n.paddingLeft-n.paddingRight-margins.leftMargin-margins.rightMargin-original.paddingLeft-original.paddingRight
                    val safeH=n.height-n.paddingTop-n.paddingBottom-margins.topMargin-margins.bottomMargin-original.paddingTop-original.paddingBottom
                    assertTrue(safeW>0 && safeH>0)
                    val direction=VerticalText.uiDirection()
                    val paint=TextPaint(original.paint).apply {color=Color.BLACK}
                    var wrapped=VerticalText.wrapLabel(text,paint,min(240f*original.resources.displayMetrics.density,safeH.toFloat()),direction)
                    var bounds=VerticalText.bounds(wrapped,paint,direction,GlyphOrientation.MIXED,1f)
                    if(ceil(bounds.width())>safeW) {
                        wrapped=VerticalText.wrapLabel(text,paint,safeH.toFloat(),direction)
                        bounds=VerticalText.bounds(wrapped,paint,direction,GlyphOrientation.MIXED,1f)
                    }
                    assertTrue("Bounded characterization requires nominally fitting controls",
                        ceil(bounds.width())<=safeW && ceil(bounds.height())<=safeH)
                    val width=original.width
                    val height=ceil(bounds.height()).toInt()+original.paddingTop+original.paddingBottom
                    val x=if(direction==TextDirection.VERTICAL_RL) width-original.paddingRight-bounds.width() else original.paddingLeft.toFloat()
                    val y=original.paddingTop.toFloat()
                    val guard=ceil(paint.textSize*4).toInt()
                    val shiftX=guard-floor(min(0f,x)).toInt()
                    val refWidth=ceil(max(width.toFloat(),x+bounds.width())).toInt()+shiftX+guard
                    val reference=Bitmap.createBitmap(refWidth,height+2*guard,Bitmap.Config.ARGB_8888)
                    try {
                        Canvas(reference).apply {translate(shiftX+x,guard+y)
                            VerticalText.draw(this,wrapped,paint,direction,GlyphOrientation.MIXED)}
                        val diagnostic=object: View(a) {
                            override fun onDraw(canvas: Canvas) {
                                canvas.save();canvas.translate(x,y)
                                VerticalText.draw(canvas,wrapped,paint,direction,GlyphOrientation.MIXED)
                                canvas.restore()
                            }
                        }.apply {this.tag="diagnostic_vertical_body";importantForAccessibility=View.IMPORTANT_FOR_ACCESSIBILITY_NO}
                        n.removeView(original)
                        n.addView(diagnostic,FrameLayout.LayoutParams(margins).apply {this.height=height})
                        settle()
                        assertEquals(width,diagnostic.width);assertEquals(height,diagnostic.height)
                        val pixels=compareReferenceToParent(n,diagnostic,reference,shiftX,guard,tag+"-"+kind,true)
                        if(kind=="unsupported-zwj") {
                            assertTrue("Counterexample must show ACTUAL ink loss, not just nominal overhang",
                                pixels.getInt("clipped_ink_pixels")>0)
                            clippedCounterexamples++
                        } else {
                            assertEquals("Fitting ordinary/joined-word controls must remain contained",0,pixels.getInt("clipped_ink_pixels"))
                            ordinaryControls++
                        }
                        rows.put(baseRow(tag).put("kind",kind).put("logical_text",text)
                            .put("direction",direction.name).put("text_size_px",paint.textSize)
                            .put("font_scale",a.resources.configuration.fontScale)
                            .put("paint_locales",paint.textLocales.toLanguageTags())
                            .put("nominal_width",bounds.width()).put("nominal_height",bounds.height())
                            .put("safe_width",safeW).put("safe_height",safeH).put("nominal_fits",true)
                            .put("scope","test-only vertical drawing child through unchanged Notice").put("pixels",pixels))
                    } finally {reference.recycle();host(a).removeView(n);settle()}
                    assertEquals(0,ShadowToast.shownToastCount())
                }
            }
            assertEquals(5,clippedCounterexamples);assertEquals(10,ordinaryControls);assertEquals(15,rows.length())
        }
    }

    private fun horizontalPixels(n: FrameLayout,body: TextView,id: String,capture: Boolean): JSONObject {
        assertEquals(0,body.scrollX);assertEquals(0,body.scrollY)
        val guard=ceil(body.textSize*4).toInt()
        val completeHeight=body.layout.height+body.compoundPaddingTop+body.compoundPaddingBottom
        val reference=Bitmap.createBitmap(body.width+2*guard,max(body.height,completeHeight)+2*guard,Bitmap.Config.ARGB_8888)
        val background=body.background
        assertEquals(Gravity.TOP,body.gravity and Gravity.VERTICAL_GRAVITY_MASK)
        assertEquals(0f,body.shadowRadius,0f)
        // TextView.onDraw selects stateful text paint before drawing its Layout.
        // Prime that real path rather than guessing EditorColours/paint state.
        val priming=Bitmap.createBitmap(body.width,body.height,Bitmap.Config.ARGB_8888)
        try {body.draw(Canvas(priming))} finally {priming.recycle()}
        try {
            Canvas(reference).apply {
                translate((guard+body.compoundPaddingLeft).toFloat(),(guard+body.extendedPaddingTop).toFloat())
                body.layout.draw(this)
            }
            // Paint exactly the live TextView via its actual parent, omitting only the background.
            body.background=null
            // TextView's own content clip precedes the actual FrameLayout child/parent clips.
            // API30/35 onDraw uses this padding/scroll rule; no text shadow or vertical gravity here.
            val maxScroll=body.layout.height-(body.height-body.compoundPaddingTop-body.compoundPaddingBottom)
            val contentClip=Rect(body.compoundPaddingLeft,0,body.width-body.compoundPaddingRight,
                body.height-if(maxScroll==0) 0 else body.extendedPaddingBottom)
            return compareReferenceToParent(n,body,reference,guard,guard,id,capture,contentClip)
        } finally {body.background=background;reference.recycle()}
    }

    private fun compareReferenceToParent(n: FrameLayout,child: View,reference: Bitmap,shiftX: Int,shiftY: Int,
        id: String,capture: Boolean,drawingClip: Rect=Rect(0,0,child.width,child.height)): JSONObject {
        assertTrue(n.clipChildren);assertTrue(child.width>0 && child.height>0)
        val ref=IntArray(reference.width*reference.height)
        reference.getPixels(ref,0,reference.width,0,0,reference.width,reference.height)
        val expected=IntArray(n.width*n.height)
        var total=0;var clipped=0;var left=Int.MAX_VALUE;var top=Int.MAX_VALUE
        var right=Int.MIN_VALUE;var bottom=Int.MIN_VALUE
        for(i in ref.indices) if(Color.alpha(ref[i])!=0) {
            total++
            val x=i%reference.width-shiftX;val y=i/reference.width-shiftY
            left=min(left,x);top=min(top,y);right=max(right,x+1);bottom=max(bottom,y+1)
            val nx=child.left+x;val ny=child.top+y
            val inParent=nx in 0 until n.width && ny in 0 until n.height &&
                (!n.clipToPadding || nx>=n.paddingLeft && nx<n.width-n.paddingRight &&
                    ny>=n.paddingTop && ny<n.height-n.paddingBottom)
            if(x in 0 until child.width && y in 0 until child.height && drawingClip.contains(x,y) && inParent) expected[ny*n.width+nx]=ref[i]
            else clipped++
        }
        assertTrue("Reference must have painted positive-control ink: "+id,total>0)
        assertTrue("Reference guard must not itself crop any ink: "+id,
            left> -shiftX && top> -shiftY && right<reference.width-shiftX && bottom<reference.height-shiftY)
        val actualBitmap=Bitmap.createBitmap(n.width,n.height,Bitmap.Config.ARGB_8888)
        try {
            n.draw(Canvas(actualBitmap))
            val actual=IntArray(expected.size)
            actualBitmap.getPixels(actual,0,n.width,0,0,n.width,n.height)
            assertArrayEquals("Actual parent pixels must equal independently clipped full reference: "+id,expected,actual)
            val visible=actual.count {Color.alpha(it)!=0}
            assertEquals("Parent must lose precisely the escaped reference ink: "+id,total-clipped,visible)
            if(capture) {savePng(reference,id+"-reference");savePng(actualBitmap,id+"-parent")}
            return JSONObject().put("reference_ink_pixels",total).put("visible_ink_pixels",visible)
                .put("clipped_ink_pixels",clipped).put("left",left).put("top",top).put("right",right).put("bottom",bottom)
                .put("parent_reference_pixel_equal",true).put("reference_guard_clear",true)
        } finally {actualBitmap.recycle()}
    }

    private data class SeenEvent(val type: Int,val changes: Int,val source: View?,val text: List<String>)
    private inner class EventRecorder(private val rows: JSONArray,private val language: String): View.AccessibilityDelegate() {
        var phase="setup"
        val events=mutableListOf<SeenEvent>()
        override fun onRequestSendAccessibilityEvent(host: ViewGroup,child: View,event: AccessibilityEvent): Boolean {
            val source=Shadow.extract<ShadowAccessibilityRecord>(event).sourceRoot
            val text=event.text.map {it.toString()}
            events.add(SeenEvent(event.eventType,event.contentChangeTypes,source,text))
            rows.put(baseRow(language).put("record_kind","event_request").put("phase",phase).put("uptime_ms",now())
                .put("event_type",event.eventType).put("content_change_types",event.contentChangeTypes)
                .put("source_identity",source?.let {System.identityHashCode(it)} ?: JSONObject.NULL)
                .put("source_tag",source?.tag?.toString() ?: JSONObject.NULL).put("event_text",JSONArray(text))
                .put("source_logical_text",(source as? TextView)?.text?.toString() ?: JSONObject.NULL)
                .put("child_identity",System.identityHashCode(child)))
            return super.onRequestSendAccessibilityEvent(host,child,event)
        }
    }

    private fun assertLogicalText(body: TextView,text: String) {
        assertEquals(text,body.text.toString())
        val node=body.createAccessibilityNodeInfo()
        try {assertEquals(text,node.text.toString())} finally {node.recycle()}
        assertEquals(View.ACCESSIBILITY_LIVE_REGION_POLITE,body.accessibilityLiveRegion)
        assertEquals(View.IMPORTANT_FOR_ACCESSIBILITY_YES,body.importantForAccessibility)
    }

    private fun assertInsets(a: Activity,n: FrameLayout) {
        val safe=host(a).rootWindowInsets.getInsets(WindowInsets.Type.systemBars() or WindowInsets.Type.displayCutout() or WindowInsets.Type.ime())
        val location=IntArray(2);n.getLocationInWindow(location)
        // Independent coordinate subtraction, not a call to the production inset helper.
        assertEquals(max(0,safe.left-location[0]),n.paddingLeft)
        assertEquals(max(0,safe.top-location[1]),n.paddingTop)
        assertEquals(max(0,location[0]+n.width-n.rootView.width+safe.right),n.paddingRight)
        assertEquals(max(0,location[1]+n.height-n.rootView.height+safe.bottom),n.paddingBottom)
    }

    /** Same WM-state injection as PR26. No real IME or replacement inset implementation. */
    private fun injectIme(decor: View,height: Int) {
        fun call(target: Any,name: String,vararg p: Reflection.ClassParameter<*>): Any? =
            Reflection.callInstanceMethod<Any?>(target,name,*p)
        val root=call(decor,"getViewRootImpl")!!
        val controller=call(root,"getInsetsController")!!
        val state=call(controller,"getState")!!
        val stateClass=Class.forName("android.view.InsetsState")
        val copy=stateClass.getConstructor(stateClass,Boolean::class.javaPrimitiveType).newInstance(state,true)
        val frame=Reflection.getField<Rect>(controller,"mFrame")
        assertTrue(frame.width()>0 && frame.height()>height)
        val source=if(Build.VERSION.SDK_INT<31) call(copy,"getSource",Reflection.ClassParameter.from(Int::class.javaPrimitiveType,13))!!
            else call(copy,"getOrCreateSource",Reflection.ClassParameter.from(Int::class.javaPrimitiveType,
                Reflection.getStaticField<Int>(Class.forName("android.view.InsetsSource"),"ID_IME")),
                Reflection.ClassParameter.from(Int::class.javaPrimitiveType,WindowInsets.Type.ime()))!!
        call(source,"setFrame",Reflection.ClassParameter.from(Rect::class.java,Rect(frame.left,frame.bottom-height,frame.right,frame.bottom)))
        call(source,"setVisible",Reflection.ClassParameter.from(Boolean::class.javaPrimitiveType,height>0))
        @Suppress("UNCHECKED_CAST")
        call(controller,"onStateChanged",Reflection.ClassParameter.from(stateClass as Class<Any>,copy))
        call(root,"dispatchApplyInsets",Reflection.ClassParameter.from(View::class.java,decor))
        assertEquals(height>0,decor.rootWindowInsets.isVisible(WindowInsets.Type.ime()))
    }

    private fun withFullInsetsMode(check: ()->Unit) {
        val type=Class.forName("android.view.ViewRootImpl")
        val old=if(Build.VERSION.SDK_INT==30) Reflection.getStaticField<Int>(type,"sNewInsetsMode") else null
        try {if(old!=null) Reflection.setStaticField(type,"sNewInsetsMode",2);check()}
        finally {if(old!=null) Reflection.setStaticField(type,"sNewInsetsMode",old)}
    }

    private fun withActivity(tag: String,edgeToEdge: Boolean=false,check: (NoticeActivity)->Unit) {
        AppLanguage.select(app,tag)
        PaintApplication.currentResources=AppLanguage.wrap(app).resources
        val controller=Robolectric.buildActivity(NoticeActivity::class.java)
        val a=controller.get()
        a.setTheme(R.style.ClassicPaintTheme)
        controller.setup()
        a.window.setDecorFitsSystemWindows(!edgeToEdge)
        a.window.setLayout(420,680)
        a.setContentView(FrameLayout(a))
        controller.visible().windowFocusChanged(true);settle()
        try {
            assertEquals(tag,a.resources.configuration.locales[0].toLanguageTag())
            assertEquals(tag,Locale.getDefault().toLanguageTag())
            assertTrue(host(a).isAttachedToWindow);assertTrue(host(a).width>0 && host(a).height>0)
            assertEquals(1f,a.resources.configuration.fontScale,0f)
            assertEquals(1f,a.resources.displayMetrics.density,0f)
            check(a)
        } finally {a.finish();controller.close();settle();ShadowToast.reset()}
    }

    private fun advanceTo(deadline: Long) {
        val remaining=deadline-now()
        assertTrue("Fixture must reach its assertion before the deadline",remaining>=0)
        settle(remaining)
    }

    private fun savePng(bitmap: Bitmap,id: String) {
        File(output,"api"+Build.VERSION.SDK_INT+"-"+id+".png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))
        }
    }

    private fun baseRow(tag: String)=JSONObject().put("api",Build.VERSION.SDK_INT).put("locale",tag)
    private fun report(name: String,check: (JSONArray)->Unit) {
        val rows=JSONArray()
        var completed=false
        try {check(rows);completed=true} finally {
            File(output,"api"+Build.VERSION.SDK_INT+"-"+name+".json").writeText(JSONObject()
                .put("schema",1).put("completed",completed)
                .put("build_commit",System.getenv("GITHUB_SHA") ?: "local-unreported")
                .put("run_id",System.getenv("GITHUB_RUN_ID") ?: JSONObject.NULL)
                .put("evidence_kind","Compiled-resource Robolectric NATIVE characterization; not installed execution or TalkBack speech")
                .put("production_vertical_route",false).put("rows",rows).toString(2)+"\n")
        }
    }

    private fun withLanguageState(check: ()->Unit) {
        val oldLocale=Locale.getDefault()
        val oldResources=PaintApplication.currentResources
        val preferences=app.getSharedPreferences("app-language",Context.MODE_PRIVATE)
        val oldTag=preferences.getString("language-tag",null)
        val hadInitialized=preferences.contains("platform-initialized")
        val oldInitialized=preferences.getBoolean("platform-initialized",false)
        val manager=if(Build.VERSION.SDK_INT>=33) app.getSystemService(LocaleManager::class.java) else null
        val oldPlatform=manager?.applicationLocales
        try {check()} finally {
            if(oldPlatform!=null) manager.applicationLocales=oldPlatform
            val edit=preferences.edit()
            if(oldTag==null) edit.remove("language-tag") else edit.putString("language-tag",oldTag)
            if(hadInitialized) edit.putBoolean("platform-initialized",oldInitialized) else edit.remove("platform-initialized")
            assertTrue(edit.commit())
            PaintApplication.currentResources=oldResources
            Locale.setDefault(oldLocale)
        }
    }
}
