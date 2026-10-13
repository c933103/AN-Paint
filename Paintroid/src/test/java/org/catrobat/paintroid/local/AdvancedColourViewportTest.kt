/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.graphics.Color
import android.graphics.Rect
import android.os.Looper
import android.view.View
import android.widget.FrameLayout
import android.widget.GridLayout
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RuntimeEnvironment
import org.robolectric.RobolectricTestRunner
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.util.Locale

/** Native-rendered JVM layout checks; installed pointer/state evidence is separate. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w640dp-h320dp-land-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class AdvancedColourViewportTest {
    private fun idle()=shadowOf(Looper.getMainLooper()).idle()
    private fun withPicker(tag: String="en-US",processTag: String?=null,block: (AlertDialog)->Unit) {
        val context=RuntimeEnvironment.getApplication() as Context
        val oldLocale=Locale.getDefault();val oldTag=AppLanguage.selectedTag(context)
        val oldResources=PaintApplication.currentResources
        AppLanguage.select(context,tag)
        val controller=Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        controller.setup().visible().windowFocusChanged(true)
        val activity=controller.get();AppLanguage.refresh(activity)
        // The dialog must follow its rendering resources even when framework
        // configuration dispatch has reset the unrelated process default.
        processTag?.let {Locale.setDefault(Locale.forLanguageTag(it))}
        val dialog=AdvancedColourDialog(activity,Color.RED,false,initialMode=1) {}.show()
        try {idle();block(dialog)} finally {
            dialog.dismiss();idle();controller.pause().stop().destroy()
            AppLanguage.select(context,oldTag);Locale.setDefault(oldLocale);PaintApplication.currentResources=oldResources
        }
    }
    private fun complete(view: View) {
        val local=Rect()
        assertTrue("Positive size: ${view.tag}",view.width>0 && view.height>0)
        assertTrue("Visible: ${view.tag}",view.getLocalVisibleRect(local))
        assertEquals("All ancestors retain complete bounds: ${view.tag}",Rect(0,0,view.width,view.height),local)
    }
    private val tabTags=listOf("colour_mode_0","colour_mode_3","colour_advanced_tab","colour_mode_1","colour_mode_2")
    private fun caption(view: TextView) {
        val layout=checkNotNull(view.layout)
        assertTrue(layout.lineCount>0)
        val transformed=view.transformationMethod?.getTransformation(view.text,view) ?: view.text
        assertEquals(transformed.length,layout.getLineEnd(layout.lineCount-1))
        assertTrue(layout.height<=view.height-view.totalPaddingTop-view.totalPaddingBottom)
        for(line in 0 until layout.lineCount) {
            assertEquals(0,layout.getEllipsisCount(line))
            assertTrue(layout.getLineLeft(line)>=-.5f && layout.getLineRight(line)<=layout.width+.5f)
        }
    }
    @Test fun wideShortLandscapeKeepsEditorAndFixedControlsInsideAllAncestors() {
      for(tag in listOf("en-US","hu")) withPicker(tag) {dialog ->
        val root=dialog.window!!.decorView
        val inner=root.findViewWithTag<ScrollView>("colour_editor_scroll")
        complete(inner)
        assertTrue("Editor content must overflow",inner.getChildAt(0).height>inner.height)
        for(tag in listOf("colour_advanced_tab","custom_colours_panel","add_custom_colour")) {
            val view=root.findViewWithTag<View>(tag);complete(view)
            if(view is TextView) caption(view)
        }
        tabTags.forEach {complete(root.findViewWithTag(it));caption(root.findViewWithTag(it))}
        complete(dialog.getButton(AlertDialog.BUTTON_NEGATIVE))
      }
    }
    @Test @Config(fontScale=2f,qualifiers="w640dp-h320dp-land-xhdpi")
    fun largeShortLandscapeKeepsNaturalCaptionsAndReachablePreviewRail() {
      for(tag in listOf("en-US","hu")) withPicker(tag) {dialog ->
        val root=dialog.window!!.decorView
        val editor=root.findViewWithTag<ScrollView>("colour_editor_scroll")
        val controls=root.findViewWithTag<ScrollView>("colour_controls_scroll")
        val add=root.findViewWithTag<TextView>("add_custom_colour")
        val selected=root.findViewWithTag<TextView>("selected_colour_caption")
        val sample=root.findViewWithTag<View>("new_colour_preview")
        assertEquals(2f,add.resources.configuration.fontScale,0f)
        assertEquals(android.util.TypedValue.applyDimension(android.util.TypedValue.COMPLEX_UNIT_SP,
            12f,add.resources.displayMetrics),add.textSize,0f)
        caption(add);caption(selected)
        complete(editor);complete(controls)
        assertTrue(editor.getChildAt(0).height>editor.height)
        val density=add.resources.displayMetrics.density
        assertTrue(add.height>=48*density)
        assertEquals((64*density+.5f).toInt(),sample.width)
        assertEquals((24*density+.5f).toInt(),sample.height)
        val overflowing=controls.getChildAt(0).height>controls.height
        if(tag=="hu") assertTrue("The long caption exercises the scrolling rail",overflowing)
        val editorOffset=editor.scrollY
        // fullScroll otherwise animates after this assertion's looper turn.
        // Installed coverage below uses real gestures; this is a layout model.
        controls.isSmoothScrollingEnabled=false
        controls.fullScroll(View.FOCUS_DOWN);idle()
        if(overflowing) assertTrue(controls.scrollY>0)
        complete(add);complete(selected);complete(sample)
        assertEquals("Preview scrolling is independent of the colour editor",editorOffset,editor.scrollY)
        controls.fullScroll(View.FOCUS_UP);idle()
        assertEquals(0,controls.scrollY)
        complete(root.findViewWithTag("custom_colour_selection"))
        complete(root.findViewWithTag("custom_colour_0"))
        complete(dialog.getButton(AlertDialog.BUTTON_NEGATIVE))
      }
    }

    @Test @Config(fontScale=2f,qualifiers="w640dp-h320dp-land-mdpi")
    fun largePreviewRailReflowsWithinTheInstalledShortViewport() {
      for(tag in listOf("en-US","hu")) withPicker(tag) {dialog ->
        val root=dialog.window!!.decorView
        val holder=root.findViewWithTag<FrameLayout>("colour_dialog_holder")
        // API35's retained native failure has a 104px Hungarian rail. Reproduce
        // that parent constraint, including the shell's 8dp vertical padding,
        // instead of relying on Robolectric's taller dialog title/footer model.
        val density=holder.resources.displayMetrics.density
        val height=(112*density+.5f).toInt()
        holder.measure(View.MeasureSpec.makeMeasureSpec(holder.width,View.MeasureSpec.EXACTLY),
            View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.EXACTLY))
        holder.layout(holder.left,holder.top,holder.right,holder.top+height)
        val controls=root.findViewWithTag<ScrollView>("colour_controls_scroll")
        val editor=root.findViewWithTag<ScrollView>("colour_editor_scroll")
        assertTrue("Only the overflowing preview rail needs more width",controls.width>220*density)
        assertTrue("At least half the columns remain for editing",editor.width>=controls.width)
        assertTrue("The editor still has a finite viewport",editor.height>0)
        assertEquals((104*density+.5f).toInt(),controls.height)
        controls.scrollTo(0,controls.getChildAt(0).height)
        for(name in listOf("add_custom_colour","selected_colour_caption")) {
            val view=root.findViewWithTag<TextView>(name);caption(view);complete(view)
        }
        complete(root.findViewWithTag("new_colour_preview"))
      }
    }

    @Test @Config(qualifiers="w320dp-h640dp-port-mdpi")
    fun portraitKeepsAllSixteenSavedSlotsAtFiniteWidths() {
      for(tag in listOf("en-US","hu")) withPicker(tag) {dialog ->
        val root=dialog.window!!.decorView
        val slots=(0 until 16).map {root.findViewWithTag<View>("custom_colour_$it")}
        assertEquals(16,slots.toSet().size)
        assertEquals(8,(slots.first().parent as GridLayout).columnCount)
        slots.forEach {complete(it);assertTrue(it.contentDescription.isNotBlank())}
        complete(root.findViewWithTag("add_custom_colour"));caption(root.findViewWithTag("add_custom_colour"))
        tabTags.forEach {complete(root.findViewWithTag(it));caption(root.findViewWithTag(it))}
      }
    }
    @Test @Config(qualifiers="w412dp-h900dp-port-mdpi")
    fun verticalScriptRetainsItsSeparateFormAndSixteenFiniteSavedSlots()=withPicker("mnc-Mong") {dialog ->
        val root=dialog.window!!.decorView
        assertNotNull(root.findViewWithTag<View>("vertical_colour_form"))
        val slots=(0 until 16).map {root.findViewWithTag<View>("custom_colour_$it")}
        assertEquals(16,slots.toSet().size)
        assertEquals(8,(slots.first().parent as GridLayout).columnCount)
        slots.forEach {assertTrue(it.width>0 && it.height>0);assertTrue(it.contentDescription.isNotBlank())}
    }

    @Test fun horizontalColumnsAndWindowResizeFollowResourcesDespiteVerticalProcessDefault() {
      for(processTag in listOf("lzh-Hant","mnc-Mong")) withPicker("en-US",processTag) {dialog ->
        val root=dialog.window!!.decorView
        val holder=root.findViewWithTag<FrameLayout>("colour_dialog_holder")
        assertFalse(VerticalText.uiVertical(holder.context))
        assertEquals(processTag,Locale.getDefault().toLanguageTag())
        assertNull(root.findViewWithTag<View>("vertical_colour_form"))
        assertEquals(LinearLayout.HORIZONTAL,(holder.getChildAt(0) as LinearLayout).orientation)
        val visible=Rect();root.getWindowVisibleDisplayFrame(visible)
        val maximum=(holder.resources.displayMetrics.density*900+.5f).toInt()
        assertEquals("The horizontal resize listener follows the same resource context",
            minOf(visible.width(),maximum),dialog.window!!.attributes.width)
        complete(root.findViewWithTag("colour_editor_scroll"))
        complete(root.findViewWithTag("add_custom_colour"))
        // A later default reset cannot turn the already attached editor sideways.
        Locale.setDefault(Locale.forLanguageTag(if(processTag=="lzh-Hant") "mnc-Mong" else "lzh-Hant"))
        root.requestLayout();idle()
        assertEquals(LinearLayout.HORIZONTAL,(holder.getChildAt(0) as LinearLayout).orientation)
        assertEquals(minOf(visible.width(),maximum),dialog.window!!.attributes.width)
      }
    }

    @Test @Config(qualifiers="w412dp-h900dp-port-mdpi")
    fun verticalColourFormFollowsResourcesDespiteHorizontalProcessDefault() {
      for(tag in listOf("mnc-Mong","lzh-Hant","en-XV","qaa-Zsye-XV")) withPicker(tag,"en-US") {dialog ->
        val root=dialog.window!!.decorView
        val form=root.findViewWithTag<View>("vertical_colour_form")
        assertNotNull(form)
        assertTrue(VerticalText.uiVertical(form.context))
        assertEquals("en-US",Locale.getDefault().toLanguageTag())
        assertNotNull(root.findViewWithTag<View>("vertical_dialog_columns"))
        assertTrue(form.width>0 && form.height>0)
        val slots=(0 until 16).map {root.findViewWithTag<View>("custom_colour_$it")}
        assertEquals(16,slots.toSet().size)
        slots.forEach {assertTrue(it.width>0 && it.height>0)}
      }
    }
}
