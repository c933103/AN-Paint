/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.content.Context
import android.text.Editable
import android.text.InputType
import android.text.TextWatcher
import android.view.View
import android.widget.*
import java.util.Locale
import kotlin.math.*

/** Canonical pixel dimensions survive unit changes without cumulative rounding. */
class DimensionControls(context: Context, val original: ImageDimensions, initial: ImageDimensions = original,
    prefix: String = "size", locked: Boolean = true) : LinearLayout(context) {
    val widthInput = EditText(context)
    val heightInput = EditText(context)
    val aspectLock = CheckBox(context).apply { text = ui(R.string.ui_lock_aspect_ratio); tag = "${prefix}_lock"; isChecked = locked }
    private val widthLabel = TextView(context)
    private val heightLabel = TextView(context)
    private val result = TextView(context).apply { tag = "${prefix}_result"; textSize = 13f }
    private var percent = false
    private var syncing = false
    private var target: ImageDimensions? = initial
    var changed: (ImageDimensions?) -> Unit = {}
    val dimensions get() = target
    init {
        orientation = VERTICAL
        val units = RadioGroup(context).apply { orientation = HORIZONTAL; tag = "${prefix}_units" }
        listOf(ui(R.string.ui_pixels), ui(R.string.ui_percent)).forEachIndexed { i, text ->
            units.addView(RadioButton(context).apply {
                this.text = text; id = View.generateViewId(); tag = "${prefix}_${if (i == 0) "pixels" else "percent"}"; isChecked = i == 0
                setOnClickListener { units.check(id); if (percent != (i == 1)) { percent = i == 1; display(); changed(target) } }
            },LayoutParams(0,-2,1f))
        }
        addView(units)
        val row = LinearLayout(context)
        listOf(Triple(widthInput,widthLabel,"width"),Triple(heightInput,heightLabel,"height")).forEach { (edit,label,name) ->
            val column = LinearLayout(context).apply { orientation = VERTICAL; setPadding(0,0,8,0) }
            label.textSize = 13f; column.addView(label)
            edit.tag = "${prefix}_$name"; edit.isSingleLine = true; edit.setSelectAllOnFocus(true); column.addView(edit)
            row.addView(column,LayoutParams(0,-2,1f))
        }
        addView(row); addView(aspectLock); addView(result)
        aspectLock.setOnCheckedChangeListener { _, checked -> if (checked && !syncing) read(true) }
        fun watch(edit: EditText, width: Boolean) = edit.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) = Unit
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) { if (!syncing) read(width) }
            override fun afterTextChanged(s: Editable?) = Unit
        })
        watch(widthInput,true); watch(heightInput,false); display()
    }
    private fun number(input: EditText) = uiNumber(input.text.toString())?.takeIf { it.isFinite() && it > 0 && (percent || it == floor(it)) }
    private fun pixels(value: Double?, base: Int): Int? {
        val n = value?.let { if (percent) it * base / 100 else it } ?: return null
        return if (n.isFinite() && n.roundToLong() in 1..Int.MAX_VALUE.toLong()) n.roundToInt() else null
    }
    private fun format(value: Double) = String.format(Locale.ROOT,"%.4f",value).trimEnd('0').trimEnd('.')
    private fun read(fromWidth: Boolean) {
        syncing = true
        val active = if (fromWidth) widthInput else heightInput
        val other = if (fromWidth) heightInput else widthInput
        val base = if (fromWidth) original.width else original.height
        val otherBase = if (fromWidth) original.height else original.width
        if (aspectLock.isChecked) number(active)?.let { n ->
            val next = if (percent) n else n * otherBase / base
            other.setText(if (percent) format(next) else if (next <= Int.MAX_VALUE && next >= .5) next.roundToInt().toString() else "")
        }
        val w = pixels(number(widthInput),original.width); val h = pixels(number(heightInput),original.height)
        target = if (w != null && h != null) ImageDimensions(w,h) else null
        showResult(); syncing = false; changed(target)
    }
    fun setDimensions(size: ImageDimensions) { target = size; display(); changed(target) }
    private fun showResult() { result.text = target?.describe() ?: ui(R.string.ui_enter_positive_dimensions_that_resolve_to_at_least) }
    private fun display() {
        syncing = true
        val unit = if (percent) "%" else "px"
        widthLabel.text = ui(R.string.ui_width, unit); heightLabel.text = ui(R.string.ui_height, unit)
        listOf(widthInput,heightInput).forEach { it.inputType = InputType.TYPE_CLASS_NUMBER or if (percent) InputType.TYPE_NUMBER_FLAG_DECIMAL else 0 }
        widthInput.contentDescription = ui(R.string.ui_width_in, if (percent) ui(R.string.ui_percent_fd8671) else ui(R.string.ui_pixels_6ec9c2))
        heightInput.contentDescription = ui(R.string.ui_height_in, if (percent) ui(R.string.ui_percent_fd8671) else ui(R.string.ui_pixels_6ec9c2))
        target?.let { size ->
            widthInput.setText(if (percent) format(size.width * 100.0 / original.width) else size.width.toString())
            heightInput.setText(if (percent) format(size.height * 100.0 / original.height) else size.height.toString())
        }
        showResult(); syncing = false
    }
}
