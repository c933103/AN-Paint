/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Color
import org.catrobat.paintroid.classic.*
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File
import java.util.zip.ZipEntry
import java.util.zip.ZipFile
import java.util.zip.ZipOutputStream

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class DraftHistoryTest {
    private fun directory()=File(RuntimeEnvironment.getApplication().filesDir,"history-test-${java.util.UUID.randomUUID()}").apply {mkdirs()}
    @Test fun savedStackRestoresPixelSizesAndOrderWithoutAnyOriginalSessionFiles() {
        val folder=directory();val store=AutosaveStore(folder)
        val first=PaintDocument(12,8,File(folder,"old-cache"))
        first.foreground=Color.RED;first.fill(0,0)
        first.resize(6,4,true);first.foreground=Color.BLUE;first.fill(0,0)
        first.undo()
        store.write(first.bitmap,null,JSONObject().put("version",1),first.historySnapshot())
        first.close();File(folder,"old-cache").deleteRecursively()
        val second=PaintDocument(1,1,File(folder,"new-cache"))
        try {
            val draft=store.read(historyReader=second::readHistory) {_,_->}
            assertFalse(draft.historyFailed);second.replace(draft.image);second.restoreHistory(draft.history!!)
            assertTrue(second.canUndo);assertTrue(second.canRedo);assertEquals(6,second.bitmap.width)
            second.redo();assertEquals(Color.BLUE,second.bitmap.getPixel(0,0))
            second.undo();assertEquals(Color.RED,second.bitmap.getPixel(0,0))
            second.undo();assertEquals(12,second.bitmap.width);assertEquals(8,second.bitmap.height)
            second.undo();assertEquals(Color.WHITE,second.bitmap.getPixel(0,0));assertFalse(second.canUndo)
        } finally {second.close();folder.deleteRecursively()}
    }
    @Test fun incompleteHistoryWriteKeepsThePreviousAtomicDraftAndDamagedHistoryDoesNotDiscardItsCanvas() {
        val folder=directory();val store=AutosaveStore(folder);val doc=PaintDocument(8,6,File(folder,"cache"))
        try {
            doc.foreground=Color.RED;doc.fill(0,0)
            store.write(doc.bitmap,null,JSONObject().put("version",1),doc.historySnapshot())
            val original=store.file.readBytes()
            doc.historySnapshot().undo.first().file.delete()
            try {store.write(doc.bitmap,null,JSONObject().put("version",1),doc.historySnapshot());fail("Missing history must fail the whole transaction")} catch(_:java.io.IOException) {}
            assertArrayEquals(original,store.file.readBytes())
            val replacement=File(folder,"damaged.zip")
            ZipFile(store.file).use {source ->ZipOutputStream(replacement.outputStream()).use {out ->
                source.entries().asSequence().forEach {entry ->
                    out.putNextEntry(ZipEntry(entry.name))
                    if(entry.name=="history/undo/0.rgba") out.write("damaged".toByteArray()) else source.getInputStream(entry).use {it.copyTo(out)}
                    out.closeEntry()
                }
            }}
            replacement.copyTo(store.file,overwrite=true)
            val recovered=store.read(historyReader=doc::readHistory) {_,_->}
            try {assertTrue(recovered.historyFailed);assertNull(recovered.history);assertEquals(Color.RED,recovered.image.getPixel(0,0))}
            finally {recovered.image.recycle()}
        } finally {doc.close();folder.deleteRecursively()}
    }
}
