/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.graphics.Color
import android.os.Build
import android.os.Process
import android.widget.EditText
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.catrobat.paintroid.R
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File

/** Ordinary instrumentation in a genuinely new process after host force-stop. */
@android.annotation.TargetApi(35)
@RunWith(AndroidJUnit4::class)
class AcceptedCreditRestartVerifyTest {
    @Test fun acceptedTextIsRecoverableWithoutAutomaticDocumentAssociation() {
        val f=AcceptedCreditRestartFixture
        assertEquals(35,Build.VERSION.SDK_INT)
        assertNotEquals("Verify must retain normal runner cleanup","false",
            InstrumentationRegistry.getArguments().getString("waitForActivitiesToComplete"))
        val marker=f.json(f.markerFile)
        assertNotEquals("Verify runs in a different PID",marker.getInt("pid"),Process.myPid())
        assertTrue("Verify process started after the seed process",
            Process.getStartElapsedRealtime()>marker.getLong("process_start"))
        val source=marker.getString("source")
        val fixture=marker.getString("fixture")
        assertEquals("https://catrobat.org/wp-content/uploads/2025/01/Restart_$fixture.png",source)
        val expected=f.acceptedText(fixture)
        assertEquals(marker.getString("accepted_sha256"),f.digest(expected.toByteArray(Charsets.UTF_8)))
        // Read before launch: no restoration, teardown or fresh autosave can hide
        // whether the killed process left the original disk state unchanged.
        assertEquals(marker.getString("autosave_sha256"),f.digest(File(f.context.filesDir,"classic-autosave.zip")))
        val session=File(f.context.filesDir,marker.getString("session"))
        val snapshot=File(f.context.filesDir,"retained-image-credits/${marker.getString("snapshot")}.json")
        assertEquals(marker.getString("session_sha256"),f.digest(session))
        assertEquals(marker.getString("snapshot_sha256"),f.digest(snapshot))
        f.assertCreditJson(f.json(session),source,expected)
        f.assertCreditJson(f.json(snapshot),source,expected)
        f.assertOriginalArchive(source)
        val scenario=f.launchEditor()
        try {
            f.onMain {f.assertOriginalDrawing(f.editor,source)}
            f.openArchive(source,expected)
            f.tap("legacy_credit_done")
            f.await("original editor resumed") {f.editor.hasWindowFocus() && !f.editor.busy}
            f.onMain {f.assertOriginalDrawing(f.editor,source)}
            // New is a production menu action. The saved original is not dirty,
            // so no discard shortcut or direct document mutation is needed.
            f.menu("File",R.string.ui_new)
            f.onMain {
                (f.view("size_width") as EditText).setText("19")
                (f.view("size_height") as EditText).setText("13")
            }
            f.positive()
            f.await("new blank drawing") {!f.editor.busy && f.editor.document.bitmap.width==19 && f.editor.document.bitmap.height==13}
            f.onMain {
                assertTrue("New must not inherit archived credits",f.editor.document.imageCredits.isEmpty())
                f.assertPixels(f.editor.document.bitmap,19,13) {_,_->Color.WHITE}
            }
            f.openArchive(source,expected)
            f.onMain {
                assertTrue("Browsing never associates the archive automatically",f.editor.document.imageCredits.isEmpty())
                f.assertPixels(f.editor.document.bitmap,19,13) {_,_->Color.WHITE}
            }
            f.tap("legacy_credit_add")
            f.await("explicit selected attachment") {!f.editor.busy && f.editor.document.imageCredits.size==1}
            f.onMain {
                assertEquals(listOf(source),f.editor.document.imageCredits.map {it.source})
                assertEquals(listOf(expected),f.editor.document.imageCredits.map {it.text})
                f.assertPixels(f.editor.document.bitmap,19,13) {_,_->Color.WHITE}
            }
        } finally {
            // Only the verify phase may finish activities normally.
            scenario.close()
        }
    }
}
