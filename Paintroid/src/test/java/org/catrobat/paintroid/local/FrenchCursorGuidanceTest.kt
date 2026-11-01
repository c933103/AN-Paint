/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.app.LocaleManager
import android.content.Context
import android.content.res.Resources
import android.os.LocaleList
import android.os.Looper
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
import org.robolectric.shadows.ShadowToast
import java.io.File
import java.util.Locale
import java.util.concurrent.TimeUnit

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class FrenchCursorGuidanceTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousPlatform: LocaleList
    private lateinit var previousPreferences: Map<String,*>
    private val help get() = PriorityWordingExpectations.resources("fr").getString(R.string.ui_cursor_help31)
    private val draw get() = PriorityWordingExpectations.resources("fr").getString(R.string.ui_cursor_pan_draw32)
    private val move get() = PriorityWordingExpectations.resources("fr").getString(R.string.ui_cursor_pan_move32)

    @Before fun selectFrench() {
        previousResources=PaintApplication.currentResources
        previousLocale=Locale.getDefault()
        previousPlatform=context.getSystemService(LocaleManager::class.java)!!.applicationLocales
        previousPreferences=context.getSharedPreferences("app-language",0).all.toMap()
        for(name in listOf("classic-recovery.png","classic-autosave.zip","classic-autosave.zip.bak"))
            File(context.filesDir,name).delete()
        context.getSharedPreferences("classic-ui",0).edit().clear().commit()
        AppLanguage.select(context,"fr")
    }
    @After fun restoreLocale() {
        ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
        context.getSystemService(LocaleManager::class.java)!!.applicationLocales=previousPlatform
        val edit=context.getSharedPreferences("app-language",0).edit().clear()
        previousPreferences.forEach { (key,value) -> when(value) {
            is String -> edit.putString(key,value)
            is Boolean -> edit.putBoolean(key,value)
            else -> error("Unexpected language preference: $key")
        } }
        edit.commit()
        PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
    }
    private fun idle()=shadowOf(Looper.getMainLooper()).idleFor(32,TimeUnit.MILLISECONDS)

    @Test fun compiledLegacyCursorHelpAliasUsesCurrentGuidance() {
        PaintApplication.currentResources=AppLanguage.wrap(context).resources
        assertEquals(help,ui(R.string.ui_cursor_help29))
    }

    @Test fun actualCursorHelpAndStartStopControlsUseFrenchGuidance() {
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        val activity=controller.get();awaitEditorStartup(activity)
        controller.visible().windowFocusChanged(true);idle()
        fun click(tag: String) {EditorTestNavigation.click(activity,tag);idle()}
        try {
            assertEquals("fr",AppLanguage.selectedTag(activity))
            click("command_View_2");click("cursor_mode_enabled")
            assertTrue(activity.paintCanvas.cursorMode)
            assertEquals(move+"\n"+ui(R.string.ui_cursor_tap_hint37),ShadowToast.getTextOfLatestToast())
            click("cursor_help")
            val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            val shown=dialog.findViewById<TextView>(android.R.id.message).text.toString()
            assertEquals(help+"\n\n"+ui(R.string.ui_cursor_tap_hint37)+"\n\n"+ui(R.string.ui_cursor_marker_help31),shown)
            dialog.dismiss()
            // The drawing tool's Help button takes the separate legacy-alias route.
            click("tool_BRUSH")
            assertTrue(activity.paintCanvas.cursorMode)
            assertEquals(PaintTool.BRUSH,activity.paintCanvas.tool)
            assertTrue(activity.window.decorView.findViewWithTag<View>("tool_help").isShown)
            click("tool_help")
            val toolDialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            assertEquals(help,toolDialog.findViewById<TextView>(android.R.id.message).text.toString())
            toolDialog.dismiss()
            click("cursor_draw_toggle");assertTrue(activity.paintCanvas.cursorDrawing)
            assertEquals(draw,ShadowToast.getTextOfLatestToast())
            click("cursor_draw_toggle");assertFalse(activity.paintCanvas.cursorDrawing)
            assertEquals(move,ShadowToast.getTextOfLatestToast())
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
            controller.pause().stop()
            val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(10)
            while(activity.busy && System.nanoTime()<deadline) {idle();Thread.sleep(5)}
            assertFalse(activity.busy);controller.destroy()
        }
    }
}
