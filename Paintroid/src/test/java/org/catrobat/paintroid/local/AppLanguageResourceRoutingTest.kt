/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.LocaleManager
import android.content.Context
import android.content.res.Configuration
import android.os.Build
import android.os.LocaleList
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.PaintApplication
import org.catrobat.paintroid.classic.TextDirection
import org.catrobat.paintroid.classic.VerticalText
import org.json.JSONArray
import org.json.JSONObject
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.io.File
import java.text.DecimalFormatSymbols
import java.util.Locale

/** Whole-catalogue selection without changing the public language preference. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
class AppLanguageResourceRoutingTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private var previousTag: String?=null
    private var previousInitialized: Boolean?=null
    private var previousPlatform: LocaleList?=null
    private lateinit var previousLocale: Locale
    private lateinit var previousResources: android.content.res.Resources

    @Before fun saveLanguage() {
        val preferences=context.getSharedPreferences("app-language",Context.MODE_PRIVATE)
        previousTag=preferences.getString("language-tag",null)
        previousInitialized=if(preferences.contains("platform-initialized"))
            preferences.getBoolean("platform-initialized",false) else null
        if(Build.VERSION.SDK_INT>=33)
            previousPlatform=context.getSystemService(LocaleManager::class.java)!!.applicationLocales
        previousLocale=Locale.getDefault();previousResources=PaintApplication.currentResources
    }

    @After fun restoreLanguage() {
        if(Build.VERSION.SDK_INT>=33)
            context.getSystemService(LocaleManager::class.java)!!.applicationLocales=previousPlatform!!
        context.getSharedPreferences("app-language",Context.MODE_PRIVATE).edit().apply {
            if(previousTag==null) remove("language-tag") else putString("language-tag",previousTag)
            if(previousInitialized==null) remove("platform-initialized")
            else putBoolean("platform-initialized",previousInitialized!!)
        }.commit()
        PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
    }

    @Test fun onlyTheTwoSpecialCataloguesUseInternalResourceVariants() {
        for(tag in AppLanguage.tags(context)) {
            val chosen=Locale.forLanguageTag(tag)
            val expected=if(tag=="ko-Kore-KR") "ko-Kore-KR-anpaint"
                        else if(tag=="qaa-Zsye-XV") "en-Zsye-XV-anpaint" else tag
            assertEquals(tag,expected,AppLanguage.resourceLocale(chosen).toLanguageTag())
        }
        assertFalse(AppLanguage.tags(context).any {it.contains("anpaint")})
        val chosen=Locale.forLanguageTag("ko-Kore-KR")
        val original=DecimalFormatSymbols(chosen)
        val routed=DecimalFormatSymbols(AppLanguage.resourceLocale(chosen))
        assertEquals(original.zeroDigit,routed.zeroDigit)
        assertEquals(original.decimalSeparator,routed.decimalSeparator)
        assertEquals(original.groupingSeparator,routed.groupingSeparator)
        assertEquals(original.minusSign,routed.minusSign)
        assertEquals(original.currencySymbol,routed.currencySymbol)
    }

    private fun reviewedTatarLatinScriptRow(row:JSONObject):JSONObject {
        require(row.keys().asSequence().toSet()==setOf("requested_tag","resource_tag","expected"))
        require(row.getString("requested_tag")=="tt-Latn" && row.getString("resource_tag")=="tt-Latn")
        val old=row.getJSONObject("expected")
        require(old.keys().asSequence().toSet()==setOf("ui_save","ui_menu_file","language20_device_default"))
        require(old.getString("ui_save")=="Saqlaw" && old.getString("ui_menu_file")=="Fayl")
        require(old.getString("language20_device_default")=="Use device language")
        val fixture=JSONObject(File("../tools/fixtures/exact_script_priority_wording/tt-Latn.json").readText(Charsets.UTF_8))
        assertEquals("tt-Latn",fixture.getString("locale"))
        val rows=fixture.getJSONObject("rows")
        for(key in listOf("ui_save","ui_menu_file")) assertEquals(old.getString(key),rows.getJSONObject(key).getString("compiled_display"))
        val label=rows.getJSONObject("language20_device_default")
        assertTrue(label.isNull("previous_target"));assertEquals("edited",label.getString("decision"))
        assertEquals("Use device language",label.getJSONObject("source").getString("value"))
        return JSONObject(row.toString()).apply {getJSONObject("expected").put("language20_device_default",label.getString("compiled_display"))}
    }
    @Test fun tatarLatinDeviceLabelRejectsChangedHistoricalRows() {
        val original=JSONObject("""{"requested_tag":"tt-Latn","resource_tag":"tt-Latn","expected":{"ui_save":"Saqlaw","ui_menu_file":"Fayl","language20_device_default":"Use device language"}}""")
        val snapshot=original.toString()
        assertEquals("Caylanma telen qullanu",reviewedTatarLatinScriptRow(original).getJSONObject("expected").getString("language20_device_default"))
        assertEquals(snapshot,original.toString())
        val invalid=mutableListOf<JSONObject>()
        for(key in listOf("requested_tag","resource_tag","expected")) invalid.add(JSONObject(snapshot).apply {remove(key)})
        for(key in listOf("requested_tag","resource_tag")) invalid.add(JSONObject(snapshot).apply {put(key,"tt-Cyrl")})
        invalid.add(JSONObject(snapshot).apply {put("extra",true)})
        for(key in listOf("ui_save","ui_menu_file","language20_device_default")) {
            invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").remove(key)})
            invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").put(key,"forged")})
        }
        invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").put("extra",true)})
        invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").put("language20_device_default","Caylanma telen qullanu")})
        assertEquals(14,invalid.size)
        for(row in invalid) {
            var rejected=false
            try {reviewedTatarLatinScriptRow(row)} catch (_:Exception) {rejected=true}
            assertTrue("Changed historical Tatar-Latin row must fail: $row",rejected)
        }
        assertEquals(snapshot,original.toString())
    }

    private fun reviewedUzbekScriptRow(row:JSONObject):JSONObject {
        require(row.keys().asSequence().toSet()==setOf("requested_tag","resource_tag","expected"))
        require(row.getString("requested_tag")=="uz-Latn" && row.getString("resource_tag")=="uz-Latn")
        val old=row.getJSONObject("expected")
        require(old.keys().asSequence().toSet()==setOf("ui_save","ui_menu_file","language20_device_default"))
        require(old.getString("ui_save")=="Saqlash" && old.getString("ui_menu_file")=="Fayl")
        require(old.getString("language20_device_default")=="Use device language")
        // Independently reviewed addition; the historical routing fixture stays untouched.
        return JSONObject(row.toString()).apply {
            getJSONObject("expected").put("language20_device_default","Qurilma tilidan foydalanish")
        }
    }

    @Test fun uzbekDeviceLabelSuccessorRejectsChangedHistoricalRows() {
        val original=JSONObject("""{"requested_tag":"uz-Latn","resource_tag":"uz-Latn","expected":{"ui_save":"Saqlash","ui_menu_file":"Fayl","language20_device_default":"Use device language"}}""")
        val snapshot=original.toString()
        val current=reviewedUzbekScriptRow(original)
        assertEquals("Qurilma tilidan foydalanish",current.getJSONObject("expected").getString("language20_device_default"))
        assertEquals(snapshot,original.toString())
        val invalid=mutableListOf<JSONObject>()
        for(key in listOf("requested_tag","resource_tag","expected"))
            invalid.add(JSONObject(snapshot).apply {remove(key)})
        for(key in listOf("requested_tag","resource_tag"))
            invalid.add(JSONObject(snapshot).apply {put(key,"uz")})
        invalid.add(JSONObject(snapshot).apply {put("extra",true)})
        for(key in listOf("ui_save","ui_menu_file","language20_device_default")) {
            invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").remove(key)})
            invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").put(key,"forged")})
        }
        invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").put("extra",true)})
        invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").put("language20_device_default","Qurilma tilidan foydalanish")})
        assertEquals(14,invalid.size)
        for(row in invalid) {
            var rejected=false
            try {reviewedUzbekScriptRow(row)} catch (_:Exception) {rejected=true}
            assertTrue("Changed historical row must fail: $row",rejected)
        }
    }

    private fun reviewedTatarScriptRow(row:JSONObject):JSONObject {
        require(row.keys().asSequence().toSet()==setOf("requested_tag","resource_tag","expected"))
        require(row.getString("requested_tag")=="tt-Cyrl" && row.getString("resource_tag")=="tt-Cyrl")
        val old=row.getJSONObject("expected")
        require(old.keys().asSequence().toSet()==setOf("ui_save","ui_menu_file","language20_device_default"))
        require(old.getString("ui_save")=="Саклау" && old.getString("ui_menu_file")=="Файл")
        require(old.getString("language20_device_default")=="Use device language")
        // Independently reviewed addition; the historical routing fixture stays untouched.
        return JSONObject(row.toString()).apply {
            getJSONObject("expected").put("language20_device_default","Җайланма телен куллану")
        }
    }

    @Test fun tatarDeviceLabelSuccessorRejectsChangedHistoricalRows() {
        val original=JSONObject("""{"requested_tag":"tt-Cyrl","resource_tag":"tt-Cyrl","expected":{"ui_save":"Саклау","ui_menu_file":"Файл","language20_device_default":"Use device language"}}""")
        val snapshot=original.toString()
        val current=reviewedTatarScriptRow(original)
        assertEquals("Җайланма телен куллану",current.getJSONObject("expected").getString("language20_device_default"))
        assertEquals(snapshot,original.toString())
        val invalid=mutableListOf<JSONObject>()
        for(key in listOf("requested_tag","resource_tag","expected"))
            invalid.add(JSONObject(snapshot).apply {remove(key)})
        for(key in listOf("requested_tag","resource_tag"))
            invalid.add(JSONObject(snapshot).apply {put(key,"tt")})
        invalid.add(JSONObject(snapshot).apply {put("extra",true)})
        for(key in listOf("ui_save","ui_menu_file","language20_device_default")) {
            invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").remove(key)})
            invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").put(key,"forged")})
        }
        invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").put("extra",true)})
        invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").put("language20_device_default","Җайланма телен куллану")})
        assertEquals(14,invalid.size)
        for(row in invalid) {
            var rejected=false
            try {reviewedTatarScriptRow(row)} catch (_:Exception) {rejected=true}
            assertTrue("Changed historical row must fail: $row",rejected)
        }
    }

    private fun reviewedMongolianScriptRow(row:JSONObject):JSONObject {
        require(row.keys().asSequence().toSet()==setOf("requested_tag","resource_tag","expected"))
        require(row.getString("requested_tag")=="mn-Cyrl-MN" && row.getString("resource_tag")=="mn-Cyrl-MN")
        val old=row.getJSONObject("expected")
        require(old.keys().asSequence().toSet()==setOf("ui_save","ui_menu_file","language20_device_default"))
        require(old.getString("ui_save")=="Хадгалах" && old.getString("ui_menu_file")=="Файл")
        require(old.getString("language20_device_default")=="Төхөөрөмжийн хэл")
        // Bind the complete accepted fixture before this finite historical-row projection.
        val bytes=File("../tools/fixtures/current_localization/moroccan_arabic_mongolian_toki_pona_priority_wording.json").readBytes()
        val sha=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        require(sha=="02b4dcb288d76cc53c7d50e2e91375cd6aecffbf9a404a3d0a61987e86197f62")
        val bound=JSONObject(String(bytes,Charsets.UTF_8))
        val source=bound.getJSONObject("sources").getJSONObject("language20_device_default")
        require(source.getString("type")=="string" && source.getString("source")=="Use device language")
        require(source.getJSONObject("attributes").getString("name")=="language20_device_default")
        val locale=bound.getJSONObject("locales").getJSONObject("mn-Cyrl-MN")
        require(locale.getJSONObject("predecessors").getJSONObject("language20_device_default").getString("target")=="Төхөөрөмжийн хэл")
        require(locale.getJSONObject("accepted").getString("language20_device_default")=="Төхөөрөмжийн хэлийг ашиглах")
        // The historical routing fixture stays untouched; no catalogue rollback.
        return JSONObject(row.toString()).apply {
            getJSONObject("expected").put("language20_device_default","Төхөөрөмжийн хэлийг ашиглах")
        }
    }

    @Test fun mongolianDeviceLabelSuccessorRejectsChangedHistoricalRows() {
        val original=JSONObject("""{"requested_tag":"mn-Cyrl-MN","resource_tag":"mn-Cyrl-MN","expected":{"ui_save":"Хадгалах","ui_menu_file":"Файл","language20_device_default":"Төхөөрөмжийн хэл"}}""")
        val snapshot=original.toString()
        val current=reviewedMongolianScriptRow(original)
        assertEquals("Төхөөрөмжийн хэлийг ашиглах",current.getJSONObject("expected").getString("language20_device_default"))
        assertEquals(snapshot,original.toString())
        val invalid=mutableListOf<JSONObject>()
        for(key in listOf("requested_tag","resource_tag","expected"))
            invalid.add(JSONObject(snapshot).apply {remove(key)})
        for(key in listOf("requested_tag","resource_tag"))
            invalid.add(JSONObject(snapshot).apply {put(key,"mn")})
        invalid.add(JSONObject(snapshot).apply {put("extra",true)})
        for(key in listOf("ui_save","ui_menu_file","language20_device_default")) {
            invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").remove(key)})
            invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").put(key,"forged")})
        }
        invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").put("extra",true)})
        invalid.add(JSONObject(snapshot).apply {getJSONObject("expected").put("language20_device_default","Төхөөрөмжийн хэлийг ашиглах")})
        assertEquals(14,invalid.size)
        for(row in invalid) {
            var rejected=false
            try {reviewedMongolianScriptRow(row)} catch (_:Exception) {rejected=true}
            assertTrue("Changed historical row must fail: $row",rejected)
        }
    }

    @Test fun everyExplicitScriptAndRegionalControlResolvesItsExpectedGeneralUiCatalogue() {
        val expected=javaClass.getResourceAsStream("/exact-script-resources/expected.json")!!
            .bufferedReader().use {JSONArray(it.readText())}
        assertEquals(28,expected.length())
        val keys=mapOf("ui_save" to R.string.ui_save,"ui_menu_file" to R.string.ui_menu_file,
            "language20_device_default" to R.string.language20_device_default)
        val observations=JSONArray();val failures=mutableListOf<String>()
        for(index in 0 until expected.length()) {
            val historical=expected.getJSONObject(index)
            val row=when(historical.getString("requested_tag")) {
                "uz-Latn" -> reviewedUzbekScriptRow(historical)
                "tt-Latn" -> reviewedTatarLatinScriptRow(historical)
                "tt-Cyrl" -> reviewedTatarScriptRow(historical)
                "mn-Cyrl-MN" -> reviewedMongolianScriptRow(historical)
                else -> historical
            }
            val tag=row.getString("requested_tag")
            AppLanguage.select(context,tag)
            val wrapped=AppLanguage.wrap(context)
            assertEquals(tag,AppLanguage.selectedTag(context))
            assertEquals(tag,context.getSharedPreferences("app-language",Context.MODE_PRIVATE)
                .getString("language-tag",null))
            if(Build.VERSION.SDK_INT>=33) assertEquals(tag,
                context.getSystemService(LocaleManager::class.java)!!.applicationLocales[0].toLanguageTag())
            assertEquals(tag,Locale.getDefault().toLanguageTag())
            assertEquals(row.getString("resource_tag"),wrapped.resources.configuration.locales[0].toLanguageTag())
            val actual=JSONObject()
            for((name,id) in keys) {
                val value=wrapped.getString(id);actual.put(name,value)
                if(value!=row.getJSONObject("expected").getString(name))
                    failures.add("$tag $name expected ${row.getJSONObject("expected").getString(name)} but was $value")
            }
            observations.put(JSONObject().put("requested_tag",tag)
                .put("persisted_tag",AppLanguage.selectedTag(context))
                .put("resource_tag",wrapped.resources.configuration.locales[0].toLanguageTag())
                .put("expected",row.getJSONObject("expected")).put("actual",actual))
        }
        val directory=File("build/reports/exact-script-resource-routing").apply {mkdirs()}
        File(directory,"api${RuntimeEnvironment.getApiLevel()}.json").writeText(observations.toString(2)+"\n")
        assertTrue(failures.joinToString("\n"),failures.isEmpty())
    }

    @Test fun mixedScriptPluralUsesTheWholeCatalogueAndKeepsFormatArguments() {
        AppLanguage.select(context,"ko-Kore-KR")
        val resources=AppLanguage.wrap(context).resources
        val expected="미리 보기: 12 × 34 px\n2개 이미지에 適用합니다. 配置된 이미지를 자르면 連結된 이미지의 位置도 조정될 수 있습니다."
        assertEquals(expected,resources.getQuantityString(R.plurals.ui_crop_preview_images,2,12,34,2))
        assertEquals("貯藏",resources.getString(R.string.ui_save))
        assertEquals("이미지 크레딧을 複寫할 수 없습니다.",resources.getString(R.string.commons_credit_copy_failed))
    }

    @Test @Config(sdk=[21,24,30,35])
    fun emojiEnglishKeepsPublicIdentityWholeStringsAndEnglishPluralsAcrossSwitches() {
        val controller=Robolectric.buildActivity(LocalizedTestActivity::class.java).setup()
        try {
            val activity=controller.get()
            // Repeated switches also guard against the private English mirror
            // winning ordinary English selection or retaining stale plural rules.
            for(tag in listOf("qaa-Zsye-XV","en-XV","en-001","en-AU","en-CA","en-GB",
                    "en-IN","en-SG","en-US","fr","qaa-Zsye-XV")) {
                AppLanguage.select(context,tag)
                val wrapped=AppLanguage.wrap(context)
                val changed=Configuration(activity.resources.configuration).apply {
                    fontScale=2f;screenWidthDp=640;screenHeightDp=320
                    orientation=Configuration.ORIENTATION_LANDSCAPE
                }
                AppLanguage.refresh(activity,changed)
                val emoji=tag=="qaa-Zsye-XV"
                val expectedTag=if(emoji) "en-Zsye-XV-anpaint" else tag
                assertEquals(tag,AppLanguage.selectedTag(context))
                assertEquals(tag,context.getSharedPreferences("app-language",Context.MODE_PRIVATE)
                    .getString("language-tag",null))
                assertEquals(tag,Locale.getDefault().toLanguageTag())
                if(Build.VERSION.SDK_INT>=33) assertEquals(tag,
                    context.getSystemService(LocaleManager::class.java)!!.applicationLocales.toLanguageTags())
                assertNotSame(context.resources,activity.resources)
                assertSame(activity.resources,PaintApplication.currentResources)
                @Suppress("DEPRECATION")
                val publicLocale=if(Build.VERSION.SDK_INT>=24) context.resources.configuration.locales[0]
                    else context.resources.configuration.locale
                assertEquals(tag,publicLocale.toLanguageTag())
                for(localized in listOf(wrapped,activity)) {
                    val resources=localized.resources
                    @Suppress("DEPRECATION")
                    val resourceLocale=if(Build.VERSION.SDK_INT>=24) resources.configuration.locales[0]
                        else resources.configuration.locale
                    assertEquals(expectedTag,resourceLocale.toLanguageTag())
                    val direction=when(tag) {
                        "qaa-Zsye-XV" -> TextDirection.VERTICAL_RL
                        "en-XV" -> TextDirection.VERTICAL_LR
                        else -> TextDirection.HORIZONTAL
                    }
                    assertEquals(direction,VerticalText.uiDirection(localized))
                    assertEquals(when {emoji -> "💾 Save";tag=="fr" -> "Enregistrer";else -> "Save"},
                        resources.getString(R.string.ui_save))
                    if(emoji) {
                        assertEquals("📁 File",resources.getString(R.string.ui_menu_file))
                        assertEquals("🌐 Use device language",resources.getString(R.string.language20_device_default))
                        for(count in 0..20) {
                            val noun=if(count==1) "image" else "images"
                            assertEquals("Emoji English count=$count",
                                "✅ Preview: 123 × 45 px\nApply to $count $noun. Cropping placed images may move their attached images.",
                                resources.getQuantityString(R.plurals.ui_crop_preview_images,count,123,45,count))
                        }
                    }
                }
                assertEquals(640,activity.resources.configuration.screenWidthDp)
                assertEquals(320,activity.resources.configuration.screenHeightDp)
                assertEquals(2f,activity.resources.configuration.fontScale,0f)
                assertEquals(Configuration.ORIENTATION_LANDSCAPE,activity.resources.configuration.orientation)
            }
        } finally {controller.pause().stop().destroy()}
    }

    @Test @Config(sdk=[35]) fun systemEmojiSelectionAndDeviceLabelKeepThePublicTag() {
        AppLanguage.select(context,"")
        val manager=context.getSystemService(LocaleManager::class.java)!!
        manager.applicationLocales=LocaleList.forLanguageTags("qaa-Zsye-XV")
        assertEquals("qaa-Zsye-XV",AppLanguage.selectedTag(context))
        assertEquals("💾 Save",AppLanguage.wrap(context).getString(R.string.ui_save))
        assertEquals("qaa-Zsye-XV",manager.applicationLocales.toLanguageTags())
        assertEquals("qaa-Zsye-XV",AppLanguage.locale(context).toLanguageTag())
        AppLanguage.select(context,"fr")
        assertEquals("🌐 Use device language",
            AppLanguage.deviceDefaultLabel(context,Locale.forLanguageTag("qaa-Zsye-XV")))
        assertEquals("fr",AppLanguage.selectedTag(context))
    }

    @Test fun russianCropPreviewKeepsCountsAndWarnsThatAttachedImagesMove() {
        AppLanguage.select(context,"ru")
        val resources=AppLanguage.wrap(context).resources
        // All reachable selections, including None (0), within the 20-image cap.
        for(count in 0..20) {
            val targets=when(count) {
                1 -> "Применить к 1 изображению."
                in 2..4 -> "Применить к $count изображениям."
                else -> "Изображений для обрезки: $count."
            }
            val expected="Предпросмотр: 123 × 45 px\n$targets " +
                "При обрезке размещённых изображений присоединённые к ним изображения могут переместиться."
            assertEquals("Russian selected count=$count",expected,
                resources.getQuantityString(R.plurals.ui_crop_preview_images,count,123,45,count))
        }
    }

    @Test fun refreshKeepsTheRequestedTagAndLiveConfigurationAcrossRepeatedSwitches() {
        val controller=Robolectric.buildActivity(LocalizedTestActivity::class.java).setup()
        try {
            val activity=controller.get()
            for((tag,save) in listOf("ko-Kore-KR" to "貯藏","ko-KR" to "저장",
                    "fr" to "Enregistrer","ko-Kore-KR" to "貯藏")) {
                AppLanguage.select(context,tag)
                val changed=Configuration(activity.resources.configuration).apply {
                    fontScale=2f;screenWidthDp=640;screenHeightDp=320
                    orientation=Configuration.ORIENTATION_LANDSCAPE
                }
                AppLanguage.refresh(activity,changed)
                assertNotSame(context.resources,activity.resources)
                assertEquals(tag,AppLanguage.selectedTag(activity))
                assertEquals(tag,Locale.getDefault().toLanguageTag())
                assertEquals(save,activity.getString(R.string.ui_save))
                assertEquals(640,activity.resources.configuration.screenWidthDp)
                assertEquals(320,activity.resources.configuration.screenHeightDp)
                assertEquals(2f,activity.resources.configuration.fontScale,0f)
                assertEquals(Configuration.ORIENTATION_LANDSCAPE,activity.resources.configuration.orientation)
            }
        } finally {controller.pause().stop().destroy()}
    }

    @Test @Config(sdk=[35]) fun systemAppLanguageKeepsThePublicMixedScriptTag() {
        AppLanguage.select(context,"")
        val manager=context.getSystemService(LocaleManager::class.java)!!
        manager.applicationLocales=LocaleList.forLanguageTags("ko-Kore-KR")
        assertEquals("ko-Kore-KR",AppLanguage.selectedTag(context))
        assertEquals("貯藏",AppLanguage.wrap(context).getString(R.string.ui_save))
        assertEquals("ko-Kore-KR",manager.applicationLocales[0].toLanguageTag())
        assertEquals("ko-Kore-KR",AppLanguage.locale(context).toLanguageTag())
    }

    @Test fun deviceDefaultLabelUsesTheExactCatalogueWithoutChangingTheSelection() {
        AppLanguage.select(context,"fr")
        assertEquals("시스템 言語 使用",
            AppLanguage.deviceDefaultLabel(context,Locale.forLanguageTag("ko-Kore-KR")))
        assertEquals("fr",AppLanguage.selectedTag(context))
        assertEquals("fr",context.getSharedPreferences("app-language",Context.MODE_PRIVATE)
            .getString("language-tag",null))
    }
}
