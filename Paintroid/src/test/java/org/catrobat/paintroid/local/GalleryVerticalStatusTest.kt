/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Rect
import android.text.Spanned
import android.text.style.ReplacementSpan
import android.view.View
import android.widget.TextView
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.LooperMode
import java.util.Locale
import kotlin.math.ceil

/** Real persistent gallery failures must use the accepted shared column renderer. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class GalleryVerticalStatusTest {
    @Test @Config(fontScale=1f)
    fun everyVerticalProfileUsesReachableColumnsAtNormalText()=check(1f)

    @Test @Config(fontScale=2f)
    fun everyVerticalProfileUsesReachableColumnsAtLargeText()=check(2f)

    private fun check(scale: Float) {
        GallerySvgReadabilityFixture.check(listOf("mn-Mong","mnc-Mong","lzh-Hant","en-XV","qaa-Zsye-XV"),scale,
            reportDirectory="gallery-vertical-status") {tag,status ->
            assertVerticalStatus(status,tag)
            val description=status.rootView.findViewWithTag<TextView>("gallery_description")
            val expected=IllustrationSource.COMMONS.label+" "+status.context.getString(IllustrationSource.COMMONS.descriptionId)
            assertEquals("All provider/description wording must remain",expected,description.text.toString())
            assertEquals("Accessibility must expose the same full description once",expected,description.createAccessibilityNodeInfo().text.toString())
            val styled=description.text as Spanned
            assertEquals(1,styled.getSpans(0,styled.length,ReplacementSpan::class.java).size)
            assertEquals("An atomic vertical span must occupy one native paragraph, not paint twice",1,description.layout.lineCount)
            GalleryControlsLayoutTest.assertFullLayout("$tag/description",description)
        }
    }

    private fun assertVerticalStatus(status: TextView,tag: String) {
        val direction=VerticalText.uiDirection(Locale.forLanguageTag(tag))
        assertNotEquals(TextDirection.HORIZONTAL,direction)
        val styled=status.text as Spanned
        val spans=styled.getSpans(0,styled.length,ReplacementSpan::class.java)
        assertEquals("One shared vertical renderer must cover the entire message",1,spans.size)
        assertEquals(0,styled.getSpanStart(spans.single()))
        assertEquals(styled.length,styled.getSpanEnd(spans.single()))
        assertEquals("Accessibility keeps the full source text",styled.toString(),status.createAccessibilityNodeInfo().text.toString())
        assertEquals(View.ACCESSIBILITY_LIVE_REGION_POLITE,status.accessibilityLiveRegion)
        assertNull(status.ellipsize)
        val layout=requireNotNull(status.layout)
        assertEquals(styled.length,layout.getLineEnd(layout.lineCount-1))
        assertTrue(layout.height<=status.height-status.totalPaddingTop-status.totalPaddingBottom)
        val density=status.resources.displayMetrics.density
        val label=VerticalText.wrapLabel(styled.toString(),status.paint,(144*density+.5f).toInt().toFloat(),direction)
        val bounds=VerticalText.bounds(label,status.paint,direction,GlyphOrientation.MIXED,1f)
        assertTrue("All columns must be measured before scrolling",ceil(bounds.width()).toInt()<=status.width-status.compoundPaddingLeft-status.compoundPaddingRight)
        val rail=status.parent as ColumnScrollView
        val end=(status.width-rail.width+rail.paddingLeft+rail.paddingRight).coerceAtLeast(0)
        assertEquals("Each replacement message starts at its first reading column",if(direction==TextDirection.VERTICAL_RL) end else 0,rail.scrollX)
        for(position in listOf(0,end)) {
            rail.scrollTo(position,0)
            val visible=Rect()
            assertTrue(status.getLocalVisibleRect(visible))
            assertEquals("The column rail may scroll horizontally but cannot cut off vertical ink",status.height,visible.height())
            if(position==0) assertEquals(0,visible.left)
            if(position==end) assertEquals(status.width,visible.right)
        }
        // Leave the previous message at its opposite end. The next real failure
        // must reset the same rail, including when the new reason is shorter.
        rail.scrollTo(if(direction==TextDirection.VERTICAL_RL) 0 else end,0)
    }
}
