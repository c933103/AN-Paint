/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.app.Activity
import android.app.AlertDialog
import android.text.Editable
import android.text.InputType
import android.text.TextWatcher
import android.widget.*
import java.util.Locale
import kotlin.math.roundToInt

class ImageResizeDialog(
    private val activity: Activity, private val source: ImageDimensions,
    private val residentPixels: Long, private val policy: () -> ImageMemoryPolicy,
    private val previousAttempt: ImageDimensions? = null,
    private val resize: (ImageDimensions) -> Unit, private val cancel: () -> Unit,
    private val memoryRequirements: ImportMemoryRequirements = ImportMemoryRequirements()
) {
    fun show(): AlertDialog {
        val density = activity.resources.displayMetrics.density
        fun dp(n: Int) = (n * density + .5f).toInt()
        fun label(value: String, name: String) = TextView(activity).apply { text = value; tag = name; textSize = 14f; setPadding(0,dp(5),0,dp(5)) }
        val body = LinearLayout(activity).apply { orientation = LinearLayout.VERTICAL; setPadding(dp(20),dp(8),dp(20),dp(12)) }
        body.addView(label(ui(R.string.ui_original_decoded_image_rgba_4_bytes_pixel_estimated, source.describe(), memoryLabel(source.pixels * 4.0), memoryLabel(memoryRequirements.estimatedBytes(ImportPlan.create(source,source),residentPixels))), "resize_original"))
        body.addView(label(ui(R.string.ui_the_full_image_and_working_buffers_exceed_the), "resize_reason"))
        val budget = label("", "resize_budget"); body.addView(budget)
        val maxScale = previousAttempt?.let { it.width.toDouble() / source.width * .75 } ?: 1.0
        val suggested = memoryRequirements.suggestResize(source,policy(),residentPixels,maxScale) ?: ImageDimensions(1,1)
        val sizing = DimensionControls(activity,source,suggested,"resize",true)
        body.addView(label(ui(R.string.ui_resize_the_copy), "resize_heading")); body.addView(sizing)
        val estimate = label("", "resize_estimate"); body.addView(estimate)
        body.addView(label(ui(if(memoryRequirements.hasNativeWork) R.string.ui_codec_resize_memory_floor else R.string.ui_estimates_include_the_current_canvas_and_clipboard_sampled), "resize_explanation"))
        var accepted = false
        val dialog = AlertDialog.Builder(activity).setTitle(ui(R.string.ui_resize_large_image))
            .setView(ScrollView(activity).apply { addView(body) })
            .setNegativeButton(ui(R.string.ui_cancel), null).setPositiveButton(ui(R.string.ui_resize_and_load), null).create()
        fun target(): ImageDimensions? = sizing.dimensions?.takeIf { it.width <= source.width && it.height <= source.height }
        fun refresh(): Boolean {
            val current = policy()
            budget.text = String.format(Locale.ROOT, ui(R.string.ui_current_safe_editing_budget_s_up_to_2f), memoryLabel(current.workingBytes.toDouble()), current.maxPixels(residentPixels) / 1_000_000.0)
            val size = target()
            val plan = size?.let { ImportPlan.create(source,it) }
            val fits = plan != null && memoryRequirements.accepts(current,plan,residentPixels)
            val cannotResize=memoryRequirements.hasNativeWork && !memoryRequirements.accepts(current,ImportPlan.create(source,ImageDimensions(1,1)),residentPixels)
            estimate.text = if (size == null) ui(R.string.ui_enter_positive_dimensions_no_larger_than_the_original)
                else ui(R.string.ui_copy_decoded_image_at_this_size_estimated_loading, size.describe(), memoryLabel(size.pixels * 4.0), memoryLabel(memoryRequirements.estimatedBytes(plan!!,residentPixels))) +
                    if (fits) ui(R.string.ui_fits_the_current_budget) else if(cannotResize) "\n"+ui(R.string.ui_no_resize_fits_decoder_memory) else ui(R.string.ui_too_large_for_the_current_budget_reduce_the)
            dialog.getButton(AlertDialog.BUTTON_POSITIVE)?.isEnabled = fits
            return fits
        }
        sizing.changed = { refresh() }
        dialog.setOnDismissListener { if (!accepted) cancel() }
        dialog.setOnShowListener {
            refresh()
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
                if (refresh()) { accepted = true; val size = target()!!; dialog.dismiss(); resize(size) }
            }
        }
        dialog.show(); return dialog
    }
}
