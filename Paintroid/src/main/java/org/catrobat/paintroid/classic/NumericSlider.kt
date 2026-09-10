/* AN Paint, 2026-09-10. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.AlertDialog
import android.content.Context
import android.text.InputType
import android.view.Gravity
import android.widget.*

/** A slider with a large, tappable value: exact entry needs no narrow inline keyboard field. */
class NumericSlider(context: Context, val name: String, value: Int, val minimum: Int, val maximum: Int,
    val changed: (Int) -> Unit) : LinearLayout(context) {
    val slider=SeekBar(context)
    val number=Button(context)
    private fun dp(n: Int)=(n*resources.displayMetrics.density+.5f).toInt()
    init {
        orientation=VERTICAL
        number.isAllCaps=false;number.textSize=11f;number.setPadding(0,0,0,0);number.minWidth=0;number.minimumWidth=0
        addView(number,LayoutParams(-1,dp(44)))
        slider.max=maximum-minimum;slider.progress=value.coerceIn(minimum,maximum)-minimum
        slider.contentDescription=name;addView(slider,LayoutParams(-1,dp(44)))
        fun display(n: Int) { number.text="$name: $n";number.contentDescription="$name: $n. Tap to type a number." }
        display(slider.progress+minimum)
        slider.setOnSeekBarChangeListener(object: SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(bar: SeekBar?,n: Int,user: Boolean) { display(n+minimum);changed(n+minimum) }
            override fun onStartTrackingTouch(bar: SeekBar?)=Unit
            override fun onStopTrackingTouch(bar: SeekBar?)=Unit
        })
        number.setOnClickListener {
            val input=EditText(context).apply { tag="numeric_input";inputType=InputType.TYPE_CLASS_NUMBER;setText((slider.progress+minimum).toString());selectAll();gravity=Gravity.CENTER }
            val dialog=AlertDialog.Builder(context).setTitle(name).setMessage("Enter a whole number from $minimum to $maximum.")
                .setView(input).setPositiveButton("Apply",null).setNegativeButton("Cancel",null).create()
            dialog.setOnShowListener { dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
                val n=input.text.toString().toIntOrNull()
                if(n==null || n !in minimum..maximum) input.error="Enter a number from $minimum to $maximum."
                else { slider.progress=n-minimum;dialog.dismiss() }
            } };dialog.show()
        }
    }
}
