/* AN Paint, 2026-09-10. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.app.AlertDialog
import android.content.Context
import android.view.Gravity
import android.view.MotionEvent
import android.view.ViewParent
import android.widget.*

/** A slider with a large, tappable value: exact entry needs no narrow inline keyboard field. */
class NumericSlider(context: Context, val name: String, value: Int, val minimum: Int, val maximum: Int,
    val changed: (Int) -> Unit) : LinearLayout(context) {
    val slider: SeekBar=object: SeekBar(context) {
        private var dragParent: ViewParent?=null
        private fun releaseDrag() {
            dragParent?.requestDisallowInterceptTouchEvent(false)
            dragParent=null
        }
        override fun onTouchEvent(event: MotionEvent): Boolean {
            if(event.actionMasked==MotionEvent.ACTION_DOWN) {
                releaseDrag()
                // AbsSeekBar waits for touch slop inside a scrolling container.
                // Claim DOWN first, before a horizontal ancestor can steal MOVE.
                if(isEnabled) {
                    dragParent=parent
                    dragParent?.requestDisallowInterceptTouchEvent(true)
                }
            }
            var handled=false
            try {
                handled=super.onTouchEvent(event)
                return handled
            } finally {
                // POINTER_UP is not terminal while another finger remains down.
                if(!handled || event.actionMasked==MotionEvent.ACTION_UP || event.actionMasked==MotionEvent.ACTION_CANCEL) releaseDrag()
            }
        }
        override fun setEnabled(enabled: Boolean) {
            super.setEnabled(enabled)
            if(!enabled) releaseDrag()
        }
        override fun onDetachedFromWindow() {
            releaseDrag()
            super.onDetachedFromWindow()
        }
    }
    val number=FlowButton(context).apply {columnHeightDp=112}
    private fun dp(n: Int)=(n*resources.displayMetrics.density+.5f).toInt()
    init {
        orientation=if(VerticalText.uiVertical()) HORIZONTAL else VERTICAL;isBaselineAligned=false
        number.isAllCaps=false;number.textSize=11f;number.setPadding(0,0,0,0);number.minWidth=0;number.minimumWidth=0
        addView(number,LayoutParams(if(VerticalText.uiVertical()) -2 else -1,if(VerticalText.uiVertical()) -2 else dp(44)))
        slider.max=maximum-minimum;slider.progress=value.coerceIn(minimum,maximum)-minimum
        slider.contentDescription=name;addView(slider,LayoutParams(if(VerticalText.uiVertical()) dp(100) else -1,dp(44)))
        fun display(n: Int) { number.text=ui(R.string.ui_numeric_slider_value,name,n);number.contentDescription=ui(R.string.ui_tap_to_type_a_number, name, n) }
        display(slider.progress+minimum)
        slider.setOnSeekBarChangeListener(object: SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(bar: SeekBar?,n: Int,user: Boolean) { display(n+minimum);changed(n+minimum) }
            override fun onStartTrackingTouch(bar: SeekBar?)=Unit
            override fun onStopTrackingTouch(bar: SeekBar?)=Unit
        })
        number.setOnClickListener {
            val input=EditText(context).apply {
                tag="numeric_input";LocaleNumberInput.configure(this)
                setText((slider.progress+minimum).toString());selectAll();gravity=Gravity.CENTER
            }
            val dialog=EditorDialogBuilder(context).setTitle(name).setMessage(ui(R.string.ui_enter_a_whole_number_from_to, minimum, maximum))
                .setView(input).setPositiveButton(ui(R.string.ui_apply),null).setNegativeButton(ui(R.string.ui_cancel),null).create()
            dialog.setOnShowListener { dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
                val n=input.text.toString().toIntOrNull()
                if(n==null || n !in minimum..maximum) input.error=ui(R.string.ui_enter_a_number_from_to, minimum, maximum)
                else { slider.progress=n-minimum;dialog.dismiss() }
            } };dialog.show()
        }
    }
}
