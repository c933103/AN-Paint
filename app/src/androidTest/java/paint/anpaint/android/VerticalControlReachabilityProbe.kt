/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.Instrumentation
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Point
import android.graphics.Rect
import android.os.SystemClock
import android.view.View
import android.widget.EditText
import android.widget.HorizontalScrollView
import android.widget.ScrollView
import android.widget.Spinner
import androidx.test.uiautomator.UiDevice
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.NumericSlider
import org.junit.Assert.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicReference

/** Additional real-input assertions, separate from the accepted capture-state matrix.
 * No production listeners, progress values, scroll offsets or dialog callbacks are replaced.
 * Read-only view/model observations supply coordinates and verify native input effects.
 */
internal class VerticalControlReachabilityProbe(
    private val instrumentation: Instrumentation,
    private val activity: ()->ClassicPaintActivity,
    private val saveRoot: ()->View,
    private val name: String
) {
    private val device=UiDevice.getInstance(instrumentation)
    private val context get()=instrumentation.targetContext
    private val directory=File(context.getExternalFilesDir(null),"vertical-locale-evidence/reachability")
    private val observations=JSONArray()
    private val screenshots=JSONArray()
    private val receipt=JSONObject().put("case",name).put("success",false)
        .put("device_sdk",android.os.Build.VERSION.SDK_INT)
        .put("observations",observations).put("screenshots",screenshots)
    private val documentNameField=ClassicPaintActivity::class.java.getDeclaredField("filename").apply {isAccessible=true}
    private val draftName=onMain {saveRoot().findViewWithTag<EditText>("export_filename").text.toString()}
    private val documentName=onMain {documentNameField.get(activity()) as String}
    private val canvas: Bitmap=onMain {activity().document.bitmap.copy(Bitmap.Config.ARGB_8888,false)}
    private val tool=onMain {activity().paintCanvas.tool}
    private val rememberedQuality=context.getSharedPreferences("export",0).getInt("quality",95)
    private var nativeSwipes=0
    private var cancelledDraftQuality=0

    init {
        assertFailedVisibilityIsEmpty()
        assertTrue("Reachability evidence directory",directory.isDirectory || directory.mkdirs())
        receipt.put("filename",draftName).put("remembered_quality_before_cancel",rememberedQuality)
        writeReceipt()
    }

    fun exerciseBothEndpointsAndCancelRoute() {
        try {
            snapshot("before")
            revealComplete("quality label and readout") {quality().number}
            revealComplete("complete quality control") {quality()}
            assertQualityGeometry()
            // Each target differs from the preceding value, including a persisted
            // endpoint from the first orientation. A missed gesture cannot pass.
            val endpoints=if(onMain {quality().slider.progress}==0) listOf(100,1) else listOf(1,100)
            for(value in endpoints) {
                dragTo(value)
                snapshot(if(value==1) "minimum" else "maximum")
            }
            revealComplete("filename field") {saveRoot().findViewWithTag<EditText>("export_filename")}
            revealComplete("filename preview") {saveRoot().findViewWithTag<View>("vertical_filename_preview")}
            assertDraft()
            snapshot("filename")
            revealComplete("JPEG explanation") {saveRoot().findViewWithTag<View>("export_description")}
            assertDraft()
            snapshot("description")
            // The previous orientation may have committed an endpoint. Never
            // let Cancel's draft equal that remembered value: such a precondition
            // could not detect an erroneous commit performed only on Cancel.
            if(onMain {quality().slider.progress+quality().minimum}==rememberedQuality)
                dragTo(if(rememberedQuality==1) 100 else 1)
            revealComplete("Cancel action") {saveRoot().findViewById<View>(android.R.id.button2)}
            cancelledDraftQuality=onMain {quality().slider.progress+quality().minimum}
            assertNotEquals("Cancel must discard a genuinely changed draft",rememberedQuality,cancelledDraftQuality)
            receipt.put("cancel_draft_quality",cancelledDraftQuality)
            snapshot("cancel-ready")
            onMain {
                assertEquals("Cancel precondition remains unchanged",cancelledDraftQuality,quality().slider.progress+quality().minimum)
                assertNotEquals("Cancel input must distinguish draft from remembered quality",rememberedQuality,cancelledDraftQuality)
            }
            receipt.put("endpoint_values",JSONArray().put(1).put(100))
            writeReceipt()
        } catch(failure: Throwable) {recordFailure(failure);throw failure}
    }

    fun assertCancelledDraftWasNotCommitted() {
        assertTrue("Cancel observed a valid distinct draft",cancelledDraftQuality in 1..100 && cancelledDraftQuality!=rememberedQuality)
        assertEquals("Cancelled native quality is not persisted",rememberedQuality,
            context.getSharedPreferences("export",0).getInt("quality",95))
        assertCanvasAndDocument()
        receipt.put("cancel_preserved_quality",true)
        writeReceipt()
    }

    /** Called only after the original Cancel/reopen/Back/no-request assertions. */
    fun confirmViaNativeAction(value: Int,requests: List<Intent>) {
        try {
            assertTrue("Only this new Choose location action may request a destination",requests.isEmpty())
            assertDraft()
            revealComplete("confirmation quality") {quality()}
            assertQualityGeometry()
            // Establish a different endpoint with real input when necessary.
            if(onMain {quality().slider.progress+quality().minimum}==value) dragTo(if(value==1) 100 else 1)
            dragTo(value)
            revealComplete("Choose location action") {saveRoot().findViewById<View>(android.R.id.button1)}
            assertDraft()
            snapshot("choose-ready")
            val bounds=onMain {completeBounds(saveRoot().findViewById<View>(android.R.id.button1))
                ?: throw AssertionError("Choose location moved before native tap")}
            assertTrue("Native Choose location tap",device.click(bounds.centerX(),bounds.centerY()))
            instrumentation.waitForIdleSync()
            waitUntil("single intercepted destination request") {requests.size==1}
            val request=requests.single()
            assertEquals(Intent.ACTION_CREATE_DOCUMENT,request.action)
            assertEquals("image/jpeg",request.type)
            assertEquals("Native filename survives scrolling, endpoints and action",draftName,request.getStringExtra(Intent.EXTRA_TITLE))
            assertEquals("Native quality reaches the real Save callback",value,
                context.getSharedPreferences("export",0).getInt("quality",-1))
            assertCanvasAndDocument()
            // ActivityMonitor returns RESULT_CANCELED, so no actual provider,
            // file, permission grant, save encoding or external destination runs.
            snapshot("returned",dialog=false)
            receipt.put("confirmed_quality",value).put("destination_requests",1)
                .put("destination_action",request.action).put("destination_mime",request.type)
                .put("destination_filename",request.getStringExtra(Intent.EXTRA_TITLE))
                .put("canvas_and_document_preserved",true).put("native_scroll_gestures",nativeSwipes)
                .put("success",true)
            writeReceipt()
        } catch(failure: Throwable) {recordFailure(failure);throw failure}
        finally {canvas.recycle()}
    }

    private fun quality()=saveRoot().findViewWithTag<NumericSlider>("export_quality")
    private fun assertDraft()=onMain {
        assertEquals("JPEG still selected", "JPEG",saveRoot().findViewWithTag<Spinner>("export_format").selectedItem.toString())
        assertEquals("Draft filename unchanged",draftName,saveRoot().findViewWithTag<EditText>("export_filename").text.toString())
        assertCanvasAndDocument()
    }
    private fun assertCanvasAndDocument()=onMain {
        assertTrue("All canvas pixels retained",canvas.sameAs(activity().document.bitmap))
        assertEquals("Document filename retained",documentName,documentNameField.get(activity()))
        assertEquals("Selected tool retained",tool,activity().paintCanvas.tool)
        assertNull(activity().lastIoError)
    }
    private fun assertQualityGeometry()=onMain {
        val quality=quality()
        assertEquals("JPEG minimum",1,quality.minimum);assertEquals("JPEG maximum",100,quality.maximum)
        assertEquals("Native SeekBar full range",99,quality.slider.max)
        for((label,view) in listOf("quality" to quality,"readout" to quality.number,"seekbar" to quality.slider))
            assertNotNull("Complete $label must fit the current clipped viewport: ${geometry(view)}",completeBounds(view))
        val thumb=thumbBounds()
        assertTrue("The complete native thumb is inside the SeekBar viewport: $thumb",visibleBounds(quality.slider).contains(thumb))
    }
    private fun thumbBounds(): Rect {
        val slider=quality().slider
        val raw=rawBounds(slider)
        return Rect(requireNotNull(slider.thumb).bounds).apply {
            offset(raw.left+slider.paddingLeft-slider.thumbOffset,raw.top+slider.paddingTop)
        }
    }
    private fun dragTo(value: Int) {
        revealComplete("quality endpoint $value") {quality()}
        assertQualityGeometry()
        val (first,last,before)=onMain {
            val quality=quality();val slider=quality.slider;val raw=rawBounds(slider)
            val current=slider.progress+quality.minimum
            assertNotEquals("Endpoint requires a real value change",value,current)
            val minimumAtRight=slider.layoutDirection==View.LAYOUT_DIRECTION_RTL
            val right=(value==100) != minimumAtRight
            // One pixel into the padded end guarantees the exact boundary,
            // independent of AbsSeekBar's touch/thumb rounding offset.
            val x=(if(right) raw.right-slider.paddingRight+1 else raw.left+slider.paddingLeft-1)
                .coerceIn(raw.left,raw.right-1)
            val thumb=thumbBounds()
            val start=Point(thumb.centerX(),thumb.centerY())
            val end=Point(x,raw.centerY())
            assertTrue("Current thumb is a visible native touch target",visibleBounds(slider).contains(start.x,start.y))
            assertTrue("Requested endpoint is a visible native touch target",visibleBounds(slider).contains(end.x,end.y))
            Triple(start,end,current)
        }
        assertTrue("Native drag to JPEG quality $value",device.swipe(arrayOf(first,last,last,last),12))
        instrumentation.waitForIdleSync()
        waitUntil("native quality equals $value") {quality().slider.progress+quality().minimum==value}
        assertDraft();assertQualityGeometry()
        onMain {
            assertEquals("Visible numeric readout matches actual native value",
                activity().getString(R.string.ui_numeric_slider_value,quality().name,value),quality().number.text.toString())
            observations.put(JSONObject().put("kind","endpoint").put("before",before).put("value",value)
                .put("from",JSONArray().put(first.x).put(first.y)).put("to",JSONArray().put(last.x).put(last.y))
                .put("geometry",geometry(quality())).put("seekbar",geometry(quality().slider)).put("thumb",rect(thumbBounds())))
        }
        writeReceipt()
    }

    /** Full bounds, not the old center/minimum-tap-area visibility criterion. */
    private fun completeBounds(view: View): Rect? {
        if(!view.isShown || view.width<=0 || view.height<=0) return null
        val raw=rawBounds(view);val visible=visibleBounds(view)
        return raw.takeIf {visible.contains(raw)}
    }
    private fun revealComplete(label: String,target: ()->View) {
        val seen=mutableSetOf<String>()
        repeat(24) {
            instrumentation.waitForIdleSync()
            if(onMain {completeBounds(target())!=null}) {
                onMain {observations.put(JSONObject().put("kind","reachable").put("label",label).put("geometry",geometry(target())))}
                assertDraft();writeReceipt();return
            }
            val gesture=onMain {
                val view=target();val raw=rawBounds(view)
                assertTrue("Shown target $label",view.isShown)
                var parent=view.parent as? View
                var found: Triple<View,Rect,Int>?=null
                while(parent!=null && found==null) {
                    val candidate=parent;val visible=visibleBounds(candidate)
                    val horizontal=candidate is HorizontalScrollView
                    if(!visible.isEmpty && (horizontal || candidate is ScrollView)) {
                        val direction=if(horizontal) when {
                            raw.left<visible.left -> -1
                            raw.right>visible.right -> 1
                            else -> 0
                        } else when {
                            raw.top<visible.top -> -1
                            raw.bottom>visible.bottom -> 1
                            else -> 0
                        }
                        if(direction!=0 && (if(horizontal) candidate.canScrollHorizontally(direction) else candidate.canScrollVertically(direction)))
                            found=Triple(candidate,visible,direction)
                    }
                    parent=candidate.parent as? View
                }
                found ?: throw AssertionError("No native scroll route to complete $label: ${geometry(view)}")
            }
            val (scroll,bounds,direction)=gesture
            val before=onMain {"${scroll.scrollX},${scroll.scrollY},${rawBounds(target())}"}
            assertTrue("Native scrolling must not loop for $label: $before",seen.add(before))
            val horizontal=scroll is HorizontalScrollView
            val raw=onMain {rawBounds(target())}
            val hidden=if(horizontal) {
                if(direction<0) bounds.left-raw.left else raw.right-bounds.right
            } else if(direction<0) bounds.top-raw.top else raw.bottom-bounds.bottom
            val span=if(horizontal) bounds.width() else bounds.height()
            val slop=android.view.ViewConfiguration.get(context).scaledTouchSlop
            // Match the missing edge plus native touch slop. A fixed long swipe
            // can alternate across a control that actually fits the viewport.
            val distance=(hidden+slop+2).coerceIn(slop+1,span*3/5)
            val low=if(horizontal) bounds.left+bounds.width()/5 else bounds.top+bounds.height()/5
            val high=if(horizontal) bounds.right-bounds.width()/5 else bounds.bottom-bounds.height()/5
            // Use the bottom of the content viewport, away from the top-aligned
            // native SeekBar. Never use a programmatic scroll or progress setter.
            val lane=if(horizontal) bounds.bottom-maxOf(2,(4*context.resources.displayMetrics.density).toInt()) else bounds.centerX()
            val start=if(direction>0) high else low
            val end=if(direction>0) start-distance else start+distance
            val first=if(horizontal) Point(start,lane) else Point(lane,start)
            val last=if(horizontal) Point(end,lane) else Point(lane,end)
            onMain {observations.put(JSONObject().put("kind","scroll-before").put("label",label).put("geometry",geometry(target())))}
            assertTrue("Native reveal gesture $label",device.swipe(arrayOf(first,last,last,last),20))
            nativeSwipes++
            settle(target)
            onMain {observations.put(JSONObject().put("kind","scroll-after").put("label",label).put("geometry",geometry(target())))}
            assertDraft();writeReceipt()
        }
        throw AssertionError("Complete $label was not reached within the native gesture bound")
    }
    private fun settle(target: ()->View) {
        var previous="";var changedAt=SystemClock.uptimeMillis()
        waitUntil("native scroll settled") {
            val signature=geometry(target()).toString()
            if(signature!=previous || target().isLayoutRequested) {previous=signature;changedAt=SystemClock.uptimeMillis();false}
            else SystemClock.uptimeMillis()-changedAt>=150
        }
    }
    private fun snapshot(state: String,dialog: Boolean=true) {
        val root=onMain {if(dialog) saveRoot() else activity().window.decorView}
        settle {root}
        val complete=CountDownLatch(1)
        val second=Runnable {complete.countDown()}
        val first=Runnable {root.postOnAnimation(second)}
        val committed=Runnable {root.postOnAnimation(first)}
        val observer=onMain {root.viewTreeObserver.also {
            assertTrue("Screenshot window is hardware accelerated",root.isHardwareAccelerated)
            it.registerFrameCommitCallback(committed);root.invalidate()
        }}
        try {assertTrue("Reachability screenshot frame committed",complete.await(3,TimeUnit.SECONDS))}
        finally {onMain {if(observer.isAlive) observer.unregisterFrameCommitCallback(committed);root.removeCallbacks(first);root.removeCallbacks(second)}}
        val file=File(directory,"$name-$state.png")
        assertTrue("Fresh reachability screenshot",device.takeScreenshot(file));assertTrue(file.length()>0)
        screenshots.put(file.name)
        if(dialog) onMain {
            observations.put(JSONObject().put("kind","capture").put("state",state)
                .put("quality",quality().slider.progress+quality().minimum)
                .put("filename",saveRoot().findViewWithTag<EditText>("export_filename").text.toString())
                .put("geometry",geometry(quality())).put("seekbar",geometry(quality().slider))
                .put("readout",geometry(quality().number)).put("thumb",rect(thumbBounds())))
        }
        writeReceipt()
    }
    private fun geometry(view: View): JSONObject {
        val parents=JSONArray();var parent=view.parent as? View
        while(parent!=null) {
            if(parent is HorizontalScrollView || parent is ScrollView) parents.put(JSONObject()
                .put("class",parent.javaClass.name).put("scroll_x",parent.scrollX).put("scroll_y",parent.scrollY)
                .put("raw",rect(rawBounds(parent))).put("visible",rect(visibleBounds(parent))))
            parent=parent.parent as? View
        }
        return JSONObject().put("raw",rect(rawBounds(view))).put("visible",rect(visibleBounds(view)))
            .put("fully_visible",completeBounds(view)!=null).put("parents",parents)
    }
    private fun rawBounds(view: View): Rect {
        val location=IntArray(2);view.getLocationOnScreen(location)
        return Rect(location[0],location[1],location[0]+view.width,location[1]+view.height)
    }
    /** Installed negative: Android may leave nonempty output on a false result. */
    private fun assertFailedVisibilityIsEmpty()=onMain {
        var observed=false
        val fullyClipped=object: View(context) {
            override fun getGlobalVisibleRect(bounds: Rect,offset: Point?): Boolean {
                observed=true;bounds.set(10,20,110,120);return false
            }
        }
        assertTrue("False visibility cannot credit nonempty output",visibleBounds(fullyClipped).isEmpty)
        assertTrue("False/nonempty native visibility fixture was called",observed)
    }
    private fun visibleBounds(view: View): Rect {
        val bounds=Rect();if(!view.getGlobalVisibleRect(bounds)) return Rect()
        val location=IntArray(2);view.rootView.getLocationOnScreen(location)
        bounds.offset(location[0],location[1]);return bounds
    }
    private fun rect(value: Rect)=JSONArray().put(value.left).put(value.top).put(value.right).put(value.bottom)
    private fun writeReceipt() {File(directory,"$name.json").writeText(receipt.toString(2)+"\n")}
    private fun recordFailure(failure: Throwable) {
        receipt.put("failure",failure.toString());writeReceipt()
        try {device.takeScreenshot(File(directory,"$name-failure.png"))} catch(capture: Throwable) {failure.addSuppressed(capture)}
    }
    private fun waitUntil(label: String,condition: ()->Boolean) {
        val until=SystemClock.uptimeMillis()+15000
        while(SystemClock.uptimeMillis()<until) {
            if(onMain(condition)) return
            SystemClock.sleep(25)
        }
        throw AssertionError("Timed out: $label")
    }
    private fun <T> onMain(action: ()->T): T {
        if(android.os.Looper.myLooper()==android.os.Looper.getMainLooper()) return action()
        val result=AtomicReference<T>();val failure=AtomicReference<Throwable?>()
        instrumentation.runOnMainSync {try {result.set(action())} catch(error: Throwable) {failure.set(error)}}
        failure.get()?.let {throw it};return result.get()
    }
}
