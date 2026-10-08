/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.app.LocaleManager
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.content.res.Resources
import android.os.Build
import android.os.Bundle
import android.os.LocaleList
import android.os.Looper
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.FrameLayout
import android.widget.Spinner
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.ImageCredit
import org.catrobat.paintroid.classic.LocaleTypography
import org.catrobat.paintroid.classic.MediaGalleryActivity
import org.catrobat.paintroid.classic.PaintApplication
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
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.LooperMode
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.shadows.ShadowToast
import java.time.Duration
import java.util.Locale

/** Gallery draft recovery and Nôm feedback together; no network or installed-app claims. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class GalleryCreditNotificationRecoveryTest {
    private lateinit var controller: ActivityController<MediaGalleryActivity>
    private lateinit var launchIntent: Intent
    private lateinit var previousLocale: Locale
    private lateinit var previousResources: Resources
    private var previousTag: String?=null
    private var previousPlatformInitialized: Boolean?=null
    private var previousPlatformLocales: LocaleList?=null
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val preferences get()=context.getSharedPreferences("app-language",Context.MODE_PRIVATE)
    private val gallery get()=controller.get()
    private val original=ImageCredit("https://example.org/a.png","Original creator and source")
    private fun advance(ms: Long=0)=shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(ms))

    @Before fun selectNom() {
        previousLocale=Locale.getDefault()
        previousResources=PaintApplication.currentResources
        previousTag=preferences.getString("language-tag",null)
        previousPlatformInitialized=if(preferences.contains("platform-initialized"))
            preferences.getBoolean("platform-initialized",false) else null
        if(Build.VERSION.SDK_INT>=33)
            previousPlatformLocales=context.getSystemService(LocaleManager::class.java)!!.applicationLocales
        // Locale.setDefault alone is overwritten by the gallery's AppLanguage.wrap.
        AppLanguage.select(context,"vi-Hani")
        PaintApplication.currentResources=AppLanguage.wrap(context).resources
        ShadowToast.reset()
    }

    @After fun cleanup() {
        try {
            if(::controller.isInitialized && !gallery.isDestroyed) controller.pause().stop().destroy()
            advance() // Flush deferred notice cleanup after dialog/activity detach.
        } finally {
            if(Build.VERSION.SDK_INT>=33) context.getSystemService(LocaleManager::class.java)!!
                .applicationLocales=previousPlatformLocales!!
            preferences.edit().apply {
                if(previousTag==null) remove("language-tag") else putString("language-tag",previousTag)
                if(previousPlatformInitialized==null) remove("platform-initialized")
                else putBoolean("platform-initialized",previousPlatformInitialized!!)
            }.commit()
            PaintApplication.currentResources=previousResources
            Locale.setDefault(previousLocale)
            ShadowToast.reset()
        }
    }

    private fun launch(credits: List<ImageCredit>,state: Bundle?=null) {
        launchIntent=Intent(context,MediaGalleryActivity::class.java)
            .putExtra("document_image_credits",ImageCredit.write(credits).toString())
        createGallery(state)
    }

    private fun createGallery(state: Bundle?) {
        controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,launchIntent)
        controller.create(state).start().resume().visible().windowFocusChanged(true)
        advance()
        assertEquals("vi-Hani",AppLanguage.selectedTag(gallery))
        assertEquals("vi-Hani",gallery.resources.configuration.locales[0].toLanguageTag())
        assertEquals("vi-Hani",Locale.getDefault().toLanguageTag())
    }

    private fun field(dialog: AlertDialog)=dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text")
    private fun host(dialog: AlertDialog)=dialog.window!!.decorView.findViewById<FrameLayout>(android.R.id.content)
    private fun notice(dialog: AlertDialog)=host(dialog).findViewWithTag<View>("locale_notification")
    private fun click(dialog: AlertDialog,tag: String) {
        assertTrue(dialog.window!!.decorView.findViewWithTag<Button>(tag).performClick())
        advance()
    }

    private fun openEditor(): AlertDialog {
        assertTrue(gallery.window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick())
        return attachedEditor()
    }

    private fun attachedEditor(): AlertDialog {
        // In PAUSED mode, show/recreation needs ViewRoot traversal, not only focus dispatch.
        advance()
        val dialog=requireNotNull(ShadowAlertDialog.getLatestAlertDialog())
        assertTrue(dialog.isShowing)
        controller.windowFocusChanged(false)
        dialog.window!!.decorView.dispatchWindowFocusChanged(true)
        assertTrue(host(dialog).isAttachedToWindow)
        assertTrue(field(dialog).isAttachedToWindow)
        assertTrue(host(dialog).isShown)
        return dialog
    }

    private fun saveAndDestroy(): Bundle {
        val state=Bundle()
        controller.saveInstanceState(state).pause().stop().destroy()
        advance()
        return state
    }

    private fun assertResult(credits: List<ImageCredit>) {
        assertEquals(Activity.RESULT_OK,shadowOf(gallery).resultCode)
        val result=requireNotNull(shadowOf(gallery).resultIntent)
        assertFalse(result.hasExtra("gallery_file"))
        assertEquals(credits,ImageCredit.read(JSONArray(result.getStringExtra("document_image_credits"))))
    }

    private fun assertUncommitted() {
        assertEquals(Activity.RESULT_CANCELED,shadowOf(gallery).resultCode)
        assertNull(shadowOf(gallery).resultIntent)
    }

    private fun assertDialogFeedback(dialog: AlertDialog,resource: Int): View {
        val current=requireNotNull(notice(dialog))
        val text=requireNotNull(host(dialog).findViewWithTag<TextView>("locale_notification_text"))
        val expected=gallery.getString(resource)
        assertTrue("The actual feedback resource must exercise Nôm supplementary glyphs",expected.codePoints().anyMatch {it>0xffff})
        assertEquals(expected,text.text.toString())
        assertNotNull(LocaleTypography.typeface(gallery))
        assertSame(LocaleTypography.typeface(gallery),text.typeface)
        expected.codePoints().filter {it>0xffff}.forEach {point ->
            assertTrue("Nôm feedback glyph U+${point.toString(16)}",text.paint.hasGlyph(String(Character.toChars(point))))
        }
        assertTrue(current.isAttachedToWindow)
        assertSame(host(dialog),current.parent)
        assertEquals(1,(0 until host(dialog).childCount).count {host(dialog).getChildAt(it).tag=="locale_notification"})
        assertNull("Dialog feedback must not be hidden behind the modal window",
            gallery.window.decorView.findViewWithTag<View>("locale_notification"))
        assertNull("The attached Nôm dialog must use its bundled-font notice",ShadowToast.getLatestToast())
        assertTrue(dialog.isShowing)
        return current
    }

    @Test fun restoredSaveUsesTheNewDialogAndOldNoticeTimeoutCannotRemoveItsFeedback() {
        launch(listOf(original))
        val oldDialog=openEditor()
        val confirmed=original.copy(text="Confirmed before interruption")
        field(oldDialog).setText(confirmed.text)
        click(oldDialog,"gallery_credit_save")
        assertResult(listOf(confirmed))
        val oldNotice=assertDialogFeedback(oldDialog,R.string.gallery_credit_saved)
        advance(1000)
        val revised=confirmed.copy(text="Unconfirmed correction\n変更内容: cropped")
        field(oldDialog).setText(revised.text)

        val saved=saveAndDestroy()
        assertEquals(listOf(confirmed),ImageCredit.read(JSONArray(saved.getString("document_image_credits"))))
        assertTrue(saved.getBoolean("document_image_credits_edited"))
        assertEquals(original.source,saved.getString("image_credit_editor_source"))
        assertEquals(revised.text,saved.getString("image_credit_editor_draft"))
        assertFalse(oldDialog.isShowing)
        assertFalse(oldNotice.isAttachedToWindow)
        assertNull("Detached dialog children must be cleaned before reuse",oldNotice.parent)
        assertNull(notice(oldDialog))

        createGallery(saved)
        val restored=attachedEditor()
        assertNotSame(oldDialog,restored)
        assertNotSame(field(oldDialog),field(restored))
        assertEquals(revised.text,field(restored).text.toString())
        assertResult(listOf(confirmed)) // The recovered field has not committed itself.
        assertNull(notice(restored))
        click(restored,"gallery_credit_save")
        assertResult(listOf(revised))
        val current=assertDialogFeedback(restored,R.string.gallery_credit_saved)
        assertNotSame(oldNotice,current)
        assertNull(oldNotice.parent)
        advance(1100) // Past the old notice's original deadline, before the new one.
        assertSame(current,notice(restored))
        advance(1000)
        assertNull(notice(restored))
        assertNull(current.parent)
    }

    @Test fun restoredEmptyDraftCopyCommitsOnlyItsSelectedSourceAndCancelKeepsThatCommit() {
        val second=ImageCredit("https://example.org/b.png","Second saved credit")
        val saved=Bundle().apply {
            putString("document_image_credits",ImageCredit.write(listOf(original,second)).toString())
            putBoolean("document_image_credits_edited",false)
            putString("image_credit_editor_source",second.source)
            putString("image_credit_editor_draft","")
        }
        launch(listOf(original,second),saved)
        val restored=attachedEditor()
        assertEquals(1,restored.window!!.decorView.findViewWithTag<Spinner>("gallery_credit_source").selectedItemPosition)
        assertEquals("",field(restored).text.toString())
        assertUncommitted()
        click(restored,"gallery_credit_copy")
        val committed=listOf(original,second.copy(text=""))
        assertResult(committed)
        val clipboard=gallery.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        assertEquals("",clipboard.primaryClip!!.getItemAt(0).text.toString())
        val oldNotice=assertDialogFeedback(restored,R.string.gallery_credit_copied)

        field(restored).setText("Discard only this later draft")
        restored.cancel()
        advance()
        assertFalse(restored.isShowing)
        assertFalse(oldNotice.isAttachedToWindow)
        assertNull(oldNotice.parent)
        val again=saveAndDestroy()
        assertFalse(again.containsKey("image_credit_editor_source"))
        assertFalse(again.containsKey("image_credit_editor_draft"))
        assertEquals(committed,ImageCredit.read(JSONArray(again.getString("document_image_credits"))))
        assertTrue(again.getBoolean("document_image_credits_edited"))
        createGallery(again)
        assertFalse(ShadowAlertDialog.getLatestAlertDialog()?.isShowing==true)
        assertResult(committed)
        gallery.window.decorView.findViewWithTag<Button>("gallery_done").performClick()
        assertResult(committed)
    }

    @Test fun cancellingAnInterruptedUncommittedDraftDoesNotSaveOrReopenIt() {
        launch(listOf(original))
        val oldDialog=openEditor()
        field(oldDialog).setText("Discard this interrupted draft")
        assertUncommitted()
        val saved=saveAndDestroy()
        assertEquals(listOf(original),ImageCredit.read(JSONArray(saved.getString("document_image_credits"))))
        assertFalse(saved.getBoolean("document_image_credits_edited"))
        assertFalse(oldDialog.isShowing)
        createGallery(saved)
        val restored=attachedEditor()
        assertNotSame(oldDialog,restored)
        assertEquals("Discard this interrupted draft",field(restored).text.toString())
        assertUncommitted()
        restored.cancel() // Back/cancellation must not call Save, Copy or Done.
        advance()
        assertUncommitted()
        assertNull(ShadowToast.getLatestToast())
        val again=saveAndDestroy()
        assertFalse(again.containsKey("image_credit_editor_source"))
        assertFalse(again.containsKey("image_credit_editor_draft"))
        assertEquals(listOf(original),ImageCredit.read(JSONArray(again.getString("document_image_credits"))))
        assertFalse(again.getBoolean("document_image_credits_edited"))
        createGallery(again)
        assertFalse(ShadowAlertDialog.getLatestAlertDialog()?.isShowing==true)
        gallery.window.decorView.findViewWithTag<Button>("gallery_done").performClick()
        assertUncommitted()
    }
}
