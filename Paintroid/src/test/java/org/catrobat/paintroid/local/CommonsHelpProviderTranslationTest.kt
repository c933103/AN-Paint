/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.app.LocaleManager
import android.content.Context
import android.content.res.Configuration
import android.graphics.Paint
import android.os.Build
import android.os.LocaleList
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
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
import java.util.Locale

/** Resource inventory and actual Help/source-picker routes; not a full language/layout audit. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CommonsHelpProviderTranslationTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val scopedTags=listOf(
        "af", "ain-Kana", "ain-Latn", "ar", "bo", "ceb", "de", "dz",
        "el", "en-001", "en-AU", "en-CA", "en-GB", "en-IN", "en-SG", "en-US",
        "en-XV", "eo", "es-419", "es-ES", "et", "fi", "fr", "hak-Hant-TW",
        "hak-Latn-TW", "hu", "id", "it", "ja", "jje", "ko-KP", "ko-KR",
        "ko-Kore-KR", "lt", "lv", "lzh-Hant", "mn-Cyrl-MN", "mn-Mong", "mnc-Mong", "ms",
        "nan-Hant-TW", "nan-Latn-TW", "nl", "pt-BR", "pt-PT", "qaa-Zsye-XV", "ru", "ryu",
        "sw", "tl", "tr", "vi", "vi-Hani", "wuu-Hans", "yue-Hant", "yue-Latn",
        "zh-CN", "zh-HK", "zh-TW"
    )
    private fun resourcesFor(tag: String)=context.createConfigurationContext(Configuration().apply {
        setLocales(LocaleList.forLanguageTags(tag))
    }).resources

    @Test fun all59CataloguesContainTheirExactCommonsCaptionAndBundledGlyphs() {
        val english=resourcesFor("en-GB").getString(R.string.ui_help23)
        for(tag in scopedTags) {
            val resources=resourcesFor(tag)
            val help=resources.getString(R.string.ui_help23)
            val caption=resources.getString(R.string.commons_blank_maps)
            assertEquals("$tag exactly one Commons caption",1,help.windowed(caption.length).count {it==caption})
            assertTrue("$tag Catrobat retained",help.contains("Catrobat"))
            assertTrue("$tag Openclipart retained",help.contains("Openclipart"))
            if(!tag.startsWith("en-")) assertNotEquals("$tag is not an English-filled override",english,help)
            if(tag in listOf("vi-Hani","mn-Mong","mnc-Mong")) {
                val paint=Paint().apply {typeface=LocaleTypography.typeface(context,Locale.forLanguageTag(tag))}
                caption.codePoints().filter {point -> point>0x7f &&
                    Character.getType(point)!=Character.FORMAT.toInt() &&
                    Character.getType(point)!=Character.NON_SPACING_MARK.toInt()
                }.distinct().forEach {point ->
                    assertTrue("$tag missing U+${point.toString(16)}",paint.hasGlyph(String(Character.toChars(point))))
                }
            }
        }
    }

    @Test fun other81OfferedTagsUseTheGenuineDefaultHelpFallback() {
        // The host contract verifies these XML catalogues do not contain ui_help23.
        val remaining=AppLanguage.tags(context).filter {it !in scopedTags}
        assertEquals(81,remaining.size)
        val english=resourcesFor("en-GB").getString(R.string.ui_help23)
        for(tag in remaining) assertEquals("$tag explicit incomplete/fallback",english,
            resourcesFor(tag).getString(R.string.ui_help23))
    }

    @Test fun representativeWordingUsesCompleteLabelsAndReviewedPunctuation() {
        val passages=mapOf(
            "en-GB" to "Irasutoya, Openclipart and “Wikimedia Commons · Blank maps…”",
            "fr" to "Irasutoya, Openclipart et « Wikimedia Commons · Cartes muettes… »",
            "ja" to "いらすとや、Openclipart、［Wikimedia Commons · 白地図…］",
            "vi-Hani" to "Irasutoya, Openclipart 吧 「Wikimedia Commons · 版圖 𤿰…」",
            "et" to "Irasutoyat, Opencliparti ja valikut „Wikimedia Commons · Kontuurkaardid…“",
            "fi" to "Irasutoyan, Openclipartin ja ”Wikimedia Commons · Ääriviivakartat…” -valinnan"
        )
        for((tag,passage) in passages) assertTrue(tag,resourcesFor(tag).getString(R.string.ui_help23).contains(passage))
    }

    /** Capture preference presence before any selectedTag call can perform migration. */
    private fun withLanguage(tag: String,check: ()->Unit) {
        val preferences=context.getSharedPreferences("app-language",Context.MODE_PRIVATE)
        val hadTag=preferences.contains("language-tag")
        val oldTag=preferences.getString("language-tag",null)
        val hadInitialized=preferences.contains("platform-initialized")
        val oldInitialized=preferences.getBoolean("platform-initialized",false)
        val manager=if(Build.VERSION.SDK_INT>=33) context.getSystemService(LocaleManager::class.java) else null
        val oldPlatform=manager?.applicationLocales
        val oldLocale=Locale.getDefault()
        val oldResources=PaintApplication.currentResources
        try {
            AppLanguage.select(context,tag)
            PaintApplication.currentResources=AppLanguage.wrap(context).resources
            check()
        } finally {
            shadowOf(Looper.getMainLooper()).idle()
            if(oldPlatform!=null) manager?.applicationLocales=oldPlatform
            preferences.edit().apply {
                if(hadTag) putString("language-tag",oldTag) else remove("language-tag")
                if(hadInitialized) putBoolean("platform-initialized",oldInitialized) else remove("platform-initialized")
            }.commit()
            PaintApplication.currentResources=oldResources
            Locale.setDefault(oldLocale)
        }
    }
    private fun texts(view: View): List<TextView> =
        (if(view is TextView) listOf(view) else emptyList()) +
            (if(view is ViewGroup) (0 until view.childCount).flatMap {texts(view.getChildAt(it))} else emptyList())

    @Test @Config(sdk=[35])
    fun realFileHelpAndOtherImagesPickerAgreeAfterDismissalAndLanguageChanges() {
        assertEquals(listOf("CATROBAT","IRASUTOYA","OPENCLIPART","COMMONS"),IllustrationSource.values().map {it.name})
        for(tag in listOf("fr","ja","mn-Mong","vi-Hani","am")) withLanguage(tag) {
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
            val activity=controller.get()
            try {
                awaitEditorStartup(activity)
                val expected=resourcesFor(tag).getString(R.string.ui_help23)
                val caption=resourcesFor(tag).getString(R.string.commons_blank_maps)
                repeat(2) {
                    EditorTestNavigation.command(activity,"File",7)
                    val help=ShadowAlertDialog.getLatestAlertDialog()
                    assertTrue("$tag Help visible",help.isShowing)
                    assertEquals("$tag complete Help body through the real File command",1,
                        texts(help.window!!.decorView).count {it.text.toString()==expected})
                    assertTrue(expected.contains(caption))
                    assertTrue(help.getButton(AlertDialog.BUTTON_POSITIVE).performClick())
                    EditorTestNavigation.idle();assertFalse(help.isShowing)
                }
                EditorTestNavigation.click(activity,"menu_Draw")
                val category=activity.window.decorView.findViewWithTag<ToolCategoryButton>("category_INSERT")
                if(!category.expanded) EditorTestNavigation.click(activity,"category_INSERT")
                val tile=activity.window.decorView.findViewWithTag<View>("insert_other_images")
                assertTrue(tile.isShown);assertTrue(tile.performClick());EditorTestNavigation.idle()
                val picker=ShadowAlertDialog.getLatestAlertDialog()
                val entries=(0 until picker.listView.adapter.count).map {picker.listView.adapter.getItem(it).toString()}
                assertEquals(listOf(ui(R.string.ui_from_device34),ui(R.string.ui_catrobat_sticker_gallery),
                    "Irasutoya","Openclipart",caption),entries)
                assertTrue(picker.getButton(AlertDialog.BUTTON_NEGATIVE).performClick())
                EditorTestNavigation.idle();assertFalse(picker.isShowing)
            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.takeIf {it.isShowing}?.dismiss()
                controller.pause().stop().destroy()
            }
        }
    }
}
