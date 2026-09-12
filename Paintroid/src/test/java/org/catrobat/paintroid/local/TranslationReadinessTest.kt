/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.content.Context
import android.os.Looper
import android.view.View
import android.widget.EditText
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.NumericSlider
import org.catrobat.paintroid.classic.PaintTool
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.shadows.ShadowPopupMenu
import java.util.concurrent.TimeUnit

/** These use fallback English text in an RTL locale; they do not supply a translation. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="ar-rEG-w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class TranslationReadinessTest {
    private fun withEditor(check: (ClassicPaintActivity) -> Unit) {
        val context=RuntimeEnvironment.getApplication() as Context
        context.filesDir.listFiles()?.filter { it.name.startsWith("classic-") }?.forEach { it.delete() }
        context.getSharedPreferences("classic-ui",0).edit().clear().commit()
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        val activity=controller.get()
        try {
            shadowOf(Looper.getMainLooper()).idleFor(50,TimeUnit.MILLISECONDS)
            check(activity)
        } finally {
            controller.pause().stop()
            val until=System.nanoTime()+10_000_000_000
            while(activity.busy && System.nanoTime()<until) {
                shadowOf(Looper.getMainLooper()).idle();Thread.sleep(10)
            }
            controller.destroy()
        }
    }

    @Test fun numericEntryAcceptsArabicDigitsAndKeepsLocalizedValueLabel() = withEditor { activity ->
        var value=0
        val control=NumericSlider(activity,activity.getString(R.string.ui_size_px),1,1,100) { value=it }
        control.number.performClick()
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        dialog.window!!.decorView.findViewWithTag<EditText>("numeric_input").setText("٩٩")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertFalse(dialog.isShowing)
        assertEquals(99,value)
        assertEquals(activity.getString(R.string.ui_numeric_slider_value,control.name,99),control.number.text.toString())
    }

    @Test fun rtlLocaleKeepsSidebarArrowAndPaletteAttachedInPortrait() = withEditor { activity ->
        checkPanelGeometry(activity)
        val root=activity.window.decorView
        root.findViewWithTag<View>("tool_WATERCOLOR").performClick()
        assertEquals(PaintTool.WATERCOLOR,activity.paintCanvas.tool)
        assertEquals("WATERCOLOR",activity.paintCanvas.tool.name)
        root.findViewWithTag<View>("sidebar_toggle").performClick()
        assertEquals(View.GONE,root.findViewWithTag<View>("sidebar").visibility)
        root.findViewWithTag<View>("sidebar_toggle").performClick()
        shadowOf(Looper.getMainLooper()).idleFor(50,TimeUnit.MILLISECONDS)
        checkPanelGeometry(activity)
    }

    @Test
    @Config(qualifiers="ar-rEG-w900dp-h412dp-land-xhdpi")
    fun rtlLandscapeMenuKeepsSubmenusAndRunsCommandsByStableIdentity() = withEditor { activity ->
        checkPanelGeometry(activity)
        val root=activity.window.decorView
        root.findViewWithTag<View>("compact_menu").performClick()
        val popup=ShadowPopupMenu.getLatestPopupMenu()
        assertNotNull(popup)
        val menu=popup.menu
        assertEquals(6,menu.size())
        for(index in 0 until menu.size()) assertTrue(menu.getItem(index).hasSubMenu())
        val viewMenu=menu.getItem(2).subMenu!!
        val fit=(0 until viewMenu.size()).map {viewMenu.getItem(it)}.single {it.title.toString()==activity.getString(R.string.ui_fit_image)}
        activity.paintCanvas.zoomAt(3f)
        assertTrue(viewMenu.performIdentifierAction(fit.itemId,0))
        val board=activity.paintCanvas
        val inset=20f*activity.resources.displayMetrics.density
        val centre=board.toScreen(activity.document.bitmap.width/2f,activity.document.bitmap.height/2f)
        assertEquals((board.width-inset)/2f,centre.x,.1f)
        assertEquals((board.height-inset)/2f,centre.y,.1f)
    }

    private fun checkPanelGeometry(activity: ClassicPaintActivity) {
        val root=activity.window.decorView
        val sidebar=root.findViewWithTag<View>("sidebar")
        val arrow=root.findViewWithTag<View>("sidebar_toggle")
        val canvas=root.findViewWithTag<View>("canvas_and_palette")
        val palette=root.findViewWithTag<View>("palette_bar")
        val indicator=root.findViewWithTag<View>("colour_status")
        fun location(view: View)=IntArray(2).also {view.getLocationOnScreen(it)}
        assertEquals(location(sidebar)[0],location(arrow)[0])
        assertTrue(location(canvas)[0]>=location(sidebar)[0]+sidebar.width)
        assertEquals(location(indicator)[1],location(palette)[1])
        assertTrue(location(palette)[0]>=location(indicator)[0]+indicator.width)
    }
}
