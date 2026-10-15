/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.LocaleManager
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.net.Uri
import android.os.Build
import android.os.Looper
import android.view.View
import android.webkit.WebView
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.IllustrationPage
import org.catrobat.paintroid.classic.IllustrationSource
import org.catrobat.paintroid.classic.MediaGalleryActivity
import org.catrobat.paintroid.classic.PaintApplication
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.LooperMode
import org.robolectric.util.ReflectionHelpers
import java.io.ByteArrayInputStream
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.InputStream
import java.net.HttpURLConnection
import java.net.URL
import java.util.Locale
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

/** Actual selection/download/status path; only transport responses are substituted, with no live requests. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class GalleryRedirectTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val catrobat="https://catrobat.org/wp-content/uploads/2025/01/Needle_Yellow.png"
    private val commons="https://upload.wikimedia.org/wikipedia/commons/a/a1/Example.png"
    private val messageId=R.string.ui_the_gallery_redirected_outside_its_supported_hosts
    private val wording by lazy {JSONObject(File("../tools/fixtures/current_localization/gallery_redirect_current_wording.json").readText())
        .getJSONObject("values").getJSONObject("ui_the_gallery_redirected_outside_its_supported_hosts")}
    private fun status(activity: MediaGalleryActivity)=activity.window.decorView.findViewWithTag<TextView>("gallery_status")
    private fun await(done: ()->Boolean) {
        val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(10)
        while(!done() && System.nanoTime()<deadline) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(5)}
        shadowOf(Looper.getMainLooper()).idle()
        assertTrue("Background operation timed out",done())
    }
    private class Connection(url: URL,private val code: Int=200,private val location: String?=null,
        private val stream: InputStream=ByteArrayInputStream(byteArrayOf())): HttpURLConnection(url) {
        @Volatile var disconnected=false
        @Volatile var streamOpened=false
        override fun connect()=Unit
        override fun disconnect() {disconnected=true;stream.close()}
        override fun usingProxy()=false
        override fun getResponseCode()=code
        override fun getInputStream(): InputStream {streamOpened=true;return stream}
        override fun getHeaderField(name: String): String?=if(name=="Location") location else null
    }
    private fun imageBytes(): ByteArray {
        val bitmap=Bitmap.createBitmap(3,2,Bitmap.Config.ARGB_8888)
        return try {ByteArrayOutputStream().also {assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))}.toByteArray()}
        finally {bitmap.recycle()}
    }
    private fun select(activity: MediaGalleryActivity,source: String=catrobat) {
        val web=ReflectionHelpers.getField<WebView>(activity,"web")
        val action=Uri.Builder().scheme(IllustrationPage.USE_SCHEME).authority("insert")
            .appendQueryParameter("source",source)
            .appendQueryParameter("page",if(source==commons) "https://commons.wikimedia.org/wiki/File:Example.png" else IllustrationSource.CATROBAT.home)
            .appendQueryParameter("title","Controlled redirect fixture").build()
        assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,action.toString()))
    }
    private fun assertRejected(activity: MediaGalleryActivity,expectedReason: String) {
        assertFalse(activity.downloading)
        assertFalse(activity.isFinishing)
        assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
        assertNull(shadowOf(activity).resultIntent)
        assertEquals(View.VISIBLE,status(activity).visibility)
        assertEquals(activity.getString(R.string.ui_could_not_load_gallery_image,expectedReason),status(activity).text.toString())
    }
    private fun withGallery(provider: IllustrationSource=IllustrationSource.CATROBAT,tag: String="en-001",check: (MediaGalleryActivity)->Unit)=withLanguageState {
        AppLanguage.select(context,tag)
        PaintApplication.currentResources=AppLanguage.wrap(context).resources
        val controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,
            Intent(context,MediaGalleryActivity::class.java).putExtra("gallery_provider",provider.name))
        val before=context.cacheDir.listFiles().orEmpty().filter {it.name.startsWith("gallery-")}.map {it.name}.toSet()
        try {
            val activity=controller.setup().visible().get()
            activity.openConnection={throw AssertionError("Unconfigured transport must never contact a provider")}
            check(activity)
        } finally {
            val activity=controller.get()
            if(!activity.isDestroyed) controller.pause().stop().destroy()
            await {!activity.downloading}
            val created=context.cacheDir.listFiles().orEmpty().filter {it.name.startsWith("gallery-") && it.name !in before}
            // A successful caller explicitly consumes/deletes its handed-back file; failures must leave none.
            try {assertTrue("Redirect fixture left temporary files: ${created.map {it.name}}",created.isEmpty())}
            finally {created.forEach {it.delete()}}
        }
    }
    private fun rejectedRedirect(target: String,provider: IllustrationSource=IllustrationSource.COMMONS,tag: String="en-001")=withGallery(provider,tag) {activity ->
        val source=if(provider==IllustrationSource.COMMONS) commons else catrobat
        assertTrue(provider.allowsDownload(Uri.parse(source)))
        assertFalse(provider.allowsDownload(Uri.parse(target)))
        val redirect=Connection(URL(source),302,target)
        val opened=mutableListOf<String>()
        activity.openConnection={url ->opened.add(url.toString());redirect}
        select(activity,source);await {!activity.downloading}
        assertEquals(listOf(source),opened)
        assertTrue(redirect.disconnected);assertFalse(redirect.streamOpened)
        assertRejected(activity,wording.getString(tag))
        assertFalse(status(activity).text.toString().contains("fixture-query-value"))
        assertFalse(status(activity).text.toString().contains(target))
    }

    @Test fun sameHostUnsupportedPathUsesNeutralReasonInEnglishFrenchAndJapanese() {
        for(tag in listOf("en-001","fr","ja")) {
            for(path in listOf("thumb/a/a1/Example.png/320px-Example.png","archive/a/a1/Example.png"))
                rejectedRedirect("https://upload.wikimedia.org/wikipedia/commons/$path?token=fixture-query-value",tag=tag)
        }
    }
    @Test fun offHostRedirectUsesTheSameAccuratePolicyReason() =
        rejectedRedirect("https://unrelated.example/Example.png?token=fixture-query-value")
    @Test fun insecureSchemeIsRejectedBeforeOpeningTheTarget() =
        rejectedRedirect(commons.replace("https:","http:")+"?token=fixture-query-value")
    @Test fun unsupportedPortIsRejectedBeforeOpeningTheTarget() =
        rejectedRedirect(commons.replace("upload.wikimedia.org","upload.wikimedia.org:8443"))
    @Test fun userInfoIsRejectedBeforeOpeningTheTarget() =
        rejectedRedirect(commons.replace("upload.wikimedia.org","fixture-user@upload.wikimedia.org"))
    @Test fun unsupportedExtensionIsRejectedBeforeOpeningTheTarget() =
        rejectedRedirect(commons.replace("Example.png","Example.html"))

    @Test fun rejectedRedirectCanBeRetriedAndAllowedRelativeRedirectReturnsTheOriginalSource()=withGallery {activity ->
        val rejected=Connection(URL(catrobat),302,"https://unrelated.example/image.png")
        activity.openConnection={rejected};select(activity);await {!activity.downloading}
        assertRejected(activity,"The gallery redirected to an unsupported image URL.")
        val target=URL(URL(catrobat),"other.png")
        val redirect=Connection(URL(catrobat),302,"other.png")
        val image=Connection(target,stream=ByteArrayInputStream(imageBytes()))
        val opened=mutableListOf<String>()
        activity.openConnection={url ->opened.add(url.toString());if(opened.size==1) redirect else image}
        select(activity);await {!activity.downloading}
        assertEquals(listOf(catrobat,target.toString()),opened)
        assertFalse(redirect.instanceFollowRedirects);assertFalse(image.instanceFollowRedirects)
        assertTrue(redirect.disconnected);assertTrue(image.disconnected);assertTrue(image.streamOpened)
        assertEquals(Activity.RESULT_OK,shadowOf(activity).resultCode);assertTrue(activity.isFinishing)
        val result=shadowOf(activity).resultIntent
        assertEquals(catrobat,result.getStringExtra("gallery_source"))
        val file=File(activity.cacheDir,result.getStringExtra("gallery_file")!!)
        try {assertTrue(file.isFile);assertTrue(file.length()>0)} finally {file.delete()}
    }
    @Test fun fiveRedirectsAreAllowedButTheSixthCannotOpenAnotherConnection() {
        for(redirects in listOf(5,6)) withGallery {activity ->
            val connections=mutableListOf<Connection>()
            activity.openConnection={url ->
                Connection(url,if(connections.size<redirects) 302 else 200,
                    if(connections.size<redirects) "next-${connections.size}.png" else null,
                    ByteArrayInputStream(imageBytes())).also {connections.add(it)}
            }
            select(activity);await {!activity.downloading}
            assertEquals(6,connections.size)
            assertTrue(connections.all {it.disconnected && !it.instanceFollowRedirects})
            if(redirects==5) {
                assertEquals(Activity.RESULT_OK,shadowOf(activity).resultCode)
                assertTrue(connections.last().streamOpened)
                File(activity.cacheDir,shadowOf(activity).resultIntent.getStringExtra("gallery_file")!!).delete()
            } else {
                assertRejected(activity,activity.getString(R.string.ui_too_many_gallery_redirects))
                assertTrue(connections.none {it.streamOpened})
            }
        }
    }
    @Test fun closingAfterAnAllowedRedirectCleansItsDownloadAndCannotReturnAnImage()=withGallery {activity ->
        val started=CountDownLatch(1);val release=CountDownLatch(1)
        val stream=object: ByteArrayInputStream(imageBytes()) {
            override fun read(buffer: ByteArray,offset: Int,length: Int): Int {
                started.countDown();release.await() // The test always releases this gate in finally.
                return super.read(buffer,offset,length)
            }
        }
        val redirect=Connection(URL(catrobat),302,"other.png")
        val image=Connection(URL(URL(catrobat),"other.png"),stream=stream)
        var calls=0
        activity.openConnection={if(++calls==1) redirect else image}
        try {
            select(activity);assertTrue(started.await(5,TimeUnit.SECONDS))
            activity.finish()
        } finally {release.countDown()}
        await {!activity.downloading}
        assertEquals(2,calls);assertTrue(redirect.disconnected);assertTrue(image.disconnected)
        assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
        assertNull(shadowOf(activity).resultIntent)
    }
    @Test fun everyPickerLocaleResolvesItsCompleteMessageOrExplicitEnglishFallback()=withLanguageState {
        val fixture=JSONObject(File("../tools/fixtures/current_localization/gallery_redirect_current_wording.json").readText())
        val expected=fixture.getJSONObject("values").getJSONObject("ui_the_gallery_redirected_outside_its_supported_hosts")
        val scope=JSONObject(File("../tools/fixtures/current_localization/locale_contract_scope.json").readText())
        val fallback=scope.getJSONArray("fallback_tags").let {array ->(0 until array.length()).map {array.getString(it)}.toSet()}
        for(tag in AppLanguage.tags(context)) {
            AppLanguage.select(context,tag)
            val raw=if(tag in fallback) expected.getString("default") else expected.getString(tag)
            assertEquals("Whole compiled redirect message for $tag",raw.replace("\\'", "'").replace("\\\"", "\""),
                AppLanguage.wrap(context).getString(messageId))
        }
    }
    private fun withLanguageState(check: ()->Unit) {
        val preferences=context.getSharedPreferences("app-language",Context.MODE_PRIVATE)
        val oldTag=preferences.getString("language-tag",null)
        val oldInitialized=if(preferences.contains("platform-initialized")) preferences.getBoolean("platform-initialized",false) else null
        val manager=if(Build.VERSION.SDK_INT>=33) context.getSystemService(LocaleManager::class.java) else null
        val oldPlatform=manager?.applicationLocales
        val oldLocale=Locale.getDefault();val oldResources=PaintApplication.currentResources
        try {check()} finally {
            if(manager!=null) manager.applicationLocales=oldPlatform!!
            preferences.edit().apply {
                if(oldTag==null) remove("language-tag") else putString("language-tag",oldTag)
                if(oldInitialized==null) remove("platform-initialized") else putBoolean("platform-initialized",oldInitialized)
            }.commit()
            PaintApplication.currentResources=oldResources;Locale.setDefault(oldLocale)
        }
    }
}
