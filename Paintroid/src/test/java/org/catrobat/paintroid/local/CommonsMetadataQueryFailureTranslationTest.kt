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

/** M04 only: exact resources and explicit fallbacks, not linguistic acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
class CommonsMetadataQueryFailureTranslationTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val expectedMessages=mapOf(
        "af" to "Die navraag vir Commons-metadata het misluk",
        "ain-Kana" to "タトゥㇺ (ノカ オルㇱペ) アナㇰ Commons アコヌ エアイカㇷ゚.",
        "ain-Latn" to "Tatum (noka oruspe) anak Commons a=konu eaykap.",
        "ar" to "فشل الاستعلام عن بيانات Commons الوصفية",
        "bo" to "Commons ལ་པར་གྱི་གནས་ཚུལ་དྲིས་པ་ལམ་ལྷོངས་མ་བྱུང་།",
        "ceb" to "Wala molampos ang pagpangayo sa metadata gikan sa Commons",
        "de" to "Die Abfrage der Commons-Metadaten ist fehlgeschlagen",
        "dz" to "Commons གི་མེ་ཊ་གནས་སྡུད་འདྲི་དཔྱད་འབད་མ་ཚུགས།",
        "el" to "Το ερώτημα για τα μεταδεδομένα του Commons απέτυχε",
        "en-001" to "Commons metadata query failed",
        "en-AU" to "Commons metadata query failed",
        "en-CA" to "Commons metadata query failed",
        "en-GB" to "Commons metadata query failed",
        "en-IN" to "Commons metadata query failed",
        "en-SG" to "Commons metadata query failed",
        "en-US" to "Commons metadata query failed",
        "en-XV" to "Commons metadata query failed",
        "eo" to "La peto pri metadatenoj de Commons malsukcesis",
        "es-419" to "Falló la consulta de metadatos de Commons",
        "es-ES" to "Falló la consulta de metadatos de Commons",
        "et" to "Commonsi metaandmete päring ebaõnnestus",
        "fi" to "Commons-metatietojen kysely epäonnistui",
        "fr" to "La requête de métadonnées de Commons a échoué",
        "hak-Hant-TW" to "查 Commons 个中繼資料失敗。",
        "hak-Latn-TW" to "Chhà Commons ke chûng-ki chṳ̂-liau sṳt-phai.",
        "hu" to "A Commons metaadatainak lekérdezése sikertelen",
        "id" to "Kueri metadata Commons gagal",
        "it" to "La richiesta dei metadati di Commons non è riuscita",
        "ja" to "Commonsのメタデータの問い合わせに失敗しました",
        "jje" to "Commons 메타데이터 질의가 실패헷수다.",
        "ko-KP" to "Commons 메타자료 요청에 실패하였습니다.",
        "ko-KR" to "Commons 메타데이터 조회에 실패했습니다.",
        "ko-Kore-KR" to "Commons 메타데이터 照會에 失敗했습니다.",
        "lt" to "„Commons“ metaduomenų užklausa nepavyko",
        "lv" to "Commons metadatu vaicājums neizdevās",
        "lzh-Hant" to "查詢 Commons 中繼資料未成。",
        "mn-Cyrl-MN" to "Commons-ын мета өгөгдлийн хүсэлт амжилтгүй боллоо.",
        "mn-Mong" to "Commons ᠠᠴᠠ ᠵᠢᠷᠤᠭ ᠤᠨ ᠮᠡᠳᠡᠭᠡᠯᠡᠯ ᠢ ᠯᠠᠪᠯᠠᠬᠤ ᠬᠦᠰᠡᠯᠲᠡ ᠪᠦᠲᠦᠭᠰᠡᠨ ᠦᠭᠡᠢ᠃",
        "mnc-Mong" to "Commons᠎ᡩᡝ ᠨᡳᡵᡠᡤᠠᠨ᠎ᡳ ᠮᡝᠵᡳᡤᡝ᠎ᠪᡝ ᡶᠣᠨᠵᡳᠮᡝ ᠮᡠᡨᡝᡥᡝᡴᡡ.",
        "ms" to "Pertanyaan metadata Commons gagal",
        "nan-Hant-TW" to "查詢 Commons 的中繼資料失敗。",
        "nan-Latn-TW" to "Chhâ-sûn Commons ê tiong-kè chu-liāu sit-pāi.",
        "nl" to "De aanvraag voor Commons-metadata is mislukt",
        "pt-BR" to "Falha na consulta aos metadados do Commons",
        "pt-PT" to "A consulta aos metadados do Commons falhou",
        "qaa-Zsye-XV" to "⚠️ Commons 🗂️ 🔎 ❌",
        "ru" to "Запрос метаданных Commons завершился ошибкой",
        "ryu" to "Commonsんかい メタデータ たぬむしぬ ないはんちゃん。",
        "sw" to "Ombi la metadata ya Commons halikufaulu",
        "fil" to "Nabigo ang kahilingan para sa metadata ng Commons",
        "tr" to "Commons meta verileri sorgusu başarısız oldu",
        "vi" to "Truy vấn siêu dữ liệu của Commons thất bại",
        "vi-Hani" to "追問超與料𧵑 Commons 失敗。",
        "wuu-Hans" to "Commons 个元数据查询失败。",
        "yue-Hant" to "Commons 嘅中繼資料查詢失敗。",
        "yue-Latn" to "Commons ge3 zung1 gai3 zi1 liu6 caa4 seon1 sat1 baai6.",
        "zh-CN" to "Commons 元数据查询失败",
        "zh-HK" to "Commons 中繼資料查詢失敗",
        "zh-TW" to "Commons 中繼資料查詢失敗"
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
    @Test fun allRequired59CataloguesHaveExplicitProposals() {
        assertEquals("Unresolved required proposals are a failing completeness gate, not English-filled translations",59,expectedMessages.size)
    }
    @Test fun allOfferedTagsResolveTheirExplicitMessageOrDocumentedFallback() {
        assertEquals(171,AppLanguage.tags(context).size)
        var fallbacks=0
        for(tag in AppLanguage.tags(context)) {
            val resources=resourcesFor(tag)
            val expected=expectedMessages[tag] ?: "Commons metadata query failed".also {fallbacks++}
            assertEquals(tag,expected,resources.getString(R.string.commons_metadata_query_failed))
            assertTrue(expected.contains("Commons"))
        }
        assertEquals(112,fallbacks)
    }
}
