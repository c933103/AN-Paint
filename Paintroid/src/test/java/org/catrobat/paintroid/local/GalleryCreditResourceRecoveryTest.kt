/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.net.Uri
import android.os.Bundle
import android.os.Looper
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONArray
import org.json.JSONObject
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
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.shadows.ShadowToast
import java.io.File
import java.time.Duration
import java.util.concurrent.TimeUnit

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class GalleryCreditResourceRecoveryTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private fun advance()=shadowOf(Looper.getMainLooper()).idleFor(Duration.ZERO)
    private val credit=ImageCredit("https://example.org/raw.png","Original creator")
    private fun field(dialog: AlertDialog)=dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text")
    private fun notice(dialog: AlertDialog)=dialog.window!!.decorView.findViewWithTag<TextView>("locale_notification_text")?.text?.toString()
        ?: ShadowToast.getTextOfLatestToast()
    private fun session(): CreditEditSession=CreditEditSession.create(context.filesDir,listOf(credit),CreditEditContext.ledgerOnly(listOf(credit)))

    @Test fun failedRawSnapshotShowsAnErrorAndKeepsTheFieldAndPreviousFile() {
        val session=session();val launch=Intent(context,MediaGalleryActivity::class.java).putExtra(CreditEditSession.EXTRA_SESSION,session.token)
        val controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,launch).setup()
        val heap=CreditSessionJson.availableHeap;val stored=File(context.filesDir,session.token)
        try {
            val activity=controller.get()
            activity.window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick();advance()
            val dialog=ShadowAlertDialog.getLatestAlertDialog();val raw="𠀀漢".repeat(30000)
            field(dialog).setText(raw);val before=stored.readBytes()
            CreditSessionJson.availableHeap={1024}
            ShadowToast.reset()
            val state=Bundle();controller.saveInstanceState(state);advance()
            assertEquals(activity.getString(R.string.gallery_credit_could_not_save),notice(dialog))
            assertEquals(raw,field(dialog).text.toString());assertTrue(dialog.isShowing)
            assertArrayEquals(before,stored.readBytes())
            assertEquals(session.token,state.getString(CreditEditSession.EXTRA_SESSION))
            assertFalse(state.containsKey("image_credit_editor_draft"))
            assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
        } finally {
            CreditSessionJson.availableHeap=heap
            controller.pause().stop().destroy();advance();session.discard();ShadowToast.reset()
        }
    }
    @Test fun saveCopyAndDoneResourceRefusalNeverClaimSuccessOrClearTheField() {
        val session=session();val launch=Intent(context,MediaGalleryActivity::class.java).putExtra(CreditEditSession.EXTRA_SESSION,session.token)
        val controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,launch).setup()
        val heap=CreditSessionJson.availableHeap
        try {
            val activity=controller.get()
            activity.window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick();advance()
            val dialog=ShadowAlertDialog.getLatestAlertDialog();val raw="Valid-sized pending attribution 𠀀".repeat(1000)
            field(dialog).setText(raw);val stored=File(context.filesDir,session.token);val before=stored.readBytes()
            CreditSessionJson.availableHeap={1024}
            for(tag in listOf("gallery_credit_save","gallery_credit_copy","gallery_credit_done")) {
                ShadowToast.reset();dialog.window!!.decorView.findViewWithTag<Button>(tag).performClick();advance()
                assertTrue(dialog.isShowing);assertEquals(raw,field(dialog).text.toString())
                assertEquals(activity.getString(R.string.gallery_credit_could_not_save),notice(dialog))
                assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
                assertArrayEquals(before,stored.readBytes())
            }
        } finally {
            CreditSessionJson.availableHeap=heap
            controller.pause().stop().destroy();advance();session.discard();ShadowToast.reset()
        }
    }
    @Test fun galleryResourceRestoreErrorRetainsItsTokenAcrossAnotherRecreationAndCanRetry() {
        val session=session();val raw="𠀀漢\n\"\\".repeat(40000)
        session.saveDraft(GalleryCredits.EditorDraft(credit.source,raw))
        // The token deliberately exists only in the saved state, not the launch Intent.
        val launch=Intent(context,MediaGalleryActivity::class.java)
        var state=Bundle().apply {putString(CreditEditSession.EXTRA_SESSION,session.token)}
        val heap=CreditSessionJson.availableHeap;val stored=File(context.filesDir,session.token);val before=stored.readBytes()
        var controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,launch)
        try {
            CreditSessionJson.availableHeap={64L*1024}
            controller.create(state).start().resume().visible();advance()
            val error=ShadowAlertDialog.getLatestAlertDialog()
            assertTrue(error.isShowing)
            assertEquals(controller.get().getString(R.string.gallery_credit_could_not_save),error.findViewById<TextView>(android.R.id.message).text.toString())
            assertEquals(Activity.RESULT_CANCELED,shadowOf(controller.get()).resultCode)
            state=Bundle();controller.saveInstanceState(state).pause().stop().destroy();advance()
            assertEquals(session.token,state.getString(CreditEditSession.EXTRA_SESSION))
            assertArrayEquals(before,stored.readBytes())
            CreditSessionJson.availableHeap=heap
            controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,launch).create(state).start().resume().visible();advance()
            val restored=ShadowAlertDialog.getLatestAlertDialog()
            assertTrue(restored.isShowing);assertEquals(raw,field(restored).text.toString())
            assertFalse(CreditEditSession.open(context.filesDir,session.token).accepted)
        } finally {
            CreditSessionJson.availableHeap=heap
            if(!controller.get().isDestroyed)controller.pause().stop().destroy()
            advance()
            session.discard()
        }
    }
    private fun withMainRetry(seedSameSource: Boolean=false,resourceBudget: (()->Long)?=null,expectLoadError: Boolean=true,
        action: (ActivityController<ClassicPaintActivity>,CreditEditSession,ByteArray)->Unit) {
        AutosaveStore(context.filesDir).exists()
        listOf("classic-autosave.zip","classic-autosave.zip.bak","classic-autosave.zip.new","classic-recovery.png")
            .forEach {File(context.filesDir,it).delete()}
        val filesBefore=context.filesDir.listFiles().orEmpty().map {it.name}.toSet()
        val archive=File(context.filesDir,"retained-image-credits")
        val archiveBefore=archive.listFiles().orEmpty().map {it.name}.toSet()
        val session=session();session.saveDraft(GalleryCredits.EditorDraft(credit.source,"𠀀".repeat(40000)))
        val stored=File(context.filesDir,session.token);val before=stored.readBytes()
        if(seedSameSource) {
            val image=Bitmap.createBitmap(4,3,Bitmap.Config.ARGB_8888)
            try {AutosaveStore(context.filesDir).write(image,null,JSONObject().put("version",1)
                .put("image_credits",JSONObject().put("committed",ImageCredit.write(listOf(credit)))
                    .put("floating",JSONArray()).put("selection_sources_known",true)))} finally {image.recycle()}
        }
        val heap=CreditSessionJson.availableHeap
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java)
        try {
            CreditSessionJson.availableHeap=resourceBudget ?: {64L*1024}
            controller.create(Bundle().apply {putString("main_credit_session",session.token)}).start().resume().visible();advance()
            if(expectLoadError) {
                val error=ShadowAlertDialog.getLatestAlertDialog()
                assertTrue(error.isShowing)
                assertEquals(controller.get().getString(R.string.gallery_credit_could_not_save),error.findViewById<TextView>(android.R.id.message).text.toString())
            }
            CreditSessionJson.availableHeap=heap
            action(controller,session,before)
        } finally {
            CreditSessionJson.availableHeap=heap
            controller.pause().stop();AutosaveStore(context.filesDir).exists();advance()
            controller.destroy();AutosaveStore(context.filesDir).exists();advance()
            // Delete only sessions/snapshots created by this fixture, after lifecycle workers join.
            context.filesDir.listFiles().orEmpty().filter {it.name.startsWith("credit-edit-") && it.name !in filesBefore}.forEach {it.delete()}
            archive.listFiles().orEmpty().filter {it.name !in archiveBefore}.forEach {it.delete()}
            listOf("classic-autosave.zip","classic-autosave.zip.bak","classic-autosave.zip.new","classic-recovery.png")
                .forEach {File(context.filesDir,it).delete()}
        }
    }
    private fun mainState(controller: ActivityController<ClassicPaintActivity>)=Bundle().also {controller.saveInstanceState(it);advance()}
    private fun closeRestoreError() {ShadowAlertDialog.getLatestAlertDialog().getButton(AlertDialog.BUTTON_POSITIVE).performClick();advance()}
    private fun addSameSource(activity: ClassicPaintActivity) {
        activity.document.paste(Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888),true,listOf(credit))
        activity.document.finishSelection()
    }
    private fun openMainEditor(activity: ClassicPaintActivity) {
        ClassicPaintActivity::class.java.getDeclaredMethod("showImageCredits",GalleryCredits.EditorDraft::class.java,CreditEditSession::class.java)
            .apply {isAccessible=true}.invoke(activity,null,null)
        advance()
    }
    private fun openNewDialog(activity: ClassicPaintActivity): AlertDialog {
        ClassicPaintActivity::class.java.getDeclaredMethod("dimensionsDialog",Boolean::class.java,Boolean::class.java)
            .apply {isAccessible=true}.invoke(activity,false,true)
        advance();return ShadowAlertDialog.getLatestAlertDialog()
    }
    private fun awaitIo(activity: ClassicPaintActivity) {
        val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(10)
        while(activity.busy && System.nanoTime()<deadline) {advance();Thread.sleep(5)}
        advance();assertFalse("Background operation timed out",activity.busy)
    }
    @Test fun mainEditorResourceRestoreFailureIsVisibleAndKeepsItsRecoveryToken()=withMainRetry {controller,session,before->
        assertEquals(session.token,mainState(controller).getString("main_credit_session"))
        assertArrayEquals(before,File(context.filesDir,session.token).readBytes())
    }
    @Test fun failedFreshEditorKeepsRetryButSuccessfulFreshSaveCannotReviveIt()=withMainRetry {controller,session,before->
        closeRestoreError();val activity=controller.get();addSameSource(activity)
        val heap=CreditSessionJson.availableHeap
        try {
            CreditSessionJson.availableHeap={0}
            openMainEditor(activity) // Fresh session exists, but constructing its field is refused.
            assertEquals(session.token,mainState(controller).getString("main_credit_session"))
            assertArrayEquals(before,File(context.filesDir,session.token).readBytes())
        } finally {CreditSessionJson.availableHeap=heap}
        openMainEditor(activity)
        val editor=ShadowAlertDialog.getLatestAlertDialog()
        assertTrue(editor.isShowing);assertEquals(credit.text,field(editor).text.toString())
        field(editor).setText("A newer accepted attribution")
        editor.window!!.decorView.findViewWithTag<Button>("gallery_credit_done").performClick();advance()
        assertFalse(editor.isShowing)
        assertEquals("A newer accepted attribution",activity.document.imageCredits.single().text)
        assertFalse(mainState(controller).containsKey("main_credit_session"))
        assertArrayEquals(before,File(context.filesDir,session.token).readBytes())
    }
    @Test fun canceledOrInvalidNewKeepsRetryButSuccessfulNewDetachesItWithoutDeletingText()=withMainRetry {controller,session,before->
        closeRestoreError();val activity=controller.get()
        openNewDialog(activity).getButton(AlertDialog.BUTTON_NEGATIVE).performClick();advance()
        assertEquals(session.token,mainState(controller).getString("main_credit_session"))
        val dialog=openNewDialog(activity)
        dialog.window!!.decorView.findViewWithTag<EditText>("size_width").setText("0")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();advance()
        assertTrue(dialog.isShowing)
        assertEquals(session.token,mainState(controller).getString("main_credit_session"))
        dialog.window!!.decorView.findViewWithTag<EditText>("size_width").setText("8")
        dialog.window!!.decorView.findViewWithTag<EditText>("size_height").setText("6")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();advance()
        assertFalse(dialog.isShowing)
        addSameSource(activity)
        assertEquals(credit.text,activity.document.imageCredits.single().text)
        assertFalse(mainState(controller).containsKey("main_credit_session"))
        assertArrayEquals(before,File(context.filesDir,session.token).readBytes())
    }
    @Test fun failedWholeImageReplacementKeepsRetryButSuccessfulReplacementDetachesIt()=withMainRetry {controller,session,before->
        closeRestoreError();val activity=controller.get()
        val file=File(context.cacheDir,"credit-retry-replacement.png")
        try {
            file.writeText("invalid image")
            activity.onActivityResult(ClassicPaintActivity.OPEN_IMAGE,Activity.RESULT_OK,Intent().setData(Uri.fromFile(file)))
            awaitIo(activity)
            assertEquals(session.token,mainState(controller).getString("main_credit_session"))
            val image=Bitmap.createBitmap(4,3,Bitmap.Config.ARGB_8888)
            try {file.outputStream().use {assertTrue(image.compress(Bitmap.CompressFormat.PNG,100,it))}} finally {image.recycle()}
            activity.onActivityResult(ClassicPaintActivity.OPEN_IMAGE,Activity.RESULT_OK,Intent().setData(Uri.fromFile(file)))
            awaitIo(activity)
            assertNull(activity.lastIoError);assertEquals(4,activity.document.bitmap.width);assertEquals(3,activity.document.bitmap.height)
            addSameSource(activity)
            assertEquals(credit.text,activity.document.imageCredits.single().text)
            assertFalse(mainState(controller).containsKey("main_credit_session"))
            assertArrayEquals(before,File(context.filesDir,session.token).readBytes())
        } finally {file.delete()}
    }
    @Test fun parsedDraftWithRefusedEditorStaysRetryOnlyAndNewCanDetachIt() {
        var heapQueries=0
        withMainRetry(seedSameSource=true,resourceBudget={heapQueries++;if(heapQueries==1)128L*1024*1024 else 0L},expectLoadError=false) {controller,session,before->
            assertTrue("Parse must succeed before the editor allocation is refused",heapQueries>=2)
            val activity=controller.get()
            assertEquals(credit.text,activity.document.imageCredits.single().text)
            assertEquals(session.token,mainState(controller).getString("main_credit_session"))
            val dialog=openNewDialog(activity)
            dialog.window!!.decorView.findViewWithTag<EditText>("size_width").setText("8")
            dialog.window!!.decorView.findViewWithTag<EditText>("size_height").setText("6")
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();advance()
            assertFalse(dialog.isShowing);addSameSource(activity)
            assertFalse(mainState(controller).containsKey("main_credit_session"))
            assertEquals(credit.text,activity.document.imageCredits.single().text)
            assertArrayEquals(before,File(context.filesDir,session.token).readBytes())
        }
    }

    @Test fun onlySuccessfulExplicitGalleryEditsSupersedeThePendingRawRetry()=withMainRetry {controller,old,before->
        closeRestoreError();val activity=controller.get();addSameSource(activity)
        fun own(token: String) {
            // Controlled exact-token launch handoff; actual Android routing is separate coverage.
            ClassicPaintActivity::class.java.getDeclaredField("galleryCreditSessionToken")
                .apply {isAccessible=true}.set(activity,token)
        }
        val unedited=session();own(unedited.token)
        activity.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,unedited.result());advance()
        assertEquals(old.token,mainState(controller).getString("main_credit_session"))
        val canceled=session();own(canceled.token)
        activity.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_CANCELED,null);advance()
        assertEquals(old.token,mainState(controller).getString("main_credit_session"))
        val accepted=session()
        accepted.edit(credit.source,"New explicit Gallery text") {ImageCreditArchive.retainAccepted(context,it)}
        own("credit-edit-00000000-0000-0000-0000-000000000000.json")
        activity.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,accepted.result());advance()
        assertEquals(old.token,mainState(controller).getString("main_credit_session"))
        assertEquals(credit.text,activity.document.imageCredits.single().text)
        own(accepted.token)
        activity.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,accepted.result());advance()
        assertEquals("New explicit Gallery text",activity.document.imageCredits.single().text)
        assertFalse(mainState(controller).containsKey("main_credit_session"))
        assertArrayEquals(before,File(context.filesDir,old.token).readBytes())
    }

}
