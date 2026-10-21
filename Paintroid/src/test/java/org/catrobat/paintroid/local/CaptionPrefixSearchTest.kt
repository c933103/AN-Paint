/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import org.catrobat.paintroid.classic.CaptionPrefixSearch
import org.junit.Assert.*
import org.junit.Test
import java.util.Random

class CaptionPrefixSearchTest {
    @Test fun ordinaryCaptionsKeepTheLongestFitEvenWhenFittingIsNotMonotone() {
        val random=Random(114)
        for(count in 1..64) repeat(30) {
            val accepted=BooleanArray(count) {random.nextBoolean()}
            val expected=(count-1 downTo 0).firstOrNull {accepted[it]}
            assertEquals(expected,CaptionPrefixSearch.choose(count,{it}) {accepted[it]})
        }
    }

    @Test fun longCaptionsUseBoundedTrialsAndRetainTheOrdinaryFittingBoundary() {
        for(count in listOf(65,128,4096,65536,Int.MAX_VALUE)) {
            for(boundary in listOf(-1,0,1,32,count/2,count-2,count-1)) {
                val tested=mutableSetOf<Int>()
                val result=CaptionPrefixSearch.choose(count,{index ->
                    assertTrue(index in 0 until count)
                    assertTrue("A prefix is constructed at most once",tested.add(index))
                    index
                }) {it<=boundary}
                assertEquals(boundary.takeIf {it>=0},result)
                val logarithmic=32-Integer.numberOfLeadingZeros(count)
                assertTrue("$count clusters used ${tested.size} trials",tested.size<=logarithmic+66)
            }
        }
    }

    @Test fun refinementHandlesAnIsolatedFitWithoutTreatingTheOracleAsMonotone() {
        val tested=mutableSetOf<Int>()
        val result=CaptionPrefixSearch.choose(4096,{it.also(tested::add)}) {it==63 || it==500}
        // A distant nonmonotonic island need not be the selected global maximum.
        // The visible result must be an actually tested fitting candidate.
        assertEquals(63,result)
        assertTrue(result in tested)
        assertTrue(tested.size<=79)
    }

    @Test fun neverReturnsAnUntestedCandidateOrOverflowsWhenNothingFits() {
        data class Label(val count: Int)
        val accepted=mutableListOf<Label>()
        val chosen=CaptionPrefixSearch.choose(65536,::Label) {label ->
            (label.count==7 || label.count==31).also {if(it) accepted.add(label)}
        }
        assertNotNull(chosen)
        assertTrue(accepted.any {it===chosen})
        assertNull(CaptionPrefixSearch.choose(65536,{it}) {false})
        assertNull(CaptionPrefixSearch.choose(0,{fail("Empty text has no shortened prefix");it}) {true})
    }
}
