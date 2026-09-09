/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later.
 * Artwork replaced 2026-09-09 with KDE Breeze Icons, LGPL-3.0-or-later.
 * See artwork/breeze and Help > Icon licences for copyright and full terms.
 */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.*
import android.view.View
import org.catrobat.paintroid.R

enum class EditIcon(val label: String) { UNDO("Undo"), REDO("Redo"), CUT("Cut"), COPY("Copy"), PASTE("Paste"), MINUS("Zoom out"), PLUS("Zoom in"), SELECT_ALL("Select all"), SIDEBAR("Toggle toolbox") }

class ActionButton(context: Context, val icon: EditIcon) : View(context) {
    private val glyph = CopyleftIcon(context, when (icon) {
        EditIcon.UNDO -> R.drawable.breeze_undo
        EditIcon.REDO -> R.drawable.breeze_redo
        EditIcon.CUT -> R.drawable.breeze_cut
        EditIcon.COPY -> R.drawable.breeze_copy
        EditIcon.PASTE -> R.drawable.breeze_paste
        EditIcon.SELECT_ALL -> R.drawable.breeze_select_all
        EditIcon.MINUS -> R.drawable.breeze_zoom_out
        EditIcon.PLUS -> R.drawable.breeze_zoom_in
        EditIcon.SIDEBAR -> R.drawable.breeze_down
    })
    private val collapseGlyph = if (icon == EditIcon.SIDEBAR) CopyleftIcon(context, R.drawable.breeze_up) else null
    init {
        isClickable = true; isFocusable = true; contentDescription = icon.label
        if (android.os.Build.VERSION.SDK_INT >= 26) tooltipText = icon.label
    }
    override fun onDraw(c: Canvas) {
        super.onDraw(c)
        val side = minOf(width, height).toFloat()
        c.save(); c.translate((width - side) / 2, (height - side) / 2); c.scale(side / 48, side / 48)
        val p = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = if (isPressed || icon==EditIcon.SIDEBAR && isSelected) 0xffb8d9f6.toInt() else 0xffdedfdd.toInt() }
        c.drawRoundRect(3f, 3f, 45f, 45f, 4f, 4f, p)
        val current = if (icon == EditIcon.SIDEBAR && isSelected) requireNotNull(collapseGlyph) else glyph
        current.draw(c, 5f, 5f, 43f, 43f, if (isEnabled) 0xff233b4d.toInt() else 0xff8a969f.toInt())
        c.restore()
    }
    override fun drawableStateChanged() { super.drawableStateChanged(); invalidate() }
    override fun setEnabled(enabled: Boolean) { super.setEnabled(enabled); invalidate() }
}
