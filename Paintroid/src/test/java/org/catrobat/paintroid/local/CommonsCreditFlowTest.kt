/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.content.res.Configuration
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.net.Uri
import android.os.Looper
import android.webkit.WebView
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Before
import org.junit.After
import java.util.Locale
import android.content.res.Resources
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowDialog
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.shadows.ShadowToast
import org.robolectric.util.ReflectionHelpers
import java.io.ByteArrayInputStream
import java.io.File
import java.io.InputStream
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CommonsCreditFlowTest {
    private val source="https://upload.wikimedia.org/wikipedia/commons/a/ab/Test_map.svg"
    private val page="https://commons.wikimedia.org/wiki/File:Test_map.svg"
    private val svg="""<svg xmlns="http://www.w3.org/2000/svg" width="40" height="24"><rect x="4" y="4" width="30" height="16" fill="none" stroke="black"/></svg>"""
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private lateinit var previousTag: String
    private lateinit var previousLocale: Locale
    private lateinit var previousResources: Resources
    private fun selectLanguage(tag: String) {
        AppLanguage.select(context,tag)
        PaintApplication.currentResources=AppLanguage.wrap(context).resources
    }
    @After fun restoreLanguage() {
        AppLanguage.select(context,previousTag)
        PaintApplication.currentResources=previousResources
        Locale.setDefault(previousLocale)
    }
    @Before fun clear() {
        previousTag=AppLanguage.selectedTag(context)
        previousLocale=Locale.getDefault()
        previousResources=PaintApplication.currentResources
        selectLanguage("en-US")
        context.getSharedPreferences("image-credits",0).edit().clear().commit()
        context.getSharedPreferences("commons-attribution-v1",0).edit().clear().commit()
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-") || it.name.startsWith("credit-edit-")}
            ?.forEach {it.deleteRecursively()}
        File(context.filesDir,"retained-image-credits").deleteRecursively()
        context.cacheDir.listFiles()?.filter {it.name.startsWith("gallery-")}?.forEach {it.delete()}
    }
    private class Connection(url: URL,private val input: InputStream,private val status: Int=200): HttpURLConnection(url) {
        var disconnected=false
        override fun connect()=Unit
        override fun disconnect() {disconnected=true;input.close()}
        override fun usingProxy()=false
        override fun getResponseCode()=status
        override fun getInputStream()=input
    }
    private fun gallery(credits: List<ImageCredit> = emptyList())=Robolectric.buildActivity(MediaGalleryActivity::class.java,
        Intent(context,MediaGalleryActivity::class.java).putExtra("gallery_provider",IllustrationSource.COMMONS.name)
            .putExtra("document_image_credits",ImageCredit.write(credits).toString())).setup()
    private fun gallery(main: ClassicPaintActivity): ActivityController<MediaGalleryActivity> {
        // Use the editor's real launch so accepted results have its exact ownership token.
        ReflectionHelpers.callInstanceMethod<Void>(main,"showOtherImages")
        val dialog=ShadowAlertDialog.getLatestAlertDialog()
        val position=IllustrationSource.values().indexOf(IllustrationSource.COMMONS)+1
        dialog.listView.performItemClick(null,position,position.toLong())
        shadowOf(Looper.getMainLooper()).idle()
        val request=shadowOf(main).nextStartedActivityForResult
        assertNotNull("The source picker must open Commons",request)
        assertEquals(ClassicPaintActivity.GALLERY_IMAGE,request.requestCode)
        assertEquals(IllustrationSource.COMMONS.name,request.intent.getStringExtra("gallery_provider"))
        assertNotNull(request.intent.getStringExtra(CreditEditSession.EXTRA_SESSION))
        return Robolectric.buildActivity(MediaGalleryActivity::class.java,request.intent).setup()
    }
    private fun session(activity: MediaGalleryActivity): CreditEditSession {
        val token=ReflectionHelpers.getField<CreditEditSession>(activity,"creditSession").token
        return CreditEditSession.open(activity.filesDir,token)
    }
    private fun fixtureConnections(activity: MediaGalleryActivity,artist: String="Mapper A") {
        activity.openConnection={url ->Connection(url,ByteArrayInputStream((if(url.host=="commons.wikimedia.org")
            CommonsTestMetadata.response(source,page,artist) else svg).toByteArray()))}
    }
    private fun select(activity: MediaGalleryActivity,copy: Boolean=false) {
        val web=ReflectionHelpers.getField<WebView>(activity,"web")
        val action=Uri.Builder().scheme(if(copy) GalleryPage.CREDIT_SCHEME else IllustrationPage.USE_SCHEME)
            .authority(if(copy) "copy" else "insert").appendQueryParameter("source",source)
            .appendQueryParameter("page",page).appendQueryParameter("title","Test blank map").build()
        assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,action.toString()))
    }
    private fun await(done: ()->Boolean) {
        val limit=System.nanoTime()+TimeUnit.SECONDS.toNanos(12)
        while(!done() && System.nanoTime()<limit) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(5)}
        shadowOf(Looper.getMainLooper()).idle();assertTrue("Operation timed out",done())
    }
    private fun clipboard()=(context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).primaryClip!!.getItemAt(0).text.toString()
    private fun storedCredit(): ImageCredit {
        val record=CommonsAttribution.parse(CommonsTestMetadata.response(source,page),source)
        CommonsAttribution.cache(context,record)
        return ImageCredit(source,record.text(true))
    }
    @Test fun metadataAndImageRequestsUseTheInstalledApplicationVersion() {
        val info=context.packageManager.getPackageInfo(context.packageName,0)
        val originalVersion=info.versionName
        info.versionName="91.2-regression"
        shadowOf(context.packageManager).installPackage(info)
        val controller=gallery();val activity=controller.get()
        val connections=mutableListOf<Connection>()
        try {
            activity.openConnection={url ->
                Connection(url,ByteArrayInputStream((if(url.host=="commons.wikimedia.org")
                    CommonsTestMetadata.response(source,page) else svg).toByteArray())).also {connections.add(it)}
            }
            select(activity);await {activity.isFinishing && !activity.downloading}
            assertEquals(setOf("commons.wikimedia.org","upload.wikimedia.org"),connections.map {it.url.host}.toSet())
            assertEquals(2,connections.size)
            for(connection in connections) assertEquals(
                "AN-Paint/91.2-regression (https://github.com/c933103/AN-Paint; Android)",
                connection.getRequestProperty("User-Agent"))
        } finally {
            controller.pause().stop().destroy()
            info.versionName=originalVersion
            shadowOf(context.packageManager).installPackage(info)
        }
    }

    @Test fun copyFromFileFetchesOnlyMetadataAndDoesNotRecordInsertion() {
        selectLanguage("fr")
        val controller=gallery();val activity=controller.get();var count=0
        try {
            activity.openConnection={url ->
                assertEquals("commons.wikimedia.org",url.host);count++
                Connection(url,ByteArrayInputStream(CommonsTestMetadata.response(source,page).toByteArray()))
            }
            select(activity,copy=true);await {!activity.downloading}
            assertEquals(1,count);assertTrue(clipboard().contains("Mapper A"));assertTrue(clipboard().contains("by-sa/3.0/"))
            assertFalse(clipboard().contains("antiAlias=false"));assertTrue(session(activity).credits.isEmpty())
            assertFalse(clipboard().contains("AN Paint:"));assertFalse(clipboard().contains("background=#FFFFFF"))
            assertEquals(CommonsAttribution.cached(context,source)!!.text(false),clipboard())
            assertFalse(session(activity).accepted);assertFalse(activity.isFinishing)
            assertTrue(activity.cacheDir.listFiles()!!.none {it.name.startsWith("gallery-")})
            assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
        } finally {controller.pause().stop().destroy()}
    }
    @Test fun actualGalleryToEditorInsertionRetainsCopyableCreditsAfterReopening() {
        selectLanguage("fr")
        val controller=gallery();val activity=controller.get()
        try {
            fixtureConnections(activity)
            select(activity);await {activity.isFinishing && !activity.downloading}
            assertTrue(session(activity).credits.isEmpty());assertFalse(session(activity).accepted)
            assertEquals(session(activity).token,shadowOf(activity).resultIntent.getStringExtra(CreditEditSession.EXTRA_SESSION))
            val mainController=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
            val main=mainController.get()
            try {
                awaitEditorStartup(main)
                main.document.newImage(40,24)
                assertTrue(main.document.imageCredits.isEmpty())
                main.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,shadowOf(activity).resultIntent)
                await {!main.busy};assertNull(main.lastIoError);assertNotNull(main.document.selection)
                assertEquals(40,main.document.selection!!.image!!.width)
                assertEquals(24,main.document.selection!!.image!!.height)
                assertEquals(listOf(source),main.document.imageCredits.map {it.source})
                val credit=ImageCredit.text(main.document.imageCredits)
                for(text in listOf("Mapper A","Mapper B","by-sa/3.0/",source,page,"antiAlias=false")) assertTrue(credit.contains(text))
                assertTrue(credit.lines().contains("AN Paint: SVG → PNG; taille d’origine; antiAlias=false; strokeDashArray=none; background=#FFFFFF."))
                main.document.finishSelection()
                // A later UI language does not rewrite the document's already generated credit.
                selectLanguage("ja")
                AppLanguage.refresh(main)
                val reopened=gallery(main)
                try {
                    reopened.get().openConnection={error("Stored credits must copy offline")}
                    reopened.get().window.decorView.findViewWithTag<Button>("gallery_copy_credits").performClick()
                    assertEquals(credit,clipboard())
                    assertEquals(main.document.imageCredits,session(reopened.get()).credits)
                    assertFalse(session(reopened.get()).accepted)
                } finally {reopened.pause().stop().destroy()}
            } finally {mainController.pause().stop();await {!main.busy};mainController.destroy()}
        } finally {controller.pause().stop().destroy()}
    }
    private fun setClipboard(text: String) {
        (context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager)
            .setPrimaryClip(ClipData.newPlainText("credit test",text))
    }
    private fun assertNoCreditTextMessage(activity: MediaGalleryActivity) {
        val message=activity.window.decorView.findViewWithTag<TextView>("locale_notification_text")?.text?.toString()
            ?: ShadowToast.getTextOfLatestToast()
        assertEquals("No image credit text is available.",message)
        assertEquals(activity.getString(R.string.ui_no_gallery_images_have_been_inserted),message)
    }
    @Test fun everyPickerLocaleResolvesCompleteEmptyCreditTextOrEnglishFallback() {
        val fixture=JSONObject(File("../tools/fixtures/current_localization/gallery_empty_credit_current_wording.json").readText())
        val expected=fixture.getJSONObject("values").getJSONObject("ui_no_gallery_images_have_been_inserted")
        val scope=JSONObject(File("../tools/fixtures/current_localization/locale_contract_scope.json").readText())
        val fallback=scope.getJSONArray("fallback_tags").let { values ->
            (0 until values.length()).map { values.getString(it) }.toSet()
        }
        for(tag in AppLanguage.tags(context)) {
            AppLanguage.select(context,tag)
            val selected=AppLanguage.wrap(context)
            val raw=if(tag in fallback) expected.getString("default") else expected.getString(tag)
            val message=raw.replace("\\'", "'").replace("\\\"", "\"")
            assertEquals("Complete empty-credit message for $tag",message,
                selected.getString(R.string.ui_no_gallery_images_have_been_inserted))
        }
    }
    @Test fun initiallyEmptyCreditCopyAndEditorDescribeTextAndLeaveClipboardUntouched() {
        val controller=gallery();val activity=controller.get()
        try {
            activity.openConnection={error("An empty credit action must work offline")}
            setClipboard("Keep the existing clipboard")
            activity.window.decorView.findViewWithTag<Button>("gallery_copy_credits").performClick()
            assertNoCreditTextMessage(activity)
            assertEquals("Keep the existing clipboard",clipboard())
            ShadowToast.reset()
            activity.window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick()
            assertNoCreditTextMessage(activity)
            assertNull(ReflectionHelpers.getField<GalleryCredits.EditorSession>(activity,"creditEditor"))
            assertEquals("Keep the existing clipboard",clipboard())
            assertTrue(session(activity).credits.isEmpty())
            assertFalse(session(activity).accepted)
            assertFalse(activity.isFinishing)
        } finally {controller.pause().stop().destroy();ShadowToast.reset()}
    }
    @Test fun insertedImageThenSavedEmptyCreditReportsUnavailableTextAfterGalleryReentry() =
        insertedImageThenSavedBlankCredit("")

    @Test fun insertedImageThenSavedWhitespaceCreditPreservesRawEditAndReportsUnavailableText() =
        insertedImageThenSavedBlankCredit(" \n\t ")

    private fun insertedImageThenSavedBlankCredit(blankText: String) {
        val mainController=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        val main=mainController.get()
        try {
            awaitEditorStartup(main);main.document.newImage(40,24)
            val first=gallery(main)
            try {
                fixtureConnections(first.get())
                select(first.get());await {first.get().isFinishing && !first.get().downloading}
                assertEquals(Activity.RESULT_OK,shadowOf(first.get()).resultCode)
                // The download gallery has finished; insertion happens only after its result returns.
                main.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,shadowOf(first.get()).resultCode,shadowOf(first.get()).resultIntent)
                await {!main.busy};assertNull(main.lastIoError);assertNotNull(main.document.selection)
                assertEquals(40,main.document.selection!!.image!!.width)
                assertEquals(24,main.document.selection!!.image!!.height)
                main.document.finishSelection()
            } finally {first.pause().stop().destroy()}
            val original=main.document.imageCredits.single()
            assertEquals(source,original.source);assertTrue(original.text.isNotBlank())
            val pixels=main.document.bitmap.copy(Bitmap.Config.ARGB_8888,false)
            try {
                // Reopen through the editor's source picker with this document's ownership session.
                val reopened=gallery(main);val activity=reopened.get()
                try {
                    activity.openConnection={error("Stored credit edit/copy must work offline")}
                    activity.window.decorView.findViewWithTag<Button>("gallery_copy_credits").performClick()
                    assertEquals(original.text,clipboard()) // Nonempty Copy all control.
                    assertFalse(session(activity).accepted)
                    activity.window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick()
                    shadowOf(Looper.getMainLooper()).idle()
                    val dialog=ShadowAlertDialog.getLatestAlertDialog()
                    val field=dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text")
                    assertEquals(original.text,field.text.toString())
                    field.setText(blankText)
                    dialog.window!!.decorView.findViewWithTag<Button>("gallery_credit_save").performClick()
                    assertTrue(dialog.isShowing)
                    assertTrue(session(activity).accepted)
                    assertEquals(listOf(original.copy(text=blankText)),session(activity).credits)
                    dialog.window!!.decorView.findViewWithTag<Button>("gallery_credit_done").performClick()
                    assertFalse(dialog.isShowing)
                    assertEquals("",ImageCredit.text(session(activity).credits))
                    setClipboard("Keep the existing clipboard")
                    activity.window.decorView.findViewWithTag<Button>("gallery_copy_credits").performClick()
                    assertNoCreditTextMessage(activity)
                    assertEquals("Keep the existing clipboard",clipboard())
                    assertFalse(activity.isFinishing)
                    activity.window.decorView.findViewWithTag<Button>("gallery_done").performClick()
                    assertTrue(activity.isFinishing)
                    assertEquals(Activity.RESULT_OK,shadowOf(activity).resultCode)
                    main.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,shadowOf(activity).resultCode,shadowOf(activity).resultIntent)
                    assertEquals(listOf(original.copy(text=blankText)),main.document.imageCredits)
                    assertNull(main.document.selection)
                    assertTrue("Editing attribution must not remove or alter the inserted image",pixels.sameAs(main.document.bitmap))
                } finally {reopened.pause().stop().destroy()}
                val persisted=gallery(main)
                try {
                    persisted.get().window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick()
                    val dialog=ShadowAlertDialog.getLatestAlertDialog()
                    assertTrue("A source with blank credit text remains editable",dialog.isShowing)
                    assertEquals(blankText,dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").text.toString())
                    dialog.cancel()
                } finally {persisted.pause().stop().destroy()}
            } finally {pixels.recycle()}
        } finally {mainController.pause().stop();await {!main.busy};mainController.destroy();ShadowToast.reset()}
    }
    @Test fun explicitSingleCreditCopyStillAcceptsAndCopiesAnEmptyField() {
        val original=storedCredit();val controller=gallery(listOf(original));val activity=controller.get()
        try {
            setClipboard("previous text")
            activity.window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick()
            // The dialog's onShow callback installs the tagged Copy button and listener.
            shadowOf(Looper.getMainLooper()).idle()
            val dialog=ShadowAlertDialog.getLatestAlertDialog()
            dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").setText("")
            dialog.window!!.decorView.findViewWithTag<Button>("gallery_credit_copy").performClick()
            assertEquals("",clipboard())
            assertTrue(session(activity).accepted)
            assertEquals(listOf(original.copy(text="")),session(activity).credits)
            assertTrue(dialog.isShowing)
            dialog.cancel()
        } finally {controller.pause().stop().destroy();ShadowToast.reset()}
    }
    @Test fun failedEditorDecodeCannotAttachCachedMetadataOrChangeTheDrawing() {
        val controller=gallery();val activity=controller.get()
        try {
            fixtureConnections(activity)
            select(activity);await {activity.isFinishing && !activity.downloading}
            val result=shadowOf(activity).resultIntent
            val file=File(activity.cacheDir,result.getStringExtra("gallery_file")!!)
            assertNotNull(CommonsAttribution.cached(context,source));assertTrue(session(activity).credits.isEmpty())
            file.writeText("Corrupt image after a valid download and metadata snapshot")
            val mainController=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
            val main=mainController.get()
            try {
                awaitEditorStartup(main)
                main.document.background=Color.GREEN;main.document.newImage(40,24)
                main.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,result)
                await {!main.busy}
                assertNotNull(main.lastIoError);assertNull(main.document.selection)
                assertTrue(main.document.imageCredits.isEmpty())
                assertEquals(40,main.document.bitmap.width);assertEquals(24,main.document.bitmap.height)
                assertEquals(Color.GREEN,main.document.bitmap.getPixel(0,0))
            } finally {mainController.pause().stop();await {!main.busy};mainController.destroy();file.delete()}
        } finally {controller.pause().stop().destroy()}
    }
    @Test fun rotationKeepsTheSameDownloadAndOriginalDimensions() {
        val controller=gallery();val activity=controller.get()
        val started=CountDownLatch(1);val release=CountDownLatch(1);var files=0;var metadata=0
        try {
            activity.openConnection={url ->
                if(url.host=="commons.wikimedia.org") {metadata++;Connection(url,ByteArrayInputStream(CommonsTestMetadata.response(source,page).toByteArray()))}
                else {
                    files++
                    Connection(url,object: ByteArrayInputStream(svg.toByteArray()) {
                        override fun read(buffer: ByteArray,offset: Int,length: Int): Int {
                            started.countDown();check(release.await(8,TimeUnit.SECONDS));return super.read(buffer,offset,length)
                        }
                    })
                }
            }
            select(activity);assertTrue(started.await(5,TimeUnit.SECONDS))
            val landscape=Configuration(activity.resources.configuration).apply {orientation=Configuration.ORIENTATION_LANDSCAPE;screenWidthDp=900;screenHeightDp=412}
            controller.configurationChange(landscape)
            assertSame(activity,controller.get());assertFalse(activity.isDestroyed);assertTrue(activity.downloading)
            release.countDown();await {activity.isFinishing && !activity.downloading}
            assertEquals(1,files);assertEquals(1,metadata)
            val file=File(activity.cacheDir,shadowOf(activity).resultIntent.getStringExtra("gallery_file")!!)
            try {
                val bitmap=BitmapFactory.decodeFile(file.path)
                try {assertEquals(40,bitmap.width);assertEquals(24,bitmap.height)} finally {bitmap.recycle()}
            } finally {file.delete()}
        } finally {release.countDown();controller.pause().stop().destroy()}
    }
    @Test fun emptyUnconfirmedCreditDraftSurvivesRecreationWithoutOverwritingSavedText() {
        val original=storedCredit()
        val controller=gallery(listOf(original))
        try {
            controller.get().window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick()
            shadowOf(Looper.getMainLooper()).idle()
            ShadowDialog.getLatestDialog().window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").setText("")
            controller.recreate();shadowOf(Looper.getMainLooper()).idle()
            val dialog=ShadowDialog.getLatestDialog()
            assertTrue(dialog.isShowing)
            assertEquals("",dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").text.toString())
            assertEquals(listOf(original),session(controller.get()).credits)
            assertEquals(GalleryCredits.EditorDraft(source,""),session(controller.get()).draft)
            assertFalse(session(controller.get()).accepted)
            assertEquals(Activity.RESULT_CANCELED,shadowOf(controller.get()).resultCode)
            dialog.cancel();shadowOf(Looper.getMainLooper()).idle()
            controller.recreate();shadowOf(Looper.getMainLooper()).idle()
            assertFalse(ShadowDialog.getLatestDialog().isShowing)
            assertEquals(listOf(original),session(controller.get()).credits)
            assertNull(session(controller.get()).draft);assertFalse(session(controller.get()).accepted)
        } finally {controller.pause().stop().destroy()}
    }
    @Test fun editedCreditIsCopiedExactlyAndSurvivesBothRecreationAndReinsertion() {
        val original=storedCredit();val edited="Émilie · かな · 𠀀\nCustom attribution and changes."
        val mainController=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        val main=mainController.get()
        try {
            awaitEditorStartup(main);main.document.newImage(40,24)
            assertTrue(main.document.paste(Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888),true,listOf(original)))
            main.document.finishSelection()
            val controller=gallery(main)
            try {
                val token=controller.get().intent.getStringExtra(CreditEditSession.EXTRA_SESSION)
                controller.get().window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick()
                shadowOf(Looper.getMainLooper()).idle()
                var dialog=ShadowDialog.getLatestDialog()
                dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").setText(edited)
                controller.recreate();shadowOf(Looper.getMainLooper()).idle();dialog=ShadowDialog.getLatestDialog()
                assertEquals(edited,dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").text.toString())
                assertEquals(listOf(original),session(controller.get()).credits)
                dialog.window!!.decorView.findViewWithTag<Button>("gallery_credit_copy").performClick()
                shadowOf(Looper.getMainLooper()).idle()
                assertEquals(edited,clipboard());assertEquals(listOf(original.copy(text=edited)),session(controller.get()).credits)
                assertTrue(session(controller.get()).accepted)
                assertEquals(token,shadowOf(controller.get()).resultIntent.getStringExtra(CreditEditSession.EXTRA_SESSION))
                controller.recreate();shadowOf(Looper.getMainLooper()).idle();dialog=ShadowDialog.getLatestDialog()
                assertEquals(edited,dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").text.toString())
                assertEquals(edited,ImageCredit.text(session(controller.get()).credits))
                dialog.cancel();shadowOf(Looper.getMainLooper()).idle()
                controller.get().window.decorView.findViewWithTag<Button>("gallery_done").performClick()
                assertEquals(Activity.RESULT_OK,shadowOf(controller.get()).resultCode)
                main.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,shadowOf(controller.get()).resultIntent)
                assertEquals(listOf(original.copy(text=edited)),main.document.imageCredits)
            } finally {controller.pause().stop().destroy()}
            selectLanguage("ja")
            AppLanguage.refresh(main)
            val reinserted=gallery(main)
            try {
                val token=reinserted.get().intent.getStringExtra(CreditEditSession.EXTRA_SESSION)
                fixtureConnections(reinserted.get(),artist="Updated Mapper")
                select(reinserted.get());await {reinserted.get().isFinishing && !reinserted.get().downloading}
                val result=shadowOf(reinserted.get()).resultIntent
                assertEquals(token,result.getStringExtra(CreditEditSession.EXTRA_SESSION))
                assertEquals(listOf(original.copy(text=edited)),session(reinserted.get()).credits)
                assertTrue(CommonsAttribution.cached(context,source)!!.text(false).contains("Updated Mapper"))
                main.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,result)
                await {!main.busy};assertNull(main.lastIoError);assertNotNull(main.document.selection)
                main.document.finishSelection()
                assertEquals(listOf(original.copy(text=edited)),main.document.imageCredits)
                assertEquals(edited,ImageCredit.text(main.document.imageCredits))
            } finally {reinserted.pause().stop().destroy()}
        } finally {mainController.pause().stop();await {!main.busy};mainController.destroy()}
    }
    @Test fun metadataFailureCleansUpTheImageAndDoesNotAddCredits() {
        val controller=gallery();val activity=controller.get()
        try {
            activity.openConnection={url ->Connection(url,ByteArrayInputStream(svg.toByteArray()),if(url.host=="commons.wikimedia.org") 503 else 200)}
            select(activity);await {!activity.downloading}
            assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode);assertFalse(activity.isFinishing)
            assertTrue(session(activity).credits.isEmpty());assertFalse(session(activity).accepted)
            assertTrue(activity.cacheDir.listFiles()!!.none {it.name.startsWith("gallery-")})
        } finally {controller.pause().stop().destroy()}
    }
}
