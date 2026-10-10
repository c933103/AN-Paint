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

/** All 140 offered tags have explicit exact-catalogue or default-fallback disposition. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
class CommonsCopyCreditTranslationTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val scopedTags=setOf(
        "af", "ain-Kana", "ain-Latn", "ar", "bo", "ceb", "de", "dz",
        "el", "en-001", "en-AU", "en-CA", "en-GB", "en-IN", "en-SG", "en-US",
        "en-XV", "eo", "es-419", "es-ES", "et", "fi", "fr", "hak-Hant-TW",
        "hak-Latn-TW", "hu", "id", "it", "ja", "jje", "ko-KP", "ko-KR",
        "ko-Kore-KR", "lt", "lv", "lzh-Hant", "mn-Cyrl-MN", "mn-Mong", "mnc-Mong", "ms",
        "nan-Hant-TW", "nan-Latn-TW", "nl", "pt-BR", "pt-PT", "qaa-Zsye-XV", "ru", "ryu",
        "sw", "tl", "tr", "vi", "vi-Hani", "wuu-Hans", "yue-Hant", "yue-Latn",
        "zh-CN", "zh-HK", "zh-TW"
    )
    // Exact language-tag expectations are independent of Android's fallback resolution.
    private val expectedMessages=mapOf(
        "af" to listOf("Kon nie die beeldkrediet kopieer nie.", "Kon nie die beeldkrediet kopieer nie: %1\$s", "Onvoldoende geheue om die beeldkrediet te kopieer."),
        "ain-Kana" to listOf("ノカ オルㇱペ アアットゥㇷ゚テ エアイカㇷ゚.", "ノカ オルㇱペ アアットゥㇷ゚テ エアイカㇷ゚: %1\$s", "ノカ オルㇱペ アアットゥㇷ゚テ クス RAM エハイェ."),
        "ain-Latn" to listOf("Noka oruspe a=attupte eaykap.", "Noka oruspe a=attupte eaykap: %1\$s", "Noka oruspe a=attupte kusu RAM ehaye."),
        "ar" to listOf("تعذر نسخ اعتماد الصورة.", "تعذر نسخ اعتماد الصورة: %1\$s", "لا توجد ذاكرة كافية لنسخ اعتماد الصورة."),
        "bo" to listOf("པར་རིས་ཀྱི་གསལ་བཤད་འདྲ་བཤུས་བྱེད་མ་ཐུབ།", "པར་རིས་ཀྱི་གསལ་བཤད་འདྲ་བཤུས་བྱེད་མ་ཐུབ: %1\$s", "པར་རིས་ཀྱི་གསལ་བཤད་འདྲ་བཤུས་བྱེད་པར་དྲན་ཤེས་མི་འདང་།"),
        "ceb" to listOf("Dili makopya ang kredito sa hulagway.", "Dili makopya ang kredito sa hulagway: %1\$s", "Kulang ang memorya aron kopyahon ang kredito sa hulagway."),
        "de" to listOf("Der Bildnachweis konnte nicht kopiert werden.", "Der Bildnachweis konnte nicht kopiert werden: %1\$s", "Nicht genügend Speicher, um den Bildnachweis zu kopieren."),
        "dz" to listOf("གཟུགས་བརྙན་གྱི་གསལ་བཤད་འདྲ་བཤུས་འབད་མ་ཚུགས།", "གཟུགས་བརྙན་གྱི་གསལ་བཤད་འདྲ་བཤུས་འབད་མ་ཚུགས: %1\$s", "གཟུགས་བརྙན་གྱི་གསལ་བཤད་འདྲ་བཤུས་འབད་ནི་དྲན་ཚད་མི་ལང་།"),
        "el" to listOf("Δεν ήταν δυνατή η αντιγραφή της αναφοράς δημιουργού της εικόνας.", "Δεν ήταν δυνατή η αντιγραφή της αναφοράς δημιουργού της εικόνας: %1\$s", "Δεν υπάρχει αρκετή μνήμη για την αντιγραφή της αναφοράς δημιουργού της εικόνας."),
        "en-001" to listOf("Could not copy image credit.", "Could not copy image credit: %1\$s", "Not enough memory to copy image credit."),
        "en-AU" to listOf("Could not copy image credit.", "Could not copy image credit: %1\$s", "Not enough memory to copy image credit."),
        "en-CA" to listOf("Could not copy image credit.", "Could not copy image credit: %1\$s", "Not enough memory to copy image credit."),
        "en-GB" to listOf("Could not copy image credit.", "Could not copy image credit: %1\$s", "Not enough memory to copy image credit."),
        "en-IN" to listOf("Could not copy image credit.", "Could not copy image credit: %1\$s", "Not enough memory to copy image credit."),
        "en-SG" to listOf("Could not copy image credit.", "Could not copy image credit: %1\$s", "Not enough memory to copy image credit."),
        "en-US" to listOf("Could not copy image credit.", "Could not copy image credit: %1\$s", "Not enough memory to copy image credit."),
        "en-XV" to listOf("Could not copy image credit.", "Could not copy image credit: %1\$s", "Not enough memory to copy image credit."),
        "eo" to listOf("Ne eblis kopii la bildan agnoskon.", "Ne eblis kopii la bildan agnoskon: %1\$s", "Ne sufiĉas memoro por kopii la bildan agnoskon."),
        "es-419" to listOf("No se pudo copiar la atribución de la imagen.", "No se pudo copiar la atribución de la imagen: %1\$s", "No hay memoria suficiente para copiar la atribución de la imagen."),
        "es-ES" to listOf("No se pudo copiar la atribución de la imagen.", "No se pudo copiar la atribución de la imagen: %1\$s", "No hay memoria suficiente para copiar la atribución de la imagen."),
        "et" to listOf("Pildi viidet ei saanud kopeerida.", "Pildi viidet ei saanud kopeerida: %1\$s", "Pildi viite kopeerimiseks pole piisavalt mälu."),
        "fi" to listOf("Kuvan krediittiä ei voitu kopioida.", "Kuvan krediittiä ei voitu kopioida: %1\$s", "Muisti ei riitä kuvan krediitin kopioimiseen."),
        "fr" to listOf("Impossible de copier les crédits de l’image.", "Impossible de copier les crédits de l’image : %1\$s", "Mémoire insuffisante pour copier les crédits de l’image."),
        "hak-Hant-TW" to listOf("做毋得複製圖像致謝。", "做毋得複製圖像致謝：%1\$s", "記憶體毋罅，做毋得複製圖像致謝。"),
        "hak-Latn-TW" to listOf("Cho-m̀-tet fu̍k-chṳ thù-siong chṳ-chhia.", "Cho-m̀-tet fu̍k-chṳ thù-siong chṳ-chhia: %1\$s", "Ki-yit thí m̀ la, cho-m̀-tet fu̍k-chṳ thù-siong chṳ-chhia."),
        "hu" to listOf("A képi forrásmegjelölést nem sikerült másolni.", "A képi forrásmegjelölést nem sikerült másolni: %1\$s", "Nincs elég memória a képi forrásmegjelölés másolásához."),
        "id" to listOf("Tidak dapat menyalin kredit gambar.", "Tidak dapat menyalin kredit gambar: %1\$s", "Memori tidak cukup untuk menyalin kredit gambar."),
        "it" to listOf("Impossibile copiare l’attribuzione dell’immagine.", "Impossibile copiare l’attribuzione dell’immagine: %1\$s", "Memoria insufficiente per copiare l’attribuzione dell’immagine."),
        "ja" to listOf("画像クレジットをコピーできませんでした。", "画像クレジットをコピーできませんでした: %1\$s", "画像クレジットをコピーするためのメモリが不足しています。"),
        "jje" to listOf("이미지 크레딧을 복사허지 못허엿수다.", "이미지 크레딧을 복사허지 못허엿수다: %1\$s", "이미지 크레딧을 복사헐 만큼 메모리가 엇수다."),
        "ko-KP" to listOf("화상 감사의 말을 복사할 수 없습니다.", "화상 감사의 말을 복사할 수 없습니다: %1\$s", "화상 감사의 말을 복사할 기억기가 부족합니다."),
        "ko-KR" to listOf("이미지 크레딧을 복사할 수 없습니다.", "이미지 크레딧을 복사할 수 없습니다: %1\$s", "이미지 크레딧을 복사할 메모리가 부족합니다."),
        "ko-Kore-KR" to listOf("이미지 크레딧을 複寫할 수 없습니다.", "이미지 크레딧을 複寫할 수 없습니다: %1\$s", "이미지 크레딧을 複寫할 메모리가 부족합니다."),
        "lt" to listOf("Nepavyko nukopijuoti vaizdo priskyrimo.", "Nepavyko nukopijuoti vaizdo priskyrimo: %1\$s", "Nepakanka atminties vaizdo priskyrimui nukopijuoti."),
        "lv" to listOf("Nevarēja nokopēt attēla norādi.", "Nevarēja nokopēt attēla norādi: %1\$s", "Nepietiek atmiņas attēla norādes kopēšanai."),
        "lzh-Hant" to listOf("未能複製圖像出處。", "未能複製圖像出處：%1\$s", "記憶體不足，未能複製圖像出處。"),
        "mn-Cyrl-MN" to listOf("Зургийн эх сурвалжийн мэдээллийг хуулж чадсангүй.", "Зургийн эх сурвалжийн мэдээллийг хуулж чадсангүй: %1\$s", "Зургийн эх сурвалжийн мэдээллийг хуулахад санах ой хүрэлцэхгүй."),
        "mn-Mong" to listOf("ᠵᠢᠷᠤᠭ ᠤᠨ ᠲᠠᠯᠠᠷᠬᠠᠯ ᠢ ᠬᠠᠭᠤᠯᠪᠤᠷᠢᠯᠠᠵᠤ ᠴᠢᠳᠠᠭᠰᠠᠨ ᠦᠭᠡᠢ᠃", "ᠵᠢᠷᠤᠭ ᠤᠨ ᠲᠠᠯᠠᠷᠬᠠᠯ ᠢ ᠬᠠᠭᠤᠯᠪᠤᠷᠢᠯᠠᠵᠤ ᠴᠢᠳᠠᠭᠰᠠᠨ ᠦᠭᠡᠢ: %1\$s", "ᠵᠢᠷᠤᠭ ᠤᠨ ᠲᠠᠯᠠᠷᠬᠠᠯ ᠢ ᠬᠠᠭᠤᠯᠪᠤᠷᠢᠯᠠᠬᠤ ᠳᠤ ᠣᠢ ᠬᠦᠷᠦᠯᠴᠡᠬᠦ ᠦᠭᠡᠢ᠃"),
        "mnc-Mong" to listOf("ᠨᡳᡵᡠᡤᠠᠨ ᡳ ᡤᡝᠪᡠᠯᡝᡥᡝ ᠪᠠᡳᡨᠠ ᠪᡝ ᡩᡠᡵᠰᡠᡴᡳᠯᡝᠮᡝ ᠮᡠᡨᡝᡵᠠᡴᡡ.", "ᠨᡳᡵᡠᡤᠠᠨ ᡳ ᡤᡝᠪᡠᠯᡝᡥᡝ ᠪᠠᡳᡨᠠ ᠪᡝ ᡩᡠᡵᠰᡠᡴᡳᠯᡝᠮᡝ ᠮᡠᡨᡝᡵᠠᡴᡡ: %1\$s", "ᠨᡳᡵᡠᡤᠠᠨ ᡳ ᡤᡝᠪᡠᠯᡝᡥᡝ ᠪᠠᡳᡨᠠ ᠪᡝ ᡩᡠᡵᠰᡠᡴᡳᠯᡝᡵᡝ ᡩᡝ RAM ᡥᠠᠮᡳᡵᠠᡴᡡ."),
        "ms" to listOf("Tidak dapat menyalin kredit imej.", "Tidak dapat menyalin kredit imej: %1\$s", "Memori tidak mencukupi untuk menyalin kredit imej."),
        "nan-Hant-TW" to listOf("袂當複製圖片致謝。", "袂當複製圖片致謝：%1\$s", "記憶體無夠，袂當複製圖片致謝。"),
        "nan-Latn-TW" to listOf("Bē-tàng ho̍k-chè tô͘-phìⁿ tì-siā.", "Bē-tàng ho̍k-chè tô͘-phìⁿ tì-siā: %1\$s", "Kì-ek-thé bô kàu, bē-tàng ho̍k-chè tô͘-phìⁿ tì-siā."),
        "nl" to listOf("Kan de afbeeldingscredits niet kopiëren.", "Kan de afbeeldingscredits niet kopiëren: %1\$s", "Onvoldoende geheugen om de afbeeldingscredits te kopiëren."),
        "pt-BR" to listOf("Não foi possível copiar o crédito da imagem.", "Não foi possível copiar o crédito da imagem: %1\$s", "Não há memória suficiente para copiar o crédito da imagem."),
        "pt-PT" to listOf("Não foi possível copiar o crédito da imagem.", "Não foi possível copiar o crédito da imagem: %1\$s", "Não há memória suficiente para copiar o crédito da imagem."),
        "qaa-Zsye-XV" to listOf("⚠️ Could not copy image credit.", "⚠️ Could not copy image credit: %1\$s", "⚠️ Not enough memory to copy image credit."),
        "ru" to listOf("Не удалось скопировать сведения об авторстве изображения.", "Не удалось скопировать сведения об авторстве изображения: %1\$s", "Недостаточно памяти для копирования сведений об авторстве изображения."),
        "ryu" to listOf("画像クレジットや コピーさらびらんたん。", "画像クレジットや コピーさらびらんたん: %1\$s", "画像クレジット コピーすんためぬメモリぬ足らびらん。"),
        "sw" to listOf("Sifa za picha hazikuweza kunakiliwa.", "Sifa za picha hazikuweza kunakiliwa: %1\$s", "Kumbukumbu haitoshi kunakili sifa za picha."),
        "tl" to listOf("Hindi makopya ang pagkilala para sa larawan.", "Hindi makopya ang pagkilala para sa larawan: %1\$s", "Kulang ang memory para kopyahin ang pagkilala para sa larawan."),
        "tr" to listOf("Görüntünün atıf bilgisi kopyalanamadı.", "Görüntünün atıf bilgisi kopyalanamadı: %1\$s", "Görüntünün atıf bilgisini kopyalamak için yeterli bellek yok."),
        "vi" to listOf("Không thể sao chép ghi công hình ảnh.", "Không thể sao chép ghi công hình ảnh: %1\$s", "Không đủ bộ nhớ để sao chép ghi công hình ảnh."),
        "vi-Hani" to listOf("空 体 抄 劄 𥱬 功 形 影.", "空 体 抄 劄 𥱬 功 形 影: %1\$s", "空 𨁥 部𢖵 抵 抄 劄 𥱬 功 形 影."),
        "wuu-Hans" to listOf("图片致谢复制勿了。", "图片致谢复制勿了：%1\$s", "内存勿够，图片致谢复制勿了。"),
        "yue-Hant" to listOf("複製唔到圖片鳴謝。", "複製唔到圖片鳴謝：%1\$s", "記憶體唔夠，複製唔到圖片鳴謝。"),
        "yue-Latn" to listOf("Fuk1 zai3 m4 dou2 tou4 pin2 ming4 ze6.", "Fuk1 zai3 m4 dou2 tou4 pin2 ming4 ze6: %1\$s", "Gei3 jik1 tai2 m4 gau3, fuk1 zai3 m4 dou2 tou4 pin2 ming4 ze6."),
        "zh-CN" to listOf("无法复制图片致谢信息。", "无法复制图片致谢信息：%1\$s", "内存不足，无法复制图片致谢信息。"),
        "zh-HK" to listOf("無法複製圖片鳴謝。", "無法複製圖片鳴謝：%1\$s", "記憶體不足，無法複製圖片鳴謝。"),
        "zh-TW" to listOf("無法複製圖片致謝資訊。", "無法複製圖片致謝資訊：%1\$s", "記憶體不足，無法複製圖片致謝資訊。")
    )
    private val fallbackTags=setOf(
        "am", "ast", "az", "be", "bg", "bn", "br", "bs",
        "ca", "ca-ES-valencia", "ckb", "cs", "csb", "cy", "da", "eu-ES",
        "fa", "fa-IR", "fy", "ga", "gd", "gl", "gu", "he",
        "hi", "hne", "hr", "hy", "ia", "is", "jv", "ka",
        "kab", "kk", "km", "kn", "ku", "ky", "la", "lo",
        "mai", "mk", "ml-IN", "mr", "mww", "my", "nds", "ne",
        "nn", "no", "oc", "pa-IN", "pl", "ps", "ro", "rw",
        "sd", "se", "shn", "si", "sk", "sl", "sq", "sr-Cyrl",
        "sr-Latn", "sv", "ta", "tdd", "te", "th", "tok", "tt-Cyrl",
        "tt-Latn", "ug", "uk", "ur", "uz-Latn", "wa", "xh", "yi",
        "za"
    )
    private val defaultMessages=listOf("Could not copy image credit.", "Could not copy image credit: %1\$s", "Not enough memory to copy image credit.")
    private val keys=listOf(R.string.commons_credit_copy_failed,R.string.commons_credit_copy_failed_reason,
        R.string.commons_credit_copy_out_of_memory)
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
        assertEquals(tag,wrapped.resources.configuration.locales[0].toLanguageTag())
        PaintApplication.currentResources=wrapped.resources
        return wrapped.resources
    }
    @Test fun all59ExactCataloguesResolveWholeMessagesAndKeepReasonArgumentVerbatim() {
        val reason="Provider 50%: %1\$s · détails\nTry again."
        val mismatches=mutableListOf<String>()
        val observations=org.json.JSONArray()
        for(tag in scopedTags) {
            val resources=resourcesFor(tag)
            val actual=keys.map {resources.getString(it)}
            observations.put(org.json.JSONObject().put("requested_tag",tag)
                .put("persisted_tag",AppLanguage.selectedTag(context))
                .put("resource_tag",resources.configuration.locales[0].toLanguageTag())
                .put("expected",org.json.JSONArray(expectedMessages.getValue(tag)))
                .put("actual",org.json.JSONArray(actual)))
            if(expectedMessages.getValue(tag)!=actual)
                mismatches.add("$tag expected ${expectedMessages.getValue(tag)} but was $actual")
            for(key in keys) {
                val text=resources.getString(key)
                assertTrue("$tag nonempty resource",text.isNotBlank())
            }
            val template=resources.getString(R.string.commons_credit_copy_failed_reason)
            assertEquals(1,template.windowed(4).count {it=="%1\$s"})
            assertEquals(template.replace("%1\$s",reason),resources.getString(R.string.commons_credit_copy_failed_reason,reason))
            assertFalse(resources.getString(R.string.commons_credit_copy_failed).contains("%"))
            assertFalse(resources.getString(R.string.commons_credit_copy_out_of_memory).contains("%"))
        }
        val report=java.io.File("build/reports/commons-copy-credit-resolution").apply {mkdirs()}
        java.io.File(report,"api${RuntimeEnvironment.getApiLevel()}.json").writeText(observations.toString(2)+"\n")
        assertTrue("Every exact manifest message must resolve through persisted app-language selection:\n"+
            mismatches.joinToString("\n"),mismatches.isEmpty())
    }
    @Test fun remaining81OfferedTagsExplicitlyResolveTheDefaultEnglishFallback() {
        val remaining=AppLanguage.tags(context).filter {it !in scopedTags}
        assertEquals(140,AppLanguage.tags(context).size);assertEquals(59,scopedTags.size);assertEquals(81,remaining.size)
        assertEquals(fallbackTags,remaining.toSet())
        for(tag in remaining) assertEquals("$tag documented default fallback is incomplete localization",
            defaultMessages,keys.map {resourcesFor(tag).getString(it)})
    }
}
