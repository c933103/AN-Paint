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

/** M01 and M05–M12 through production producers and WebView routes; no provider requests. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[35],qualifiers="w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class CommonsImportFailureFlowTest {
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
    private class Connection(url: URL,val input: InputStream,private val code: Int=200,private val redirect: String?=null): HttpURLConnection(url) {
        var disconnected=false
        var read=false
        override fun connect()=Unit
        override fun disconnect() {disconnected=true}
        override fun usingProxy()=false
        override fun getResponseCode()=code
        override fun getHeaderField(name: String): String?=if(name=="Location") redirect else null
        override fun getInputStream(): InputStream {read=true;return input}
    }
    private fun response(url: URL,body: String=CommonsTestMetadata.response(source,page),code: Int=200)=
        Connection(url,TrackedInput(body.toByteArray(Charsets.UTF_8)),code)
    private fun select(activity: MediaGalleryActivity,insert: Boolean=false,artworkPage: String=page) {
        val web=ReflectionHelpers.getField<WebView>(activity,"web")
        val action=Uri.Builder().scheme(if(insert) IllustrationPage.USE_SCHEME else GalleryPage.CREDIT_SCHEME)
            .authority(if(insert) "insert" else "copy")
            .appendQueryParameter("source",source).appendQueryParameter("page",artworkPage).build()
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
    private data class MetadataCase(val body: String,val type: Class<out Exception>,val key: Int)
    private fun metadataCases(): List<MetadataCase> {
        fun changed(edit: (org.json.JSONObject,org.json.JSONObject)->Unit): String {
            val root=org.json.JSONObject(CommonsTestMetadata.response(source,page))
            val item=root.getJSONObject("query").getJSONArray("pages").getJSONObject(0)
            edit(root,item);return root.toString()
        }
        return listOf(
            MetadataCase("""{"query":{"pages":[]}}""",CommonsImportFailure.AmbiguousFile::class.java,R.string.commons_metadata_ambiguous_file),
            MetadataCase(changed {root,item ->root.getJSONObject("query").getJSONArray("pages").put(item)},
                CommonsImportFailure.AmbiguousFile::class.java,R.string.commons_metadata_ambiguous_file),
            MetadataCase(changed {_,item ->item.put("missing",true)},CommonsImportFailure.MetadataUnavailable::class.java,R.string.commons_metadata_unavailable),
            MetadataCase(changed {_,item ->item.put("ns",0)},CommonsImportFailure.MetadataUnavailable::class.java,R.string.commons_metadata_unavailable),
            MetadataCase(changed {_,item ->item.remove("ns")},CommonsImportFailure.MetadataUnavailable::class.java,R.string.commons_metadata_unavailable),
            MetadataCase(CommonsTestMetadata.response(source.replace("Test_","Other_"),page),
                CommonsImportFailure.MetadataOriginalMismatch::class.java,R.string.commons_metadata_original_mismatch),
            MetadataCase(CommonsTestMetadata.response(source,"https://example.org/not-a-file"),
                CommonsImportFailure.InvalidAttributionPage::class.java,R.string.commons_metadata_invalid_page),
            MetadataCase(changed {_,item ->item.getJSONArray("imageinfo").getJSONObject(0).getJSONObject("extmetadata")
                .put("Artist",org.json.JSONObject().put("value","A".repeat(64*1024+1)))},
                CommonsImportFailure.FieldTooLarge::class.java,R.string.commons_metadata_field_too_large)
        )
    }
    private fun connect(activity: MediaGalleryActivity,requests: MutableList<Connection>,body: String) {
        activity.openConnection={url ->response(url,if(url.host=="commons.wikimedia.org") body else svg).also {requests.add(it)}}
    }
    private fun assertFailure(activity: MediaGalleryActivity,insert: Boolean,key: Int,before: Set<String>,
        draft: GalleryCredits.EditorDraft?=null) {
        val text=expected(activity,insert,activity.getString(key))
        assertEquals(View.VISIBLE,status(activity).visibility)
        assertEquals(text,status(activity).text.toString())
        assertEquals(text,status(activity).createAccessibilityNodeInfo().text.toString())
        assertEquals(View.ACCESSIBILITY_LIVE_REGION_POLITE,status(activity).accessibilityLiveRegion)
        unchanged(activity,before,draft)
    }
    private fun retry(activity: MediaGalleryActivity,insert: Boolean,requests: MutableList<Connection>,before: Set<String>) {
        connect(activity,requests,CommonsTestMetadata.response(source,page,"Émilie 50%: %1\$s · かな"))
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
            for(value in listOf("Émilie 50%: %1\$s · かな","Mapper B","by-sa/3.0/",source,page))
                assertTrue(value,clipboardText()!!.contains(value))
        }
        assertEquals(listOf(existing),session(activity).credits)
    }
    @Test fun directMetadataFailuresRetainIOExceptionTypesAndNoWorkerProse() {
        for(case in metadataCases()) {
            val error=runCatching {CommonsAttribution.parse(case.body,source)}.exceptionOrNull()
            assertNotNull(error);assertEquals(case.type,error!!::class.java)
            assertTrue(error is IOException);assertTrue(error is CommonsImportFailure);assertNull(error.message)
        }
        // The raw HTML field limit remains UTF-16 length, including surrogate pairs.
        for(accepted in listOf("A".repeat(64*1024),"😀".repeat(32*1024)))
            assertEquals(accepted,CommonsAttribution.plain(accepted))
        for(rejected in listOf("A".repeat(64*1024+1),"😀".repeat(32*1024)+"A"))
            assertTrue(runCatching {CommonsAttribution.plain(rejected)}.exceptionOrNull() is CommonsImportFailure.FieldTooLarge)
        val record=CommonsAttribution.parse(CommonsTestMetadata.response(source,page),source)
        assertEquals(source,record.source);assertEquals(page,record.page)
        for(value in listOf("Mapper A","Mapper B","CC BY-SA 3.0","https://example.org/original-map"))
            assertTrue(record.text(false).contains(value))
    }
    @Test fun everyMetadataValidationConditionUsesBothLiveActionsAndRecovers() {
        for(insert in listOf(false,true)) for(case in metadataCases()) withGallery("fr") {activity ->
            val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
            val cached=CommonsAttribution.cached(activity,source)
            connect(activity,requests,case.body);select(activity,insert);await {!activity.downloading}
            assertFailure(activity,insert,case.key,before)
            assertEquals(cached,CommonsAttribution.cached(activity,source))
            assertEquals(if(insert) 2 else 1,requests.size)
            assertTrue(requests.all {it.read && it.disconnected && (it.input as TrackedInput).closed})
            assertNull(ReflectionHelpers.getField<HttpURLConnection?>(activity,"activeConnection"))
            retry(activity,insert,requests,before)
        }
    }
    @Test fun cacheCommitFailureIsTypedAndBothActionsKeepEditsThenRecover() {
        val record=CommonsAttribution.parse(CommonsTestMetadata.response(source,page),source)
        val direct=CommonsCacheFailureContext(context)
        val error=runCatching {CommonsAttribution.cache(direct,record)}.exceptionOrNull()
        assertTrue(error is CommonsImportFailure.CacheFailed);assertTrue(error is IOException);assertNull(error!!.message)
        for(insert in listOf(false,true)) withGallery("fr") {activity ->
            val base=activity.baseContext;val rejecting=CommonsCacheFailureContext(base)
            ReflectionHelpers.setField(activity,"mBase",rejecting)
            try {
                val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
                val cached=CommonsAttribution.cached(activity,source)
                val draft=GalleryCredits.EditorDraft(source,"Unsaved edit · かな · 50%: %1\$s")
                session(activity).saveDraft(draft);val revision=session(activity).revision
                connect(activity,requests,CommonsTestMetadata.response(source,page));select(activity,insert);await {!activity.downloading}
                assertFailure(activity,insert,R.string.commons_metadata_cache_failed,before,draft)
                assertEquals(1,rejecting.refusedCommits);assertEquals(revision,session(activity).revision)
                assertEquals(cached,CommonsAttribution.cached(activity,source));assertTrue(session(activity).edits.isEmpty())
                assertTrue(requests.all {it.read && it.disconnected && (it.input as TrackedInput).closed})
                rejecting.reject=false;retry(activity,insert,requests,before)
            } finally {ReflectionHelpers.setField(activity,"mBase",base)}
        }
    }
    @Test fun invalidPageIsTypedBeforeConnectingAndBothEntryGuardsMakeZeroRequests() {
        val invalid="https://commons.wikimedia.org/wiki/Category:Blank_maps"
        var opened=0
        val error=runCatching {CommonsAttribution.fetch(context,source,invalid,{opened++;response(it)},{},{})}.exceptionOrNull()
        assertTrue(error is CommonsImportFailure.NotFilePage);assertTrue(error is IllegalArgumentException)
        assertNull(error!!.message);assertEquals(0,opened)
        for(insert in listOf(false,true)) withGallery {activity ->
            activity.openConnection={opened++;response(it)}
            val before=files(activity);select(activity,insert,invalid)
            assertEquals(0,opened);assertFalse(activity.downloading);unchanged(activity,before)
        }
    }
    @Test fun insertionPageTruncationTriggersTypedPreconditionWithoutMetadataRequestAndRetryWorks()=withGallery {activity ->
        val longPage="https://commons.wikimedia.org/w/index.php?padding="+"x".repeat(4096)+"&title=File%3ATest_map.svg"
        assertTrue(IllustrationSource.COMMONS.isArtworkPage(Uri.parse(longPage)))
        assertFalse(IllustrationSource.COMMONS.isArtworkPage(Uri.parse(longPage.take(4096))))
        val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
        connect(activity,requests,CommonsTestMetadata.response(source,page))
        select(activity,true,longPage);await {!activity.downloading}
        assertFailure(activity,true,R.string.commons_metadata_not_file_page,before)
        assertEquals(listOf("upload.wikimedia.org"),requests.map {it.url.host})
        assertTrue(requests.all {it.disconnected && (it.input as TrackedInput).closed})
        retry(activity,true,requests,before)
    }
    @Test fun copyCreditDoesNotTruncateTheValidIndexPage()=withGallery {activity ->
        val longPage="https://commons.wikimedia.org/w/index.php?padding="+"x".repeat(4096)+"&title=File%3ATest_map.svg"
        val requests=Collections.synchronizedList(mutableListOf<Connection>())
        connect(activity,requests,CommonsTestMetadata.response(source,page));select(activity,false,longPage);await {!activity.downloading}
        assertEquals(View.GONE,status(activity).visibility);assertEquals(1,requests.size)
        assertEquals("File:Test_map.svg",Uri.parse(requests.single().url.toString()).getQueryParameter("titles"))
        assertTrue(clipboardText()!!.contains("Mapper A"));assertEquals(listOf(existing),session(activity).credits)
    }
    @Test fun redirectedOriginalMismatchFailsBeforeReadingBodyOrMetadataAndRetryWorks()=withGallery {activity ->
        val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
        val other=source.replace("Test_","Other_")
        activity.openConnection={url ->Connection(url,TrackedInput(svg.toByteArray()),
            if(url.toString()==source) 302 else 200,other).also {requests.add(it)}}
        select(activity,true);await {!activity.downloading}
        assertFailure(activity,true,R.string.commons_download_original_mismatch,before)
        assertEquals(listOf(source,other),requests.map {it.url.toString()})
        assertTrue(requests.all {it.disconnected && !it.read})
        assertNull(ReflectionHelpers.getField<HttpURLConnection?>(activity,"activeConnection"))
        retry(activity,true,requests,before)
    }
    @Test @Config(shadows=[CommonsPngFailureShadow::class])
    fun pngEncodingFalseIsTypedRecyclesBitmapClosesOutputAndInsertionCleansBothFiles() {
        CommonsPngFailureShadow.resetFailure()
        try {
            val input=java.io.File.createTempFile("commons-fixture-",".svg",context.cacheDir).apply {writeText(svg)}
            val output=java.io.File.createTempFile("commons-fixture-",".png",context.cacheDir)
            try {
                CommonsPngFailureShadow.reject=true
                val error=runCatching {BlankMapSvg.renderOriginal(input,output,ImageMemoryPolicy.forDevice(context))}.exceptionOrNull()
                assertTrue(error is CommonsImportFailure.PngEncodeFailed);assertTrue(error is IOException);assertNull(error!!.message)
                assertTrue(CommonsPngFailureShadow.rejectedBitmap!!.isRecycled)
                assertTrue(runCatching {CommonsPngFailureShadow.rejectedStream!!.write(1)}.exceptionOrNull() is IOException)
            } finally {input.delete();output.delete()}
            withGallery("fr") {activity ->
                val before=files(activity);val requests=Collections.synchronizedList(mutableListOf<Connection>())
                connect(activity,requests,CommonsTestMetadata.response(source,page));select(activity,true);await {!activity.downloading}
                assertFailure(activity,true,R.string.commons_svg_png_encode_failed,before)
                assertEquals(listOf("upload.wikimedia.org"),requests.map {it.url.host})
                assertTrue(requests.all {it.disconnected && (it.input as TrackedInput).closed})
                assertTrue(CommonsPngFailureShadow.rejectedBitmap!!.isRecycled)
                assertTrue(runCatching {CommonsPngFailureShadow.rejectedStream!!.write(1)}.exceptionOrNull() is IOException)
                CommonsPngFailureShadow.reject=false;retry(activity,true,requests,before)
            }
        } finally {CommonsPngFailureShadow.resetFailure()}
    }
    private fun typedFailures(): List<Pair<Exception,Int>> = listOf(
        CommonsImportFailure.NotFilePage() to R.string.commons_metadata_not_file_page,
        CommonsImportFailure.AmbiguousFile() to R.string.commons_metadata_ambiguous_file,
        CommonsImportFailure.MetadataUnavailable() to R.string.commons_metadata_unavailable,
        CommonsImportFailure.MetadataOriginalMismatch() to R.string.commons_metadata_original_mismatch,
        CommonsImportFailure.InvalidAttributionPage() to R.string.commons_metadata_invalid_page,
        CommonsImportFailure.FieldTooLarge() to R.string.commons_metadata_field_too_large,
        CommonsImportFailure.CacheFailed() to R.string.commons_metadata_cache_failed,
        CommonsImportFailure.DownloadOriginalMismatch() to R.string.commons_download_original_mismatch,
        CommonsImportFailure.PngEncodeFailed() to R.string.commons_svg_png_encode_failed)
    @Test fun allTypedReasonsResolveOnlyWhenTheAliveUiCallbackRuns() {
        for(insert in listOf(false,true)) for((error,key) in typedFailures().take(if(insert) 9 else 7)) withGallery {activity ->
            assertNull(error.message)
            assertEquals(key in setOf(R.string.commons_metadata_not_file_page,R.string.commons_download_original_mismatch),
                error is IllegalArgumentException)
            val before=files(activity);activity.openConnection={throw error}
            select(activity,insert)
            val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(12)
            while(activity.downloading && System.nanoTime()<deadline) Thread.sleep(5)
            assertFalse(activity.downloading)
            val original=PaintApplication.currentResources
            val liveReason="Live UI resource · 50%: %1\$s\n${original.getResourceEntryName(key)}"
            @Suppress("DEPRECATION")
            val live=object: android.content.res.Resources(original.assets,original.displayMetrics,original.configuration) {
                override fun getString(id: Int): String {
                    if(id!=key) return super.getString(id)
                    assertEquals(Looper.getMainLooper(),Looper.myLooper());return liveReason
                }
            }
            PaintApplication.currentResources=live
            shadowOf(Looper.getMainLooper()).idle()
            assertEquals(original.getString(if(insert) R.string.ui_could_not_load_gallery_image else
                R.string.commons_credit_copy_failed_reason,liveReason),status(activity).text.toString())
            unchanged(activity,before)
        }
    }
    @Test fun untypedFormerEnglishReasonsAndPercentNewlineDetailAreNeverClassifiedOrReformatted() {
        val extra="  Provider 50%: %1\$s · détails\nTry again.  "
        for(insert in listOf(false,true)) withGallery("fr") {activity ->
            val before=files(activity)
            for(reason in listOf(
                "Not a Commons file page",
                "Commons metadata returned an ambiguous file",
                "Commons file metadata is unavailable",
                "Commons attribution does not match the selected original file",
                "Invalid Commons attribution page",
                "Commons attribution field exceeds the text limit",
                "Could not retain Commons attribution",
                "The Commons download redirected to a different original file.",
                "Could not encode blank map as PNG"
            )+listOf(extra,null,""," \n\t")) {
                activity.openConnection={throw IOException(reason)};select(activity,insert);await {!activity.downloading}
                val text=if(!insert && reason.isNullOrBlank()) activity.getString(R.string.commons_credit_copy_failed)
                    else expected(activity,insert,reason ?: "null")
                assertEquals(text,status(activity).text.toString());unchanged(activity,before)
            }
        }
    }
    @Test fun destructionDropsEveryQueuedTypedFailure() {
        for(insert in listOf(false,true)) for((error,_) in typedFailures().take(if(insert) 9 else 7)) withGallery {activity ->
            val before=files(activity);activity.openConnection={throw error};select(activity,insert)
            val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(12)
            while(activity.downloading && System.nanoTime()<deadline) Thread.sleep(5)
            assertFalse(activity.downloading)
            val loading=status(activity).text.toString()
            activity.finish();activeController.pause().stop().destroy();shadowOf(Looper.getMainLooper()).idle()
            assertEquals(loading,status(activity).text.toString());assertEquals("Previous clipboard",clipboardText())
            assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
            assertEquals(before,files(activity));assertEquals(listOf(existing),session(activity).credits)
        }
    }
    @Test fun duplicateAndDestroyedInFlightMetadataRequestsStayCancelled() {
        for(insert in listOf(false,true)) withGallery {activity ->
            val before=files(activity);val entered=CountDownLatch(1);val release=CountDownLatch(1)
            val requests=Collections.synchronizedList(mutableListOf<Connection>());var closed=false
            val input=object: ByteArrayInputStream(metadataCases().first().body.toByteArray(Charsets.UTF_8)) {
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
                val loading=status(activity).text.toString();select(activity,insert)
                assertEquals(if(insert) 2 else 1,requests.size)
                activity.finish();activeController.pause().stop().destroy();release.countDown();await {!activity.downloading}
                assertTrue(closed);assertTrue(requests.all {it.disconnected})
                assertEquals(loading,status(activity).text.toString());assertEquals("Previous clipboard",clipboardText())
                assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
                assertEquals(before,files(activity));assertEquals(listOf(existing),session(activity).credits)
            } finally {release.countDown()}
        }
    }
    @Test fun rotationKeepsThePendingMetadataOperationAndItsTypedResult()=withGallery("fr") {activity ->
        val entered=CountDownLatch(1);val release=CountDownLatch(1)
        val before=files(activity);var requests=0
        activity.openConnection={url ->requests++;entered.countDown();check(release.await(10,TimeUnit.SECONDS));
            response(url,metadataCases().first().body)}
        try {
            select(activity);assertTrue(entered.await(10,TimeUnit.SECONDS))
            val config=android.content.res.Configuration(activity.resources.configuration)
            config.orientation=android.content.res.Configuration.ORIENTATION_LANDSCAPE
            activity.onConfigurationChanged(config)
            assertTrue(activity.downloading);select(activity);assertEquals(1,requests)
            release.countDown();await {!activity.downloading}
            assertFailure(activity,false,R.string.commons_metadata_ambiguous_file,before)
        } finally {release.countDown()}
    }
    @Test @Config(qualifiers="w320dp-h640dp-port-xhdpi",fontScale=1f)
    fun newReasonsRetainFullAccessibleTextInPortrait()=readable(1f,320,640)
    @Test @Config(qualifiers="w640dp-h320dp-land-xhdpi",fontScale=2f)
    fun newReasonsRetainFullAccessibleTextInLargeFontShortLandscape()=readable(2f,640,320)
    private fun readable(scale: Float,widthDp: Int,heightDp: Int) {
        for(insert in listOf(false,true)) for(tag in listOf("en-GB","fr","ar","ja","vi-Hani","mn-Mong","mnc-Mong")) withGallery(tag) {activity ->
            val before=files(activity)
            val candidates=typedFailures().take(if(insert) 9 else 7)
            // All nine English messages and a longest complete reason in each representative script.
            val cases=if(tag=="en-GB") candidates else listOf(candidates.maxBy {activity.getString(it.second).length})
            for((error,key) in cases) {
                activity.openConnection={throw error};select(activity,insert);await {!activity.downloading}
                assertFailure(activity,insert,key,before)
                val text=expected(activity,insert,activity.getString(key))
                val root=activity.window.decorView;val density=activity.resources.displayMetrics.density
                val width=(widthDp*density+.5f).toInt();val height=(heightDp*density+.5f).toInt()
                fun layoutRoot() {
                    root.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),
                        View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.EXACTLY));root.layout(0,0,width,height)
                }
                layoutRoot()
                val view=status(activity);assertEquals(scale,activity.resources.configuration.fontScale,0f)
                assertNull(view.ellipsize);assertTrue(view.isShown)
                val layout=requireNotNull(view.layout)
                assertEquals(text.length,layout.getLineEnd(layout.lineCount-1))
                assertTrue(layout.height<=view.height-view.totalPaddingTop-view.totalPaddingBottom)
                for(line in 0 until layout.lineCount) assertEquals(0,layout.getEllipsisCount(line))
                if(VerticalText.uiVertical()) {
                    val rail=view.parent as ColumnScrollView
                    val end=(view.width-rail.width+rail.paddingLeft+rail.paddingRight).coerceAtLeast(0)
                    for(position in listOf(0,end)) {
                        rail.scrollTo(position,0);val visible=android.graphics.Rect()
                        assertTrue(view.getLocalVisibleRect(visible));assertEquals(view.height,visible.height())
                        if(position==0) assertEquals(0,visible.left)
                        if(position==end) assertEquals(view.width,visible.right)
                    }
                    // A second real failure must reset reading position rather than retain the end.
                    select(activity,insert);await {!activity.downloading};layoutRoot()
                    assertEquals(if(VerticalText.uiDirection()==TextDirection.VERTICAL_RL) end else 0,rail.scrollX)
                } else if(heightDp>=640) GallerySvgReadabilityFixture.assertEntireMessageVisible(view)
                else {
                    val scroll=root.findViewWithTag<GalleryControlsScroll>("gallery_controls_scroll")
                    assertTrue(scroll.height>0)
                    val start=android.graphics.Rect();assertTrue(view.getLocalVisibleRect(start));assertEquals(0,start.top)
                    val box=android.graphics.Rect(0,0,view.width,view.height)
                    scroll.offsetDescendantRectToMyCoords(view,box);scroll.scrollTo(0,box.bottom-scroll.height)
                    val end=android.graphics.Rect();assertTrue(view.getLocalVisibleRect(end));assertEquals(view.height,end.bottom)
                    select(activity,insert);await {!activity.downloading};layoutRoot()
                    val restored=android.graphics.Rect();assertTrue(view.getLocalVisibleRect(restored));assertEquals(0,restored.top)
                }
                if(tag=="ar") assertEquals(View.LAYOUT_DIRECTION_RTL,view.layoutDirection)
                val directory=java.io.File("build/reports/commons-import-failures").apply {mkdirs()}
                val name="api35-$tag-${widthDp}x${heightDp}-font$scale-${if(insert) "insert" else "copy"}-${activity.resources.getResourceEntryName(key)}"
                val bitmap=android.graphics.Bitmap.createBitmap(width,height,android.graphics.Bitmap.Config.ARGB_8888)
                try {
                    root.draw(android.graphics.Canvas(bitmap))
                    java.io.File(directory,"$name.png").outputStream().use {
                        assertTrue(bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it))
                    }
                } finally {bitmap.recycle()}
                java.io.File(directory,"$name.json").writeText(org.json.JSONObject()
                    .put("evidence_kind","Robolectric NATIVE capture; requires visual inspection; not installed-device or TalkBack evidence")
                    .put("locale",tag).put("font_scale",scale).put("message",text)
                    .put("all_characters_laid_out",true).put("status_width",view.width).put("status_height",view.height).toString(2)+"\n")
            }
        }
    }
}
