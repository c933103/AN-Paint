/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.os.Bundle
import android.os.Parcel
import org.catrobat.paintroid.classic.*
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.io.File

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
class CreditEditSessionTest {
    private fun folder()=File(RuntimeEnvironment.getApplication().filesDir,"credit-session-${java.util.UUID.randomUUID()}").apply {mkdirs()}
    private fun rejected(action: ()->Unit) {
        try {action();fail("The operation must be rejected as a whole")}
        catch(_: IllegalArgumentException) { }
    }
    private fun CreditEditSession.edit(source: String,text: String)=edit(source,text) {"immutable-snapshot-${java.util.UUID.randomUUID()}"}
    private fun state(credits: List<ImageCredit>)=JSONObject().put("committed",ImageCredit.write(credits))
        .put("floating",JSONArray()).put("selection_sources_known",true)

    @Test fun previouslyReadableTwoHundredKiBCreditRemainsAcceptedAndUsesTokenTransport() {
        val folder=folder();val credit=ImageCredit("https://example.org/art.png","𠀀".repeat(51000))
        try {
            val session=CreditEditSession.create(folder,listOf(credit),CreditEditContext.ledgerOnly(listOf(credit)))
            session.edit(credit.source,credit.text+"漢")
            val result=session.result()
            assertEquals(session.token,result.getStringExtra(CreditEditSession.EXTRA_SESSION))
            assertFalse(result.hasExtra("document_image_credits"))
            val reopened=CreditEditSession.open(folder,session.token)
            assertTrue(reopened.accepted);assertEquals(credit.text+"漢",reopened.credits.single().text)
        } finally {folder.deleteRecursively()}
    }

    @Test fun actualNonCreditMetadataAndAggregateSourcesDetermineCapacity() {
        val folder=folder()
        val first=ImageCredit("https://example.org/a","First");val second=ImageCredit("https://example.org/b","Second")
        val metadata=JSONObject().put("version",1).put("other_metadata","漢".repeat(60000))
            .put("image_credits",state(listOf(first,second)))
        try {
            val context=CreditEditContext(metadata,HistoryArchive.manifest(RasterHistory.Snapshot()))
            val session=CreditEditSession.create(folder,listOf(first,second),context)
            val previous=File(folder,session.token).readBytes()
            // This single field is below256KiB, but its actual document envelope is too large.
            rejected {session.edit(first.source,"𠀀".repeat(25000))}
            assertArrayEquals(previous,File(folder,session.token).readBytes())
            assertEquals(listOf(first,second),session.credits);assertFalse(session.accepted)
            session.edit(first.source,"𠀀".repeat(10000))
            rejected {session.edit(second.source,"漢".repeat(20000))}
            assertEquals(second,session.credits.last())
        } finally {folder.deleteRecursively()}
    }

    @Test fun projectedHistoryNormalizesCatalogAndIndicesExactlyLikeTheWriter() {
        val credits=(0..12).map {ImageCredit("https://example.org/${it/2}","variant $it")}
        val entries=credits.mapIndexed {i,c ->RasterHistory.Entry(File("unused-$i"),2,2,listOf(c))}
        val snapshot=RasterHistory.Snapshot(entries.take(7),entries.drop(7))
        val edits=(0..6).map {ImageCredit("https://example.org/$it","same replacement for source $it")}
        val replacements=edits.associateBy {it.source}
        fun amend(stack: List<RasterHistory.Entry>)=stack.map {it.copy(imageCredits=it.imageCredits.map {c -> replacements[c.source] ?: c})}
        val context=CreditEditContext(JSONObject().put("version",1).put("image_credits",state(credits.distinctBy {it.source})),HistoryArchive.manifest(snapshot))
        val projected=context.edited(edits).json().getJSONObject("history")
        val actual=HistoryArchive.manifest(RasterHistory.Snapshot(amend(snapshot.undo),amend(snapshot.redo)))
        assertEquals(actual.toString(),projected.toString())
    }

    @Test fun rejectedRawDraftSurvivesOffloadedRecreationWithoutBeingAcceptedOrParceled() {
        val folder=folder();val credit=ImageCredit("https://example.org/a","Previously accepted")
        val raw="𠀀漢\n\"\\".repeat(100000)
        try {
            val session=CreditEditSession.create(folder,listOf(credit),CreditEditContext.ledgerOnly(listOf(credit)))
            session.saveDraft(GalleryCredits.EditorDraft(credit.source,raw))
            rejected {session.edit(credit.source,raw)}
            val state=Bundle();session.saveState(state)
            assertFalse(state.containsKey("image_credit_editor_draft"))
            val parcel=Parcel.obtain()
            try {parcel.writeBundle(state);assertTrue(parcel.dataSize()<4096)} finally {parcel.recycle()}
            val reopened=CreditEditSession.open(folder,state.getString(CreditEditSession.EXTRA_SESSION)!!)
            assertEquals(raw,reopened.draft!!.text);assertEquals(listOf(credit),reopened.credits)
            assertFalse(reopened.accepted)
        } finally {folder.deleteRecursively()}
    }

    @Test fun oldAutosaveReceiptCannotDeleteANewerAcceptedRevision() {
        val folder=folder();val credit=ImageCredit("https://example.org/a","Original")
        try {
            val session=CreditEditSession.create(folder,listOf(credit),CreditEditContext.ledgerOnly(listOf(credit)))
            session.edit(credit.source,"First");val oldRevision=session.revision
            session.edit(credit.source,"Second");val latest=session.revision
            assertFalse(session.retireAfterAdoption(oldRevision))
            assertEquals("Second",CreditEditSession.open(folder,session.token).credits.single().text)
            session.saveDraft(null)
            assertTrue(session.retireAfterAdoption(latest))
            assertFalse(File(folder,session.token).exists())
        } finally {folder.deleteRecursively()}
    }

    @Test fun adoptionKeepsUnfinishedTextUntilItsExplicitDiscard() {
        val folder=folder();val credit=ImageCredit("https://example.org/a","Original")
        try {
            val session=CreditEditSession.create(folder,listOf(credit),CreditEditContext.ledgerOnly(listOf(credit)))
            session.edit(credit.source,"Accepted")
            val raw="𠀀".repeat(100000)
            session.saveDraft(GalleryCredits.EditorDraft(credit.source,raw))
            assertTrue(session.retireAfterAdoption(session.revision))
            assertEquals(raw,CreditEditSession.open(folder,session.token).draft!!.text)
            // The original UI instance observes the worker's persisted adoption receipt.
            session.saveDraft(null)
            assertFalse(File(folder,session.token).exists())
        } finally {folder.deleteRecursively()}
    }

    @Test fun aNewDrawingOrLaterCreditVersionDoesNotCountAsDurableAdoption() {
        val folder=folder();val credit=ImageCredit("https://example.org/a","Original")
        try {
            val session=CreditEditSession.create(folder,listOf(credit),CreditEditContext.ledgerOnly(listOf(credit)))
            session.edit(credit.source,"Accepted")
            val accepted=credit.copy(text="Accepted")
            fun metadata(credits: List<ImageCredit>)=JSONObject().put("version",1).put("image_credits",state(credits))
            assertTrue(session.representedBy(metadata(listOf(accepted)),RasterHistory.Snapshot()))
            assertFalse(session.representedBy(metadata(emptyList()),RasterHistory.Snapshot()))
            assertFalse(session.representedBy(metadata(listOf(credit.copy(text="Later version"))),RasterHistory.Snapshot()))
            val historical=RasterHistory.Entry(File("unused"),2,2,listOf(accepted))
            assertTrue(session.representedBy(metadata(emptyList()),RasterHistory.Snapshot(listOf(historical))))
        } finally {folder.deleteRecursively()}
    }

    @Test fun privateTokensRejectPaths() {
        val folder=folder()
        try {for(token in listOf("../other.json","/tmp/credit-edit.json","credit-edit-../../other.json"))
            rejected {CreditEditSession.open(folder,token)}}
        finally {folder.deleteRecursively()}
    }
}
