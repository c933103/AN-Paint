/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.app.Activity
import android.app.AlertDialog
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.widget.*
import java.util.Locale
import kotlin.math.roundToLong

/** Shared output dimension; each source retains its own crop and aspect ratio. */
class NormalizeImagesDialog(private val activity: Activity,private val assembly: ImageAssembly,private val axis: NormalizeAxis) {
    fun show(): AlertDialog {
        require(assembly.images.isNotEmpty())
        val isWidth = axis == NormalizeAxis.WIDTH
        val sizes = assembly.images.map { if (axis == NormalizeAxis.WIDTH) it.placedSize.width else it.placedSize.height }
        val largest = sizes.maxOrNull()!!; val smallest = sizes.minOrNull()!!
        fun dp(n: Int) = (n*activity.resources.displayMetrics.density+.5f).toInt()
        val body = LinearLayout(activity).apply { orientation=LinearLayout.VERTICAL; setPadding(dp(18),dp(6),dp(18),dp(8)) }
        body.addView(TextView(activity).apply { text=ui(if (isWidth) R.string.ui_normalize_width_intro else R.string.ui_normalize_height_intro, sizes.size) })
        val units = RadioGroup(activity).apply { orientation=LinearLayout.HORIZONTAL }
        val input = EditText(activity).apply { tag="normalize_value"; isSingleLine=true; setSelectAllOnFocus(true); LocaleNumberInput.configure(this); setText(largest.toString()) }
        val info = TextView(activity).apply { tag="normalize_info"; setPadding(0,dp(8),0,dp(8)) }
        var percent = false
        fun value(): Int? {
            val number=uiNumber(input.text.toString())?.takeIf { it.isFinite() && it>0 && (percent || it==kotlin.math.floor(it)) } ?: return null
            val target=if (percent) number*largest/100 else number
            return target.roundToLong().takeIf { it in 1..Int.MAX_VALUE.toLong() }?.toInt()
        }
        fun display(pixels: Int) {
            input.setText(if (percent) String.format(Locale.ROOT,"%.4f",pixels*100.0/largest).trimEnd('0').trimEnd('.') else pixels.toString())
        }
        val dialog=EditorDialogBuilder(activity).setTitle(ui(if (axis == NormalizeAxis.WIDTH) R.string.ui_same_width else R.string.ui_same_height))
            .setView(ScrollView(activity).apply { addView(body) }).setNegativeButton(ui(R.string.ui_cancel),null).setPositiveButton(ui(R.string.ui_apply_to_all),null).create()
        fun refresh() {
            var valid=false
            try {
                val target=value() ?: throw IllegalArgumentException(ui(R.string.ui_enter_a_positive_size))
                val normalized=assembly.images.map { it.copy(normalization=ImageNormalization(axis,target)).placedSize }
                val other=normalized.map { if (axis==NormalizeAxis.WIDTH) it.height else it.width }
                info.text=ui(if (isWidth) R.string.ui_normalize_width_info else R.string.ui_normalize_height_info, target, other.minOrNull(), other.maxOrNull(), largest)
                valid=true
            } catch (error: IllegalArgumentException) { info.text=error.message }
            dialog.getButton(AlertDialog.BUTTON_POSITIVE)?.isEnabled=valid
        }
        listOf(ui(R.string.ui_pixels),ui(R.string.ui_percent)).forEachIndexed { index,label ->
            units.addView(RadioButton(activity).apply {
                id=View.generateViewId(); tag="normalize_${if(index==0) "pixels" else "percent"}"; text=label; isChecked=index==0
                setOnClickListener {
                    val old=value(); units.check(id); percent=index==1
                    LocaleNumberInput.configure(input, decimal = percent)
                    input.contentDescription=if (percent) ui(if (isWidth) R.string.ui_normalize_width_input_percent else R.string.ui_normalize_height_input_percent, largest) else ui(if (isWidth) R.string.ui_width else R.string.ui_height, "px")
                    old?.let { display(it) }; refresh()
                }
            },LinearLayout.LayoutParams(0,-2,1f))
        }
        input.contentDescription=ui(if (isWidth) R.string.ui_width else R.string.ui_height, "px")
        body.addView(units); body.addView(input)
        val presets=LinearLayout(activity)
        listOf(ui(R.string.ui_smallest) to smallest,ui(R.string.ui_largest) to largest).forEach { (label,pixels) ->
            presets.addView(Button(activity).apply { text=label; isAllCaps=false; tag="normalize_${label.lowercase(Locale.ROOT)}"; setOnClickListener { display(pixels); refresh() } },LinearLayout.LayoutParams(0,dp(48),1f))
        }
        body.addView(presets); body.addView(info)
        body.addView(Button(activity).apply {
            text=ui(R.string.ui_restore_original_sizes); isAllCaps=false; tag="normalize_reset"
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
