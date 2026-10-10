/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.annotation.TargetApi
import android.app.Activity
import android.content.Context
import android.content.ContextWrapper
import android.graphics.Typeface
import android.graphics.Insets
import android.graphics.Rect
import android.graphics.drawable.GradientDrawable
import android.os.Handler
import android.os.Looper
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.view.WindowInsets
import android.view.accessibility.AccessibilityManager
import android.widget.FrameLayout
import android.widget.TextView
import android.widget.Toast

/** Font-capable feedback owned by the foreground window, never an overlay window. */
@TargetApi(30)
internal object LocaleNotification {
    private const val TAG="locale_notification"

    private fun activity(context: Context): Activity? {
        var current=context
        while(current is ContextWrapper) {
            if(current is Activity) return current
            val next=current.baseContext
            if(next===current) return null
            current=next
        }
        return null
    }

    fun show(context: Context,text: CharSequence,duration: Int,font: Typeface,anchor: View?): Boolean {
        val owner=activity(context) ?: return false
        if(owner.isFinishing || owner.isDestroyed || owner.window.decorView.windowVisibility!=View.VISIBLE) return false
        if(anchor!=null && activity(anchor.context)!==owner) return false
        val windowRoot=anchor?.rootView ?: owner.window.decorView
        val host=(windowRoot.findViewById<View>(android.R.id.content) as? FrameLayout) ?: return false
        // Visible dialogs and multi-window activities need not hold input focus.
        // These are ordinary child views; they cannot float over another app.
        if(!host.isAttachedToWindow || !host.isShown || host.windowVisibility!=View.VISIBLE) return false
        // The old instance owns its timeout. It can never remove its replacement.
        host.findViewWithTag<Notice>(TAG)?.dismiss()
        val notice=Notice(owner,text,font)
        host.addView(notice,FrameLayout.LayoutParams(-1,-1))
        notice.requestApplyInsets()
        val base=if(duration==Toast.LENGTH_LONG) 3500 else 2000
        val accessibility=owner.getSystemService(Context.ACCESSIBILITY_SERVICE) as AccessibilityManager
        notice.scheduleDismiss(accessibility.getRecommendedTimeoutMillis(base,AccessibilityManager.FLAG_CONTENT_TEXT).toLong())
        return true
    }

    internal fun insetPadding(insets: Insets,x: Int,y: Int,width: Int,height: Int,windowWidth: Int,windowHeight: Int)=Rect(
        (insets.left-x).coerceAtLeast(0),
        (insets.top-y).coerceAtLeast(0),
        (x+width-windowWidth+insets.right).coerceAtLeast(0),
        (y+height-windowHeight+insets.bottom).coerceAtLeast(0)
    )

    private class Notice(context: Context,text: CharSequence,font: Typeface): FrameLayout(context) {
        private val callbackHandler=Handler(Looper.getMainLooper())
        private val expire=Runnable {dismiss()}
        private val dismissLater=Runnable {dismiss()}
        private var dismissed=false
        private fun dp(value: Int)=(value*resources.displayMetrics.density+.5f).toInt()
        init {
            tag=TAG
            isClickable=false
            isFocusable=false
            addView(TextView(context).apply {
                tag="locale_notification_text"
                this.text=text
                typeface=font
                textSize=14f
                setTextColor(EditorColours.onPrimaryContainer)
                setPadding(dp(16),dp(12),dp(16),dp(12))
                background=GradientDrawable().apply {
                    setColor(EditorColours.primaryContainer)
                    cornerRadius=dp(8).toFloat()
                }
                accessibilityLiveRegion=View.ACCESSIBILITY_LIVE_REGION_POLITE
                importantForAccessibility=View.IMPORTANT_FOR_ACCESSIBILITY_YES
                isClickable=false
                isFocusable=false
            },LayoutParams(-1,-2,Gravity.BOTTOM).apply {setMargins(dp(16),dp(16),dp(16),dp(16))})
        }

        // Drawing, taps and gestures continue to reach the editor underneath.
        override fun dispatchTouchEvent(event: MotionEvent)=false

        override fun onApplyWindowInsets(insets: WindowInsets): WindowInsets {
            updateInsets()
            return insets
        }

        override fun onLayout(changed: Boolean,left: Int,top: Int,right: Int,bottom: Int) {
            updateInsets()
            super.onLayout(changed,left,top,right,bottom)
        }

        private fun updateInsets() {
            val insets=rootWindowInsets?.getInsets(WindowInsets.Type.systemBars() or WindowInsets.Type.displayCutout() or WindowInsets.Type.ime()) ?: return
            val location=IntArray(2)
            getLocationInWindow(location)
            // The content may already be inset. Subtract its window offset so
            // legacy fitted windows and API35 edge-to-edge windows both work.
            val padding=insetPadding(insets,location[0],location[1],width,height,rootView.width,rootView.height)
            if(padding.left!=paddingLeft || padding.top!=paddingTop || padding.right!=paddingRight || padding.bottom!=paddingBottom) {
                setPadding(padding.left,padding.top,padding.right,padding.bottom)
            }
        }

        fun scheduleDismiss(timeout: Long) {callbackHandler.postDelayed(expire,timeout)}
        fun dismiss() {
            callbackHandler.removeCallbacks(expire)
            callbackHandler.removeCallbacks(dismissLater)
            if(dismissed) return
            // Android dispatches detach/visibility callbacks before clearing the
            // parent. Guard before removeView so re-entry cannot remove twice.
            dismissed=true
            (parent as? ViewGroup)?.removeView(this)
        }
        private fun dismissAfterDispatch() {
            callbackHandler.removeCallbacks(expire)
            callbackHandler.removeCallbacks(dismissLater)
            // A Handler post runs even after detach. A View post can instead wait
            // for reattachment, leaving a stale notice in a reused dialog.
            if(!dismissed) callbackHandler.post(dismissLater)
        }
        override fun onDetachedFromWindow() {
            dismissAfterDispatch()
            super.onDetachedFromWindow()
        }
        override fun onWindowVisibilityChanged(visibility: Int) {
            super.onWindowVisibilityChanged(visibility)
            // Never mutate the parent's child array during lifecycle dispatch.
            if(visibility!=View.VISIBLE) dismissAfterDispatch()
        }
    }
}
