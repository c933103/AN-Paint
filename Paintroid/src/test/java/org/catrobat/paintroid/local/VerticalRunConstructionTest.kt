/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import org.catrobat.paintroid.classic.GlyphOrientation
import org.catrobat.paintroid.classic.VerticalText
import org.junit.Assert.assertEquals
import org.junit.Test

/** Run construction only; native ink/shaping remains covered separately. */
class VerticalRunConstructionTest {
    private fun runs(text: String, orientation: GlyphOrientation): List<Pair<String,Boolean>> {
        val method=VerticalText::class.java.getDeclaredMethod("runs",String::class.java,GlyphOrientation::class.java)
        method.isAccessible=true
        return (method.invoke(VerticalText,text,orientation) as List<*>).map { value ->
            val run=value!!
            val textField=run.javaClass.getDeclaredField("text").apply {isAccessible=true}
            val uprightField=run.javaClass.getDeclaredField("upright").apply {isAccessible=true}
            (textField.get(run) as String) to uprightField.getBoolean(run)
        }
    }
    @Test fun fullLengthSidewaysTextIsOneUnchangedRun() {
        val text="a".repeat(8192)
        for(orientation in listOf(GlyphOrientation.SIDEWAYS,GlyphOrientation.MIXED))
            assertEquals(listOf(text to false),runs(text,orientation))
    }
    @Test fun longLatinPrefixRetainsTheUnchangedMongolianSuffixBoundary() {
        val prefix="a".repeat(8189)
        val suffix="\u202fᠤᠨ"
        for(orientation in listOf(GlyphOrientation.SIDEWAYS,GlyphOrientation.MIXED))
            assertEquals(listOf(prefix to false,suffix to false),runs(prefix+suffix,orientation))
        val root="ᠵᠢᠷᠤᠭ\u202fᠤᠨ"
        assertEquals(listOf(root to false),runs(root,GlyphOrientation.SIDEWAYS))
    }
    @Test fun uprightBoundariesFlushWithoutLosingAdjacentText() {
        val left="a".repeat(4095);val right="b".repeat(4096)
        assertEquals(listOf(left to false,"日" to true,right to false),runs(left+"日"+right,GlyphOrientation.MIXED))
        assertEquals(listOf((left+"日"+right) to false),runs(left+"日"+right,GlyphOrientation.SIDEWAYS))
        assertEquals(listOf("a" to true,"日" to true,"b" to true),runs("a日b",GlyphOrientation.UPRIGHT))
        assertEquals(emptyList<Pair<String,Boolean>>(),runs("",GlyphOrientation.SIDEWAYS))
    }
}
