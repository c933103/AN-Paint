/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.LocaleManager
import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.os.Looper
import android.view.View
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.EditText
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.IllustrationSource
import org.catrobat.paintroid.classic.MediaGalleryActivity
import org.catrobat.paintroid.classic.PaintApplication
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.mockito.Mockito
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.LooperMode
import org.robolectric.util.ReflectionHelpers
import java.io.File
import java.util.Locale

/** Real Terms clicks and production WebView callbacks; offline Robolectric, not browser/provider execution. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class GalleryExternalLinkTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val terms=mapOf(
        IllustrationSource.CATROBAT to "https://developer.catrobat.org/pages/legal/licenses/catrobat/",
        IllustrationSource.IRASUTOYA to "https://www.irasutoya.com/p/terms.html",
        IllustrationSource.OPENCLIPART to "https://openclipart.org/share",
        IllustrationSource.COMMONS to "https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia"
    )
    private fun status(activity: MediaGalleryActivity)=activity.window.decorView.findViewWithTag<TextView>("gallery_status")
    private fun web(activity: MediaGalleryActivity)=ReflectionHelpers.getField<WebView>(activity,"web")
    private fun clickTerms(activity: MediaGalleryActivity) {
        assertTrue(activity.window.decorView.findViewWithTag<View>("gallery_terms").performClick())
        shadowOf(Looper.getMainLooper()).idle()
    }
    private fun assertViewIntent(intent: Intent,expected: String) {
        assertEquals(Intent.ACTION_VIEW,intent.action)
        assertEquals(expected,intent.dataString)
        assertNull(intent.component)
        assertNull(intent.`package`)
        assertEquals(0,intent.flags)
    }
    private fun assertGalleryRetained(activity: MediaGalleryActivity,provider: IllustrationSource) {
        assertEquals(provider.home,shadowOf(web(activity)).lastLoadedUrl)
        assertEquals("retained query",activity.window.decorView.findViewWithTag<EditText>("gallery_search").text.toString())
        assertFalse(activity.downloading)
        assertFalse(activity.isFinishing)
        assertFalse(activity.isDestroyed)
    }

    @Test fun everyPickerLocaleResolvesItsCompleteMessageOrExplicitEnglishFallback()=withLanguageState {
        val fixture=JSONObject(File("../tools/fixtures/current_localization/gallery_external_link_current_wording.json").readText())
        val expected=fixture.getJSONObject("values").getJSONObject("gallery_external_link_no_handler")
        val scope=JSONObject(File("../tools/fixtures/current_localization/locale_contract_scope.json").readText())
        val fallback=scope.getJSONArray("fallback_tags").let { array ->
            (0 until array.length()).map { array.getString(it) }.toSet()
        }
        for(tag in AppLanguage.tags(context)) {
            AppLanguage.select(context,tag)
            val selected=AppLanguage.wrap(context)
            val raw=if(expected.has(tag)) expected.getString(tag) else expected.getString("default")
            val message=raw.replace("\\'", "'").replace("\\\"", "\"")
            assertEquals("Whole compiled message for $tag",message,selected.getString(R.string.gallery_external_link_no_handler))
        }
    }

    @Test fun missingHandlerFromActualTermsClickShowsLinkExplanationForEveryProvider() {
        for(tag in listOf("en-001","fr","ja")) for((provider,url) in terms) withGallery(provider,tag) { activity ->
            val attempted=mutableListOf<Intent>()
            activity.launchExternalActivity={intent ->attempted.add(intent);throw ActivityNotFoundException("fixture: no handler")}
            clickTerms(activity)
            assertEquals(1,attempted.size)
            assertViewIntent(attempted.single(),url)
            assertEquals(View.VISIBLE,status(activity).visibility)
            assertEquals(activity.getString(R.string.gallery_external_link_no_handler),status(activity).text.toString())
            assertNotEquals(activity.getString(R.string.ui_the_online_gallery_could_not_be_loaded_check),status(activity).text.toString())
            assertNull(shadowOf(activity).nextStartedActivity)
            assertGalleryRetained(activity,provider)
            // A repeated user attempt keeps the correct diagnostic without starting a download.
            clickTerms(activity)
            assertEquals(2,attempted.size)
            assertEquals(activity.getString(R.string.gallery_external_link_no_handler),status(activity).text.toString())
            assertGalleryRetained(activity,provider)
        }
    }

    @Test fun successfulTermsClickUsesDefaultAndroidLaunchAndKeepsGalleryState() {
        for((provider,url) in terms) withGallery(provider) { activity ->
            assertEquals(View.GONE,status(activity).visibility)
            // Do not replace the seam: exercise its production startActivity implementation.
            clickTerms(activity)
            assertViewIntent(checkNotNull(shadowOf(activity).nextStartedActivity),url)
            assertNull(shadowOf(activity).nextStartedActivity)
            assertEquals(View.GONE,status(activity).visibility)
            assertGalleryRetained(activity,provider)
        }
    }

    @Test fun actualGalleryMainFrameFailureRetainsNetworkMessageAndSubresourceErrorsDoNotReplaceIt() {
        for(tag in listOf("en-001","fr","ja")) withGallery(IllustrationSource.COMMONS,tag) { activity ->
            val browser=web(activity)
            val client=shadowOf(browser).webViewClient
            client.onReceivedError(browser,request(IllustrationSource.COMMONS.home,false),networkError())
            assertEquals(View.GONE,status(activity).visibility)
            activity.launchExternalActivity={throw ActivityNotFoundException("fixture: no handler")}
            clickTerms(activity)
            val linkMessage=status(activity).text.toString()
            client.onReceivedError(browser,request(IllustrationSource.COMMONS.home,false),networkError())
            assertEquals(linkMessage,status(activity).text.toString())
            client.onReceivedError(browser,request(IllustrationSource.COMMONS.home,true),networkError())
            assertEquals(View.VISIBLE,status(activity).visibility)
            val galleryMessage=activity.getString(R.string.ui_the_online_gallery_could_not_be_loaded_check)
            assertEquals(galleryMessage,status(activity).text.toString())
            assertNotEquals(linkMessage,galleryMessage)
            // Opening Terms does not claim to repair an earlier real gallery load failure.
            activity.launchExternalActivity={activity.startActivity(it)}
            clickTerms(activity)
            assertViewIntent(checkNotNull(shadowOf(activity).nextStartedActivity),terms.getValue(IllustrationSource.COMMONS))
            assertEquals(galleryMessage,status(activity).text.toString())
            assertGalleryRetained(activity,IllustrationSource.COMMONS)
        }
    }

    @Test fun externalHttpsNavigationUsesSameExplanationWithoutChangingNavigationPolicy() {
        withGallery(IllustrationSource.COMMONS) { activity ->
            val browser=web(activity)
            val client=shadowOf(browser).webViewClient
            val attempted=mutableListOf<Intent>()
            activity.launchExternalActivity={intent ->attempted.add(intent);throw ActivityNotFoundException("fixture: no handler")}
            assertFalse(client.shouldOverrideUrlLoading(browser,IllustrationSource.COMMONS.home))
            for(url in listOf("http://example.invalid/terms","file:///terms","javascript:alert(1)","intent://terms"))
                assertTrue(client.shouldOverrideUrlLoading(browser,url))
            assertTrue(attempted.isEmpty())
            assertEquals(View.GONE,status(activity).visibility)
            val external="https://example.invalid/terms"
            assertTrue(client.shouldOverrideUrlLoading(browser,external))
            assertViewIntent(attempted.single(),external)
            assertEquals(activity.getString(R.string.gallery_external_link_no_handler),status(activity).text.toString())
            assertGalleryRetained(activity,IllustrationSource.COMMONS)
        }
    }

    @Test fun unrelatedSecurityExceptionIsNotMisclassifiedAsMissingHandler() {
        withGallery(IllustrationSource.CATROBAT) { activity ->
            val failure=SecurityException("fixture: separate permission failure")
            activity.launchExternalActivity={throw failure}
            try {
                clickTerms(activity)
                fail("SecurityException must remain outside this bounded missing-handler mapping")
            } catch(actual: SecurityException) {assertSame(failure,actual)}
            assertEquals(View.GONE,status(activity).visibility)
            assertGalleryRetained(activity,IllustrationSource.CATROBAT)
        }
    }

    private fun request(url: String,mainFrame: Boolean)=object: WebResourceRequest {
        override fun getUrl()=Uri.parse(url)
        override fun isForMainFrame()=mainFrame
        override fun isRedirect()=false
        override fun hasGesture()=false
        override fun getMethod()="GET"
        override fun getRequestHeaders(): MutableMap<String,String> = mutableMapOf()
    }
    // WebResourceError is abstract and its constructor is not public in the Android SDK.
    private fun networkError(): WebResourceError=Mockito.mock(WebResourceError::class.java).apply {
        Mockito.`when`(errorCode).thenReturn(WebViewClient.ERROR_CONNECT)
        Mockito.`when`(description).thenReturn("fixture: connection failed")
    }

    private fun withGallery(provider: IllustrationSource,tag: String="en-001",check: (MediaGalleryActivity)->Unit)=withLanguageState {
        AppLanguage.select(context,tag)
        PaintApplication.currentResources=AppLanguage.wrap(context).resources
        val controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,
            Intent(context,MediaGalleryActivity::class.java).putExtra("gallery_provider",provider.name))
        try {
            val activity=controller.setup().visible().get()
            activity.window.decorView.findViewWithTag<EditText>("gallery_search").setText("retained query")
            activity.openConnection={throw AssertionError("External link tests must not download gallery images")}
            check(activity)
        } finally {
            if(!controller.get().isDestroyed) controller.pause().stop().destroy()
            shadowOf(Looper.getMainLooper()).idle()
        }
    }

    private fun withLanguageState(check: ()->Unit) {
        val preferences=context.getSharedPreferences("app-language",Context.MODE_PRIVATE)
        val oldTag=preferences.getString("language-tag",null)
        val oldInitialized=if(preferences.contains("platform-initialized")) preferences.getBoolean("platform-initialized",false) else null
        val manager=if(Build.VERSION.SDK_INT>=33) context.getSystemService(LocaleManager::class.java) else null
        val oldPlatform=manager?.applicationLocales
        val oldLocale=Locale.getDefault()
        val oldResources=PaintApplication.currentResources
        try {check()
        } finally {
            if(manager!=null) manager.applicationLocales=oldPlatform!!
            preferences.edit().apply {
                if(oldTag==null) remove("language-tag") else putString("language-tag",oldTag)
                if(oldInitialized==null) remove("platform-initialized") else putBoolean("platform-initialized",oldInitialized)
            }.commit()
            PaintApplication.currentResources=oldResources
            Locale.setDefault(oldLocale)
        }
    }
}
