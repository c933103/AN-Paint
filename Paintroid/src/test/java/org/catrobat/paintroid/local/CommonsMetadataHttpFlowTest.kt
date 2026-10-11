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

/** M02 through both real WebView action routes; all connections are local fixtures. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[35],qualifiers="w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class CommonsMetadataHttpFlowTest {
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
        var read=false
        override fun connect()=Unit
        override fun disconnect() {disconnected=true;input.close()}
        override fun usingProxy()=false
        override fun getResponseCode()=code
        override fun getInputStream(): InputStream {read=true;return input}
    }
    private fun response(url: URL,body: String=CommonsTestMetadata.response(source,page),code: Int=200)=
        Connection(url,ByteArrayInputStream(body.toByteArray()),code)
    private fun select(activity: MediaGalleryActivity,insert: Boolean=false) {
        val web=ReflectionHelpers.getField<WebView>(activity,"web")
        val action=Uri.Builder().scheme(if(insert) IllustrationPage.USE_SCHEME else GalleryPage.CREDIT_SCHEME)
            .authority(if(insert) "insert" else "copy")
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
    private val svg="""<svg xmlns="http://www.w3.org/2000/svg" width="2" height="2"><rect width="2" height="2" fill="#ffffff"/></svg>"""
    private fun files(activity: MediaGalleryActivity)=activity.cacheDir.listFiles().orEmpty()
        .filter {it.name.startsWith("gallery-")}.map {it.name}.toSet()
    private fun expected(activity: MediaGalleryActivity,insert: Boolean,reason: String)=
        activity.getString(if(insert) R.string.ui_could_not_load_gallery_image else R.string.commons_credit_copy_failed_reason,reason)
    private fun unchanged(activity: MediaGalleryActivity,before: Set<String>) {
        assertEquals(listOf(existing),session(activity).credits)
        assertFalse(session(activity).accepted);assertNull(session(activity).draft)
        assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
        assertFalse(activity.isFinishing);assertEquals(before,files(activity))
        assertEquals("Previous clipboard",clipboardText())
    }
    private fun connect(activity: MediaGalleryActivity,requests: MutableList<Connection>,code: Int,
        error: Exception?=null) {
        activity.openConnection={url ->
            if(url.host=="commons.wikimedia.org") {
                if(error!=null) throw error
                response(url,code=code).also {requests.add(it)}
            } else response(url,svg).also {requests.add(it)}
        }
    }
    private fun assertFailure(activity: MediaGalleryActivity,insert: Boolean,reason: String,before: Set<String>) {
        val text=expected(activity,insert,reason)
        assertEquals(View.VISIBLE,status(activity).visibility)
        assertEquals(text,status(activity).text.toString())
        assertEquals(text,status(activity).createAccessibilityNodeInfo().text.toString())
        assertEquals(View.ACCESSIBILITY_LIVE_REGION_POLITE,status(activity).accessibilityLiveRegion)
        unchanged(activity,before)
    }
    @Test fun everyNon200StatusHasOnlyTypedAsciiDataAndClosesWithoutReadingResponse() {
        for(code in listOf(-1,199,201,204,301,302,400,403,429,500,503)) {
            val active=mutableListOf<HttpURLConnection?>()
            val connection=response(URL("https://commons.wikimedia.org/w/api.php"),code=code)
            var failure: CommonsAttribution.HttpException?=null
            try {CommonsAttribution.fetch(context,source,page,{connection},{},{active.add(it)})}
            catch(error: CommonsAttribution.HttpException) {failure=error}
            assertNotNull("HTTP $code must fail",failure)
            assertTrue(failure is IOException);assertEquals(code,failure!!.status)
            assertNull("No worker-localized prose or provider body is attached",failure!!.message)
            assertFalse(connection.read);assertTrue(connection.disconnected)
            assertEquals(listOf(connection,null),active)
            assertFalse(connection.instanceFollowRedirects)
        }
        val ok=response(URL("https://commons.wikimedia.org/w/api.php"))
        assertEquals(source,CommonsAttribution.fetch(context,source,page,{ok},{},{}).source)
        assertTrue(ok.read);assertTrue(ok.disconnected)
    }
    @Test fun bothActionsLocalizeTypedMetadataFailureKeepStateAndRetrySuccessfully() {
        for(insert in listOf(false,true)) for(tag in listOf("en-GB","fr","ar","ja","ko-KR","ko-Kore-KR","mn-Mong","vi-Hani")) {
            withGallery(tag) {activity ->
                val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
                connect(activity,requests,503)
                select(activity,insert);await {!activity.downloading}
                val reason=activity.getString(R.string.commons_metadata_http_error,"503")
                assertTrue(reason.contains("HTTP 503"));assertFalse(reason.contains("٥٠٣"))
                assertFailure(activity,insert,reason,before)
                assertEquals(if(insert) 2 else 1,requests.size)
                assertTrue(requests.all {it.disconnected})
                assertFalse(requests.last().read)
                assertEquals(if(insert) listOf("upload.wikimedia.org","commons.wikimedia.org") else
                    listOf("commons.wikimedia.org"),requests.map {it.url.host})
                // Exact 200 is the accepted boundary. The same action recovers with provider fields untouched.
                connect(activity,requests,200)
                select(activity,insert);await {!activity.downloading}
                if(insert) {
                    assertTrue(activity.isFinishing);assertEquals(Activity.RESULT_OK,shadowOf(activity).resultCode)
                    val returned=shadowOf(activity).resultIntent
                    assertEquals(source,returned.getStringExtra("gallery_source"))
                    val file=java.io.File(activity.cacheDir,returned.getStringExtra("gallery_file")!!)
                    assertTrue(file.isFile);assertTrue(file.delete());assertEquals(before,files(activity))
                    assertEquals("Previous clipboard",clipboardText())
                } else {
                    assertEquals(View.GONE,status(activity).visibility)
                    for(value in listOf("Mapper A","Mapper B","by-sa/3.0/",source,page))
                        assertTrue(value,clipboardText()!!.contains(value))
                }
                assertEquals(listOf(existing),session(activity).credits)
                assertTrue(requests.all {it.disconnected})
            }
        }
    }
    @Test fun untypedHttpLookingAndPercentNewlineDetailsStayVerbatimOnBothActions() {
        for(insert in listOf(false,true)) for(reason in listOf("Commons metadata: HTTP 503","  Provider 50%: %1\$s · détails\nTry again.  ")) {
            withGallery("fr") {activity ->
                val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
                connect(activity,requests,200,IOException(reason))
                select(activity,insert);await {!activity.downloading}
                assertFailure(activity,insert,reason,before)
                assertEquals(if(insert) 1 else 0,requests.size)
                assertTrue(requests.all {it.disconnected})
            }
        }
    }
    @Test fun absentAndBlankUntypedReasonsRetainEachActionsExistingWrapper() {
        for(insert in listOf(false,true)) for(reason in listOf(null,""," \n\t")) withGallery("fr") {activity ->
            val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
            connect(activity,requests,200,IOException(reason));select(activity,insert);await {!activity.downloading}
            val expected=if(insert) activity.getString(R.string.ui_could_not_load_gallery_image,reason)
                else activity.getString(R.string.commons_credit_copy_failed)
            assertEquals(expected,status(activity).text.toString())
            assertEquals(expected,status(activity).createAccessibilityNodeInfo().text.toString())
            unchanged(activity,before)
        }
    }
    @Test fun duplicateAndDestroyedActivitiesDoNotPublishLateTypedFailuresForEitherAction() {
        for(insert in listOf(false,true)) withGallery("fr") {activity ->
            val before=files(activity);val entered=CountDownLatch(1);val release=CountDownLatch(1)
            val requests=Collections.synchronizedList(mutableListOf<URL>())
            var metadataDisconnected=false
            activity.openConnection={url ->
                requests.add(url)
                if(url.host=="commons.wikimedia.org") object: HttpURLConnection(url) {
                    override fun connect()=Unit
                    override fun usingProxy()=false
                    override fun disconnect() {metadataDisconnected=true;release.countDown()}
                    override fun getResponseCode(): Int {
                        entered.countDown()
                        try {assertTrue(release.await(10,TimeUnit.SECONDS))} catch(_: InterruptedException) {
                            // Still return the typed error after destruction; do not turn this into an interruption-only test.
                        }
                        return 503
                    }
                    override fun getInputStream(): InputStream {throw AssertionError("Status error must not read a body")}
                } else response(url,svg)
            }
            select(activity,insert);assertTrue(entered.await(10,TimeUnit.SECONDS))
            val loading=status(activity).text.toString()
            select(activity,insert);assertEquals(if(insert) 2 else 1,requests.size)
            activity.finish();activeController.pause().stop().destroy();release.countDown()
            await {!activity.downloading}
            assertTrue(metadataDisconnected);assertEquals(loading,status(activity).text.toString())
            assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
            assertEquals(before,files(activity));assertEquals(listOf(existing),session(activity).credits)
            assertEquals("Previous clipboard",clipboardText())
        }
    }
    @Test @Config(qualifiers="w320dp-h640dp-port-xhdpi")
    fun representativeM02StatusRetainsFullAccessibleTextAtNormalScale() = readable(1f)
    @Test @Config(qualifiers="w320dp-h640dp-port-xhdpi-fontScale200")
    fun representativeM02StatusRetainsFullAccessibleTextAtDoubleScale() = readable(2f)
    private fun readable(scale: Float) {
        for(insert in listOf(false,true)) for(tag in listOf("en-GB","fr","ar","ja","vi-Hani","mn-Mong","mnc-Mong","lzh-Hant","en-XV","qaa-Zsye-XV")) {
            withGallery(tag) {activity ->
                val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
                connect(activity,requests,503);select(activity,insert);await {!activity.downloading}
                val reason=activity.getString(R.string.commons_metadata_http_error,"503")
                assertFailure(activity,insert,reason,before)
                val text=expected(activity,insert,reason)
                val root=activity.window.decorView;val density=activity.resources.displayMetrics.density
                val width=(320*density+.5f).toInt();val height=(640*density+.5f).toInt()
                root.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),
                    View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.EXACTLY));root.layout(0,0,width,height)
                val view=status(activity);assertEquals(scale,activity.resources.configuration.fontScale,0f)
                assertNull(view.ellipsize);assertTrue(view.isShown)
                val layout=requireNotNull(view.layout)
                assertEquals(text.length,layout.getLineEnd(layout.lineCount-1))
                assertTrue(layout.height<=view.height-view.totalPaddingTop-view.totalPaddingBottom)
                if(VerticalText.uiVertical()) {
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
                val directory=java.io.File("build/reports/commons-metadata-m02").apply {mkdirs()}
                val name="api35-$tag-font$scale-${if(insert) "insert" else "copy"}"
                val bitmap=android.graphics.Bitmap.createBitmap(width,height,android.graphics.Bitmap.Config.ARGB_8888)
                try {
                    root.draw(android.graphics.Canvas(bitmap))
                    java.io.File(directory,"$name.png").outputStream().use {
                        assertTrue(bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it))
                    }
                } finally {bitmap.recycle()}
                java.io.File(directory,"$name.json").writeText(org.json.JSONObject()
                    .put("evidence_kind","Robolectric NATIVE rendering, not installed-device capture")
                    .put("locale",tag).put("font_scale",scale).put("action",if(insert) "insert" else "copy")
                    .put("message",text).put("all_characters_laid_out",true).toString(2)+"\n")
            }
        }
    }
}
