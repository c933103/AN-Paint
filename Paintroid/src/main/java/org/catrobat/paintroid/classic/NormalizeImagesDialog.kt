/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.Activity
import android.app.AlertDialog
import android.text.Editable
import android.text.InputType
import android.text.TextWatcher
import android.view.View
import android.widget.*
import java.util.Locale
import kotlin.math.roundToLong

/** Shared output dimension; each source retains its own crop and aspect ratio. */
class NormalizeImagesDialog(private val activity: Activity,private val assembly: ImageAssembly,private val axis: NormalizeAxis) {
    fun show(): AlertDialog {
        require(assembly.images.isNotEmpty())
        val name = if (axis == NormalizeAxis.WIDTH) "width" else "height"
        val sizes = assembly.images.map { if (axis == NormalizeAxis.WIDTH) it.placedSize.width else it.placedSize.height }
        val largest = sizes.maxOrNull()!!; val smallest = sizes.minOrNull()!!
        fun dp(n: Int) = (n*activity.resources.displayMetrics.density+.5f).toInt()
        val body = LinearLayout(activity).apply { orientation=LinearLayout.VERTICAL; setPadding(dp(18),dp(6),dp(18),dp(8)) }
        body.addView(TextView(activity).apply { text="Give all ${sizes.size} images the same $name. Each image keeps its own aspect ratio. Original files and crop settings stay unchanged." })
        val units = RadioGroup(activity).apply { orientation=LinearLayout.HORIZONTAL }
        val input = EditText(activity).apply { tag="normalize_value"; isSingleLine=true; setSelectAllOnFocus(true); inputType=InputType.TYPE_CLASS_NUMBER; setText(largest.toString()) }
        val info = TextView(activity).apply { tag="normalize_info"; setPadding(0,dp(8),0,dp(8)) }
        var percent = false
        fun value(): Int? {
            val number=input.text.toString().toDoubleOrNull()?.takeIf { it.isFinite() && it>0 && (percent || it==kotlin.math.floor(it)) } ?: return null
            val target=if (percent) number*largest/100 else number
            return target.roundToLong().takeIf { it in 1..Int.MAX_VALUE.toLong() }?.toInt()
        }
        fun display(pixels: Int) {
            input.setText(if (percent) String.format(Locale.ROOT,"%.4f",pixels*100.0/largest).trimEnd('0').trimEnd('.') else pixels.toString())
        }
        val dialog=AlertDialog.Builder(activity).setTitle("Same $name")
            .setView(ScrollView(activity).apply { addView(body) }).setNegativeButton("Cancel",null).setPositiveButton("Apply to all",null).create()
        fun refresh() {
            var valid=false
            try {
                val target=value() ?: throw IllegalArgumentException("Enter a positive size.")
                val normalized=assembly.images.map { it.copy(normalization=ImageNormalization(axis,target)).placedSize }
                val other=normalized.map { if (axis==NormalizeAxis.WIDTH) it.height else it.width }
                info.text="Each $name: $target px\n${if (axis==NormalizeAxis.WIDTH) "Heights" else "Widths"}: ${other.minOrNull()}–${other.maxOrNull()} px\nPercent is relative to the largest current $name: $largest px. Placed images reflow to make room."
                valid=true
            } catch (error: IllegalArgumentException) { info.text=error.message }
            dialog.getButton(AlertDialog.BUTTON_POSITIVE)?.isEnabled=valid
        }
        listOf("Pixels","Percent").forEachIndexed { index,label ->
            units.addView(RadioButton(activity).apply {
                id=View.generateViewId(); tag="normalize_${if(index==0) "pixels" else "percent"}"; text=label; isChecked=index==0
                setOnClickListener {
                    val old=value(); units.check(id); percent=index==1
                    input.inputType=InputType.TYPE_CLASS_NUMBER or if (percent) InputType.TYPE_NUMBER_FLAG_DECIMAL else 0
                    input.contentDescription="Common $name in ${if (percent) "percent of $largest pixels" else "pixels"}"
                    old?.let { display(it) }; refresh()
                }
            },LinearLayout.LayoutParams(0,-2,1f))
        }
        input.contentDescription="Common $name in pixels"
        body.addView(units); body.addView(input)
        val presets=LinearLayout(activity)
        listOf("Smallest" to smallest,"Largest" to largest).forEach { (label,pixels) ->
            presets.addView(Button(activity).apply { text=label; isAllCaps=false; tag="normalize_${label.lowercase(Locale.ROOT)}"; setOnClickListener { display(pixels); refresh() } },LinearLayout.LayoutParams(0,dp(48),1f))
        }
        body.addView(presets); body.addView(info)
        body.addView(Button(activity).apply {
            text="Restore original sizes"; isAllCaps=false; tag="normalize_reset"
            setOnClickListener { try { assembly.resetSizes(); dialog.dismiss() } catch (error: Exception) { info.text=error.message } }
        })
        input.addTextChangedListener(object: TextWatcher {
            override fun beforeTextChanged(s: CharSequence?,start: Int,count: Int,after: Int)=Unit
            override fun onTextChanged(s: CharSequence?,start: Int,before: Int,count: Int) { refresh() }
            override fun afterTextChanged(s: Editable?)=Unit
        })
        dialog.setOnShowListener {
            refresh()
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
                try { value()?.let { assembly.normalize(axis,it); dialog.dismiss() } }
                catch (error: Exception) { info.text=error.message }
            }
        }
        dialog.show(); return dialog
    }
}
