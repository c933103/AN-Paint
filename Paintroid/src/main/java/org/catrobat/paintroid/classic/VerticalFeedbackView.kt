/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.drawable.GradientDrawable
import android.view.Gravity
import android.view.View
import android.widget.ImageButton
import android.widget.LinearLayout
import android.widget.ScrollView

/** A bounded viewport, not a shortened message. Columns scroll horizontally;
 * an indivisible shaped word taller than the viewport remains vertically reachable.
 * The full original text remains on the native accessible TextView.
 */
internal class VerticalFeedbackView(context: Context,text: CharSequence): ScrollView(context) {
    val message=FlowTextView(context).apply {
        this.text=text
        textSize=14f
        tag="vertical_feedback_text"
        setTextColor(EditorColours.onPrimaryContainer)
        importantForAccessibility=View.IMPORTANT_FOR_ACCESSIBILITY_YES
        setSingleLine(false)
        maxLines=Int.MAX_VALUE
        ellipsize=null
    }
    val columns=ResponsiveDialogColumns(context).apply {
        isHorizontalScrollBarEnabled=true
        addView(message,LayoutParams(-2,-2))
    }
    private var heightLimit=(160*resources.displayMetrics.density).toInt()
    var maximumHeightPx: Int
        get()=heightLimit
        set(value) {if(heightLimit!=value) {heightLimit=value.coerceAtLeast(1);requestLayout()}}
    // Measurement probes must not enqueue another parent traversal each time a
    // footer changes the candidate body height.
    fun measureWithin(widthMeasureSpec: Int,maximum: Int) {
        heightLimit=maximum.coerceAtLeast(1)
        forceLayout()
        measure(widthMeasureSpec,MeasureSpec.makeMeasureSpec(heightLimit,MeasureSpec.AT_MOST))
    }
    val hasOverflow: Boolean get()=message.measuredWidth>columns.measuredWidth-columns.paddingLeft-columns.paddingRight ||
        columns.measuredHeight>measuredHeight-paddingTop-paddingBottom

    init {
        tag="vertical_feedback_viewport"
        isFillViewport=false
        isVerticalScrollBarEnabled=true
        addView(columns,LayoutParams(-1,-2))
    }
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        val available=if(MeasureSpec.getMode(heightMeasureSpec)==MeasureSpec.UNSPECIFIED) maximumHeightPx
            else minOf(maximumHeightPx,MeasureSpec.getSize(heightMeasureSpec))
        val columnHeight=((available-paddingTop-paddingBottom)/resources.displayMetrics.density).toInt().coerceAtLeast(1)
        if(message.columnHeightDp!=columnHeight) {
            message.columnHeightDp=columnHeight
            message.forceLayout()
            columns.forceLayout()
            message.invalidate()
        }
        // ScrollView measures its child without a vertical cap. Do not constrain
        // FlowTextView itself: that would clip a nonbreaking Mongolian word.
        super.onMeasure(widthMeasureSpec,MeasureSpec.makeMeasureSpec(available.coerceAtLeast(1),MeasureSpec.AT_MOST))
    }
}

/** The dismiss action never moves with either message scroll rail. Decide whether
 * it is needed during measurement, not in a later traversal or timeout callback.
 */
internal class VerticalFeedbackCard(context: Context,text: CharSequence,prefix: String,dismiss: ()->Unit): LinearLayout(context) {
    val viewport=VerticalFeedbackView(context,text)
    val done=FlowButton(context).apply {
        this.text=context.getString(org.catrobat.paintroid.R.string.ui_done)
        tag="${prefix}_dismiss"
        columnHeightDp=48
        setOnClickListener {dismiss()}
    }
    val compactDone=ImageButton(context).apply {
        contentDescription=done.text
        tag="${prefix}_dismiss_compact"
        setImageResource(android.R.drawable.ic_menu_close_clear_cancel)
        setColorFilter(EditorColours.onPrimaryContainer)
        setPadding(dp(10),dp(10),dp(10),dp(10))
        setOnClickListener {dismiss()}
        visibility=View.GONE
    }
    val dismissControl: View get()=if(compactDone.visibility==View.VISIBLE) compactDone else done
    var hasOverflow=false
        private set
    var persistent=false
        private set
    var deferred=false
        private set
    private fun dp(n: Int)=(n*resources.displayMetrics.density+.5f).toInt()
    init {
        tag="${prefix}_card"
        orientation=VERTICAL
        setPadding(dp(16),dp(12),dp(16),dp(12))
        background=GradientDrawable().apply {setColor(EditorColours.primaryContainer);cornerRadius=dp(8).toFloat()}
        viewport.message.tag="${prefix}_text"
        addView(viewport,LayoutParams(-1,-2))
        addView(done,LayoutParams(-2,-2).apply {gravity=Gravity.END})
        addView(compactDone,LayoutParams(dp(44),dp(44)).apply {gravity=Gravity.END})
    }
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        val available=if(MeasureSpec.getMode(heightMeasureSpec)==MeasureSpec.UNSPECIFIED) dp(240)
            else MeasureSpec.getSize(heightMeasureSpec)
        // Preserve a usable body and a real 44dp target before spending space
        // on decoration. Very small windows retain the card invisibly until resize.
        val padding=if(available<dp(112)) 0 else dp(12)
        setPadding(if(MeasureSpec.getSize(widthMeasureSpec)<dp(100)) 0 else dp(16),padding,
            if(MeasureSpec.getSize(widthMeasureSpec)<dp(100)) 0 else dp(16),padding)
        val bodySpace=(available-paddingTop-paddingBottom).coerceAtLeast(1)
        val bodyWidth=(MeasureSpec.getSize(widthMeasureSpec)-paddingLeft-paddingRight).coerceAtLeast(1)
        viewport.measureWithin(MeasureSpec.makeMeasureSpec(bodyWidth,MeasureSpec.EXACTLY),minOf(dp(160),bodySpace))
        hasOverflow=viewport.hasOverflow
        persistent=persistent || hasOverflow
        var footerHeight=0
        var compact=false
        if(persistent) {
            done.measure(MeasureSpec.makeMeasureSpec(0,MeasureSpec.UNSPECIFIED),
                MeasureSpec.makeMeasureSpec(0,MeasureSpec.UNSPECIFIED))
            compact=done.measuredHeight+dp(44)>bodySpace || done.measuredWidth>bodyWidth
            footerHeight=if(compact) dp(44) else done.measuredHeight
        }
        deferred=persistent && (bodySpace<footerHeight+dp(44) || bodyWidth<dp(44))
        // Do not toggle visibility off and on during repeated measurements: doing
        // so can enqueue layouts and accessibility changes without a text change.
        done.visibility=if(persistent && !compact) View.VISIBLE else View.GONE
        compactDone.visibility=if(persistent && compact) View.VISIBLE else View.GONE
        visibility=if(deferred) View.INVISIBLE else View.VISIBLE
        if(deferred) {
            isClickable=false
            setMeasuredDimension(MeasureSpec.getSize(widthMeasureSpec),0)
            return
        }
        viewport.measureWithin(MeasureSpec.makeMeasureSpec(bodyWidth,MeasureSpec.EXACTLY),minOf(dp(160),bodySpace-footerHeight))
        super.onMeasure(widthMeasureSpec,heightMeasureSpec)
        hasOverflow=viewport.hasOverflow
        isClickable=persistent && !deferred
    }
}
