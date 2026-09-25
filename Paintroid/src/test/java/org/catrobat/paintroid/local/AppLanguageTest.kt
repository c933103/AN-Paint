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
        assertEquals("en-001",tags.first())
        assertEquals(tags.drop(1).sortedWith(String.CASE_INSENSITIVE_ORDER),tags.drop(1))
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

    @Test fun regionalLabelsLegacyMigrationsAndStarterChoicesUseTheirCatalogues() {
        val tags=AppLanguage.tags(context)
        assertTrue(tags.containsAll(listOf("en-001","en-US","en-SG","en-IN","es-ES","es-419","ko-KR","ko-KP","pt-PT")))
        assertFalse(tags.any {it in listOf("en","es","ko","pt","cju","nan-TW-Hant","nan-TW-Latn")})
        assertEquals("English (International) [en-001]",AppLanguage.name("en-001"))
        assertEquals("Bahasa Indonesia [id]",AppLanguage.name("id"))
        assertEquals("Nederlands [nl]",AppLanguage.name("nl"))
        for((before,after) in listOf("en" to "en-001","es" to "es-ES","ko" to "ko-KR","pt" to "pt-PT","ain" to "ain-Latn","cju" to "jje","tai" to "tdd","tt" to "tt-Cyrl")) {
            context.getSharedPreferences("app-language",0).edit().putString("language-tag",before).commit()
            assertEquals(after,AppLanguage.selectedTag(context))
            assertEquals(after,context.getSharedPreferences("app-language",0).getString("language-tag",null))
        }
        val completeLowResourceTags=listOf("jje","mnc-Mong","ryu","ain-Kana","ain-Latn")
        assertTrue(tags.containsAll(completeLowResourceTags))
        for(tag in completeLowResourceTags) {
            assertTrue(AppLanguage.name(tag).endsWith("[$tag]"))
            assertEquals(tag,Locale.forLanguageTag(tag).toLanguageTag())
            AppLanguage.select(context,tag)
            val wrapped=AppLanguage.wrap(context)
            assertEquals(tag,AppLanguage.selectedTag(wrapped))
            assertEquals(tag,wrapped.resources.configuration.locales[0].toLanguageTag())
            assertNotEquals("File",wrapped.getString(R.string.ui_menu_file))
            assertNotEquals(listOf("Brush","Save","Cancel"),
                listOf(wrapped.getString(R.string.ui_brush),wrapped.getString(R.string.ui_save),wrapped.getString(R.string.ui_cancel)))
        }
        val starterTags=listOf("yue-Hant","yue-Latn","af","ku","tt-Cyrl","tt-Latn","lv","et","is","la","oc","se","my","shn","km","lo","ceb","jv","bo","ug","za","tdd","mww","nan-Hant-TW","nan-Latn-TW","hak-Hant","hak-Latn","wuu-Hans")
        assertEquals(28,starterTags.size)
        for(tag in starterTags) {
            assertTrue(tag,tag in tags);assertTrue(AppLanguage.name(tag).endsWith("[$tag]"))
            assertEquals(tag,Locale.forLanguageTag(tag).toLanguageTag())
            AppLanguage.select(context,tag)
            val wrapped=AppLanguage.wrap(context)
            assertEquals(tag,AppLanguage.selectedTag(wrapped))
            assertEquals(tag,wrapped.resources.configuration.locales[0].toLanguageTag())
            if(tag in listOf("lv","et","is","oc","my","tt-Cyrl","tt-Latn","yue-Hant","yue-Latn","ug","af","bo","lo")) assertNotEquals("File",wrapped.getString(R.string.ui_menu_file))
            // Completed translations and shared loanwords must not be frozen to an old English fallback.
            assertNotEquals(wrapped.getString(R.string.ui_discard_changes23),wrapped.getString(R.string.ui_keep_editing23))
            val vocabulary=listOf(wrapped.getString(R.string.ui_brush),wrapped.getString(R.string.ui_save),wrapped.getString(R.string.ui_cancel))
            assertNotEquals(listOf("Brush","Save","Cancel"),vocabulary)
            assertEquals("Save in the unsaved prompt must use the selected catalogue: $tag",
                wrapped.getString(R.string.ui_save),wrapped.getString(R.string.ui_save_a5d0d9))
        }
        assertFalse("The mistaken Tai collection choice is removed",tags.contains("tai"))
        assertEquals("ᥖᥭᥰ ᥖᥬᥲ ᥑᥨᥒᥰ [tdd]",AppLanguage.name("tdd"))
        AppLanguage.select(context,"tdd")
        assertEquals("ᥟᥛᥱ ᥞᥥᥖᥱ",AppLanguage.wrap(context).getString(R.string.ui_cancel))
        assertEquals("ᥛᥨᥢᥳ ᥛᥥᥰ",AppLanguage.wrap(context).getString(R.string.ui_menu_edit))
        AppLanguage.select(context,"en-US")
        assertEquals("Add color",AppLanguage.wrap(context).getString(R.string.ui_add_colour26))
        for(tag in listOf("en-001","en-SG","en-IN")) {
            AppLanguage.select(context,tag)
            assertEquals("Add colour",AppLanguage.wrap(context).getString(R.string.ui_add_colour26))
        }
    }

    @Test fun pickerPinsInternationalEnglishAndMongolianWordsFoldBesideTheCode()=checkMongolianPickerRow(16f)

    @Test @Config(qualifiers="en-rUS-w320dp-h640dp-port-xhdpi")
    fun narrowPickerFitsMongolianAutonymAndCodeAtLargeTextSize()=checkMongolianPickerRow(24f)

    @Test @Config(qualifiers="en-rUS-w900dp-h412dp-land-xhdpi")
    fun landscapePickerFitsTheFoldedMongolianOption()=checkMongolianPickerRow(16f)

    @Test fun manchuPickerFoldsNativeWordsAndKeepsTheCodeHorizontal()=checkMongolianPickerRow(16f,"mnc-Mong")

    private fun checkMongolianPickerRow(textSize: Float,tag: String="mn-Mong") {
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        val activity=controller.get()
        try {
            val picker=AppLanguage.showPicker(activity) {}
            val list=picker.listView
            assertEquals("English (International) [en-001]",list.adapter.getItem(1))
            val index=AppLanguage.tags(activity).indexOf(tag)+1
            list.setSelectionFromTop(index,0)
            shadowOf(Looper.getMainLooper()).idle()
            val row=list.getChildAt(index-list.firstVisiblePosition) as TextView
            row.textSize=textSize
            shadowOf(Looper.getMainLooper()).idle()
            val layout=row.layout;val last=layout.lineCount-1
            assertEquals(AppLanguage.name(tag),row.text.toString())
            assertEquals(row.text.length,layout.getLineEnd(last))
            val span=(row.text as android.text.Spanned).getSpans(0,row.text.length,android.text.style.ReplacementSpan::class.java).single()
            assertEquals("The horizontal locale code must remain outside the vertical span",
                row.text.indexOf(" ["),(row.text as android.text.Spanned).getSpanEnd(span))
            val font=android.graphics.Paint(row.paint).apply {typeface=android.graphics.Typeface.createFromAsset(activity.assets,"fonts/notosansmongolian.ttf")}
            assertTrue("The native name words must occupy adjacent columns",
                span.getSize(row.paint,row.text,0,row.text.indexOf(" ["),null)>=2*font.fontSpacing-1)
            assertEquals(0,layout.getEllipsisCount(last))
            assertTrue("The mounted list row must fit its ${layout.height}px caption inside ${row.height}px (layout height ${row.layoutParams.height})",
                layout.height<=row.height-row.totalPaddingTop-row.totalPaddingBottom)
            val image=android.graphics.Bitmap.createBitmap(row.width,row.height,android.graphics.Bitmap.Config.ARGB_8888)
            row.draw(android.graphics.Canvas(image))
            val neighbour=list.getChildAt(index-list.firstVisiblePosition+1) as android.widget.CheckedTextView
            val neighbourImage=android.graphics.Bitmap.createBitmap(neighbour.width,neighbour.height,android.graphics.Bitmap.Config.ARGB_8888)
            neighbour.draw(android.graphics.Canvas(neighbourImage));neighbourImage.recycle()
            val mark=(row as android.widget.CheckedTextView).checkMarkDrawable.bounds
            assertEquals("The vertical radio must align with ordinary language rows",neighbour.checkMarkDrawable.bounds.left,mark.left)
            assertEquals(neighbour.checkMarkDrawable.bounds.right,mark.right)
            val file=java.io.File("build/reports/classic-preview/language-${tag}-code-${textSize.toInt()}-${activity.resources.configuration.orientation}.png");file.parentFile.mkdirs()
            file.outputStream().use {image.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it)};image.recycle()
            val decor=picker.window!!.decorView
            val menu=android.graphics.Bitmap.createBitmap(decor.width,decor.height,android.graphics.Bitmap.Config.ARGB_8888)
            decor.draw(android.graphics.Canvas(menu))
            java.io.File(file.parentFile,"language-menu-${textSize.toInt()}-${activity.resources.configuration.orientation}.png").outputStream().use {menu.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it)};menu.recycle()
            picker.dismiss()
        } finally {
            controller.pause().stop()
            val end=System.nanoTime()+10_000_000_000L
            while(activity.busy && System.nanoTime()<end) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(10)}
            controller.destroy()
        }
    }

    @Test @Config(sdk=[33]) fun androidScriptOnlyChinesePreferenceMigratesToRegionalChoice() {
        val manager=context.getSystemService(LocaleManager::class.java)!!
        manager.applicationLocales=LocaleList.forLanguageTags("zh-Hant")
        assertEquals("zh-TW",AppLanguage.selectedTag(context))
        assertEquals("zh-TW",manager.applicationLocales[0].toLanguageTag())
        manager.applicationLocales=LocaleList.forLanguageTags("tai")
        assertEquals("tdd",AppLanguage.selectedTag(context))
        assertEquals("tdd",manager.applicationLocales[0].toLanguageTag())
    }

    @Test fun tatarScriptsAndAdditionalGimpLanguagesSelectTheirOwnResources() {
        val extra=listOf("am","ast","be","br","ca-ES-valencia","ckb","csb","dz","eo","ga","gd","ka","ky","mr","nds","ne","nn","rw","xh","yi")
        val tags=AppLanguage.tags(context)
        assertTrue(tags.containsAll(extra));assertFalse("kw" in tags)
        for(tag in extra) {
            AppLanguage.select(context,tag)
            assertEquals(tag,AppLanguage.wrap(context).resources.configuration.locales[0].toLanguageTag())
            assertTrue(AppLanguage.name(tag).endsWith("[$tag]"))
        }
        AppLanguage.select(context,"tt-Cyrl")
        var selected=AppLanguage.wrap(context)
        assertEquals("Саклау",selected.getString(R.string.ui_save))
        assertEquals("Төзәтмәләрне кире кагу",selected.getString(R.string.ui_discard_changes23))
        assertEquals("Үзгәртүне дәвам итү",selected.getString(R.string.ui_keep_editing23))
        AppLanguage.select(context,"tt-Latn")
        selected=AppLanguage.wrap(context)
        assertEquals("Saqlaw",selected.getString(R.string.ui_save))
        assertEquals("Tözätmälärne kire qağu",selected.getString(R.string.ui_discard_changes23))
        assertEquals("Üzgärtüne däwam itü",selected.getString(R.string.ui_keep_editing23))
        assertEquals("Pumala",selected.getString(R.string.ui_brush))
    }

    @Test @Config(sdk=[30,33]) fun deviceDefaultChoiceUsesSystemLanguageEvenWithAnotherAppLanguage() {
        AppLanguage.select(context,"ja")
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        val activity=controller.get()
        try {
            val picker=AppLanguage.showPicker(activity) {}
            assertEquals("Use device language",picker.listView.adapter.getItem(0))
            assertNotEquals(activity.getString(R.string.language20_device_default),picker.listView.adapter.getItem(0))
            assertEquals("ja",AppLanguage.selectedTag(activity))
            picker.dismiss()
        } finally {
            controller.pause().stop()
            val end=System.nanoTime()+10_000_000_000L
            while(activity.busy && System.nanoTime()<end) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(10)}
            controller.destroy()
        }
    }

    @Test fun requestedRegionsAndArmenianHaveTheirOwnMainMenuResources() {
        val expected=mapOf("hy" to "Ֆայլ", "es-ES" to "Archivo", "es-419" to "Archivo",
            "pt-PT" to "Ficheiro", "pt-BR" to "Arquivo", "ko-KR" to "파일", "ko-KP" to "파일",
            "sr-Cyrl" to "Датотека", "sr-Latn" to "Datoteka", "yue-Hant" to "檔案", "yue-Latn" to "Dong2 on3")
        for((tag,file) in expected) {
            AppLanguage.select(context,tag)
            val resources=AppLanguage.wrap(context).resources
            assertEquals(tag,file,resources.getString(R.string.ui_menu_file))
            assertNotEquals(tag,"Cursor drawing",resources.getString(R.string.ui_cursor_drawing32))
        }
        AppLanguage.select(context,"ko-KP")
        assertEquals("리용방법",AppLanguage.wrap(context).getString(R.string.ui_how_to_use))
        AppLanguage.select(context,"ko-KR")
        assertEquals("사용 방법",AppLanguage.wrap(context).getString(R.string.ui_how_to_use))
    }

    @Test fun chosenLanguagePersistsAndChangesResourcesAndDecimalInput() {
        AppLanguage.select(context, "fr")
        val wrapped = AppLanguage.wrap(context)
        PaintApplication.currentResources = wrapped.resources
        assertEquals("fr", AppLanguage.selectedTag(wrapped))
        assertEquals("Annuler", wrapped.getString(R.string.ui_undo))
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
