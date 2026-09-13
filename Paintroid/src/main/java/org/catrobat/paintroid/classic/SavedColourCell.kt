/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.Canvas
import android.graphics.Paint
import android.view.View

/** Empty saved slots keep the same size and a visible add affordance. */
internal class SavedColourCell(context: Context) : View(context) {
    var colour: Int? = null
        set(value) { field=value;invalidate() }
    override fun onDraw(canvas: Canvas) {
        val d=resources.displayMetrics.density
        val p=Paint(Paint.ANTI_ALIAS_FLAG).apply {color=colour ?: EditorColours.surface}
        canvas.drawRect(d,d,width-d,height-d,p)
        p.style=Paint.Style.STROKE;p.strokeWidth=2*d;p.color=EditorColours.outline
        canvas.drawRect(d,d,width-d,height-d,p)
        if(colour==null) {
            canvas.drawLine(width/2f-5*d,height/2f,width/2f+5*d,height/2f,p)
            canvas.drawLine(width/2f,height/2f-5*d,width/2f,height/2f+5*d,p)
        }
    }
}
