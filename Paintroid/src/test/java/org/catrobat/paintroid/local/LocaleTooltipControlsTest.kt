/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.LocaleManager
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.os.LocaleList
import android.os.Looper
import android.text.Spanned
import android.text.TextPaint
import android.text.style.MetricAffectingSpan
import android.view.View
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.util.ReflectionHelpers
import java.io.File
import java.util.Locale
import java.util.concurrent.TimeUnit

/** Exercises the actual editor/assembly callsites, including their existing help listeners. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[35],qualifiers="w420dp-h680dp-port-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class LocaleTooltipControlsTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private lateinit var previous: Locale
    private lateinit var resources: Resources
    private lateinit var platformLocales: LocaleList
    private lateinit var preferences: Map<String,*>
    @Before fun remember() {
        previous=Locale.getDefault();resources=PaintApplication.currentResources
        platformLocales=context.getSystemService(LocaleManager::class.java)!!.applicationLocales
        preferences=context.getSharedPreferences("app-language",0).all.toMap()
        for(name in listOf("classic-recovery.png","classic-autosave.zip","classic-autosave.zip.bak")) File(context.filesDir,name).delete()
        context.getSharedPreferences("classic-ui",0).edit().clear().commit()
    }
    @After fun restore() {
        ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
        context.getSystemService(LocaleManager::class.java)!!.applicationLocales=platformLocales
        val edit=context.getSharedPreferences("app-language",0).edit().clear()
        preferences.forEach { (key,value) -> when(value) {
            is String -> edit.putString(key,value)
            is Boolean -> edit.putBoolean(key,value)
            else -> error("Unexpected language preference: $key")
        } }
        edit.commit();PaintApplication.currentResources=resources;Locale.setDefault(previous)
    }
    private fun settle()=shadowOf(Looper.getMainLooper()).idleFor(32,TimeUnit.MILLISECONDS)
    private fun check(view: View,expected: String,tag: String) {
        assertEquals(expected,view.tooltipText.toString())
        val spans=(view.tooltipText as? Spanned)?.getSpans(0,view.tooltipText.length,MetricAffectingSpan::class.java).orEmpty()
        if(tag in setOf("vi-Hani","wuu-Hans")) {
            val paint=TextPaint();spans.single().updateMeasureState(paint)
            assertSame(LocaleTypography.typeface(view.context),paint.typeface)
        } else assertTrue(spans.isEmpty())
    }
    private fun popupLabel(view: View): TextView {
        val popup=requireNotNull(LocaleTooltipWindowTest.popup(view))
        return ReflectionHelpers.getField(popup,"mMessageView")
    }

    @Test fun editorToolCategoryPanelAndCursorRefreshRetainTheirExistingHelpPaths() {
        AppLanguage.select(context,"vi-Hani")
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        val activity=controller.get();awaitEditorStartup(activity)
        controller.visible().windowFocusChanged(true);settle()
        fun view(tag: String)=activity.window.decorView.findViewWithTag<View>(tag)
        fun click(tag: String) {EditorTestNavigation.click(activity,tag);settle()}
        try {
            click("menu_Draw")
            val tool=view("tool_PENCIL")
            check(tool,PaintTool.PENCIL.label,"vi-Hani")
            assertTrue(tool.performLongClick());settle()
            assertTrue(ShadowAlertDialog.getLatestAlertDialog().isShowing)
            assertNull(LocaleTooltipWindowTest.popup(tool));ShadowAlertDialog.getLatestAlertDialog().dismiss()
            val category=view("category_BRUSH") as ToolCategoryButton
            check(category,category.contentDescription.toString(),"vi-Hani")
            assertTrue(category.performLongClick());assertEquals(category.contentDescription.toString(),popupLabel(category).text.toString())
            // The real click changes the selected tool and refreshes the category caption.
            click("tool_WATERCOLOR")
            check(category,category.contentDescription.toString(),"vi-Hani")
            assertTrue(category.tooltipText.toString().contains(PaintTool.WATERCOLOR.label))
            if(LocaleTooltipWindowTest.popup(category)!=null) {
                assertTrue(category.performAccessibilityAction(android.view.accessibility.AccessibilityNodeInfo.AccessibilityAction.ACTION_HIDE_TOOLTIP.id,null))
            }
            assertTrue(category.performLongClick());settle()
            val refreshed=popupLabel(category)
            assertEquals(category.contentDescription.toString(),refreshed.text.toString())
            val refreshedPaint=TextPaint(refreshed.paint)
            (refreshed.text as Spanned).getSpans(0,refreshed.length(),MetricAffectingSpan::class.java).single().updateMeasureState(refreshedPaint)
            assertSame(LocaleTypography.typeface(activity),refreshedPaint.typeface)
            click("menu_View")
            val grid=view("command_View_1")
            check(grid,ui(R.string.ui_pixel_grid_help33),"vi-Hani")
            assertTrue(grid.performLongClick());settle()
            assertTrue(ShadowAlertDialog.getLatestAlertDialog().isShowing);assertNull(LocaleTooltipWindowTest.popup(grid))
            ShadowAlertDialog.getLatestAlertDialog().dismiss()
            check(view("command_View_0"),view("command_View_0").contentDescription.toString(),"vi-Hani")
            click("command_View_2");click("cursor_mode_enabled")
            val cursor=view("cursor_draw_toggle")
            check(cursor,ui(R.string.ui_cursor_start31),"vi-Hani")
            click("cursor_draw_toggle");assertTrue(activity.paintCanvas.cursorDrawing)
            check(cursor,ui(R.string.ui_cursor_stop31),"vi-Hani")
            click("cursor_draw_toggle");assertFalse(activity.paintCanvas.cursorDrawing)
            check(cursor,ui(R.string.ui_cursor_start31),"vi-Hani")
            assertTrue(cursor.performLongClick());settle()
            assertTrue(ShadowAlertDialog.getLatestAlertDialog().isShowing);assertNull(LocaleTooltipWindowTest.popup(cursor))
            ShadowAlertDialog.getLatestAlertDialog().dismiss()
            val save=view("save_image")
            check(save,EditIcon.SAVE.label,"vi-Hani")
            assertTrue(save.performLongClick());settle()
            val help=activity.window.decorView.findViewWithTag<TextView>("locale_notification_text")
            assertNotNull(help);assertEquals(EditIcon.SAVE.label,help.text.toString())
            assertNull(LocaleTooltipWindowTest.popup(save))
            for(tag in listOf("wuu-Hans","ar","mn-Mong","vi-Hani")) {
                val old=view("save_image")
                AppLanguage.select(activity,tag)
                val config=Configuration(activity.resources.configuration).apply {
                    orientation=if(tag=="wuu-Hans") Configuration.ORIENTATION_LANDSCAPE else Configuration.ORIENTATION_PORTRAIT
                }
                activity.onConfigurationChanged(config);settle()
                assertFalse(old.isAttachedToWindow);assertNull(LocaleTooltipWindowTest.popup(old))
                check(view("save_image"),EditIcon.SAVE.label,tag)
                check(view("cursor_draw_toggle"),ui(R.string.ui_cursor_start31),tag)
                assertEquals(EditIcon.SAVE.label,view("save_image").contentDescription.toString())
            }
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
            controller.pause().stop()
            val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(10)
            while(activity.busy && System.nanoTime()<deadline) {settle();Thread.sleep(5)}
            assertFalse(activity.busy);controller.destroy()
        }
    }

    @Test fun assemblyActionUsesNativeLongPressAndRebuildDetachesItsPopup() {
        AppLanguage.select(context,"wuu-Hans")
        File(context.filesDir,"image-assembly").deleteRecursively()
        val controller=Robolectric.buildActivity(AssemblyActivity::class.java).setup()
        val activity=controller.get();controller.visible().windowFocusChanged(true);settle()
        try {
            val undo=activity.window.decorView.findViewWithTag<View>("assembly_undo")
            // Empty assembly disables Undo; an enabled action is required by native long press.
            undo.isEnabled=true
            check(undo,EditIcon.UNDO.label,"wuu-Hans")
            assertTrue(undo.performLongClick());settle();assertEquals(EditIcon.UNDO.label,popupLabel(undo).text.toString())
            val popup=LocaleTooltipWindowTest.popupContent(undo)!!
            assertTrue(popup.isAttachedToWindow)
            AppLanguage.select(activity,"vi-Hani")
            activity.onConfigurationChanged(Configuration(activity.resources.configuration).apply {orientation=Configuration.ORIENTATION_LANDSCAPE})
            settle();assertFalse(undo.isAttachedToWindow);assertFalse(popup.isAttachedToWindow)
            assertNull(LocaleTooltipWindowTest.popup(undo))
            val rebuilt=activity.window.decorView.findViewWithTag<View>("assembly_undo")
            check(rebuilt,EditIcon.UNDO.label,"vi-Hani")
            assertEquals(EditIcon.UNDO.label,rebuilt.contentDescription.toString())
        } finally {controller.close()}
    }
}
