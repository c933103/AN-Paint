/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.Path
import android.widget.Button

/** Compact canvas control; Button text remains available to accessibility services. */
internal class CursorDrawingButton(context: Context): Button(context) {
    init {
        background=null
        minWidth=0;minimumWidth=0;minHeight=0;minimumHeight=0
        setPadding(0,0,0,0)
    }
    override fun onDraw(canvas: Canvas) {
        canvas.save();canvas.scale(width/48f,height/48f)
        val p=Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color=if(isSelected || isPressed) EditorColours.primaryContainer else EditorColours.surfaceContainer
        }
        canvas.drawCircle(24f,24f,22f,p)
        p.style=Paint.Style.STROKE;p.strokeWidth=1f
        p.color=if(isSelected) EditorColours.primary else EditorColours.outline
        canvas.drawCircle(24f,24f,22f,p)
        p.style=Paint.Style.FILL
        p.color=if(!isEnabled) EditorColours.disabledOnSurface else if(isSelected) EditorColours.onPrimaryContainer else EditorColours.onSurface
        if(isSelected) canvas.drawRect(16f,16f,32f,32f,p)
        else canvas.drawPath(Path().apply {moveTo(18f,14f);lineTo(34f,24f);lineTo(18f,34f);close()},p)
        canvas.restore()
    }
    override fun drawableStateChanged() {super.drawableStateChanged();invalidate()}
}
