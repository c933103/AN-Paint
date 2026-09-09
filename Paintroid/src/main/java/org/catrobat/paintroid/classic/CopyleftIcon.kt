/* AN Paint integration, 2026-09-09. GNU AGPL-3.0-or-later.
 * Loaded artwork: KDE Breeze Icons, Copyright (C) 2014 Uri Herrera and others.
 * Artwork licence: LGPL-3.0-or-later. See artwork/breeze and Help > Icon licences.
 */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.Canvas
import androidx.appcompat.content.res.AppCompatResources

/** A cached, tintable resource; the original SVGs and conversion script ship in source. */
internal class CopyleftIcon(context: Context, resource: Int) {
    private val drawable = requireNotNull(AppCompatResources.getDrawable(context, resource)).mutate()
    private var lastTint: Int? = null

    fun draw(canvas: Canvas, left: Float, top: Float, right: Float, bottom: Float, colour: Int) {
        if (lastTint != colour) { drawable.setTint(colour); lastTint = colour }
        canvas.save()
        canvas.translate(left, top)
        canvas.scale((right - left) / 44f, (bottom - top) / 44f)
        drawable.setBounds(0, 0, 44, 44)
        drawable.draw(canvas)
        canvas.restore()
    }
}
