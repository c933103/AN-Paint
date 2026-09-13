/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.content.Context
import android.graphics.Color
import android.os.Looper
import android.view.View
import android.widget.EditText
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.AdvancedColourDialog
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
import java.util.concurrent.TimeUnit
import java.util.Locale

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
        shadowOf(Looper.getMainLooper()).idle()
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        dialog.window!!.decorView.findViewWithTag<EditText>("numeric_input").setText("٩٩")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        shadowOf(Looper.getMainLooper()).idle()
        assertFalse(dialog.isShowing)
        assertEquals(99,value)
        assertEquals(activity.getString(R.string.ui_numeric_slider_value,control.name,99),control.number.text.toString())
    }

    @Test
    @Config(qualifiers="fr-rFR-w412dp-h900dp-port-xhdpi")
    fun colourFieldsAcceptDecimalCommaWithoutDroppingTheFraction() = withEditor { activity ->
        val oldLocale=Locale.getDefault()
        Locale.setDefault(Locale.FRANCE)
        try {
            val picker=AdvancedColourDialog(activity,Color.RED,false) {}
            val dialog=picker.show()
            shadowOf(Looper.getMainLooper()).idle()
            val root=dialog.window!!.decorView
            root.findViewWithTag<View>("colour_advanced_tab").performClick()
            val hue=root.findViewWithTag<EditText>("colour_h")
            hue.setText("120,5")
            assertEquals("120,5",hue.text.toString());assertNull(hue.error)
            assertEquals(120.5f,picker.value.hsv[0],.001f)
            val saturation=root.findViewWithTag<EditText>("colour_s")
            saturation.setText("50,5")
            assertNull(saturation.error);assertEquals(.505f,picker.value.hsv[1],.0001f)
            // Ordinary decimal-dot input remains accepted for pasted numbers.
            hue.setText("240.25")
            assertNull(hue.error);assertEquals(240.25f,picker.value.hsv[0],.001f)
            dialog.dismiss()
        } finally {Locale.setDefault(oldLocale)}
    }

    @Test fun colourFieldsAcceptArabicDigitsAndDecimalSeparatorAndRejectOutOfRange() = withEditor { activity ->
        val oldLocale=Locale.getDefault()
        Locale.setDefault(Locale("ar","EG"))
        try {
            var selected=Color.BLACK
            val picker=AdvancedColourDialog(activity,Color.RED,false) {selected=it}
            val dialog=picker.show()
            // AlertDialog delivers OnShow on the main queue; install its validated
            // positive-button handler before exercising invalid/valid submission.
            shadowOf(Looper.getMainLooper()).idle()
            val root=dialog.window!!.decorView
            root.findViewWithTag<View>("colour_advanced_tab").performClick()
            val hue=root.findViewWithTag<EditText>("colour_h")
            hue.setText("١٢٠٫٥")
            assertEquals("١٢٠٫٥",hue.text.toString());assertNull(hue.error)
            assertEquals(120.5f,picker.value.hsv[0],.001f)
            val red=root.findViewWithTag<EditText>("colour_r")
            red.setText("٢٥٦")
            assertEquals(activity.getString(R.string.ui_colour_component_range,255),red.error.toString())
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            shadowOf(Looper.getMainLooper()).idle()
            assertTrue(dialog.isShowing);assertEquals(Color.BLACK,selected)
            red.setText("١٢٨")
            assertNull(red.error);assertEquals(128,Color.red(picker.value.colour))
            assertEquals(activity.getString(R.string.ui_colour_red_range),red.contentDescription.toString())
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            shadowOf(Looper.getMainLooper()).idle()
            assertFalse(dialog.isShowing);assertEquals(picker.value.colour,selected)
        } finally {Locale.setDefault(oldLocale)}
    }

    @Test fun rtlLocaleKeepsSidebarArrowAndPaletteAttachedInPortrait() = withEditor { activity ->
        checkPanelGeometry(activity)
        val root=activity.window.decorView
        root.findViewWithTag<View>("tool_WATERCOLOR").performClick()
        assertEquals(PaintTool.WATERCOLOR,activity.paintCanvas.tool)
        assertEquals("WATERCOLOR",activity.paintCanvas.tool.name)
        root.findViewWithTag<View>("sidebar_toggle").performClick()
        assertFalse(root.findViewWithTag<View>("sidebar").isShown)
        root.findViewWithTag<View>("sidebar_toggle").performClick()
        shadowOf(Looper.getMainLooper()).idleFor(50,TimeUnit.MILLISECONDS)
        checkPanelGeometry(activity)
    }

    @Test
    @Config(qualifiers="ar-rEG-w900dp-h412dp-land-xhdpi")
    fun rtlLandscapeMenuKeepsSubmenusAndRunsCommandsByStableIdentity() = withEditor { activity ->
        checkPanelGeometry(activity)
        val root=activity.window.decorView
        assertNull(root.findViewWithTag<View>("compact_menu"))
        for(tab in listOf("Main","File","Edit","View","Color")) assertNotNull(root.findViewWithTag<View>("menu_$tab"))
        activity.paintCanvas.zoomAt(3f)
        root.findViewWithTag<View>("zoom_fit_view").performClick()
        val board=activity.paintCanvas
        val inset=20f*activity.resources.displayMetrics.density
        val centre=board.toScreen(activity.document.bitmap.width/2f,activity.document.bitmap.height/2f)
        assertEquals((board.width-inset)/2f,centre.x,.1f)
        assertEquals((board.height-inset)/2f,centre.y,.1f)
    }

    private fun checkPanelGeometry(activity: ClassicPaintActivity) {
        val root=activity.window.decorView
        val arrow=root.findViewWithTag<View>("sidebar_toggle")
        val tabs=root.findViewWithTag<View>("tabs_row")
        val canvas=activity.paintCanvas
        fun location(view: View)=IntArray(2).also {view.getLocationOnScreen(it)}
        assertEquals(location(tabs)[1],location(arrow)[1])
        assertEquals(root.width,canvas.width)
        assertTrue(location(canvas)[1]>=location(tabs)[1]+tabs.height)
        assertTrue(canvas.height>0)
        assertNotNull(root.findViewWithTag<View>("menu_Color"))
    }
}
