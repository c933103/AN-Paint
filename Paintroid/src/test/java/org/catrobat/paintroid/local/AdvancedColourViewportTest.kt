/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.graphics.Color
import android.graphics.Rect
import android.os.Looper
import android.view.View
import android.widget.GridLayout
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
    private fun withPicker(tag: String="en-US",block: (AlertDialog)->Unit) {
        val context=RuntimeEnvironment.getApplication() as Context
        val oldLocale=Locale.getDefault();val oldTag=AppLanguage.selectedTag(context)
        val oldResources=PaintApplication.currentResources
        AppLanguage.select(context,tag)
        val controller=Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        controller.setup().visible().windowFocusChanged(true)
        val activity=controller.get();AppLanguage.refresh(activity)
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
}
