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

/** M04 through both real WebView action routes; all connections are local fixtures. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[35],qualifiers="w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class CommonsMetadataQueryFailureFlowTest {
    private lateinit var activeController: ActivityController<MediaGalleryActivity>
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val source="https://upload.wikimedia.org/wikipedia/commons/a/ab/Test_map.svg"
    private val page="https://commons.wikimedia.org/wiki/File:Test_map.svg"
    private val existing=ImageCredit(source,"Edited credit · Émilie · かな\nhttps://example.org/credit · CC BY-SA 3.0")
    private val clipboard get()=context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
    private fun clipboardText()=clipboard.primaryClip?.getItemAt(0)?.text?.toString()
    private fun status(activity: MediaGalleryActivity)=activity.window.decorView.findViewWithTag<TextView>("gallery_status")
    private fun session(activity: MediaGalleryActivity)=ReflectionHelpers.getField<CreditEditSession>(activity,"creditSession")
    private class TrackedInput(val bytes: ByteArray): ByteArrayInputStream(bytes) {
        var closed=false
        override fun close() {closed=true;super.close()}
    }
    private class Connection(url: URL,val input: InputStream,private val code: Int=200): HttpURLConnection(url) {
        var disconnected=false
        var read=false
        override fun connect()=Unit
        override fun disconnect() {disconnected=true}
        override fun usingProxy()=false
        override fun getResponseCode()=code
        override fun getInputStream(): InputStream {read=true;return input}
    }
    private fun response(url: URL,body: String=CommonsTestMetadata.response(source,page),code: Int=200)=
        Connection(url,TrackedInput(body.toByteArray(Charsets.UTF_8)),code)
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
        shadowOf(Looper.getMainLooper()).idle();assertTrue("Metadata operation timed out",done())
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
    private fun unchanged(activity: MediaGalleryActivity,before: Set<String>,draft: GalleryCredits.EditorDraft?=null) {
        assertEquals(listOf(existing),session(activity).credits)
        assertFalse(session(activity).accepted);assertEquals(draft,session(activity).draft)
        assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
        assertFalse(activity.isFinishing);assertEquals(before,files(activity))
        assertEquals("Previous clipboard",clipboardText())
    }
    private val queryError="""{"error":{"code":"fixture-code","info":"Provider detail 50%: %1${'$'}s\nNot for display"}}"""
    private fun connect(activity: MediaGalleryActivity,requests: MutableList<Connection>,failed: Boolean,
        error: Exception?=null) {
        activity.openConnection={url ->
            if(url.host=="commons.wikimedia.org") {
                if(error!=null) throw error
                response(url,if(failed) queryError else CommonsTestMetadata.response(source,page,"Émilie · かな")).also {requests.add(it)}
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
    @Test fun everyTopLevelErrorValueIsTypedButNestedErrorAndValidMetadataAreNot() {
        for(value in listOf("{}","null","false","0","[]","\"provider text\"")) {
            try {CommonsAttribution.parse("{\"error\":$value}",source);fail("Present error must fail: $value")}
            catch(error: CommonsAttribution.QueryFailureException) {
                assertNull("Do not attach provider fields or worker-localized prose",error.message)
                assertTrue(error is IOException)
            }
        }
        val valid=CommonsTestMetadata.response(source,page,"Émilie · かな")
        val nested=org.json.JSONObject(valid).put("unrelated",org.json.JSONObject().put("error","ignored")).toString()
        for(body in listOf(valid,nested)) {
            val record=CommonsAttribution.parse(body,source)
            assertEquals(source,record.source);assertTrue(record.text(false).contains("Émilie · かな"))
        }
        try {CommonsAttribution.parse("{",source);fail("Malformed JSON must retain its own exception")}
        catch(error: org.json.JSONException) {assertNotNull(error.message)}
    }
    @Test fun queryErrorFetchClosesInputDisconnectsAndClearsActiveWithoutProviderLeakage() {
        val connection=response(URL("https://commons.wikimedia.org/w/api.php"),queryError)
        val active=mutableListOf<HttpURLConnection?>()
        try {CommonsAttribution.fetch(context,source,page,{connection},{},{active.add(it)});fail("Query error must fail")}
        catch(error: CommonsAttribution.QueryFailureException) {assertNull(error.message)}
        assertTrue(connection.read);assertTrue((connection.input as TrackedInput).closed)
        assertTrue(connection.disconnected);assertEquals(listOf(connection,null),active)
        assertFalse(connection.instanceFollowRedirects)
    }
    @Test fun httpResponseLimitFieldAndValidationReasonsRemainSeparate() {
        val active=mutableListOf<HttpURLConnection?>()
        val connection=response(URL("https://commons.wikimedia.org/w/api.php"),queryError,503)
        try {CommonsAttribution.fetch(context,source,page,{connection},{},{active.add(it)});fail("HTTP error must precede reading the body")}
        catch(error: CommonsAttribution.HttpException) {assertEquals(503,error.status);assertNull(error.message)}
        assertFalse(connection.read);assertTrue(connection.disconnected);assertEquals(listOf(connection,null),active)
        val oversize=response(URL("https://commons.wikimedia.org/w/api.php")," ".repeat(2*1024*1024+1))
        try {CommonsAttribution.fetch(context,source,page,{oversize},{},{});fail("M03 limit must remain distinct")}
        catch(error: CommonsAttribution.ResponseLimitException) {assertNull(error.message)}
        assertTrue((oversize.input as TrackedInput).closed);assertTrue(oversize.disconnected)
        try {CommonsAttribution.plain("A".repeat(64*1024+1));fail("M09 field limit must remain distinct")}
        catch(error: IOException) {assertFalse(error is CommonsAttribution.QueryFailureException);assertTrue(error is CommonsImportFailure.FieldTooLarge);assertNull(error.message)}
        try {CommonsAttribution.parse("{\"query\":{\"pages\":[]}}",source);fail("M05 ambiguity must remain distinct")}
        catch(error: IOException) {assertFalse(error is CommonsAttribution.QueryFailureException);assertTrue(error is CommonsImportFailure.AmbiguousFile);assertNull(error.message)}
    }
    @Test fun bothActionsLocalizeTypedMetadataFailureKeepStateAndRetryWithValidMetadata() {
        for(insert in listOf(false,true)) for(tag in listOf("en-GB","fr","ar","ja","ko-KR","ko-Kore-KR","mn-Mong","vi-Hani")) {
            withGallery(tag) {activity ->
                val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
                val cachedBefore=CommonsAttribution.cached(activity,source)
                connect(activity,requests,true)
                select(activity,insert);await {!activity.downloading}
                val reason=activity.getString(R.string.commons_metadata_query_failed)
                assertFailure(activity,insert,reason,before)
                assertEquals(cachedBefore,CommonsAttribution.cached(activity,source))
                assertEquals(if(insert) 2 else 1,requests.size)
                assertTrue(requests.all {it.disconnected})
                assertTrue(requests.all {(it.input as TrackedInput).closed})
                assertEquals(if(insert) listOf("upload.wikimedia.org","commons.wikimedia.org") else
                    listOf("commons.wikimedia.org"),requests.map {it.url.host})
                // The same real action recovers with valid metadata and keeps provider fields intact.
                connect(activity,requests,false)
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
                    for(value in listOf("Émilie · かな","Mapper B","by-sa/3.0/",source,page))
                        assertTrue(value,clipboardText()!!.contains(value))
                }
                assertEquals(listOf(existing),session(activity).credits)
                assertTrue(requests.all {it.disconnected});assertTrue(requests.all {(it.input as TrackedInput).closed})
            }
        }
    }
    @Test fun typedFailurePreservesAnUnacceptedCreditDraftForBothActions() {
        for(insert in listOf(false,true)) withGallery("fr") {activity ->
            val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
            val draft=GalleryCredits.EditorDraft(source,"Unaccepted edit · Émilie · かな\n50%: %1\$s")
            session(activity).saveDraft(draft)
            val revision=session(activity).revision
            connect(activity,requests,true);select(activity,insert);await {!activity.downloading}
            assertEquals(expected(activity,insert,activity.getString(R.string.commons_metadata_query_failed)),
                status(activity).text.toString())
            unchanged(activity,before,draft);assertEquals(revision,session(activity).revision)
            assertTrue(session(activity).edits.isEmpty());assertNull(session(activity).acceptedSnapshot)
        }
    }
    @Test fun queuedTypedFailureResolvesResourcesOnlyWhenTheAliveUiCallbackRuns() {
        for(insert in listOf(false,true)) withGallery("en-GB") {activity ->
            val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
            connect(activity,requests,true);select(activity,insert)
            val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(12)
            while(activity.downloading && System.nanoTime()<deadline) Thread.sleep(5)
            assertFalse(activity.downloading)
            // Switch the same global UI resource provider the production ui() helper uses,
            // without dispatching the already queued callback or recreating this activity.
            val config=android.content.res.Configuration(activity.resources.configuration)
            config.setLocales(android.os.LocaleList(Locale.FRENCH))
            val french=activity.createConfigurationContext(config).resources
            PaintApplication.currentResources=french
            shadowOf(Looper.getMainLooper()).idle()
            val reason=french.getString(R.string.commons_metadata_query_failed)
            assertNotEquals("Commons metadata query failed",reason)
            assertEquals(french.getString(if(insert) R.string.ui_could_not_load_gallery_image else
                R.string.commons_credit_copy_failed_reason,reason),status(activity).text.toString())
            unchanged(activity,before)
        }
    }
    @Test fun untypedQueryLookingAndPercentNewlineDetailsStayVerbatimOnBothActions() {
        for(insert in listOf(false,true)) for(reason in listOf("Commons metadata query failed","  Provider 50%: %1\$s · détails\nTry again.  ")) {
            withGallery("fr") {activity ->
                val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
                connect(activity,requests,false,IOException(reason))
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
            connect(activity,requests,false,IOException(reason));select(activity,insert);await {!activity.downloading}
            val expected=if(insert) activity.getString(R.string.ui_could_not_load_gallery_image,reason)
                else activity.getString(R.string.commons_credit_copy_failed)
            assertEquals(expected,status(activity).text.toString())
            assertEquals(expected,status(activity).createAccessibilityNodeInfo().text.toString())
            unchanged(activity,before)
        }
    }
    @Test fun destructionDropsQueuedTypedQueryFailures() {
        for(insert in listOf(false,true)) withGallery("fr") {activity ->
            val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
            connect(activity,requests,true);select(activity,insert)
            // Do not dispatch the queued UI callback before destruction.
            val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(12)
            while(activity.downloading && System.nanoTime()<deadline) Thread.sleep(5)
            assertFalse(activity.downloading);assertTrue(requests.all {it.disconnected})
            val loading=status(activity).text.toString()
            activity.finish();activeController.pause().stop().destroy();shadowOf(Looper.getMainLooper()).idle()
            assertEquals(loading,status(activity).text.toString());assertEquals("Previous clipboard",clipboardText())
            assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
            assertEquals(before,files(activity));assertEquals(listOf(existing),session(activity).credits)
        }
    }
    @Test fun duplicateAndDestroyedInFlightQueryRequestsRemainCancelled() {
        for(insert in listOf(false,true)) withGallery("fr") {activity ->
            val before=files(activity);val entered=CountDownLatch(1);val release=CountDownLatch(1)
            val requests=Collections.synchronizedList(mutableListOf<Connection>())
            var closed=false
            val input=object: ByteArrayInputStream(queryError.toByteArray(Charsets.UTF_8)) {
                override fun read(buffer: ByteArray,offset: Int,length: Int): Int {
                    entered.countDown()
                    try {assertTrue(release.await(10,TimeUnit.SECONDS))} catch(_: InterruptedException) { }
                    return super.read(buffer,offset,length)
                }
                override fun close() {closed=true;super.close()}
            }
            activity.openConnection={url ->
                (if(url.host=="commons.wikimedia.org") Connection(url,input) else response(url,svg)).also {requests.add(it)}
            }
            try {
                select(activity,insert);assertTrue(entered.await(10,TimeUnit.SECONDS))
                val loading=status(activity).text.toString()
                select(activity,insert);assertEquals(if(insert) 2 else 1,requests.size)
                activity.finish();activeController.pause().stop().destroy();release.countDown();await {!activity.downloading}
                assertTrue(closed);assertTrue(requests.all {it.disconnected})
                assertEquals(loading,status(activity).text.toString());assertEquals("Previous clipboard",clipboardText())
                assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
                assertEquals(before,files(activity));assertEquals(listOf(existing),session(activity).credits)
            } finally {release.countDown()}
        }
    }
    @Test fun destroyedActivityDropsAlreadyQueuedSuccessAndRemovesReturnedFile() {
        for(insert in listOf(false,true)) withGallery("fr") {activity ->
            val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
            connect(activity,requests,false);select(activity,insert)
            // Do not drain the paused main looper before destruction: success is already posted.
            val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(12)
            while(activity.downloading && System.nanoTime()<deadline) Thread.sleep(5)
            assertFalse(activity.downloading);assertTrue(requests.all {it.disconnected})
            assertNotNull(CommonsAttribution.cached(activity,source))
            val loading=status(activity).text.toString()
            activity.finish();activeController.pause().stop().destroy();shadowOf(Looper.getMainLooper()).idle()
            assertEquals(loading,status(activity).text.toString());assertEquals("Previous clipboard",clipboardText())
            assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
            assertEquals(before,files(activity));assertEquals(listOf(existing),session(activity).credits)
        }
    }
    @Test @Config(qualifiers="w320dp-h640dp-port-xhdpi",fontScale=2f)
    fun repeatedVerticalQueryFailureResetsScrolledStatusToReadingStart() {
        for(insert in listOf(false,true)) for(tag in listOf("mn-Mong","mnc-Mong")) withGallery(tag) {activity ->
            val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
            connect(activity,requests,true);select(activity,insert);await {!activity.downloading}
            val root=activity.window.decorView;val density=activity.resources.displayMetrics.density
            val width=(320*density+.5f).toInt();val height=(640*density+.5f).toInt()
            fun layoutRoot() {
                root.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),
                    View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.EXACTLY));root.layout(0,0,width,height)
            }
            layoutRoot()
            val view=status(activity);val rail=view.parent as ColumnScrollView
            val end=(view.width-rail.width+rail.paddingLeft+rail.paddingRight).coerceAtLeast(0)
            assertTrue("Fixture must exercise an actual scrolled status",end>0)
            assertEquals("Mongolian and Manchu start at the leftmost reading column",0,rail.scrollX)
            rail.scrollTo(end,0);assertEquals(end,rail.scrollX)
            select(activity,insert);await {!activity.downloading};layoutRoot()
            assertEquals("The second actual failed action must restore reading start",0,rail.scrollX)
            assertFailure(activity,insert,activity.getString(R.string.commons_metadata_query_failed),before)
            assertEquals(if(insert) 4 else 2,requests.size)
            assertTrue(requests.all {it.disconnected})
        }
    }
    @Test @Config(qualifiers="w320dp-h640dp-port-xhdpi")
    fun representativeM04StatusRetainsFullAccessibleTextAtNormalScale() = readable(1f)
    @Test @Config(qualifiers="w320dp-h640dp-port-xhdpi",fontScale=2f)
    fun representativeM04StatusRetainsFullAccessibleTextAtDoubleScale() = readable(2f)
    @Test @Config(qualifiers="w640dp-h320dp-land-xhdpi")
    fun shortLandscapeM04RetainsFullAccessibleTextAtNormalScale() = readable(1f,640,320)
    @Test @Config(qualifiers="w640dp-h320dp-land-xhdpi",fontScale=2f)
    fun shortLandscapeM04RetainsFullAccessibleTextAtDoubleScale() = readable(2f,640,320)
    private fun readable(scale: Float,widthDp: Int=320,heightDp: Int=640) {
        val failures=mutableListOf<String>()
        var completedProfiles=0
        for(insert in listOf(false,true)) for(tag in listOf("en-GB","ain-Kana","ain-Latn","bo","ryu","fr","ar","ja","vi-Hani","mn-Mong","mnc-Mong","lzh-Hant","en-XV","qaa-Zsye-XV")) {
            var metadataFinished=false
            try {withGallery(tag) {activity ->
                val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
                connect(activity,requests,true);select(activity,insert);await {!activity.downloading}
                metadataFinished=true
                val reason=activity.getString(R.string.commons_metadata_query_failed)
                assertFailure(activity,insert,reason,before)
                val text=expected(activity,insert,reason)
                val root=activity.window.decorView;val density=activity.resources.displayMetrics.density
                val width=(widthDp*density+.5f).toInt();val height=(heightDp*density+.5f).toInt()
                root.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),
                    View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.EXACTLY));root.layout(0,0,width,height)
                val view=status(activity);assertEquals(scale,activity.resources.configuration.fontScale,0f)
                assertNull(view.ellipsize);assertTrue(view.isShown)
                val layout=requireNotNull(view.layout)
                // Retain failed-profile pixels and measured geometry before any layout oracle.
                // This is diagnostic evidence; the original assertions below still decide acceptance.
                if(widthDp==640 && heightDp==320 && scale==1f)
                    recordLandscapeDiagnostic(root,view,tag,insert,scale)
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
                    root.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),
                        View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.EXACTLY));root.layout(0,0,width,height)
                    assertEquals("Capture must follow the completed reading-start layout",
                        if(VerticalText.uiDirection()==TextDirection.VERTICAL_RL) end else 0,rail.scrollX)
                } else {
                    if(heightDp>=640) GallerySvgReadabilityFixture.assertEntireMessageVisible(view)
                    else {
                        val scroll=root.findViewWithTag<GalleryControlsScroll>("gallery_controls_scroll")
                        assertTrue("Short landscape must retain a visible scroll viewport",scroll.height>0)
                        for(line in 0 until layout.lineCount) {
                            assertEquals(0,layout.getEllipsisCount(line))
                        }
                        val inkLabel="api35-$tag-${widthDp}x${heightDp}-font$scale-${if(insert) "insert" else "copy"}"
                        capturePaintedInk(view).use {ink ->
                            recordPaintedInk(ink,inkLabel);assertReadableInk(ink,inkLabel)
                        }
                        val start=android.graphics.Rect()
                        assertTrue(view.getLocalVisibleRect(start));assertEquals(0,start.top)
                        assertEquals(view.width,start.width())
                        val box=android.graphics.Rect(0,0,view.width,view.height)
                        scroll.offsetDescendantRectToMyCoords(view,box)
                        scroll.scrollTo(0,box.bottom-scroll.height)
                        val end=android.graphics.Rect()
                        assertTrue(view.getLocalVisibleRect(end));assertEquals(view.height,end.bottom)
                        assertEquals(view.width,end.width())
                        scroll.revealStart(view);root.requestLayout()
                        root.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),
                            View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.EXACTLY));root.layout(0,0,width,height)
                        val restored=android.graphics.Rect()
                        assertTrue(view.getLocalVisibleRect(restored));assertEquals(0,restored.top)
                    }
                    if(tag=="ar") assertEquals(View.LAYOUT_DIRECTION_RTL,view.layoutDirection)
                }
                val directory=java.io.File("build/reports/commons-metadata-m04").apply {mkdirs()}
                val name="api35-$tag-${widthDp}x${heightDp}-font$scale-${if(insert) "insert" else "copy"}"
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
                    .put("message",text).put("all_characters_laid_out",true)
                    .put("status_parent_scroll_x",(view.parent as View).scrollX).toString(2)+"\n")
            }} catch(failure: AssertionError) {
                if(!metadataFinished) throw failure
                // withGallery has already performed its normal cleanup. Keep other profiles
                // observable, without retrying the failed action or converting failure to success.
                failures.add("$tag ${if(insert) "insert" else "copy"} ${widthDp}x$heightDp font$scale: ${failure.message}")
            }
            completedProfiles++
        }
        if(widthDp==640 && heightDp==320 && scale==1f) {
            val directory=java.io.File("build/reports/commons-metadata-m04-diagnostic").apply {mkdirs()}
            java.io.File(directory,"normal-landscape-outcomes.json").writeText(org.json.JSONObject()
                .put("evidence_kind","Current source-bound structural/readability checks; exact raster differences require separate review")
                .put("advance_guard_role","Diagnostic only; original_horizontal_guard=false is not a claim of painted-ink clipping")
                .put("pixel_acceptance_role","Exact raster reports are unmasked diagnostics; all_profiles_passed does not imply exact pixel equality or disposition of review_required frames")
                .put("completed_profiles",completedProfiles).put("expected_profiles",28)
                .put("failures",org.json.JSONArray(failures)).put("all_profiles_passed",failures.isEmpty()).toString(2)+"\n")
        }
        assertTrue("Readability profile failures:\n"+failures.joinToString("\n"),failures.isEmpty())
    }

    private data class PaintedInkFrame(
        val actual: android.graphics.Bitmap,val reference: android.graphics.Bitmap,
        val referencePixels: IntArray,val referenceBox: android.graphics.Rect,
        val originX: Int,val originY: Int,val contentWidth: Int,val glyphBounds: android.graphics.RectF,
        val viewBoundsWidth: Boolean,val layoutBoundsWidth: Boolean,val shiftedStart: Boolean,val leadingInset: Int,
        val inkPixels: Int,val inkLeft: Int,val inkRight: Int,val edgePixels: Int,
        val horizontalOverflow: Int,val outsideView: Int,val missingInk: Int,val differentPixels: Int,
        val componentCount: Int,val missingComponents: Int,val missingOpaque: Int
    ): java.io.Closeable {
        override fun close() {actual.recycle();reference.recycle()}
    }

    /** API35, plain horizontal status only. Unsupported drawing features fail closed. */
    private fun capturePaintedInk(view: TextView,translationX: Int=0,
        clipLeft: Int=0,clipRight: Int=view.width,expectedBoundsWidth: Boolean=true,
        clipOut: android.graphics.Rect?=null): PaintedInkFrame {
        val layout=requireNotNull(view.layout)
        assertFalse("Horizontal oracle must not replace the vertical route",VerticalText.uiVertical())
        assertEquals("Reference must contain the complete actual text",view.text.toString(),layout.text.toString())
        assertTrue(view.text.isNotEmpty());assertTrue(layout.lineCount>0)
        var covered=0
        for(line in 0 until layout.lineCount) {
            assertEquals("Contiguous UTF-16 line coverage",covered,layout.getLineStart(line))
            assertEquals("No ellipsis in the complete reference",0,layout.getEllipsisCount(line))
            val end=layout.getLineEnd(line);assertTrue(end>=covered);covered=end
        }
        assertEquals(view.text.length,covered)
        val spanned=view.text as? android.text.Spanned
        val spans=spanned?.getSpans(0,view.text.length,Any::class.java).orEmpty()
        assertTrue("Only one measured geometry-only paragraph margin is supported",spans.size<=1)
        var leadingInset=0
        for(span in spans) {
            assertEquals(android.text.style.LeadingMarginSpan.Standard::class.java,span.javaClass)
            assertEquals(0,spanned!!.getSpanStart(span));assertEquals(view.text.length,spanned.getSpanEnd(span))
            assertEquals(android.text.Spanned.SPAN_EXCLUSIVE_EXCLUSIVE,spanned.getSpanFlags(span))
            val margin=span as android.text.style.LeadingMarginSpan.Standard
            leadingInset=margin.getLeadingMargin(true)
            assertTrue(leadingInset>0 && leadingInset<=kotlin.math.ceil(view.paint.textSize*2f).toInt())
            assertEquals(leadingInset,margin.getLeadingMargin(false))
        }
        assertEquals(android.text.Layout.Alignment.ALIGN_NORMAL,layout.alignment)
        assertEquals("Explicitly bound width-mode for this observation",expectedBoundsWidth,view.useBoundsForWidth)
        assertEquals("View and native Layout must agree on bounds-based width",view.useBoundsForWidth,layout.useBoundsForWidth)
        assertFalse("Shifted-overhang views need a separately reviewed origin",view.shiftDrawingOffsetForStartOverhang)
        assertFalse("Shifted-overhang layouts need a separately reviewed origin",layout.shiftDrawingOffsetForStartOverhang)
        assertNull(view.background);assertNull(view.foreground)
        assertTrue(view.compoundDrawables.all {it==null});assertNull(view.transformationMethod)
        assertEquals(-1,view.selectionStart);assertEquals(-1,view.selectionEnd)
        assertEquals(android.view.Gravity.TOP,view.gravity and android.view.Gravity.VERTICAL_GRAVITY_MASK)
        assertEquals(0,view.scrollX);assertEquals(0,view.scrollY)
        assertEquals(0f,view.rotation,0f);assertEquals(0f,view.rotationX,0f);assertEquals(0f,view.rotationY,0f)
        assertEquals(0f,view.translationX,0f);assertEquals(0f,view.translationY,0f)
        assertEquals(1f,view.scaleX,0f);assertEquals(1f,view.scaleY,0f);assertEquals(1f,view.alpha,0f)
        assertEquals(android.graphics.Paint.Style.FILL,view.paint.style)
        assertNull(view.paint.shader);assertNull(view.paint.colorFilter);assertNull(view.paint.maskFilter);assertNull(view.paint.pathEffect)
        assertFalse(view.paint.isUnderlineText);assertFalse(view.paint.isStrikeThruText);assertFalse(view.paint.isFakeBoldText)
        assertEquals(0f,view.paint.textSkewX,0f);assertEquals(0,view.paint.baselineShift)
        assertEquals(0f,view.shadowRadius,0f)
        val originX=view.compoundPaddingLeft
        val originY=view.baseline-layout.getLineBaseline(0)
        assertEquals("TOP baseline must identify the real draw origin",view.extendedPaddingTop,originY)
        val contentWidth=view.width-view.compoundPaddingLeft-view.compoundPaddingRight
        assertEquals("Native layout width must be the actual text clip width",contentWidth,layout.width)
        fun boundedBitmap(width: Int,height: Int): android.graphics.Bitmap {
            assertTrue("Positive, bounded native raster allocation",width>0 && height>0 && width.toLong()*height<=16_000_000L)
            return android.graphics.Bitmap.createBitmap(width,height,android.graphics.Bitmap.Config.ARGB_8888)
        }
        val actual=boundedBitmap(view.width,view.height)
        var reference: android.graphics.Bitmap?=null
        try {
            // The actual view retains its own native clip. No view/paint/text property is changed.
            val actualCanvas=android.graphics.Canvas(actual)
            actualCanvas.clipRect(clipLeft,0,clipRight,view.height)
            if(clipOut!=null) actualCanvas.clipOutRect(clipOut)
            actualCanvas.translate(translationX.toFloat(),0f);view.draw(actualCanvas)
            // API35 derives this box from actual glyphs, including marks outside line metrics.
            // The union prevents a wholly displaced glyph from disappearing beyond a fixed margin.
            val bounds=android.graphics.RectF(layout.computeDrawingBoundingBox()).apply {offset(translationX.toFloat(),0f)}
            // API35 glyph bounds omit paragraph margins. The exact allowed span can
            // move any paragraph by at most this measured inset in either direction.
            val xs=mutableListOf(0f,layout.width.toFloat(),bounds.left-leadingInset,bounds.right+leadingInset)
            val ys=mutableListOf(0f,layout.height.toFloat(),bounds.top,bounds.bottom)
            for(line in 0 until layout.lineCount) {
                xs.add(layout.getLineLeft(line)+translationX);xs.add(layout.getLineRight(line)+translationX)
                ys.add(layout.getLineTop(line).toFloat());ys.add(layout.getLineBottom(line).toFloat())
            }
            assertTrue("Finite native glyph and line geometry",(xs+ys).all {it.isFinite() && kotlin.math.abs(it)<100_000f})
            assertTrue(bounds.left<=bounds.right && bounds.top<=bounds.bottom)
            // Two pixels are allocation guard only, never a containment or comparison tolerance.
            val box=android.graphics.Rect(kotlin.math.floor(xs.minOrNull()!!).toInt()-2,
                kotlin.math.floor(ys.minOrNull()!!).toInt()-2,kotlin.math.ceil(xs.maxOrNull()!!).toInt()+2,
                kotlin.math.ceil(ys.maxOrNull()!!).toInt()+2)
            val complete=boundedBitmap(box.width(),box.height());reference=complete
            val canvas=android.graphics.Canvas(complete)
            canvas.translate((translationX-box.left).toFloat(),(-box.top).toFloat());layout.draw(canvas)
            val expectedPixels=IntArray(complete.width*complete.height)
            complete.getPixels(expectedPixels,0,complete.width,0,0,complete.width,complete.height)
            val actualPixels=IntArray(actual.width*actual.height)
            actual.getPixels(actualPixels,0,actual.width,0,0,actual.width,actual.height)
            var ink=0;var left=Int.MAX_VALUE;var right=Int.MIN_VALUE;var edges=0
            var overflow=0;var outside=0;var missing=0;var different=0;var missingOpaque=0
            fun actualPixel(index: Int): Int {
                val vx=originX+box.left+index%complete.width
                val vy=originY+box.top+index/complete.width
                return if(vx in 0 until actual.width && vy in 0 until actual.height) actualPixels[vy*actual.width+vx] else 0
            }
            for(y in 0 until complete.height) for(x in 0 until complete.width) {
                val pixel=expectedPixels[y*complete.width+x]
                if((pixel ushr 24)==0) continue
                ink++;val localX=box.left+x;val localY=box.top+y
                if((pixel ushr 24)==255 && (actualPixel(y*complete.width+x) ushr 24)==0) missingOpaque++
                left=minOf(left,localX);right=maxOf(right,localX+1)
                if(x==0 || y==0 || x==complete.width-1 || y==complete.height-1) edges++
                if(localX<0 || localX>=contentWidth) overflow++
                val vx=originX+localX;val vy=originY+localY
                if(vx !in 0 until actual.width || vy !in 0 until actual.height) {outside++;missing++}
                else if((actualPixels[vy*actual.width+vx] ushr 24)==0) missing++
            }
            // Compare the WHOLE actual view against the independent full reference. The
            // expected reference is never obtained by cropping the already-clipped actual view.
            for(y in 0 until actual.height) for(x in 0 until actual.width) {
                val rx=x-originX-box.left;val ry=y-originY-box.top
                val expected=if(rx in 0 until complete.width && ry in 0 until complete.height)
                    expectedPixels[ry*complete.width+rx] else 0
                if(actualPixels[y*actual.width+x]!=expected) different++
            }
            // Eight-connected alpha>0 components are a conservative hard-loss check,
            // not glyph segmentation. Partial mark/stroke changes still require review.
            val visited=BooleanArray(expectedPixels.size);val queue=IntArray(ink.coerceAtLeast(1))
            var components=0;var missingComponents=0
            for(seed in expectedPixels.indices) {
                if(visited[seed] || (expectedPixels[seed] ushr 24)==0) continue
                components++;var head=0;var tail=1;queue[0]=seed;visited[seed]=true;var survives=false
                while(head<tail) {
                    val index=queue[head++];val x=index%complete.width;val y=index/complete.width
                    if((actualPixel(index) ushr 24)!=0) survives=true
                    for(dy in -1..1) for(dx in -1..1) {
                        val nx=x+dx;val ny=y+dy
                        if(nx !in 0 until complete.width || ny !in 0 until complete.height) continue
                        val next=ny*complete.width+nx
                        if(!visited[next] && (expectedPixels[next] ushr 24)!=0) {
                            visited[next]=true;queue[tail++]=next
                        }
                    }
                }
                if(!survives) missingComponents++
            }
            return PaintedInkFrame(actual,complete,expectedPixels,box,originX,originY,contentWidth,bounds,
                view.useBoundsForWidth,layout.useBoundsForWidth,layout.shiftDrawingOffsetForStartOverhang,leadingInset,ink,left,right,edges,overflow,outside,missing,different,
                components,missingComponents,missingOpaque)
        } catch(failure: Throwable) {actual.recycle();reference?.recycle();throw failure}
    }

    private fun exactPixelsMatch(frame: PaintedInkFrame)=frame.inkPixels>0 && frame.edgePixels==0 &&
        frame.horizontalOverflow==0 && frame.outsideView==0 &&
        frame.missingInk==0 && frame.differentPixels==0

    private fun assertReadableInk(frame: PaintedInkFrame,label: String) {
        assertTrue("$label complete reference must contain native ink",frame.inkPixels>0)
        assertEquals("$label reference raster must not touch allocation boundary",0,frame.edgePixels)
        assertEquals("$label complete reference ink component missing",0,frame.missingComponents)
        assertEquals("$label opaque reference ink completely missing",0,frame.missingOpaque)
        // Exact differences remain visible in the full PNGs/JSON and require explicit
        // review. Passing these hard checks does not establish exact-pixel equality.
    }

    private fun assertPaintedInk(frame: PaintedInkFrame,label: String) {
        assertTrue("$label complete reference must contain native ink",frame.inkPixels>0)
        assertEquals("$label reference raster must not touch allocation boundary",0,frame.edgePixels)
        assertEquals("$label horizontal painted-ink overflow",0,frame.horizontalOverflow)
        assertEquals("$label full reference ink lies outside the actual view",0,frame.outsideView)
        assertEquals("$label clipped expected ink",0,frame.missingInk)
        assertEquals("$label exact full-reference/actual-view ARGB mismatch",0,frame.differentPixels)
    }

    private fun paintedInkReport(frame: PaintedInkFrame)=org.json.JSONObject()
        .put("reference_source","Complete native Layout with API35 actual-glyph bounds; never an actual-view crop")
        .put("reference_box",frame.referenceBox.toShortString()).put("glyph_bounds",frame.glyphBounds.toString())
        .put("origin_x",frame.originX).put("origin_y",frame.originY).put("content_width",frame.contentWidth)
        .put("view_use_bounds_for_width",frame.viewBoundsWidth).put("layout_use_bounds_for_width",frame.layoutBoundsWidth)
        .put("shift_drawing_offset_for_start_overhang",frame.shiftedStart).put("measured_leading_inset_px",frame.leadingInset)
        .put("ink_pixels",frame.inkPixels).put("ink_left",frame.inkLeft).put("ink_right_exclusive",frame.inkRight)
        .put("allocation_edge_pixels",frame.edgePixels).put("horizontal_overflow_pixels",frame.horizontalOverflow)
        .put("outside_view_pixels",frame.outsideView).put("missing_expected_ink_pixels",frame.missingInk)
        .put("different_argb_pixels",frame.differentPixels).put("alpha_cutoff",0).put("position_tolerance_px",0)
        .put("color_tolerance",0)
        .put("ink_components",frame.componentCount).put("missing_complete_components",frame.missingComponents)
        .put("missing_opaque_reference_pixels",frame.missingOpaque)
        .put("component_scope","Eight-connected alpha>0 ink, not glyph segmentation; unexplained partial loss requires review")
        .put("exact_pixel_comparison_passed",exactPixelsMatch(frame))
        .put("review_required",!exactPixelsMatch(frame))

    private fun recordPaintedInk(frame: PaintedInkFrame,label: String) {
        val directory=java.io.File("build/reports/commons-metadata-m04-painted-ink").apply {mkdirs()}
        for((suffix,bitmap) in listOf("actual-textview" to frame.actual,"complete-layout" to frame.reference))
            java.io.File(directory,"$label-$suffix.png").outputStream().use {
                check(bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it))
            }
        java.io.File(directory,"$label.json").writeText(paintedInkReport(frame)
            .put("evidence_kind","Robolectric NATIVE unmasked exact-raster diagnostic; consult hard JUnit checks and explicit review disposition")
            .toString(2)+"\n")
    }

    @Test @Config(qualifiers="w640dp-h320dp-land-xhdpi")
    fun paintedInkOracleRejectsNativeOverflowAndClippedEdgeGlyphsAtNormalScale() = inkOracleNegativeControls(1f)
    @Test @Config(qualifiers="w640dp-h320dp-land-xhdpi",fontScale=2f)
    fun paintedInkOracleRejectsNativeOverflowAndClippedEdgeGlyphsAtDoubleScale() = inkOracleNegativeControls(2f)

    private fun inkOracleNegativeControls(scale: Float) {
        val outcomes=org.json.JSONArray();val resetOutcomes=org.json.JSONArray()
        for(tag in listOf("en-GB","ain-Kana","bo","ar","ja","vi-Hani")) withGallery(tag) {activity ->
            val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
            connect(activity,requests,true);select(activity);await {!activity.downloading}
            assertFailure(activity,false,activity.getString(R.string.commons_metadata_query_failed),before)
            val root=activity.window.decorView;val density=activity.resources.displayMetrics.density
            val width=(640*density+.5f).toInt();val height=(320*density+.5f).toInt()
            root.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),
                View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.EXACTLY));root.layout(0,0,width,height)
            val view=status(activity);val text=view.text.toString();val layout=requireNotNull(view.layout)
            assertEquals(scale,activity.resources.configuration.fontScale,0f)
            val label="api35-$tag-640x320-font$scale-negative-controls"
            if(tag=="ar" && scale==2f) {
                // Independent original plain TextView at the same native width, text and font.
                // The real repaired status is never switched back or edited for this control.
                val beforeView=TextView(activity).apply {
                    paint.set(view.paint);setTextColor(view.currentTextColor)
                    setPadding(view.paddingLeft,view.paddingTop,view.paddingRight,view.paddingBottom)
                    gravity=view.gravity;layoutDirection=view.layoutDirection;textDirection=view.textDirection
                    textAlignment=view.textAlignment;includeFontPadding=view.includeFontPadding
                    setLineSpacing(view.lineSpacingExtra,view.lineSpacingMultiplier)
                    breakStrategy=view.breakStrategy;hyphenationFrequency=view.hyphenationFrequency
                    justificationMode=view.justificationMode;lineBreakStyle=view.lineBreakStyle;lineBreakWordStyle=view.lineBreakWordStyle
                    useBoundsForWidth=false;shiftDrawingOffsetForStartOverhang=false;this.text=view.text.toString()
                }
                beforeView.measure(View.MeasureSpec.makeMeasureSpec(view.width,View.MeasureSpec.EXACTLY),
                    View.MeasureSpec.makeMeasureSpec(0,View.MeasureSpec.UNSPECIFIED))
                beforeView.layout(0,0,beforeView.measuredWidth,beforeView.measuredHeight)
                capturePaintedInk(beforeView,expectedBoundsWidth=false).use {beforeInk ->
                    recordPaintedInk(beforeInk,"$label-original-plain-before")
                    assertTrue("Original Arabic native start bearing must overflow",beforeInk.horizontalOverflow>0)
                    assertTrue("Original Arabic draw must really lose expected ink",beforeInk.missingInk>0)
                    assertEquals(0,beforeInk.edgePixels)
                }
            }
            capturePaintedInk(view).use {intact ->
                recordPaintedInk(intact,"$label-intact");assertReadableInk(intact,"$label intact")
                val cases=org.json.JSONArray()
                val originalBounds=android.graphics.RectF(layout.computeDrawingBoundingBox())
                fun paintState()=listOf(view.paint.color,view.paint.flags,view.paint.textSize,
                    view.paint.textScaleX,view.paint.textSkewX,view.paint.typeface,view.paint.textLocales,
                    view.paint.baselineShift,view.paint.bgColor,view.paint.shader,view.paint.colorFilter,
                    view.paint.maskFilter,view.paint.pathEffect,view.paint.style,view.paint.strokeWidth)
                val originalPaint=paintState()
                fun geometry()=listOf(view.width,view.height,view.scrollX,view.scrollY,view.compoundPaddingLeft,
                    view.compoundPaddingRight,view.extendedPaddingTop,view.extendedPaddingBottom,view.baseline,
                    (view.text as? android.text.Spanned)?.let {s ->
                        s.getSpans(0,s.length,android.text.style.LeadingMarginSpan.Standard::class.java).map {
                            listOf(s.getSpanStart(it),s.getSpanEnd(it),s.getSpanFlags(it),it.getLeadingMargin(true),it.getLeadingMargin(false))
                        }
                    },layout.width,layout.height,layout.lineCount,view.useBoundsForWidth,layout.useBoundsForWidth,
                    view.shiftDrawingOffsetForStartOverhang,layout.shiftDrawingOffsetForStartOverhang)+(0 until layout.lineCount).flatMap {line ->
                        listOf(layout.getLineStart(line),layout.getLineEnd(line),layout.getLineTop(line),
                            layout.getLineBottom(line),layout.getLineBaseline(line))
                    }
                val originalGeometry=geometry()
                fun rejects(name: String,frame: PaintedInkFrame,cause: String) {
                    frame.use {
                        assertEquals("Probe must preserve the native layout's cached glyph bounds",
                            originalBounds,layout.computeDrawingBoundingBox())
                        assertEquals("Probe must preserve native paint state",originalPaint,paintState())
                        assertEquals("Probe must preserve view and layout geometry",originalGeometry,geometry())
                        assertTrue("Native mutation must retain nonzero reference ink",frame.inkPixels>0)
                        assertEquals("Mutation must not disappear outside the reference allocation",0,frame.edgePixels)
                        assertEquals("Integer translation/clipping must retain every reference ink pixel",intact.inkPixels,frame.inkPixels)
                        assertFalse("Native mutation must change actual pixels",frame.actual.sameAs(intact.actual))
                        if(cause=="clipped expected ink") {
                            assertArrayEquals("Clipping changes the actual draw only",intact.referencePixels,frame.referencePixels)
                            assertTrue("Clip must remove additional ink beyond any intact diagnostic mismatch",
                                frame.missingInk>intact.missingInk)
                        } else assertTrue("Translation must physically overflow the content box",frame.horizontalOverflow>0)
                        recordPaintedInk(frame,"$label-$name")
                        var rejected=false
                        try {assertPaintedInk(frame,"$label $name")}
                        catch(failure: AssertionError) {
                            assertTrue("Reject for the intended defect: ${failure.message}",failure.message.orEmpty().contains(cause))
                            rejected=true
                        }
                        assertTrue("The oracle must reject the native draw mutation",rejected)
                        assertEquals(text,view.text.toString());assertEquals(text,layout.text.toString())
                        assertEquals(text,view.createAccessibilityNodeInfo().text.toString())
                        assertEquals(originalBounds,layout.computeDrawingBoundingBox())
                        assertEquals(originalPaint,paintState());assertEquals(originalGeometry,geometry())
                        cases.put(paintedInkReport(frame).put("mutation",name).put("rejected",true).put("reason",cause)
                            .put("actual_draw_changed",true).put("newly_missing_expected_ink_pixels",
                                if(cause=="clipped expected ink") frame.missingInk-intact.missingInk else org.json.JSONObject.NULL))
                    }
                }
                rejects("left-overflow",capturePaintedInk(view,translationX=-intact.inkLeft-1),"horizontal painted-ink overflow")
                rejects("right-overflow",capturePaintedInk(view,translationX=intact.contentWidth-intact.inkRight+1),"horizontal painted-ink overflow")
                rejects("wholly-left-of-view",capturePaintedInk(view,translationX=-4*intact.contentWidth),"horizontal painted-ink overflow")
                rejects("wholly-right-of-view",capturePaintedInk(view,translationX=4*intact.contentWidth),"horizontal painted-ink overflow")
                rejects("clip-first-spatial-ink",capturePaintedInk(view,clipLeft=intact.originX+intact.inkLeft+1),"clipped expected ink")
                rejects("clip-last-spatial-ink",capturePaintedInk(view,clipRight=intact.originX+intact.inkRight-1),"clipped expected ink")
                outcomes.put(org.json.JSONObject().put("locale",tag).put("font_scale",scale).put("intact_structural_passed",true)
                    .put("intact_exact_pixel_comparison_passed",exactPixelsMatch(intact)).put("review_required",!exactPixelsMatch(intact))
                    .put("logical_first_character_is_rtl",layout.isRtlCharAt(0)).put("cases",cases))
            }
            if(tag=="en-GB") outcomes.getJSONObject(outcomes.length()-1)
                .put("complete_loss_controls",recordCompleteGlyphLossControls(activity,view,label))
            resetOutcomes.put(checkInsetReset(activity,view,width,height,label))
        }
        val directory=java.io.File("build/reports/commons-metadata-m04-painted-ink").apply {mkdirs()}
        java.io.File(directory,"native-negative-controls-font$scale.json").writeText(outcomes.toString(2)+"\n")
        java.io.File(directory,"native-inset-resets-font$scale.json").writeText(resetOutcomes.toString(2)+"\n")
    }

    private fun recordCompleteGlyphLossControls(activity: MediaGalleryActivity,template: TextView,label: String): org.json.JSONArray {
        val outcomes=org.json.JSONArray()
        // A separate full glyph and a detached combining acute on separate native lines.
        // No bitmap is edited; the Canvas clip changes only the actual TextView draw.
        val view=TextView(activity).apply {
            paint.set(template.paint);setTextColor(template.currentTextColor)
            gravity=android.view.Gravity.TOP;includeFontPadding=template.includeFontPadding
            useBoundsForWidth=true;shiftDrawingOffsetForStartOverhang=false
            text="A\n  \u0301"
        }
        view.measure(View.MeasureSpec.makeMeasureSpec(template.width,View.MeasureSpec.EXACTLY),
            View.MeasureSpec.makeMeasureSpec(0,View.MeasureSpec.UNSPECIFIED))
        view.layout(0,0,view.measuredWidth,view.measuredHeight)
        val layout=requireNotNull(view.layout);assertEquals(2,layout.lineCount)
        val originalText=view.text.toString();val originalBounds=android.graphics.RectF(layout.computeDrawingBoundingBox())
        capturePaintedInk(view).use {intact ->
            recordPaintedInk(intact,"$label-complete-loss-intact");assertPaintedInk(intact,"$label complete-loss intact")
            assertReadableInk(intact,"$label complete-loss intact")
            for((line,name) in listOf(0 to "whole-glyph",1 to "detached-mark")) {
                val clip=android.graphics.Rect(0,intact.originY+layout.getLineTop(line),view.width,
                    intact.originY+layout.getLineBottom(line))
                var removed=0
                for(index in intact.referencePixels.indices) {
                    val x=intact.originX+intact.referenceBox.left+index%intact.reference.width
                    val y=intact.originY+intact.referenceBox.top+index/intact.reference.width
                    if((intact.referencePixels[index] ushr 24)!=0 && clip.contains(x,y)) removed++
                }
                assertTrue("Each independent content-loss control must remove real native ink",removed>0)
                capturePaintedInk(view,clipOut=clip).use {mutant ->
                    recordPaintedInk(mutant,"$label-remove-$name")
                    assertArrayEquals(intact.referencePixels,mutant.referencePixels)
                    assertEquals(originalBounds,layout.computeDrawingBoundingBox())
                    assertEquals(originalText,view.text.toString());assertEquals(originalText,layout.text.toString())
                    assertEquals(originalText,view.createAccessibilityNodeInfo().text.toString())
                    assertEquals("Only the selected line's ink is removed",removed,mutant.missingInk)
                    assertTrue("Native clip must remove a complete component",mutant.missingComponents>0)
                    var rejected=false
                    try {assertReadableInk(mutant,"$label remove $name")}
                    catch(failure: AssertionError) {
                        assertTrue(failure.message.orEmpty().contains("complete reference ink component missing"));rejected=true
                    }
                    assertTrue("Hard readability guard must detect complete content loss",rejected)
                    outcomes.put(paintedInkReport(mutant).put("mutation","remove-$name").put("rejected",true)
                        .put("reason","complete reference ink component missing").put("removed_native_ink_pixels",removed))
                }
            }
            val opaque=intact.referencePixels.indices.firstOrNull {index ->
                (intact.referencePixels[index] ushr 24)==255 &&
                    intact.referenceBox.top+index/intact.reference.width in layout.getLineTop(0) until layout.getLineBottom(0)
            }
            assertNotNull("The independent glyph must contain an opaque stroke sample",opaque)
            val index=opaque!!
            val x=intact.originX+intact.referenceBox.left+index%intact.reference.width
            val y=intact.originY+intact.referenceBox.top+index/intact.reference.width
            capturePaintedInk(view,clipOut=android.graphics.Rect(x,y,x+1,y+1)).use {mutant ->
                recordPaintedInk(mutant,"$label-remove-opaque-stroke")
                assertArrayEquals(intact.referencePixels,mutant.referencePixels)
                assertEquals(originalBounds,layout.computeDrawingBoundingBox())
                assertEquals(originalText,view.text.toString());assertEquals(originalText,layout.text.toString())
                assertEquals(originalText,view.createAccessibilityNodeInfo().text.toString())
                assertEquals("One actual native sample is removed",1,mutant.missingInk)
                assertEquals("The complete component must still survive",0,mutant.missingComponents)
                assertEquals("The removed sample must be opaque",1,mutant.missingOpaque)
                var rejected=false
                try {assertReadableInk(mutant,"$label remove opaque stroke")}
                catch(failure: AssertionError) {
                    assertTrue(failure.message.orEmpty().contains("opaque reference ink completely missing"));rejected=true
                }
                assertTrue("The independent opaque-loss guard must reject stroke removal",rejected)
                outcomes.put(paintedInkReport(mutant).put("mutation","remove-opaque-stroke").put("rejected",true)
                    .put("reason","opaque reference ink completely missing").put("removed_native_ink_pixels",1))
            }
        }
        return outcomes
    }

    private fun checkInsetReset(activity: MediaGalleryActivity,view: TextView,width: Int,height: Int,label: String): org.json.JSONObject {
        val root=activity.window.decorView
        val original=view.text.toString();val originalSize=view.textSize
        fun inset()=(view.text as? android.text.Spanned)?.let {s ->
            s.getSpans(0,s.length,android.text.style.LeadingMarginSpan.Standard::class.java).singleOrNull()?.getLeadingMargin(true)
        } ?: 0
        val initialInset=inset()
        fun measure(w: Int=width) {
            root.requestLayout();root.measure(View.MeasureSpec.makeMeasureSpec(w,View.MeasureSpec.EXACTLY),
                View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.EXACTLY));root.layout(0,0,w,height)
        }
        fun show(message: String) {
            MediaGalleryActivity::class.java.getDeclaredMethod("showStatus",String::class.java)
                .apply {isAccessible=true}.invoke(activity,message)
        }
        val results=org.json.JSONArray()
        fun check(name: String,message: String) {
            assertEquals(message,view.text.toString());assertEquals(message,view.createAccessibilityNodeInfo().text.toString())
            capturePaintedInk(view).use {frame ->
                recordPaintedInk(frame,"$label-reset-$name");assertReadableInk(frame,"$label reset $name")
                results.put(paintedInkReport(frame).put("case",name).put("message",message)
                    .put("text_size_px",view.textSize).put("view_width",view.width))
            }
        }
        try {
            assertFalse("Status is settled before same-height replacement",view.isLayoutRequested)
            show(original)
            assertTrue("Status setter must request its own glyph remeasurement",view.isLayoutRequested)
            repeat(3) {measure();assertEquals("Remeasure must not accumulate the margin",initialInset,inset())}
            measure(width-48);check("width",original)
            view.setTextSize(android.util.TypedValue.COMPLEX_UNIT_PX,originalSize*.75f)
            measure();check("font",original)
            view.setTextSize(android.util.TypedValue.COMPLEX_UNIT_PX,originalSize)
            val mixed=original+"\nABC\nالعربية"
            show(mixed);measure();check("mixed-paragraphs",mixed)
            show("OK");measure();check("short-message","OK")
            assertEquals("A new short status must not retain the old margin",0,inset())
            show(original);measure();check("restored",original)
            assertEquals("Restoring the same font, width and text restores its measured margin",initialInset,inset())
        } finally {
            view.setTextSize(android.util.TypedValue.COMPLEX_UNIT_PX,originalSize);show(original);measure()
        }
        return org.json.JSONObject().put("profile",label).put("initial_inset",initialInset)
            .put("repeat_count",3).put("cases",results).put("all_structural_checks_passed",true)
            .put("review_required",(0 until results.length()).any {results.getJSONObject(it).getBoolean("review_required")})
    }

    private fun recordLandscapeDiagnostic(root: View,view: TextView,tag: String,insert: Boolean,scale: Float) {
        val layout=requireNotNull(view.layout)
        val directory=java.io.File("build/reports/commons-metadata-m04-diagnostic").apply {mkdirs()}
        val name="api35-$tag-640x320-font$scale-${if(insert) "insert" else "copy"}-before-checks"
        fun save(bitmap: android.graphics.Bitmap,suffix: String) {
            java.io.File(directory,"$name$suffix.png").outputStream().use {
                check(bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it))
            }
        }
        val screen=android.graphics.Bitmap.createBitmap(root.width,root.height,android.graphics.Bitmap.Config.ARGB_8888)
        try {root.draw(android.graphics.Canvas(screen));save(screen,"")} finally {screen.recycle()}
        val margin=kotlin.math.ceil(view.textSize*2).toInt().coerceAtLeast(32)
        val ink=android.graphics.Bitmap.createBitmap(layout.width+2*margin,layout.height+2*margin,
            android.graphics.Bitmap.Config.ARGB_8888)
        val lines=org.json.JSONArray()
        val inkEdges=org.json.JSONObject()
        try {
            // Draw the SAME native Layout onto a transparent, expanded canvas. This separates
            // typographic advance from actual painted ink without changing the view or its text.
            val canvas=android.graphics.Canvas(ink);canvas.translate(margin.toFloat(),margin.toFloat())
            layout.draw(canvas);save(ink,"-expanded-layout")
            val pixels=IntArray(ink.width*ink.height)
            ink.getPixels(pixels,0,ink.width,0,0,ink.width,ink.height)
            fun painted(x: Int,y: Int)=(pixels[y*ink.width+x] ushr 24)!=0
            inkEdges.put("left",(0 until ink.height).any {painted(0,it)})
                .put("right",(0 until ink.height).any {painted(ink.width-1,it)})
                .put("top",(0 until ink.width).any {painted(it,0)})
                .put("bottom",(0 until ink.width).any {painted(it,ink.height-1)})
            for(line in 0 until layout.lineCount) {
                var left=ink.width;var right=-1;var outside=0
                val top=(margin+layout.getLineTop(line)).coerceAtLeast(0)
                val bottom=(margin+layout.getLineBottom(line)).coerceAtMost(ink.height)
                for(y in top until bottom) for(x in 0 until ink.width) {
                    if((pixels[y*ink.width+x] ushr 24)!=0) {
                        left=minOf(left,x);right=maxOf(right,x)
                        if(x<margin || x>=margin+layout.width) outside++
                    }
                }
                lines.put(org.json.JSONObject()
                    .put("line",line).put("start",layout.getLineStart(line)).put("end",layout.getLineEnd(line))
                    .put("text",view.text.subSequence(layout.getLineStart(line),layout.getLineEnd(line)).toString())
                    .put("left",layout.getLineLeft(line)).put("right",layout.getLineRight(line))
                    .put("max",layout.getLineMax(line)).put("width_including_trailing_whitespace",layout.getLineWidth(line))
                    .put("top",layout.getLineTop(line)).put("bottom",layout.getLineBottom(line))
                    .put("baseline",layout.getLineBaseline(line)).put("paragraph_direction",layout.getParagraphDirection(line))
                    .put("ellipsis_count",layout.getEllipsisCount(line))
                    .put("original_horizontal_guard",layout.getLineLeft(line)>=-1f && layout.getLineRight(line)<=layout.width+1f)
                    .put("ink_left",if(right>=0) left-margin else org.json.JSONObject.NULL)
                    .put("ink_right_exclusive",if(right>=0) right-margin+1 else org.json.JSONObject.NULL)
                    .put("ink_pixels_outside_layout",outside))
            }
        } finally {ink.recycle()}
        val visible=android.graphics.Rect();val intersects=view.getLocalVisibleRect(visible)
        val window=IntArray(2);view.getLocationInWindow(window)
        val parent=view.parent as View
        val report=org.json.JSONObject()
            .put("evidence_kind","Robolectric NATIVE pre-assertion diagnostic; not installed-device or acceptance evidence")
            .put("locale",tag).put("action",if(insert) "insert" else "copy").put("font_scale",scale)
            .put("message",view.text.toString()).put("accessibility_text",view.createAccessibilityNodeInfo().text.toString())
            .put("viewport_width",root.width).put("viewport_height",root.height)
            .put("density",view.resources.displayMetrics.density).put("scaled_density",view.resources.displayMetrics.scaledDensity)
            .put("configured_font_scale",view.resources.configuration.fontScale)
            .put("resource_locales",view.resources.configuration.locales.toLanguageTags()).put("text_locales",view.textLocales.toLanguageTags())
            .put("text_size_px",view.textSize).put("break_strategy",view.breakStrategy).put("hyphenation_frequency",view.hyphenationFrequency)
            .put("view_width",view.width).put("view_height",view.height).put("layout_class",layout.javaClass.name)
            .put("layout_width",layout.width).put("layout_height",layout.height).put("line_count",layout.lineCount)
            .put("content_width",view.width-view.compoundPaddingLeft-view.compoundPaddingRight)
            .put("content_height",view.height-view.totalPaddingTop-view.totalPaddingBottom)
            .put("padding_left",view.totalPaddingLeft).put("padding_top",view.totalPaddingTop)
            .put("padding_right",view.totalPaddingRight).put("padding_bottom",view.totalPaddingBottom)
            .put("window_x",window[0]).put("window_y",window[1]).put("layout_direction",view.layoutDirection)
            .put("visible_bounds",visible.toShortString()).put("intersects_visible_area",intersects)
            .put("parent_class",parent.javaClass.name).put("parent_width",parent.width).put("parent_height",parent.height)
            .put("parent_scroll_x",parent.scrollX).put("parent_scroll_y",parent.scrollY)
            .put("all_characters_laid_out",layout.lineCount>0 && layout.getLineEnd(layout.lineCount-1)==view.text.length)
            .put("expanded_layout_margin_px",margin).put("expanded_canvas_edge_touch",inkEdges)
            .put("ink_measurement_limit","Nontransparent pixels in each native line box on a finite expanded canvas. Edge contact can mean the probe itself clips ink; inspect root and expanded pixels. Does not establish device behavior.")
            .put("lines",lines)
        java.io.File(directory,"$name.json").writeText(report.toString(2)+"\n")
    }
}
