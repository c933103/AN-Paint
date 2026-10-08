/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import org.catrobat.paintroid.classic.ImageCreditTextPages
import org.junit.Assert.*
import org.junit.Test

class ImageCreditTextPagesTest {
    @Test fun pagesKeepEveryCodeUnitAndNeverSplitASupplementaryCharacter() {
        val original="a".repeat(ImageCreditTextPages.PAGE_CHARS-1)+"\uD86D\uDC40"+
            "\uD86D\uDC40\uD83C\uDFA8\"\\\n".repeat(50_000)
        val pages=ImageCreditTextPages(original)
        val values=(0 until pages.count).map {pages.text(it)}
        assertTrue(values.all {it.length<=ImageCreditTextPages.PAGE_CHARS})
        assertEquals(ImageCreditTextPages.PAGE_CHARS-1,values.first().length)
        for(index in 1 until values.size) {
            assertFalse(Character.isHighSurrogate(values[index-1].last()) && Character.isLowSurrogate(values[index].first()))
        }
        assertEquals(original,values.joinToString(""))
    }

    @Test fun emptyAndExactlyOnePageDoNotAcquireAnExtraBlankPage() {
        val empty=ImageCreditTextPages("")
        assertEquals(1,empty.count);assertEquals("",empty.text(0))
        val exact=ImageCreditTextPages("x".repeat(ImageCreditTextPages.PAGE_CHARS))
        assertEquals(1,exact.count);assertEquals(ImageCreditTextPages.PAGE_CHARS,exact.text(0).length)
    }
}
