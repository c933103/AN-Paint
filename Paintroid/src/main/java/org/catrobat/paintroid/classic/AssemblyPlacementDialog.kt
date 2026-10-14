/* AN Paint additions, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.Activity
import android.app.AlertDialog
import android.graphics.Typeface
import android.text.InputType
import android.view.View
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import org.catrobat.paintroid.R

/** Text placement uses the numbered source list, independently of the tray's sort order. */
class AssemblyLayoutDialog(private val activity: Activity, private val assembly: ImageAssembly) {
    fun show(): AlertDialog {
        require(assembly.images.isNotEmpty())
        val body = placementBody(activity)
        body.addView(placementText(activity, ui(R.string.ui_assembly_numeric_help)))
        val pattern = EditText(activity).apply {
            tag = "assembly_layout_pattern"
            contentDescription = ui(R.string.ui_assembly_numeric_layout)
            hint = "12\n3\n456"
            inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_MULTI_LINE or InputType.TYPE_TEXT_FLAG_NO_SUGGESTIONS
            minLines = 3
            typeface = Typeface.MONOSPACE
            textDirection = View.TEXT_DIRECTION_LTR
            gravity = android.view.Gravity.TOP or android.view.Gravity.LEFT
            setHorizontallyScrolling(true)
        }
        body.addView(pattern)
        val blankWidth = placementPixelInput(activity, "assembly_blank_width", ui(R.string.ui_assembly_blank_width), 0)
        val blankHeight = placementPixelInput(activity, "assembly_blank_height", ui(R.string.ui_assembly_blank_height), 0)
        body.addView(placementText(activity, ui(R.string.ui_assembly_blank_width)))
        body.addView(blankWidth)
        body.addView(placementText(activity, ui(R.string.ui_assembly_blank_height)))
        body.addView(blankHeight)
        val error = placementText(activity, "").apply { tag = "assembly_layout_error"; accessibilityLiveRegion = View.ACCESSIBILITY_LIVE_REGION_POLITE }
        body.addView(error)
        body.addView(placementText(activity, ui(R.string.ui_assembly_numeric_sources)))
        assembly.images.forEachIndexed { index, image ->
            body.addView(placementText(activity, ui(R.string.ui_assembly_numbered_source, (index + 1).toString(), image.name)))
        }
        val dialog = placementDialog(activity, ui(R.string.ui_assembly_numeric_layout), body)
        dialog.setOnShowListener {
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
                try {
                    val width = placementPixels(blankWidth) ?: throw IllegalArgumentException(ui(R.string.ui_assembly_spacing_nonnegative))
                    val height = placementPixels(blankHeight) ?: throw IllegalArgumentException(ui(R.string.ui_assembly_spacing_nonnegative))
                    assembly.arrangeNumeric(pattern.text.toString(), width, height)
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

/** Independent target coordinates deliberately allow overlap; source pixels and crops stay intact. */
class AssemblyPositionDialog(private val activity: Activity, private val assembly: ImageAssembly, private val imageId: String) {
    fun show(): AlertDialog {
        val image = assembly.image(imageId)
        val rect = assembly.layout()[imageId]
        val body = placementBody(activity)
        val number = (assembly.images.indexOfFirst { it.id == imageId } + 1).toString()
        body.addView(placementText(activity, ui(R.string.ui_assembly_numbered_source, number, image.name)))
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
