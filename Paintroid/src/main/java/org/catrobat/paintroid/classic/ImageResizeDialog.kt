/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

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
    private val resize: (ImageDimensions) -> Unit, private val cancel: () -> Unit
) {
    fun show(): AlertDialog {
        val density = activity.resources.displayMetrics.density
        fun dp(n: Int) = (n * density + .5f).toInt()
        fun label(value: String, name: String) = TextView(activity).apply { text = value; tag = name; textSize = 14f; setPadding(0,dp(5),0,dp(5)) }
        val body = LinearLayout(activity).apply { orientation = LinearLayout.VERTICAL; setPadding(dp(20),dp(8),dp(20),dp(12)) }
        body.addView(label("Original: ${source.describe()}\nDecoded image: ${memoryLabel(source.pixels * 4.0)} (RGBA, 4 bytes/pixel)\nEstimated editing memory without resizing: ${memoryLabel(source.pixels * 12.0 + residentPixels * 4.0)}", "resize_original"))
        body.addView(label("The full image and working buffers exceed the current safe budget, or Android could not allocate them. Resize a copy to edit it. Your original file will stay unchanged.", "resize_reason"))
        val budget = label("", "resize_budget"); body.addView(budget)
        val maxScale = previousAttempt?.let { it.width.toDouble() / source.width * .75 } ?: 1.0
        val suggested = policy().suggestResize(source,residentPixels,maxScale) ?: ImageDimensions(1,1)
        val sizing = DimensionControls(activity,source,suggested,"resize",true)
        body.addView(label("Resize the copy", "resize_heading")); body.addView(sizing)
        val estimate = label("", "resize_estimate"); body.addView(estimate)
        body.addView(label("Estimates include the current canvas and clipboard, sampled decoding and editing buffers. Actual memory use varies. A smaller copy loses detail; PNG transparency is preserved.", "resize_explanation"))
        var accepted = false
        val dialog = AlertDialog.Builder(activity).setTitle("Resize large image?")
            .setView(ScrollView(activity).apply { addView(body) })
            .setNegativeButton("Cancel", null).setPositiveButton("Resize and load", null).create()
        fun target(): ImageDimensions? = sizing.dimensions?.takeIf { it.width <= source.width && it.height <= source.height }
        fun refresh(): Boolean {
            val current = policy()
            budget.text = String.format(Locale.ROOT, "Current safe editing budget: %s · up to %.2f MP before decoder overhead", memoryLabel(current.workingBytes.toDouble()), current.maxPixels(residentPixels) / 1_000_000.0)
            val size = target()
            val plan = size?.let { ImportPlan.create(source,it) }
            val fits = plan != null && current.accepts(plan,residentPixels)
            estimate.text = if (size == null) "Enter positive dimensions no larger than the original."
                else "Copy: ${size.describe()}\nDecoded image at this size: ${memoryLabel(size.pixels * 4.0)}\nEstimated loading/editing memory: ${memoryLabel(plan!!.estimatedBytes(residentPixels))}\n" +
                    if (fits) "Fits the current budget." else "Too large for the current budget. Reduce the dimensions or cancel and free memory."
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
