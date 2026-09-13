/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.app.Activity
import android.app.AlertDialog
import android.graphics.*
import android.text.*
import android.util.TypedValue
import android.view.*
import android.widget.*
import org.json.JSONObject

data class TextSettings(val text: String="",val size: Float=32f,val font: Int=0,val bold: Boolean=false,val italic: Boolean=false,
    val underline: Boolean=false,val strike: Boolean=false,val box: Boolean=false,val alignment: Int=0,val spacing: Float=1f,val direction: TextDirection=VerticalText.uiDirection(),val glyphOrientation: GlyphOrientation=GlyphOrientation.MIXED) {
    fun json()=JSONObject().apply {
        put("text",text.take(8192));put("size",size.toDouble());put("font",font);put("bold",bold);put("italic",italic)
        put("direction",direction.name);put("glyph_orientation",glyphOrientation.name)
        put("underline",underline);put("strike",strike);put("box",box);put("alignment",alignment);put("spacing",spacing.toDouble())
    }
    companion object {
        fun read(o: JSONObject?) = if (o==null) TextSettings() else TextSettings(o.optString("text"),o.optDouble("size",32.0).toFloat(),o.optInt("font"),o.optBoolean("bold"),o.optBoolean("italic"),
            o.optBoolean("underline"),o.optBoolean("strike"),o.optBoolean("box"),o.optInt("alignment").coerceIn(0,2),o.optDouble("spacing",1.0).toFloat(),TextDirection.values().firstOrNull {it.name==o.optString("direction")} ?: TextDirection.HORIZONTAL,
            GlyphOrientation.values().firstOrNull {it.name==o.optString("glyph_orientation")} ?: GlyphOrientation.MIXED)
    }
}

class TextStyleDialog(private val activity: Activity,private val initial: TextSettings,private val foreground: Int,private val background: Int,
    private val commit: (TextSettings,Typeface) -> Boolean) {
    fun show(): AlertDialog {
        fun dp(n: Int)=(n*activity.resources.displayMetrics.density+.5f).toInt()
        fun label(text: String)=TextView(activity).apply { this.text=text;textSize=13f }
        val body=LinearLayout(activity).apply { orientation=LinearLayout.VERTICAL;setPadding(dp(16),dp(6),dp(16),dp(10)) }
        val input=EditText(activity).apply { tag="text_content";hint=ui(R.string.ui_type_text);setText(initial.text);inputType=InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_MULTI_LINE;filters=arrayOf(InputFilter.LengthFilter(8192));minLines=2 }
        body.addView(input)
        val catalog=FontCatalog(activity)
        val font=Spinner(activity).apply { tag="text_font";contentDescription=ui(R.string.ui_font_family);adapter=catalog.adapter();setSelection(initial.font.coerceIn(catalog.fonts.indices)) }
        body.addView(label(ui(R.string.ui_font)));body.addView(font,LinearLayout.LayoutParams(-1,dp(48)))
        fun number(value: String,tagName: String)=EditText(activity).apply { tag=tagName;inputType=InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_FLAG_DECIMAL;setText(value);setSelectAllOnFocus(true);isSingleLine=true }
        val size=number(initial.size.toInt().toString(),"text_size")
        val spacing=number((initial.spacing*100).toInt().toString(),"text_spacing")
        val sizes=LinearLayout(activity)
        listOf(ui(R.string.ui_size_pixels) to size,ui(R.string.ui_line_spacing) to spacing).forEach { (name,field) ->
            val col=LinearLayout(activity).apply { orientation=LinearLayout.VERTICAL;addView(label(name));addView(field) }
            sizes.addView(col,LinearLayout.LayoutParams(0,-2,1f))
        };body.addView(sizes)
        fun check(text: String,tagName: String,value: Boolean)=CheckBox(activity).apply { this.text=text;tag=tagName;isChecked=value }
        val bold=check(ui(R.string.ui_bold),"text_bold",initial.bold);val italic=check(ui(R.string.ui_italic),"text_italic",initial.italic)
        val underline=check(ui(R.string.ui_underline),"text_underline",initial.underline);val strike=check(ui(R.string.ui_strikethrough),"text_strike",initial.strike)
        listOf(bold,italic,underline,strike).chunked(2).forEach { items ->
            val row=LinearLayout(activity);items.forEach { row.addView(it,LinearLayout.LayoutParams(0,dp(48),1f)) };body.addView(row)
        }
        val align=Spinner(activity).apply { tag="text_alignment";contentDescription=ui(R.string.ui_text_alignment);adapter=ArrayAdapter(activity,android.R.layout.simple_spinner_dropdown_item,arrayOf(ui(R.string.ui_left_aligned),ui(R.string.ui_centred),ui(R.string.ui_right_aligned)));setSelection(initial.alignment) }
        body.addView(align,LinearLayout.LayoutParams(-1,dp(48)))
        val direction=Spinner(activity).apply {tag="text_direction";contentDescription=ui(R.string.ui_text_direction23)
            adapter=ArrayAdapter(activity,android.R.layout.simple_spinner_dropdown_item,arrayOf(ui(R.string.ui_horizontal23),ui(R.string.ui_vertical_rl23),ui(R.string.ui_vertical_lr23)));setSelection(initial.direction.ordinal)}
        body.addView(label(ui(R.string.ui_text_direction23)));body.addView(direction,LinearLayout.LayoutParams(-1,dp(48)))
        val glyphs=Spinner(activity).apply {tag="text_glyph_orientation";contentDescription=ui(R.string.ui_vertical_letters23)
            adapter=ArrayAdapter(activity,android.R.layout.simple_spinner_dropdown_item,arrayOf(ui(R.string.ui_vertical_mixed23),ui(R.string.ui_vertical_sideways23),ui(R.string.ui_vertical_upright23)));setSelection(initial.glyphOrientation.ordinal)}
        body.addView(label(ui(R.string.ui_vertical_letters23)));body.addView(glyphs,LinearLayout.LayoutParams(-1,dp(48)))
        body.addView(label(ui(R.string.ui_vertical_hint23)))
        val box=check(ui(R.string.ui_fill_text_box_with_bg_colour),"text_box",initial.box);body.addView(box)
        body.addView(label(ui(R.string.ui_preview)))
        val preview=TextPreview(activity).apply {tag="text_preview"}
        body.addView(preview,LinearLayout.LayoutParams(-1,dp(180)))
        val credit=Button(activity).apply { text=ui(R.string.ui_font_licences);tag="font_licences";isAllCaps=false;setOnClickListener { LegalInfo.showAsset(activity,ui(R.string.ui_font_licences),"legal/FONT_NOTICES.txt") } }
        body.addView(credit,LinearLayout.LayoutParams(-1,dp(48)))
        fun style()=(if (bold.isChecked) Typeface.BOLD else 0) or (if (italic.isChecked) Typeface.ITALIC else 0)
        fun update() {
            val face=catalog.faceForText(font.selectedItemPosition,input.text.toString(),style());input.typeface=face;preview.face=face
            preview.value=input.text.toString().ifBlank { ui(R.string.ui_aa_bb_0123) }
            preview.pixels=(uiNumber(size.text.toString())?.toFloat() ?: 32f).coerceIn(1f,1024f)
            preview.foregroundColour=foreground;preview.backgroundColour=background
            preview.underline=underline.isChecked;preview.strike=strike.isChecked;preview.opaque=box.isChecked
            preview.direction=TextDirection.values()[direction.selectedItemPosition]
            preview.orientation=GlyphOrientation.values()[glyphs.selectedItemPosition]
            preview.spacing=((uiNumber(spacing.text.toString())?.toFloat() ?: 100f)/100).coerceIn(.5f,3f)
            preview.align=arrayOf(Paint.Align.LEFT,Paint.Align.CENTER,Paint.Align.RIGHT)[align.selectedItemPosition]
            glyphs.visibility=if(preview.direction==TextDirection.HORIZONTAL) View.GONE else View.VISIBLE
            val names=if(preview.direction==TextDirection.HORIZONTAL) arrayOf(ui(R.string.ui_left_aligned),ui(R.string.ui_centred),ui(R.string.ui_right_aligned))
                else arrayOf(ui(R.string.ui_top23),ui(R.string.ui_centred),ui(R.string.ui_bottom23))
            val old=align.selectedItemPosition
            if(align.getItemAtPosition(0)!=names[0]) {align.adapter=ArrayAdapter(activity,android.R.layout.simple_spinner_dropdown_item,names);align.setSelection(old)}
            preview.invalidate()
        }
        val watcher=object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?,start: Int,count: Int,after: Int)=Unit
            override fun onTextChanged(s: CharSequence?,start: Int,before: Int,count: Int) { update() }
            override fun afterTextChanged(s: Editable?)=Unit
        }
        listOf(input,size,spacing).forEach { it.addTextChangedListener(watcher) }
        listOf(bold,italic,underline,strike,box).forEach { it.setOnCheckedChangeListener { _,_ -> update() } }
        val selected=object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?,view: View?,position: Int,id: Long) { update() }
            override fun onNothingSelected(parent: AdapterView<*>?)=Unit
        };font.onItemSelectedListener=selected;align.onItemSelectedListener=selected;direction.onItemSelectedListener=selected;glyphs.onItemSelectedListener=selected
        val dialog=AlertDialog.Builder(activity).setTitle(ui(R.string.ui_place_text)).setView(ScrollView(activity).apply { addView(body) })
            .setNegativeButton(ui(R.string.ui_cancel),null).setPositiveButton(ui(R.string.ui_add_text),null).create()
        dialog.setOnShowListener { dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
            val pixels=uiNumber(size.text.toString())?.toFloat();val percent=uiNumber(spacing.text.toString())?.toFloat()
            when {
                pixels==null || pixels !in 1f..1024f -> size.error=ui(R.string.ui_use_1_1024_pixels)
                percent==null || percent !in 50f..300f -> spacing.error=ui(R.string.ui_use_50_300)
                else -> {
                    val settings=TextSettings(input.text.toString(),pixels,font.selectedItemPosition,bold.isChecked,italic.isChecked,underline.isChecked,strike.isChecked,box.isChecked,align.selectedItemPosition,percent/100,TextDirection.values()[direction.selectedItemPosition],GlyphOrientation.values()[glyphs.selectedItemPosition])
                    if (commit(settings,catalog.faceForText(settings.font,settings.text,style()))) dialog.dismiss()
                }
            }
        } }
        update();dialog.show();return dialog
    }
}

internal class TextPreview(context: android.content.Context): View(context) {
    var value="";var face: Typeface=Typeface.DEFAULT;var pixels=32f
    var foregroundColour=Color.BLACK;var backgroundColour=Color.WHITE;var opaque=false;var underline=false;var strike=false
    var direction=TextDirection.HORIZONTAL;var orientation=GlyphOrientation.MIXED;var spacing=1f;var align=Paint.Align.LEFT
    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas);canvas.drawColor(EditorColours.surfaceContainer)
        val p=Paint(Paint.ANTI_ALIAS_FLAG).apply {color=foregroundColour;textSize=pixels;typeface=face;isUnderlineText=underline;isStrikeThruText=strike}
        val bounds=VerticalText.bounds(value,p,direction,orientation,spacing)
        val margin=8*resources.displayMetrics.density
        val scale=minOf(1f,(width-2*margin)/bounds.width().coerceAtLeast(1f),(height-2*margin)/bounds.height().coerceAtLeast(1f)).coerceAtLeast(.0001f)
        canvas.save();canvas.translate(margin,margin);canvas.scale(scale,scale)
        if(opaque) canvas.drawRect(bounds,Paint().apply {color=backgroundColour})
        VerticalText.draw(canvas,value,p,direction,orientation,spacing,align);canvas.restore()
    }
}
