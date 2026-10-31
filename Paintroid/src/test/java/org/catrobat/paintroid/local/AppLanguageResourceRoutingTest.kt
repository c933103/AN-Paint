/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.LocaleManager
import android.content.Context
import android.content.res.Configuration
import android.os.Build
import android.os.LocaleList
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.ui
import org.catrobat.paintroid.classic.uiQuantity
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

    @Test @Config(sdk=[33])
    fun everyOfferedLanguageResolvesCompiledBoundariesWithoutPerStringActivities() {
        val contracts=listOf(
            R.string.ui_width_in to arrayOf<Any>("unit 100%"),
            R.string.formats22_at_least_frames to arrayOf<Any>(21001),
            R.string.formats22_animation_message to arrayOf<Any>("GIF", "21"),
            R.string.ui_d_d_px_d_pixels_2f_mp to arrayOf<Any>(640,480,307200L,0.3072))
        for(tag in AppLanguage.tags(context)) {
            val locale=AppLanguage.resourceLocale(Locale.forLanguageTag(tag))
            AppLanguage.select(context,tag)
            assertEquals(tag,AppLanguage.selectedTag(context))
            val resources=AppLanguage.wrap(context).resources
            assertEquals(tag,locale,resources.configuration.locales[0])
            // Independent of process-default language, with no Activity per value.
            Locale.setDefault(Locale.US)
            PaintApplication.currentResources=resources
            assertTrue(tag,resources.getString(R.string.ui_save).isNotEmpty())
            for((id,args) in contracts) {
                val template=resources.getString(id)
                assertEquals("$tag/${resources.getResourceEntryName(id)}",
                    String.format(locale,template,*args),ui(id,*args))
            }
            for(count in listOf(0,1,2,3,21,101)) {
                val template=resources.getQuantityString(R.plurals.ui_crop_preview_images,count)
                assertEquals("$tag/crop/$count",String.format(locale,template,24,16,count),
                    uiQuantity(resources,R.plurals.ui_crop_preview_images,count,24,16,count))
            }
        }
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

    @Test fun everyExplicitScriptAndRegionalControlResolvesItsExpectedGeneralUiCatalogue() {
        val expected=javaClass.getResourceAsStream("/exact-script-resources/expected.json")!!
            .bufferedReader().use {JSONArray(it.readText())}
        assertEquals(28,expected.length())
        val keys=mapOf("ui_save" to R.string.ui_save,"ui_menu_file" to R.string.ui_menu_file,
            "language20_device_default" to R.string.language20_device_default)
        val observations=JSONArray();val failures=mutableListOf<String>()
        for(index in 0 until expected.length()) {
            val row=expected.getJSONObject(index)
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
                // Device-language captions are approval history, not script-routing boundaries.
                val retiredCaption=name=="language20_device_default" && tag in setOf("tt-Latn","tt-Cyrl","uz-Latn","mn-Cyrl-MN")
                if(!retiredCaption && value!=row.getJSONObject("expected").getString(name))
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
