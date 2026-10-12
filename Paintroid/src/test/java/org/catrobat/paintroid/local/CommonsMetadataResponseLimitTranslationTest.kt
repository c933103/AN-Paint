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

/** M03 only: exact resources and explicit fallbacks, not linguistic acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
class CommonsMetadataResponseLimitTranslationTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val expectedMessages=mapOf(
        "ain-Kana" to "Commons オㇿ ワ アウㇰ タトゥㇺ (ノカ オルㇱペ) アナㇰ ポロ カㇱパ ワ アウㇰ エアイカㇷ゚.",
        "ain-Latn" to "Commons or wa a=uk tatum (noka oruspe) anak poro kaspa wa a=uk eaykap.",
        "mnc-Mong" to "ᠨᡳᡵᡠᡤᠠᠨ ᡳ Commons ᠴᡳ ᠠᠯᡳᠮᡝ ᡤᠠᡳᡥᠠ ᠮᡝᠵᡳᡤᡝ ᡳ ᡠᡥᡝᡵᡳ ᡴᡝᠮᡠᠨ ᡨᠣᡴᡨᠣᡥᠣ ᡴᡝᠮᡠᠨ ᠴᡳ ᡶᡠᠯᡠ.",
        "af" to "Commons-metadata oorskry die groottelimiet vir antwoorde",
        "ar" to "تتجاوز بيانات Commons الوصفية الحد الأقصى لحجم الاستجابة",
        "bo" to "Commons ཀྱི་མེ་ཊ་གནས་ཚུལ་གྱི་ལན་ནི་ལན་གྱི་ཆེ་ཆུང་གི་ཚད་ལས་བརྒལ་ཡོད།",
        "ceb" to "Ang metadata gikan sa Commons milapas sa limit sa gidak-on sa tubag",
        "de" to "Die Commons-Metadaten überschreiten die maximale Antwortgröße",
        "dz" to "Commons གི་མེ་ཊ་གནས་ཚུལ་གྱི་ལན་འདི་ ལན་གྱི་ཆེ་ཆུང་གི་ཚད་ལས་བརྒལ་ཡོད།",
        "el" to "Τα μεταδεδομένα του Commons υπερβαίνουν το όριο μεγέθους απόκρισης",
        "en-001" to "Commons metadata exceeds the response limit",
        "en-AU" to "Commons metadata exceeds the response limit",
        "en-CA" to "Commons metadata exceeds the response limit",
        "en-GB" to "Commons metadata exceeds the response limit",
        "en-IN" to "Commons metadata exceeds the response limit",
        "en-SG" to "Commons metadata exceeds the response limit",
        "en-US" to "Commons metadata exceeds the response limit",
        "en-XV" to "Commons metadata exceeds the response limit",
        "eo" to "La metadatenoj de Commons superas la grandolimon de la respondo",
        "es-419" to "Los metadatos de Commons superan el límite de tamaño de la respuesta",
        "es-ES" to "Los metadatos de Commons superan el límite de tamaño de la respuesta",
        "et" to "Commons-metaandmed ületavad vastuse suuruse piirangu",
        "fi" to "Commons-metatiedot ylittävät vastauksen kokorajan",
        "fr" to "Les métadonnées de Commons dépassent la taille maximale autorisée pour une réponse",
        "hak-Hant-TW" to "Commons 个中繼資料回應超出回應大細上限。",
        "hak-Latn-TW" to "Commons ke chûng-ki chṳ̂-liau fì-tap ke thai-se chhêu chhut sông-han.",
        "hu" to "A Commons metaadatai meghaladják a válasz méretkorlátját",
        "id" to "Metadata Commons melebihi batas ukuran respons",
        "it" to "I metadati di Commons superano il limite di dimensione della risposta",
        "ja" to "Commonsのメタデータが応答サイズの上限を超えています",
        "jje" to "Commons 메타데이터 응답 크기가 한도를 넘엇수다.",
        "ko-KP" to "Commons 설명 정보의 응답 크기가 한도를 초과합니다.",
        "ko-KR" to "Commons 메타데이터 응답 크기가 한도를 초과합니다.",
        "ko-Kore-KR" to "Commons 메타데이터 應答 크기가 限度를 超過합니다.",
        "lt" to "„Commons“ metaduomenys viršija atsakymo dydžio ribą",
        "lv" to "Commons metadati pārsniedz atbildes izmēra ierobežojumu",
        "lzh-Hant" to "Commons 中繼資料之應答逾應答大小之限。",
        "mn-Cyrl-MN" to "Commons-ийн мета өгөгдлийн хариуны хэмжээ хязгаараас хэтэрсэн.",
        "mn-Mong" to "Commons ᠤᠨ ᠮᠧᠲ᠋ᠠ ᠥᠭᠭᠦᠭᠳᠡᠯ ᠦᠨ ᠬᠠᠷᠢᠭᠤ ᠶᠢᠨ ᠬᠡᠮᠵᠢᠶ᠎ᠡ ᠬᠢᠵᠠᠭᠠᠷ ᠠᠴᠠ ᠬᠡᠲᠦᠷᠡᠪᠡ᠃",
        "ms" to "Metadata Commons melebihi had saiz respons",
        "nan-Hant-TW" to "Commons 的中繼資料回應超過回應大細上限。",
        "nan-Latn-TW" to "Commons ê tiong-kè chu-liāu hôe-èng chhiau-kòe hôe-èng tōa-sè siōng-hān.",
        "nl" to "De metadata van Commons overschrijden de maximale responsgrootte",
        "pt-BR" to "Os metadados do Commons excedem o limite de tamanho da resposta",
        "pt-PT" to "Os metadados do Commons excedem o limite de tamanho da resposta",
        "qaa-Zsye-XV" to "⚠️ Commons 🗂️ 📥📏 > 🚧",
        "ru" to "Метаданные Commons превышают лимит размера ответа",
        "ryu" to "Commonsぬメタデータ応答や、応答サイズぬ上限やか まぎさいびーん。",
        "sw" to "Metadata kutoka Commons inazidi kikomo cha ukubwa wa jibu",
        "tl" to "Lumampas ang metadata mula sa Commons sa limitasyon ng laki ng tugon",
        "tr" to "Commons meta verileri yanıt boyutu sınırını aşıyor",
        "vi" to "Siêu dữ liệu từ Commons vượt quá giới hạn kích thước phản hồi",
        "vi-Hani" to "戟 𡱩 返回 超 與 料 𧵑 Commons 越 過 界限.",
        "wuu-Hans" to "Commons 个元数据响应超出响应大小上限。",
        "yue-Hant" to "Commons 嘅中繼資料回應超出回應大小上限。",
        "yue-Latn" to "Commons ge3 zung1 gai3 zi1 liu6 wui4 jing3 ciu1 ceot1 wui4 jing3 daai6 siu2 soeng6 haan6.",
        "zh-CN" to "Commons 元数据超出响应大小上限",
        "zh-HK" to "Commons 中繼資料超出回應大小上限",
        "zh-TW" to "Commons 中繼資料超出回應大小上限"
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
        // Preference identity is unchanged; this one catalogue uses an internal
        // variant so Android cannot tie it with implicit-script ordinary Korean.
        val resourceTag=if(tag=="ko-Kore-KR") "ko-Kore-KR-anpaint" else tag
        assertEquals(resourceTag,wrapped.resources.configuration.locales[0].toLanguageTag())
        PaintApplication.currentResources=wrapped.resources
        return wrapped.resources
    }
    @Test fun allRequired59CataloguesHaveExplicitProposals() {
        assertEquals("Unresolved required proposals are a failing completeness gate, not English-filled translations",59,expectedMessages.size)
    }
    @Test fun all140TagsResolveTheirExplicitMessageOrDocumentedFallback() {
        assertEquals(140,AppLanguage.tags(context).size)
        var fallbacks=0
        for(tag in AppLanguage.tags(context)) {
            val resources=resourcesFor(tag)
            val expected=expectedMessages[tag] ?: "Commons metadata exceeds the response limit".also {fallbacks++}
            assertEquals(tag,expected,resources.getString(R.string.commons_metadata_response_too_large))
            assertTrue(expected.contains("Commons"))
        }
        assertEquals(81,fallbacks)
    }
}
