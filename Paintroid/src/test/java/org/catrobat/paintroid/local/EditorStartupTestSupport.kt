/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.os.Looper
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.junit.Assert.assertTrue
import org.robolectric.Shadows.shadowOf
import java.util.concurrent.TimeUnit

/** Activity creation returns before recovery finishes. Resumed fixtures also await the
 * first traversal, so its fresh-canvas sizing cannot later overwrite a fixture's edits.
 * A deliberately stopped editor can test durable recovery without requiring a window layout.
 */
internal fun awaitEditorStartup(activity: ClassicPaintActivity,requireLayout: Boolean=true) {
    val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(10)
    fun ready()=activity.startupReady && (!requireLayout || (activity.paintCanvas.width>0 && activity.paintCanvas.height>0))
    while(!ready() && System.nanoTime()<deadline) {
        if(activity.startupReady) shadowOf(Looper.getMainLooper()).idleFor(16,TimeUnit.MILLISECONDS)
        else shadowOf(Looper.getMainLooper()).idle()
        if(!ready()) Thread.sleep(5)
    }
    shadowOf(Looper.getMainLooper()).idle()
    assertTrue("Editor startup did not finish within 10 seconds; last I/O error: ${activity.lastIoError}",
        activity.startupReady)
    assertTrue("Editor canvas did not complete its initial layout within 10 seconds",ready())
}
