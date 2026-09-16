/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.Rect

/** Display-only reduction: every source pixel contributes before a small overview is sampled. */
internal class CanvasBitmapOverview : AutoCloseable {
    private val paint=Paint(0).apply {isAntiAlias=false;isFilterBitmap=false}
    private var source: Bitmap?=null
    private var generation=0
    private var level=0
    private var reduced: Bitmap?=null

    fun draw(canvas: Canvas,bitmap: Bitmap,zoom: Float) {
        var targetLevel=0
        var width=bitmap.width;var height=bitmap.height;var scale=zoom
        while(scale<.5f && (width>1 || height>1)) {
            width=(width+1)/2;height=(height+1)/2;scale*=2;targetLevel++
        }
        if(source!==bitmap || generation!=bitmap.generationId || level!=targetLevel) {
            close()
            if(targetLevel>0) {
                var current=bitmap
                try {
                    repeat(targetLevel) {
                        val next=Bitmap.createScaledBitmap(current,(current.width+1)/2,(current.height+1)/2,true)
                        if(current!==bitmap) current.recycle()
                        current=next
                    }
                    reduced=current
                } catch(error: OutOfMemoryError) {
                    // A preview allocation must not damage the editable image or history.
                    if(current!==bitmap) current.recycle()
                }
            }
            source=bitmap;generation=bitmap.generationId;level=targetLevel
        }
        paint.isFilterBitmap=zoom<1f
        val image=reduced ?: bitmap
        canvas.drawBitmap(image,null,Rect(0,0,bitmap.width,bitmap.height),paint)
    }

    override fun close() {reduced?.recycle();reduced=null;source=null;generation=0;level=0}
}
