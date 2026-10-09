/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.*
import android.content.pm.ProviderInfo
import android.database.Cursor
import android.net.Uri
import android.os.Bundle
import android.os.Looper
import android.os.Parcel
import android.os.ParcelFileDescriptor
import android.widget.Button
import android.widget.Spinner
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.LegacyImageCredits
import org.catrobat.paintroid.classic.LegacyImageCreditsActivity
import org.catrobat.paintroid.classic.ImageCreditTextPages
import org.catrobat.paintroid.classic.ImageCreditArchive
import org.catrobat.paintroid.classic.ImageCredit
import org.catrobat.paintroid.classic.CreditEditSession
import org.catrobat.paintroid.classic.MediaGalleryActivity
import org.json.JSONArray
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
import org.robolectric.annotation.LooperMode
import org.robolectric.shadows.ShadowContentResolver
import java.io.File
import java.io.IOException
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
@LooperMode(LooperMode.Mode.PAUSED)
class LegacyImageCreditsActivityTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val preferences get()=context.getSharedPreferences("image-credits",Context.MODE_PRIVATE)
    private lateinit var controller: ActivityController<LegacyImageCreditsActivity>
    private val activity get()=controller.get()
    private val source="https://example.org/old.png"
    private val second="https://example.org/second.png"
    private fun seed(text: String) {
        assertTrue(preferences.edit().putStringSet("sources",setOf(source,second))
            .putString("generated:$source","Original generated source")
            .putString("text:$source",text).putString("text:$second","").commit())
    }
    private fun launch(state: Bundle?=null) {
        controller=Robolectric.buildActivity(LegacyImageCreditsActivity::class.java)
        controller.create(state).start().resume().visible()
        shadowOf(Looper.getMainLooper()).idle()
    }
    private fun click(tag: String) {
        assertTrue(activity.window.decorView.findViewWithTag<Button>(tag).performClick())
        shadowOf(Looper.getMainLooper()).idle()
    }
    private fun text()=activity.window.decorView.findViewWithTag<TextView>("legacy_credit_text")
    private fun saveAndDestroy(): Bundle {
        val state=Bundle();controller.saveInstanceState(state).pause().stop().destroy();return state
    }
    private fun parcelSize(bundle: Bundle): Int = Parcel.obtain().let {parcel ->
        try {parcel.writeBundle(bundle);parcel.dataSize()} finally {parcel.recycle()}
    }
    @Before fun start() {preferences.edit().clear().commit();File(context.filesDir,"retained-image-credits").deleteRecursively()}
    @After fun cleanup() {
        if(::controller.isInitialized && !activity.isDestroyed)controller.pause().stop().destroy()
        preferences.edit().clear().commit();File(context.filesDir,"retained-image-credits").deleteRecursively()
    }

    @Test fun exactLegacyTextIsReadableAndOnlyExplicitSelectionReturnsAFixedSizeToken() {
        val original=" Edited creator\nOriginal source \uD86D\uDC40\n"
        seed(original);val before=preferences.all;launch()
        assertEquals(original,text().text.toString());assertFalse(text().isTextSelectable)
        assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
        assertNull(shadowOf(activity).resultIntent)
        activity.window.decorView.findViewWithTag<Spinner>("legacy_credit_source").setSelection(1)
        shadowOf(Looper.getMainLooper()).idle();assertEquals("",text().text.toString())
        click("legacy_credit_add")
        val result=shadowOf(activity).resultIntent
        assertEquals(Activity.RESULT_OK,shadowOf(activity).resultCode)
        assertEquals(setOf(LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN),result.extras!!.keySet())
        assertEquals(ImageCreditArchive.selectionToken(ImageCredit(second,"")),result.getStringExtra(LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN))
        assertTrue(parcelSize(result.extras!!)<1024)
        assertEquals(before,preferences.all)
    }

    @Test fun registeredExportProviderWritesAndClosesEveryUtf8Byte() {
        val original="\uD86D\uDC40\"\\\n".repeat(50_000)
        val output=File(context.cacheDir,"legacy-credit-resolver-control.txt")
        val provider=OutputProvider().apply {
            file=output;attachInfo(this@LegacyImageCreditsActivityTest.context,ProviderInfo().apply {authority="legacy.fixture"})
        }
        assertSame(context,provider.context)
        ShadowContentResolver.registerProviderInternal("legacy.fixture",provider)
        val resolver=context.contentResolver
        val executor=Executors.newSingleThreadExecutor()
        try {
            // Future.get exposes resolver/write/close failures with their original cause.
            executor.submit<Unit> {
                val stream=resolver.openOutputStream(Uri.parse("content://legacy.fixture/text"),"wt")
                    ?: throw IOException("No output stream")
                stream.writer(Charsets.UTF_8).use {it.write(original)}
            }.get(5,TimeUnit.SECONDS)
            assertArrayEquals(original.toByteArray(Charsets.UTF_8),output.readBytes())
        } finally {executor.shutdownNow()}
    }

    @Test fun oversizedArchiveRecreationAndExportKeepRawTextOutOfBinderStateAndWriteEveryByte() {
        val oversized="\uD86D\uDC40\"\\\n".repeat(50_000)
        seed(oversized);val before=preferences.all;launch()
        val pages=ImageCreditTextPages(oversized)
        assertEquals(pages.text(0),text().text.toString());assertFalse(text().isTextSelectable)
        assertTrue(text().text.length<=ImageCreditTextPages.PAGE_CHARS)
        click("legacy_credit_next");assertEquals(pages.text(1),text().text.toString())
        click("legacy_credit_export")
        val request=shadowOf(activity).nextStartedActivityForResult
        assertEquals(Intent.ACTION_CREATE_DOCUMENT,request.intent.action)
        assertEquals("text/plain",request.intent.type)
        assertTrue(parcelSize(request.intent.extras!!)<1024)
        val state=saveAndDestroy()
        assertTrue("Archive text must never enter Activity saved state",parcelSize(state)<16_384)
        launch(state);assertEquals(pages.text(1),text().text.toString())
        val output=File(context.cacheDir,"legacy-credit-export.txt")
        val provider=OutputProvider().apply {
            file=output;attachInfo(this@LegacyImageCreditsActivityTest.context,ProviderInfo().apply {authority="legacy.fixture"})
        }
        ShadowContentResolver.registerProviderInternal("legacy.fixture",provider)
        activity.onActivityResult(LegacyImageCreditsActivity.EXPORT_TEXT,Activity.RESULT_OK,
            Intent().setData(Uri.parse("content://legacy.fixture/text")))
        val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(5)
        val status=activity.window.decorView.findViewWithTag<TextView>("legacy_credit_status")
        while(status.text.toString()!=activity.getString(R.string.gallery_credit_saved) && System.nanoTime()<deadline) {
            shadowOf(Looper.getMainLooper()).idle();Thread.sleep(5)
        }
        assertEquals(activity.getString(R.string.gallery_credit_saved),status.text.toString())
        assertArrayEquals(oversized.toByteArray(Charsets.UTF_8),output.readBytes())
        assertEquals(before,preferences.all)
    }

    @Test fun invalidOrSelfTargetingExportResultCannotOverwritePrivateDraftOrArchivedCredits() {
        seed("Legacy text");val beforePreferences=preferences.all
        val retained=ImageCreditArchive.retainAccepted(context,listOf(ImageCredit(source,"Legacy text")))
        val archiveFile=File(context.filesDir,"retained-image-credits/$retained.json")
        val beforeArchive=archiveFile.readBytes()
        val draft=File(context.filesDir,"classic-autosave.zip")
        val priorDraft=if(draft.exists())draft.readBytes() else null
        val sentinel=byteArrayOf(0x50,0x4b,3,4,17,31,63,127)
        draft.writeBytes(sentinel)
        try {
            launch()
            val selfAuthority="${activity.packageName}.fileprovider"
            for(uri in listOf(Uri.fromFile(draft),
                Uri.parse("content://$selfAuthority/shared_images/export.txt"),
                Uri.parse("content://0@$selfAuthority/shared_images/export.txt"))) {
                click("legacy_credit_export")
                activity.onActivityResult(LegacyImageCreditsActivity.EXPORT_TEXT,Activity.RESULT_OK,Intent().setData(uri))
                shadowOf(Looper.getMainLooper()).idle()
                assertEquals(activity.getString(R.string.ui_could_not_complete_the_operation),
                    activity.window.decorView.findViewWithTag<TextView>("legacy_credit_status").text.toString())
                assertArrayEquals(sentinel,draft.readBytes())
                assertArrayEquals(beforeArchive,archiveFile.readBytes())
                assertEquals(beforePreferences,preferences.all)
                assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
            }
        } finally {
            if(priorDraft==null)draft.delete() else draft.writeBytes(priorDraft)
            ImageCreditArchive.releaseAccepted(context,retained)
        }
    }

    @Test fun cancellingArchiveOrFilePickerDoesNotAttachDeleteOrTruncateRecords() {
        seed("Stored credit");val before=preferences.all;launch()
        click("legacy_credit_export")
        activity.onActivityResult(LegacyImageCreditsActivity.EXPORT_TEXT,Activity.RESULT_CANCELED,null)
        assertNull(shadowOf(activity).resultIntent)
        click("legacy_credit_done")
        assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
        assertEquals(before,preferences.all)
    }

    @Test fun retainedAcceptedVersionsAreSelectableWithoutLegacyPreferencesAndRestoreByImmutableRecordToken() {
        val first=ImageCreditArchive.retainAccepted(context,listOf(ImageCredit(source,"First accepted version")))
        val second=ImageCreditArchive.retainAccepted(context,listOf(ImageCredit(source,"Second accepted version")))
        val records=ImageCreditArchive.records(context)
        val chosen=records.last();val discarded=if(chosen.credit.text=="First accepted version") second else first
        launch()
        activity.window.decorView.findViewWithTag<Spinner>("legacy_credit_source").setSelection(1)
        shadowOf(Looper.getMainLooper()).idle();assertEquals(chosen.credit.text,text().text.toString())
        val state=saveAndDestroy()
        ImageCreditArchive.releaseAccepted(context,discarded)
        launch(state)
        assertEquals(chosen.credit.text,text().text.toString())
        click("legacy_credit_add")
        val result=shadowOf(activity).resultIntent
        assertEquals(chosen.token,result.getStringExtra(LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN))
        assertEquals(chosen.credit,ImageCreditArchive.find(context,chosen.token))
        assertTrue(preferences.all.isEmpty())
    }

    @Test fun galleryExposesTheArchiveAndForwardsOnlyTheChosenIdentifierAlongsideModernEdits() {
        seed("Legacy text")
        val modern=ImageCredit("https://example.org/current.png","Modern text")
        val gallery=Robolectric.buildActivity(MediaGalleryActivity::class.java,
            Intent(context,MediaGalleryActivity::class.java)
                .putExtra("document_image_credits",ImageCredit.write(listOf(modern)).toString()))
        try {
            val screen=gallery.create().start().resume().visible().get()
            shadowOf(Looper.getMainLooper()).idle()
            assertTrue(screen.window.decorView.findViewWithTag<Button>("gallery_legacy_credits").performClick())
            val request=shadowOf(screen).nextStartedActivityForResult
            assertEquals(LegacyImageCreditsActivity::class.java.name,request.intent.component!!.className)
            assertNull("Navigation must not transport the raw archive",request.intent.extras)
            val token=ImageCreditArchive.selectionToken(ImageCredit(source,"Legacy text"))
            screen.onActivityResult(request.requestCode,Activity.RESULT_OK,
                Intent().putExtra(LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN,token))
            val result=shadowOf(screen).resultIntent
            assertEquals(Activity.RESULT_OK,shadowOf(screen).resultCode)
            assertEquals(token,result.getStringExtra(LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN))
            assertEquals(listOf(modern),ImageCredit.read(JSONArray(result.getStringExtra("document_image_credits"))))
            assertFalse(result.extras!!.keySet().any {it.contains("text")})
            assertEquals("Legacy text",preferences.getString("text:$source",null))
        } finally {gallery.pause().stop().destroy()}
    }

    @Test fun uneditedGalleryArchiveResultKeepsItsSessionUntilTheParentConsumesIt() {
        seed("Legacy text")
        val gallery=Robolectric.buildActivity(MediaGalleryActivity::class.java,
            Intent(context,MediaGalleryActivity::class.java).putExtra("document_image_credits","[]"))
        var token: String?=null
        try {
            val screen=gallery.create().start().resume().visible().get()
            screen.window.decorView.findViewWithTag<Button>("gallery_legacy_credits").performClick()
            val request=shadowOf(screen).nextStartedActivityForResult
            screen.onActivityResult(request.requestCode,Activity.RESULT_OK,Intent().putExtra(
                LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN,ImageCreditArchive.selectionToken(ImageCredit(source,"Legacy text"))))
            token=shadowOf(screen).resultIntent.getStringExtra(CreditEditSession.EXTRA_SESSION)
            assertNotNull(token);assertTrue(screen.isFinishing)
            gallery.pause().stop().destroy()
            val pending=CreditEditSession.open(context.filesDir,token!!)
            assertFalse(pending.accepted);assertNull(pending.draft)
            assertTrue(pending.credits.isEmpty())
        } finally {
            if(!gallery.get().isDestroyed)gallery.pause().stop().destroy()
            token?.let {runCatching {CreditEditSession.open(context.filesDir,it).discard()}}
        }
    }

    @Test fun unreadableArchiveDoesNotClaimThatNoImagesWereInserted() {
        val token=ImageCreditArchive.retainAccepted(context,listOf(ImageCredit(source,"Stored")))
        File(context.filesDir,"retained-image-credits/$token.json").writeText("not valid json")
        launch()
        assertEquals("",text().text.toString())
        assertEquals(activity.getString(R.string.legacy_credits_unreadable),
            activity.window.decorView.findViewWithTag<TextView>("legacy_credit_status").text.toString())
        assertFalse(activity.window.decorView.findViewWithTag<Button>("legacy_credit_add").isEnabled)
        assertTrue(File(context.filesDir,"retained-image-credits/$token.json").isFile)
    }

    class OutputProvider: ContentProvider() {
        lateinit var file: File
        override fun onCreate()=true
        override fun openFile(uri: Uri,mode: String): ParcelFileDescriptor = ParcelFileDescriptor.open(file,
            ParcelFileDescriptor.MODE_CREATE or ParcelFileDescriptor.MODE_TRUNCATE or ParcelFileDescriptor.MODE_WRITE_ONLY)
        override fun getType(uri: Uri)="text/plain"
        override fun query(uri: Uri,projection: Array<out String>?,selection: String?,selectionArgs: Array<out String>?,sortOrder: String?): Cursor?=null
        override fun insert(uri: Uri,values: ContentValues?): Uri?=null
        override fun delete(uri: Uri,selection: String?,selectionArgs: Array<out String>?)=0
        override fun update(uri: Uri,values: ContentValues?,selection: String?,selectionArgs: Array<out String>?)=0
    }
}
