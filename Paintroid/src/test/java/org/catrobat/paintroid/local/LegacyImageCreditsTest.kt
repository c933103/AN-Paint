/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import org.catrobat.paintroid.classic.GalleryCredits
import org.catrobat.paintroid.classic.ImageCredit
import org.catrobat.paintroid.classic.ImageCreditArchive
import org.catrobat.paintroid.classic.LegacyImageCredits
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config

/** Read the actual old preference format without claiming it belongs to any artwork. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
class LegacyImageCreditsTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val preferences get()=context.getSharedPreferences("image-credits",Context.MODE_PRIVATE)
    private val source="https://example.org/old.png"

    @Before fun clearPreferences() { assertTrue(preferences.edit().clear().commit()) }
    @After fun cleanup() { preferences.edit().clear().commit() }

    @Test fun editedTextTakesPrecedenceOverGeneratedTextWithoutReformatting() {
        val edited="  Original creator\nChanges: cropped\n\uD86D\uDC40 \uD83C\uDFA8\n"
        assertTrue(preferences.edit().putStringSet("sources",setOf(source))
            .putString("generated:$source","Generated original")
            .putString("text:$source",edited).commit())
        val before=preferences.all
        assertEquals(listOf(ImageCredit(source,edited)),LegacyImageCredits.read(context))
        assertEquals(before,preferences.all)
    }

    @Test fun explicitlyEmptyEditedAndGeneratedStringsAreNotRegenerated() {
        val second="https://example.org/second.png"
        assertTrue(preferences.edit().putStringSet("sources",setOf(second,source))
            .putString("text:$source","").putString("generated:$source","Do not restore")
            .putString("generated:$second","").commit())
        assertEquals(listOf(ImageCredit(source,""),ImageCredit(second,"")),LegacyImageCredits.read(context))
    }

    @Test fun generatedProviderTextAndSourceOnlyCatrobatFallbackMatchHistoricalPrecedence() {
        val second="https://example.org/provider.png"
        val generated="Irasutoya — Takashi Mifune\nOriginal terms and source"
        assertTrue(preferences.edit().putStringSet("sources",setOf(second,source))
            .putString("generated:$second",generated).commit())
        assertEquals(listOf(ImageCredit(source,GalleryCredits.credit(source)),ImageCredit(second,generated)),
            LegacyImageCredits.read(context))
    }

    @Test fun repeatedReadsExposeUnindexedValuesWithoutAdoptingOrChangingPreferences() {
        assertTrue(preferences.edit().putStringSet("sources",setOf(source))
            .putString("text:$source","Original saved credit")
            .putString("text:https://example.org/orphan.png","Unlisted entry").commit())
        val before=preferences.all
        val first=LegacyImageCredits.read(context)
        repeat(3) { assertEquals(first,LegacyImageCredits.read(context)) }
        assertEquals(listOf(ImageCredit(source,"Original saved credit"),
            ImageCredit("https://example.org/orphan.png","Unlisted entry")),first)
        assertEquals(before,preferences.all)
    }

    @Test fun oversizedLegacyTextIsReadableWithoutTruncationOrPreferenceDeletion() {
        // The former editor had no text limit. This exceeds the old entire-draft
        // JSON cap in UTF-8 bytes and must remain accessible outside a draft ledger.
        val oversized="\uD86D\uDC40\"\\\n".repeat(50_000)
        assertTrue(oversized.toByteArray(Charsets.UTF_8).size>262144)
        assertTrue(preferences.edit().putStringSet("sources",setOf(source))
            .putString("text:$source",oversized).commit())
        assertEquals(oversized,LegacyImageCredits.read(context).single().text)
        assertEquals(oversized,preferences.getString("text:$source",null))
    }

    @Test fun selectionTokensAreBoundedAndInvalidOrMissingTokensCannotSelectAnArchiveEntry() {
        assertTrue(preferences.edit().putStringSet("sources",setOf(source))
            .putString("text:$source","Selected text").commit())
        val token=ImageCreditArchive.selectionToken(ImageCredit(source,"Selected text"))
        assertEquals(64,token.length)
        assertEquals(ImageCredit(source,"Selected text"),ImageCreditArchive.find(context,token))
        assertNull(ImageCreditArchive.find(context,null))
        assertNull(ImageCreditArchive.find(context,source))
        assertNull(ImageCreditArchive.find(context,"0".repeat(64)))
        assertNull(ImageCreditArchive.find(context,"a".repeat(100_000)))
    }

    @Test fun missingSourceSetStillExposesEditedAndGeneratedOnlyEntriesWithoutRewritingThem() {
        val second="https://example.org/second.png"
        assertTrue(preferences.edit().putString("text:$source","")
            .putString("generated:$source","Superseded generated text")
            .putString("generated:$second","Kept for recovery").commit())
        val before=preferences.all
        assertTrue(LegacyImageCredits.hasRecords(context))
        assertEquals(listOf(ImageCredit(source,""),ImageCredit(second,"Kept for recovery")),LegacyImageCredits.read(context))
        assertEquals(before,preferences.all)
    }
}
