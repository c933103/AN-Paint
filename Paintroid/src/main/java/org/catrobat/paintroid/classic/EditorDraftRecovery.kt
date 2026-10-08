/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.BitmapFactory
import android.graphics.Color
import android.graphics.RectF
import org.catrobat.paintroid.R
import org.json.JSONObject
import java.io.File

/** Entirely worker-owned until the editor accepts the matching storage revision. */
internal data class RecoveredEditor(
    val document: PaintDocument,
    val metadata: JSONObject?,
    val restored: Boolean,
    val filename: String,
    val textSettings: TextSettings,
    val savedTarget: SavedTarget?,
    val draftStatus: String,
    val autosaveBlocked: Boolean,
    val lastAutosaveError: String?,
    val recoveryNotice: String?
)

internal fun recoverEditor(context: Context,autosave: AutosaveStore): AutosaveStore.Recovery<RecoveredEditor> = autosave.recover {
    var owner: PaintDocument?=null
    fun checkSize(w: Int,h: Int) {ImageMemoryPolicy.forDevice(context).check(w,h,owner?.residentPixels ?: 0)}
    var filename=ui(R.string.ui_untitled)
    var textSettings=TextSettings()
    var savedTarget: SavedTarget?=null
    var draftStatus=ui(R.string.ui_draft_not_saved_yet)
    var autosaveBlocked=false
    var lastAutosaveError: String?=null
    var recoveryNotice: String?=null
    fun preserveFailedDraft(reason: String) {
        try {
            autosave.preserveForRecovery(retainOriginal=true)
            recoveryNotice=ui(R.string.ui_a_separate_recovery_copy_has_been_kept_use,reason)
            draftStatus=ui(R.string.ui_previous_draft_kept_for_recovery)
        } catch(_: Exception) {
            autosaveBlocked=true
            lastAutosaveError=ui(R.string.ui_the_previous_draft_could_not_be_preserved_separately)
            draftStatus=ui(R.string.ui_autosave_paused_use_save)
            recoveryNotice=ui(R.string.ui_autosave_is_paused_to_protect_that_draft_use,reason)
        }
    }
    try {
        val document: PaintDocument
        document = PaintDocument(historyDirectory = File(context.cacheDir,"classic-history"),
            allocationGuard = { w,h -> checkSize(w,h) }).also {owner=it}
        var recovered: JSONObject?=null
        var restored=false
        if (autosave.exists()) try {
            val draft=autosave.read(historyReader=document::readHistory) { w,h -> checkSize(w,h) }
            recovered=draft.metadata
            textSettings=TextSettings.read(recovered.optJSONObject("text_settings"))
            savedTarget=SavedTarget.read(recovered.optJSONObject("save_target"))
            document.background=recovered.optInt("background",Color.WHITE)
            document.replace(draft.image)
            draft.history?.let {document.restoreHistory(it)}
            if(draft.historyFailed) {
                autosave.preserveForRecovery(retainOriginal=true)
                recoveryNotice=ui(R.string.ui_history_unavailable34)
            }
            draft.floating?.let { image ->
                val r=recovered!!.getJSONArray("floating_rect")
                document.restoreFloatingSelection(image,RectF(r.getDouble(0).toFloat(),r.getDouble(1).toFloat(),r.getDouble(2).toFloat(),r.getDouble(3).toFloat()),recovered!!.optDouble("floating_rotation",0.0).toFloat(),SelectionOutline.read(recovered!!.optJSONArray("selection_outline")))
            }
            document.restoreImageCredits(recovered.optJSONObject("image_credits"))
            filename=recovered.optString("filename",ui(R.string.ui_recovered_image))
            document.foreground=recovered.optInt("foreground",Color.BLACK)
            document.strokeWidth=recovered.optDouble("stroke_width",5.0).toFloat()
            document.cornerRadius=recovered.optDouble("corner_radius",16.0).toFloat().coerceAtLeast(0f)
            document.brushTip=recovered.optInt("brush_tip");document.shapeStyle=recovered.optInt("shape_style")
            document.tolerance=recovered.optDouble("tolerance",0.0).toFloat()
            document.watercolorStrength=recovered.optInt("watercolor_strength",50).coerceIn(1,100)
            document.strokeSmoothing=recovered.optBoolean("stroke_smoothing")
            document.antialiasing=recovered.optBoolean("antialiasing",false)
            document.sprayRadius=recovered.optDouble("spray_radius",document.strokeWidth*2.0).toFloat().coerceIn(1f,100f)
            if (recovered.optBoolean("dirty")) document.edited()
            draftStatus=ui(R.string.ui_draft_restored);restored=true
        } catch (_: Exception) { recovered=null;preserveFailedDraft(ui(R.string.ui_the_previous_draft_could_not_be_restored)) }
          catch (_: OutOfMemoryError) { recovered=null;preserveFailedDraft(ui(R.string.ui_the_previous_draft_needs_more_memory_to_reopen)) }
        if (!restored) {
            val recovery=File(context.filesDir,"classic-recovery.png")
            if (recovery.isFile) try {
                val bounds=BitmapFactory.Options().apply { inJustDecodeBounds=true }
                BitmapFactory.decodeFile(recovery.path,bounds);checkSize(bounds.outWidth,bounds.outHeight)
                BitmapFactory.decodeFile(recovery.path,BitmapFactory.Options().apply { inMutable=true;inScaled=false })?.let {
                    document.replace(it)
                    val old=context.getSharedPreferences("classic",Context.MODE_PRIVATE)
                    filename=old.getString("filename",ui(R.string.ui_recovered_image)) ?: ui(R.string.ui_recovered_image)
                    if (old.getBoolean("dirty",false)) document.edited()
                    restored=true;draftStatus=ui(R.string.ui_draft_restored)
                }
            } catch (_: Exception) { } catch (_: OutOfMemoryError) { }
        }

        RecoveredEditor(document,recovered,restored,filename,textSettings,savedTarget,draftStatus,
            autosaveBlocked,lastAutosaveError,recoveryNotice)
    } catch(error: Throwable) {owner?.close();throw error}
}
