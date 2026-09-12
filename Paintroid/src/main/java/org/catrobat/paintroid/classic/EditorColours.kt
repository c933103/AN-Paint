/* AN Paint, 2026. AGPL-3.0-or-later. Palette data: AOSP, Apache-2.0. */
package org.catrobat.paintroid.classic

import androidx.core.content.res.ResourcesCompat
import org.catrobat.paintroid.R

/** Material 3 semantic colours for controls and guides, never document pixels. */
internal object EditorColours {
    private fun colour(id: Int) = ResourcesCompat.getColor(PaintApplication.currentResources, id, null)
    val primary get() = colour(R.color.editor_primary)
    val onPrimary get() = colour(R.color.editor_on_primary)
    val primaryContainer get() = colour(R.color.editor_primary_container)
    val onPrimaryContainer get() = colour(R.color.editor_on_primary_container)
    val secondaryContainer get() = colour(R.color.editor_secondary_container)
    val onSecondaryContainer get() = colour(R.color.editor_on_secondary_container)
    val tertiary get() = colour(R.color.editor_tertiary)
    val onTertiary get() = colour(R.color.editor_on_tertiary)
    val tertiaryContainer get() = colour(R.color.editor_tertiary_container)
    val onTertiaryContainer get() = colour(R.color.editor_on_tertiary_container)
    val surface get() = colour(R.color.editor_surface)
    val surfaceContainer get() = colour(R.color.editor_surface_container)
    val surfaceContainerHigh get() = colour(R.color.editor_surface_container_high)
    val surfaceContainerHighest get() = colour(R.color.editor_surface_container_highest)
    val surfaceDim get() = colour(R.color.editor_surface_dim)
    val onSurface get() = colour(R.color.editor_on_surface)
    val onSurfaceVariant get() = colour(R.color.editor_on_surface_variant)
    val outline get() = colour(R.color.editor_outline)
    val outlineVariant get() = colour(R.color.editor_outline_variant)
    val error get() = colour(R.color.editor_error)
    val inverseSurface get() = colour(R.color.editor_inverse_surface)
    val disabledOnSurface get() = colour(R.color.editor_disabled_on_surface)
}
