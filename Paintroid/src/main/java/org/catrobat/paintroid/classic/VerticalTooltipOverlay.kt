/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.Rect
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.view.ViewTreeObserver
import android.view.WindowInsets
import android.view.accessibility.AccessibilityManager
import android.widget.FrameLayout
import java.lang.ref.WeakReference

/** Same-window, nonmodal tooltip. Only gestures starting in an overflowing card
 * are owned here; drawing outside the card and the current IME focus are untouched.
 */
internal class VerticalTooltipOverlay(anchor: View,text: CharSequence,private val onDismiss: (VerticalTooltipOverlay)->Unit): FrameLayout(anchor.context) {
    companion object {const val TAG="vertical_tooltip_overlay"}
    private val anchor=WeakReference(anchor)
    private val handler=Handler(Looper.getMainLooper())
    private val expire=Runnable {dismiss()}
    private val dismissLater=Runnable {dismiss()}
    private var dismissed=false
    private var capturingGesture=false
    private var timed=false
    private var appliedInsets: WindowInsets?=null
    private val anchorRect=Rect()
    private val previousSafeBounds=Rect()
    private var observer: ViewTreeObserver?=null
    val card=VerticalFeedbackCard(context,text,"vertical_tooltip") {dismiss()}
    val persistent get()=card.persistent
    private val followAnchor=ViewTreeObserver.OnPreDrawListener {
        val view=this.anchor.get()
        if(view==null || !view.isAttachedToWindow || !view.isShown || view.windowVisibility!=VISIBLE) dismissAfterDispatch()
        else {
            val bounds=Rect()
            if(!view.getGlobalVisibleRect(bounds)) dismissAfterDispatch()
            else {
                val safe=safeBounds()
                if(bounds!=anchorRect || safe!=previousSafeBounds) {
                    anchorRect.set(bounds);previousSafeBounds.set(safe);requestLayout()
                }
            }
        }
        true
    }
    init {
        tag=TAG
        isClickable=false
        isFocusable=false
        addView(card,LayoutParams(-2,-2))
    }
    private fun edge(safe: Rect)=if(safe.height()<dp(160) || safe.width()<dp(100)) dp(4) else dp(16)
    private fun dp(n: Int)=(n*resources.displayMetrics.density+.5f).toInt()
    /** Intersect visible display/IME bounds with this content frame. The frame may
     * already be inset, including legacy adjustResize and inset dialog windows.
     */
    internal fun safeBounds(width: Int=measuredWidth,height: Int=measuredHeight): Rect {
        val origin=IntArray(2);getLocationOnScreen(origin)
        val visible=Rect();getWindowVisibleDisplayFrame(visible)
        val safe=Rect(0,0,width,height)
        val screen=Rect(visible).apply {offset(-origin[0],-origin[1])}
        if(!safe.intersect(screen)) safe.setEmpty()
        if(Build.VERSION.SDK_INT>=30) {
            val inset=(appliedInsets ?: rootWindowInsets)?.getInsets(WindowInsets.Type.systemBars() or WindowInsets.Type.displayCutout() or WindowInsets.Type.ime())
            if(inset!=null) {
                val location=IntArray(2);getLocationInWindow(location)
                val padding=LocaleNotification.insetPadding(inset,location[0],location[1],width,height,rootView.measuredWidth,rootView.measuredHeight)
                if(!safe.intersect(Rect(padding.left,padding.top,width-padding.right,height-padding.bottom))) safe.setEmpty()
            }
        }
        return safe
    }
    override fun onApplyWindowInsets(insets: WindowInsets): WindowInsets {
        appliedInsets=insets
        requestLayout()
        return insets
    }
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        setMeasuredDimension(MeasureSpec.getSize(widthMeasureSpec),MeasureSpec.getSize(heightMeasureSpec))
        val safe=safeBounds()
        val margin=edge(safe)
        card.measure(MeasureSpec.makeMeasureSpec(minOf(dp(420),(safe.width()-2*margin).coerceAtLeast(1)),MeasureSpec.EXACTLY),
            MeasureSpec.makeMeasureSpec((safe.height()-2*margin).coerceAtLeast(1),MeasureSpec.AT_MOST))
    }
    override fun onLayout(changed: Boolean,left: Int,top: Int,right: Int,bottom: Int) {
        val safe=safeBounds()
        val view=anchor.get()
        if(view==null) {dismissAfterDispatch();return}
        if(card.deferred) {handler.removeCallbacks(expire);timed=false;return}
        val margin=edge(safe)
        val origin=IntArray(2);getLocationOnScreen(origin)
        val position=IntArray(2);view.getLocationOnScreen(position)
        val minX=safe.left+margin;val maxX=(safe.right-margin-card.measuredWidth).coerceAtLeast(minX)
        val x=(position[0]-origin[0]+(view.width-card.measuredWidth)/2).coerceIn(minX,maxX)
        val minY=safe.top+margin;val maxY=(safe.bottom-margin-card.measuredHeight).coerceAtLeast(minY)
        val below=position[1]-origin[1]+view.height+dp(8)
        val above=position[1]-origin[1]-card.measuredHeight-dp(8)
        val y=(if(below<=maxY) below else above).coerceIn(minY,maxY)
        card.layout(x,y,x+card.measuredWidth,y+card.measuredHeight)
        if(persistent) {handler.removeCallbacks(expire);timed=false}
        else if(!timed && !dismissed) {
            timed=true
            val accessibility=context.getSystemService(Context.ACCESSIBILITY_SERVICE) as AccessibilityManager
            val duration=if(Build.VERSION.SDK_INT>=29) accessibility.getRecommendedTimeoutMillis(3500,AccessibilityManager.FLAG_CONTENT_TEXT) else 3500
            handler.postDelayed(expire,duration.toLong())
        }
    }
    override fun dispatchTouchEvent(event: MotionEvent): Boolean {
        if(event.actionMasked==MotionEvent.ACTION_DOWN) capturingGesture=persistent && !card.deferred &&
            event.x>=card.left && event.x<card.right && event.y>=card.top && event.y<card.bottom
        if(!capturingGesture) return false
        super.dispatchTouchEvent(event)
        if(event.actionMasked==MotionEvent.ACTION_UP || event.actionMasked==MotionEvent.ACTION_CANCEL) capturingGesture=false
        return true
    }
    fun dismiss() {
        handler.removeCallbacks(expire);handler.removeCallbacks(dismissLater)
        if(dismissed) return
        dismissed=true
        onDismiss(this)
        (parent as? ViewGroup)?.removeView(this)
    }
    fun dismissAfterDispatch() {
        handler.removeCallbacks(expire);handler.removeCallbacks(dismissLater)
        if(!dismissed) handler.post(dismissLater)
    }
    override fun onAttachedToWindow() {
        super.onAttachedToWindow()
        observer=viewTreeObserver.also {it.addOnPreDrawListener(followAnchor)}
    }
    override fun onDetachedFromWindow() {
        observer?.takeIf {it.isAlive}?.removeOnPreDrawListener(followAnchor)
        observer=null
        dismissAfterDispatch()
        super.onDetachedFromWindow()
    }
    override fun onWindowVisibilityChanged(visibility: Int) {
        super.onWindowVisibilityChanged(visibility)
        if(visibility!=VISIBLE) dismissAfterDispatch()
    }
}
