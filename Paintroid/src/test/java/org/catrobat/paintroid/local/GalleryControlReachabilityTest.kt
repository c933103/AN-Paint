/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.content.Intent
import android.content.res.Configuration
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Rect
import android.net.Uri
import android.os.Looper
import android.os.SystemClock
import android.util.DisplayMetrics
import android.view.Display
import android.view.MotionEvent
import android.view.View
import android.webkit.WebView
import android.widget.EditText
import android.widget.TextView
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
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.shadows.ShadowDisplayManager
import org.robolectric.util.ReflectionHelpers
import java.io.File
import java.util.Locale

/** Real Activity controls remain reachable by scrolling, focus and clicks in small windows. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class GalleryControlReachabilityTest {
    @Test @Config(fontScale=1f)
    fun portraitControlsAtNormalText()=check()

    @Test @Config(fontScale=2f)
    fun portraitControlsAtLargeText()=check()

    @Test @Config(fontScale=2f,qualifiers="w240dp-h480dp-port-xhdpi")
    fun narrowControlsAtLargeText()=check()

    @Test @Config(fontScale=2f,qualifiers="w640dp-h320dp-land-xhdpi")
    fun landscapeControlsAtLargeText()=check()

    private fun check() {
        val app=RuntimeEnvironment.getApplication() as Context
        val originalTag=AppLanguage.selectedTag(app)
        val originalLocale=Locale.getDefault()
        val originalResources=PaintApplication.currentResources
        val credit=ImageCredit("https://example.org/gallery-layout.png","Retained layout fixture credit")
        val retained=ImageCreditArchive.retainAccepted(app,listOf(credit))
        try {
            for(tag in listOf("fr","hak-Latn-TW","ar","vi-Hani","bo","dz","mn-Mong","mnc-Mong","lzh-Hant")) {
                AppLanguage.select(app,tag);PaintApplication.currentResources=AppLanguage.wrap(app).resources
                val controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,
                    Intent(app,MediaGalleryActivity::class.java).putExtra("gallery_provider",IllustrationSource.COMMONS.name)
                        .putExtra("document_image_credits",ImageCredit.write(listOf(credit)).toString()))
                    .setup().visible().windowFocusChanged(true)
                val activity=controller.get()
                try {
                    val root=activity.window.decorView
                    val controls=root.findViewWithTag<GalleryControlsScroll>("gallery_controls_scroll")
                    val status=root.findViewWithTag<TextView>("gallery_status")
                    val web=ReflectionHelpers.getField<WebView>(activity,"web")
                    val message=activity.getString(R.string.ui_could_not_load_gallery_image,activity.getString(R.string.commons_svg_original_size_unavailable))
                    ReflectionHelpers.callInstanceMethod<Unit>(activity,"showStatus",ReflectionHelpers.ClassParameter.from(String::class.java,message))
                    layout(root)
                    record(root,tag,"status")
                    GalleryControlsLayoutTest.assertFullLayout("$tag/status",status)
                    assertEveryPartReachable(status,controls)
                    val actions=listOf("gallery_copy_credits","gallery_edit_credits","gallery_terms","gallery_done",
                        "gallery_legacy_credits","gallery_back","gallery_search_go")
                    val rectangles=JSONArray()
                    for(name in actions) {
                        val button=root.findViewWithTag<TextView>(name)
                        assertNotNull(name,button)
                        GalleryControlsLayoutTest.assertFullLayout("$tag/$name",button)
                        assertEveryPartReachable(button,controls)
                        assertTrue(button.isEnabled);assertTrue(button.isClickable)
                        assertEquals(button.text.toString(),button.createAccessibilityNodeInfo().text.toString())
                        rectangles.put(JSONObject().put("tag",name).put("width",button.width).put("height",button.height)
                            .put("text",button.text.toString()))
                    }
                    val search=root.findViewWithTag<EditText>("gallery_search")
                    val label=activity.getString(R.string.ui_search34)
                    assertNull("Use a hint/labelFor, never a fixed description on the editable query",search.contentDescription)
                    if(VerticalText.uiVertical()) {
                        val caption=root.findViewWithTag<TextView>("gallery_search_label")
                        assertEquals(search.id,caption.labelFor);assertEquals(label,caption.text.toString())
                        assertEveryPartReachable(caption,controls)
                    } else assertEquals(label,search.hint.toString())
                    assertTrue(search.requestFocus())
                    assertEveryPartReachable(search,controls)
                    assertTrue(search.createAccessibilityNodeInfo().isEditable)
                    search.setText("map & नदी 山")
                    layout(root)
                    assertEquals("map & नदी 山",search.text.toString())
                    assertEquals("Accessibility must expose the edited query",search.text.toString(),search.createAccessibilityNodeInfo().text.toString())
                    search.setText("another नदी 山")
                    assertEquals("Accessibility must update after a second edit",search.text.toString(),search.createAccessibilityNodeInfo().text.toString())
                    search.setText("map & नदी 山")
                    assertTrue(root.findViewWithTag<View>("gallery_search_go").performClick())
                    assertEquals("map & नदी 山 incategory:\"Blank maps\"",Uri.parse(web.url).getQueryParameter("search"))
                    search.onEditorAction(android.view.inputmethod.EditorInfo.IME_ACTION_SEARCH)
                    assertEquals("map & नदी 山 incategory:\"Blank maps\"",Uri.parse(web.url).getQueryParameter("search"))
                    record(root,tag,"search",rectangles)
                    if(tag=="fr" || tag=="mn-Mong") {
                        val original=Configuration(activity.resources.configuration)
                        val originalMetrics=DisplayMetrics().apply {setTo(activity.resources.displayMetrics)}
                        val rotated=Configuration(original).apply {
                            screenWidthDp=original.screenHeightDp;screenHeightDp=original.screenWidthDp
                            orientation=if(original.orientation==Configuration.ORIENTATION_LANDSCAPE)
                                Configuration.ORIENTATION_PORTRAIT else Configuration.ORIENTATION_LANDSCAPE
                        }
                        fun resizeWindow(config: Configuration,metrics: DisplayMetrics,changed: Int,phase: String) {
                            controller.configurationChange(config,metrics,changed)
                            layout(root)
                            // Preserve measured evidence of the former fixture: config/decor
                            // can change while ViewRoot still clips at the old window size.
                            recordWindow(root,tag,"$phase-config-only")
                            val orientation=if(config.orientation==Configuration.ORIENTATION_LANDSCAPE) "land" else "port"
                            ShadowDisplayManager.changeDisplay(Display.DEFAULT_DISPLAY,
                                "+w${config.screenWidthDp}dp-h${config.screenHeightDp}dp-$orientation")
                            // visible() dispatches the Display-backed frame resize and idles
                            // the paused looper. Never fabricate child sizes or visible rects.
                            controller.visible();layout(root)
                            recordWindow(root,tag,"$phase-window-resized")
                            val visible=Rect();assertTrue(root.getLocalVisibleRect(visible))
                            assertEquals("Fixture ViewRoot width must match the resized decor",root.width,visible.width())
                            assertEquals("Fixture ViewRoot height must match the resized decor",root.height,visible.height())
                            assertEquals(original.fontScale,activity.resources.configuration.fontScale,0f)
                        }
                        val rotatedMetrics=DisplayMetrics().apply {
                            setTo(originalMetrics)
                            widthPixels=(rotated.screenWidthDp*density+.5f).toInt()
                            heightPixels=(rotated.screenHeightDp*density+.5f).toInt()
                        }
                        try {
                            resizeWindow(rotated,rotatedMetrics,original.diff(rotated),"rotated")
                            assertSame("Rotation retains the active gallery",activity,controller.get())
                            assertSame("Rotation retains the browser",web,ReflectionHelpers.getField<WebView>(activity,"web"))
                            assertSame("Rotation retains the native edit buffer",search,root.findViewWithTag<EditText>("gallery_search"))
                            assertEquals("map & नदी 山",search.text.toString())
                            for(name in actions) {
                                val button=root.findViewWithTag<TextView>(name)
                                GalleryControlsLayoutTest.assertFullLayout("$tag/rotated/$name",button)
                                assertEveryPartReachable(button,controls)
                            }
                            assertEveryPartReachable(search,controls)
                        } finally {resizeWindow(original,originalMetrics,rotated.diff(original),"restored")}
                    }
                    assertTrue(root.findViewWithTag<View>("gallery_back").performClick())
                    assertTrue(root.findViewWithTag<View>("gallery_copy_credits").performClick())
                    assertTrue(root.findViewWithTag<View>("gallery_edit_credits").performClick())
                    val dialog=ShadowAlertDialog.getLatestAlertDialog()
                    assertTrue(dialog.isShowing);dialog.dismiss();shadowOf(Looper.getMainLooper()).idle()
                    assertTrue(root.findViewWithTag<View>("gallery_terms").performClick())
                    assertEquals(IllustrationSource.COMMONS.terms,shadowOf(activity).nextStartedActivity.data.toString())
                    assertTrue(root.findViewWithTag<View>("gallery_legacy_credits").performClick())
                    assertEquals(LegacyImageCreditsActivity::class.java.name,shadowOf(activity).nextStartedActivity.component!!.className)
                    if(VerticalText.uiVertical()) assertSeparateScrollGestures(root,status,controls)
                    val visible=Rect()
                    assertTrue("WebView must remain visible",web.getGlobalVisibleRect(visible))
                    assertEquals(web.height,visible.height());assertEquals(web.width,visible.width())
                    val density=activity.resources.displayMetrics.density
                    assertTrue("Controls must leave a usable browser viewport",web.height>=minOf((120*density+.5f).toInt(),(web.parent as View).height/3))
                    assertEveryPartReachable(root.findViewWithTag<View>("gallery_done"),controls)
                    assertTrue(root.findViewWithTag<View>("gallery_done").performClick());assertTrue(activity.isFinishing)
                } finally {activity.finish();controller.pause().stop().destroy()}
            }
        } finally {
            ImageCreditArchive.releaseAccepted(app,retained)
            AppLanguage.select(app,originalTag);PaintApplication.currentResources=originalResources;Locale.setDefault(originalLocale)
        }
    }

    private fun layout(root: View) {
        val metrics=root.resources.displayMetrics;val config=root.resources.configuration
        val width=(config.screenWidthDp*metrics.density+.5f).toInt();val height=(config.screenHeightDp*metrics.density+.5f).toInt()
        root.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.EXACTLY))
        root.layout(0,0,width,height)
    }

    private fun assertEveryPartReachable(view: View,controls: GalleryControlsScroll) {
        assertTrue(view.width>0 && view.height>0)
        // Request every viewport-sized slice through the real ancestor chain.
        // Oversized labels/status are accepted only when both endpoints and all
        // intermediate slices can actually be brought inside the visible clip.
        val side=(24*view.resources.displayMetrics.density+.5f).toInt()
        val xs=(0 until view.width step maxOf(side,controls.width/2)).toList()+maxOf(0,view.width-side)
        val ys=(0 until view.height step maxOf(side,controls.height/2)).toList()+maxOf(0,view.height-side)
        for(x in xs) for(y in ys) {
            val requested=Rect(x,y,minOf(view.width,x+side),minOf(view.height,y+side))
            view.requestRectangleOnScreen(Rect(requested),true)
            val visible=Rect()
            assertTrue("${view.tag} must intersect its visible ancestors",view.getLocalVisibleRect(visible))
            assertTrue("${view.tag} cannot reveal $requested; visible $visible",visible.contains(requested))
        }
        // Keep stronger simultaneous visibility whenever the viewport can hold
        // this view, rather than replacing every full-visibility assertion.
        if(view.width<=controls.width && view.height<=controls.height) {
            view.requestRectangleOnScreen(Rect(0,0,view.width,view.height),true)
            val visible=Rect();assertTrue(view.getLocalVisibleRect(visible))
            assertEquals(view.width,visible.width());assertEquals(view.height,visible.height())
        }
    }

    private fun assertSeparateScrollGestures(root: View,status: TextView,controls: GalleryControlsScroll) {
        val rail=status.parent as ColumnScrollView
        if(status.width<=rail.width) return
        controls.revealStart(rail);layout(root);rail.scrollTo(0,0)
        val shown=Rect();assertTrue(rail.getGlobalVisibleRect(shown))
        val origin=IntArray(2);controls.getLocationOnScreen(origin)
        val x=(shown.left+shown.width()*.75f)-origin[0]
        val y=(shown.top+shown.height()*.5f)-origin[1]
        fun drag(dx: Float,dy: Float) {
            val now=SystemClock.uptimeMillis()
            for((i,action) in listOf(MotionEvent.ACTION_DOWN,MotionEvent.ACTION_MOVE,MotionEvent.ACTION_MOVE,MotionEvent.ACTION_CANCEL).withIndex()) {
                val fraction=if(i==0) 0f else if(i==1) .5f else 1f
                val event=MotionEvent.obtain(now,now+i*30,action,x+dx*fraction,y+dy*fraction,0)
                try {controls.dispatchTouchEvent(event)} finally {event.recycle()}
            }
        }
        val oldY=controls.scrollY
        drag(-minOf(160f,shown.width()*.5f),0f)
        assertTrue("Horizontal drag must move the column rail",rail.scrollX>0)
        assertEquals("Horizontal drag must not steal the parent vertical scroll",oldY,controls.scrollY)
        val oldX=rail.scrollX
        drag(0f,-minOf(120f,shown.height()*.4f))
        assertTrue("Vertical drag must reach the remaining controls",controls.scrollY>oldY)
        assertEquals("Vertical drag must not move columns sideways",oldX,rail.scrollX)
    }

    private fun windowGeometry(root: View): JSONObject {
        val window=Rect();root.getWindowVisibleDisplayFrame(window)
        val display=Rect();root.display.getRectSize(display)
        val viewRoot=ReflectionHelpers.callInstanceMethod<Any>(root,"getViewRootImpl")
        val views=JSONArray()
        for(name in listOf("gallery_controls_scroll","gallery_description","gallery_status","gallery_actions","gallery_navigation",
            "gallery_copy_credits","gallery_edit_credits","gallery_terms","gallery_done","gallery_legacy_credits",
            "gallery_back","gallery_search_go","gallery_search")) {
            val view=root.findViewWithTag<View>(name) ?: continue
            val visible=Rect();val intersects=view.getLocalVisibleRect(visible)
            val node=view.createAccessibilityNodeInfo()
            try {views.put(JSONObject().put("tag",name).put("attached",view.isAttachedToWindow)
                .put("left",view.left).put("top",view.top).put("width",view.width).put("height",view.height)
                .put("scroll_x",view.scrollX).put("scroll_y",view.scrollY)
                .put("intersects",intersects).put("visible",visible.toString())
                .put("node_class",node.className?.toString() ?: JSONObject.NULL)
                .put("node_text",node.text?.toString() ?: JSONObject.NULL)
                .put("node_description",node.contentDescription?.toString() ?: JSONObject.NULL)
                .put("node_editable",node.isEditable)
                .put("native_line_count",(view as? TextView)?.layout?.lineCount ?: JSONObject.NULL))
            } finally {node.recycle()}
        }
        return JSONObject().put("decor_width",root.width).put("decor_height",root.height)
            .put("view_root_width",ReflectionHelpers.getField<Int>(viewRoot,"mWidth"))
            .put("view_root_height",ReflectionHelpers.getField<Int>(viewRoot,"mHeight"))
            .put("display",display.toString()).put("window",window.toString()).put("views",views)
    }

    private fun recordWindow(root: View,tag: String,phase: String) {
        val config=root.resources.configuration
        val stem="api${RuntimeEnvironment.getApiLevel()}-$tag-font${config.fontScale}-${config.screenWidthDp}x${config.screenHeightDp}-$phase"
        val folder=File("build/reports/gallery-controls").apply {mkdirs()}
        File(folder,"$stem.json").writeText(windowGeometry(root).toString(2)+"\n")
    }

    private fun record(root: View,tag: String,phase: String,buttons: JSONArray=JSONArray()) {
        val config=root.resources.configuration
        val stem="api${RuntimeEnvironment.getApiLevel()}-$tag-font${config.fontScale}-${config.screenWidthDp}x${config.screenHeightDp}-$phase"
        val folder=File("build/reports/gallery-controls").apply {mkdirs()}
        val image=Bitmap.createBitmap(root.width,root.height,Bitmap.Config.ARGB_8888)
        try {root.draw(Canvas(image));File(folder,"$stem.png").outputStream().use {assertTrue(image.compress(Bitmap.CompressFormat.PNG,100,it))}}
        finally {image.recycle()}
        File(folder,"$stem.json").writeText(JSONObject().put("evidence_kind","Robolectric NATIVE host rendering, not an installed-device capture")
            .put("window_geometry",windowGeometry(root)).put("locale",tag).put("font_scale",config.fontScale).put("width",root.width).put("height",root.height).put("buttons",buttons).toString(2)+"\n")
    }
}
