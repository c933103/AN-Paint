/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.content.Context
import android.graphics.*
import android.view.View
import kotlin.math.min

class AssemblyThumbnail(context: Context,private val item: AssemblyImage,private val bitmap: Bitmap?) : View(context) {
    init { contentDescription = ui(R.string.ui_cropped_thumbnail, item.name) }
    override fun onDraw(canvas: Canvas) {
        val image = bitmap ?: return
        val crop = item.crop
        val scale = min(width.toFloat()/crop.width(),height.toFloat()/crop.height())
        val w = crop.width()*scale; val h = crop.height()*scale
        val dest = RectF((width-w)/2,(height-h)/2,(width+w)/2,(height+h)/2)
        val src = RectF(crop.left.toFloat()*image.width/item.dimensions.width,crop.top.toFloat()*image.height/item.dimensions.height,
            crop.right.toFloat()*image.width/item.dimensions.width,crop.bottom.toFloat()*image.height/item.dimensions.height)
        val matrix = Matrix().apply { setRectToRect(src,dest,Matrix.ScaleToFit.FILL) }
        canvas.save(); canvas.clipRect(dest); canvas.drawBitmap(image,matrix,Paint(Paint.FILTER_BITMAP_FLAG)); canvas.restore()
    }
}
