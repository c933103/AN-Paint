/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.LocaleManager
import android.content.Context
import android.content.res.Configuration
import android.os.Build
import android.os.LocaleList
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.PaintApplication
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

    @Test fun onlyTheCollidingPublicTagUsesAnInternalResourceVariant() {
        for(tag in AppLanguage.tags(context)) {
            val chosen=Locale.forLanguageTag(tag)
            val expected=if(tag=="ko-Kore-KR") "ko-Kore-KR-anpaint" else tag
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

    @Test fun everyExplicitScriptAndRegionalControlResolvesItsExpectedGeneralUiCatalogue() {
        val expected=javaClass.getResourceAsStream("/exact-script-resources/expected.json")!!
            .bufferedReader().use {JSONArray(it.readText())}
        assertEquals(28,expected.length())
        val keys=mapOf("ui_save" to R.string.ui_save,"ui_menu_file" to R.string.ui_menu_file,
            "language20_device_default" to R.string.language20_device_default)
        val observations=JSONArray();val failures=mutableListOf<String>()
        for(index in 0 until expected.length()) {
            val row=expected.getJSONObject(index);val tag=row.getString("requested_tag")
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
        val expected="미리 보기: 12 × 34 px\n2개 이미지에 適用합니다. 配置된 이미지를 자르면 連結된 이미지의 位置도 조정됩니다."
        assertEquals(expected,resources.getQuantityString(R.plurals.ui_crop_preview_images,2,12,34,2))
        assertEquals("貯藏",resources.getString(R.string.ui_save))
        assertEquals("이미지 크레딧을 複寫할 수 없습니다.",resources.getString(R.string.commons_credit_copy_failed))
    }

    @Test fun refreshKeepsTheRequestedTagAndLiveConfigurationAcrossRepeatedSwitches() {
        val controller=Robolectric.buildActivity(Activity::class.java).setup()
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
