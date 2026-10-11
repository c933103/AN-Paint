/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Rect
import android.os.Looper
import android.os.SystemClock
import android.view.MotionEvent
import android.view.View
import android.widget.EditText
import android.widget.ScrollView
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
import java.io.File
import java.time.Duration
import java.util.Locale

/** Identical baseline/candidate diagnostic. A successful capture is NOT a fit pass.
 * Negative geometry and unhandled/unreachable pointer attempts are retained as data.
 * The separate strict LocalizedDialogLayoutTest remains the candidate acceptance gate. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w640dp-h320dp-land-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class AdvancedColourLayoutDiagnosticTest {
    private fun idle()=shadowOf(Looper.getMainLooper()).idle()
    private fun bounds(view: View): JSONObject {
        val rect=Rect();val visible=view.getLocalVisibleRect(rect)
        val location=IntArray(2);view.getLocationOnScreen(location)
        val result=JSONObject().put("tag",view.tag).put("width",view.width).put("height",view.height)
            .put("screen_x",location[0]).put("screen_y",location[1])
            .put("visible",visible).put("visible_local",rect.toShortString())
            .put("whole_view_visible",visible && rect==Rect(0,0,view.width,view.height))
        if(view is TextView) {
            result.put("text",view.text.toString())
            val layout=view.layout
            if(layout!=null && layout.lineCount>0) {
                val transformed=view.transformationMethod?.getTransformation(view.text,view)?.toString() ?: view.text.toString()
                result.put("layout_height",layout.height).put("line_count",layout.lineCount)
                val fit=layout.getLineEnd(layout.lineCount-1)==transformed.length &&
                    layout.height<=view.height-view.totalPaddingTop-view.totalPaddingBottom &&
                    (0 until layout.lineCount).all {layout.getEllipsisCount(it)==0 && layout.getLineLeft(it)>=-1 && layout.getLineRight(it)<=layout.width+1}
                result.put("intrinsic_text_fit",fit)
                result.put("all_text_lines_visible",fit && visible &&
                    (0 until layout.lineCount).all {line->rect.contains(Rect(view.totalPaddingLeft,view.totalPaddingTop+layout.getLineTop(line),view.width-view.totalPaddingRight,view.totalPaddingTop+layout.getLineBottom(line)))})
            }
        }
        return result
    }
    private fun scrollAncestors(view: View): JSONArray {
        val rows=JSONArray();var current: View?=view
        while(current!=null) {rows.put(JSONObject().put("class",current.javaClass.name).put("tag",current.tag)
            .put("scroll_y",current.scrollY).put("height",current.height));current=current.parent as? View}
        return rows
    }
    private fun pointer(root: View,view: View,swipe: Boolean): JSONObject {
        val visible=Rect()
        val result=JSONObject().put("before",bounds(view)).put("ancestors_before",scrollAncestors(view))
        if(!view.getLocalVisibleRect(visible) || visible.width()<2 || visible.height()<2) return result.put("attempted",false).put("reason","No visible pointer target")
        val location=IntArray(2);val origin=IntArray(2);view.getLocationOnScreen(location);root.getLocationOnScreen(origin)
        val x=(location[0]-origin[0]+visible.centerX()).toFloat()
        val first=location[1]-origin[1]+visible.top+visible.height()*(if(swipe) .85f else .5f)
        val last=if(swipe) location[1]-origin[1]+visible.top+visible.height()*.15f else first
        val time=SystemClock.uptimeMillis();val steps=if(swipe) 10 else 1;val handled=JSONArray()
        for(step in 0..steps) {
            val action=when(step) {0->MotionEvent.ACTION_DOWN;steps->MotionEvent.ACTION_UP;else->MotionEvent.ACTION_MOVE}
            val event=MotionEvent.obtain(time,time+step*20L,action,x,first+(last-first)*step/steps,0)
            try {handled.put(root.dispatchTouchEvent(event))} finally {event.recycle()}
        }
        shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(250))
        return result.put("attempted",true).put("event_handled",handled).put("after",bounds(view)).put("ancestors_after",scrollAncestors(view))
    }
    private fun runDiagnostic() {
        val app=RuntimeEnvironment.getApplication() as Context
        val oldLocale=Locale.getDefault();val oldTag=AppLanguage.selectedTag(app);val oldResources=PaintApplication.currentResources
        try {
            for(tag in listOf("en-US","hu")) {
                AppLanguage.select(app,tag)
                val controller=Robolectric.buildActivity(Activity::class.java);controller.get().setTheme(R.style.ClassicPaintTheme)
                controller.setup().visible().windowFocusChanged(true)
                val activity=controller.get();AppLanguage.refresh(activity)
                var commits=0;var closed=0
                val dialog=AdvancedColourDialog(activity,Color.RED,false,closed={closed++},initialMode=1) {commits++}.show();idle()
                try {
                    val root=dialog.window!!.decorView
                    val holder=root.findViewWithTag<View>("colour_dialog_holder");val inner=root.findViewWithTag<ScrollView>("colour_editor_scroll")
                    val field=root.findViewWithTag<EditText>("colour_hex")
                    val controls=listOf("colour_advanced_tab","custom_colours_panel","add_custom_colour").map {root.findViewWithTag<View>(it)} +
                        listOf(dialog.getButton(AlertDialog.BUTTON_NEGATIVE),dialog.getButton(AlertDialog.BUTTON_POSITIVE),field)
                    assertTrue(root.width>0 && root.height>0)
                    val report=JSONObject().put("diagnostic_only",true).put("fit_acceptance",false)
                        .put("evidence_kind","Robolectric NATIVE, actual production AdvancedColourDialog; not physical-device acceptance")
                        .put("sdk",RuntimeEnvironment.getApiLevel()).put("locale",tag).put("font_scale",activity.resources.configuration.fontScale)
                        .put("window_width",root.width).put("window_height",root.height).put("holder",bounds(holder))
                        .put("initial_controls",JSONArray(controls.map {bounds(it)})).put("inner_initial",bounds(inner))
                    val directory=File("build/reports/advanced-colour-diagnostic").apply {mkdirs()}
                    val name="api${RuntimeEnvironment.getApiLevel()}-$tag-font${activity.resources.configuration.fontScale}"
                    fun capture(phase: String) {
                        val bitmap=Bitmap.createBitmap(root.width,root.height,Bitmap.Config.ARGB_8888)
                        try {root.draw(Canvas(bitmap));File(directory,"$name-$phase.png").outputStream().use {assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))}} finally {bitmap.recycle()}
                    }
                    capture("initial")
                    report.put("inner_pointer_swipe",pointer(root,inner,true));capture("after-swipe")
                    val requested=Rect(0,0,field.width,field.height);field.requestRectangleOnScreen(Rect(requested),true);idle()
                    report.put("field_reveal",bounds(field)).put("field_pointer",pointer(root,field,false)).put("field_focused_after_pointer",field.hasFocus())
                    capture("after-field-pointer")
                    val cancel=dialog.getButton(AlertDialog.BUTTON_NEGATIVE)
                    cancel.requestRectangleOnScreen(Rect(0,0,cancel.width,cancel.height),true);idle()
                    report.put("cancel_pointer",pointer(root,cancel,false)).put("dialog_showing_after_cancel",dialog.isShowing)
                        .put("commit_callbacks",commits).put("closed_callbacks",closed)
                    File(directory,"$name.json").writeText(report.toString(2)+"\n")
                } finally {dialog.dismiss();controller.pause().stop().destroy();idle()}
            }
        } finally {AppLanguage.select(app,oldTag);PaintApplication.currentResources=oldResources;Locale.setDefault(oldLocale)}
    }
    @Test @Config(fontScale=1f) fun recordNormalShortLandscapeWithoutClaimingAcceptance()=runDiagnostic()
    @Test @Config(fontScale=2f) fun recordLargeShortLandscapeWithoutClaimingAcceptance()=runDiagnostic()
}
