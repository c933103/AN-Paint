/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.*
import android.text.Layout
import android.text.StaticLayout
import android.text.TextPaint
import java.util.Locale
import kotlin.math.ceil
import kotlin.math.max

enum class TextDirection { HORIZONTAL, VERTICAL_RL, VERTICAL_LR }
enum class GlyphOrientation { MIXED, SIDEWAYS, UPRIGHT }

/** Shared shaping and measurements for inserted text, previews and vertical UI labels. */
internal object VerticalText {
    fun uiDirection(): TextDirection {
        val locale=Locale.getDefault()
        return when {locale.language=="lzh"->TextDirection.VERTICAL_RL
            locale.language=="mn" && locale.script=="Mong"->TextDirection.VERTICAL_LR
            else->TextDirection.HORIZONTAL}
    }
    fun uiVertical()=uiDirection()!=TextDirection.HORIZONTAL
    private var mongolianFace: Typeface?=null
    fun uiTypeface(context: Context): Typeface? {
        if(Locale.getDefault().language!="mn" || Locale.getDefault().script!="Mong") return null
        return mongolianFace ?: Typeface.createFromAsset(context.assets,"fonts/notosansmongolian.ttf").also {mongolianFace=it}
    }
    /** Preserve surrogate pairs, combining marks, variation selectors and ZWJ sequences. */
    fun clusters(text: String): List<String> {
        val result=mutableListOf<String>();var i=0;var previous=-1;var regionalCount=0
        while(i<text.length) {
            val cp=Character.codePointAt(text,i);val count=Character.charCount(cp);val part=text.substring(i,i+count)
            val type=Character.getType(cp)
            val regional=cp in 0x1f1e6..0x1f1ff
            val attach=result.isNotEmpty() && (previous==0x200d || cp==0x200d || cp in 0xfe00..0xfe0f || cp in 0xe0100..0xe01ef ||
                cp in 0x1f3fb..0x1f3ff || type==Character.NON_SPACING_MARK.toInt() || type==Character.COMBINING_SPACING_MARK.toInt() ||
                type==Character.ENCLOSING_MARK.toInt() || regional && regionalCount%2==1)
            if(attach) result[result.lastIndex]+=part else result.add(part)
            regionalCount=if(regional) regionalCount+1 else 0;previous=cp;i+=count
        }
        return result
    }
    private fun upright(text: String): Boolean {
        val cp=Character.codePointAt(text,0)
        return cp in 0x2e80..0xa4cf || cp in 0xac00..0xd7ff || cp in 0xf900..0xfaff || cp in 0xfe10..0xfe4f ||
            cp in 0xff01..0xff60 || cp in 0x1f000..0x1ffff || cp in 0x20000..0x3ffff
    }
    private val punctuation=mapOf('、' to '︑','。' to '︒','「' to '﹁','」' to '﹂','『' to '﹃','』' to '﹄','（' to '︵','）' to '︶','【' to '︻','】' to '︼','…' to '︙')
    private data class Run(val text: String,val upright: Boolean)
    private fun runs(line: String,orientation: GlyphOrientation): List<Run> {
        if(orientation==GlyphOrientation.SIDEWAYS) return listOf(Run(line,false))
        val result=mutableListOf<Run>()
        for(cluster in clusters(line)) {
            val up=orientation==GlyphOrientation.UPRIGHT || upright(cluster)
            if(!up && result.lastOrNull()?.upright==false) {
                val last=result.removeAt(result.lastIndex);result.add(Run(last.text+cluster,false))
            } else result.add(Run(cluster,up))
        }
        return result
    }
    @Suppress("DEPRECATION")
    private fun layout(text: String,paint: Paint): StaticLayout {
        val p=TextPaint(paint)
        return StaticLayout(text,p,ceil(max(1f,Layout.getDesiredWidth(text,p))).toInt()+2,Layout.Alignment.ALIGN_NORMAL,1f,0f,false)
    }
    fun bounds(text: String,paint: Paint,direction: TextDirection,orientation: GlyphOrientation,spacing: Float): RectF {
        val lines=text.split('\n');val cell=paint.fontSpacing;val step=cell*spacing
        if(direction==TextDirection.HORIZONTAL) return RectF(0f,0f,lines.maxOf {layout(it,paint).width}.toFloat(),(lines.size-1)*step+cell)
        val heights=lines.map {line->runs(line,orientation).sumOf {if(it.upright) cell.toDouble() else layout(it.text,paint).width.toDouble()}.toFloat()}
        return RectF(0f,0f,(lines.size-1)*step+cell,heights.maxOrNull()?.coerceAtLeast(cell) ?: cell)
    }
    fun draw(canvas: Canvas,text: String,paint: Paint,direction: TextDirection,orientation: GlyphOrientation,
        spacing: Float=1f,alignment: Paint.Align=Paint.Align.LEFT) {
        val lines=text.split('\n');val cell=paint.fontSpacing;val step=cell*spacing
        val bounds=bounds(text,paint,direction,orientation,spacing)
        fun offset(length: Float,full: Float)=when(alignment) {Paint.Align.CENTER->(full-length)/2;Paint.Align.RIGHT->full-length;else->0f}
        if(direction==TextDirection.HORIZONTAL) {
            lines.forEachIndexed {i,line->val shaped=layout(line,paint);canvas.save();canvas.translate(offset(shaped.width.toFloat(),bounds.width()),i*step);shaped.draw(canvas);canvas.restore()}
            return
        }
        lines.forEachIndexed {i,line->
            val column=if(direction==TextDirection.VERTICAL_LR) i*step else bounds.width()-cell-i*step
            val runs=runs(line,orientation)
            val length=runs.sumOf {if(it.upright) cell.toDouble() else layout(it.text,paint).width.toDouble()}.toFloat()
            var y=offset(length,bounds.height())
            for(run in runs) {
                val shaped=layout(if(run.upright && run.text.length==1) punctuation[run.text[0]]?.toString() ?: run.text else run.text,paint)
                canvas.save()
                if(run.upright) {canvas.translate(column+(cell-shaped.width)/2,y+(cell-shaped.height)/2);shaped.draw(canvas);y+=cell}
                else {canvas.translate(column+(cell+shaped.height)/2,y);canvas.rotate(90f);shaped.draw(canvas);y+=shaped.width}
                canvas.restore()
            }
        }
    }
    fun drawLabel(canvas: Canvas,text: String,paint: Paint,rect: RectF,direction: TextDirection=uiDirection()) {
        if(rect.width()<=0 || rect.height()<=0 || text.isEmpty()) return
        val label=if(direction==TextDirection.HORIZONTAL) text else text.trim().replace(Regex("\\s+"),"\n")
        val bounds=bounds(label,paint,direction,GlyphOrientation.MIXED,1f)
        val scale=minOf(1f,rect.width()/bounds.width().coerceAtLeast(1f),rect.height()/bounds.height().coerceAtLeast(1f))
        canvas.save();canvas.translate(rect.centerX()-bounds.width()*scale/2,rect.centerY()-bounds.height()*scale/2)
        canvas.scale(scale,scale);draw(canvas,label,paint,direction,GlyphOrientation.MIXED);canvas.restore()
    }
}
