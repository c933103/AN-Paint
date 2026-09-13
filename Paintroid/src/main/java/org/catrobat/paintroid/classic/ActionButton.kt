/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later.
 * Artwork replaced 2026-09-09 with KDE Breeze Icons, LGPL-3.0-or-later.
 * See artwork/breeze and Help > Icon licences for copyright and full terms.
 */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.*
import android.view.View
import org.catrobat.paintroid.R

enum class EditIcon(private val labelId: Int) { UNDO(R.string.ui_undo), REDO(R.string.ui_redo), CUT(R.string.ui_cut), COPY(R.string.ui_copy), PASTE(R.string.ui_paste), MINUS(R.string.ui_zoom_out), PLUS(R.string.ui_zoom_in), SELECT_ALL(R.string.ui_select_all), SIDEBAR(R.string.ui_toggle_toolbox);
    val label: String get() = ui(labelId)
}

class ActionButton(context: Context, val icon: EditIcon) : FlowButton(context) {
    private val glyph=when(icon) {
        EditIcon.UNDO->R.drawable.breeze_undo;EditIcon.REDO->R.drawable.breeze_redo
        EditIcon.CUT->R.drawable.breeze_cut;EditIcon.COPY->R.drawable.breeze_copy;EditIcon.PASTE->R.drawable.breeze_paste
        EditIcon.SELECT_ALL->R.drawable.breeze_select_all;EditIcon.MINUS->R.drawable.breeze_zoom_out;EditIcon.PLUS->R.drawable.breeze_zoom_in
        EditIcon.SIDEBAR->R.drawable.breeze_down
    }
    init {text=if(icon==EditIcon.SIDEBAR) "" else icon.label;textSize=9f;contentDescription=icon.label;labelledIcon(glyph,22)}
    override fun setSelected(selected: Boolean) {
        super.setSelected(selected)
        if(icon==EditIcon.SIDEBAR) labelledIcon(if(selected) R.drawable.breeze_up else R.drawable.breeze_down,24)
    }
}
