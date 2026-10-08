/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
import android.graphics.Color
import org.catrobat.paintroid.classic.*
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File
import java.util.zip.ZipFile

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class AutosaveMetadataBoundsTest {
    private fun folder()=File(RuntimeEnvironment.getApplication().filesDir,"credit-bounds-${java.util.UUID.randomUUID()}").apply {mkdirs()}
    private fun image(colour: Int)=Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888).apply {eraseColor(colour)}
    private fun rejected(action: ()->Unit) {
        try {action();fail("An oversized operation must be rejected as a whole")}
        catch(_: IllegalArgumentException) { }
    }
    private fun metadata(text: String)=JSONObject().put("version",1).put("note",text)

    @Test fun exactUtf8ArchiveLimitRoundTripsAndOneByteOverflowPreservesThePreviousZip() {
        val folder=folder();val store=AutosaveStore(folder)
        val red=image(Color.RED);val blue=image(Color.BLUE)
        // Supplementary characters consume four UTF-8 bytes, unlike String.length's two units.
        val prefix="𠀀漢\n\"\\".repeat(200)
        val padding=AutosaveStore.MAX_METADATA_BYTES-metadata(prefix).toString().toByteArray(Charsets.UTF_8).size
        val valid=metadata(prefix+"a".repeat(padding))
        try {
            assertEquals(AutosaveStore.MAX_METADATA_BYTES,valid.toString().toByteArray(Charsets.UTF_8).size)
            store.write(red,null,valid)
            val original=store.file.readBytes()
            val restored=store.read {_,_->}
            assertEquals(valid.getString("note"),restored.metadata.getString("note"))
            assertEquals(Color.RED,restored.image.getPixel(0,0));restored.image.recycle()
            rejected {store.write(blue,null,metadata(valid.getString("note")+"a"))}
            assertArrayEquals(original,store.file.readBytes())
            val after=store.read {_,_->}
            assertEquals(Color.RED,after.image.getPixel(0,0));after.image.recycle()
            ZipFile(store.file).use {assertEquals(AutosaveStore.MAX_METADATA_BYTES.toLong(),it.getEntry("draft.json").size)}
        } finally {red.recycle();blue.recycle();folder.deleteRecursively()}
    }

    @Test fun oversizedHistoryIndexCannotReplaceAReadableDrawing() {
        val folder=folder();val store=AutosaveStore(folder);val pixels=image(Color.RED)
        try {
            store.write(pixels,null,metadata("original"))
            val original=store.file.readBytes()
            val entry=RasterHistory.Entry(File(folder,"not-read-before-validation"),2,2,
                listOf(ImageCredit("https://example.org/a","𠀀".repeat(HistoryArchive.MAX_INDEX_BYTES/4))))
            rejected {store.write(pixels,null,metadata("new"),RasterHistory.Snapshot(listOf(entry)))}
            assertArrayEquals(original,store.file.readBytes())
        } finally {pixels.recycle();folder.deleteRecursively()}
    }

}
