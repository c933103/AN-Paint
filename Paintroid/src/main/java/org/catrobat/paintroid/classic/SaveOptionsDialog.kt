/* AN Paint, 2026-09-10. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.app.Activity
import android.app.AlertDialog
import android.view.View
import android.widget.*

enum class ImageFormat(val label: String,val mime: String,val extension: String,val supportsLossless: Boolean=false) {
    // Append values to retain the saved-state ordinals used by earlier builds.
    PNG("PNG", "image/png", ".png"), JPEG("JPEG", "image/jpeg", ".jpg"),
    JPEG_XL("JPEG XL", "image/jxl", ".jxl",true), WEBP("WebP","image/webp",".webp",true),
    HEIC("HEIC","image/heic",".heic"), AVIF("AVIF","image/avif",".avif",true)
}
data class ExportOptions(val format: ImageFormat=ImageFormat.PNG,val quality: Int=95,val lossless: Boolean=true)

class SaveOptionsDialog(private val activity: Activity,private val initial: ExportOptions,
    private val chooseFormat: Boolean=false,private val confirm: (ExportOptions)->Unit,private val cancel: ()->Unit) {
    fun show(): AlertDialog {
        var format=initial.format;var quality=initial.quality;var lossless=initial.lossless
        val body=LinearLayout(activity).apply {orientation=LinearLayout.VERTICAL;setPadding(24,12,24,12)}
        val losslessBox=CheckBox(activity).apply {tag="export_lossless";isChecked=lossless}
        val slider=NumericSlider(activity,ui(R.string.ui_quality),quality,1,100) {quality=it}.apply {tag="export_quality"}
        val explanation=TextView(activity).apply {text=ui(R.string.ui_higher_quality_usually_makes_a_larger_file_lossless)}
        fun update() {
            losslessBox.text=ui(R.string.ui_lossless_format,format.label)
            losslessBox.visibility=if(format.supportsLossless) View.VISIBLE else View.GONE
            slider.visibility=if(format!=ImageFormat.PNG && !(format.supportsLossless && lossless)) View.VISIBLE else View.GONE
            explanation.visibility=if(format==ImageFormat.PNG) View.GONE else View.VISIBLE
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
        return AlertDialog.Builder(activity).setTitle(if(chooseFormat) ui(R.string.ui_save_and_share_41edb4) else ui(R.string.ui_save_as, format.label))
            .setView(ScrollView(activity).apply {addView(body)})
            .setPositiveButton(ui(R.string.ui_choose_location)) {_,_ -> confirm(ExportOptions(format,quality,format.supportsLossless && lossless))}
            .setNegativeButton(ui(R.string.ui_cancel)) {_,_ -> cancel()}.setOnCancelListener {cancel()}.show()
    }
}
