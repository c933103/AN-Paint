/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R
import android.app.Activity
import android.app.AlertDialog
import android.text.InputType
import android.view.View
import android.widget.*

enum class ImageFormat(private val displayLabel: String,val mime: String,val extension: String,val supportsLossless: Boolean=false) {
    // Append values to retain the saved-state ordinals used by earlier builds.
    PNG("PNG", "image/png", ".png"), JPEG("JPEG", "image/jpeg", ".jpg"),
    JPEG_XL("JPEG XL", "image/jxl", ".jxl",true), WEBP("WebP","image/webp",".webp",true),
    HEIC("HEIC","image/heic",".heic"), AVIF("AVIF","image/avif",".avif",true),
    BMP("BMP","image/bmp",".bmp"), GIF("GIF","image/gif",".gif"),
    DIB("DIB","image/x-dib",".dib"), TIFF("TIFF","image/tiff",".tif"),
    ICO("ICO","image/vnd.microsoft.icon",".ico"), BASE64("Base64 text","text/plain",".txt"),
    ASCII_ART("ASCII art","text/plain",".txt");
    val label: String get()=when(this) {BASE64->ui(R.string.formats22_base64_label);ASCII_ART->ui(R.string.formats22_ascii_label);else->displayLabel}
    val supportsQuality: Boolean get() = this in listOf(JPEG,JPEG_XL,WEBP,HEIC,AVIF)
    val canSaveLosslessly: Boolean get() = this in listOf(PNG,JPEG_XL,WEBP,AVIF,BMP,DIB,TIFF,BASE64)
    val isDerivedExport: Boolean get() = this == ICO || this == ASCII_ART
}
data class ExportOptions(val format: ImageFormat=ImageFormat.PNG,val quality: Int=95,val lossless: Boolean=true,val dither: Boolean=true,val tiffCompressed: Boolean=true,
    val icoSize: Int=256,val asciiColumns: Int=100,val asciiInvert: Boolean=false)
data class SaveRequest(val options: ExportOptions,val fileName: String)

object ExportNames {
    fun withExtension(name: String,format: ImageFormat): String {
        val trimmed=name.trim()
        val suffix=(ImageFormat.values().map {it.extension}+listOf(".jpeg",".jpe",".jfif",".tiff",".pdf"))
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
    private val initialFilename: String="", private val export: Boolean=false) {
    fun show(): AlertDialog {
        val formats=ImageFormat.values().filter {if(share) true else if(export) it.supportsQuality || it in listOf(ImageFormat.GIF,ImageFormat.ICO,ImageFormat.ASCII_ART) else it.canSaveLosslessly}
        var format=initial.format.takeIf {it in formats} ?: formats.first();var quality=initial.quality;var lossless=if(share) initial.lossless else !export
        val body=LinearLayout(activity).apply {orientation=LinearLayout.VERTICAL;setPadding(24,12,24,12)}
        body.addView(TextView(activity).apply {text=ui(if(export) R.string.ui_export_explanation23 else R.string.ui_save_explanation23)})
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
        val tiffCompressionBox=CheckBox(activity).apply {tag="export_tiff_compressed";text=ui(R.string.formats22_tiff_compression);isChecked=initial.tiffCompressed}
        val iconEdges=listOf(16,24,32,48,64,128,256)
        var icoSize=initial.icoSize.takeIf {it in iconEdges} ?: 256
        val iconControls=LinearLayout(activity).apply {orientation=LinearLayout.VERTICAL;tag="export_ico_controls"}
        iconControls.addView(TextView(activity).apply {text=ui(R.string.formats22_ico_size)})
        iconControls.addView(Spinner(activity).apply {
            tag="export_ico_size";contentDescription=ui(R.string.formats22_ico_size)
            adapter=ArrayAdapter(activity,android.R.layout.simple_spinner_dropdown_item,iconEdges.map {"$it × $it"})
            setSelection(iconEdges.indexOf(icoSize))
            onItemSelectedListener=object: AdapterView.OnItemSelectedListener {
                override fun onNothingSelected(parent: AdapterView<*>?)=Unit
                override fun onItemSelected(parent: AdapterView<*>?,view: View?,position: Int,id: Long) {icoSize=iconEdges[position]}
            }
        })
        var asciiColumns=initial.asciiColumns.coerceIn(40,240)
        val asciiControls=LinearLayout(activity).apply {orientation=LinearLayout.VERTICAL;tag="export_ascii_controls"}
        asciiControls.addView(NumericSlider(activity,ui(R.string.formats22_ascii_columns),asciiColumns,40,240) {asciiColumns=it}.apply {tag="export_ascii_columns"})
        val asciiInvert=CheckBox(activity).apply {tag="export_ascii_invert";text=ui(R.string.formats22_ascii_invert);isChecked=initial.asciiInvert}
        asciiControls.addView(asciiInvert)
        val slider=NumericSlider(activity,ui(R.string.ui_quality),quality,1,100) {quality=it}.apply {tag="export_quality"}
        val explanation=FlowTextView(activity).apply {tag="export_description"}
        fun update() {
            losslessBox.text=ui(R.string.ui_lossless_format,format.label)
            losslessBox.visibility=if(share && format.supportsLossless) View.VISIBLE else View.GONE
            slider.visibility=if(format.supportsQuality && !(format.supportsLossless && lossless)) View.VISIBLE else View.GONE
            ditherBox.visibility=if(format==ImageFormat.GIF) View.VISIBLE else View.GONE
            tiffCompressionBox.visibility=if(format==ImageFormat.TIFF) View.VISIBLE else View.GONE
            iconControls.visibility=if(format==ImageFormat.ICO) View.VISIBLE else View.GONE
            asciiControls.visibility=if(format==ImageFormat.ASCII_ART) View.VISIBLE else View.GONE
            explanation.text=ui(when(format) {
                ImageFormat.GIF -> R.string.save20_gif_description
                ImageFormat.BMP -> R.string.save20_bmp_description
                ImageFormat.DIB -> R.string.formats22_dib_description
                ImageFormat.TIFF -> R.string.formats22_tiff_description
                ImageFormat.ICO -> R.string.formats22_ico_description
                ImageFormat.BASE64 -> R.string.formats22_base64_description
                ImageFormat.ASCII_ART -> R.string.formats22_ascii_description
                ImageFormat.JPEG,ImageFormat.HEIC -> R.string.save20_lossy_quality_description
                else -> R.string.ui_higher_quality_usually_makes_a_larger_file_lossless
            })
            explanation.visibility=if(format==ImageFormat.PNG) View.GONE else View.VISIBLE
        }
        losslessBox.setOnCheckedChangeListener {_,checked ->lossless=checked;update()}
        body.addView(Spinner(activity).apply {
            tag="export_format";contentDescription=ui(R.string.save20_file_format)
            adapter=ArrayAdapter(activity,android.R.layout.simple_spinner_dropdown_item,formats.map {it.label})
            setSelection(formats.indexOf(format))
            onItemSelectedListener=object: AdapterView.OnItemSelectedListener {
                override fun onNothingSelected(parent: AdapterView<*>?)=Unit
                override fun onItemSelected(parent: AdapterView<*>?,view: View?,position: Int,id: Long) {
                    format=formats[position]
                    if(filename.text.isNotBlank()) filename.setText(ExportNames.withExtension(filename.text.toString(),format))
                    update()
                }
            }
        },LinearLayout.LayoutParams(-1,-2))
        body.addView(losslessBox);body.addView(slider);body.addView(ditherBox);body.addView(tiffCompressionBox);body.addView(iconControls);body.addView(asciiControls);body.addView(explanation)
        update()
        val content: View=if(VerticalText.uiVertical()) {
            val form=LinearLayout(activity).apply {orientation=LinearLayout.HORIZONTAL;isBaselineAligned=false;tag="vertical_save_form"}
            val tall=(activity.resources.configuration.screenHeightDp-260).coerceIn(144,280)
            val d=activity.resources.displayMetrics.density
            fun prose(value: String)=FlowTextView(activity).apply {text=value;columnHeightDp=tall;textSize=14f;setPadding((8*d).toInt(),0,(8*d).toInt(),0)}
            fun field(label: String,control: View) {
                val column=LinearLayout(activity).apply {orientation=LinearLayout.HORIZONTAL;isBaselineAligned=false}
                if(control is Spinner) VerticalUi.spinner(control,tall)
                column.addView(prose(label));column.addView(VerticalUi.detach(control),LinearLayout.LayoutParams(((if(control is Spinner) 68 else 128)*d).toInt(),-2))
                form.addView(column)
            }
            // A vertical filename preview sits beside the native keyboard field. Identifiers and numeric
            // values remain editable with Android's selection/IME support, independent of reading direction.
            val nameColumn=LinearLayout(activity).apply {orientation=LinearLayout.VERTICAL}
            val preview=prose(filename.text.toString()).apply {tag="vertical_filename_preview"}
            nameColumn.addView(preview)
            nameColumn.addView(VerticalUi.detach(filename),LinearLayout.LayoutParams((128*d).toInt(),-2))
            filename.addTextChangedListener(object: android.text.TextWatcher {
                override fun beforeTextChanged(s: CharSequence?,start: Int,count: Int,after: Int)=Unit
                override fun onTextChanged(s: CharSequence?,start: Int,before: Int,count: Int) {preview.text=s}
                override fun afterTextChanged(s: android.text.Editable?)=Unit
            })
            field(ui(R.string.save20_file_name),nameColumn)
            field(ui(R.string.save20_file_format),body.findViewWithTag<Spinner>("export_format"))
            listOf(losslessBox,slider,ditherBox,tiffCompressionBox,iconControls,asciiControls,explanation).forEach {control ->
                VerticalUi.detach(control)
                if(control is LinearLayout && control !is NumericSlider) VerticalUi.panel(control,tall)
                if(control is TextView) VerticalUi.caption(control,tall)
                if(control is FlowTextView) control.columnHeightDp=tall
                form.addView(control,LinearLayout.LayoutParams(if(control is NumericSlider) (176*d).toInt() else -2,-2).apply {setMargins((8*d).toInt(),0,(8*d).toInt(),0)})
            }
            form.addView(prose(ui(if(export) R.string.ui_export_explanation23 else R.string.ui_save_explanation23)))
            form.layoutDirection=if(VerticalText.uiDirection()==TextDirection.VERTICAL_RL) View.LAYOUT_DIRECTION_RTL else View.LAYOUT_DIRECTION_LTR
            form
        } else ScrollView(activity).apply {addView(body)}
        val dialog=EditorDialogBuilder(activity).setTitle(if(share) ui(R.string.ui_save_and_share_41edb4) else ui(if(export) R.string.ui_export_as23 else R.string.save20_title))
            .setView(content)
            .setPositiveButton(ui(R.string.ui_choose_location),null)
            .setNegativeButton(ui(R.string.ui_cancel)) {_,_ -> cancel()}.setOnCancelListener {cancel()}.create()
        dialog.setOnShowListener {
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
                val name=filename.text.toString()
                if(!ExportNames.valid(name,format)) filename.error=ui(R.string.save20_invalid_name)
                else {
                    confirm(SaveRequest(ExportOptions(format,quality,format.supportsLossless && lossless,ditherBox.isChecked,tiffCompressionBox.isChecked,icoSize,asciiColumns,asciiInvert.isChecked),ExportNames.withExtension(name,format)))
                    dialog.dismiss()
                }
            }
        }
        dialog.show();return dialog
    }
}
