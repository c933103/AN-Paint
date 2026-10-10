/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.LocaleManager
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.Looper
import android.net.Uri
import android.view.View
import android.webkit.WebView
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.LooperMode
import org.robolectric.shadows.ShadowToast
import org.robolectric.util.ReflectionHelpers
import java.io.ByteArrayInputStream
import java.io.IOException
import java.io.InputStream
import java.net.HttpURLConnection
import java.net.URL
import java.util.Collections
import java.util.Locale
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

/** Real WebView Copy credit route; fixture connections only, no provider requests. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[35],qualifiers="w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class CommonsCopyCreditErrorTest {
    private lateinit var activeController: ActivityController<MediaGalleryActivity>
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val source="https://upload.wikimedia.org/wikipedia/commons/a/ab/Test_map.svg"
    private val page="https://commons.wikimedia.org/wiki/File:Test_map.svg"
    private val existing=ImageCredit(source,"Edited credit · Émilie · かな\nhttps://example.org/credit · CC BY-SA 3.0")
    private val clipboard get()=context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
    private fun clipboardText()=clipboard.primaryClip?.getItemAt(0)?.text?.toString()
    private fun status(activity: MediaGalleryActivity)=activity.window.decorView.findViewWithTag<TextView>("gallery_status")
    private fun session(activity: MediaGalleryActivity)=ReflectionHelpers.getField<CreditEditSession>(activity,"creditSession")
    private class Connection(url: URL,private val input: InputStream,private val code: Int=200): HttpURLConnection(url) {
        var disconnected=false
        override fun connect()=Unit
        override fun disconnect() {disconnected=true;input.close()}
        override fun usingProxy()=false
        override fun getResponseCode()=code
        override fun getInputStream()=input
    }
    private fun response(url: URL,body: String=CommonsTestMetadata.response(source,page),code: Int=200)=
        Connection(url,ByteArrayInputStream(body.toByteArray()),code)
    private fun select(activity: MediaGalleryActivity) {
        val web=ReflectionHelpers.getField<WebView>(activity,"web")
        val action=Uri.Builder().scheme(GalleryPage.CREDIT_SCHEME).authority("copy")
            .appendQueryParameter("source",source).appendQueryParameter("page",page).build()
        assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,action.toString()))
    }
    private fun await(done: ()->Boolean) {
        val limit=System.nanoTime()+TimeUnit.SECONDS.toNanos(12)
        while(!done() && System.nanoTime()<limit) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(5)}
        shadowOf(Looper.getMainLooper()).idle();assertTrue("Copy-credit operation timed out",done())
    }
    private fun withGallery(tag: String="en-GB",run: (MediaGalleryActivity)->Unit) {
        val preferences=context.getSharedPreferences("app-language",Context.MODE_PRIVATE)
        val oldTag=preferences.getString("language-tag",null)
        val oldInitialized=if(preferences.contains("platform-initialized")) preferences.getBoolean("platform-initialized",false) else null
        val manager=if(Build.VERSION.SDK_INT>=33) context.getSystemService(LocaleManager::class.java) else null
        val oldPlatform=manager?.applicationLocales
        val oldLocale=Locale.getDefault();val oldResources=PaintApplication.currentResources
        val oldPublish=GalleryCredits.publishClipboard
        try {
            AppLanguage.select(context,tag);PaintApplication.currentResources=AppLanguage.wrap(context).resources
            clipboard.setPrimaryClip(ClipData.newPlainText("fixture","Previous clipboard"));ShadowToast.reset()
            val controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,
                Intent(context,MediaGalleryActivity::class.java).putExtra("gallery_provider",IllustrationSource.COMMONS.name)
                    .putExtra("document_image_credits",ImageCredit.write(listOf(existing)).toString())).setup().visible()
            activeController=controller
            try {run(controller.get())}
            finally {if(!controller.get().isDestroyed) controller.pause().stop().destroy();shadowOf(Looper.getMainLooper()).idle()}
        } finally {
            GalleryCredits.publishClipboard=oldPublish
            if(oldPlatform!=null) manager?.applicationLocales=oldPlatform
            preferences.edit().apply {
                if(oldTag==null) remove("language-tag") else putString("language-tag",oldTag)
                if(oldInitialized==null) remove("platform-initialized") else putBoolean("platform-initialized",oldInitialized)
            }.commit()
            PaintApplication.currentResources=oldResources;Locale.setDefault(oldLocale);ShadowToast.reset()
        }
    }
    private fun unchanged(activity: MediaGalleryActivity,requests: List<URL>,filesBefore: Set<String>) {
        assertTrue("Only the Commons metadata API may be requested",requests.all {it.host=="commons.wikimedia.org" && it.path=="/w/api.php"})
        assertEquals(listOf(existing),session(activity).credits)
        assertFalse(session(activity).accepted);assertNull(session(activity).draft)
        assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
        assertFalse(activity.isFinishing)
        assertEquals(filesBefore,activity.cacheDir.listFiles().orEmpty().filter {it.name.startsWith("gallery-")}.map {it.name}.toSet())
    }
    private fun files(activity: MediaGalleryActivity)=activity.cacheDir.listFiles().orEmpty()
        .filter {it.name.startsWith("gallery-")}.map {it.name}.toSet()
    private fun checkFailure(tag: String="en-GB",expected: (MediaGalleryActivity)->String,
        open: (URL)->HttpURLConnection) = withGallery(tag) {activity ->
        val requests=Collections.synchronizedList(mutableListOf<URL>());val before=files(activity)
        activity.openConnection={url ->requests.add(url);open(url)}
        select(activity);await {!activity.downloading}
        assertEquals(1,requests.size)
        assertEquals(View.VISIBLE,status(activity).visibility)
        assertEquals(expected(activity),status(activity).text.toString())
        assertEquals(expected(activity),status(activity).createAccessibilityNodeInfo().text.toString())
        assertEquals("Previous clipboard",clipboardText())
        unchanged(activity,requests,before)
        // The same action can recover after a failed metadata request.
        activity.openConnection={url ->requests.add(url);response(url)}
        select(activity);await {!activity.downloading}
        assertEquals(2,requests.size);assertEquals(View.GONE,status(activity).visibility)
        val copied=clipboardText()!!
        for(value in listOf("Mapper A","Mapper B","by-sa/3.0/",source,page)) assertTrue(value,copied.contains(value))
        assertFalse(copied.contains("antiAlias=false"));assertFalse(copied.contains("background=#FFFFFF"))
        assertEquals(CommonsAttribution.cached(activity,source)!!.text(false),copied)
        unchanged(activity,requests,before)
    }
    @Test fun httpFailureNamesCopyCreditAndDisconnectsWithoutFetchingAnImage() {
        var connection: Connection?=null
        checkFailure(expected={it.getString(R.string.commons_credit_copy_failed_reason,"Commons metadata: HTTP 503")}) {
            response(it,code=503).also {value ->connection=value}
        }
        assertTrue(connection!!.disconnected)
    }
    @Test fun providerAndFrameworkDetailIsInsertedVerbatimOnce() {
        val reason="  Provider quota 50%: %1\$s · détails\nTry again.  "
        checkFailure("fr",{it.getString(R.string.commons_credit_copy_failed_reason,reason)}) {throw IOException(reason)}
    }
    @Test fun missingEmptyAndWhitespaceOnlyReasonsUseReasonlessCreditMessage() {
        for(reason in listOf(null,""," \n\t")) checkFailure(expected={it.getString(R.string.commons_credit_copy_failed)}) {throw IOException(reason)}
    }
    @Test fun metadataQueryAndValidationFailuresKeepTheirExistingReasons() {
        val cases=listOf(
            "{\"error\":{\"code\":\"fixture\"}}" to "Commons metadata query failed",
            "{\"query\":{\"pages\":[]}}" to "Commons metadata returned an ambiguous file",
            "{\"query\":{\"pages\":[{\"ns\":6,\"missing\":true}]}}" to "Commons file metadata is unavailable",
            CommonsTestMetadata.response("https://upload.wikimedia.org/wikipedia/commons/a/ab/Other.svg",page) to "Commons attribution does not match the selected original file",
            CommonsTestMetadata.response(source,"https://example.org/not-commons") to "Invalid Commons attribution page"
        )
        for((body,reason) in cases) checkFailure(expected={it.getString(R.string.commons_credit_copy_failed_reason,reason)}) {response(it,body)}
    }
    @Test fun oversizedMetadataResponseAndAttributionFieldKeepTheirExistingReasons() {
        checkFailure(expected={it.getString(R.string.commons_credit_copy_failed_reason,"Commons metadata exceeds the response limit")}) {
            response(it," ".repeat(2*1024*1024+1))
        }
        checkFailure(expected={it.getString(R.string.commons_credit_copy_failed_reason,"Commons attribution field exceeds the text limit")}) {
            response(it,CommonsTestMetadata.response(source,page,"A".repeat(64*1024+1)))
        }
    }
    @Test fun malformedMetadataKeepsFrameworkDetailWithoutAnExceptionClassName() {
        val body="{"
        val reason=try {CommonsAttribution.parse(body,source);error("Invalid fixture unexpectedly parsed")}
            catch(error: org.json.JSONException) {requireNotNull(error.message)}
        checkFailure(expected={it.getString(R.string.commons_credit_copy_failed_reason,reason)}) {response(it,body)}
    }
    @Test fun persistedMixedScriptKoreanSelectionUsesItsExactCopyCreditMessageInTheGallery() =
        checkFailure("ko-Kore-KR",{"이미지 크레딧을 複寫할 수 없습니다: Commons metadata: HTTP 503"}) {response(it,code=503)}
    @Test fun metadataMemoryFailureDoesNotClaimImageInspection() =
        checkFailure(expected={it.getString(R.string.commons_credit_copy_out_of_memory)}) {throw OutOfMemoryError("fixture")}
    @Test fun metadataLinkageFailureDoesNotClaimAnImageColourConverterFailure() =
        checkFailure(expected={it.getString(R.string.commons_credit_copy_failed)}) {throw UnsatisfiedLinkError("fixture implementation name")}
    @Test fun rejectedClipboardRetainsExistingGenericFailureAndNeverClaimsCopied()=withGallery {activity ->
        val before=files(activity);val requests=mutableListOf<URL>()
        activity.openConnection={url ->requests.add(url);response(url)}
        GalleryCredits.publishClipboard={_,_->throw IllegalStateException("fixture clipboard rejection")}
        select(activity);await {!activity.downloading}
        assertEquals("Previous clipboard",clipboardText())
        assertEquals(activity.getString(R.string.ui_could_not_complete_the_operation),ShadowToast.getTextOfLatestToast())
        assertEquals(View.GONE,status(activity).visibility);unchanged(activity,requests,before)
    }
    @Test fun duplicateTapWhileMetadataIsPendingStartsOnlyOneRequest()=withGallery {activity ->
        val started=CountDownLatch(1);val release=CountDownLatch(1)
        val requests=Collections.synchronizedList(mutableListOf<URL>());val before=files(activity)
        activity.openConnection={url ->requests.add(url);started.countDown();check(release.await(8,TimeUnit.SECONDS));response(url)}
        try {
            select(activity);assertTrue(started.await(5,TimeUnit.SECONDS));select(activity)
            assertEquals(1,requests.size);assertTrue(activity.downloading)
            release.countDown();await {!activity.downloading}
            assertEquals(1,requests.size);unchanged(activity,requests,before)
        } finally {release.countDown()}
    }
    @Test fun destroyedGalleryDoesNotPublishPendingMetadataFailure()=withGallery {activity ->
        val started=CountDownLatch(1);val release=CountDownLatch(1)
        val worker=ReflectionHelpers.getField<java.util.concurrent.ExecutorService>(activity,"worker")
        activity.openConnection={url ->started.countDown();release.await(8,TimeUnit.SECONDS);response(url,code=503)}
        select(activity);assertTrue(started.await(5,TimeUnit.SECONDS))
        val before=status(activity).text.toString()
        activeController.pause().stop().destroy();release.countDown()
        await {!activity.downloading};assertTrue(worker.isShutdown)
        assertEquals("Previous clipboard",clipboardText());assertEquals(before,status(activity).text.toString())
        assertEquals(listOf(existing),session(activity).credits);assertFalse(session(activity).accepted)
    }
    @Test @Config(fontScale=1f)
    fun copyCreditMessagesRemainReadableInRepresentativeScriptsAtNormalScale()=readability(1f)
    @Test @Config(fontScale=2f)
    fun copyCreditMessagesRemainReadableInRepresentativeScriptsAtLargeScale()=readability(2f)
    private fun readability(scale: Float) {
        val reason="Commons metadata: HTTP 503"
        for(tag in listOf("fr","ar","vi-Hani","mn-Mong","mnc-Mong")) withGallery(tag) {activity ->
            val cases=listOf(
                R.string.commons_credit_copy_failed_reason to IOException(reason),
                R.string.commons_credit_copy_failed to UnsatisfiedLinkError("fixture"),
                R.string.commons_credit_copy_out_of_memory to OutOfMemoryError("fixture")
            )
            for((key,error) in cases) {
                activity.openConnection={throw error}
                select(activity);await {!activity.downloading}
                val expected=if(error is IOException) activity.getString(key,reason) else activity.getString(key)
                val root=activity.window.decorView;val density=activity.resources.displayMetrics.density
                val width=(320*density+.5f).toInt();val height=(640*density+.5f).toInt()
                root.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),
                    View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.EXACTLY));root.layout(0,0,width,height)
                val view=status(activity)
                assertEquals(expected,view.text.toString());assertEquals(scale,activity.resources.configuration.fontScale,0f)
                assertEquals(expected,view.createAccessibilityNodeInfo().text.toString())
                assertEquals(View.ACCESSIBILITY_LIVE_REGION_POLITE,view.accessibilityLiveRegion)
                assertNull(view.ellipsize);assertTrue(view.isShown)
                val layout=requireNotNull(view.layout)
                assertEquals(expected.length,layout.getLineEnd(layout.lineCount-1))
                assertTrue(layout.height<=view.height-view.totalPaddingTop-view.totalPaddingBottom)
                if(VerticalText.uiVertical()) {
                    val styled=view.text as android.text.Spanned
                    val spans=styled.getSpans(0,styled.length,android.text.style.ReplacementSpan::class.java)
                    assertEquals(1,spans.size);assertEquals(0,styled.getSpanStart(spans.single()))
                    assertEquals(styled.length,styled.getSpanEnd(spans.single()))
                    val rail=view.parent as ColumnScrollView
                    val end=(view.width-rail.width+rail.paddingLeft+rail.paddingRight).coerceAtLeast(0)
                    for(position in listOf(0,end)) {
                        rail.scrollTo(position,0);val visible=android.graphics.Rect()
                        assertTrue(view.getLocalVisibleRect(visible));assertEquals(view.height,visible.height())
                        if(position==0) assertEquals(0,visible.left)
                        if(position==end) assertEquals(view.width,visible.right)
                    }
                    rail.resetToReadingStart()
                } else {
                    GallerySvgReadabilityFixture.assertEntireMessageVisible(view)
                    if(tag=="ar") assertEquals(View.LAYOUT_DIRECTION_RTL,view.layoutDirection)
                }
                val directory=java.io.File("build/reports/commons-copy-credit-errors").apply {mkdirs()}
                val name="api35-$tag-font$scale-${activity.resources.getResourceEntryName(key)}"
                val bitmap=android.graphics.Bitmap.createBitmap(width,height,android.graphics.Bitmap.Config.ARGB_8888)
                try {
                    root.draw(android.graphics.Canvas(bitmap))
                    java.io.File(directory,"$name.png").outputStream().use {
                        assertTrue(bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it))
                    }
                } finally {bitmap.recycle()}
                java.io.File(directory,"$name.json").writeText(org.json.JSONObject()
                    .put("evidence_kind","Robolectric NATIVE rendering, not installed-device capture")
                    .put("locale",tag).put("font_scale",scale).put("message",expected)
                    .put("status_width",view.width).put("status_height",view.height)
                    .put("all_characters_laid_out",layout.getLineEnd(layout.lineCount-1)==expected.length)
                    .toString(2)+"\n")
                shadowOf(Looper.getMainLooper()).idleFor(5,TimeUnit.SECONDS)
                assertEquals(View.VISIBLE,view.visibility);assertEquals(expected,view.text.toString())
            }
        }
    }

}
