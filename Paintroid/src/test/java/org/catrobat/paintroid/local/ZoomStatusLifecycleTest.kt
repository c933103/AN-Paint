/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.content.res.Configuration
import android.graphics.Color
import android.os.Looper
import android.view.View
import android.widget.LinearLayout
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.AutosaveStore
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.PaintApplication
import org.catrobat.paintroid.classic.VerticalText
import org.catrobat.paintroid.classic.ZoomStatusLayout
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
import java.util.Locale

/** Code-regression fixture for the transient locale/view-tree mismatch at stop.
 * It is not a language review, a picker journey, or a new rendering policy.
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[35],qualifiers="w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ZoomStatusLifecycleTest {
    @Test fun oldVerticalFooterCanAutosaveAfterResourceLocaleBecomesHorizontal() {
        val app=RuntimeEnvironment.getApplication() as Context
        val oldTag=AppLanguage.selectedTag(app)
        val oldLocale=Locale.getDefault()
        val oldResources=PaintApplication.currentResources
        var activeController: ActivityController<ClassicPaintActivity>?=null
        var activeActivity: ClassicPaintActivity?=null
        var original: Configuration?=null
        var setupCompleted=false
        var stopped=false
        var stopCompleted=false
        var failure: Throwable?=null
        fun awaitIdle(activity: ClassicPaintActivity) {
            val until=System.nanoTime()+15_000_000_000L
            do {
                shadowOf(Looper.getMainLooper()).idle()
                if(!activity.busy) return
                Thread.sleep(10)
            } while(System.nanoTime()<until)
            fail("Real lifecycle autosave did not finish")
        }
        try {
            app.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {check(it.delete())}
            app.getSharedPreferences("classic-ui",0).edit().clear().commit()
            AppLanguage.select(app,"en-XV")
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java)
            activeController=controller
            val activity=controller.get()
            activeActivity=activity
            controller.setup().visible().windowFocusChanged(true)
            setupCompleted=true
            val verticalConfiguration=Configuration(activity.resources.configuration)
            original=verticalConfiguration
            awaitEditorStartup(activity);awaitIdle(activity)
            assertTrue(VerticalText.uiVertical(activity))
            val root=activity.window.decorView
            val footer=root.findViewWithTag<View>("status_bar")
            val rail=root.findViewWithTag<View>("vertical_status_rail")
            assertTrue(footer is LinearLayout)
            assertFalse(footer is ZoomStatusLayout)
            assertNotNull(rail)
            activity.document.newImage(19,13)
            activity.document.bitmap.setPixel(4,7,Color.MAGENTA)
            // Model the observed framework resource change before the old tree
            // receives stop. Do not rebuild the workspace or disable autosave.
            val horizontal=Configuration(verticalConfiguration).apply {setLocale(Locale.US)}
            @Suppress("DEPRECATION")
            activity.resources.updateConfiguration(horizontal,activity.resources.displayMetrics)
            assertFalse(VerticalText.uiVertical(activity))
            assertSame(footer,root.findViewWithTag<View>("status_bar"))
            assertSame(rail,root.findViewWithTag<View>("vertical_status_rail"))
            controller.pause();stopped=true;controller.stop();stopCompleted=true
            awaitIdle(activity)
            assertNull(activity.lastAutosaveError)
            val store=AutosaveStore(app.filesDir)
            assertTrue("Real stop wrote an autosave",store.exists())
            val draft=store.read {width,height ->
                assertEquals(19,width);assertEquals(13,height)
            }
            try {
                assertEquals(19,draft.image.width);assertEquals(13,draft.image.height)
                assertEquals("Stop saved the new marked document",Color.MAGENTA,draft.image.getPixel(4,7))
            } finally {draft.image.recycle();draft.floating?.recycle()}
        } catch(error: Throwable) {
            failure=error
        } finally {
            fun cleanup(action: ()->Unit) {
                try {action()} catch(error: Throwable) {
                    if(failure==null) failure=error else failure!!.addSuppressed(error)
                }
            }
            cleanup {
                val activity=activeActivity
                if(activity!=null && original!=null) {
                    @Suppress("DEPRECATION")
                    activity.resources.updateConfiguration(original,activity.resources.displayMetrics)
                }
            }
            cleanup {
                val controller=activeController
                val activity=activeActivity
                if(setupCompleted && controller!=null && activity!=null) {
                    if(!stopped) {controller.pause();stopped=true;controller.stop();stopCompleted=true}
                // A failed stop can leave busy set before any write was queued.
                // Do not mask that original exception with a cleanup timeout.
                    if(stopCompleted) awaitIdle(activity)
                }
            }
            cleanup {activeController?.destroy()}
            cleanup {AppLanguage.select(app,oldTag)}
            cleanup {PaintApplication.currentResources=oldResources;Locale.setDefault(oldLocale)}
        }
        failure?.let {throw it}
    }
}
