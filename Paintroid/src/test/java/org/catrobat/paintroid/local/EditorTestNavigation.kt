/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.Spinner
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.ImageFormat
import org.junit.Assert.*
import org.robolectric.Shadows.shadowOf
import org.robolectric.shadows.ShadowAlertDialog

/** Interacts with real tabs and controls; no popup-menu shadows or private action calls. */
internal object EditorTestNavigation {
    fun idle()=shadowOf(Looper.getMainLooper()).idle()
    fun buttons(view: View): List<Button> = if(view is Button) listOf(view) else if(view is ViewGroup)
        (0 until view.childCount).flatMap {buttons(view.getChildAt(it))} else emptyList()
    fun click(activity: ClassicPaintActivity,tag: String) {
        val root=activity.window.decorView
        val actual=when(tag) {"trim_canvas"->"command_Edit_1";"select_all"->"command_Edit_0";else->tag}
        val tab=when {actual.startsWith("command_")->actual.split('_')[1]
            actual.startsWith("colour_") || actual in listOf("foreground_colour","background_colour","swap_colours","reset_colours")->"Color"
            actual=="tool_ZOOM"->"View"
            actual.startsWith("tool_") || actual.startsWith("category_")->"Draw";else->null}
        if(tab!=null) {root.findViewWithTag<View>("menu_$tab").performClick();idle()}
        val view=root.findViewWithTag<View>(actual)
        assertNotNull("Missing control $actual",view)
        if(view is android.widget.CompoundButton) {val checked=view.isChecked;view.performClick();assertNotEquals(checked,view.isChecked)}
        else assertTrue("Click $actual",view.performClick())
        idle()
    }
    fun command(activity: ClassicPaintActivity,tab: String,index: Int)=click(activity,"command_${tab}_$index")
    fun named(activity: ClassicPaintActivity,tab: String,label: String) {
        click(activity,"menu_$tab")
        val button=buttons(activity.window.decorView.findViewWithTag("panel_${tab}_commands")).single {it.text.toString()==label}
        assertTrue(button.performClick());idle()
    }
    fun format(spinner: Spinner,format: ImageFormat) {
        val index=(0 until spinner.count).single {spinner.getItemAtPosition(it).toString()==format.label}
        spinner.setSelection(index);idle()
    }
    fun chooseLocationIfShown() {
        val dialog=ShadowAlertDialog.getLatestAlertDialog() ?: return
        if(dialog.isShowing && dialog.window!!.decorView.findViewWithTag<View>("export_format")!=null) {
            assertTrue(dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick());idle()
        }
    }
}
