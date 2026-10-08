/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Color
import android.os.Looper
import android.widget.Button
import android.widget.EditText
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
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
import java.io.File
import java.io.IOException

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class LegacyImageCreditsUpgradeTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val preferences get()=context.getSharedPreferences("image-credits",Context.MODE_PRIVATE)
    private var controller: ActivityController<ClassicPaintActivity>?=null
    private val activity get()=controller!!.get()
    private val legacy=ImageCredit("https://example.org/old.png","Edited old creator\nChanges: cropped")
    private val modern=ImageCredit("https://example.org/current.png","Modern source")
    private fun clearDraft() {
        AutosaveStore(context.filesDir).exists() // Join outstanding lifecycle writes before deleting fixtures.
        listOf("classic-autosave.zip","classic-autosave.zip.bak","classic-autosave.zip.new","classic-recovery.png")
            .forEach {File(context.filesDir,it).delete()}
    }
    private fun stop() {
        controller?.let {
            it.pause().stop();AutosaveStore(context.filesDir).exists();shadowOf(Looper.getMainLooper()).idle()
            it.destroy();AutosaveStore(context.filesDir).exists()
        }
        controller=null
    }
    private fun launch() {
        controller=Robolectric.buildActivity(ClassicPaintActivity::class.java)
        controller!!.create().start().resume().visible();shadowOf(Looper.getMainLooper()).idle()
    }
    private fun state(credits: List<ImageCredit>)=JSONObject().put("committed",ImageCredit.write(credits))
        .put("floating",ImageCredit.write(emptyList())).put("selection_sources_known",true)
    private fun seedDraft(kind: String) {
        if(kind=="fresh")return
        val image=Bitmap.createBitmap(7,5,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.BLUE)}
        try {
            if(kind=="old_png") File(context.filesDir,"classic-recovery.png").outputStream().use {
                assertTrue(image.compress(Bitmap.CompressFormat.PNG,100,it))
            } else {
                val metadata=JSONObject().put("version",1)
                if(kind=="modern_empty")metadata.put("image_credits",state(emptyList()))
                if(kind=="modern_populated")metadata.put("image_credits",state(listOf(modern)))
                AutosaveStore(context.filesDir).write(image,null,metadata)
            }
        } finally {image.recycle()}
    }
    @Before fun prepare() {
        File(context.filesDir,"retained-image-credits").deleteRecursively()
        clearDraft();preferences.edit().clear().putStringSet("sources",setOf(legacy.source))
            .putString("generated:${legacy.source}","Original generated credit")
            .putString("text:${legacy.source}",legacy.text).commit()
    }
    @After fun cleanup() {stop();clearDraft();preferences.edit().clear().commit();File(context.filesDir,"retained-image-credits").deleteRecursively()}

    @Test fun allRestoreFormatsAndFreshCanvasesKeepTheArchiveAccessibleWithoutInventingAssociation() {
        val originalArchive=preferences.all
        for(kind in listOf("old_zip","old_png","modern_empty","modern_populated","fresh")) {
            clearDraft();seedDraft(kind);launch()
            assertEquals(kind,if(kind=="modern_populated") listOf(modern) else emptyList<ImageCredit>(),activity.document.imageCredits)
            assertEquals(listOf(legacy),LegacyImageCredits.read(activity))
            if(kind!="fresh") {
                assertEquals(kind,7,activity.document.bitmap.width)
                assertEquals(kind,Color.BLUE,activity.document.bitmap.getPixel(0,0))
            }
            ReflectionHelpers.callInstanceMethod<Any>(activity,"showAboutOptions")
            val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            val labels=(0 until dialog.listView.adapter.count).map {dialog.listView.adapter.getItem(it).toString()}
            assertTrue(kind,activity.getString(R.string.legacy_credits_title) in labels)
            dialog.dismiss()
            activity.document.newImage(8,6);assertTrue(activity.document.imageCredits.isEmpty())
            activity.document.replace(Bitmap.createBitmap(3,4,Bitmap.Config.ARGB_8888),asEdit=true,retainCredits=false)
            assertTrue(activity.document.imageCredits.isEmpty())
            assertEquals(originalArchive,preferences.all)
            stop()
        }
    }

    @Test fun explicitSelectionAttachesOnceAndNeverOverwritesAnExistingEmptyModernCredit() {
        launch();val pixels=activity.document.bitmap;val colour=pixels.getPixel(0,0)
        fun deliver()=activity.onActivityResult(ClassicPaintActivity.LEGACY_CREDITS,Activity.RESULT_OK,
            Intent().putExtra(LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN,ImageCreditArchive.selectionToken(LegacyImageCredits.read(activity).single())))
        deliver();assertEquals(listOf(legacy),activity.document.imageCredits)
        assertSame(pixels,activity.document.bitmap);assertEquals(colour,pixels.getPixel(0,0))
        activity.document.editImageCredit(legacy.source,"")
        deliver();assertEquals(listOf(legacy.copy(text="")),activity.document.imageCredits)
        assertEquals(legacy.text,preferences.getString("text:${legacy.source}",null))
        stop();launch()
        assertEquals(listOf(legacy.copy(text="")),activity.document.imageCredits)
    }

    @Test fun rejectedProspectiveAttachmentLeavesPixelsSelectionHistoryAndCreditsUnchanged() {
        val folder=File(context.cacheDir,"legacy-atomic-${java.util.UUID.randomUUID()}")
        val doc=PaintDocument(8,6,folder)
        try {
            doc.paste(Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.RED)},true,listOf(modern))
            val pixels=doc.bitmap;val selection=doc.selection;val before=doc.imageCreditsState().toString()
            val history=doc.historySnapshot();var changes=0;doc.changed={changes++}
            val oversized=legacy.copy(text="\uD86D\uDC40".repeat(100_000))
            try {
                doc.attachImageCredit(oversized) {projected ->
                    assertEquals(oversized,ImageCredit.read(projected.getJSONArray("committed")).single())
                    throw IOException("Rejected prospective draft")
                }
                fail("Rejected credit must not be attached")
            } catch(_: IOException) { }
            assertSame(pixels,doc.bitmap);assertSame(selection,doc.selection)
            assertEquals(before,doc.imageCreditsState().toString());assertEquals(history,doc.historySnapshot())
            assertEquals(0,changes)
            assertFalse(doc.attachImageCredit(modern.copy(text="Do not overwrite")) {fail("Duplicate must not need validation")})
            assertEquals(listOf(modern),doc.imageCredits)
        } finally {doc.close();folder.deleteRecursively()}
    }

    @Test fun oversizedExplicitSelectionIsRejectedBeforeMutatingDocumentOrItsValidAutosave() {
        launch()
        val oversized="\uD86D\uDC40\"\\\n".repeat(50_000)
        preferences.edit().putString("text:${legacy.source}",oversized).commit()
        val doc=activity.document;val bitmap=doc.bitmap;val beforeCredits=doc.imageCreditsState().toString()
        val store=AutosaveStore(context.filesDir)
        val metadata=ReflectionHelpers.callInstanceMethod<JSONObject>(activity,"draftMetadata")
        store.write(doc.bitmap,null,metadata,doc.historySnapshot())
        val beforeDraft=store.file.readBytes()
        activity.onActivityResult(ClassicPaintActivity.LEGACY_CREDITS,Activity.RESULT_OK,
            Intent().putExtra(LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN,ImageCreditArchive.selectionToken(LegacyImageCredits.read(activity).single())))
        assertSame(bitmap,doc.bitmap);assertEquals(beforeCredits,doc.imageCreditsState().toString())
        assertArrayEquals(beforeDraft,store.file.readBytes())
        assertEquals(oversized,LegacyImageCredits.read(activity).single().text)
        assertTrue((ShadowAlertDialog.getLatestAlertDialog() as AlertDialog).isShowing)
        ShadowAlertDialog.getLatestAlertDialog().dismiss()
    }

    @Test fun acceptedGalleryResultSurvivesFreshEditorWithoutAdoptionAndOnlyDurableExactAdoptionReleasesIt() {
        seedDraft("modern_populated")
        val gallery=Robolectric.buildActivity(MediaGalleryActivity::class.java,
            Intent(context,MediaGalleryActivity::class.java)
                .putExtra("document_image_credits",ImageCredit.write(listOf(modern)).toString()))
        val revised=modern.copy(text="Accepted gallery edit \uD86D\uDC40")
        lateinit var result: Intent
        lateinit var receipt: CreditEditSession.AdoptionReceipt
        try {
            val screen=gallery.create().start().resume().visible().get()
            shadowOf(Looper.getMainLooper()).idle()
            screen.window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick()
            shadowOf(Looper.getMainLooper()).idle()
            val editor=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            editor.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").setText(revised.text)
            editor.window!!.decorView.findViewWithTag<Button>("gallery_credit_save").performClick()
            assertEquals(Activity.RESULT_OK,shadowOf(screen).resultCode)
            result=shadowOf(screen).resultIntent
            val session=CreditEditSession.open(context.filesDir,result.getStringExtra(CreditEditSession.EXTRA_SESSION)!!)
            receipt=session.adoptionReceipt!!
            assertEquals(listOf(revised),session.credits)
        } finally {gallery.pause().stop().destroy()}
        // A process/task loss before result delivery must not turn this into a blank or
        // automatically re-associated ledger. The original draft still owns its old text.
        launch()
        assertEquals(listOf(modern),activity.document.imageCredits)
        assertTrue(ImageCreditArchive.records(context).any {it.credit==revised})
        // A raw inline ledger cannot bypass session ownership either.
        activity.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,
            Intent().putExtra("document_image_credits",ImageCredit.write(listOf(revised)).toString()))
        assertEquals(listOf(modern),activity.document.imageCredits)
        ShadowAlertDialog.getLatestAlertDialog().dismiss()
        // A stale accepted result cannot authorize attribution in a fresh editor.
        activity.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,result)
        assertEquals(listOf(modern),activity.document.imageCredits)
        ShadowAlertDialog.getLatestAlertDialog().dismiss()
        ReflectionHelpers.setField(activity,"galleryCreditSessionToken","credit-edit-00000000-0000-0000-0000-000000000000.json")
        activity.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,result)
        assertEquals(listOf(modern),activity.document.imageCredits)
        ShadowAlertDialog.getLatestAlertDialog().dismiss()
        // This controlled fixture now models the matching launch handoff. Actual Android
        // process routing is covered separately, not claimed by this direct callback.
        ReflectionHelpers.setField(activity,"galleryCreditSessionToken",result.getStringExtra(CreditEditSession.EXTRA_SESSION))
        activity.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,result)
        assertEquals(listOf(revised),activity.document.imageCredits)
        assertTrue("Memory adoption is not durability",ImageCreditArchive.records(context).any {it.credit==revised})
        stop() // Joins the actual autosave and its immutable-receipt cleanup.
        assertFalse(ImageCreditArchive.records(context).any {it.credit==revised})
        ImageCreditArchive.releaseAccepted(context,receipt.snapshotToken) // Idempotent repeated completion.
        assertEquals(listOf(legacy),ImageCreditArchive.records(context).map {it.credit})
        launch();assertEquals(listOf(revised),activity.document.imageCredits)
        assertEquals(legacy.text,preferences.getString("text:${legacy.source}",null))
    }

    @Test fun saveAndExportExposeArchiveNavigationEvenWithAnEmptyModernLedger() {
        launch()
        for(export in listOf(false,true)) {
            var opened=0;var cancelled=0
            val dialog=SaveOptionsDialog(activity,ExportOptions(if(export) ImageFormat.ICO else ImageFormat.PNG),
                confirm={fail("Archive access must not save an image")},cancel={cancelled++},
                export=export,legacyCredits={opened++}).show()
            assertTrue(dialog.window!!.decorView.findViewWithTag<Button>("export_legacy_credits").performClick())
            assertEquals(1,opened);assertEquals(1,cancelled);assertFalse(dialog.isShowing)
            assertTrue(activity.document.imageCredits.isEmpty())
        }
    }
}
