/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R
import android.app.Activity
import android.app.AlertDialog
import android.text.InputType
import android.view.View
import android.widget.*

enum class ImageFormat(val label: String,val mime: String,val extension: String,val supportsLossless: Boolean=false) {
    // Append values to retain the saved-state ordinals used by earlier builds.
    PNG("PNG", "image/png", ".png"), JPEG("JPEG", "image/jpeg", ".jpg"),
    JPEG_XL("JPEG XL", "image/jxl", ".jxl",true), WEBP("WebP","image/webp",".webp",true),
    HEIC("HEIC","image/heic",".heic"), AVIF("AVIF","image/avif",".avif",true),
    BMP("BMP","image/bmp",".bmp"), GIF("GIF","image/gif",".gif");
    val supportsQuality: Boolean get() = this !in listOf(PNG,BMP,GIF)
}
data class ExportOptions(val format: ImageFormat=ImageFormat.PNG,val quality: Int=95,val lossless: Boolean=true,val dither: Boolean=true)
data class SaveRequest(val options: ExportOptions,val fileName: String)

object ExportNames {
    fun withExtension(name: String,format: ImageFormat): String {
        val trimmed=name.trim()
        val suffix=(ImageFormat.values().map {it.extension}+listOf(".jpeg",".jpe",".jfif",".dib"))
            .firstOrNull {trimmed.endsWith(it,true)}
        return (if(suffix==null) trimmed else trimmed.dropLast(suffix.length))+format.extension
    }
    fun valid(name: String,format: ImageFormat): Boolean {
        val stem=withExtension(name,format).removeSuffix(format.extension)
        return stem.isNotBlank() && stem!="." && stem!=".." && name.none {it=='/' || it=='\\' || it.isISOControl()}
    }
}

/** One options panel precedes Android's destination picker for every Save as format. */
class SaveOptionsDialog(private val activity: Activity,private val initial: ExportOptions,
    private val share: Boolean=false,private val confirm: (SaveRequest)->Unit,private val cancel: ()->Unit,
    private val initialFilename: String="") {
    fun show(): AlertDialog {
        var format=initial.format;var quality=initial.quality;var lossless=initial.lossless
        val body=LinearLayout(activity).apply {orientation=LinearLayout.VERTICAL;setPadding(24,12,24,12)}
        body.addView(TextView(activity).apply {text=ui(R.string.save20_file_name)})
        val filename=EditText(activity).apply {
            tag="export_filename";setSingleLine(true)
            inputType=InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_CAP_SENTENCES
            setText(ExportNames.withExtension(initialFilename.ifBlank {ui(R.string.ui_untitled)},format))
            contentDescription=ui(R.string.save20_file_name)
            selectAll()
        }
        body.addView(filename,LinearLayout.LayoutParams(-1,-2))
        body.addView(TextView(activity).apply {text=ui(R.string.save20_file_format)})
        val losslessBox=CheckBox(activity).apply {tag="export_lossless";isChecked=lossless}
        val ditherBox=CheckBox(activity).apply {tag="export_dither";text=ui(R.string.save20_dither);isChecked=initial.dither}
        val slider=NumericSlider(activity,ui(R.string.ui_quality),quality,1,100) {quality=it}.apply {tag="export_quality"}
        val explanation=TextView(activity).apply {tag="export_description"}
        fun update() {
            losslessBox.text=ui(R.string.ui_lossless_format,format.label)
            losslessBox.visibility=if(format.supportsLossless) View.VISIBLE else View.GONE
            slider.visibility=if(format.supportsQuality && !(format.supportsLossless && lossless)) View.VISIBLE else View.GONE
            ditherBox.visibility=if(format==ImageFormat.GIF) View.VISIBLE else View.GONE
            explanation.text=ui(when(format) {
                ImageFormat.GIF -> R.string.save20_gif_description
                ImageFormat.BMP -> R.string.save20_bmp_description
                ImageFormat.JPEG,ImageFormat.HEIC -> R.string.save20_lossy_quality_description
                else -> R.string.ui_higher_quality_usually_makes_a_larger_file_lossless
            })
            explanation.visibility=if(format==ImageFormat.PNG) View.GONE else View.VISIBLE
        }
        body.addView(Spinner(activity).apply {
            tag="export_format";contentDescription=ui(R.string.save20_file_format)
            adapter=ArrayAdapter(activity,android.R.layout.simple_spinner_dropdown_item,ImageFormat.values().map {it.label})
            setSelection(format.ordinal)
            onItemSelectedListener=object: AdapterView.OnItemSelectedListener {
                override fun onNothingSelected(parent: AdapterView<*>?)=Unit
                override fun onItemSelected(parent: AdapterView<*>?,view: View?,position: Int,id: Long) {
                    format=ImageFormat.values()[position]
                    if(filename.text.isNotBlank()) filename.setText(ExportNames.withExtension(filename.text.toString(),format))
                    update()
                }
            }
        },LinearLayout.LayoutParams(-1,-2))
        body.addView(losslessBox);body.addView(slider);body.addView(ditherBox);body.addView(explanation)
        losslessBox.setOnCheckedChangeListener {_,checked -> lossless=checked;update()};update()
        val dialog=AlertDialog.Builder(activity).setTitle(if(share) ui(R.string.ui_save_and_share_41edb4) else ui(R.string.save20_title))
            .setView(ScrollView(activity).apply {addView(body)})
            .setPositiveButton(ui(R.string.ui_choose_location),null)
            .setNegativeButton(ui(R.string.ui_cancel)) {_,_ -> cancel()}.setOnCancelListener {cancel()}.create()
        dialog.setOnShowListener {
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
                val name=filename.text.toString()
                if(!ExportNames.valid(name,format)) filename.error=ui(R.string.save20_invalid_name)
                else {
                    confirm(SaveRequest(ExportOptions(format,quality,format.supportsLossless && lossless,ditherBox.isChecked),ExportNames.withExtension(name,format)))
                    dialog.dismiss()
                }
            }
        }
        dialog.show();return dialog
    }
}
