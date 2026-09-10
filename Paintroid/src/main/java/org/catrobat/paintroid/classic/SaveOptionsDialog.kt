/* AN Paint, 2026-09-10. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.Activity
import android.app.AlertDialog
import android.view.View
import android.widget.*

enum class ImageFormat(val label: String,val mime: String,val extension: String) {
    PNG("PNG", "image/png", ".png"), JPEG("JPEG", "image/jpeg", ".jpg"), JPEG_XL("JPEG XL", "image/jxl", ".jxl")
}
data class ExportOptions(val format: ImageFormat=ImageFormat.PNG,val quality: Int=95,val lossless: Boolean=true)

class SaveOptionsDialog(private val activity: Activity,private val initial: ExportOptions,
    private val chooseFormat: Boolean=false,private val confirm: (ExportOptions)->Unit,private val cancel: ()->Unit) {
    fun show(): AlertDialog {
        var format=initial.format;var quality=initial.quality;var lossless=initial.lossless
        val body=LinearLayout(activity).apply {orientation=LinearLayout.VERTICAL;setPadding(24,12,24,12)}
        val losslessBox=CheckBox(activity).apply {tag="export_lossless";text="Lossless JPEG XL";isChecked=lossless}
        val slider=NumericSlider(activity,"Quality (%)",quality,1,100) {quality=it}.apply {tag="export_quality"}
        val explanation=TextView(activity).apply {text="Higher quality usually makes a larger file. Lossless keeps every colour value."}
        fun update() {
            losslessBox.visibility=if(format==ImageFormat.JPEG_XL) View.VISIBLE else View.GONE
            slider.visibility=if(format==ImageFormat.JPEG || format==ImageFormat.JPEG_XL && !lossless) View.VISIBLE else View.GONE
        }
        if(chooseFormat) body.addView(Spinner(activity).apply {
            tag="export_format";adapter=ArrayAdapter(activity,android.R.layout.simple_spinner_dropdown_item,ImageFormat.values().map {it.label})
            setSelection(format.ordinal)
            onItemSelectedListener=object: AdapterView.OnItemSelectedListener {
                override fun onNothingSelected(parent: AdapterView<*>?)=Unit
                override fun onItemSelected(parent: AdapterView<*>?,view: View?,position: Int,id: Long) {format=ImageFormat.values()[position];update()}
            }
        })
        body.addView(losslessBox);body.addView(slider);body.addView(explanation)
        losslessBox.setOnCheckedChangeListener {_,checked -> lossless=checked;update()};update()
        return AlertDialog.Builder(activity).setTitle(if(chooseFormat) "Save and share" else "Save as ${format.label}")
            .setView(ScrollView(activity).apply {addView(body)})
            .setPositiveButton("Choose location…") {_,_ -> confirm(ExportOptions(format,quality,lossless))}
            .setNegativeButton("Cancel") {_,_ -> cancel()}.setOnCancelListener {cancel()}.show()
    }
}
