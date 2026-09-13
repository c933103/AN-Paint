/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. Dynamic colour indicator; panel arrows replaced 2026-09-09 with KDE Breeze Icons (LGPL-3.0-or-later). */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.*
import android.view.View
import android.widget.FrameLayout
import android.widget.LinearLayout
import java.util.Locale
import org.catrobat.paintroid.R

class ColourStatusButton(context: Context) : FrameLayout(context) {
    var foreground = Color.BLACK
    var backgroundColour = Color.WHITE
    var editForeground: () -> Unit = {}
    var editBackground: () -> Unit = {}
    private val foregroundTarget = View(context).apply {
        tag="foreground_colour";isClickable=true;isFocusable=true
        setOnClickListener { editForeground() }
    }
    private val backgroundTarget = View(context).apply {
        tag="background_colour";isClickable=true;isFocusable=true
        setOnClickListener { editBackground() }
    }
    init {
        isClickable=true;isFocusable=true;setWillNotDraw(false)
        val colours=LinearLayout(context).apply { orientation=if(VerticalText.uiVertical()) LinearLayout.HORIZONTAL else LinearLayout.VERTICAL }
        colours.addView(foregroundTarget,LinearLayout.LayoutParams(if(VerticalText.uiVertical()) 0 else -1,if(VerticalText.uiVertical()) -1 else 0,1f))
        colours.addView(backgroundTarget,LinearLayout.LayoutParams(if(VerticalText.uiVertical()) 0 else -1,if(VerticalText.uiVertical()) -1 else 0,1f))
        // Separate targets keep foreground/background editing accessible.
        addView(colours,LayoutParams(-1,-1).apply { rightMargin=0 })
    }
    fun refresh() {
        foregroundTarget.contentDescription=ui(R.string.ui_foreground_edit_colour,hex(foreground))
        backgroundTarget.contentDescription=ui(R.string.ui_background_edit_colour,hex(backgroundColour))
        contentDescription=ui(R.string.ui_foreground_colour)+" / "+ui(R.string.ui_background_colour)
        invalidate()
    }
    private fun hex(c: Int)=String.format(Locale.ROOT,"#%06X",c and 0xffffff)
    override fun onDraw(c: Canvas) {
        super.onDraw(c)
        val d=resources.displayMetrics.density
        val p=Paint(Paint.ANTI_ALIAS_FLAG)
        if(VerticalText.uiVertical()) {
            listOf(foreground to ui(R.string.ui_fg),backgroundColour to ui(R.string.ui_bg)).forEachIndexed {i,(colour,name) ->
                val left=i*width/2f
                p.color=colour;c.drawRect(left+2*d,2*d,left+width/2f-2*d,height-2*d,p)
                val luminance=androidx.core.graphics.ColorUtils.calculateLuminance(colour)
                p.color=if(luminance>.179) Color.BLACK else Color.WHITE;p.textSize=11*resources.displayMetrics.scaledDensity
                p.typeface=VerticalText.uiTypeface(context) ?: Typeface.DEFAULT_BOLD
                val caption=name+"\n"+hex(colour)
                val bounds=VerticalText.bounds(caption,p,VerticalText.uiDirection(),GlyphOrientation.MIXED,1f)
                c.save();c.translate(left+(width/2f-bounds.width())/2,(height-bounds.height())/2)
                VerticalText.draw(c,caption,p,VerticalText.uiDirection(),GlyphOrientation.MIXED);c.restore()
            }
            return
        }
        val colourRight=width.toFloat()
        listOf(foreground to ui(R.string.ui_fg),backgroundColour to ui(R.string.ui_bg)).forEachIndexed { i,(colour,name) ->
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
        p.style=Paint.Style.STROKE;p.strokeWidth=d;p.color=EditorColours.outline
        c.drawRect(2*d,d,width-2*d,height-d,p)
    }
    override fun performClick(): Boolean { super.performClick();return true }
    override fun drawableStateChanged() { super.drawableStateChanged();invalidate() }
}
