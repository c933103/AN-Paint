/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.LooperMode

/** AN-W04 diagnostic candidate. Deliberately outside Gradle test source sets.
 * Copy into Paintroid/src/test/.../local only in the separately authorized fix.
 * Current source lacks the required vertical renderer. This has NOT been run.
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class GalleryVerticalStatusRegressionCandidate {
    @Test fun verticalGalleryErrorsUseColumnsAndRemainCompletelyReachable() {
        GallerySvgReadabilityFixture.check(listOf("mn-Mong","mnc-Mong","lzh-Hant","en-XV","qaa-Zsye-XV")) {
                tag,status ->
            assertTrue("$tag gallery_status lacks vertical rendering",GallerySvgReadabilityFixture.hasVerticalRenderer(status))
            // A scrollable-column fix needs a reachability assertion for every column;
            // do not weaken this into testing only retained text or an isolated helper.
            GallerySvgReadabilityFixture.assertEntireMessageVisible(status)
        }
    }
}
