/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.LocaleManager
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.content.res.Resources
import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Rect
import android.net.Uri
import android.os.Build
import android.os.LocaleList
import android.os.Looper
import android.view.View
import android.webkit.WebView
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
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
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.LooperMode
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.util.ReflectionHelpers
import java.io.ByteArrayInputStream
import java.io.ByteArrayOutputStream
import java.io.File
import java.net.HttpURLConnection
import java.net.URL
import java.util.Base64
import java.util.Locale
import java.util.concurrent.ConcurrentLinkedQueue
import java.util.concurrent.CountDownLatch
import java.util.concurrent.ExecutorService
import java.util.concurrent.TimeUnit

/**
 * Real WebView selection -> downloader -> ImportedImage byte classification. Only
 * HTTPS transport and JXL's native-info call are substituted; neither transport nor
 * ImportedImage throws the injected linkage failure. The successful JXL control is
 * metadata-validation coverage, not native decoding. NativeCodecTest and
 * PlatformColourImportTest retain the installed-device native success controls.
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class GalleryNativeComponentFailureTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val source="https://catrobat.org/wp-content/uploads/fixture.jxl"
    private val pngSource="https://catrobat.org/wp-content/uploads/fixture.png"
    private val jpegSource="https://catrobat.org/wp-content/uploads/fixture.jpg"
    private val existing=ImageCredit("https://catrobat.org/wp-content/uploads/existing.png",
        "Existing creator credit · Émilie · かな")
    private val clipboard get()=context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
    private var previousTag: String?=null
    private var previousInitialized: Boolean?=null
    private var previousPlatform: LocaleList?=null
    private lateinit var previousLocale: Locale
    private lateinit var previousResources: Resources
    private lateinit var previousNativeInfo: (String)->IntArray
    private val observations=ConcurrentLinkedQueue<NativeObservation>()

    private data class NativeObservation(val file: File,val bytes: ByteArray,val onWorker: Boolean)
    private class Connection(url: URL,bytes: ByteArray): HttpURLConnection(url) {
        private val input=ByteArrayInputStream(bytes)
        @Volatile var disconnected=false
        override fun connect()=Unit
        override fun disconnect() {disconnected=true;input.close()}
        override fun usingProxy()=false
        override fun getResponseCode()=200
        override fun getInputStream()=input
    }

    @Before fun prepare() {
        // selectedTag itself can migrate preferences; snapshot the raw state first.
        val preferences=context.getSharedPreferences("app-language",Context.MODE_PRIVATE)
        previousTag=preferences.getString("language-tag",null)
        previousInitialized=if(preferences.contains("platform-initialized")) preferences.getBoolean("platform-initialized",false) else null
        previousPlatform=if(Build.VERSION.SDK_INT>=33) context.getSystemService(LocaleManager::class.java)?.applicationLocales else null
        previousLocale=Locale.getDefault();previousResources=PaintApplication.currentResources
        previousNativeInfo=JxlCodec.readNativeInfo
        AppLanguage.select(context,"en-GB")
        PaintApplication.currentResources=AppLanguage.wrap(context).resources
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-") || it.name.startsWith("credit-edit-")}
            ?.forEach {it.deleteRecursively()}
        context.cacheDir.listFiles()?.filter {
            it.name.startsWith("gallery-") || it.name.startsWith("classic-import-") || it.name.startsWith("colour-input-")
        }?.forEach {it.deleteRecursively()}
        context.getSharedPreferences("classic-ui",0).edit().clear().commit()
        context.getSharedPreferences("image-credits",0).edit().clear().putString("fixture","Unchanged credit cache").commit()
        clipboard.setPrimaryClip(ClipData.newPlainText("fixture","Previous clipboard"))
    }

    @After fun restore() {
        // Every withGallery block drains its worker before this shared seam is restored.
        JxlCodec.readNativeInfo=previousNativeInfo
        ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
        if(Build.VERSION.SDK_INT>=33 && previousPlatform!=null)
            context.getSystemService(LocaleManager::class.java)?.applicationLocales=previousPlatform!!
        context.getSharedPreferences("app-language",Context.MODE_PRIVATE).edit().apply {
            if(previousTag==null) remove("language-tag") else putString("language-tag",previousTag)
            if(previousInitialized==null) remove("platform-initialized") else putBoolean("platform-initialized",previousInitialized!!)
        }.commit()
        PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
    }

    private fun await(description: String,done: ()->Boolean) {
        val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(10)
        while(!done() && System.nanoTime()<deadline) {
            shadowOf(Looper.getMainLooper()).idle();Thread.sleep(5)
        }
        shadowOf(Looper.getMainLooper()).idle()
        assertTrue("Timed out: $description",done())
    }
    private fun withGallery(run: (ActivityController<MediaGalleryActivity>,MediaGalleryActivity)->Unit) {
        val intent=Intent(context,MediaGalleryActivity::class.java)
            .putExtra("document_image_credits",ImageCredit.write(listOf(existing)).toString())
        val controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,intent).setup().visible()
        val activity=controller.get()
        activity.openConnection={error("A test must supply its fixture transport; never contact a provider")}
        try {run(controller,activity)} finally {
            if(!activity.isDestroyed) controller.pause().stop().destroy()
            await("gallery worker cleanup") {!activity.downloading}
            // A successful handback transfers ownership; clean it if an assertion
            // failed before the editor or the success-control block consumed it.
            shadowOf(activity).resultIntent?.getStringExtra("gallery_file")?.let {name ->
                if(name.startsWith("gallery-") && File(name).name==name) File(context.cacheDir,name).delete()
            }
        }
    }
    private fun withEditor(run: (ClassicPaintActivity)->Unit) {
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup().visible()
        val editor=controller.get()
        try {
            awaitEditorStartup(editor)
            editor.document.background=Color.GREEN;editor.document.newImage(32,24)
            assertTrue(editor.document.attachImageCredit(existing) {})
            editor.document.markSaved()
            run(editor)
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
            controller.pause().stop();await("editor worker cleanup") {!editor.busy};controller.destroy()
        }
    }
    private fun select(activity: MediaGalleryActivity,url: String=source) {
        val web=ReflectionHelpers.getField<WebView>(activity,"web")
        assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,url))
        shadowOf(Looper.getMainLooper()).idle()
    }
    private fun session(activity: MediaGalleryActivity)=ReflectionHelpers.getField<CreditEditSession>(activity,"creditSession")
    private fun status(activity: MediaGalleryActivity)=activity.window.decorView.findViewWithTag<TextView>("gallery_status")
    private fun jxlBytes()=Base64.getMimeDecoder().decode(
        File("src/androidTest/assets/colour-fixtures/linear16.jxl.b64").readText())
    private fun imageBytes(format: Bitmap.CompressFormat): ByteArray {
        val image=Bitmap.createBitmap(3,1,Bitmap.Config.ARGB_8888)
        image.setPixel(0,0,Color.RED);image.setPixel(1,0,Color.GREEN);image.setPixel(2,0,Color.BLUE)
        return try {
            ByteArrayOutputStream().also {assertTrue(image.compress(format,100,it))}.toByteArray()
        } finally {image.recycle()}
    }
    private fun observeNativeInfo(path: String) {
        val file=File(path)
        observations.add(NativeObservation(file,file.readBytes(),Looper.myLooper()!=Looper.getMainLooper()))
    }
    private fun assertDownloadedJxl(bytes: ByteArray,observation: NativeObservation) {
        assertTrue("Native info must run on the asynchronous download worker",observation.onWorker)
        assertEquals(context.cacheDir,observation.file.parentFile)
        assertTrue(observation.file.name.startsWith("gallery-"))
        assertTrue("The temporary suffix must not be how JXL is identified",observation.file.name.endsWith(".image"))
        assertArrayEquals("Exact downloaded JXL bytes reached native info",bytes,observation.bytes)
        val magic=observation.bytes
        val raw=magic.size>=2 && magic[0]==0xff.toByte() && magic[1]==0x0a.toByte()
        val container=magic.size>=12 && magic.copyOfRange(0,12).contentEquals(
            byteArrayOf(0,0,0,12,0x4a,0x58,0x4c,0x20,13,10,-121,10))
        assertTrue("Fixture must contain a real JXL signature",raw || container)
    }
    private fun assertCreditsUnchanged(activity: MediaGalleryActivity) {
        assertEquals(listOf(existing),session(activity).credits)
        assertFalse(session(activity).accepted);assertTrue(session(activity).edits.isEmpty())
        assertNull(session(activity).draft)
        assertEquals("Previous clipboard",clipboard.primaryClip!!.getItemAt(0).text.toString())
        assertEquals(mapOf("fixture" to "Unchanged credit cache"),context.getSharedPreferences("image-credits",0).all)
    }
    private fun assertNoTemporaryImages() {
        assertTrue("Failed/cancelled imports must remove all staged image files",
            context.cacheDir.listFiles().orEmpty().none {
                it.name.startsWith("gallery-") || it.name.startsWith("classic-import-") || it.name.startsWith("colour-input-")
            })
    }
    private fun assertNoResult(activity: MediaGalleryActivity) {
        assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
        assertNull("A failed import must not return a gallery file or credit edits",shadowOf(activity).resultIntent)
        assertFalse(activity.downloading)
        assertNoTemporaryImages();assertCreditsUnchanged(activity)
    }
    private fun assertNeutralFullMessage(activity: MediaGalleryActivity) {
        val reason=activity.getString(R.string.gallery_image_component_unavailable)
        assertEquals("A required image component is unavailable. The image was not imported.",reason)
        val expected=activity.getString(R.string.ui_could_not_load_gallery_image,reason)
        val view=status(activity)
        assertEquals(expected,view.text.toString())
        assertFalse(view.text.contains(activity.getString(R.string.colour_converter_unavailable)))
        assertEquals(expected,view.createAccessibilityNodeInfo().text.toString())
        assertEquals(View.ACCESSIBILITY_LIVE_REGION_POLITE,view.accessibilityLiveRegion)
        val root=activity.window.decorView;val density=activity.resources.displayMetrics.density
        val width=(412*density+.5f).toInt();val height=(900*density+.5f).toInt()
        root.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),
            View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.EXACTLY));root.layout(0,0,width,height)
        assertTrue(view.isShown);assertNull(view.ellipsize)
        val layout=requireNotNull(view.layout)
        assertTrue(layout.lineCount>0)
        assertEquals("Full UTF-16 message must be laid out",expected.length,layout.getLineEnd(layout.lineCount-1))
        assertTrue(layout.height<=view.height-view.totalPaddingTop-view.totalPaddingBottom)
        for(line in 0 until layout.lineCount) assertEquals(0,layout.getEllipsisCount(line))
        val visible=Rect();assertTrue(view.getGlobalVisibleRect(visible))
        assertEquals(view.width,visible.width());assertEquals(view.height,visible.height())
    }

    @Test fun nativeInfoLinkageFailuresAreNeutralRepeatableAndAllowPlatformPngRetry() = withEditor {editor ->
        val previous=editor.document.bitmap
        withGallery {_,activity ->
            val bytes=jxlBytes()
            // The selected .png name serves real JXL bytes: classification must inspect
            // the content, even when the source name suggests an ordinary platform image.
            // Model initial load failure followed by failures after JVM class initialization.
            val failures=listOf(UnsatisfiedLinkError("fixture native symbol"),
                NoClassDefFoundError("fixture failed initialization"),NoClassDefFoundError("fixture repeated initialization"))
            for((index,failure) in failures.withIndex()) {
                JxlCodec.readNativeInfo={path -> observeNativeInfo(path);throw failure}
                val connection=Connection(URL(pngSource),bytes);activity.openConnection={connection}
                select(activity,pngSource);await("native-info rejection") {!activity.downloading}
                assertEquals(index+1,observations.size)
                assertDownloadedJxl(bytes,observations.last())
                assertTrue(connection.disconnected);assertFalse(observations.last().file.exists())
                assertNoResult(activity);assertFalse(activity.isFinishing);assertNeutralFullMessage(activity)
                assertSame(previous,editor.document.bitmap);assertNull(editor.document.selection)
                assertFalse(editor.document.dirty);assertEquals(listOf(existing),editor.document.imageCredits)
                assertNull(editor.lastIoError)
            }
            // Leave the failing native seam installed. PNG bytes served under a .jxl
            // source name must bypass it and still import through the platform decoder.
            val png=imageBytes(Bitmap.CompressFormat.PNG)
            val connection=Connection(URL(source),png);activity.openConnection={connection}
            select(activity,source);await("PNG retry result") {!activity.downloading && activity.isFinishing}
            assertEquals(3,observations.size);assertTrue(connection.disconnected)
            assertEquals(Activity.RESULT_OK,shadowOf(activity).resultCode)
            val result=shadowOf(activity).resultIntent
            assertEquals(source,result.getStringExtra("gallery_source"))
            val returned=File(context.cacheDir,result.getStringExtra("gallery_file")!!)
            assertArrayEquals(png,returned.readBytes());assertCreditsUnchanged(activity)
            editor.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,result)
            await("PNG editor import") {!editor.busy}
            assertNull(editor.lastIoError);assertNotNull(editor.document.selection)
            assertEquals(Color.RED,editor.document.selection!!.image.getPixel(0,0))
            assertEquals(listOf(existing.source,source),editor.document.imageCredits.map {it.source})
            assertEquals(3,observations.size);assertFalse(returned.exists());assertNoTemporaryImages()
        }
    }

    @Test fun successfulJxlNativeInfoStubValidatesAndReturnsTheDownloadedFile() = withGallery {_,activity ->
        val bytes=jxlBytes()
        JxlCodec.readNativeInfo={path -> observeNativeInfo(path);intArrayOf(6,1,16)}
        val connection=Connection(URL(source),bytes);activity.openConnection={connection}
        select(activity);await("stubbed JXL validation result") {!activity.downloading && activity.isFinishing}
        assertEquals(Activity.RESULT_OK,shadowOf(activity).resultCode)
        assertEquals(1,observations.size);assertDownloadedJxl(bytes,observations.single())
        val result=shadowOf(activity).resultIntent
        val returned=File(context.cacheDir,result.getStringExtra("gallery_file")!!)
        try {
            assertTrue(connection.disconnected);assertTrue(returned.isFile)
            assertEquals(source,result.getStringExtra("gallery_source"))
            assertArrayEquals(bytes,returned.readBytes());assertCreditsUnchanged(activity)
            // This validates the metadata/handback branch only; no native decode is attempted.
        } finally {returned.delete()}
        assertNoTemporaryImages()
    }

    @Test fun finishingWhileNativeInfoIsPendingSuppressesLateFailureAndDeletesTheFile() =
        cancelWhileNativeInfoIsPending(destroy=false)

    @Test fun destroyingWhileNativeInfoIsPendingSuppressesLateFailureAndDeletesTheFile() =
        cancelWhileNativeInfoIsPending(destroy=true)

    private fun cancelWhileNativeInfoIsPending(destroy: Boolean) = withGallery {controller,activity ->
        val entered=CountDownLatch(1);val release=CountDownLatch(1)
        val bytes=jxlBytes()
        JxlCodec.readNativeInfo={path ->
            observeNativeInfo(path);entered.countDown()
            // Model a native call that cannot be cancelled by Thread.interrupt(). A
            // timed await here could itself cause failure and falsely pass this test.
            var interrupted=false
            while(true) {
                try {release.await();break} catch(_: InterruptedException) {interrupted=true}
            }
            if(interrupted) Thread.currentThread().interrupt()
            throw UnsatisfiedLinkError("fixture late native failure")
        }
        val connection=Connection(URL(source),bytes);activity.openConnection={connection}
        try {
            select(activity)
            assertTrue("Download must reach the native-info boundary",entered.await(10,TimeUnit.SECONDS))
            assertTrue(activity.downloading);assertEquals(1,observations.size)
            assertDownloadedJxl(bytes,observations.single())
            assertTrue(observations.single().file.isFile)
            val previousStatus=status(activity).text.toString()
            if(destroy) controller.pause().stop().destroy() else activity.finish()
            release.countDown();await("late native failure cleanup") {!activity.downloading}
            assertNoResult(activity);assertTrue(connection.disconnected)
            assertFalse(observations.single().file.exists())
            assertEquals("Late failure must not update a closed gallery",previousStatus,status(activity).text.toString())
            if(destroy) assertTrue(ReflectionHelpers.getField<ExecutorService>(activity,"worker").isShutdown)
        } finally {release.countDown()}
    }

    @Test fun unsupportedWebSelectionIsRejectedBeforeTransportOrNativeInfo() = withGallery {_,activity ->
        var connections=0;var nativeCalls=0
        activity.openConnection={connections++;Connection(it,jxlBytes())}
        JxlCodec.readNativeInfo={nativeCalls++;intArrayOf(6,1,16)}
        val unsupported=listOf("https://catrobat.org.evil.example/fixture.jxl",
            "https://catrobat.org/wp-content/uploads/fixture.exe","file:///fixture.jxl")
        for(url in unsupported) {
            val use=Uri.Builder().scheme(IllustrationPage.USE_SCHEME).authority("insert")
                .appendQueryParameter("source",url).build().toString()
            select(activity,use)
            // Join any accidentally scheduled work before checking the negative control.
            ReflectionHelpers.getField<ExecutorService>(activity,"worker").submit {}.get(10,TimeUnit.SECONDS)
            shadowOf(Looper.getMainLooper()).idle()
            assertEquals(0,connections);assertEquals(0,nativeCalls)
            assertNoResult(activity);assertFalse(activity.isFinishing)
        }
    }

    @Test fun profiledJpegValidatesInGalleryThenEditorReportsTheSpecificConverterFailure() = withEditor {editor ->
        val before=editor.document.bitmap
        val beforePixels=IntArray(before.width*before.height).also {before.getPixels(it,0,before.width,0,0,before.width,before.height)}
        var nativeInfoCalls=0
        JxlCodec.readNativeInfo={nativeInfoCalls++;throw UnsatisfiedLinkError("JXL must not inspect a JPEG")}
        withGallery {_,activity ->
            val jpeg=imageBytes(Bitmap.CompressFormat.JPEG)
            assertTrue("Use an actual profiled JPEG",jpeg.toString(Charsets.ISO_8859_1).contains("ICC_PROFILE"))
            val connection=Connection(URL(jpegSource),jpeg);activity.openConnection={connection}
            select(activity,jpegSource);await("profiled JPEG gallery validation") {!activity.downloading && activity.isFinishing}
            assertEquals(Activity.RESULT_OK,shadowOf(activity).resultCode)
            assertTrue(connection.disconnected);assertEquals(0,nativeInfoCalls)
            val result=shadowOf(activity).resultIntent
            val returned=File(context.cacheDir,result.getStringExtra("gallery_file")!!)
            assertArrayEquals(jpeg,returned.readBytes());assertCreditsUnchanged(activity)
            val inspected=ImportedImage(returned,"profiled.jpg")
            assertEquals(ImageDimensions(3,1),inspected.dimensions)
            assertTrue("Validation recognizes explicit colour metadata without JNI",
                inspected.platformColour!!.metadataWorkingBytes>0)
            // As in ClassicWorkspaceTest.unavailableColourConverterReportsErrorAndClearsBusyState,
            // Robolectric has no app anpaint_heif JNI. The real PlatformImageColour.convert
            // catches that LinkageError only during editor decode, after gallery validation.
            // This depends on the host JNI being absent; installed native success is tested
            // separately by PlatformColourImportTest. Do not inject into gallery transport.
            editor.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,result)
            await("profiled JPEG editor rejection") {!editor.busy}
            assertEquals(editor.getString(R.string.ui_could_not_open_image)+". "+
                editor.getString(R.string.colour_converter_unavailable),editor.lastIoError)
            assertFalse(editor.lastIoError!!.contains(editor.getString(R.string.gallery_image_component_unavailable)))
            assertSame(before,editor.document.bitmap);assertFalse(before.isRecycled)
            val afterPixels=IntArray(beforePixels.size).also {before.getPixels(it,0,before.width,0,0,before.width,before.height)}
            assertArrayEquals(beforePixels,afterPixels)
            assertNull(editor.document.selection);assertFalse(editor.document.dirty)
            assertEquals(listOf(existing),editor.document.imageCredits);assertEquals(0,nativeInfoCalls)
            assertFalse(returned.exists());assertNoTemporaryImages()
        }
    }

    @Test fun everyPickerLocaleResolvesTheWholeNeutralReasonOrExplicitEnglishFallback() {
        val key="gallery_image_component_unavailable"
        val fixture=JSONObject(File("../tools/fixtures/current_localization/gallery_native_component_current_wording.json").readText())
        val expected=fixture.getJSONObject("values").getJSONObject(key)
        val scope=JSONObject(File("../tools/fixtures/current_localization/locale_contract_scope.json").readText())
        fun tags(values: JSONArray)=(0 until values.length()).map {values.getString(it)}.toSet()
        val scoped=tags(scope.getJSONArray("scoped_tags"));val fallback=tags(scope.getJSONArray("fallback_tags"))
        val offered=AppLanguage.tags(context)
        assertEquals(59,scoped.size);assertEquals(112,fallback.size);assertEquals(171,offered.size)
        assertTrue(scoped.intersect(fallback).isEmpty());assertEquals(scoped+fallback,offered.toSet())
        assertEquals(listOf("cs", "sv"), tags(fixture.getJSONArray("additional_reviewed_tags")).toList())
        assertEquals(scoped+"cs"+"sv"+"default",expected.keys().asSequence().toSet())
        val constraints=fixture.getJSONObject("constraints").getJSONObject(key)
        assertEquals(0,constraints.getInt("child_elements"));assertEquals(0,constraints.getJSONObject("placeholders").length())
        assertEquals(0,constraints.getInt("escaped_newline_count"))
        assertEquals("A required image component is unavailable. The image was not imported.",expected.getString("default"))
        for(tag in offered) {
            AppLanguage.select(context,tag)
            val selected=AppLanguage.wrap(context)
            val raw=expected.getString(if(expected.has(tag)) tag else "default")
            val message=raw.replace("\\'","'").replace("\\\"","\"")
            assertEquals("Complete neutral native-component reason for $tag",message,
                selected.getString(R.string.gallery_image_component_unavailable))
            assertTrue(message.isNotBlank())
        }
        // Exact fixture/resource agreement preserves the bounded wording contract; it
        // does not certify linguistic fluency or whole-language acceptance of any locale.
    }
}
