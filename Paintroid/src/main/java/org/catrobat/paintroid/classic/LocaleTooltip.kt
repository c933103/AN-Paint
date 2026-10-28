/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.os.Handler
import android.os.Looper
import android.os.Bundle
import android.view.MotionEvent
import android.view.ViewConfiguration
import android.view.accessibility.AccessibilityManager
import android.view.accessibility.AccessibilityNodeInfo
import java.lang.ref.WeakReference
import android.graphics.Typeface
import android.os.Build
import android.text.SpannableString
import android.text.Spanned
import android.text.TextPaint
import android.text.style.MetricAffectingSpan
import android.view.View

/** Native tooltip windows are outside the Activity typography installer.
 * Horizontal profiles retain Android's native placement, input and lifecycle.
 * Vertical profiles use an anchored child of the same window, never a separate
 * popup above the keyboard or a touch-blocking full-window overlay.
 */
internal object LocaleTooltip {
    private fun binding(view: View): Binding =
        (view.getTag(org.catrobat.paintroid.R.id.locale_tooltip_binding) as? Binding) ?: Binding(view).also {
            view.setTag(org.catrobat.paintroid.R.id.locale_tooltip_binding,it)
        }
    internal fun logicalText(view: View): CharSequence? =
        (view.getTag(org.catrobat.paintroid.R.id.locale_tooltip_binding) as? Binding)?.value
    fun set(view: View,text: CharSequence?) {
        if(Build.VERSION.SDK_INT<26) return
        binding(view).apply {value=text;refresh()}
    }
    /** Explicit composition preserves existing Help actions without reflection. */
    fun setHelpAction(view: View,action: (View)->Boolean) {
        if(Build.VERSION.SDK_INT<26) {view.setOnLongClickListener {action(it)};return}
        binding(view).apply {help=action;refresh()}
    }

    private class Binding(view: View): View.OnAttachStateChangeListener {
        private val anchor=WeakReference(view)
        var value: CharSequence?=null
        var help: ((View)->Boolean)?=null
        private val handler=Handler(Looper.getMainLooper())
        private var overlay: VerticalTooltipOverlay?=null
        private var verticalBindings=false
        private var lastConfiguration: android.content.res.Configuration?=null
        private var lastValue: CharSequence?=null
        private var lastHelp: ((View)->Boolean)?=null
        private var originalLongClickable=false
        private var originalDelegate: androidx.core.view.AccessibilityDelegateCompat?=null
        private var observer: android.view.ViewTreeObserver?=null
        private val reveal=Runnable {show()}
        private val focus=android.view.ViewTreeObserver.OnWindowFocusChangeListener {focused -> if(!focused) hide(true)}
        init {
            view.addOnAttachStateChangeListener(this)
            if(view.isAttachedToWindow) onViewAttachedToWindow(view)
        }
        private val delegate=object: androidx.core.view.AccessibilityDelegateCompat() {
            override fun dispatchPopulateAccessibilityEvent(host: View,event: android.view.accessibility.AccessibilityEvent): Boolean =
                originalDelegate?.dispatchPopulateAccessibilityEvent(host,event) ?: super.dispatchPopulateAccessibilityEvent(host,event)
            override fun onInitializeAccessibilityEvent(host: View,event: android.view.accessibility.AccessibilityEvent) {
                originalDelegate?.onInitializeAccessibilityEvent(host,event) ?: super.onInitializeAccessibilityEvent(host,event)
            }
            override fun onPopulateAccessibilityEvent(host: View,event: android.view.accessibility.AccessibilityEvent) {
                originalDelegate?.onPopulateAccessibilityEvent(host,event) ?: super.onPopulateAccessibilityEvent(host,event)
            }
            override fun onRequestSendAccessibilityEvent(host: android.view.ViewGroup,child: View,event: android.view.accessibility.AccessibilityEvent): Boolean =
                originalDelegate?.onRequestSendAccessibilityEvent(host,child,event) ?: super.onRequestSendAccessibilityEvent(host,child,event)
            override fun sendAccessibilityEvent(host: View,eventType: Int) {
                originalDelegate?.sendAccessibilityEvent(host,eventType) ?: super.sendAccessibilityEvent(host,eventType)
            }
            override fun sendAccessibilityEventUnchecked(host: View,event: android.view.accessibility.AccessibilityEvent) {
                originalDelegate?.sendAccessibilityEventUnchecked(host,event) ?: super.sendAccessibilityEventUnchecked(host,event)
            }
            override fun getAccessibilityNodeProvider(host: View): androidx.core.view.accessibility.AccessibilityNodeProviderCompat? =
                originalDelegate?.getAccessibilityNodeProvider(host) ?: super.getAccessibilityNodeProvider(host)
            override fun onInitializeAccessibilityNodeInfo(host: View,info: androidx.core.view.accessibility.AccessibilityNodeInfoCompat) {
                originalDelegate?.onInitializeAccessibilityNodeInfo(host,info) ?: super.onInitializeAccessibilityNodeInfo(host,info)
                info.tooltipText=value
                if(Build.VERSION.SDK_INT>=28 && !value.isNullOrEmpty()) info.addAction(if(overlay!=null)
                    androidx.core.view.accessibility.AccessibilityNodeInfoCompat.AccessibilityActionCompat.ACTION_HIDE_TOOLTIP else
                    androidx.core.view.accessibility.AccessibilityNodeInfoCompat.AccessibilityActionCompat.ACTION_SHOW_TOOLTIP)
            }
            override fun performAccessibilityAction(host: View,action: Int,args: Bundle?): Boolean {
                if(Build.VERSION.SDK_INT>=28) {
                    if(action==AccessibilityNodeInfo.AccessibilityAction.ACTION_SHOW_TOOLTIP.id) return show()
                    if(action==AccessibilityNodeInfo.AccessibilityAction.ACTION_HIDE_TOOLTIP.id) {hide();return true}
                }
                return originalDelegate?.performAccessibilityAction(host,action,args) ?: super.performAccessibilityAction(host,action,args)
            }
        }
        fun refresh() {
            val view=anchor.get() ?: return
            val configuration=android.content.res.Configuration(view.resources.configuration)
            val snapshot=value?.let {if(it is Spanned) android.text.SpannedString(it) else it.toString()}
            // Status refreshes often reassign an unchanged caption. They must not
            // cancel hover dwell or remove an overflow card the user is reading.
            if(lastConfiguration==configuration && lastValue==snapshot && lastHelp===help) return
            lastConfiguration=configuration;lastValue=snapshot;lastHelp=help
            // Caption updates may originate inside visibility/config dispatch.
            // Retire the old child after that traversal, never mutate its sibling array.
            hide(true)
            val vertical=VerticalText.uiVertical(view.context) && !value.isNullOrEmpty()
            if(!vertical) {
                if(verticalBindings) {
                    view.setOnHoverListener(null)
                    view.setOnLongClickListener(null)
                    view.isLongClickable=originalLongClickable
                    androidx.core.view.ViewCompat.setAccessibilityDelegate(view,originalDelegate)
                    originalDelegate=null
                    verticalBindings=false
                }
                view.tooltipText=format(view.context,value)
                help?.let {action -> view.setOnLongClickListener {action(it)}}
                return
            }
            if(!verticalBindings) {
                originalLongClickable=view.isLongClickable
                originalDelegate=androidx.core.view.ViewCompat.getAccessibilityDelegate(view)
                verticalBindings=true
            }
            // All application Help listeners on these controls are composed through
            // setHelpAction; no listener reflection or duplicate native tooltip.
            view.tooltipText=null
            view.setOnLongClickListener {target ->
                hide()
                if(help?.invoke(target)==true) true else show()
            }
            view.setOnHoverListener {target,event ->
                val accessibility=target.context.getSystemService(Context.ACCESSIBILITY_SERVICE) as AccessibilityManager
                if(accessibility.isTouchExplorationEnabled) false else {
                    when(event.actionMasked) {
                        MotionEvent.ACTION_HOVER_ENTER -> {
                            handler.removeCallbacks(reveal)
                            if(overlay==null) handler.postDelayed(reveal,ViewConfiguration.getLongPressTimeout().toLong())
                        }
                        MotionEvent.ACTION_HOVER_EXIT -> {
                            handler.removeCallbacks(reveal)
                            if(overlay?.persistent!=true) hide()
                        }
                    }
                    false
                }
            }
            androidx.core.view.ViewCompat.setAccessibilityDelegate(view,delegate)
        }
        fun show(): Boolean {
            val view=anchor.get() ?: return false
            val text=value?.takeIf {it.isNotEmpty()} ?: return false
            if(!VerticalText.uiVertical(view.context) || !view.isAttachedToWindow || !view.isShown || view.windowVisibility!=View.VISIBLE) return false
            val host=view.rootView.findViewById<View>(android.R.id.content) as? android.widget.FrameLayout ?: return false
            if(!host.isAttachedToWindow || !host.isShown) return false
            hide()
            // One anchored tooltip per window. Its own timers cannot remove a replacement.
            host.findViewWithTag<VerticalTooltipOverlay>(VerticalTooltipOverlay.TAG)?.dismiss()
            val next=VerticalTooltipOverlay(view,text) {dismissed -> if(overlay===dismissed) overlay=null}
            overlay=next
            host.addView(next,android.widget.FrameLayout.LayoutParams(-1,-1))
            next.requestApplyInsets()
            return true
        }
        private fun hide(deferred: Boolean=false) {
            handler.removeCallbacks(reveal)
            val old=overlay
            overlay=null
            if(deferred) old?.dismissAfterDispatch() else old?.dismiss()
        }
        override fun onViewAttachedToWindow(view: View) {
            observer?.takeIf {it.isAlive}?.removeOnWindowFocusChangeListener(focus)
            observer=view.viewTreeObserver.also {it.addOnWindowFocusChangeListener(focus)}
        }
        override fun onViewDetachedFromWindow(view: View) {
            hide(true)
            observer?.takeIf {it.isAlive}?.removeOnWindowFocusChangeListener(focus)
            observer=null
        }
    }

    internal fun format(context: Context,text: CharSequence?): CharSequence? {
        if(text.isNullOrEmpty()) return text
        val previous=(text as? Spanned)?.getSpans(0,text.length,Face::class.java).orEmpty()
        val font=if(VerticalText.uiVertical(context)) null else LocaleTypography.typeface(context)
        if(font==null && previous.isEmpty()) return text
        // Copy rather than mutate caller-owned text; retain every unrelated span.
        return SpannableString(text).apply {
            previous.forEach {removeSpan(it)}
            if(font!=null) setSpan(Face(font),0,length,Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)
        }
    }

    /** TypefaceSpan(Typeface) is API28-only; native tooltips start at API26. */
    private class Face(private val font: Typeface): MetricAffectingSpan() {
        private fun apply(paint: TextPaint) {
            paint.typeface=Typeface.create(font,paint.typeface?.style ?: Typeface.NORMAL)
        }
        override fun updateMeasureState(paint: TextPaint)=apply(paint)
        override fun updateDrawState(paint: TextPaint)=apply(paint)
    }
}
