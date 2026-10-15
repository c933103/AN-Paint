/* AN Paint additions, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.Activity
import android.app.AlertDialog
import android.view.View
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import org.catrobat.paintroid.R

/** Independent target coordinates deliberately allow overlap; source pixels and crops stay intact. */
class AssemblyPositionDialog(private val activity: Activity, private val assembly: ImageAssembly, private val imageId: String) {
    fun show(): AlertDialog {
        val image = assembly.image(imageId)
        val rect = assembly.layout()[imageId]
        val body = placementBody(activity)
        body.addView(placementText(activity, image.name))
        body.addView(placementText(activity, ui(R.string.ui_assembly_position_help)))
        val x = placementPixelInput(activity, "assembly_position_x", ui(R.string.ui_assembly_target_x), rect?.left ?: 0)
        val y = placementPixelInput(activity, "assembly_position_y", ui(R.string.ui_assembly_target_y), rect?.top ?: 0)
        body.addView(placementText(activity, ui(R.string.ui_assembly_target_x)))
        body.addView(x)
        body.addView(placementText(activity, ui(R.string.ui_assembly_target_y)))
        body.addView(y)
        val error = placementText(activity, "").apply { tag = "assembly_position_error"; accessibilityLiveRegion = View.ACCESSIBILITY_LIVE_REGION_POLITE }
        body.addView(error)
        val dialog = placementDialog(activity, ui(R.string.ui_assembly_exact_position), body)
        dialog.setOnShowListener {
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
                try {
                    val targetX = placementPixels(x) ?: throw IllegalArgumentException(ui(R.string.ui_assembly_position_nonnegative))
                    val targetY = placementPixels(y) ?: throw IllegalArgumentException(ui(R.string.ui_assembly_position_nonnegative))
                    assembly.position(imageId, targetX, targetY)
                    dialog.dismiss()
                } catch (problem: Exception) {
                    error.text = problem.message ?: ui(R.string.ui_could_not_complete_the_operation)
                }
            }
        }
        dialog.show()
        return dialog
    }
}

private fun placementBody(activity: Activity) = LinearLayout(activity).apply {
    orientation = LinearLayout.VERTICAL
    val pad = (16 * activity.resources.displayMetrics.density + .5f).toInt()
    setPadding(pad, pad / 2, pad, pad / 2)
}

private fun placementText(activity: Activity, value: String) = TextView(activity).apply { text = value }

private fun placementPixelInput(activity: Activity, fieldTag: String, label: String, value: Int) = EditText(activity).apply {
    tag = fieldTag
    contentDescription = label
    isSingleLine = true
    setSelectAllOnFocus(true)
    LocaleNumberInput.configure(this)
    setText(value.toString())
}

private fun placementPixels(input: EditText): Int? = uiNumber(input.text.toString())
    ?.takeIf { it.isFinite() && it >= 0 && it <= Int.MAX_VALUE && it == kotlin.math.floor(it) }?.toInt()

private fun placementDialog(activity: Activity, title: String, body: View): AlertDialog = EditorDialogBuilder(activity)
    .setTitle(title)
    .setView(ScrollView(activity).apply { isFillViewport = true; addView(body) })
    .setNegativeButton(ui(R.string.ui_cancel), null)
    .setPositiveButton(ui(R.string.ui_apply), null)
    .create()
