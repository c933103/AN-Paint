/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.Typeface
import android.os.Build
import android.text.SpannableString
import android.text.Spanned
import android.text.TextPaint
import android.text.style.MetricAffectingSpan
import android.view.View

/** Native tooltip windows are outside the Activity typography installer.
 * Decorate their text without replacing Android's placement, input or lifecycle.
 * Vertical column layout needs a separate overflow design for the native popup.
 */
internal object LocaleTooltip {
    fun set(view: View,text: CharSequence?) {
        if(Build.VERSION.SDK_INT>=26) view.tooltipText=format(view.context,text)
    }

    internal fun format(context: Context,text: CharSequence?): CharSequence? {
        if(text.isNullOrEmpty()) return text
        val previous=(text as? Spanned)?.getSpans(0,text.length,Face::class.java).orEmpty()
        val font=if(VerticalText.uiVertical()) null else LocaleTypography.typeface(context)
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
