/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.content.res.Configuration
import android.os.LocaleList
import android.os.Build
import android.app.LocaleManager
import org.catrobat.paintroid.classic.PaintApplication
import org.junit.Before
import org.junit.After
import java.util.Locale
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config

/** M02 only: exact resources and explicit fallbacks, not linguistic acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
class CommonsMetadataHttpTranslationTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val expectedMessages=mapOf(
        "af" to "Commons-metadata: HTTP %1\$s",
        "ain-Kana" to "Commons コㇿ イヤヌ ネワ オルㇱペ: HTTP %1\$s",
        "ain-Latn" to "Commons kor iyanu newa oruspe: HTTP %1\$s",
        "ar" to "بيانات Commons الوصفية: HTTP %1\$s",
        "bo" to "Commons གྱི་མེ་ཊ་གནས་ཚུལ། HTTP %1\$s",
        "ceb" to "Metadata sa Commons: HTTP %1\$s",
        "de" to "Commons-Metadaten: HTTP %1\$s",
        "dz" to "Commons གི་མེ་ཊ་གནས་ཚུལ། HTTP %1\$s",
        "el" to "Μεταδεδομένα Commons: HTTP %1\$s",
        "en-001" to "Commons metadata: HTTP %1\$s",
        "en-AU" to "Commons metadata: HTTP %1\$s",
        "en-CA" to "Commons metadata: HTTP %1\$s",
        "en-GB" to "Commons metadata: HTTP %1\$s",
        "en-IN" to "Commons metadata: HTTP %1\$s",
        "en-SG" to "Commons metadata: HTTP %1\$s",
        "en-US" to "Commons metadata: HTTP %1\$s",
        "en-XV" to "Commons metadata: HTTP %1\$s",
        "eo" to "Metadatenoj de Commons: HTTP %1\$s",
        "es-419" to "Metadatos de Commons: HTTP %1\$s",
        "es-ES" to "Metadatos de Commons: HTTP %1\$s",
        "et" to "Commonsi metaandmed: HTTP %1\$s",
        "fi" to "Commonsin metatiedot: HTTP %1\$s",
        "fr" to "Métadonnées de Commons : HTTP %1\$s",
        "hak-Hant-TW" to "Commons 个中繼資料：HTTP %1\$s",
        "hak-Latn-TW" to "Commons ke chûng-ki chṳ̂-liau: HTTP %1\$s",
        "hu" to "A Commons metaadatai: HTTP %1\$s",
        "id" to "Metadata Commons: HTTP %1\$s",
        "it" to "Metadati di Commons: HTTP %1\$s",
        "ja" to "Commons のメタデータ: HTTP %1\$s",
        "jje" to "Commons 메타데이터: HTTP %1\$s",
        "ko-KP" to "Commons 자료의 설명 정보: HTTP %1\$s",
        "ko-KR" to "Commons 메타데이터: HTTP %1\$s",
        "ko-Kore-KR" to "Commons 메타데이터: HTTP %1\$s",
        "lt" to "Commons metaduomenys: HTTP %1\$s",
        "lv" to "Commons metadati: HTTP %1\$s",
        "lzh-Hant" to "Commons 之中繼資料：HTTP %1\$s",
        "mn-Cyrl-MN" to "Commons-ийн мета өгөгдөл: HTTP %1\$s",
        "mn-Mong" to "Commons ᠤᠨ ᠮᠧᠲ᠋ᠠ ᠮᠡᠳᠡᠭᠳᠡᠯ: HTTP %1\$s",
        "mnc-Mong" to "Commons ᡳ ᠵᡳᠰᡝ ᡳ ᡥᠠᠴᡳᠨ ᠪᡝ ᡤᡳᠰᡠᡵᡝᡥᡝ ᡥᡝᡵᡤᡝᠨ: HTTP %1\$s",
        "ms" to "Metadata Commons: HTTP %1\$s",
        "nan-Hant-TW" to "Commons 中繼資料：HTTP %1\$s",
        "nan-Latn-TW" to "Commons tiong kè chu-liāu: HTTP %1\$s",
        "nl" to "Commons-metadata: HTTP %1\$s",
        "pt-BR" to "Metadados do Commons: HTTP %1\$s",
        "pt-PT" to "Metadados do Commons: HTTP %1\$s",
        "qaa-Zsye-XV" to "⚠️ Commons metadata: HTTP %1\$s",
        "ru" to "Метаданные Commons: HTTP %1\$s",
        "ryu" to "Commons ぬメタデータ: HTTP %1\$s",
        "sw" to "Metadata ya Commons: HTTP %1\$s",
        "fil" to "Metadata ng Commons: HTTP %1\$s",
        "tr" to "Commons meta verileri: HTTP %1\$s",
        "vi" to "Siêu dữ liệu Commons: HTTP %1\$s",
        "vi-Hani" to "超 與 料 Commons: HTTP %1\$s",
        "wuu-Hans" to "Commons 元数据：HTTP %1\$s",
        "yue-Hant" to "Commons 中繼資料：HTTP %1\$s",
        "yue-Latn" to "Commons zung1 gai3 zi1 liu2: HTTP %1\$s",
        "zh-CN" to "Commons 元数据：HTTP %1\$s",
        "zh-HK" to "Commons 中繼資料：HTTP %1\$s",
        "zh-TW" to "Commons 中繼資料：HTTP %1\$s"
    )
    private var previousTag: String?=null
    private var previousInitialized: Boolean?=null
    private var previousPlatform: LocaleList?=null
    private lateinit var previousLocale: Locale
    private lateinit var previousResources: android.content.res.Resources
    @Before fun saveLanguageState() {
        val preferences=context.getSharedPreferences("app-language",Context.MODE_PRIVATE)
        previousTag=preferences.getString("language-tag",null)
        previousInitialized=if(preferences.contains("platform-initialized")) preferences.getBoolean("platform-initialized",false) else null
        if(Build.VERSION.SDK_INT>=33) previousPlatform=context.getSystemService(LocaleManager::class.java)!!.applicationLocales
        previousLocale=Locale.getDefault();previousResources=PaintApplication.currentResources
    }
    @After fun restoreLanguageState() {
        if(Build.VERSION.SDK_INT>=33) context.getSystemService(LocaleManager::class.java)!!.applicationLocales=previousPlatform!!
        context.getSharedPreferences("app-language",Context.MODE_PRIVATE).edit().apply {
            if(previousTag==null) remove("language-tag") else putString("language-tag",previousTag)
            if(previousInitialized==null) remove("platform-initialized") else putBoolean("platform-initialized",previousInitialized!!)
        }.commit()
        PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
    }
    private fun resourcesFor(tag: String): android.content.res.Resources {
        AppLanguage.select(context,tag)
        assertEquals("Persist the exact requested application tag",tag,AppLanguage.selectedTag(context))
        val wrapped=AppLanguage.wrap(context)
        // Public identity is unchanged. Private resource variants separate Korean
        // catalogues and supply English grammar for the emoji catalogue.
        val resourceTag=if(tag=="ko-Kore-KR") "ko-Kore-KR-anpaint"
            else if(tag=="qaa-Zsye-XV") "en-Zsye-XV-anpaint" else tag
        assertEquals(resourceTag,wrapped.resources.configuration.locales[0].toLanguageTag())
        PaintApplication.currentResources=wrapped.resources
        return wrapped.resources
    }
    @Test fun allOfferedTagsResolveTheirExplicitMessageOrDocumentedFallbackWithAsciiStatus() {
        assertEquals(171,AppLanguage.tags(context).size)
        assertEquals(59,expectedMessages.size)
        var fallbacks=0
        for(tag in AppLanguage.tags(context)) {
            val resources=resourcesFor(tag)
            val template=expectedMessages[tag] ?: "Commons metadata: HTTP %1\$s".also {fallbacks++}
            assertEquals(tag,template,resources.getString(R.string.commons_metadata_http_error))
            for(code in listOf(-1,199,201,204,301,403,429,500,503)) {
                val expected=template.replace("%1\$s",code.toString())
                assertEquals("$tag HTTP $code",expected,
                    resources.getString(R.string.commons_metadata_http_error,code.toString()))
                assertTrue(expected.contains("HTTP ${code}"))
            }
        }
        assertEquals(112,fallbacks)
    }
}
