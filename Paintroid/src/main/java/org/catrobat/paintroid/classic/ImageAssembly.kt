/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.graphics.Rect
import android.util.AtomicFile
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.util.Locale
import kotlin.math.roundToInt

enum class SnapEdge { RIGHT, BOTTOM }
enum class NormalizeAxis { WIDTH, HEIGHT }
data class ImageNormalization(val axis: NormalizeAxis,val pixels: Int)
data class Attachment(val anchor: String?, val edge: SnapEdge?)
data class AssemblyImage(val id: String, val file: File, val name: String, val timestamp: Long?,
    val dimensions: ImageDimensions, val crop: Rect = Rect(0,0,dimensions.width,dimensions.height), val attachment: Attachment? = null, val normalization: ImageNormalization? = null,val pageIndex: Int = 0) {
    init {require(pageIndex>=0)}
    val croppedSize get() = ImageDimensions(crop.width(),crop.height())
    val placedSize: ImageDimensions get() {
        val n = normalization ?: return croppedSize
        require(n.pixels > 0) { ui(R.string.ui_use_a_positive_target_dimension) }
        val base = if (n.axis == NormalizeAxis.WIDTH) crop.width() else crop.height()
        val other = if (n.axis == NormalizeAxis.WIDTH) crop.height() else crop.width()
        require(base > 0 && other > 0) { ui(R.string.ui_the_crop_must_contain_at_least_one_pixel) }
        val scaled = (other.toLong()*n.pixels+base/2)/base
        require(scaled in 1..Int.MAX_VALUE.toLong()) { ui(R.string.ui_the_normalized_image_dimensions_are_outside_android_s) }
        return if (n.axis == NormalizeAxis.WIDTH) ImageDimensions(n.pixels,scaled.toInt()) else ImageDimensions(scaled.toInt(),n.pixels)
    }
}
data class SnapTarget(val attachment: Attachment, val rect: Rect)
enum class AssemblySort(private val labelId: Int) { NAME_ASC(R.string.ui_filename_a_z), NAME_DESC(R.string.ui_filename_z_a), OLDEST(R.string.ui_modified_oldest_first), NEWEST(R.string.ui_modified_newest_first);
    val label: String get() = ui(labelId)
}
data class CropMargins(val left: Double, val top: Double, val right: Double, val bottom: Double, val percent: Boolean) {
    fun rect(size: ImageDimensions): Rect {
        val values = listOf(left,top,right,bottom)
        require(values.all { it.isFinite() && it >= 0 }) { ui(R.string.ui_trim_amounts_must_be_zero_or_greater) }
        fun amount(n: Double, base: Int): Int {
            val p = if (percent) n * base / 100 else n
            require(p <= base && (percent || n == kotlin.math.floor(n))) { ui(R.string.ui_trim_amounts_must_fit_inside_each_image_use) }
            return p.roundToInt()
        }
        val r = Rect(amount(left,size.width),amount(top,size.height),size.width-amount(right,size.width),size.height-amount(bottom,size.height))
        require(r.width() > 0 && r.height() > 0) { ui(R.string.ui_the_trim_would_remove_the_entire_image) }
        return r
    }
}

/** Original files stay on disk. Crops and attachments are reversible metadata edits. */
class ImageAssembly(val directory: File) {
    companion object { const val MAX_IMAGES = 20 }
    private val saved = AtomicFile(File(directory,"project.json"))
    private var state = emptyList<AssemblyImage>()
    private val undo = java.util.ArrayDeque<List<AssemblyImage>>()
    private val redo = java.util.ArrayDeque<List<AssemblyImage>>()
    val images: List<AssemblyImage> get() = state
    val canUndo get() = undo.isNotEmpty()
    val canRedo get() = redo.isNotEmpty()
    var changed: () -> Unit = {}
    init { directory.mkdirs(); if (saved.baseFile.exists()) state = read(); validate(state); prune() }
    fun image(id: String) = state.first { it.id == id }
    fun sorted(sort: AssemblySort): List<AssemblyImage> {
        val name = compareBy<AssemblyImage> { it.name.lowercase(Locale.ROOT) }.thenBy { it.name }.thenBy { it.id }
        return when (sort) {
            AssemblySort.NAME_ASC -> state.sortedWith(name)
            AssemblySort.NAME_DESC -> state.sortedWith(name.reversed())
            else -> state.sortedWith(Comparator { a,b ->
                when {
                    a.timestamp == null && b.timestamp == null -> name.compare(a,b)
                    a.timestamp == null -> 1
                    b.timestamp == null -> -1
                    a.timestamp == b.timestamp -> name.compare(a,b)
                    sort == AssemblySort.OLDEST -> a.timestamp.compareTo(b.timestamp)
                    else -> b.timestamp.compareTo(a.timestamp)
                }
            })
        }
    }
    fun add(items: List<AssemblyImage>) {
        require(state.size + items.size <= MAX_IMAGES) { ui(R.string.ui_an_assembly_can_contain_up_to_20_images_86d995) }
        change(state + items)
    }
    /** Remove one image from the attachment tree and promote its successor into the gap. */
    private fun detached(id: String): List<AssemblyImage> {
        val removed = image(id); val incoming = removed.attachment ?: return state
        val children = state.filter { it.attachment?.anchor == id }
        val promoted = children.firstOrNull { it.attachment?.edge == incoming.edge }
            ?: children.firstOrNull { it.attachment?.edge == SnapEdge.RIGHT } ?: children.firstOrNull()
        var next = state.map { when (it.id) {
            id -> it.copy(attachment = null)
            promoted?.id -> it.copy(attachment = incoming)
            else -> it
        } }
        if (promoted != null) for (child in children.filter { it.id != promoted.id }) {
            val edge = child.attachment!!.edge!!
            var tail = promoted.id
            repeat(MAX_IMAGES) { next.firstOrNull { it.attachment?.anchor == tail && it.attachment.edge == edge }?.let { tail = it.id } }
            next = next.map { if (it.id == child.id) it.copy(attachment = Attachment(tail,edge)) else it }
        }
        return reflow(next)
    }
    fun unplace(id: String) = change(detached(id))
    fun remove(id: String) = change(detached(id).filter { it.id != id })
    fun normalize(axis: NormalizeAxis,pixels: Int) = change(reflow(state.map { it.copy(normalization=ImageNormalization(axis,pixels)) }))
    fun resetSizes() = change(reflow(state.map { it.copy(normalization=null) }))
    /** Preserve valid attachments; if resized branches collide, reattach only those needing room. */
    private fun reflow(items: List<AssemblyImage>): List<AssemblyImage> {
        val desired = layout(items)
        try { validate(items); return items } catch (_: IllegalArgumentException) { }
        var next = items.map { it.copy(attachment=null) }
        val pending = items.filter { it.attachment != null }.toMutableList()
        val done = mutableSetOf<String>()
        while (pending.isNotEmpty()) {
            val item = pending.firstOrNull { it.attachment!!.anchor == null || it.attachment.anchor in done }
                ?: throw IllegalArgumentException(ui(R.string.ui_invalid_image_attachments))
            val alternatives = if (done.isEmpty()) listOf(Attachment(null,null)) else
                listOf(item.attachment!!) + next.filter { it.id in done }.flatMap { anchor -> SnapEdge.values().map { Attachment(anchor.id,it) } }
            var best: List<AssemblyImage>? = null; var distance = Double.POSITIVE_INFINITY
            for ((index,a) in alternatives.distinct().withIndex()) {
                val candidate = next.map { if (it.id == item.id) it.copy(attachment=a) else it }
                try {
                    validate(candidate)
                    val rect = layout(candidate).getValue(item.id); val original = desired.getValue(item.id)
                    val dx=rect.left.toDouble()-original.left; val dy=rect.top.toDouble()-original.top
                    val score = if (index == 0 && a == item.attachment) -1.0 else dx*dx+dy*dy
                    if (score < distance) { best=candidate; distance=score }
                } catch (_: IllegalArgumentException) { }
            }
            next = best ?: throw IllegalArgumentException(ui(R.string.ui_the_images_cannot_fit_within_android_s_coordinate))
            done.add(item.id); pending.remove(item)
        }
        validate(next); return next
    }
    fun clear() = change(emptyList())
    fun crop(ids: Set<String>, margins: CropMargins) {
        require(ids.isNotEmpty()) { ui(R.string.ui_choose_at_least_one_image) }
        change(state.map { if (it.id in ids) it.copy(crop = margins.rect(it.dimensions)) else it })
    }
    fun crop(id: String, rect: Rect) = change(state.map { if (it.id == id) it.copy(crop = Rect(rect)) else it })
    fun crop(crops: Map<String,Rect>) = change(state.map { item -> crops[item.id]?.let { item.copy(crop = Rect(it)) } ?: item })
    fun place(id: String, attachment: Attachment) = change(detached(id).map { if (it.id == id) it.copy(attachment = attachment) else it })
    fun targets(id: String): List<SnapTarget> {
        val item = image(id); val base = detached(id)
        if (base.none { it.attachment != null }) return listOf(SnapTarget(Attachment(null,null),Rect(0,0,item.placedSize.width,item.placedSize.height)))
        return base.filter { it.attachment != null && it.id != id }.flatMap { anchor -> SnapEdge.values().mapNotNull { edge ->
            val a = Attachment(anchor.id,edge)
            try {
                val next = base.map { if (it.id == id) it.copy(attachment = a) else it }
                validate(next); SnapTarget(a,layout(next).getValue(id))
            } catch (_: IllegalArgumentException) { null }
        } }
    }
    fun layoutWithout(id: String) = layout(detached(id))
    fun layout() = layout(state)
    fun size(): ImageDimensions? {
        val rects = layout().values
        return if (rects.isEmpty()) null else ImageDimensions(rects.maxOf { it.right },rects.maxOf { it.bottom })
    }
    private fun layout(items: List<AssemblyImage>): Map<String,Rect> {
        val result = linkedMapOf<String,Rect>(); val resolving = mutableSetOf<String>()
        val byId = items.associateBy { it.id }
        fun resolve(item: AssemblyImage): Rect {
            result[item.id]?.let { return it }
            require(resolving.add(item.id)) { ui(R.string.ui_an_image_cannot_attach_to_itself_or_one) }
            val a = item.attachment ?: throw IllegalArgumentException(ui(R.string.ui_the_attachment_image_is_not_placed))
            var x = 0; var y = 0
            if (a.anchor != null) {
                val parent = resolve(byId[a.anchor] ?: throw IllegalArgumentException(ui(R.string.ui_the_attachment_image_is_missing)))
                require(a.edge != null)
                x = if (a.edge == SnapEdge.RIGHT) parent.right else parent.left
                y = if (a.edge == SnapEdge.BOTTOM) parent.bottom else parent.top
            }
            val size = item.placedSize
            val right = x.toLong()+size.width; val bottom = y.toLong()+size.height
            require(right <= Int.MAX_VALUE && bottom <= Int.MAX_VALUE) { ui(R.string.ui_the_assembly_exceeds_android_s_coordinate_range) }
            val r = Rect(x,y,right.toInt(),bottom.toInt()); result[item.id] = r; resolving.remove(item.id); return r
        }
        items.filter { it.attachment != null }.forEach { resolve(it) }; return result
    }
    private fun validate(items: List<AssemblyImage>) {
        require(items.size <= MAX_IMAGES && items.map { it.id }.distinct().size == items.size)
        require(items.count { it.attachment != null && it.attachment.anchor == null } <= 1) { ui(R.string.ui_the_first_image_starts_at_the_top_left) }
        items.forEach { require(it.crop.left >= 0 && it.crop.top >= 0 && it.crop.right <= it.dimensions.width && it.crop.bottom <= it.dimensions.height && it.crop.width() > 0 && it.crop.height() > 0) { ui(R.string.ui_the_crop_must_stay_inside_the_image) }; it.placedSize }
        val rects = layout(items).values.toList()
        for (i in rects.indices) for (j in i+1 until rects.size) require(!Rect.intersects(rects[i],rects[j])) { ui(R.string.ui_that_arrangement_overlaps_another_image_use_a_different) }
    }
    private fun change(next: List<AssemblyImage>) {
        validate(next); if (next == state) return
        write(next); undo.addLast(state); if (undo.size > 50) undo.removeFirst(); redo.clear(); state = next; prune(); changed()
    }
    fun undo() { if (undo.isNotEmpty()) { val next = undo.last; write(next); undo.removeLast(); redo.addLast(state); state = next; prune(); changed() } }
    fun redo() { if (redo.isNotEmpty()) { val next = redo.last; write(next); redo.removeLast(); undo.addLast(state); state = next; prune(); changed() } }
    private fun prune() {
        val retained = (state + undo.flatMap { it } + redo.flatMap { it }).map { it.file.name }.toSet()
        directory.listFiles()?.filter { it.isFile && it.name.endsWith(".image") && it.name !in retained }?.forEach { it.delete() }
    }
    private fun write(items: List<AssemblyImage>) {
        val list = JSONArray()
        items.forEach { item -> list.put(JSONObject().apply {
            put("id",item.id); put("file",item.file.name); put("name",item.name); put("time",item.timestamp ?: JSONObject.NULL)
            put("width",item.dimensions.width); put("height",item.dimensions.height);put("page",item.pageIndex)
            put("crop",JSONArray(listOf(item.crop.left,item.crop.top,item.crop.right,item.crop.bottom)))
            item.normalization?.let { put("normalize_axis",it.axis.name); put("normalize_pixels",it.pixels) }
            item.attachment?.let { put("placed",true); put("anchor",it.anchor ?: JSONObject.NULL); put("edge",it.edge?.name ?: JSONObject.NULL) }
        }) }
        val stream = saved.startWrite()
        try { stream.write(JSONObject().put("version",3).put("images",list).toString().toByteArray(Charsets.UTF_8)); saved.finishWrite(stream) }
        catch (error: Throwable) { saved.failWrite(stream); throw error }
    }
    private fun read(): List<AssemblyImage> {
        val list = JSONObject(saved.readFully().toString(Charsets.UTF_8)).getJSONArray("images")
        require(list.length() <= MAX_IMAGES)
        return (0 until list.length()).map { i ->
            val o = list.getJSONObject(i); val file = File(directory,o.getString("file"))
            require(file.canonicalFile.parentFile == directory.canonicalFile && file.isFile) { ui(R.string.ui_an_assembly_source_image_is_missing) }
            val c = o.getJSONArray("crop")
            AssemblyImage(o.getString("id"),file,o.getString("name"),if (o.isNull("time")) null else o.getLong("time"),
                ImageDimensions(o.getInt("width"),o.getInt("height")),Rect(c.getInt(0),c.getInt(1),c.getInt(2),c.getInt(3)),
                if (o.optBoolean("placed")) Attachment(if (o.isNull("anchor")) null else o.getString("anchor"),if (o.isNull("edge")) null else SnapEdge.valueOf(o.getString("edge"))) else null,
                if (o.has("normalize_axis")) ImageNormalization(NormalizeAxis.valueOf(o.getString("normalize_axis")),o.getInt("normalize_pixels")) else null,o.optInt("page",0))
        }
    }
}
