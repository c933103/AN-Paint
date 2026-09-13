/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.Activity
import android.app.AlertDialog
import android.graphics.Bitmap
import android.text.Editable
import android.text.InputType
import android.text.TextWatcher
import android.view.Gravity
import android.widget.*
import org.catrobat.paintroid.R
import java.io.File
import java.io.InputStream
import java.io.IOException
import java.util.concurrent.ExecutorService

/** A provider copy is bounded on disk; Base64 is unwrapped once, before all format inspection. */
object ImportFiles {
    const val MAX_BYTES = 512L * 1024 * 1024
    fun copy(input: InputStream, destination: File) {
        destination.outputStream().use { output ->
            val buffer=ByteArray(64*1024);var total=0L
            while(true) {
                val count=input.read(buffer);if(count<0) break
                total+=count
                if(total>MAX_BYTES) throw IOException(ui(R.string.formats22_import_limit))
                output.write(buffer,0,count)
            }
        }
    }
    fun normalize(file: File) {
        if(TextImageCodec.inspect(file)) TextImageCodec.decodeToFile(file,file,MAX_BYTES)
    }
}

/** Owns the staged file until selection succeeds. Inspection and previews stay off the UI thread. */
class ImportSelection(private val activity: Activity,private val worker: ExecutorService,
    private val residentPixels: ()->Long,private val selected: (ImportedImage)->Unit,
    private val cancelled: ()->Unit,private val failed: (Throwable)->Unit) {
    private var file: File?=null
    private var name=""
    private var dialog: AlertDialog?=null
    private var preview: Bitmap?=null
    private var previewView: ImageView?=null
    @Volatile private var active=true
    @Volatile private var disposed=false
    @Volatile private var generation=0

    fun start(staged: File,displayName: String) {
        file=staged;name=displayName
        worker.execute {
            try {
                ImportFiles.normalize(staged)
                if(disposed) {staged.delete();return@execute}
                val kind=when {PdfCodec.isPdf(staged)->"PDF";TiffCodec.isTiff(staged)->"TIFF";else->null}
                val pages=when(kind) {"PDF"->PdfCodec.pageCount(staged);"TIFF"->TiffCodec.pageCount(staged);else->0}
                val animation=if(kind==null) AnimationInfo.inspect(staged) else null
                activity.runOnUiThread {
                    if(!alive()) dispose()
                    else if(kind!=null) showPages(kind,pages)
                    else if(animation!=null) showAnimation(animation)
                    else finishSelection(0)
                }
            } catch(error: Exception) {fail(error)} catch(error: OutOfMemoryError) {fail(error)}
            finally {if(disposed) staged.delete()}
        }
    }

    private fun alive()=active && !activity.isDestroyed && !activity.isFinishing
    private fun releasePreview() {previewView?.setImageDrawable(null);preview?.recycle();preview=null}
    /** Called by the owner during destruction; a dismissed dialog never continues an import. */
    fun dispose() {
        disposed=true;active=false;generation++;dialog?.dismiss();dialog=null;releasePreview();file?.delete();file=null
    }
    private fun cancel() {dispose();cancelled()}
    private fun fail(error: Throwable) {activity.runOnUiThread {if(alive()) {dispose();failed(error)} else dispose()}}
    private fun finishSelection(page: Int) {
        val staged=file ?: return
        generation++;dialog?.dismiss();dialog=null;releasePreview()
        worker.execute {
            try {
                val source=ImportedImage(staged,name,page)
                activity.runOnUiThread {
                    if(!alive()) dispose() else {active=false;file=null;selected(source)}
                }
            } catch(error: Exception) {fail(error)} catch(error: OutOfMemoryError) {fail(error)}
        }
    }
    private fun showAnimation(info: AnimationInfo) {
        val frames=if(info.frameCountExact) info.frameCount.toString() else ui(R.string.formats22_at_least_frames,info.frameCount)
        val message=if(info.frameCount<2) ui(R.string.formats22_animation_unknown,info.format) else
            ui(R.string.formats22_animation_message,info.format,frames)+"\n\n"+
                ui(if(info.pngDefaultImageSeparate) R.string.formats22_animation_poster else R.string.formats22_animation_still)
        dialog=AlertDialog.Builder(activity).setTitle(ui(R.string.formats22_animation_title)).setMessage(message)
            .setPositiveButton(ui(R.string.formats22_open_still)) {_,_->finishSelection(0)}
            .setNegativeButton(ui(R.string.ui_cancel)) {_,_->cancel()}.setOnCancelListener {cancel()}.show()
    }
    private fun showPages(kind: String,count: Int) {
        require(count>0)
        val body=LinearLayout(activity).apply {orientation=LinearLayout.VERTICAL;setPadding(24,12,24,12)}
        body.addView(TextView(activity).apply {text=ui(R.string.formats22_page_description,kind,name,count)})
        if(kind=="PDF") body.addView(TextView(activity).apply {text=ui(R.string.formats22_pdf_raster_hint)})
        val row=LinearLayout(activity).apply {gravity=Gravity.CENTER_VERTICAL}
        val previous=Button(activity).apply {text="‹";contentDescription=ui(R.string.formats22_previous_page);tag="import_previous_page"}
        val field=EditText(activity).apply {tag="import_page_number";inputType=InputType.TYPE_CLASS_NUMBER;setSingleLine(true);contentDescription=ui(R.string.formats22_page_number);setText("1");selectAll()}
        val next=Button(activity).apply {text="›";contentDescription=ui(R.string.formats22_next_page);tag="import_next_page"}
        val buttonWidth=(56*activity.resources.displayMetrics.density).toInt()
        row.addView(previous,LinearLayout.LayoutParams(buttonWidth,-2));row.addView(field,LinearLayout.LayoutParams(0,-2,1f));row.addView(next,LinearLayout.LayoutParams(buttonWidth,-2));body.addView(row)
        val status=TextView(activity).apply {tag="import_page_status"};body.addView(status)
        val image=ImageView(activity).apply {tag="import_page_preview";adjustViewBounds=true;scaleType=ImageView.ScaleType.FIT_CENTER;contentDescription=ui(R.string.formats22_page_preview)}
        previewView=image
        body.addView(image,LinearLayout.LayoutParams(-1,(220*activity.resources.displayMetrics.density).toInt()))
        val chooser=AlertDialog.Builder(activity).setTitle(ui(R.string.formats22_select_page))
            .setView(ScrollView(activity).apply {addView(body)})
            .setPositiveButton(ui(R.string.formats22_open_page),null)
            .setNegativeButton(ui(R.string.ui_cancel)) {_,_->cancel()}.setOnCancelListener {cancel()}.create()
        dialog=chooser
        fun page()=field.text.toString().toIntOrNull()?.takeIf {it in 1..count}
        fun update() {
            val value=page();val ticket=++generation
            previous.isEnabled=value!=null && value>1;next.isEnabled=value!=null && value<count
            chooser.getButton(AlertDialog.BUTTON_POSITIVE)?.isEnabled=value!=null
            image.setImageDrawable(null);releasePreview()
            if(value==null) {status.text=ui(R.string.formats22_page_range,count);return}
            status.text=ui(R.string.formats22_loading_page,value,count)
            val staged=file ?: return
            worker.execute {
                if(!active || generation!=ticket) return@execute
                var bitmap: Bitmap?=null
                try {
                    val source=ImportedImage(staged,name,value-1)
                    val dimensions=source.dimensions
                    val size=dimensions.scaled(minOf(1.0,384.0/maxOf(dimensions.width,dimensions.height)))
                    val plan=ImportPlan.create(dimensions,size);val policy=ImageMemoryPolicy.forDevice(activity)
                    val resident=residentPixels();source.checkImport(policy,plan,resident)
                    bitmap=source.decode(plan,policy.workingBytes,resident)
                    val result=bitmap;bitmap=null
                    activity.runOnUiThread {
                        if(!alive() || generation!=ticket) result.recycle()
                        else {preview=result;image.setImageBitmap(result);status.text=ui(R.string.formats22_page_dimensions,value,count,dimensions.width,dimensions.height)}
                    }
                } catch(error: Exception) {
                    activity.runOnUiThread {if(alive() && generation==ticket) status.text=ui(R.string.formats22_preview_unavailable,error.message ?: "")}
                } catch(_: OutOfMemoryError) {
                    activity.runOnUiThread {if(alive() && generation==ticket) status.text=ui(R.string.formats22_preview_memory)}
                } finally {bitmap?.recycle()}
            }
        }
        previous.setOnClickListener {page()?.let {field.setText((it-1).toString())}}
        next.setOnClickListener {page()?.let {field.setText((it+1).toString())}}
        field.addTextChangedListener(object: TextWatcher {
            override fun beforeTextChanged(s: CharSequence?,start: Int,count: Int,after: Int)=Unit
            override fun onTextChanged(s: CharSequence?,start: Int,before: Int,count: Int)=update()
            override fun afterTextChanged(s: Editable?)=Unit
        })
        chooser.setOnShowListener {update();chooser.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {page()?.let {finishSelection(it-1)}}}
        chooser.show()
    }
}
