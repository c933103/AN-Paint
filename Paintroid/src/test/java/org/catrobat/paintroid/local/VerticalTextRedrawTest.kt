/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.view.ContextThemeWrapper
import android.view.View
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.FlowButton
import org.catrobat.paintroid.classic.FlowTextView
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.util.Locale

/** Dirty/layout scheduling, not a software redraw substituted for installed pixels. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w320dp-h640dp-port-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class VerticalTextRedrawTest {
    private fun eachVerticalWidget(check: (String,TextView)->Unit) {
        val original=Locale.getDefault()
        val context=ContextThemeWrapper(RuntimeEnvironment.getApplication() as Context,R.style.ClassicPaintTheme)
        try {
            for(tag in listOf("en-XV","mnc-Mong","lzh-Hant","qaa-Zsye-XV")) {
                Locale.setDefault(Locale.forLanguageTag(tag))
                for(view in listOf<TextView>(FlowButton(context),FlowTextView(context)))
                    check("$tag/${view.javaClass.simpleName}",view)
            }
        } finally {Locale.setDefault(original)}
    }
    private fun measure(view: View) {
        val spec=View.MeasureSpec.makeMeasureSpec(2000,View.MeasureSpec.AT_MOST)
        view.measure(spec,spec);view.layout(0,0,view.measuredWidth,view.measuredHeight)
    }
    private fun resetObservation(view: TextView) {
        assertNull("Custom vertical text must exercise the missing native Layout path",view.layout)
        assertFalse(view.isLayoutRequested)
        shadowOf(view).clearWasInvalidated()
        shadowOf(view).setDidRequestLayout(false)
    }
    private fun assertScheduled(label: String,view: TextView,expected: String) {
        assertEquals(expected,view.text.toString())
        assertTrue("$label must invalidate its own displayed ink after setText",shadowOf(view).wasInvalidated())
        assertTrue("$label must remeasure its custom columns after setText",shadowOf(view).didRequestLayout())
        assertTrue(view.isLayoutRequested)
    }

    @Test fun sameLengthFilenameChangesInvalidateWithoutNativeLayout()=eachVerticalWidget {label,view ->
        view.text="Untitled.png";measure(view);resetObservation(view)
        view.text="Untitled.jpg"
        assertScheduled(label,view,"Untitled.jpg")
    }
    @Test fun repeatedNumericChangesInvalidateEvenWhenColumnSizeStaysTheSame()=eachVerticalWidget {label,view ->
        view.text="Quality (%): 95";measure(view)
        for(value in listOf(76,1,100,1,100)) {
            resetObservation(view)
            val expected="Quality (%): $value";view.text=expected
            assertScheduled(label,view,expected);measure(view)
        }
    }
    @Test fun changedTextReflowsGrowingAndEmptyColumns()=eachVerticalWidget {label,view ->
        view.text="Short";measure(view);val width=view.width;resetObservation(view)
        val long="A changing vertical caption ".repeat(20)
        view.text=long;assertScheduled(label,view,long);measure(view)
        assertTrue("$label must measure all new columns",view.width>width);val wide=view.width
        resetObservation(view);view.text="";assertScheduled(label,view,"");measure(view)
        assertTrue("$label must remove the old wide columns",view.width<wide)
    }
}
