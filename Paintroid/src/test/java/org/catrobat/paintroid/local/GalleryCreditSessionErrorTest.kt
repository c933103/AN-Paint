/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.app.LocaleManager
import android.content.Context
import android.content.Intent
import android.content.res.Resources
import android.os.Build
import android.os.Bundle
import android.os.LocaleList
import android.os.Looper
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.ImageCredit
import org.catrobat.paintroid.classic.ImageCreditArchive
import org.catrobat.paintroid.classic.CreditEditSession
import org.catrobat.paintroid.classic.LegacyImageCreditsActivity
import org.catrobat.paintroid.classic.LocaleTypography
import org.catrobat.paintroid.classic.MediaGalleryActivity
import org.catrobat.paintroid.classic.PaintApplication
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

/** Missing private transport remains readable in the actual Nôm dialog across lifecycle events. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class GalleryCreditSessionErrorTest {
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

    private fun launch(state: Bundle?=null) {
        launchIntent=Intent(context,MediaGalleryActivity::class.java).putExtra(CreditEditSession.EXTRA_SESSION,
            "credit-edit-00000000-0000-0000-0000-000000000000.json")
        controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,launchIntent)
            .create(state).start().resume().visible()
        advance()
    }
    private fun errorDialog(): AlertDialog {
        val dialog=ShadowAlertDialog.getLatestAlertDialog()
        assertTrue(dialog.isShowing);assertFalse(gallery.isFinishing)
        val text=dialog.findViewById<TextView>(android.R.id.message)
        assertEquals(gallery.getString(R.string.gallery_credit_could_not_save),text.text.toString())
        assertEquals("vi-Hani",AppLanguage.locale(gallery).toLanguageTag())
        assertNotNull(LocaleTypography.typeface(gallery))
        assertSame(LocaleTypography.typeface(gallery),text.typeface)
        assertNull(ShadowToast.getTextOfLatestToast())
        return dialog
    }
    @Test fun missingPrivateSessionKeepsNomErrorUntilDone() {
        launch()
        errorDialog().getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertTrue(gallery.isFinishing)
    }
    @Test fun cancellingMissingSessionErrorFinishesWithoutAcceptingAResult() {
        launch()
        errorDialog().cancel()
        assertTrue(gallery.isFinishing)
        assertEquals(Activity.RESULT_CANCELED,shadowOf(gallery).resultCode)
    }
    @Test fun failedRecreationIgnoresPendingArchiveResultAndKeepsEveryStoredByte() {
        val credit=ImageCredit("https://example.org/preserved.png","Accepted recovery text 𠀀")
        val retained=ImageCreditArchive.retainAccepted(context,listOf(credit))
        val stored=java.io.File(context.filesDir,"retained-image-credits/$retained.json")
        val before=stored.readBytes()
        try {
            launch();val old=errorDialog()
            val state=Bundle();controller.saveInstanceState(state).pause().stop().destroy()
            assertFalse(old.isShowing)
            launch(state);val current=errorDialog()
            // The private archive request code is stable; this models its delayed Android result.
            gallery.onActivityResult(1,Activity.RESULT_OK,Intent().putExtra(
                LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN,ImageCreditArchive.selectionToken(credit)))
            assertSame(current,errorDialog())
            assertEquals(Activity.RESULT_CANCELED,shadowOf(gallery).resultCode)
            assertArrayEquals(before,stored.readBytes())
            assertEquals(credit,ImageCreditArchive.find(context,ImageCreditArchive.selectionToken(credit)))
        } finally {ImageCreditArchive.releaseAccepted(context,retained)}
    }
}
