/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.os.Looper
import android.util.AtomicFile
import android.view.View
import android.widget.EditText
import android.widget.Spinner
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.AutosaveStore
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.ImageFormat
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.Implementation
import org.robolectric.annotation.Implements
import org.robolectric.annotation.LooperMode
import org.robolectric.annotation.RealObject
import org.robolectric.shadow.api.Shadow
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.util.ReflectionHelpers
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.util.Locale
import java.util.concurrent.ExecutorService
import java.util.concurrent.TimeUnit

/** Actual failed recovery, localized menu actions and Android picker contracts.
 * Host Android runtime coverage does not establish native-speaker acceptance.
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi",shadows=[RecoveryCopyWriteFailureAtomicFile::class])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class ProtectedDraftWarningTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val original="Unreadable previous draft that must not be replaced 作品".toByteArray(Charsets.UTF_8)
    private fun idle()=shadowOf(Looper.getMainLooper()).idle()
    private fun worker(activity: ClassicPaintActivity)=ReflectionHelpers.getField<ExecutorService>(activity,"worker")

    @Before fun clean() {
        // Join any previously admitted writes before preparing the on-disk failure fixture.
        AutosaveStore(context.filesDir).exists()
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-") && it.isFile}?.forEach {assertTrue(it.delete())}
        listOf("classic-ui","export").forEach {context.getSharedPreferences(it,0).edit().clear().commit()}
        RecoveryCopyWriteFailureAtomicFile.failedCopies=0
    }

    @Test fun englishWarningLeadsToDistinctRecoveryAndCurrentArtworkRoutes()=checkRoutes("en-US")
    @Test fun koreanWarningLeadsToDistinctRecoveryAndCurrentArtworkRoutes()=checkRoutes("ko-KR")
    @Test fun northKoreanWarningLeadsToDistinctRecoveryAndCurrentArtworkRoutes()=checkRoutes("ko-KP")
    @Test fun mixedScriptKoreanWarningLeadsToDistinctRecoveryAndCurrentArtworkRoutes()=checkRoutes("ko-Kore-KR")

    private fun checkRoutes(tag: String) {
        val previous=AppLanguage.selectedTag(context)
        val previousLocale=Locale.getDefault()
        val store=AutosaveStore(context.filesDir)
        store.file.writeBytes(original)
        AppLanguage.select(context,tag)
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java)
        val activity=controller.get()
        try {
            controller.create().start().resume().visible()
            awaitEditorStartup(activity)
            assertEquals("The real startup path attempted and failed to preserve the old draft",1,RecoveryCopyWriteFailureAtomicFile.failedCopies)
            assertTrue(ReflectionHelpers.getField<Boolean>(activity,"autosaveBlocked"))
            assertEquals(activity.getString(R.string.ui_the_previous_draft_could_not_be_preserved_separately),activity.lastAutosaveError)
            assertProtected(store)

            val notice=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            assertTrue(notice.isShowing)
            val reason=activity.getString(R.string.ui_the_previous_draft_could_not_be_restored)
            val warning=shadowOf(notice).message.toString()
            assertEquals(activity.getString(R.string.ui_autosave_is_paused_to_protect_that_draft_use,reason),warning)
            assertTrue("The triggering failure reason remains visible",warning.contains(reason))
            for(id in listOf(R.string.ui_menu_file,R.string.ui_export_recovery_copy,R.string.save20_title))
                assertTrue("Warning must name the actual menu caption: ${activity.getString(id)}",warning.contains(activity.getString(id)))
            assertTrue(warning.contains("PNG"));assertTrue(warning.contains("JPEG"));assertFalse(warning.contains("%1\$s"))
            assertTrue(notice.getButton(AlertDialog.BUTTON_POSITIVE).performClick());idle()
            assertEquals(activity.getString(R.string.ui_menu_file),activity.window.decorView.findViewWithTag<TextView>("menu_File").text.toString())

            // Make current work observably different from the protected, unreadable old draft.
            activity.document.newImage(17,11)
            activity.document.bitmap.eraseColor(Color.MAGENTA)
            activity.document.edited()
            idlePastAutosave(activity)
            assertProtected(store)

            EditorTestNavigation.named(activity,"File",activity.getString(R.string.ui_export_recovery_copy))
            val recovery=shadowOf(activity).nextStartedActivityForResult
            assertNotNull(recovery)
            assertEquals(ClassicPaintActivity.EXPORT_RECOVERY,recovery.requestCode)
            assertEquals(Intent.ACTION_CREATE_DOCUMENT,recovery.intent.action)
            assertEquals("application/zip",recovery.intent.type)
            assertTrue(recovery.intent.hasCategory(Intent.CATEGORY_OPENABLE))
            assertTrue(recovery.intent.getStringExtra(Intent.EXTRA_TITLE)!!.endsWith(".zip"))
            val recoverySource=ReflectionHelpers.getField<File>(activity,"recoveryExport")
            assertEquals(store.file.canonicalFile,recoverySource.canonicalFile)
            assertArrayEquals("Recovery export is the protected old draft, not current artwork",original,recoverySource.readBytes())
            shadowOf(activity).nextStartedActivity
            activity.onActivityResult(recovery.requestCode,Activity.RESULT_CANCELED,null);idle()
            assertFalse(activity.busy);assertProtected(store)

            // Both the explicit Cancel button and dialog cancellation leave all work intact.
            for(cancelWithButton in listOf(true,false)) {
                val options=openSaveOptions(activity)
                assertNull(shadowOf(activity).nextStartedActivityForResult)
                if(cancelWithButton) assertTrue(options.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()) else options.cancel()
                idle();assertCurrentArtwork(activity);assertProtected(store)
                assertNull(shadowOf(activity).nextStartedActivityForResult)
            }

            // PNG/JPEG are choices inside Save as, not separate File-menu commands.
            for(format in listOf(ImageFormat.PNG,ImageFormat.JPEG)) {
                val options=openSaveOptions(activity)
                val spinner=options.window!!.decorView.findViewWithTag<Spinner>("export_format")
                val choices=(0 until spinner.count).map {spinner.getItemAtPosition(it).toString()}
                assertTrue(choices.contains(ImageFormat.PNG.label));assertTrue(choices.contains(ImageFormat.JPEG.label))
                options.window!!.decorView.findViewWithTag<EditText>("export_filename").setText("Current artwork")
                EditorTestNavigation.format(spinner,format)
                assertTrue(options.getButton(AlertDialog.BUTTON_POSITIVE).performClick());idle()
                val save=shadowOf(activity).nextStartedActivityForResult
                assertNotNull(save)
                assertEquals(ClassicPaintActivity.SAVE_IMAGE,save.requestCode)
                assertEquals(Intent.ACTION_CREATE_DOCUMENT,save.intent.action)
                assertEquals(format.mime,save.intent.type)
                assertTrue(save.intent.hasCategory(Intent.CATEGORY_OPENABLE))
                assertEquals("Current artwork"+format.extension,save.intent.getStringExtra(Intent.EXTRA_TITLE))
                shadowOf(activity).nextStartedActivity
                activity.onActivityResult(save.requestCode,Activity.RESULT_CANCELED,null);idle()
                assertFalse(activity.busy);assertCurrentArtwork(activity);assertProtected(store)
            }
            idlePastAutosave(activity)
            assertProtected(store)
        } finally {
            if(!activity.isDestroyed) controller.pause().stop().destroy()
            assertTrue(worker(activity).awaitTermination(10,TimeUnit.SECONDS))
            idle()
            AppLanguage.select(context,previous);Locale.setDefault(previousLocale)
        }
        // Lifecycle saves must also respect the protection after canceled pickers.
        assertProtected(store)
    }

    private fun openSaveOptions(activity: ClassicPaintActivity): AlertDialog {
        EditorTestNavigation.named(activity,"File",activity.getString(R.string.save20_title))
        val options=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        assertTrue(options.isShowing)
        assertEquals(activity.getString(R.string.save20_title),shadowOf(options).title.toString())
        assertNotNull(options.window!!.decorView.findViewWithTag<View>("export_format"))
        return options
    }
    private fun idlePastAutosave(activity: ClassicPaintActivity) {
        shadowOf(Looper.getMainLooper()).idleFor(2,TimeUnit.SECONDS)
        worker(activity).submit {}.get(10,TimeUnit.SECONDS)
        idle()
    }
    private fun assertProtected(store: AutosaveStore) {
        assertArrayEquals("Protected original bytes were changed",original,store.file.readBytes())
        assertTrue("Failed preservation must not be reported as a usable recovery copy",store.recoveryCopies().isEmpty())
    }
    private fun assertCurrentArtwork(activity: ClassicPaintActivity) {
        assertEquals(17,activity.document.bitmap.width);assertEquals(11,activity.document.bitmap.height)
        assertEquals(Color.MAGENTA,activity.document.bitmap.getPixel(2,3))
    }
}

/** Inject only the storage failure. Recovery, warning, menu and picker code are unmodified.
 * This avoids host-user/OS-dependent chmod failures while preserving the real exception path.
 */
@Implements(AtomicFile::class)
class RecoveryCopyWriteFailureAtomicFile {
    @RealObject private lateinit var actual: AtomicFile
    companion object { @Volatile var failedCopies=0 }
    @Implementation fun startWrite(): FileOutputStream {
        if(actual.baseFile.name.startsWith("classic-draft-recovery-")) {
            failedCopies++
            throw IOException("Recovery-copy storage unavailable in this fixture")
        }
        return Shadow.directlyOn(actual,AtomicFile::class.java,"startWrite")
    }
}
