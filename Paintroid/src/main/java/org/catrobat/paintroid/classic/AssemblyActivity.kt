/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.Activity
import android.app.AlertDialog
import android.content.ActivityNotFoundException
import android.content.ClipData
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Color
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.DocumentsContract
import android.provider.OpenableColumns
import android.text.TextUtils
import android.view.Gravity
import android.view.View
import android.widget.*
import java.io.File
import java.io.IOException
import java.text.DateFormat
import java.util.Date
import java.util.UUID
import java.util.concurrent.Executors

class AssemblyActivity : Activity() {
    companion object { const val ADD_IMAGES = 801; const val SAVE_ASSEMBLY = 802 }
    lateinit var assembly: ImageAssembly; private set
    lateinit var board: AssemblyCanvas; private set
    private lateinit var tray: LinearLayout
    private lateinit var info: TextView
    private lateinit var count: TextView
    private lateinit var undo: ActionButton
    private lateinit var redo: ActionButton
    private lateinit var add: Button
    private val previews = mutableMapOf<String,Bitmap>()
    private var selected: String? = null
    private var sort = AssemblySort.NAME_ASC
    private val worker = Executors.newSingleThreadExecutor()
    @Volatile var busy = false; private set
    var lastError: String? = null; private set
    private var pendingOutput: File? = null
    private var thumbnailLoading = false
    private val failedPreviews = mutableSetOf<String>()
    private fun dp(n: Int) = (n*resources.displayMetrics.density+.5f).toInt()
    private fun text(value: String, size: Float = 13f) = TextView(this).apply { text = value; textSize = size; setTextColor(0xff233b4d.toInt()); gravity = Gravity.CENTER_VERTICAL }
    private fun button(value: String, name: String, action: () -> Unit) = Button(this).apply {
        text = value; tag = name; isAllCaps = false; textSize = 12f; minWidth = 0; minimumWidth = 0; setPadding(dp(10),0,dp(10),0)
        setOnClickListener { if (!busy) perform(action) }
    }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        try { assembly = ImageAssembly(File(filesDir,"image-assembly")) }
        catch (error: Exception) { message("The saved assembly could not be opened: ${error.message}"); return }
        savedInstanceState?.getString("pending_output")?.let { name -> File(filesDir,name).takeIf { it.parentFile == filesDir && name.startsWith("assembly-output-") && it.isFile }?.let { pendingOutput = it } }
        sort = AssemblySort.values().getOrElse(savedInstanceState?.getInt("sort") ?: 0) { AssemblySort.NAME_ASC }
        selected = savedInstanceState?.getString("selected")
        buildInterface()
    }
    override fun onConfigurationChanged(newConfig: android.content.res.Configuration) {
        super.onConfigurationChanged(newConfig)
        if (::assembly.isInitialized) buildInterface()
    }
    private fun compact() = resources.configuration.screenHeightDp < 600
    private fun buildInterface() {
        val root = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; fitsSystemWindows = true; setBackgroundColor(0xffe8e7df.toInt()) }
        setContentView(root)
        val header = LinearLayout(this).apply { gravity = Gravity.CENTER_VERTICAL; setPadding(dp(10),0,dp(6),0); setBackgroundColor(0xff1559a6.toInt()) }
        count = text("AN Paint · Image assembly",15f).apply { setTextColor(Color.WHITE); maxLines = 2 }
        header.addView(count,LinearLayout.LayoutParams(0,dp(if (compact()) 44 else 54),1f))
        undo = ActionButton(this,EditIcon.UNDO).apply { tag = "assembly_undo"; setOnClickListener { if (!busy) perform { assembly.undo() } } }
        redo = ActionButton(this,EditIcon.REDO).apply { tag = "assembly_redo"; setOnClickListener { if (!busy) perform { assembly.redo() } } }
        header.addView(undo,LinearLayout.LayoutParams(dp(48),dp(48))); header.addView(redo,LinearLayout.LayoutParams(dp(48),dp(48))); root.addView(header)
        fun actionRow(vararg views: View): LinearLayout {
            val row = LinearLayout(this); views.forEach { row.addView(it,LinearLayout.LayoutParams(-2,dp(46))) }
            root.addView(HorizontalScrollView(this).apply { isHorizontalScrollBarEnabled = false; addView(row) }); return row
        }
        add = button("Add images","assembly_add") { launchAdd() }
        actionRow(add,button("Save PNG","assembly_save") { requestOutput(false) },button("Edit in Paint","assembly_edit") { requestOutput(true) },button("How to use","assembly_help") { showHelp() })
        board = AssemblyCanvas(this,assembly) { previews[it] }.apply {
            tag = "assembly_canvas"; onError = { message(it.message ?: "Could not place the image.") }
            onSelect = { id -> selected = id; for (i in 0 until tray.childCount) tray.getChildAt(i).setBackgroundColor(if (tray.getChildAt(i).tag == "assembly_item_$id") 0xffb8d9f6.toInt() else 0xffdedfdd.toInt()) }; onStatus = { if (!busy) info.text = it }
        }
        root.addView(board,LinearLayout.LayoutParams(-1,0,1f))
        info = text("Drag placed images to move them. Hold and drag a thumbnail to add it.").apply { tag = "assembly_status"; setPadding(dp(8),dp(3),dp(8),dp(3)); minLines = if (compact()) 1 else 2; maxLines = if (compact()) 1 else 2; ellipsize = TextUtils.TruncateAt.END }
        root.addView(info,LinearLayout.LayoutParams(-1,if (compact()) dp(24) else -2))
        val editingActions = actionRow(button("Crop image","assembly_crop") { crop(false) },button("Batch crop","assembly_batch_crop") { crop(true) },
            button("Same width","assembly_same_width") { normalize(NormalizeAxis.WIDTH) },
            button("Same height","assembly_same_height") { normalize(NormalizeAxis.HEIGHT) },
            button("Unplace","assembly_unplace") { selected?.let { assembly.unplace(it) } ?: message("Tap an image first.") },
            button("Remove","assembly_remove") { selected?.let { assembly.remove(it) } ?: message("Tap an image first.") },
            button("Show all","assembly_fit") { board.fit(); info.text="Shows the whole assembly. Image and output sizes stay unchanged." },button("Clear all","assembly_clear") { assembly.clear() })
        val sortRow = LinearLayout(this).apply { gravity = Gravity.CENTER_VERTICAL; setPadding(dp(8),0,dp(8),0) }
        sortRow.addView(text("Sort tray"))
        sortRow.addView(Spinner(this).apply {
            tag = "assembly_sort"; contentDescription = "Sort images by filename or modification time"
            adapter = ArrayAdapter(this@AssemblyActivity,android.R.layout.simple_spinner_dropdown_item,AssemblySort.values().map { it.label }); setSelection(sort.ordinal)
            onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
                override fun onNothingSelected(parent: AdapterView<*>?) = Unit
                override fun onItemSelected(parent: AdapterView<*>?,view: View?,position: Int,id: Long) { sort = AssemblySort.values()[position]; if (::tray.isInitialized) renderTray() }
            }
        },LinearLayout.LayoutParams(0,dp(44),1f))
        if (compact()) editingActions.addView(sortRow,LinearLayout.LayoutParams(dp(280),dp(46))) else root.addView(sortRow)
        tray = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; tag = "assembly_thumbnails" }
        root.addView(HorizontalScrollView(this).apply { tag = "assembly_tray"; contentDescription = "Image thumbnails and filenames. Scroll horizontally for more."; addView(tray) },LinearLayout.LayoutParams(-1,dp(if (compact()) 108 else 154)))
        assembly.changed = { refresh() }; refresh(); loadMissingPreviews()
    }
    private fun perform(action: () -> Unit) { try { action() } catch (error: Exception) { message(error.message ?: "Could not complete the operation.") } catch (_: OutOfMemoryError) { message("Not enough memory for this operation. The assembly source files are retained.") } }
    private fun message(value: String) {
        lastError = value
        if (!isDestroyed && !isFinishing) AlertDialog.Builder(this).setTitle("AN Paint").setMessage(value).setPositiveButton("OK",null).show()
    }
    private fun setBusy(value: Boolean) { busy = value; if (::board.isInitialized) { board.isEnabled = !value; undo.isEnabled = !value && assembly.canUndo; redo.isEnabled = !value && assembly.canRedo; add.isEnabled = !value && assembly.images.size < 20 }; if (value) info.text = "Working…" }
    private fun refresh() {
        if (isDestroyed || !::tray.isInitialized) return
        if (assembly.images.none { it.id == selected }) selected = null
        renderTray()
        val ids = assembly.images.map { it.id }.toSet()
        previews.keys.filter { it !in ids }.forEach { previews.remove(it)?.recycle() }
        board.refresh(); count.text = "AN Paint · Image assembly\n${assembly.images.size}/20 images · ${assembly.layout().size} placed"
        val size = assembly.size()
        if (!busy) info.text = if (size == null) "Hold a thumbnail and drag it here, or tap it then tap the workspace." else "${size.width} × ${size.height} px · drag an image to move; hold a thumbnail to add."
        setBusy(busy)
        if (!busy) loadMissingPreviews()
    }
    private fun renderTray() {
        if (!::tray.isInitialized) return
        tray.removeAllViews()
        for (item in assembly.sorted(sort)) {
            val card = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL; tag = "assembly_item_${item.id}"; isFocusable = true; isClickable = true
                setPadding(dp(6),dp(4),dp(6),dp(4)); setBackgroundColor(if (item.id == selected) 0xffb8d9f6.toInt() else 0xffdedfdd.toInt())
                contentDescription = "${item.name}. ${if (item.attachment == null) "Not placed" else "Placed"}. ${item.placedSize.width} by ${item.placedSize.height} pixels. Hold and drag to place."
                setOnClickListener { if (!busy) { selected = item.id; board.select(item.id); renderTray() } }
                setOnLongClickListener {
                    if (busy) false else {
                        selected = item.id
                        val data = ClipData.newPlainText("AN Paint assembly image",item.id)
                        if (Build.VERSION.SDK_INT >= 24) startDragAndDrop(data,View.DragShadowBuilder(this),item.id,0)
                        else @Suppress("DEPRECATION") startDrag(data,View.DragShadowBuilder(this),item.id,0)
                        true
                    }
                }
            }
            card.addView(AssemblyThumbnail(this,item,previews[item.id]),LinearLayout.LayoutParams(-1,dp(if (compact()) 44 else 70)))
            card.addView(text(item.name,12f).apply { tag = "assembly_name_${item.id}"; maxLines = 2; ellipsize = TextUtils.TruncateAt.END },LinearLayout.LayoutParams(-1,dp(if (compact()) 28 else 34)))
            card.addView(text(item.timestamp?.let { DateFormat.getDateTimeInstance(DateFormat.SHORT,DateFormat.SHORT).format(Date(it)) } ?: "Time unavailable",10f).apply { maxLines = 1; ellipsize = TextUtils.TruncateAt.END })
            card.addView(text("${item.placedSize.width} × ${item.placedSize.height}${if (item.attachment == null) "" else " · placed"}",10f))
            tray.addView(card,LinearLayout.LayoutParams(dp(138),-1).apply { setMargins(dp(3),0,dp(3),0) })
        }
    }
    private fun thumbnail(item: AssemblyImage): Bitmap {
        val source = ImportedImage(item.file,item.name)
        val size = source.dimensions.scaled(minOf(1.0,384.0/maxOf(source.dimensions.width,source.dimensions.height)))
        val plan = ImportPlan.create(source.dimensions,size)
        ImageMemoryPolicy.forDevice(this).checkImport(plan,residentPixels())
        return source.decode(plan)
    }
    private fun loadMissingPreviews() {
        if (busy || thumbnailLoading || !::assembly.isInitialized) return
        val missing = assembly.images.filter { it.id !in previews && it.id !in failedPreviews }
        if (missing.isEmpty()) return
        thumbnailLoading = true; setBusy(true)
        worker.execute {
            val decoded = mutableMapOf<String,Bitmap>(); val errors = mutableSetOf<String>()
            missing.forEach { item -> try { decoded[item.id] = thumbnail(item) } catch (_: Exception) { errors.add(item.id) } catch (_: OutOfMemoryError) { errors.add(item.id) } }
            runOnUiThread {
                if (isDestroyed || isFinishing) decoded.values.forEach { it.recycle() }
                else { previews.putAll(decoded); failedPreviews.addAll(errors); thumbnailLoading = false; setBusy(false); refresh(); if (errors.isNotEmpty()) message("Some previews could not be decoded. You can remove those images or try saving the assembly.") }
            }
        }
    }
    private fun residentPixels() = intent.getLongExtra("resident_pixels",0) + 20L*384*384 // bounded preview allowance, including a crop preview
    fun launchAdd() {
        if (busy) return
        if (assembly.images.size >= 20) { message("An assembly can contain up to 20 images. Remove an image to add another."); return }
        launchPicker(Intent(Intent.ACTION_OPEN_DOCUMENT).apply { addCategory(Intent.CATEGORY_OPENABLE); type = "*/*"; putExtra(Intent.EXTRA_ALLOW_MULTIPLE,true); addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION) },ADD_IMAGES)
    }
    private fun launchPicker(intent: Intent,code: Int) {
        try { startActivityForResult(intent,code) }
        catch (_: ActivityNotFoundException) {
            if (intent.action == Intent.ACTION_OPEN_DOCUMENT) try { startActivityForResult(Intent(intent).setAction(Intent.ACTION_GET_CONTENT),code); return } catch (_: ActivityNotFoundException) { }
            message("Enable Android's Files or Documents app, then try again.")
        } catch (error: SecurityException) { message("Android blocked the file picker: ${error.message}") }
    }
    public override fun onActivityResult(requestCode: Int,resultCode: Int,data: Intent?) {
        super.onActivityResult(requestCode,resultCode,data)
        if (requestCode == ADD_IMAGES && resultCode == RESULT_OK) {
            val uris = data?.clipData?.let { clip -> (0 until clip.itemCount).map { clip.getItemAt(it).uri } } ?: listOfNotNull(data?.data)
            if (uris.isEmpty()) message("The picker returned no files.") else importImages(uris.distinct())
        } else if (requestCode == SAVE_ASSEMBLY) {
            val file = pendingOutput; pendingOutput = null
            if (resultCode == RESULT_OK && data?.data != null && file != null) saveOutput(file,data.data!!) else file?.delete()
        }
    }
    private fun metadata(uri: Uri): Pair<String,Long?> {
        var name = uri.lastPathSegment ?: "Image"; var timestamp: Long? = null
        try { contentResolver.query(uri,null,null,null,null)?.use { cursor -> if (cursor.moveToFirst()) {
            val n = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME); if (n >= 0 && !cursor.isNull(n)) name = cursor.getString(n)
            val modified = cursor.getColumnIndex(DocumentsContract.Document.COLUMN_LAST_MODIFIED)
            if (modified >= 0 && !cursor.isNull(modified)) timestamp = cursor.getLong(modified).takeIf { it > 0 }
            else { val m = cursor.getColumnIndex("date_modified"); if (m >= 0 && !cursor.isNull(m)) timestamp = cursor.getLong(m).takeIf { it > 0 && it <= Long.MAX_VALUE/1000 }?.times(1000) }
        } } } catch (_: Exception) { /* Metadata is optional; never invent a file timestamp. */ }
        return name to timestamp
    }
    private fun importImages(uris: List<Uri>) {
        if (busy) return
        if (uris.size > 20-assembly.images.size) { message("You can add ${20-assembly.images.size} more images. Select fewer files."); return }
        setBusy(true); lastError = null
        worker.execute {
            val items = mutableListOf<AssemblyImage>(); val decoded = mutableMapOf<String,Bitmap>(); val errors = mutableListOf<String>()
            uris.forEach { uri ->
                val id = UUID.randomUUID().toString(); val file = File(assembly.directory,"$id.image")
                try {
                    val (name,time) = metadata(uri)
                    contentResolver.openInputStream(uri)?.use { input -> file.outputStream().use { input.copyTo(it,64*1024) } } ?: throw IOException("No readable image data.")
                    val source = ImportedImage(file,name); val item = AssemblyImage(id,file,name,time,source.dimensions)
                    decoded[id] = thumbnail(item); items.add(item)
                } catch (error: Exception) { file.delete(); errors.add("${uri.lastPathSegment}: ${error.message}") }
                catch (_: OutOfMemoryError) { file.delete(); errors.add("${uri.lastPathSegment}: not enough memory for its preview.") }
            }
            runOnUiThread {
                if (isDestroyed || isFinishing) { decoded.values.forEach { it.recycle() }; items.forEach { it.file.delete() } }
                else {
                    previews.putAll(decoded)
                    try { if (items.isNotEmpty()) assembly.add(items) }
                    catch (error: Exception) { items.forEach { previews.remove(it.id)?.recycle(); it.file.delete() }; errors.add(error.message ?: "Could not store the assembly.") }
                    setBusy(false); refresh(); if (errors.isNotEmpty()) message(errors.joinToString("\n"))
                }
            }
        }
    }
    private fun normalize(axis: NormalizeAxis) {
        if (assembly.images.isEmpty()) { message("Add images first."); return }
        NormalizeImagesDialog(this,assembly,axis).show()
    }
    private fun crop(batch: Boolean) {
        val images = if (batch) assembly.images else assembly.images.filter { it.id == selected }
        if (images.isEmpty()) { message(if (batch) "Add images first." else "Tap an image thumbnail first."); return }
        ImageCropDialog(this,images,{ previews[it.id] }) { assembly.crop(it) }.show()
    }
    private fun renderer() = AssemblyRenderer(this,assembly.images,assembly.layout(),residentPixels())
    private fun requestOutput(toPaint: Boolean) {
        if (assembly.size() == null) { message("Place at least one image in the workspace first."); return }
        val renderer = renderer()
        if (renderer.fits(renderer.original)) makeOutput(renderer,renderer.original,toPaint) else outputSizeDialog(renderer,toPaint)
    }
    private fun outputSizeDialog(renderer: AssemblyRenderer,toPaint: Boolean,previous: ImageDimensions? = null) {
        val body = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(dp(16),dp(8),dp(16),dp(8)) }
        body.addView(text("Assembly: ${renderer.original.describe()}\nDecoded output: ${memoryLabel(renderer.original.pixels*4.0)}\nEstimated editing/render memory at original size: ${memoryLabel(renderer.estimatedBytes(renderer.original))}"))
        body.addView(text("Choose a smaller output copy. The source images and crop settings stay at their original resolution."))
        val sizing = DimensionControls(this,renderer.original,renderer.suggested(previous),"assembly_size",true); body.addView(sizing)
        val estimate = text(""); body.addView(estimate)
        val dialog = AlertDialog.Builder(this).setTitle("Assembly output size").setView(ScrollView(this).apply { addView(body) }).setNegativeButton("Cancel",null).setPositiveButton("Create output",null).create()
        fun refresh() {
            val size = sizing.dimensions
            estimate.text = if (size == null) "Enter valid dimensions." else "Estimated memory: ${memoryLabel(renderer.estimatedBytes(size))}\nCurrent working budget: ${memoryLabel(ImageMemoryPolicy.forDevice(this).workingBytes.toDouble())}\n" + if (renderer.fits(size)) "Fits the current budget." else "Choose a smaller size."
            dialog.getButton(AlertDialog.BUTTON_POSITIVE)?.isEnabled = size != null && renderer.fits(size)
        }
        sizing.changed = { refresh() }
        dialog.setOnShowListener { refresh(); dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
            refresh(); sizing.dimensions?.takeIf { renderer.fits(it) }?.let { dialog.dismiss(); makeOutput(renderer,it,toPaint) }
        } }; dialog.show()
    }
    private fun makeOutput(renderer: AssemblyRenderer,size: ImageDimensions,toPaint: Boolean) {
        setBusy(true); val file = File(filesDir,"assembly-output-${UUID.randomUUID()}.png")
        worker.execute {
            try {
                val image = renderer.render(size) { n,total -> runOnUiThread { if (!isDestroyed) info.text = "Rendering $n / $total images…" } }
                try { file.outputStream().use { if (!image.compress(Bitmap.CompressFormat.PNG,100,it)) throw IOException("PNG encoding failed.") } } finally { image.recycle() }
                runOnUiThread {
                    if (isDestroyed || isFinishing) file.delete()
                    else {
                        setBusy(false); refresh()
                        if (toPaint) { setResult(RESULT_OK,Intent().putExtra("assembly_output",file.name)); finish() }
                        else { pendingOutput?.delete(); pendingOutput = file; launchPicker(Intent(Intent.ACTION_CREATE_DOCUMENT).apply { addCategory(Intent.CATEGORY_OPENABLE); type = "image/png"; putExtra(Intent.EXTRA_TITLE,"AN-Paint-assembly.png") },SAVE_ASSEMBLY) }
                    }
                }
            } catch (_: OutOfMemoryError) { file.delete(); runOnUiThread { if (!isDestroyed) { setBusy(false); outputSizeDialog(renderer,toPaint,size) } } }
            catch (_: ImageSizeException) { file.delete(); runOnUiThread { if (!isDestroyed) { setBusy(false); outputSizeDialog(renderer,toPaint,size) } } }
            catch (error: Exception) { file.delete(); runOnUiThread { if (!isDestroyed) { setBusy(false); refresh(); message("Could not create the assembly: ${error.message}") } } }
        }
    }
    private fun saveOutput(file: File,uri: Uri) {
        setBusy(true)
        worker.execute {
            try { contentResolver.openOutputStream(uri,"wt")?.use { output -> file.inputStream().use { it.copyTo(output,64*1024) } } ?: throw IOException("The selected location is not writable.")
                runOnUiThread { if (!isDestroyed) { setBusy(false); refresh(); Toast.makeText(this,"Assembly saved",Toast.LENGTH_SHORT).show() } }
            } catch (error: Exception) { runOnUiThread { if (!isDestroyed) { setBusy(false); refresh(); message("Could not save the assembly: ${error.message}") } } }
            finally { file.delete() }
        }
    }
    private fun showHelp() = message("Add up to 20 images with Android's file picker. The bottom tray shows thumbnails, filenames, crop dimensions and file modification times when supplied by the provider. Sort by filename or modification time; sorting does not rearrange placed images.\n\nTap a thumbnail to select it. Crop image trims that image; Batch crop applies pixel or percentage margins to selected images. Drag crop handles or type amounts. Reset crop restores the original edges. Cropping is non-destructive and can be undone.\n\nHold a thumbnail, or drag an image already in the workspace, then drop it onto a highlighted edge. The translucent preview shows the exact snapped result. A right attachment aligns the tops; a bottom attachment aligns the left edges. You can also tap a thumbnail and then a + target. The first image starts at the origin. Existing attachments move when their parent is cropped. Overlaps are rejected.\n\nSame width and Same height give every input a common dimension while preserving each image's own aspect ratio. Choose pixels, percent, Smallest or Largest. Restore original sizes removes normalization and keeps crops.\n\nUnplace returns only the selected image to the tray. Following images fill its gap; they stay placed. Remove deletes only that input. Undo/Redo restore these changes. Drag a placed image to rearrange it; empty-space dragging pans. Pinch to zoom. Show all changes zoom to show the whole assembly; it never changes output dimensions.\n\nSave PNG saves the assembled image directly. Edit in Paint transfers it into the main editor as an undoable replacement. If the output exceeds the memory budget, choose a smaller output copy. Original source files stay unchanged. The current assembly is stored locally and reopens when you return.\n\nThis mode uses the same Catrobat/AGPL and asset credits in the main editor's Help menu.")
    override fun onSaveInstanceState(outState: Bundle) { outState.putString("pending_output",pendingOutput?.name); outState.putInt("sort",sort.ordinal); outState.putString("selected",selected); super.onSaveInstanceState(outState) }
    override fun onBackPressed() { if (!busy) finish() }
    override fun onDestroy() { if (::assembly.isInitialized) assembly.changed = {}; previews.values.forEach { it.recycle() }; previews.clear(); worker.shutdown(); super.onDestroy() }
}
