/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.os.Looper
import android.os.Parcel
import android.widget.Button
import android.widget.EditText
import org.catrobat.paintroid.classic.*
import org.catrobat.paintroid.R
import org.robolectric.shadows.ShadowToast
import org.json.JSONArray
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.LooperMode
import org.robolectric.shadows.ShadowAlertDialog

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
@LooperMode(LooperMode.Mode.PAUSED)
class GalleryCreditBoundsTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private fun field(dialog: AlertDialog)=dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text")
    private fun idle()=shadowOf(Looper.getMainLooper()).idle()
    private fun click(dialog: AlertDialog,tag: String) {
        // Dialog posts OnShow: wait for the real guarded listeners and tags before clicking.
        idle()
        val button=dialog.window!!.decorView.findViewWithTag<Button>(tag)
        assertNotNull("Missing credit action: $tag",button)
        assertTrue(button.performClick())
        idle()
    }

    @Test fun rejectedOversizedFieldSurvivesRecreationThenLargeValidCopyKeepsFullAttribution() {
        val first=ImageCredit("https://example.org/a","Original creator")
        val second=ImageCredit("https://example.org/b","漢".repeat(6000))
        val launch=Intent(context,MediaGalleryActivity::class.java)
            .putExtra("document_image_credits",ImageCredit.write(listOf(first,second)).toString())
        var controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,launch).setup()
        var acceptedSnapshot: String?=null
        var token: String?=null
        try {
            var activity=controller.get()
            activity.window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick()
            var dialog=ShadowAlertDialog.getLatestAlertDialog()
            val clipboard=activity.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
            clipboard.setPrimaryClip(ClipData.newPlainText("previous clipboard","Do not replace me"))
            val oversized="𠀀漢\n\"\\".repeat(40000)
            field(dialog).text.replace(0,field(dialog).length(),oversized)
            click(dialog,"gallery_credit_save");click(dialog,"gallery_credit_copy");click(dialog,"gallery_credit_done")
            assertTrue(dialog.isShowing)
            assertEquals(oversized,field(dialog).text.toString())
            assertEquals("Do not replace me",clipboard.primaryClip!!.getItemAt(0).text.toString())
            assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
            val state=Bundle();controller.saveInstanceState(state).pause().stop().destroy()
            assertFalse(state.containsKey("image_credit_editor_draft"))
            token=state.getString(CreditEditSession.EXTRA_SESSION)
            assertNotNull(token)
            val parcel=Parcel.obtain()
            try {parcel.writeBundle(state);assertTrue(parcel.dataSize()<128*1024)} finally {parcel.recycle()}
            assertEquals(oversized,CreditEditSession.open(context.filesDir,token!!).draft!!.text)
            controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,launch).create(state).start().resume().visible()
            activity=controller.get();dialog=ShadowAlertDialog.getLatestAlertDialog()
            assertTrue(dialog.isShowing);assertEquals(oversized,field(dialog).text.toString())
            assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)

            // More than64KiB remains supported: the transport threshold must not become an edit/copy cap.
            val largeValid="𠀀".repeat(50000)
            field(dialog).text.replace(0,field(dialog).length(),largeValid)
            click(dialog,"gallery_credit_copy")
            assertEquals(largeValid,clipboard.primaryClip!!.getItemAt(0).text.toString())
            assertEquals(Activity.RESULT_OK,shadowOf(activity).resultCode)
            val result=shadowOf(activity).resultIntent!!
            assertFalse(result.hasExtra("document_image_credits"))
            val session=CreditEditSession.open(context.filesDir,result.getStringExtra(CreditEditSession.EXTRA_SESSION)!!)
            acceptedSnapshot=session.acceptedSnapshot
            assertEquals(listOf(first.copy(text=largeValid),second),session.credits)
            dialog.cancel();idle() // OnDismiss clears the persisted draft asynchronously.
            val again=Bundle();controller.saveInstanceState(again)
            assertFalse(again.containsKey("image_credit_editor_draft"))
            assertNull(CreditEditSession.open(context.filesDir,token!!).draft)
            assertEquals(largeValid,CreditEditSession.open(context.filesDir,token!!).credits.first().text)
        } finally {
            if(!controller.get().isDestroyed) controller.pause().stop().destroy()
            idle()
            token?.let {runCatching {CreditEditSession.open(context.filesDir,it).discard()}}
            acceptedSnapshot?.let {ImageCreditArchive.releaseAccepted(context,it)}
        }
    }
    @Test fun clipboardFailureKeepsAcceptedSaveAndRawFieldWithoutReportingCopied() {
        val original=ImageCredit("https://example.org/a","Original")
        val revised=original.copy(text="Accepted creator — 漢𠀀")
        val launch=Intent(context,MediaGalleryActivity::class.java).putExtra("document_image_credits",ImageCredit.write(listOf(original)).toString())
        val controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,launch).setup()
        val previousPublisher=GalleryCredits.publishClipboard
        var acceptedSnapshot: String?=null;var sessionToken: String?=null
        try {
            val activity=controller.get()
            val clipboard=activity.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
            clipboard.setPrimaryClip(ClipData.newPlainText("old","Keep the prior clipboard"))
            activity.window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick()
            val dialog=ShadowAlertDialog.getLatestAlertDialog()
            field(dialog).setText(revised.text)
            GalleryCredits.publishClipboard={_,_->throw android.os.TransactionTooLargeException("Injected Binder failure")}
            ShadowToast.reset()
            click(dialog,"gallery_credit_copy")
            assertTrue(dialog.isShowing);assertEquals(revised.text,field(dialog).text.toString())
            assertEquals("Keep the prior clipboard",clipboard.primaryClip!!.getItemAt(0).text.toString())
            val result=shadowOf(activity).resultIntent!!
            assertEquals(Activity.RESULT_OK,shadowOf(activity).resultCode)
            assertEquals(listOf(revised),ImageCredit.read(JSONArray(result.getStringExtra("document_image_credits"))))
            sessionToken=result.getStringExtra(CreditEditSession.EXTRA_SESSION)
            val session=CreditEditSession.open(context.filesDir,sessionToken!!)
            acceptedSnapshot=session.acceptedSnapshot
            assertEquals(listOf(revised),session.credits)
            val notice=dialog.window!!.decorView.findViewWithTag<android.widget.TextView>("locale_notification_text")?.text?.toString()
                ?: ShadowToast.getTextOfLatestToast()
            assertEquals(ui(R.string.ui_could_not_complete_the_operation),notice)
            assertNotEquals(ui(R.string.gallery_credit_copied),notice)
        } finally {
            GalleryCredits.publishClipboard=previousPublisher
            controller.pause().stop().destroy()
            idle()
            sessionToken?.let {runCatching {CreditEditSession.open(context.filesDir,it).discard()}}
            acceptedSnapshot?.let {ImageCreditArchive.releaseAccepted(context,it)}
            ShadowToast.reset()
        }
    }

}
