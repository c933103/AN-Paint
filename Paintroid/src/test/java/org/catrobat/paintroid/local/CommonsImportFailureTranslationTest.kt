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

/** Exact new resources and declared fallback through the real language picker, on API30 and API35. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
class CommonsImportFailureTranslationTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val keys=mapOf(
        "commons_metadata_not_file_page" to R.string.commons_metadata_not_file_page,
        "commons_metadata_ambiguous_file" to R.string.commons_metadata_ambiguous_file,
        "commons_metadata_unavailable" to R.string.commons_metadata_unavailable,
        "commons_metadata_original_mismatch" to R.string.commons_metadata_original_mismatch,
        "commons_metadata_invalid_page" to R.string.commons_metadata_invalid_page,
        "commons_metadata_field_too_large" to R.string.commons_metadata_field_too_large,
        "commons_metadata_cache_failed" to R.string.commons_metadata_cache_failed,
        "commons_download_original_mismatch" to R.string.commons_download_original_mismatch,
        "commons_svg_png_encode_failed" to R.string.commons_svg_png_encode_failed)
    private val fixture get()=org.json.JSONObject(java.io.File("../tools/fixtures/current_localization/commons_import_failures_current_wording.json").readText()).getJSONObject("values")
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
    @Test fun allOfferedTagsResolveTheirRecordedCompleteValueOrEnglishFallback() {
        val values=fixture
        assertEquals(keys.keys,values.keys().asSequence().toSet())
        assertEquals(171,AppLanguage.tags(context).size)
        for(tag in AppLanguage.tags(context)) {
            val resources=resourcesFor(tag)
            for((key,id) in keys) {
                val words=values.getJSONObject(key)
                val raw=if(words.has(tag)) words.getString(tag) else words.getString("default")
                val expected=raw.replace("\\'","'").replace("\\\"","\"")
                assertEquals("$tag/$key",expected,resources.getString(id))
                assertTrue("Whole application reason must be available",expected.isNotBlank())
            }
        }
    }
    @Test fun mixedScriptKoreanKeepsItsExactPublicAndPrivateResourceIdentity() {
        for(tag in listOf("ko-KR","ko-Kore-KR")) {
            val resources=resourcesFor(tag)
            val expectedTag=if(tag=="ko-KR") tag else "ko-Kore-KR-anpaint"
            assertEquals(expectedTag,resources.configuration.locales[0].toLanguageTag())
            for((key,id) in keys) {
                val values=fixture.getJSONObject(key)
                assertEquals(values.optString(tag,values.getString("default")).replace("\\'","'"),resources.getString(id))
            }
        }
    }
}
