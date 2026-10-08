/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.os.Bundle
import android.util.AtomicFile
import org.catrobat.paintroid.classic.*
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.io.File
import java.io.IOException

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
class CreditSessionResourcesTest {
    private fun folder()=File(RuntimeEnvironment.getApplication().filesDir,"credit-resources-${java.util.UUID.randomUUID()}").apply {mkdirs()}
    private fun resourceFailure(action: ()->Unit) {
        try {action();fail("Resource exhaustion must not report success")}
        catch(_: IOException) { }
    }
    private fun controlled(action: (File)->Unit) {
        val heap=CreditSessionJson.availableHeap;val space=CreditSessionJson.usableSpace;val block=CreditSessionJson.blockSize
        val directory=folder()
        try {
            CreditSessionJson.availableHeap={128L*1024*1024}
            CreditSessionJson.usableSpace={1024L*1024*1024}
            CreditSessionJson.blockSize={4096}
            action(directory)
        } finally {
            CreditSessionJson.availableHeap=heap;CreditSessionJson.usableSpace=space;CreditSessionJson.blockSize=block
            directory.deleteRecursively()
        }
    }
    private fun session(directory: File): CreditEditSession {
        val credit=ImageCredit("https://example.org/image","Original")
        return CreditEditSession.create(directory,listOf(credit),CreditEditContext.ledgerOnly(listOf(credit)))
    }
    @Test fun streamedJsonKeepsEscapesSupplementaryAndLoneSurrogatesExactly()=controlled {directory->
        val session=session(directory)
        val text="a".repeat(4095)+"𠀀漢\n\"\\\u0000\b\t\r\u000c"+"\uD800x\uDC00"+"z".repeat(4096)
        session.saveDraft(GalleryCredits.EditorDraft(session.credits.single().source,text))
        val restored=CreditEditSession.open(directory,session.token)
        assertEquals(text,restored.draft!!.text)
        val json=JSONObject(File(directory,session.token).readText(Charsets.UTF_8))
        assertEquals(1,json.getInt("version"));assertEquals(text,json.getJSONObject("draft").getString("text"))
        assertEquals(listOf(ImageCredit(session.credits.single().source,"Original")),restored.credits)
        assertFalse(restored.accepted)
    }
    @Test fun readOldWholeJsonSessionsWithoutChangingTheirBytes()=controlled {directory->
        val session=session(directory);val file=File(directory,session.token)
        val raw="𠀀漢\n\"\\".repeat(40000)
        val old=JSONObject(file.readText()).put("draft",JSONObject().put("source",session.credits.single().source).put("text",raw))
        file.writeText(old.toString(),Charsets.UTF_8)
        val original=file.readBytes()
        assertEquals(raw,CreditEditSession.open(directory,session.token).draft!!.text)
        assertArrayEquals(original,file.readBytes())
    }
    @Test fun heapRefusalRetainsTheCompleteOldFileAndCanRetryAfterResourcesReturn()=controlled {directory->
        val session=session(directory);val raw="漢𠀀".repeat(60000)
        session.saveDraft(GalleryCredits.EditorDraft(session.credits.single().source,raw))
        val file=File(directory,session.token);val previous=file.readBytes()
        CreditSessionJson.availableHeap={64L*1024}
        resourceFailure {CreditEditSession.open(directory,session.token)}
        assertArrayEquals(previous,file.readBytes())
        val receipt=CreditSessionJson.receipt(AtomicFile(file))
        assertTrue(receipt.getBoolean("has_draft"));assertFalse(receipt.getBoolean("accepted"))
        val metadataOnly=CreditEditSession.open(directory,session.token,restoreDraft=false)
        assertTrue(metadataOnly.hasDraft);assertNull(metadataOnly.draft)
        CreditSessionJson.availableHeap={128L*1024*1024}
        assertEquals(raw,CreditEditSession.open(directory,session.token).draft!!.text)
    }
    @Test fun insufficientAtomicWorkspaceDoesNotReplaceAcceptedOrRawData()=controlled {directory->
        val session=session(directory)
        session.edit(session.credits.single().source,"Accepted") {"immutable-accepted-snapshot"}
        session.saveDraft(GalleryCredits.EditorDraft(session.credits.single().source,"Unconfirmed"))
        val file=File(directory,session.token);val previous=file.readBytes()
        CreditSessionJson.usableSpace={8192}
        resourceFailure {session.saveDraft(GalleryCredits.EditorDraft(session.credits.single().source,"New raw field"))}
        assertArrayEquals(previous,file.readBytes())
        assertEquals("Unconfirmed",session.draft!!.text);assertEquals("Accepted",session.credits.single().text)
        assertTrue(session.accepted);assertEquals("immutable-accepted-snapshot",session.acceptedSnapshot)
    }
    @Test fun lowFreeSpaceStillPermitsASmallMeasuredReplacement()=controlled {directory->
        val session=session(directory)
        // One allocation block for this small payload, plus the two-block transaction margin.
        // No percentage of the whole volume or hundreds-of-megabytes minimum is reserved.
        CreditSessionJson.usableSpace={3*4096L}
        session.saveDraft(GalleryCredits.EditorDraft(session.credits.single().source,"Small update"))
        assertEquals("Small update",CreditEditSession.open(directory,session.token).draft!!.text)
    }
    @Test fun racingDiskLossRollsBackAnAlreadyStartedAtomicWrite()=controlled {directory->
        val session=session(directory);val file=File(directory,session.token);val previous=file.readBytes()
        var reads=0
        CreditSessionJson.usableSpace={reads++;if(reads<=2)1024*1024L else 0L}
        resourceFailure {session.saveDraft(GalleryCredits.EditorDraft(session.credits.single().source,"x".repeat(100000)))}
        assertTrue("Failure must happen after preflight",reads>2)
        assertArrayEquals(previous,AtomicFile(file).openRead().use {it.readBytes()})
        assertNull(session.draft);assertFalse(session.accepted)
    }
    @Test fun snapshotChecksBeforeMakingAnEditableCopy()=controlled {
        CreditSessionJson.availableHeap={1024}
        val value=object: CharSequence {
            override val length=1000000
            override fun get(index: Int)='x'
            override fun subSequence(startIndex: Int,endIndex: Int): CharSequence=throw AssertionError("No slice may be made")
            override fun toString(): String=throw AssertionError("No large copy may be made")
        }
        resourceFailure {CreditSessionJson.snapshot("source",value)}
    }
    @Test fun adoptedRevisionCanAdvanceWithoutMaterializingOrDeletingLargeRawText()=controlled {directory->
        val session=session(directory);val source=session.credits.single().source
        session.edit(source,"Accepted") {"immutable-snapshot"}
        val raw="𠀀\n\"\\".repeat(60000)
        session.saveDraft(GalleryCredits.EditorDraft(source,raw))
        CreditSessionJson.availableHeap={64L*1024}
        val inspected=CreditEditSession.open(directory,session.token,restoreDraft=false)
        assertTrue(inspected.hasDraft)
        assertTrue(inspected.retireAfterAdoption(session.revision))
        assertEquals(session.revision,CreditSessionJson.receipt(AtomicFile(File(directory,session.token))).getLong("adopted_revision"))
        CreditSessionJson.availableHeap={128L*1024*1024}
        assertEquals(raw,CreditEditSession.open(directory,session.token).draft!!.text)
        // The older UI session observes the worker receipt and explicit dismissal may retire it.
        session.saveDraft(null);assertFalse(File(directory,session.token).exists())
    }
    @Test fun adoptionCannotEraseANewerAcceptedRevisionOrClearRawOnDiskFailure()=controlled {directory->
        val session=session(directory);val source=session.credits.single().source
        session.edit(source,"First") {"snapshot-one"};val old=session.revision
        session.edit(source,"Second") {"snapshot-two"}
        session.saveDraft(GalleryCredits.EditorDraft(source,"Keep the unconfirmed field"))
        val file=File(directory,session.token);val previous=file.readBytes()
        assertFalse(session.retireAfterAdoption(old));assertArrayEquals(previous,file.readBytes())
        CreditSessionJson.usableSpace={0}
        resourceFailure {session.retireAfterAdoption(session.revision)}
        assertArrayEquals(previous,file.readBytes())
    }
    @Test fun rawInlineProbeAndBundleNeverEncodeTheWholeRejectedField()=controlled {directory->
        val session=session(directory);val raw="x".repeat(2*1024*1024)
        session.saveDraft(GalleryCredits.EditorDraft(session.credits.single().source,raw))
        CreditSessionJson.availableHeap={64L*1024}
        // Reading this raw value would be refused at this budget. Saving token state and the
        // inline probe must nevertheless succeed without copying/encoding the whole value.
        val state=Bundle();session.saveState(state)
        assertEquals(session.token,state.getString(CreditEditSession.EXTRA_SESSION))
        assertFalse(state.containsKey("image_credit_editor_draft"))
        assertFalse(CreditEditSession.inline(raw))
        assertTrue(CreditSessionJson.fitsInline("𠀀",4));assertFalse(CreditSessionJson.fitsInline("𠀀",3))
        assertTrue(CreditSessionJson.fitsInline("漢",3));assertFalse(CreditSessionJson.fitsInline("漢",2))
    }
    @Test fun malformedUtf8AndNestedInputFailWithoutTouchingTheSession()=controlled {directory->
        val session=session(directory);val file=File(directory,session.token)
        file.writeBytes(byteArrayOf('{'.code.toByte(),'"'.code.toByte(),0xc3.toByte(),0x28,'"'.code.toByte(),':'.code.toByte(),'0'.code.toByte(),'}'.code.toByte()))
        val invalid=file.readBytes();resourceFailure {CreditEditSession.open(directory,session.token)}
        assertArrayEquals(invalid,file.readBytes())
        file.writeText("{\"version\":1,\"draft\":"+"[".repeat(34)+"0"+"]".repeat(34)+"}")
        val deep=file.readBytes();resourceFailure {CreditSessionJson.receipt(AtomicFile(file))}
        assertArrayEquals(deep,file.readBytes())
    }
    @Test fun oldReadableTwoHundredKiBCreditStillFitsAcceptedDrawingFormat()=controlled {directory->
        val credit=ImageCredit("https://example.org/large","𠀀".repeat(51000))
        val session=CreditEditSession.create(directory,listOf(credit),CreditEditContext.ledgerOnly(listOf(credit)))
        session.edit(credit.source,credit.text+"漢") {"large-snapshot"}
        assertEquals(credit.text+"漢",CreditEditSession.open(directory,session.token).credits.single().text)
        assertFalse(session.result().hasExtra("document_image_credits"))
    }
    @Test fun overflowingOrImpossibleFilesystemMeasurementsRefuseWithoutMutation()=controlled {directory->
        val session=session(directory);val file=File(directory,session.token);val original=file.readBytes()
        CreditSessionJson.blockSize={Long.MAX_VALUE}
        resourceFailure {session.saveDraft(GalleryCredits.EditorDraft(session.credits.single().source,"New"))}
        assertArrayEquals(original,file.readBytes())
        for(value in listOf(0L,-1L)) {
            CreditSessionJson.blockSize={value}
            resourceFailure {session.saveDraft(null)};assertArrayEquals(original,file.readBytes())
        }
        CreditSessionJson.blockSize={4096};CreditSessionJson.usableSpace={Long.MIN_VALUE}
        resourceFailure {session.saveDraft(null)};assertArrayEquals(original,file.readBytes())
    }
    @Test fun oldLiteralSupplementaryAdoptionUsesExactUtf8Space()=controlled {directory->
        val session=session(directory);val source=session.credits.single().source
        session.edit(source,"Accepted") {"snapshot"}
        val file=File(directory,session.token)
        val raw="𠀀".repeat(4096)
        val old=JSONObject(file.readText()).put("draft",JSONObject().put("source",source).put("text",raw))
        file.writeText(old.toString(),Charsets.UTF_8)
        assertTrue("Fixture must have literal supplementary UTF-8",file.readText().contains("𠀀"))
        val expected=file.length()-1 // adopted_revision changes from -1 to 1; other tokens are copied.
        val rounded=((expected+4095)/4096)*4096
        CreditSessionJson.usableSpace={rounded+8192}
        CreditSessionJson.availableHeap={64L*1024}
        assertTrue(session.retireAfterAdoption(session.revision))
        assertEquals(expected,file.length())
        CreditSessionJson.availableHeap={128L*1024*1024}
        assertEquals(raw,CreditEditSession.open(directory,session.token).draft!!.text)
    }
    @Test fun encoderChunksMayShareAnAlreadyAllocatedLargeFilesystemBlock()=controlled {directory->
        val session=session(directory);var calls=0
        CreditSessionJson.blockSize={65536}
        CreditSessionJson.usableSpace={calls++;if(calls<=2)3*65536L else 2*65536L}
        session.saveDraft(GalleryCredits.EditorDraft(session.credits.single().source,"x".repeat(20000)))
        assertTrue(calls>2)
        assertEquals(20000,CreditEditSession.open(directory,session.token).draft!!.text.length)
    }
    @Test fun aShortFinalChunkCannotSpendTheRollbackBlockMargin()=controlled {directory->
        val session=session(directory);val file=File(directory,session.token);val before=file.readBytes()
        var calls=0
        CreditSessionJson.usableSpace={calls++;when(calls) {1,2->7*4096L;3->5*4096L;else->2*4096L+1000}}
        resourceFailure {session.saveDraft(GalleryCredits.EditorDraft(session.credits.single().source,"x".repeat(16500)))}
        assertTrue(calls>=4)
        assertArrayEquals(before,AtomicFile(file).openRead().use {it.readBytes()})
    }

    @Test fun optionalInlineProbeAccountsForAndroidEscapedSlashes()=controlled {
        val value=JSONObject().put("source","s").put("text","/".repeat(9000))
        assertTrue(value.toString().toByteArray(Charsets.UTF_8).size>CreditEditSession.INLINE_BYTES)
        assertFalse(CreditSessionJson.fitsInline(value,CreditEditSession.INLINE_BYTES))
        val small=JSONObject().put("source","s").put("text","/".repeat(100))
        val exact=small.toString().toByteArray(Charsets.UTF_8).size
        assertTrue(CreditSessionJson.fitsInline(small,exact))
        assertFalse(CreditSessionJson.fitsInline(small,exact-1))
    }

}
