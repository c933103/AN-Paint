/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import org.catrobat.paintroid.classic.ImageCredit
import org.catrobat.paintroid.classic.ImageCreditArchive
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
class ImageCreditArchiveTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val preferences get()=context.getSharedPreferences("image-credits",Context.MODE_PRIVATE)
    private val directory get()=File(context.filesDir,"retained-image-credits")
    private val source="https://example.org/art.png"
    @Before fun prepare() {directory.deleteRecursively();preferences.edit().clear().commit()}
    @After fun cleanup() {directory.deleteRecursively();preferences.edit().clear().commit()}

    @Test fun completeAcceptedSnapshotsKeepEmptyOversizedAndRepeatedSourceRecordsExact() {
        val credits=listOf(ImageCredit(source,""),ImageCredit(source,"Another accepted version"),
            ImageCredit("https://example.org/large.png","\uD86D\uDC40\"\\\n".repeat(50_000)))
        val token=ImageCreditArchive.retainAccepted(context,credits)
        assertTrue(token.matches(Regex("[0-9a-f]{64}")))
        val stored=File(directory,"$token.json")
        assertTrue(stored.isFile)
        val before=stored.readBytes()
        val records=ImageCreditArchive.records(context)
        assertEquals(credits,records.map {it.credit})
        assertEquals(3,records.map {it.token}.distinct().size)
        records.forEach {assertEquals(it.credit,ImageCreditArchive.find(context,it.token))}
        assertArrayEquals(before,stored.readBytes())
    }

    @Test fun releasingAnOlderDurablyAdoptedSnapshotNeverDeletesANewerAcceptanceOrLegacyPreferences() {
        preferences.edit().putStringSet("sources",setOf(source)).putString("text:$source","Original legacy edit").commit()
        val before=preferences.all
        val older=ImageCreditArchive.retainAccepted(context,listOf(ImageCredit(source,"First acceptance")))
        val newer=ImageCreditArchive.retainAccepted(context,listOf(ImageCredit(source,"Newer acceptance")))
        assertNotEquals(older,newer)
        ImageCreditArchive.releaseAccepted(context,older)
        assertFalse(File(directory,"$older.json").exists())
        assertTrue(File(directory,"$newer.json").isFile)
        assertEquals(listOf("Original legacy edit","Newer acceptance"),ImageCreditArchive.records(context).map {it.credit.text})
        ImageCreditArchive.releaseAccepted(context,older) // An old completion can safely arrive again.
        assertTrue(File(directory,"$newer.json").isFile)
        assertEquals(before,preferences.all)
    }

    @Test fun identicalDisplayRecordsRetainEveryOriginUntilEachExactSnapshotIsReleased() {
        val credit=ImageCredit(source,"")
        preferences.edit().putStringSet("sources",setOf(source)).putString("text:$source","").commit()
        val older=ImageCreditArchive.retainAccepted(context,listOf(credit,credit))
        val newer=ImageCreditArchive.retainAccepted(context,listOf(credit))
        val initial=ImageCreditArchive.records(context).single()
        assertEquals(credit,initial.credit);assertEquals(4,initial.origins.size)
        ImageCreditArchive.releaseAccepted(context,older)
        val afterOlder=ImageCreditArchive.records(context).single()
        assertEquals(initial.token,afterOlder.token);assertEquals(2,afterOlder.origins.size)
        ImageCreditArchive.releaseAccepted(context,older)
        assertEquals(2,ImageCreditArchive.records(context).single().origins.size)
        ImageCreditArchive.releaseAccepted(context,newer)
        val legacyOnly=ImageCreditArchive.records(context).single()
        assertEquals(initial.token,legacyOnly.token);assertEquals(1,legacyOnly.origins.size)
        assertEquals("",preferences.getString("text:$source",null))
    }

    @Test fun damagedSnapshotIsKeptAndReportedWithoutHidingOtherReadableRecords() {
        val good=ImageCreditArchive.retainAccepted(context,listOf(ImageCredit(source,"Readable")))
        val damaged=File(directory,"${"0".repeat(64)}.json").apply {writeText("incomplete saved data")}
        val before=damaged.readBytes()
        val contents=ImageCreditArchive.contents(context)
        assertEquals(1,contents.unreadableSnapshots)
        assertEquals(listOf(ImageCredit(source,"Readable")),contents.records.map {it.credit})
        assertArrayEquals(before,damaged.readBytes())
        ImageCreditArchive.releaseAccepted(context,good)
        assertTrue(ImageCreditArchive.hasRecords(context))
        assertEquals(1,ImageCreditArchive.contents(context).unreadableSnapshots)
    }

    @Test fun invalidTokensCannotReadOrReleaseAnotherFileAndFailedRetentionDoesNotDestroyOldData() {
        val token=ImageCreditArchive.retainAccepted(context,listOf(ImageCredit(source,"Retained")))
        for(invalid in listOf("../$token","$token.json","",token+"0")) {
            ImageCreditArchive.releaseAccepted(context,invalid)
            assertNull(ImageCreditArchive.find(context,invalid))
        }
        assertEquals("Retained",ImageCreditArchive.records(context).single().credit.text)
        directory.deleteRecursively();assertTrue(directory.createNewFile())
        try {ImageCreditArchive.retainAccepted(context,listOf(ImageCredit(source,"Rejected")));fail("Unwritable archive must report failure")}
        catch(_: IOException) { }
        assertTrue(directory.isFile)
    }
}
