/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import androidx.annotation.StringRes
import androidx.annotation.DrawableRes
import org.catrobat.paintroid.R

/** Shared navigation definitions are consumed by the editor and priority/coverage checks.
 * Store resource identities, never a translation captured when the action was created.
 */
internal enum class EditorCommand(@StringRes val labelId: Int,@DrawableRes val icon: Int?=null) {
    NEW(R.string.ui_new), OPEN(R.string.ui_load_image), SAVE(R.string.ui_save),
    SAVE_AS(R.string.save20_title), EXPORT(R.string.ui_export_as23), SHARE(R.string.ui_save_and_share),
    ASSEMBLY(R.string.ui_image_assembly), HELP(R.string.ui_how_to_use), ABOUT(R.string.ui_about_credits23),
    RECOVERY_COPY(R.string.ui_export_recovery_copy),
    SELECT_ALL(R.string.ui_select_all,R.drawable.breeze_select_all),
    CANVAS_BOUNDS(R.string.ui_canvas_bounds,R.drawable.classic_bounds),
    DELETE_SELECTION(R.string.ui_delete_selection,R.drawable.classic_delete),
    CANVAS_SIZE(R.string.ui_canvas_size,R.drawable.classic_canvas_size),
    CROP_SELECTION(R.string.ui_crop_to_selection,R.drawable.classic_crop),
    RESIZE(R.string.ui_resize_image,R.drawable.classic_resize),
    FLIP_HORIZONTAL(R.string.ui_flip_horizontal,R.drawable.classic_flip_h),
    FLIP_VERTICAL(R.string.ui_flip_vertical,R.drawable.classic_flip_v),
    ROTATE_90(R.string.ui_rotate_90_clockwise,R.drawable.classic_rotate90),
    ROTATE_180(R.string.ui_rotate_180,R.drawable.classic_rotate180),
    INVERT(R.string.ui_invert_colours,R.drawable.classic_invert),
    CLEAR(R.string.ui_clear_image,R.drawable.breeze_eraser),
    NAVIGATE(R.string.ui_navigate,R.drawable.breeze_zoom_in),
    PIXEL_GRID(R.string.ui_pixel_grid33,R.drawable.classic_grid),
    CURSOR(R.string.ui_cursor_drawing32,R.drawable.classic_cursor),
    MAGNIFIER(R.string.ui_magnifier33,R.drawable.breeze_zoom_in),
    LANGUAGES(R.string.ui_languages23,R.drawable.classic_languages),
    FULLSCREEN(R.string.ui_fullscreen33,R.drawable.classic_fullscreen),
    VIEW_HELP(R.string.ui_how_to_use,android.R.drawable.ic_menu_help),
    OTHER_IMAGES(R.string.ui_other_images34), SWAP_COLOURS(R.string.ui_swap23),
    RESET_COLOURS(R.string.ui_reset_bw23), ADVANCED_COLOUR(R.string.ui_advanced), ADD_COLOUR(R.string.ui_add_colour26)
}

internal enum class EditorTab(val key: String,@StringRes val labelId: Int) {
    DRAW("Draw",R.string.ui_draw26), FILE("File",R.string.ui_menu_file), EDIT("Edit",R.string.ui_menu_edit),
    VIEW("View",R.string.ui_menu_view), COLOUR("Color",R.string.ui_colour_tab23);
    companion object {
        fun title(key: String)=ui(values().firstOrNull {it.key==key}?.labelId ?: R.string.ui_menu_help)
    }
}

internal enum class EditGroup(@StringRes val labelId: Int,@DrawableRes val icon: Int,val commands: List<EditorCommand>) {
    SELECTION(R.string.ui_category_selection,R.drawable.breeze_select,listOf(EditorCommand.SELECT_ALL,EditorCommand.DELETE_SELECTION,EditorCommand.CROP_SELECTION)),
    CANVAS(R.string.ui_edit_canvas33,R.drawable.classic_canvas_size,listOf(EditorCommand.CANVAS_BOUNDS,EditorCommand.CANVAS_SIZE,EditorCommand.RESIZE,EditorCommand.INVERT,EditorCommand.CLEAR)),
    TRANSFORM(R.string.ui_edit_transform33,R.drawable.classic_rotate90,listOf(EditorCommand.FLIP_HORIZONTAL,EditorCommand.FLIP_VERTICAL,EditorCommand.ROTATE_90,EditorCommand.ROTATE_180))
}
