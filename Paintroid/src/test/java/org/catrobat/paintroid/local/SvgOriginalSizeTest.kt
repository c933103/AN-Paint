/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import org.catrobat.paintroid.classic.SvgOriginalSize
import org.junit.Assert.*
import org.junit.Test

class SvgOriginalSizeTest {
    @Test fun preservesAbsoluteDimensionsWithoutArbitraryMaximumOrAspectRatioClamp() {
        for((width,height) in listOf(40 to 24,12000 to 1,1 to 12000,96 to 192,Int.MAX_VALUE to 1)) {
            assertEquals(SvgOriginalSize.Pixels(width,height),SvgOriginalSize.pixels(width.toDouble(),height.toDouble()))
        }
    }

    @Test fun coversFractionalPixelsWithoutClipping() {
        assertEquals(SvgOriginalSize.Pixels(13,8),SvgOriginalSize.pixels(12.25,7.01))
        assertEquals(SvgOriginalSize.Pixels(1,1),SvgOriginalSize.pixels(.25,.5))
    }

    @Test fun rejectsMissingInvalidAndOverflowingSizesWithoutInventingDefaults() {
        for(bad in listOf(-1.0,0.0,Double.NaN,Double.POSITIVE_INFINITY,Double.NEGATIVE_INFINITY,Int.MAX_VALUE.toDouble()+1)) {
            assertTrue(runCatching {SvgOriginalSize.pixels(bad,24.0)}.exceptionOrNull() is IllegalArgumentException)
            assertTrue(runCatching {SvgOriginalSize.pixels(40.0,bad)}.exceptionOrNull() is IllegalArgumentException)
        }
    }
}
