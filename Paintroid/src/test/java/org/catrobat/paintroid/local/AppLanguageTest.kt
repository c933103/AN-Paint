/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.LocaleManager
import android.content.Context
import android.content.res.Configuration
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

    @Test fun regionalAndScriptChoicesAreSortedAndLegacyPreferencesMigrate() {
        val tags=AppLanguage.tags(context)
        assertEquals(tags.sortedWith(String.CASE_INSENSITIVE_ORDER),tags)
        assertFalse(tags.contains("zh-Hant"))
        assertTrue(tags.containsAll(listOf("zh-TW","zh-HK","mn-Mong","mn-Cyrl-MN")))
        context.getSharedPreferences("app-language",0).edit().putString("language-tag","zh-Hant").commit()
        assertEquals("zh-TW",AppLanguage.selectedTag(context))
        assertEquals("zh-TW",context.getSharedPreferences("app-language",0).getString("language-tag",null))
        AppLanguage.select(context,"zh-HK")
        assertEquals("擦膠",AppLanguage.wrap(context).getString(R.string.ui_eraser))
        AppLanguage.select(context,"zh-TW")
        assertEquals("橡皮擦",AppLanguage.wrap(context).getString(R.string.ui_eraser))
        AppLanguage.select(context,"mn-Cyrl-MN")
        val resources=AppLanguage.wrap(context).resources
        assertEquals("Таслах",resources.getString(R.string.ui_cut))
        assertNotEquals(resources.getString(R.string.ui_discard_changes23),resources.getString(R.string.ui_keep_editing23))
        assertEquals(org.catrobat.paintroid.classic.TextDirection.HORIZONTAL,org.catrobat.paintroid.classic.VerticalText.uiDirection())
    }

    @Test @Config(sdk=[33]) fun androidScriptOnlyChinesePreferenceMigratesToRegionalChoice() {
        val manager=context.getSystemService(LocaleManager::class.java)!!
        manager.applicationLocales=LocaleList.forLanguageTags("zh-Hant")
        assertEquals("zh-TW",AppLanguage.selectedTag(context))
        assertEquals("zh-TW",manager.applicationLocales[0].toLanguageTag())
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
            assertEquals("ファイル", activity.window.decorView.findViewWithTag<TextView>("menu_File").text.toString())
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

    @Test fun languageOverridePreservesRotationWindowSizeAndLargeTextWithoutReplacingDocument() {
        AppLanguage.select(context, "fr")
        context.filesDir.listFiles()?.filter { it.name.startsWith("classic-") }?.forEach { it.delete() }
        val controller = Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        val activity = controller.get()
        val original = Configuration(activity.resources.configuration)
        try {
            val document = activity.document
            document.newImage(16, 16)
            document.foreground = Color.RED; document.fill(2, 2)
            document.select(RectF(2f, 2f, 10f, 10f))
            val selection = document.selection
            for (landscape in listOf(true, false)) {
                val changed = Configuration(original).apply {
                    orientation = if (landscape) Configuration.ORIENTATION_LANDSCAPE else Configuration.ORIENTATION_PORTRAIT
                    screenWidthDp = if (landscape) 900 else 412
                    screenHeightDp = if (landscape) 412 else 900
                    fontScale = 1.5f
                }
                activity.onConfigurationChanged(changed)
                val actual = activity.resources.configuration
                assertEquals(changed.orientation, actual.orientation)
                assertEquals(changed.screenWidthDp, actual.screenWidthDp)
                assertEquals(changed.screenHeightDp, actual.screenHeightDp)
                assertEquals(1.5f, actual.fontScale, 0f)
                assertEquals("fr", actual.locales[0].language)
                // A new locale context must inherit these live device settings too.
                val wrapped = AppLanguage.wrap(activity).resources.configuration
                assertEquals(actual.orientation, wrapped.orientation)
                assertEquals(actual.screenWidthDp, wrapped.screenWidthDp)
                assertEquals(actual.fontScale, wrapped.fontScale, 0f)
                assertSame(document, activity.document)
                assertSame(selection, document.selection)
                assertTrue(document.canUndo)
                assertEquals(Color.RED, document.bitmap.getPixel(0, 0))
            }
        } finally {
            activity.onConfigurationChanged(original)
            controller.pause().stop()
            val deadline = System.nanoTime() + 10_000_000_000
            while (activity.busy && System.nanoTime() < deadline) {
                shadowOf(Looper.getMainLooper()).idle(); Thread.sleep(10)
            }
            controller.destroy()
        }
    }
}
