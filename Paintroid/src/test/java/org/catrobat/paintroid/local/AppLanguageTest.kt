/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.LocaleManager
import android.content.Context
import android.graphics.Color
import android.graphics.RectF
import android.os.LocaleList
import android.os.Looper
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.PaintApplication
import org.catrobat.paintroid.classic.ui
import org.catrobat.paintroid.classic.uiNumber
import org.junit.After
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.util.Locale
import java.util.concurrent.TimeUnit

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30], qualifiers="en-rUS-w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class AppLanguageTest {
    private val oldLocale = Locale.getDefault()
    private val context get() = RuntimeEnvironment.getApplication() as Context

    @After fun restoreLanguage() {
        AppLanguage.select(context, "")
        context.getSharedPreferences("app-language", 0).edit().clear().commit()
        PaintApplication.currentResources = AppLanguage.wrap(context).resources
        Locale.setDefault(oldLocale)
    }

    @Test fun chosenLanguagePersistsAndChangesResourcesAndDecimalInput() {
        AppLanguage.select(context, "fr")
        val wrapped = AppLanguage.wrap(context)
        PaintApplication.currentResources = wrapped.resources
        assertEquals("fr", AppLanguage.selectedTag(wrapped))
        assertEquals("Défaire", wrapped.getString(R.string.ui_undo))
        assertEquals(wrapped.getString(R.string.ui_cancel), ui(R.string.ui_cancel))
        assertEquals(12.75, uiNumber("12,75")!!, .0001)
        AppLanguage.select(context, "ar")
        val arabic = AppLanguage.wrap(context)
        assertEquals("ar", arabic.resources.configuration.locales[0].language)
        assertEquals(12.75, uiNumber("١٢٫٧٥")!!, .0001)
        AppLanguage.select(context, "")
        assertEquals("", AppLanguage.selectedTag(context))
        assertEquals("en", AppLanguage.wrap(context).resources.configuration.locales[0].language)
    }

    @Test fun pickerChangesCurrentWorkspaceWithoutLosingCanvasUndoOrSelection() {
        context.filesDir.listFiles()?.filter { it.name.startsWith("classic-") }?.forEach { it.delete() }
        context.getSharedPreferences("classic-ui", 0).edit().clear().commit()
        val controller = Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        val activity = controller.get()
        try {
            shadowOf(Looper.getMainLooper()).idleFor(50, TimeUnit.MILLISECONDS)
            val document = activity.document
            document.newImage(16, 16)
            document.foreground = Color.RED; document.fill(2, 2)
            document.select(RectF(2f, 2f, 10f, 10f))
            val selection = document.selection
            val method = ClassicPaintActivity::class.java.getDeclaredMethod("buildWorkspace").apply { isAccessible = true }
            val picker = AppLanguage.showPicker(activity) { method.invoke(activity) }
            val position = AppLanguage.tags(activity).indexOf("ja") + 1
            val list = picker.listView
            list.performItemClick(list.adapter.getView(position, null, list), position, position.toLong())
            assertFalse(picker.isShowing)
            assertSame(document, activity.document)
            assertSame(selection, document.selection)
            assertTrue(document.canUndo)
            assertEquals(Color.RED, document.bitmap.getPixel(0, 0))
            assertEquals("ja", activity.resources.configuration.locales[0].language)
            assertEquals("ヘルプ", activity.window.decorView.findViewWithTag<TextView>("menu_Help").text.toString())
            assertEquals(activity.getString(R.string.gallery_use_image), ui(R.string.gallery_use_image))
        } finally {
            controller.pause().stop()
            val deadline = System.nanoTime() + 10_000_000_000
            while (activity.busy && System.nanoTime() < deadline) {
                shadowOf(Looper.getMainLooper()).idle(); Thread.sleep(10)
            }
            controller.destroy()
        }
    }

    @Test @Config(sdk=[33]) fun androidAppLanguageAndInAppPreferenceUseTheSameSetting() {
        val manager = context.getSystemService(LocaleManager::class.java)!!
        AppLanguage.select(context, "de")
        assertEquals("de", manager.applicationLocales[0].language)
        manager.applicationLocales = LocaleList.forLanguageTags("ja")
        assertEquals("ja", AppLanguage.selectedTag(context))
        assertEquals("ja", AppLanguage.wrap(context).resources.configuration.locales[0].language)
        AppLanguage.select(context, "")
        assertTrue(manager.applicationLocales.isEmpty)
    }
}
