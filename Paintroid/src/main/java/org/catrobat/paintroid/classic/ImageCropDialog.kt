/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.graphics.*
import android.text.Editable
import android.text.InputType
import android.text.TextWatcher
import android.view.MotionEvent
import android.view.View
import android.widget.*
import java.util.Locale
import kotlin.math.min

class CropPreview(context: Context) : View(context) {
    var bitmap: Bitmap? = null
    var crop: CropOverlay? = null
    var changed: (Rect) -> Unit = {}
    private var scale = 1f; private var x = 0f; private var y = 0f
    init { isFocusable = true; isClickable = true; contentDescription = "Crop preview. Drag an edge or corner; drag inside to move the crop." }
    private fun position() {
        val size = crop?.image ?: return; val pad = 14 * resources.displayMetrics.density
        scale = min((width-2*pad).coerceAtLeast(1f)/size.width,(height-2*pad).coerceAtLeast(1f)/size.height)
        x = (width-size.width*scale)/2; y = (height-size.height*scale)/2
    }
    override fun onDraw(canvas: Canvas) {
        canvas.drawColor(0xffaeb7c0.toInt()); val c = crop ?: return; position()
        canvas.save(); canvas.translate(x,y); canvas.scale(scale,scale)
        canvas.drawRect(0f,0f,c.image.width.toFloat(),c.image.height.toFloat(),Paint().apply { color = Color.WHITE })
        bitmap?.let { canvas.drawBitmap(it,null,Rect(0,0,c.image.width,c.image.height),Paint(Paint.FILTER_BITMAP_FLAG)) }
        c.draw(canvas,scale,resources.displayMetrics.density); canvas.restore()
    }
    override fun onTouchEvent(event: MotionEvent): Boolean {
        val c = crop ?: return false; position(); val p = PointF((event.x-x)/scale,(event.y-y)/scale)
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> { parent?.requestDisallowInterceptTouchEvent(true); c.begin(p,24*resources.displayMetrics.density/scale) }
            MotionEvent.ACTION_MOVE -> c.move(p)
            MotionEvent.ACTION_UP -> { c.move(p); c.end(); parent?.requestDisallowInterceptTouchEvent(false); performClick() }
            MotionEvent.ACTION_CANCEL -> { c.end(true); parent?.requestDisallowInterceptTouchEvent(false) }
        }
        changed(Rect(c.rect)); invalidate(); return true
    }
    override fun performClick(): Boolean { super.performClick(); return true }
}

/** Numeric trim margins and touch preview; batch values are relative to each original. */
class ImageCropDialog(private val activity: Activity, private val images: List<AssemblyImage>,
    private val previewBitmap: (AssemblyImage) -> Bitmap?, private val apply: (Map<String,Rect>) -> Unit) {
    fun show(): AlertDialog {
        require(images.isNotEmpty())
        fun dp(n: Int) = (activity.resources.displayMetrics.density*n+.5f).toInt()
        val body = LinearLayout(activity).apply { orientation = LinearLayout.VERTICAL; setPadding(dp(16),dp(4),dp(16),dp(8)) }
        val status = TextView(activity).apply { tag = "crop_status"; textSize = 13f }
        var reference = images.first(); var percent = false; var syncing = false
        val selected = images.filter { images.size == 1 || it.attachment == null }.map { it.id }.toMutableSet().apply { if (isEmpty()) addAll(images.map { it.id }) }
        val preview = CropPreview(activity).apply { tag = "crop_preview" }
        if (images.size > 1) body.addView(Spinner(activity).apply {
            tag = "crop_preview_image"; contentDescription = "Image shown in crop preview"
            adapter = ArrayAdapter(activity,android.R.layout.simple_spinner_dropdown_item,images.map { it.name })
            onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
                override fun onNothingSelected(parent: AdapterView<*>?) = Unit
                override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) { reference = images[position]; post { status.performClick() } }
            }
        })
        body.addView(preview,LinearLayout.LayoutParams(-1,dp(200)))
        body.addView(TextView(activity).apply { text = "Trim from the original edges. Drag the handles or enter amounts below. Source files stay unchanged."; textSize = 13f })
        val unitRow = RadioGroup(activity).apply { orientation = LinearLayout.HORIZONTAL }
        val fields = linkedMapOf<String,EditText>()
        fun margins(): CropMargins? {
            val n = fields.values.map { it.text.toString().toDoubleOrNull() ?: return null }
            return CropMargins(n[0],n[1],n[2],n[3],percent)
        }
        fun displayValues(r: Rect) {
            syncing = true
            val values = listOf(r.left,r.top,reference.dimensions.width-r.right,reference.dimensions.height-r.bottom)
            fields.values.forEachIndexed { i, field ->
                val n = if (percent) values[i]*100.0 / if (i%2 == 0) reference.dimensions.width else reference.dimensions.height else values[i].toDouble()
                field.setText(String.format(Locale.ROOT,"%.4f",n).trimEnd('0').trimEnd('.'))
            }; syncing = false
        }
        fun refresh(updatePreview: Boolean = true) {
            if (syncing) return
            try {
                val m = margins() ?: throw IllegalArgumentException("Enter a trim amount for every edge.")
                val crop = m.rect(reference.dimensions)
                if (updatePreview) { preview.bitmap = previewBitmap(reference); preview.crop = CropOverlay(reference.dimensions,crop); preview.invalidate() }
                val count = images.count { it.id in selected }
                images.filter { it.id in selected }.forEach { m.rect(it.dimensions) }
                status.text = "Preview: ${crop.width()} × ${crop.height()} px\nApply to $count image${if (count == 1) "" else "s"}. Cropping placed images repositions their attachments."
            } catch (error: IllegalArgumentException) { status.text = error.message }
        }
        listOf("Pixels", "Percent").forEachIndexed { index, name ->
            unitRow.addView(RadioButton(activity).apply {
                text = name; id = View.generateViewId(); tag = "crop_${if (index == 0) "pixels" else "percent"}"; isChecked = index == 0
                setOnClickListener {
                    unitRow.check(id)
                    val previous = try { margins()?.rect(reference.dimensions) } catch (_: IllegalArgumentException) { null }
                    percent = index == 1
                    if (previous != null) displayValues(previous)
                    fields.forEach { (name,field) -> field.contentDescription = "$name trim in ${if (percent) "percent" else "pixels"}" }
                    refresh()
                }
            },LinearLayout.LayoutParams(0,-2,1f))
        }; body.addView(unitRow)
        listOf("Left","Top","Right","Bottom").chunked(2).forEach { pair ->
            val row = LinearLayout(activity)
            pair.forEach { name ->
                val column = LinearLayout(activity).apply { orientation = LinearLayout.VERTICAL }
                column.addView(TextView(activity).apply { text = name; textSize = 13f })
                val field = EditText(activity).apply {
                    tag = "crop_${name.lowercase(Locale.ROOT)}"; contentDescription = "$name trim in pixels"; inputType = InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_FLAG_DECIMAL; isSingleLine = true; setSelectAllOnFocus(true)
                    addTextChangedListener(object : TextWatcher {
                        override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) = Unit
                        override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) { if (fields.size == 4) refresh() }
                        override fun afterTextChanged(s: Editable?) = Unit
                    })
                }; fields[name] = field; column.addView(field); row.addView(column,LinearLayout.LayoutParams(0,-2,1f))
            }; body.addView(row)
        }
        body.addView(Button(activity).apply { text = "Reset crop"; isAllCaps = false; tag = "crop_reset"; setOnClickListener { displayValues(Rect(0,0,reference.dimensions.width,reference.dimensions.height)); refresh() } })
        body.addView(status); status.setOnClickListener { refresh() }
        if (images.size > 1) {
            body.addView(TextView(activity).apply { text = "Apply to these images" })
            val checks = images.map { item -> CheckBox(activity).apply {
                text = item.name; tag = "crop_include_${item.id}"; isChecked = item.id in selected
                setOnCheckedChangeListener { _, checked -> if (checked) selected.add(item.id) else selected.remove(item.id); refresh() }
                body.addView(this)
            } }
            val actions = LinearLayout(activity)
            listOf("All" to true,"None" to false).forEach { (label,checked) -> actions.addView(Button(activity).apply {
                text = label; isAllCaps = false; tag = "crop_${label.lowercase(Locale.ROOT)}"; setOnClickListener { checks.forEach { it.isChecked = checked } }
            },LinearLayout.LayoutParams(0,-2,1f)) }; body.addView(actions)
        }
        preview.changed = { rect -> displayValues(rect); refresh(false) }
        displayValues(if (images.size == 1) reference.crop else Rect(0,0,reference.dimensions.width,reference.dimensions.height)); refresh()
        val dialog = AlertDialog.Builder(activity).setTitle(if (images.size == 1) "Crop ${reference.name}" else "Batch crop images")
            .setView(ScrollView(activity).apply { addView(body) }).setNegativeButton("Cancel",null).setPositiveButton("Apply crop",null).create()
        dialog.setOnShowListener { dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
            try {
                require(selected.isNotEmpty()) { "Choose at least one image." }
                val m = margins() ?: throw IllegalArgumentException("Enter all four trim amounts.")
                val crops = images.filter { it.id in selected }.associate { it.id to m.rect(it.dimensions) }
                apply(crops); dialog.dismiss()
            } catch (error: Exception) { status.text = error.message ?: "Could not apply the crop." }
        } }; dialog.show(); return dialog
    }
}
