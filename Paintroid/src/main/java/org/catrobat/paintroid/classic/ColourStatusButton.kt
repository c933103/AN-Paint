/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. Dynamic colour indicator; panel arrows replaced 2026-09-09 with KDE Breeze Icons (LGPL-3.0-or-later). */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.*
import android.view.View
import java.util.Locale
import org.catrobat.paintroid.R

class ColourStatusButton(context: Context) : View(context) {
    private val expandGlyph = CopyleftIcon(context, R.drawable.breeze_right)
    private val collapseGlyph = CopyleftIcon(context, R.drawable.breeze_left)
    var foreground = Color.BLACK
    var backgroundColour = Color.WHITE
    var expanded = false
    init { isClickable=true;isFocusable=true }
    fun refresh() {
        contentDescription="Foreground ${hex(foreground)}, background ${hex(backgroundColour)}. ${if (expanded) "Left arrow: collapse" else "Right arrow: expand"} colour palette."
        if (android.os.Build.VERSION.SDK_INT >= 26) tooltipText=if (expanded) "Collapse colour palette" else "Expand colour palette"
        invalidate()
    }
    private fun hex(c: Int)=String.format(Locale.ROOT,"#%06X",c and 0xffffff)
    override fun onDraw(c: Canvas) {
        val d=resources.displayMetrics.density
        val p=Paint(Paint.ANTI_ALIAS_FLAG)
        val colourRight=width-26*d
        listOf(foreground to "FG",backgroundColour to "BG").forEachIndexed { i,(colour,name) ->
            val top=i*height/2f
            p.color=colour;c.drawRect(3*d,top+2*d,colourRight,top+height/2f-2*d,p)
            fun linear(value: Int): Double { val s=value/255.0;return if (s<=.04045) s/12.92 else Math.pow((s+.055)/1.055,2.4) }
            val luminance=.2126*linear(Color.red(colour))+.7152*linear(Color.green(colour))+.0722*linear(Color.blue(colour))
            p.color=if (luminance>.179) Color.BLACK else Color.WHITE
            p.textSize=11*d;p.typeface=Typeface.DEFAULT_BOLD
            val label="$name ${hex(colour)}"
            p.textSize*=minOf(1f,(colourRight-9*d).coerceAtLeast(1f)/p.measureText(label))
            c.drawText(label,6*d,top+height/4f-(p.ascent()+p.descent())/2,p)
        }
        p.color=if (expanded || isPressed) 0xffb8d9f6.toInt() else 0xffdedfdd.toInt()
        c.drawRect(colourRight+2*d,2*d,width-2*d,height-2*d,p)
        val mid=height/2f
        (if (expanded) collapseGlyph else expandGlyph).draw(c, colourRight+2*d, mid-11*d, width-2*d, mid+11*d, 0xff233b4d.toInt())
        p.style=Paint.Style.STROKE;p.strokeWidth=d;p.color=0xff8a969f.toInt()
        c.drawRect(2*d,d,width-2*d,height-d,p)
    }
    override fun performClick(): Boolean { super.performClick();return true }
    override fun drawableStateChanged() { super.drawableStateChanged();invalidate() }
}
