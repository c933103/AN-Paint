/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.os.Bundle
import org.catrobat.paintroid.classic.*
import org.json.JSONArray
import org.json.JSONObject
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.io.File
import java.io.IOException

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
class CreditSnapshotLifetimeTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val archive get()=File(context.filesDir,"retained-image-credits")
    private val preferences get()=context.getSharedPreferences("image-credits",Context.MODE_PRIVATE)
    private lateinit var folder: File
    private val source="https://example.org/art.png"
    private val heap=CreditSessionJson.availableHeap
    private val space=CreditSessionJson.usableSpace
    private val block=CreditSessionJson.blockSize
    @Before fun prepare() {
        archive.deleteRecursively();preferences.edit().clear().commit()
        folder=File(context.filesDir,"snapshot-lifetime-${java.util.UUID.randomUUID()}").apply {mkdirs()}
    }
    @After fun cleanup() {
        CreditSessionJson.availableHeap=heap;CreditSessionJson.usableSpace=space;CreditSessionJson.blockSize=block
        folder.deleteRecursively();archive.deleteRecursively();preferences.edit().clear().commit()
    }
    private fun session(credits: List<ImageCredit> = listOf(ImageCredit(source,"Original")))=
        CreditEditSession.create(folder,credits,CreditEditContext.ledgerOnly(credits))
    private fun CreditEditSession.accept(text: String,editSource: String=source): CreditEditSession.AdoptionReceipt {
        edit(editSource,text) {ImageCreditArchive.retainAccepted(context,it)}
        return adoptionReceipt!!
    }
    private fun snapshot(receipt: CreditEditSession.AdoptionReceipt)=File(archive,"${receipt.snapshotToken}.json")
    private fun metadata(credits: List<ImageCredit>)=JSONObject().put("version",1).put("image_credits",
        JSONObject().put("committed",ImageCredit.write(credits)).put("floating",JSONArray()).put("selection_sources_known",true))
    private fun adopted(receipt: CreditEditSession.AdoptionReceipt,credits: List<ImageCredit>,history: RasterHistory.Snapshot=RasterHistory.Snapshot())=
        ImageCreditArchive.releaseAfterAdoption(context,receipt,metadata(credits),history)

    @Test fun repeatedSaveCopyAndDoneSnapshotsStayUntilExactDurableAdoption() {
        val session=session();val first=session.accept("Same accepted text")
        val second=session.accept("Same accepted text");val third=session.accept("Same accepted text")
        assertEquals(2,third.predecessors.size)
        // Result emission, saved state and dismissing the raw field do not establish durability.
        session.result();session.saveState(Bundle());session.saveDraft(null)
        assertTrue(listOf(first,second,third).all {snapshot(it).isFile})
        assertEquals(3,ImageCreditArchive.records(context).single().origins.size)
        adopted(third,session.credits)
        assertTrue(listOf(first,second,third).none {snapshot(it).exists()})
    }

    @Test fun distinctIntermediateAcceptedVersionsRemainRecoverableWhenOnlyLatestIsDurable() {
        val session=session();val first=session.accept("First");val second=session.accept("Second");val latest=session.accept("Latest")
        adopted(latest,session.credits)
        assertTrue(snapshot(first).isFile);assertTrue(snapshot(second).isFile);assertFalse(snapshot(latest).exists())
        assertEquals(setOf("First","Second"),ImageCreditArchive.records(context).map {it.credit.text}.toSet())
    }

    @Test fun exactValuesInUndoAndRedoCountButDifferentVersionsDoNot() {
        val session=session();val first=session.accept("Undo value");val middle=session.accept("Not written")
        val redo=session.accept("Redo value");val latest=session.accept("Current value")
        val history=RasterHistory.Snapshot(
            listOf(RasterHistory.Entry(File("unused-undo"),2,2,listOf(ImageCredit(source,"Undo value")))),
            listOf(RasterHistory.Entry(File("unused-redo"),2,2,listOf(ImageCredit(source,"Redo value")))))
        adopted(latest,session.credits,history)
        assertFalse(snapshot(first).exists());assertFalse(snapshot(redo).exists());assertFalse(snapshot(latest).exists())
        assertTrue(snapshot(middle).isFile)
    }

    @Test fun staleReceiptCannotGrowToReleaseNewerSnapshotsEvenIfValuesMatch() {
        val session=session();val old=session.accept("Same")
        val captured=CreditEditSession.open(folder,session.token,restoreDraft=false).adoptionReceipt!!
        val newer=session.accept("Same")
        assertTrue(captured.predecessors.isEmpty());assertEquals(1,newer.predecessors.size)
        adopted(captured,listOf(ImageCredit(source,"Same")))
        assertFalse(snapshot(old).exists());assertTrue(snapshot(newer).isFile)
        assertFalse(session.retireAfterAdoption(captured.revision))
    }

    @Test fun acceptedLineageSurvivesRecreationAndUnacceptedRawCancellation() {
        val original=session();val first=original.accept("First");val second=original.accept("")
        original.saveDraft(GalleryCredits.EditorDraft(source,"Unaccepted replacement"))
        val restored=CreditEditSession.open(folder,original.token)
        assertEquals(original.adoptionReceipt,restored.adoptionReceipt)
        assertEquals("Unaccepted replacement",restored.draft!!.text)
        restored.saveDraft(null)
        assertTrue(snapshot(first).isFile);assertTrue(snapshot(second).isFile)
        val returned=CreditEditSession.open(folder,restored.result().getStringExtra(CreditEditSession.EXTRA_SESSION)!!,restoreDraft=false)
        assertEquals(original.adoptionReceipt,returned.adoptionReceipt)
        adopted(returned.adoptionReceipt!!,returned.credits)
        assertTrue(snapshot(first).isFile);assertFalse(snapshot(second).exists())
    }

    @Test fun unlinkedOldArchiveRecordsOtherSessionsAndLegacyPreferencesAreNeverGuessedOwned() {
        val credit=ImageCredit(source,"Identical text")
        val unlinked=ImageCreditArchive.retainAccepted(context,listOf(credit))
        val unrelated=session().accept(credit.text)
        preferences.edit().putStringSet("sources",setOf(source)).putString("text:$source",credit.text).commit()
        val before=preferences.all
        val owned=session();val old=owned.accept(credit.text);val latest=owned.accept(credit.text)
        adopted(latest,owned.credits)
        assertFalse(snapshot(old).exists());assertFalse(snapshot(latest).exists())
        assertTrue(File(archive,"$unlinked.json").isFile);assertTrue(snapshot(unrelated).isFile)
        assertEquals(before,preferences.all)
        assertEquals(3,ImageCreditArchive.records(context).single().origins.size)
    }

    @Test fun missingOrDamagedPredecessorDoesNotHideOtherExplicitlyTrackedSnapshots() {
        val session=session();val missing=session.accept("Same");val damaged=session.accept("Same")
        val complete=session.accept("Same");val latest=session.accept("Same")
        ImageCreditArchive.releaseAccepted(context,missing.snapshotToken)
        snapshot(damaged).writeText("damaged original bytes")
        val before=snapshot(damaged).readBytes()
        adopted(latest,session.credits)
        assertFalse(snapshot(complete).exists());assertFalse(snapshot(latest).exists())
        assertArrayEquals(before,snapshot(damaged).readBytes())
    }

    @Test fun failedReplacementDoesNotPublishLineageOrDeleteTheUnlinkedNewSnapshot() {
        val session=session();val first=session.accept("First")
        val before=File(folder,session.token).readBytes();var interrupted: String?=null
        try {
            session.edit(source,"Interrupted replacement") {
                ImageCreditArchive.retainAccepted(context,it).also {token ->
                    interrupted=token;CreditSessionJson.usableSpace={0}
                }
            }
            fail("Session replacement must fail")
        } catch(_: IOException) { }
        CreditSessionJson.usableSpace=space
        assertArrayEquals(before,File(folder,session.token).readBytes())
        assertEquals(first,session.adoptionReceipt)
        assertEquals(first,CreditEditSession.open(folder,session.token).adoptionReceipt)
        adopted(first,session.credits)
        assertFalse(snapshot(first).exists())
        assertTrue(File(archive,"$interrupted.json").isFile)
        assertEquals("Interrupted replacement",ImageCreditArchive.records(context).single().credit.text)
    }

    @Test fun fullSnapshotMustMatchIncludingAllSourcesAndIntentionalEmptyText() {
        val other="https://example.org/other.png"
        val session=session(listOf(ImageCredit(source,"Original"),ImageCredit(other,"Other original")))
        val previous=session.accept("");val latest=session.accept("Other revised",other)
        adopted(latest,session.credits)
        assertTrue(snapshot(previous).isFile);assertFalse(snapshot(latest).exists())
        assertTrue(ImageCreditArchive.records(context).any {it.credit==ImageCredit(source,"")})
        assertTrue(ImageCreditArchive.records(context).any {it.credit==ImageCredit(other,"Other original")})
    }

    @Test fun identicalLargeUnicodeSnapshotsRemainExactAndRetireWithoutInlineTransport() {
        val session=session();val text="\uD86D\uDC40漢\"\\\n".repeat(6000)
        val previous=session.accept(text);val latest=session.accept(text)
        assertFalse(session.result().hasExtra("document_image_credits"))
        val restored=CreditEditSession.open(folder,session.token,restoreDraft=false)
        assertEquals(text,restored.credits.single().text)
        assertEquals(latest,restored.adoptionReceipt)
        adopted(latest,restored.credits)
        assertFalse(snapshot(previous).exists());assertFalse(snapshot(latest).exists())
    }

    @Test fun refusedSnapshotReadKeepsAllOwnedFilesAndCanBeRetriedWithResources() {
        val session=session();val first=session.accept("Same");val latest=session.accept("Same")
        val before=listOf(snapshot(first).readBytes(),snapshot(latest).readBytes())
        CreditSessionJson.availableHeap={0}
        adopted(latest,session.credits)
        assertArrayEquals(before[0],snapshot(first).readBytes());assertArrayEquals(before[1],snapshot(latest).readBytes())
        CreditSessionJson.availableHeap=heap
        adopted(latest,session.credits)
        assertFalse(snapshot(first).exists());assertFalse(snapshot(latest).exists())
    }

    @Test fun oldSessionWithoutLineageOnlyClaimsItsCurrentExplicitSnapshot() {
        val session=session();val unlinked=session.accept("Same");val current=session.accept("Same")
        val file=File(folder,session.token)
        val old=JSONObject(file.readText()).apply {remove("previous_accepted_snapshots")};file.writeText(old.toString())
        val restored=CreditEditSession.open(folder,session.token)
        assertTrue(restored.adoptionReceipt!!.predecessors.isEmpty())
        adopted(restored.adoptionReceipt!!,restored.credits)
        assertTrue(snapshot(unlinked).isFile);assertFalse(snapshot(current).exists())
    }
    @Test fun duplicateSourceSnapshotsRequireEveryDistinctAndEmptyRecordToBeDurable() {
        val repeated=listOf(ImageCredit(source,"First"),ImageCredit(source,""),ImageCredit(source,"Other"))
        val token=ImageCreditArchive.retainAccepted(context,repeated)
        val receipt=CreditEditSession.AdoptionReceipt(1,token)
        val stored=File(archive,"$token.json");val before=stored.readBytes()
        adopted(receipt,listOf(repeated.first()))
        assertArrayEquals(before,stored.readBytes())
        val history=RasterHistory.Snapshot(listOf(RasterHistory.Entry(File("unused"),2,2,repeated.drop(1))))
        adopted(receipt,listOf(repeated.first()),history)
        assertFalse(stored.exists())
    }

    @Test fun malformedOrUnknownLineageFailsClosedWithoutChangingAnySnapshot() {
        val session=session();val first=session.accept("First");val latest=session.accept("Latest")
        val file=File(folder,session.token);val original=JSONObject(file.readText())
        val badValues=listOf<Any>("not an array",JSONArray().put(JSONObject().put("revision",1).put("snapshot",first.snapshotToken).put("unknown",true)),
            JSONArray().put(JSONObject().put("revision",latest.revision).put("snapshot",first.snapshotToken)),
            JSONArray().put(JSONObject().put("revision","1").put("snapshot",first.snapshotToken)))
        for(value in badValues) {
            file.writeText(JSONObject(original.toString()).put("previous_accepted_snapshots",value).toString())
            try {CreditEditSession.open(folder,session.token,restoreDraft=false);fail("Unrecognized ownership metadata must not be accepted")}
            catch(_: IllegalArgumentException) { } catch(_: org.json.JSONException) { }
            assertTrue(snapshot(first).isFile);assertTrue(snapshot(latest).isFile)
        }
    }

    @Test fun malformedSnapshotFieldsArePreservedRatherThanCoercedIntoMatchingText() {
        val session=session();val previous=session.accept("null");val latest=session.accept("null")
        val stored=snapshot(previous)
        stored.writeText(JSONObject().put("version",1).put("credits",JSONArray().put(
            JSONObject().put("source",source).put("text",JSONObject.NULL))).toString())
        val before=stored.readBytes()
        adopted(latest,session.credits)
        assertArrayEquals(before,stored.readBytes());assertFalse(snapshot(latest).exists())
    }

    @Test fun streamingAdoptionKeepsLineageAndRawDraftWithoutRestoringTheLargeField() {
        val session=session();val previous=session.accept("First");val latest=session.accept("Latest")
        val raw="\uD86D\uDC40".repeat(200000)
        session.saveDraft(GalleryCredits.EditorDraft(source,raw))
        CreditSessionJson.availableHeap={64L*1024}
        val withoutDraft=CreditEditSession.open(folder,session.token,restoreDraft=false)
        assertEquals(latest,withoutDraft.adoptionReceipt)
        adopted(latest,withoutDraft.credits)
        assertTrue(withoutDraft.retireAfterAdoption(latest.revision))
        CreditSessionJson.availableHeap=heap
        val restored=CreditEditSession.open(folder,session.token)
        assertEquals(raw,restored.draft!!.text);assertEquals(latest,restored.adoptionReceipt)
        assertTrue(snapshot(previous).isFile);assertFalse(snapshot(latest).exists())
    }

}
