/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.LocaleManager
import android.content.Context
import android.os.Build
import android.os.Bundle
import android.os.LocaleList
import android.widget.TextView
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.PaintApplication
import org.junit.After
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.util.Locale

/**
 * Persisted-choice cold Activity creation and saved-state restoration, without a picker
 * callback or test-triggered refresh. This is not process-death or installed-device proof.
 * API 30 exercises the preference owner; API 35 exercises the platform locale owner.
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35], qualifiers="en-rUS-w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CantoneseColdActivityTest {
    private val application get()=RuntimeEnvironment.getApplication() as PaintApplication
    private val originalDefault=Locale.getDefault()
    private val originalResources=PaintApplication.currentResources

    @After fun restoreLanguage() {
        if(Build.VERSION.SDK_INT>=33)
            application.getSystemService(LocaleManager::class.java)!!.applicationLocales=LocaleList.getEmptyLocaleList()
        application.getSharedPreferences("app-language",Context.MODE_PRIVATE).edit().clear().commit()
        PaintApplication.currentResources=originalResources
        Locale.setDefault(originalDefault)
    }

    private fun seedPersistedChoice() {
        // Do not use select/refresh: startup must recover the stored owner itself.
        val preferences=application.getSharedPreferences("app-language",Context.MODE_PRIVATE)
        assertTrue(preferences.edit().putString("language-tag",
            if(Build.VERSION.SDK_INT>=33) "en-001" else "yue-Hant")
            .putBoolean("platform-initialized",true).commit())
        if(Build.VERSION.SDK_INT>=33)
            application.getSystemService(LocaleManager::class.java)!!.applicationLocales=LocaleList.forLanguageTags("yue-Hant")
        // A stale process default must not substitute for the persisted choice.
        Locale.setDefault(Locale.US)
    }

    private fun assertMountedMenus(activity: ClassicPaintActivity) {
        awaitEditorStartup(activity)
        assertEquals("yue-Hant",AppLanguage.selectedTag(activity))
        val file=activity.window.decorView.findViewWithTag<TextView>("menu_File")
        assertTrue("File tab mounted",file.isShown)
        // Independent script/routing boundary, not expected text from the same resolver.
        assertEquals("檔案",file.text.toString())
        EditorTestNavigation.click(activity,"menu_File")
        val save=activity.window.decorView.findViewWithTag<TextView>("command_File_2")
        assertTrue("Save command mounted",save.isShown)
        assertEquals("儲存",save.text.toString())
    }

    private fun close(controller: ActivityController<ClassicPaintActivity>) {
        controller.pause().stop().destroy()
    }

    @Test fun coldEditorReadsPersistedCantoneseWithoutPickerCallback() {
        seedPersistedChoice()
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        try {assertMountedMenus(controller.get())} finally {close(controller)}
    }

    @Test fun savedStateCreatesNewEditorWithPersistedCantoneseWithoutRefresh() {
        seedPersistedChoice()
        val first=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        val state=Bundle()
        try {
            assertMountedMenus(first.get())
            first.saveInstanceState(state)
        } finally {close(first)}
        // Deliberately stale default on a new Activity; the Application stays alive.
        Locale.setDefault(Locale.US)
        val second=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup(state)
        try {
            assertNotSame(first.get(),second.get())
            assertMountedMenus(second.get())
        } finally {close(second)}
    }
}
