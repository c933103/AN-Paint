/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.RectF
import android.util.AtomicFile
import org.catrobat.paintroid.classic.AutosaveDraft
import org.catrobat.paintroid.classic.AutosaveStore
import org.catrobat.paintroid.classic.ImageCredit
import org.catrobat.paintroid.classic.PaintDocument
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Rule
import org.junit.Test
import org.junit.rules.TemporaryFolder
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.util.ReflectionHelpers
import java.io.File
import java.io.FileOutputStream
import java.util.concurrent.Callable
import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executors
import java.util.concurrent.Future
import java.util.concurrent.TimeUnit
import java.util.concurrent.TimeoutException

/** Uses only the pre-fix public API: this test must fail before the handover repair. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class AutosaveInFlightRecoveryTest {
    @get:Rule val temporary=TemporaryFolder()

    @Test fun replacementWaitsForFirstAtomicWriteAndRestoresPixelsSelectionAndOriginalCredits() {
        val directory=temporary.newFolder("draft")
        val writer=AutosaveStore(directory)
        val replacement=AutosaveStore(directory)
        val document=PaintDocument(7,5,File(directory,"old-history"))
        val credit=ImageCredit("https://example.org/art.png","Artwork 作品\nArtist 作者 👩🏽‍🎨\nCC BY-SA 4.0\nhttps://example.org/artist")
        document.bitmap.setPixel(2,3,Color.BLUE)
        document.paste(Bitmap.createBitmap(3,2,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.MAGENTA)},
            takeOwnership=true,credits=listOf(credit))
        document.selection!!.rect.set(1f,2f,4f,4f)
        document.selection!!.rotation=17f
        val metadata=JSONObject().put("version",1)
            .put("image_credits",document.imageCreditsState())
            .put("floating_rect",JSONArray(listOf(1f,2f,4f,4f))).put("floating_rotation",17.0)
        val writeStarted=CountDownLatch(1)
        val finishWrite=CountDownLatch(1)
        ReflectionHelpers.setField(writer,"atomic",object: AtomicFile(writer.file) {
            override fun startWrite(): FileOutputStream {
                val stream=super.startWrite() // The first draft now exists only as .new.
                writeStarted.countDown()
                try {check(finishWrite.await(10,TimeUnit.SECONDS)) {"Test did not release the write"}}
                catch(error: Throwable) {super.failWrite(stream);throw error}
                return stream
            }
        })
        val threads=Executors.newFixedThreadPool(2)
        var saved: Future<*>?=null
        var recovered: Future<AutosaveDraft?>?=null
        try {
            saved=threads.submit {writer.write(document.bitmap,document.selection!!.image,metadata,document.historySnapshot())}
            assertTrue("Initial AtomicFile write started",writeStarted.await(5,TimeUnit.SECONDS))
            assertFalse("No committed draft exists yet",writer.file.exists())
            val recoveryStarted=CountDownLatch(1)
            recovered=threads.submit(Callable {
                recoveryStarted.countDown()
                if(replacement.exists()) replacement.read {_,_->} else null
            })
            assertTrue(recoveryStarted.await(5,TimeUnit.SECONDS))
            try {
                recovered.get(200,TimeUnit.MILLISECONDS)
                fail("Recovery must wait for the initial atomic draft, not initialize a blank document")
            } catch(_: TimeoutException) { /* The writer is explicitly gated, not delayed by a sleep. */ }
            finishWrite.countDown();saved.get(5,TimeUnit.SECONDS)
            val draft=recovered.get(5,TimeUnit.SECONDS)
            assertNotNull(draft)
            val restored=PaintDocument(1,1,File(directory,"new-history"))
            try {
                restored.replace(draft!!.image)
                val rect=draft.metadata.getJSONArray("floating_rect")
                restored.restoreFloatingSelection(draft.floating!!,
                    RectF(rect.getDouble(0).toFloat(),rect.getDouble(1).toFloat(),rect.getDouble(2).toFloat(),rect.getDouble(3).toFloat()),
                    draft.metadata.getDouble("floating_rotation").toFloat())
                restored.restoreImageCredits(draft.metadata.getJSONObject("image_credits"))
                assertEquals(7,restored.bitmap.width);assertEquals(5,restored.bitmap.height)
                assertEquals(Color.BLUE,restored.bitmap.getPixel(2,3))
                assertEquals(Color.WHITE,restored.bitmap.getPixel(0,0))
                assertEquals(3,restored.selection!!.image.width);assertEquals(2,restored.selection!!.image.height)
                assertEquals(Color.MAGENTA,restored.selection!!.image.getPixel(0,0))
                assertEquals(RectF(1f,2f,4f,4f),restored.selection!!.rect)
                assertEquals(17f,restored.selection!!.rotation,0f)
                assertTrue(restored.selection!!.floating)
                assertEquals(listOf(credit),restored.imageCredits)
            } finally {restored.close()}
        } finally {
            finishWrite.countDown()
            threads.shutdown()
            assertTrue("Test workers finished",threads.awaitTermination(10,TimeUnit.SECONDS))
            saved?.get(5,TimeUnit.SECONDS)
            recovered?.get(5,TimeUnit.SECONDS)?.let {
                if(!it.image.isRecycled) it.image.recycle()
                it.floating?.let {bitmap -> if(!bitmap.isRecycled) bitmap.recycle()}
            }
            document.close()
        }
    }
}
