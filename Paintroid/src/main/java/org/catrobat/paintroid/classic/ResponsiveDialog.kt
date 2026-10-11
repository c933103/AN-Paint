/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.database.DataSetObserver
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.*

/** Keep each region scrollable when large text exceeds a small dialog window.
 * The heading/actions have bounded viewports, never bounded text or line counts.
 * The central region retains at least the remaining 40% at the maximum sizes.
 */
internal class ResponsiveDialogLayout(context: Context): LinearLayout(context) {
    init {orientation=VERTICAL;setBackgroundColor(EditorColours.surface)}
    fun region(view: View,fraction: Float,tagName: String) {
        addView(RegionScrollView(context,fraction).apply {tag=tagName;addView(view)},LayoutParams(-1,-2))
    }
    fun body(view: View) {addView(view,LayoutParams(-1,-2,1f))}
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        val maximum=(resources.configuration.screenHeightDp*resources.displayMetrics.density*.88f).toInt()
        val available=if(MeasureSpec.getMode(heightMeasureSpec)==MeasureSpec.UNSPECIFIED) maximum else minOf(maximum,MeasureSpec.getSize(heightMeasureSpec))
        for(i in 0 until childCount) (getChildAt(i) as? RegionScrollView)?.windowLimit=available
        super.onMeasure(widthMeasureSpec,MeasureSpec.makeMeasureSpec(available,MeasureSpec.AT_MOST))
    }
    private class RegionScrollView(context: Context,private val fraction: Float): ScrollView(context) {
        var windowLimit=Int.MAX_VALUE
        override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
            val maximum=(minOf(windowLimit.toFloat(),resources.configuration.screenHeightDp*resources.displayMetrics.density*.88f)*fraction).toInt()
            val available=if(MeasureSpec.getMode(heightMeasureSpec)==MeasureSpec.UNSPECIFIED) maximum else minOf(maximum,MeasureSpec.getSize(heightMeasureSpec))
            super.onMeasure(widthMeasureSpec,MeasureSpec.makeMeasureSpec(available,MeasureSpec.AT_MOST))
        }
    }
}

/** Use a row only when every caption fits naturally; otherwise use full-width rows.
 * Native Button instances/listeners are retained, including validation overrides.
 */
internal class ResponsiveDialogActions(context: Context): LinearLayout(context) {
    init {gravity=Gravity.END;isBaselineAligned=false}
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        val available=(MeasureSpec.getSize(widthMeasureSpec)-paddingLeft-paddingRight).coerceAtLeast(0)
        var desired=0
        for(i in 0 until childCount) {
            val child=getChildAt(i)
            if(child.visibility==View.GONE) continue
            child.measure(MeasureSpec.makeMeasureSpec(0,MeasureSpec.UNSPECIFIED),MeasureSpec.makeMeasureSpec(0,MeasureSpec.UNSPECIFIED))
            desired+=child.measuredWidth
        }
        orientation=if(MeasureSpec.getMode(widthMeasureSpec)!=MeasureSpec.UNSPECIFIED && desired>available) VERTICAL else HORIZONTAL
        for(i in 0 until childCount) {
            val child=getChildAt(i);val width=if(orientation==VERTICAL) -1 else -2
            val params=child.layoutParams as LayoutParams
            if(params.width!=width || params.height!=-2) {params.width=width;params.height=-2;child.layoutParams=params}
        }
        super.onMeasure(widthMeasureSpec,heightMeasureSpec)
    }
    fun action(button: Button) {
        VerticalUi.detach(button)
        button.setSingleLine(false);button.maxLines=Int.MAX_VALUE;button.ellipsize=null
        addView(button,LayoutParams(-2,-2))
    }
}

/** Preserve the actual ListView, selection modes, IDs and callbacks; remove only
 * the platform row's fixed height and line/ellipsis limits. No synthetic clicks.
 */
internal class WrappingDialogChoices(private val source: ListAdapter): BaseAdapter() {
    override fun getCount()=source.count
    override fun getItem(position: Int)=source.getItem(position)
    override fun getItemId(position: Int)=source.getItemId(position)
    override fun getItemViewType(position: Int)=source.getItemViewType(position)
    override fun getViewTypeCount()=source.viewTypeCount
    override fun hasStableIds()=source.hasStableIds()
    override fun isEmpty()=source.isEmpty
    override fun areAllItemsEnabled()=source.areAllItemsEnabled()
    override fun isEnabled(position: Int)=source.isEnabled(position)
    override fun registerDataSetObserver(observer: DataSetObserver)=source.registerDataSetObserver(observer)
    override fun unregisterDataSetObserver(observer: DataSetObserver)=source.unregisterDataSetObserver(observer)
    override fun getView(position: Int,convertView: View?,parent: ViewGroup): View =
        source.getView(position,convertView,parent).also {view ->
            if(view is TextView) {view.setSingleLine(false);view.maxLines=Int.MAX_VALUE;view.ellipsize=null}
            view.layoutParams=AbsListView.LayoutParams(-1,-2)
        }
}
