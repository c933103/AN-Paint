/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
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

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CreditEditAtomicityTest {
    private fun folder()=File(RuntimeEnvironment.getApplication().filesDir,"credit-atomic-${java.util.UUID.randomUUID()}").apply {mkdirs()}
    private fun image(colour: Int)=Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888).apply {eraseColor(colour)}
    private fun rejected(action: ()->Unit) {
        try {action();fail("The operation must be rejected as a whole")}
        catch(_: IllegalArgumentException) { }
    }
    @Test fun rejectedInsertionAndMultiSourceResultPreservePixelsFloatingCreditsClipboardAndHistory() {
        val folder=folder();val doc=PaintDocument(4,4,folder)
        val first=ImageCredit("https://example.org/a","𠀀".repeat(35000))
        val second=ImageCredit("https://example.org/b","漢".repeat(32000))
        val third=ImageCredit("https://example.org/c","z".repeat(30000))
        val next=image(Color.GREEN)
        try {
            doc.paste(image(Color.RED),true,listOf(first));doc.finishSelection()
            doc.paste(image(Color.BLUE),true,listOf(second));assertTrue(doc.copySelection())
            val selection=doc.selection;val before=doc.imageCreditsState().toString()
            rejected {doc.paste(next,true,listOf(third))}
            assertSame(selection,doc.selection);assertEquals(before,doc.imageCreditsState().toString())
            assertEquals(Color.RED,doc.bitmap.getPixel(0,0));assertFalse(next.isRecycled)
            rejected {doc.editImageCredits(listOf(first.copy(text="Otherwise valid"),second.copy(text="𠀀".repeat(70000))))}
            assertEquals(before,doc.imageCreditsState().toString())
            doc.finishSelection();doc.undo();assertEquals(listOf(first),doc.imageCredits)
            doc.redo();assertEquals(listOf(first,second),doc.imageCredits)
            doc.newImage(4,4);assertTrue(doc.paste());assertEquals(listOf(second),doc.imageCredits)
        } finally {next.recycle();doc.close();folder.deleteRecursively()}
    }
    @Test fun largePreviouslyValidCreditSurvivesWriterReaderAndRestartWithoutTruncation() {
        val folder=folder();val store=AutosaveStore(folder)
        val original=PaintDocument(4,4,File(folder,"old"));val restored=PaintDocument(1,1,File(folder,"new"))
        val credit=ImageCredit("https://example.org/large.png","𠀀".repeat(50000))
        try {
            original.paste(image(Color.RED),true,listOf(credit));original.finishSelection()
            store.write(original.bitmap,null,JSONObject().put("version",1).put("image_credits",original.imageCreditsState()),original.historySnapshot())
            original.close()
            val draft=store.read(restored::readHistory) {_,_->}
            assertFalse(draft.historyFailed)
            restored.replace(draft.image);restored.restoreHistory(draft.history!!)
            restored.restoreImageCredits(draft.metadata.getJSONObject("image_credits"))
            assertEquals(listOf(credit),restored.imageCredits);assertEquals(Color.RED,restored.bitmap.getPixel(0,0))
            restored.undo();assertTrue(restored.imageCredits.isEmpty())
            restored.redo();assertEquals(listOf(credit),restored.imageCredits)
        } finally {original.close();restored.close();folder.deleteRecursively()}
    }
}
