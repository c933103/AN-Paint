/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.RectF
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

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ImageCreditLifecycleTest {
    private val credit=ImageCredit("https://example.org/art.png","Artwork — Author\nCC BY 4.0\nhttps://example.org/art")
    private fun folder()=File(RuntimeEnvironment.getApplication().filesDir,"credit-test-${java.util.UUID.randomUUID()}").apply {mkdirs()}
    private fun insert(doc: PaintDocument) {
        doc.paste(Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.RED)},true,listOf(credit))
    }
    @Test fun floatingCancellationUndoRedoAndNewDocumentKeepCreditsMatchedToInsertedPixels() {
        val folder=folder();val doc=PaintDocument(8,6,folder)
        try {
            insert(doc);assertEquals(listOf(credit),doc.imageCredits)
            doc.deleteSelection();assertTrue(doc.imageCredits.isEmpty())
            insert(doc);doc.undo();assertTrue(doc.imageCredits.isEmpty())
            assertEquals(Color.WHITE,doc.bitmap.getPixel(0,0))
            doc.redo();assertEquals(listOf(credit),doc.imageCredits)
            doc.editImageCredit(credit.source,"Edited creator and modifications")
            doc.undo();assertTrue(doc.imageCredits.isEmpty());doc.redo()
            assertEquals("Edited creator and modifications",doc.imageCredits.single().text)
            doc.editImageCredit(credit.source,credit.text)
            assertEquals(Color.RED,doc.bitmap.getPixel(0,0))
            doc.resize(10,8,true);doc.markSaved();assertEquals(listOf(credit),doc.imageCredits)
            doc.replace(Bitmap.createBitmap(3,3,Bitmap.Config.ARGB_8888),asEdit=true)
            assertEquals(listOf(credit),doc.imageCredits)
            doc.newImage(8,6);assertTrue(doc.imageCredits.isEmpty())
        } finally {doc.close();folder.deleteRecursively()}
    }
    @Test fun clipboardCarriesPendingAttributionIntoAnotherDocumentAndDeduplicatesRepeatedInsertion() {
        val folder=folder();val doc=PaintDocument(8,6,folder)
        try {
            insert(doc);assertTrue(doc.copySelection());doc.deleteSelection();doc.newImage(8,6)
            assertTrue(doc.imageCredits.isEmpty());assertTrue(doc.paste());doc.finishSelection()
            doc.paste();doc.finishSelection();assertEquals(listOf(credit),doc.imageCredits)
            doc.clear();assertTrue(doc.imageCredits.isEmpty());doc.undo();assertEquals(listOf(credit),doc.imageCredits)
        } finally {doc.close();folder.deleteRecursively()}
    }
    @Test fun floatingCopyAndCutTransferOnlyTheirOwnSourcesWithoutCommittingCancelledCredits() {
        val folder=folder();val doc=PaintDocument(8,6,folder)
        val second=ImageCredit("https://example.org/second.png","別の作品 — 作者\nCC BY-SA 4.0")
        try {
            for(cut in listOf(false,true)) {
                doc.newImage(8,6);insert(doc);doc.finishSelection()
                doc.paste(Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.BLUE)},true,listOf(second))
                assertEquals(listOf(credit),ImageCredit.read(doc.imageCreditsState().getJSONArray("committed")))
                assertEquals(listOf(second),ImageCredit.read(doc.imageCreditsState().getJSONArray("floating")))
                if(cut) assertTrue(doc.cutSelection()) else {assertTrue(doc.copySelection());doc.deleteSelection()}
                assertEquals(listOf(credit),doc.imageCredits)
                doc.newImage(8,6);assertTrue(doc.paste());doc.finishSelection()
                assertEquals(Color.BLUE,doc.bitmap.getPixel(0,0))
                assertEquals(listOf(second),doc.imageCredits)
            }
            // An ordinary uncredited image must not inherit the current canvas's source list.
            doc.paste(Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.GREEN)},true)
            assertTrue(doc.copySelection());doc.newImage(8,6);assertTrue(doc.paste());doc.finishSelection()
            assertEquals(Color.GREEN,doc.bitmap.getPixel(0,0));assertTrue(doc.imageCredits.isEmpty())
        } finally {doc.close();folder.deleteRecursively()}
    }
    @Test fun canvasSelectionsKeepConservativeSourceCreditsWhenCopiedOrLiftedAndCut() {
        val folder=folder();val doc=PaintDocument(8,6,folder)
        try {
            for(lift in listOf(false,true)) {
                doc.newImage(8,6);insert(doc);doc.finishSelection()
                doc.select(RectF(0f,0f,2f,2f))
                if(lift) doc.startMovingSelection()
                assertTrue(doc.cutSelection())
                assertEquals(Color.WHITE,doc.bitmap.getPixel(0,0))
                doc.newImage(8,6);assertTrue(doc.paste());doc.finishSelection()
                assertEquals(Color.RED,doc.bitmap.getPixel(0,0));assertEquals(listOf(credit),doc.imageCredits)
            }
        } finally {doc.close();folder.deleteRecursively()}
    }
    @Test fun replacementWithIndependentPixelsClearsCurrentCreditsAndPreservesBothHistoryStates() {
        val folder=folder();val doc=PaintDocument(8,6,folder)
        try {
            insert(doc);doc.finishSelection()
            doc.replace(Bitmap.createBitmap(3,4,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.BLUE)},asEdit=true,retainCredits=false)
            assertTrue(doc.imageCredits.isEmpty());assertEquals(Color.BLUE,doc.bitmap.getPixel(0,0))
            doc.undo();assertEquals(listOf(credit),doc.imageCredits);assertEquals(Color.RED,doc.bitmap.getPixel(0,0))
            doc.redo();assertTrue(doc.imageCredits.isEmpty());assertEquals(3,doc.bitmap.width);assertEquals(Color.BLUE,doc.bitmap.getPixel(0,0))
        } finally {doc.close();folder.deleteRecursively()}
    }
    @Test fun restoredFloatingClipboardDoesNotAcquireUnrelatedCanvasCredits() {
        val folder=folder();val store=AutosaveStore(folder)
        val old=PaintDocument(8,6,File(folder,"old-history"))
        val second=ImageCredit("https://example.org/second.png","第二の作品 — 作者")
        insert(old);old.finishSelection()
        old.paste(Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.BLUE)},true,listOf(second))
        store.write(old.bitmap,old.selection!!.image,JSONObject().put("version",1)
            .put("image_credits",old.imageCreditsState()).put("floating_rect",JSONArray(listOf(0,0,2,2))),old.historySnapshot())
        old.close()
        val restored=PaintDocument(1,1,File(folder,"new-history"))
        try {
            val draft=store.read(restored::readHistory) {_,_->}
            restored.replace(draft.image);restored.restoreHistory(draft.history!!)
            restored.restoreFloatingSelection(draft.floating!!,RectF(0f,0f,2f,2f))
            restored.restoreImageCredits(draft.metadata.optJSONObject("image_credits"))
            assertEquals(listOf(credit,second),restored.imageCredits)
            assertTrue(restored.copySelection());restored.newImage(8,6);restored.paste();restored.finishSelection()
            assertEquals(listOf(second),restored.imageCredits);assertEquals(Color.BLUE,restored.bitmap.getPixel(0,0))
        } finally {restored.close();folder.deleteRecursively()}
    }
    @Test fun legacyDraftKeepsConservativeCreditWhileKnownUncreditedSelectionStaysUncredited() {
        val folder=folder();val doc=PaintDocument(8,6,folder)
        try {
            for(known in listOf(false,true)) {
                doc.restoreFloatingSelection(Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888),RectF(0f,0f,2f,2f))
                val state=JSONObject().put("committed",ImageCredit.write(listOf(credit))).put("floating",JSONArray())
                if(known) state.put("selection_sources_known",true)
                doc.restoreImageCredits(state)
                assertTrue(doc.copySelection());doc.newImage(8,6);assertTrue(doc.paste());doc.finishSelection()
                assertEquals(if(known) emptyList<ImageCredit>() else listOf(credit),doc.imageCredits)
            }
        } finally {doc.close();folder.deleteRecursively()}
    }
    @Test fun draftRestoresFloatingCreditAndHistoryAfterOriginalDocumentAndCacheAreGone() {
        val folder=folder();val store=AutosaveStore(folder)
        val old=PaintDocument(8,6,File(folder,"old-history"));insert(old)
        val metadata=JSONObject().put("version",1).put("image_credits",old.imageCreditsState())
            .put("floating_rect",JSONArray(listOf(0,0,2,2)))
        store.write(old.bitmap,old.selection!!.image,metadata,old.historySnapshot())
        old.close();File(folder,"old-history").deleteRecursively()
        val restored=PaintDocument(1,1,File(folder,"new-history"))
        try {
            val draft=store.read(restored::readHistory) {_,_->}
            assertFalse(draft.historyFailed)
            restored.replace(draft.image);restored.restoreHistory(draft.history!!)
            restored.restoreFloatingSelection(draft.floating!!,RectF(0f,0f,2f,2f))
            restored.restoreImageCredits(draft.metadata.optJSONObject("image_credits"))
            assertEquals(listOf(credit),restored.imageCredits)
            restored.undo();assertTrue(restored.imageCredits.isEmpty())
            // Redo's source metadata must be persisted as well as the current blank document.
            store.write(restored.bitmap,null,JSONObject().put("version",1).put("image_credits",restored.imageCreditsState()),restored.historySnapshot())
            val third=PaintDocument(1,1,File(folder,"third-history"))
            try {
                val again=store.read(third::readHistory) {_,_->}
                third.replace(again.image);third.restoreHistory(again.history!!)
                third.restoreImageCredits(again.metadata.optJSONObject("image_credits"))
                third.redo();assertEquals(listOf(credit),third.imageCredits)
            } finally {third.close()}
        } finally {restored.close();folder.deleteRecursively()}
    }
}
