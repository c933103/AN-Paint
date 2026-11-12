/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.view.View
import android.widget.FrameLayout
import android.widget.ScrollView
import android.widget.HorizontalScrollView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[35],qualifiers="w640dp-h480dp-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class SharedPanelPolicyTest {
    @Test fun nativeScrollersAndDialogScrollersInheritTheSameContentOnlyPolicy() {
        val controller=Robolectric.buildActivity(Activity::class.java)
        val activity=controller.get().apply {setTheme(R.style.ClassicPaintTheme)}
        controller.setup()
        try {
            val dialog=EditorDialogBuilder(activity).create()
            for(context in listOf(activity,dialog.context)) {
                assertEquals(View.OVER_SCROLL_IF_CONTENT_SCROLLS,ScrollView(context).overScrollMode)
                assertEquals(View.OVER_SCROLL_IF_CONTENT_SCROLLS,HorizontalScrollView(context).overScrollMode)
            }
        } finally {controller.pause().stop().destroy()}
    }

    @Test fun anyBoundedPanelUsesItsContentSizeAndScrollsOnlyAfterOverflow() {
        val controller=Robolectric.buildActivity(Activity::class.java)
        val activity=controller.get().apply {setTheme(R.style.ClassicPaintTheme)}
        controller.setup()
        try {
            val panel=LimitedScrollView(activity,200,180)
            // ScrollView measures its content with an UNSPECIFIED height. A
            // bare View has no desired height there, even with a fixed parent
            // layout parameter. Use real container content with a sized child.
            val content=FrameLayout(activity)
            val item=View(activity)
            content.addView(item,FrameLayout.LayoutParams(128,64))
            panel.addView(content,FrameLayout.LayoutParams(-2,-2))
            fun layout() {
                panel.measure(View.MeasureSpec.makeMeasureSpec(500,View.MeasureSpec.AT_MOST),
                    View.MeasureSpec.makeMeasureSpec(500,View.MeasureSpec.AT_MOST))
                panel.layout(0,0,panel.measuredWidth,panel.measuredHeight)
            }
            layout()
            assertEquals(128,content.width);assertEquals(64,content.height)
            assertEquals(128,panel.width);assertEquals(64,panel.height)
            assertFalse(panel.canScrollVertically(1));assertFalse(panel.canScrollVertically(-1))
            item.layoutParams=FrameLayout.LayoutParams(256,400)
            layout()
            assertEquals(180,panel.width);assertEquals(200,panel.height)
            assertEquals(400,content.height)
            assertTrue(panel.canScrollVertically(1))
            panel.scrollTo(0,content.height)
            assertEquals(200,panel.scrollY)
            assertFalse(panel.canScrollVertically(1));assertTrue(panel.canScrollVertically(-1))
            item.layoutParams=FrameLayout.LayoutParams(128,64)
            layout()
            assertEquals(128,panel.width);assertEquals(64,panel.height)
            assertEquals(0,panel.scrollY)
            assertFalse(panel.canScrollVertically(1));assertFalse(panel.canScrollVertically(-1))
        } finally {controller.pause().stop().destroy()}
    }
}
