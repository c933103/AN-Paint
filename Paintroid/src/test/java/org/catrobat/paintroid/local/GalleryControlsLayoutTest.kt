/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.Context
import android.content.res.Resources
import android.view.ContextThemeWrapper
import android.view.View
import android.widget.LinearLayout
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.util.Locale

/** Every offered catalogue uses the actual native controls at the real system font scale. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class GalleryControlsLayoutTest {
    @Test @Config(fontScale=1f)
    fun everyCatalogueKeepsFullLabelsAtNormalScale()=check(1f)

    @Test @Config(fontScale=2f)
    fun everyCatalogueKeepsFullLabelsAtLargeScale()=check(2f)

    private fun check(scale: Float) {
        val app=RuntimeEnvironment.getApplication() as Context
        val originalTag=AppLanguage.selectedTag(app)
        val originalLocale=Locale.getDefault()
        val originalResources=PaintApplication.currentResources
        val started=System.nanoTime()
        var completedCases=0
        val tags=AppLanguage.tags(app)
        val nodes=org.json.JSONArray()
        val hintMeasurements=org.json.JSONArray()
        // Android leaves detached View accessibility nodes uninitialized. Reuse
        // one real window for the entire catalogue matrix, not one per case.
        val controller=Robolectric.buildActivity(Activity::class.java)
        val activity=controller.get().apply {setTheme(R.style.ClassicPaintTheme)}
        controller.setup().visible().windowFocusChanged(true)
        try {
            assertEquals(scale,Resources.getSystem().configuration.fontScale,0f)
            for(tag in tags) {
                AppLanguage.select(app,tag)
                val wrapped=AppLanguage.wrap(app)
                val info=app.packageManager.getActivityInfo(android.content.ComponentName(app,MediaGalleryActivity::class.java),0)
                val context=ContextThemeWrapper(wrapped,info.themeResource)
                assertEquals(scale,context.resources.configuration.fontScale,0f)
                PaintApplication.currentResources=context.resources
                val row=GalleryActions(context)
                val keys=listOf(R.string.ui_copy_all,R.string.gallery_edit_credits,R.string.ui_credits_terms,
                    R.string.ui_done,R.string.ui_search34,R.string.legacy_credits_title)
                var clicks=0
                val buttons=keys.mapIndexed {index,key ->
                    galleryButton(context,context.getString(key),"test_$key",if(index<4) 12f else null) {clicks++}.also {row.addView(it)}
                }
                val originalTextSizes=buttons.map {it.textSize}
                val host: View=if(VerticalText.uiVertical()) ColumnScrollView(context).apply {addView(row)} else row
                if(!VerticalText.uiVertical()) host.layoutDirection=context.resources.configuration.layoutDirection
                LocaleTypography.install(host)
                val searches=listOf(R.string.ui_search34,R.string.ui_search_english34).map {key ->
                    gallerySearchField(context,context.getString(key)).also {
                        it.layoutDirection=context.resources.configuration.layoutDirection;LocaleTypography.install(it)
                    }
                }
                val nodeSample=org.json.JSONObject().put("locale",tag)
                    .put("detached_button",nodeSnapshot(buttons.first()))
                    .put("detached_search",nodeSnapshot(searches.first()))
                nodes.put(nodeSample)
                activity.setContentView(LinearLayout(context).apply {
                    orientation=LinearLayout.VERTICAL
                    addView(host)
                    searches.forEach {addView(it)}
                })
                nodeSample.put("attached_button",nodeSnapshot(buttons.first()))
                    .put("attached_search",nodeSnapshot(searches.first()))
                assertTrue(host.isAttachedToWindow)
                for(widthDp in listOf(240,320,640)) {
                    clicks=0
                    measure(host,widthDp)
                    for((index,button) in buttons.withIndex()) {
                        assertEquals("$tag/$widthDp must not shrink text to fit",originalTextSizes[index],button.textSize,0f)
                        if(scale>1f && index<4) assertTrue(button.textSize>12*context.resources.displayMetrics.density)
                        assertFullLayout("$tag/$widthDp/button",button)
                        val minimum=(48*context.resources.displayMetrics.density+.5f).toInt()
                        assertTrue(button.width>=minimum);assertTrue(button.height>=minimum)
                        assertTrue(button.isAttachedToWindow)
                        assertEquals("android.widget.Button",button.createAccessibilityNodeInfo().className?.toString())
                        assertEquals(button.text.toString(),button.createAccessibilityNodeInfo().text.toString())
                        assertTrue(button.performClick())
                    }
                    assertEquals(buttons.size,clicks)
                    // No two labels may overlap after wrapping into additional rows.
                    for(a in buttons.indices) for(b in a+1 until buttons.size) {
                        val first=android.graphics.Rect(buttons[a].left,buttons[a].top,buttons[a].right,buttons[a].bottom)
                        val second=android.graphics.Rect(buttons[b].left,buttons[b].top,buttons[b].right,buttons[b].bottom)
                        assertFalse("$tag/$widthDp overlapping actions",android.graphics.Rect.intersects(first,second))
                    }
                    for(search in searches) {
                        search.setText("")
                        measure(search,widthDp)
                        val hint=org.robolectric.util.ReflectionHelpers.getField<android.text.Layout>(search,"mHintLayout")
                        hintMeasurements.put(org.json.JSONObject().put("locale",tag).put("width_dp",widthDp)
                            .put("hint",search.hint.toString()).put("view_height",search.height).put("hint_height",hint.height)
                            .put("scroll_y",search.scrollY).put("extended_padding_top",search.extendedPaddingTop)
                            .put("extended_padding_bottom",search.extendedPaddingBottom).put("empty_text_height",search.layout.height).put("total_padding_top",search.totalPaddingTop)
                            .put("total_padding_bottom",search.totalPaddingBottom).put("hint_draw_top",hintDrawTop(search)))
                        assertFullLayout("$tag/$widthDp/search hint",search,search.hint.toString())
                        assertSearchConnection("$tag/$widthDp/empty search",search)
                        assertNull("An editable field must not mask its live value with a fixed description",search.contentDescription)
                        search.setText("A long editable query ".repeat(12))
                        measure(search,widthDp)
                        assertFullLayout("$tag/$widthDp/search value",search)
                        assertTrue("Long query must actually wrap",search.layout.lineCount>1)
                        assertSearchConnection("$tag/$widthDp/wrapped search",search)
                        assertTrue(search.createAccessibilityNodeInfo().isEditable)
                        assertEquals("Accessibility must expose the current editable value",search.text.toString(),search.createAccessibilityNodeInfo().text.toString())
                    }
                    if(widthDp==240) nodeSample
                        .put("attached_button",nodeSnapshot(buttons.first()))
                        .put("attached_search",nodeSnapshot(searches.first()))
                    completedCases++
                }
            }
        } finally {
            val folder=java.io.File("build/reports/gallery-controls-matrix").apply {mkdirs()}
            java.io.File(folder,"api${RuntimeEnvironment.getApiLevel()}-font$scale.json").writeText(org.json.JSONObject()
                .put("offered_catalogues",tags.size).put("expected_cases",tags.size*3).put("completed_cases",completedCases)
                .put("accessibility_nodes",nodes).put("hint_measurements",hintMeasurements)
                .put("elapsed_seconds",(System.nanoTime()-started)/1e9).put("widths_dp",org.json.JSONArray(listOf(240,320,640)))
                .put("evidence_kind","Robolectric NATIVE control measurement; separate JUnit result determines success").toString(2)+"\n")
            activity.finish();controller.pause().stop().destroy()
            AppLanguage.select(app,originalTag);PaintApplication.currentResources=originalResources;Locale.setDefault(originalLocale)
        }
    }

    private fun nodeSnapshot(view: View): org.json.JSONObject {
        val node=view.createAccessibilityNodeInfo()
        return try {org.json.JSONObject().put("attached",view.isAttachedToWindow)
            .put("width",view.width).put("height",view.height)
            .put("class",node.className?.toString() ?: org.json.JSONObject.NULL)
            .put("text",node.text?.toString() ?: org.json.JSONObject.NULL)
            .put("description",node.contentDescription?.toString() ?: org.json.JSONObject.NULL)
            .put("editable",node.isEditable).put("clickable",node.isClickable)
        } finally {node.recycle()}
    }

    private fun measure(view: View,widthDp: Int) {
        val width=(widthDp*view.resources.displayMetrics.density+.5f).toInt()
        view.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(0,View.MeasureSpec.UNSPECIFIED))
        view.layout(0,0,width,view.measuredHeight)
    }

    internal companion object {
        fun assertSearchConnection(label: String,search: android.widget.EditText) {
            val info=android.view.inputmethod.EditorInfo()
            assertNotNull("$label native connection",search.onCreateInputConnection(info))
            assertEquals("$label keyboard Search action",android.view.inputmethod.EditorInfo.IME_ACTION_SEARCH,
                info.imeOptions and android.view.inputmethod.EditorInfo.IME_MASK_ACTION)
            assertEquals("$label must not replace Search with newline",0,
                info.imeOptions and android.view.inputmethod.EditorInfo.IME_FLAG_NO_ENTER_ACTION)
        }

        private fun hintDrawTop(view: TextView)=view.extendedPaddingTop+
            org.robolectric.util.ReflectionHelpers.callInstanceMethod<Int>(view,"getVerticalOffset",
                org.robolectric.util.ReflectionHelpers.ClassParameter.from(java.lang.Boolean.TYPE,false))-view.scrollY

        fun assertFullLayout(label: String,view: TextView,expected: String=view.text.toString()) {
            assertNull("$label must not ellipsize",view.ellipsize)
            val showingHint=view.text.isEmpty() && view.hint!=null
            val layout=requireNotNull(if(showingHint)
                org.robolectric.util.ReflectionHelpers.getField<android.text.Layout>(view,"mHintLayout") else view.layout)
            assertEquals("$label final characters",expected.length,layout.getLineEnd(layout.lineCount-1))
            if(showingHint) {
                // TextView.onDraw selects the hint's gravity offset (false).
                // totalPadding deliberately uses the empty edit buffer (true).
                val top=hintDrawTop(view)
                assertTrue("$label hint top $top is clipped",top>=view.extendedPaddingTop)
                assertTrue("$label hint bottom ${top+layout.height} is clipped at ${view.height-view.extendedPaddingBottom}",
                    top+layout.height<=view.height-view.extendedPaddingBottom)
            } else assertTrue("$label measured text height ${layout.height} exceeds ${view.height-view.totalPaddingTop-view.totalPaddingBottom}",
                layout.height<=view.height-view.totalPaddingTop-view.totalPaddingBottom)
            for(line in 0 until layout.lineCount) {
                assertEquals("$label ellipsis at $line",0,layout.getEllipsisCount(line))
                assertTrue("$label horizontal ink bounds",layout.getLineLeft(line)>=-1f && layout.getLineRight(line)<=layout.width+1f)
            }
        }
    }
}
