/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later.
 * Colour controls and generated spectrum/wheel geometry.
 */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.graphics.*
import android.graphics.drawable.GradientDrawable
import android.text.Editable
import android.text.InputType
import android.text.TextWatcher
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.core.graphics.ColorUtils
import java.util.Locale
import kotlin.math.*

class ColourValue(initial: Int) {
    var colour = initial or Color.BLACK; private set
    val hsv = FloatArray(3)
    private val hslState = FloatArray(3)
    val hsl get() = hslState.copyOf()
    init { Color.colorToHSV(initial, hsv); ColorUtils.colorToHSL(initial, hslState) }
    fun rgb(value: Int) {
        val hue = hsv[0]; colour = value or Color.BLACK; Color.colorToHSV(colour, hsv); ColorUtils.colorToHSL(colour, hslState)
        if (hsv[1] == 0f) { hsv[0] = hue; hslState[0] = hue }
    }
    fun hsv(h: Float, s: Float, v: Float) {
        hsv[0] = h % 360f; hsv[1] = s; hsv[2] = v
        colour = Color.HSVToColor(hsv)
        ColorUtils.colorToHSL(colour, hslState); hslState[0] = hsv[0]
        if (v == 0f) hslState[1] = s
    }
    fun hsl(h: Float, s: Float, l: Float) {
        hslState[0] = h % 360f; hslState[1] = s; hslState[2] = l
        colour = ColorUtils.HSLToColor(hslState)
        Color.colorToHSV(colour, hsv); hsv[0] = hslState[0]
        if (l == 0f) hsv[1] = s
    }
}

class AdvancedColourDialog(private val activity: Activity, initial: Int, private val background: Boolean, private val commit: (Int) -> Unit) {
    val value = ColourValue(initial or Color.BLACK)
    private val prefs = activity.getSharedPreferences("classic-custom-colours", Context.MODE_PRIVATE)
    private val fields = linkedMapOf<String, EditText>()
    private val custom = mutableListOf<View>()
    private lateinit var surface: ColourSurface
    private lateinit var sample: View
    private val defaults=listOf(ui(R.string.ui_pale_violet) to 0xff5b67ff.toInt(),ui(R.string.ui_gold) to 0xffffd700.toInt(),ui(R.string.ui_silver) to 0xffc0c0c0.toInt(),ui(R.string.ui_copper) to 0xffb87333.toInt())
    private fun customColour(index: Int) = prefs.getInt("colour_$index",defaults.getOrNull(index)?.second ?: Color.WHITE) or Color.BLACK
    private fun customLabel(index: Int,colour: Int): String {
        val name=defaults.getOrNull(index)?.takeIf { it.second==colour }?.first ?: ui(R.string.ui_custom_colour, index+1)
        return "$name: ${String.format(Locale.ROOT,"#%06X",colour and 0xffffff)}"
    }
    private var syncing = false
    private lateinit var honeycomb: HoneycombPalette
    private fun dp(n: Int) = (activity.resources.displayMetrics.density * n + .5f).toInt()
    private fun label(text: String) = TextView(activity).apply { this.text = text; textSize = 12f }
    private fun swatchBackground(view: View, colour: Int) {
        view.background = GradientDrawable().apply { setColor(colour); setStroke(dp(1), 0xff8e9498.toInt()) }
    }
    private fun column() = LinearLayout(activity).apply { orientation = LinearLayout.VERTICAL }
    private fun button(text: String, tag: String, action: () -> Unit) = Button(activity).apply {
        this.text = text; this.tag = tag; isAllCaps = false; textSize = 12f; setOnClickListener { action() }
    }
    fun show(): AlertDialog {
        val body = column().apply { setPadding(dp(16), dp(8), dp(16), dp(12)) }
        val tabs = LinearLayout(activity)
        val palette = column().apply { tag = "colour_palette" }
        surface = ColourSurface(activity, value).apply { tag = "colour_surface"; changed = { sync() }; visibility = View.GONE }
        val advanced = column().apply { tag = "colour_advanced"; visibility = View.GONE }
        honeycomb = HoneycombPalette(activity, value) { sync() }.apply { tag = "colour_honeycomb"; visibility = View.GONE }
        fun selectMode(mode: Int) {
            palette.visibility = if (mode == 0) View.VISIBLE else View.GONE
            honeycomb.visibility = if (mode == 3) View.VISIBLE else View.GONE
            advanced.visibility = if (mode == 1 || mode == 2) View.VISIBLE else View.GONE
            surface.visibility = advanced.visibility
            surface.wheel = mode == 2; surface.invalidate()
            surface.contentDescription = if (mode == 2) ui(R.string.ui_hue_and_saturation_wheel_value_slider_on_the) else ui(R.string.ui_hue_and_saturation_spectrum_lightness_slider_on_the)
            for (i in 0 until tabs.childCount) tabs.getChildAt(i).isSelected = i == when (mode) { 0 -> 0; 3 -> 1; else -> 2 }
        }
        listOf(Triple(ui(R.string.ui_palette), "colour_mode_0", 0), Triple(ui(R.string.ui_honeycomb), "colour_mode_3", 3), Triple(ui(R.string.ui_advanced), "colour_advanced_tab", 1)).forEach { (name, tag, mode) ->
            tabs.addView(button(name, tag) { selectMode(mode) }, LinearLayout.LayoutParams(0, dp(44), 1f))
        }
        body.addView(tabs)
        val advancedTabs = LinearLayout(activity)
        listOf(ui(R.string.ui_spectrum), ui(R.string.ui_wheel)).forEachIndexed { i, name ->
            advancedTabs.addView(button(name, "colour_mode_${i + 1}") { selectMode(i + 1) }, LinearLayout.LayoutParams(0, dp(44), 1f))
        }
        advanced.addView(advancedTabs)
        advanced.addView(surface, LinearLayout.LayoutParams(-1, dp(190)))
        palette.addView(label(ui(R.string.ui_basic_colours)))
        val basics = intArrayOf(Color.BLACK, 0xff808080.toInt(),0xff800000.toInt(),0xff808000.toInt(),0xff008000.toInt(),0xff008080.toInt(),0xff000080.toInt(),0xff800080.toInt(),
            Color.WHITE,0xffc0c0c0.toInt(),Color.RED,Color.YELLOW,Color.GREEN,Color.CYAN,Color.BLUE,Color.MAGENTA) +
            (0 until 32).map { Color.HSVToColor(floatArrayOf((it % 8) * 45f, if (it < 16) .5f else 1f, if (it % 16 < 8) 1f else .65f)) }.toIntArray()
        fun swatch(colour: Int, tagName: String, select: () -> Int): View = View(activity).apply {
            tag = tagName; contentDescription = ui(R.string.ui_colour, String.format(Locale.ROOT, "#%06X", colour and 0xffffff))
            swatchBackground(this, colour); isFocusable = true; isClickable = true
            setOnClickListener { value.rgb(select()); sync() }
        }
        basics.toList().chunked(8).forEachIndexed { rowIndex, row ->
            val line = LinearLayout(activity)
            row.forEachIndexed { i, c -> line.addView(swatch(c, "basic_colour_${rowIndex * 8 + i}") { c }, LinearLayout.LayoutParams(0, dp(28), 1f).apply { setMargins(dp(1), dp(1), dp(1), dp(1)) }) }
            palette.addView(line)
        }
        palette.addView(label(ui(R.string.ui_custom_colours_hold_a_swatch_to_replace_it)))
        repeat(2) { row ->
            val line = LinearLayout(activity)
            repeat(8) { col ->
                val index = row * 8 + col
                val view = swatch(customColour(index), "custom_colour_$index") { customColour(index) }
                view.contentDescription=customLabel(index,customColour(index))
                view.setOnLongClickListener { saveCustom(index); true }; custom.add(view)
                line.addView(view, LinearLayout.LayoutParams(0, dp(28), 1f).apply { setMargins(dp(1), dp(1), dp(1), dp(1)) })
            }; palette.addView(line)
        }
        palette.addView(button(ui(R.string.ui_add_to_custom_colours), "add_custom_colour") {
            val next = prefs.getInt("next", 4); saveCustom(next); prefs.edit().putInt("next", (next + 1) % 16).apply()
        }, LinearLayout.LayoutParams(-1, dp(44)))
        body.addView(palette); body.addView(honeycomb, LinearLayout.LayoutParams(-1, dp(278)))
        body.addView(advanced)
        val preview = LinearLayout(activity).apply { gravity = Gravity.CENTER_VERTICAL }
        preview.addView(label(ui(R.string.ui_new_colour)), LinearLayout.LayoutParams(0, dp(32), 1f))
        sample = object : View(activity) {
            override fun onDraw(canvas: Canvas) {
                val p = Paint()
                p.color = value.colour; canvas.drawRect(0f, 0f, width.toFloat(), height.toFloat(), p)
            }
        }.apply { tag = "new_colour_preview" }
        preview.addView(sample, LinearLayout.LayoutParams(dp(88), dp(28))); body.addView(preview)
        fun field(key: String, hintText: String, max: Int): LinearLayout {
            val wrap = column(); wrap.addView(label(hintText))
            val edit = EditText(activity).apply {
                tag = "colour_$key"; contentDescription = hintText; textSize = 13f
                inputType = if (key == "hex") InputType.TYPE_CLASS_TEXT else InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_FLAG_DECIMAL
                isSingleLine = true; setSelectAllOnFocus(true)
                addTextChangedListener(object : TextWatcher {
                    override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) = Unit
                    override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                        if (syncing) return
                        if (key != "hex") {
                            val n = s.toString().toFloatOrNull()
                            if (n == null || n !in 0f..max.toFloat()) { error = "0–$max"; return }
                        }
                        readFields(key)
                    }
                    override fun afterTextChanged(s: Editable?) = Unit
                })
            }; fields[key] = edit; wrap.addView(edit); return wrap
        }
        advanced.addView(field("hex", ui(R.string.ui_hex_rrggbb), 0))
        listOf(listOf(Triple("r", "R · 0–255", 255),Triple("g", "G · 0–255", 255),Triple("b", "B · 0–255", 255)),
            listOf(Triple("h", "HSV H · 0–360°", 360),Triple("s", "HSV S · 0–100%", 100),Triple("v", "HSV V · 0–100%", 100)),
            listOf(Triple("hl", "HSL H · 0–360°", 360),Triple("sl", "HSL S · 0–100%", 100),Triple("l", "HSL L · 0–100%", 100))).forEach { group ->
            val row = LinearLayout(activity)
            group.forEach { (key, label, max) -> row.addView(field(key, label, max), LinearLayout.LayoutParams(0, -2, 1f)) }
            advanced.addView(row)
        }
        val scroll = ScrollView(activity).apply { addView(body) }
        val dialog = AlertDialog.Builder(activity).setTitle(if (background) ui(R.string.ui_background_colour) else ui(R.string.ui_foreground_colour)).setView(scroll)
            .setNegativeButton(ui(R.string.ui_cancel), null).setPositiveButton(ui(R.string.ui_use_colour), null).create()
        dialog.setOnShowListener { dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
            if (fields.values.any { it.error != null }) return@setOnClickListener
            commit(value.colour or Color.BLACK); dialog.dismiss()
        } }
        sync(); dialog.show(); return dialog
    }
    private fun saveCustom(index: Int) {
        prefs.edit().putInt("colour_$index", value.colour).apply()
        swatchBackground(custom[index], value.colour)
        custom[index].contentDescription = customLabel(index,value.colour)
    }
    private fun readFields(key: String) {
        fun number(name: String, max: Float): Float? = fields[name]?.text.toString().toFloatOrNull()?.takeIf { it in 0f..max }
        try {
            when (key) {
                "hex" -> {
                    val text = fields[key]!!.text.toString().trim()
                    if (!text.matches(Regex("#[0-9a-fA-F]{6}"))) { fields[key]!!.error = ui(R.string.ui_use_rrggbb); return }
                    value.rgb(Color.parseColor(text))
                }
                "r", "g", "b" -> value.rgb(Color.rgb( (number("r",255f) ?: return).toInt(),(number("g",255f) ?: return).toInt(),(number("b",255f) ?: return).toInt()))
                "h", "s", "v" -> value.hsv(number("h",360f) ?: return,(number("s",100f) ?: return) / 100,(number("v",100f) ?: return) / 100)
                "hl", "sl", "l" -> value.hsl(number("hl",360f) ?: return,(number("sl",100f) ?: return) / 100,(number("l",100f) ?: return) / 100)
            }
            fields[key]?.error = null; sync(key)
        } catch (_: IllegalArgumentException) { fields[key]?.error = ui(R.string.ui_invalid_colour) }
    }
    private fun sync(except: String? = null) {
        syncing = true
        val c = value.colour; val hsl = value.hsl
        val numbers = mapOf("r" to Color.red(c).toFloat(),"g" to Color.green(c).toFloat(),"b" to Color.blue(c).toFloat(),
            "h" to value.hsv[0],"s" to value.hsv[1] * 100,"v" to value.hsv[2] * 100,"hl" to hsl[0],"sl" to hsl[1] * 100,"l" to hsl[2] * 100)
        fields.forEach { (key, field) -> if (key != except) {
            field.setText(if (key == "hex") String.format(Locale.ROOT, "#%06X", c and 0xffffff) else String.format(Locale.ROOT, if (key in listOf("r","g","b","a")) "%.0f" else "%.2f", numbers[key]))
            field.error = null
        } }
        sample.invalidate(); surface.invalidate(); honeycomb.invalidateSelection(); syncing = false
    }
}

/** Two advanced graphical selectors: classic H/S spectrum + L, and HSV wheel + V. */
class ColourSurface(context: Context, private val colour: ColourValue) : View(context) {
    var wheel = false
    var changed: () -> Unit = {}
    private var spectrum: Bitmap? = null
    private var brightnessDrag = false
    init { isFocusable = true; isClickable = true }
    private fun mainRect() = RectF(4f, 4f, width - 42 * resources.displayMetrics.density, height - 4f)
    override fun onDraw(c: Canvas) {
        val r = mainRect(); if (r.width() <= 0 || r.height() <= 0) return
        val p = Paint(Paint.ANTI_ALIAS_FLAG)
        var px: Float; var py: Float
        val high: Int
        if (wheel) {
            val radius = min(r.width(),r.height()) / 2
            val colours = (0..6).map { Color.HSVToColor(floatArrayOf(it * 60f,1f,1f)) }.toIntArray()
            p.shader = ComposeShader(SweepGradient(r.centerX(),r.centerY(),colours,null),RadialGradient(r.centerX(),r.centerY(),radius,intArrayOf(Color.WHITE,0x00ffffff),null,Shader.TileMode.CLAMP),PorterDuff.Mode.SRC_OVER)
            c.drawCircle(r.centerX(),r.centerY(),radius,p); p.shader = null
            val angle = Math.toRadians(colour.hsv[0].toDouble())
            px = r.centerX() + cos(angle).toFloat() * radius * colour.hsv[1]; py = r.centerY() + sin(angle).toFloat() * radius * colour.hsv[1]
            high = Color.HSVToColor(floatArrayOf(colour.hsv[0],colour.hsv[1],1f))
        } else {
            if (spectrum == null) {
                val pixels = IntArray(240 * 160)
                for (y in 0 until 160) for (x in 0 until 240) pixels[y * 240 + x] = ColorUtils.HSLToColor(floatArrayOf(x / 239f * 359.99f,1 - y / 159f,.5f))
                spectrum = Bitmap.createBitmap(pixels,240,160,Bitmap.Config.ARGB_8888)
            }
            c.drawBitmap(spectrum!!,null,r,null)
            val hsl = colour.hsl; px = r.left + hsl[0] / 360 * r.width(); py = r.top + (1 - hsl[1]) * r.height()
            high = ColorUtils.HSLToColor(floatArrayOf(hsl[0],hsl[1],.5f))
        }
        val bar = RectF(r.right + 12 * resources.displayMetrics.density,r.top,width - 6f,r.bottom)
        p.shader = if (wheel) LinearGradient(0f,bar.top,0f,bar.bottom,high,Color.BLACK,Shader.TileMode.CLAMP)
            else LinearGradient(0f,bar.top,0f,bar.bottom,intArrayOf(Color.WHITE,high,Color.BLACK),null,Shader.TileMode.CLAMP)
        c.drawRect(bar,p); p.shader = null
        val y = bar.top + (1 - if (wheel) colour.hsv[2] else colour.hsl[2]) * bar.height()
        p.style = Paint.Style.STROKE; p.strokeWidth = 4f; p.color = Color.BLACK
        c.drawCircle(px,py,8f,p); c.drawLine(bar.left - 3,y,bar.right + 3,y,p)
        p.strokeWidth = 2f; p.color = Color.WHITE; c.drawCircle(px,py,8f,p); c.drawLine(bar.left - 3,y,bar.right + 3,y,p)
    }
    override fun onTouchEvent(event: MotionEvent): Boolean {
        if (event.actionMasked == MotionEvent.ACTION_DOWN) { parent?.requestDisallowInterceptTouchEvent(true); brightnessDrag = event.x > mainRect().right }
        if (event.actionMasked in listOf(MotionEvent.ACTION_DOWN,MotionEvent.ACTION_MOVE,MotionEvent.ACTION_UP)) {
            val r = mainRect(); val vertical = (1 - (event.y - r.top) / r.height()).coerceIn(0f,1f)
            if (wheel) {
                if (brightnessDrag) colour.hsv(colour.hsv[0],colour.hsv[1],vertical)
                else {
                    val dx = event.x - r.centerX(); val dy = event.y - r.centerY()
                    colour.hsv(((atan2(dy,dx) * 180 / PI + 360) % 360).toFloat(),(hypot(dx,dy) / (min(r.width(),r.height()) / 2)).coerceIn(0f,1f),colour.hsv[2])
                }
            } else {
                val hsl = colour.hsl
                if (brightnessDrag) colour.hsl(hsl[0],hsl[1],vertical)
                else colour.hsl(((event.x - r.left) / r.width()).coerceIn(0f,.99999f) * 360,vertical,hsl[2])
            }
            invalidate(); changed()
            if (event.actionMasked == MotionEvent.ACTION_UP) { parent?.requestDisallowInterceptTouchEvent(false); performClick() }
        }
        return true
    }
    override fun performClick(): Boolean { super.performClick(); return true }
}
