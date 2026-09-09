/* AN Paint regression checks, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test

@org.junit.runner.RunWith(org.robolectric.RobolectricTestRunner::class)
@org.robolectric.annotation.Config(sdk = [33])
class ImageMemoryPolicyTest {
    private val mib=1024L*1024
    @Test fun safetyBudgetTracksSystemMemoryAndPreservesHeadroom() {
        val small=ImageMemoryPolicy.calculate(512*mib,128*mib,2*1024*mib,128*mib,true)
        val large=ImageMemoryPolicy.calculate(1024*mib,128*mib,6*1024*mib,128*mib,true)
        assertEquals(608*mib,small.workingBytes)
        assertEquals((608*mib-4_000_000)/12,small.maxPixels(1_000_000))
        assertTrue(large.maxPixels()>small.maxPixels())
        small.check(4000,3000,1_000_000) // ordinary 12 MP photos remain full resolution
    }
    @Test fun olderAndroidUsesRemainingJavaHeapAsTheTighterBudget() {
        val policy=ImageMemoryPolicy.calculate(256*mib,128*mib,4*1024*mib,128*mib,false)
        assertEquals(96*mib,policy.workingBytes)
        assertTrue(policy.maxPixels(2_000_000)<policy.maxPixels())
    }
    @Test fun zeroHeadroomRejectsCleanlyWithoutNegativeOrOverflowingThresholds() {
        val policy=ImageMemoryPolicy.calculate(128*mib,100*mib,64*mib,128*mib,false)
        assertEquals(0,policy.maxPixels())
        assertThrows(ImageSizeException::class.java) { policy.check(1,1) }
    }
    @Test fun billionPixelAndIntegerMaxDimensionsAreRejectedBeforeBitmapAllocation() {
        val policy=ImageMemoryPolicy.calculate(64*1024*mib,0,128*1024*mib,0,true)
        assertEquals(ImageMemoryPolicy.MAX_BITMAP_PIXELS,policy.maxPixels())
        for ((w,h) in listOf(32000 to 32000, Int.MAX_VALUE to Int.MAX_VALUE)) {
            val error=assertThrows(ImageSizeException::class.java) { policy.check(w,h) }
            assertTrue(error.message!!.contains("safe editing budget")); assertTrue(error.message!!.contains("No automatic resizing"))
        }
    }
    @Test fun colourModelsKeepChosenHueAndSaturationAtBlackForLaterBrightnessChange() {
        val value=ColourValue(android.graphics.Color.BLACK)
        value.hsv(120f,1f,0f); value.hsv(value.hsv[0],value.hsv[1],1f)
        assertEquals(android.graphics.Color.GREEN,value.colour)
        value.hsl(240f,1f,0f); val hsl=value.hsl; value.hsl(hsl[0],hsl[1],.5f)
        assertEquals(android.graphics.Color.BLUE,value.colour)
    }
    @Test fun importEstimateIncludesLargerSampledDecodeAndProposesSafeCopiesForExtremeDimensions() {
        val policy=ImageMemoryPolicy.calculate(256*mib,128*mib,1024*mib,0,true)
        val plan=ImportPlan.create(ImageDimensions(4000,3000),ImageDimensions(1500,1125))
        assertEquals(25_500_000.0,plan.estimatedBytes(0),0.0)
        for (source in listOf(ImageDimensions(40000,40000),ImageDimensions(Int.MAX_VALUE,Int.MAX_VALUE),ImageDimensions(1,Int.MAX_VALUE))) {
            val copy=policy.suggestResize(source,1_000_000)!!
            assertTrue(copy.pixels < source.pixels)
            assertTrue(policy.accepts(ImportPlan.create(source,copy),1_000_000))
            assertTrue(source.pixels > 0); assertFalse(memoryLabel(source.pixels * 12.0).startsWith("-"))
        }
        assertEquals(4_611_686_014_132_420_609L,ImageDimensions(Int.MAX_VALUE,Int.MAX_VALUE).pixels)
    }
    @Test fun noMemoryHasNoResizeProposalAndStillProvidesReadableOriginalEstimate() {
        val policy=ImageMemoryPolicy.calculate(128*mib,100*mib,64*mib,128*mib,false)
        val source=ImageDimensions(40000,40000)
        assertNull(policy.suggestResize(source,100))
        assertEquals("17.9 GiB",memoryLabel(source.pixels * 12.0))
    }
}
