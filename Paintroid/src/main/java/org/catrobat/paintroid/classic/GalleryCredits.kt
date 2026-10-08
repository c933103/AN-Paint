/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.Activity
import android.app.AlertDialog
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.net.Uri
import android.widget.*
import org.catrobat.paintroid.R

/** Publisher attribution is not a claim that every hosted asset has the same author. */
internal object GalleryCredits {
    const val CC_BY_SA = "https://creativecommons.org/licenses/by-sa/4.0/"
    fun credit(source: String, title: String = Uri.parse(source).lastPathSegment.orEmpty().substringBeforeLast('.'),
        provider: IllustrationSource=IllustrationSource.CATROBAT,page: String="",author: String="",licence: String="",authorUrl: String=""): String {
        val lines=mutableListOf(ui(R.string.gallery_credit_title,title.ifBlank {ui(R.string.ui_gallery_image)}))
        if(provider==IllustrationSource.CATROBAT) {
            lines.add(ui(R.string.gallery_credit_publisher))
            lines.add(ui(R.string.gallery_credit_source,source))
            lines.add(ui(R.string.gallery_credit_gallery,MediaGalleryActivity.GALLERY))
            lines.add(ui(R.string.gallery_credit_licence,licence.ifBlank {CC_BY_SA}))
        } else {
            lines.add(when {
                author.isNotBlank() -> provider.label
                provider==IllustrationSource.IRASUTOYA -> "Irasutoya — Takashi Mifune"
                else -> "Openclipart — "+ui(R.string.ui_creator_on_source34)
            })
            lines.add(ui(R.string.gallery_credit_source,page.takeIf {provider.isArtworkPage(Uri.parse(it))} ?: provider.home))
            lines.add(ui(R.string.gallery_credit_source,source))
            lines.add(licence.ifBlank {if(provider==IllustrationSource.IRASUTOYA) ui(R.string.ui_irasutoya_credit34)
                else "CC0 1.0 — https://creativecommons.org/publicdomain/zero/1.0/"})
            lines.add(provider.terms)
        }
        lines.addAll(listOf(author,authorUrl).filter {it.isNotBlank()})
        return lines.joinToString("\n")
    }
    internal var publishClipboard: (Context,ClipData)->Unit = {context,clip ->
        (context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).setPrimaryClip(clip)
    }
    fun copy(context: Context, text: String, anchor: android.view.View? = null): Boolean {
        try {publishClipboard(context,ClipData.newPlainText(ui(R.string.ui_image_credits),text))}
        catch(_: Exception) {
            // Binder/provider rejection must not roll back an accepted Save or claim Copied.
            LocaleTypography.showMessage(context,ui(R.string.ui_could_not_complete_the_operation),Toast.LENGTH_LONG,anchor)
            return false
        }
        LocaleTypography.showMessage(context,ui(R.string.gallery_credit_copied),Toast.LENGTH_SHORT,anchor)
        return true
    }

    /** An open field is a draft until one of the existing explicit save actions runs. */
    data class EditorDraft(val source: String, val text: String)
    class EditorSession(val dialog: AlertDialog, val snapshot: ()->EditorDraft) {
        internal var preserving=false
        fun dismissForRecreation() {preserving=true;dialog.dismiss()}
    }

    /** Editing is optional and separate from insertion. Footer stays outside scrolling text. */
    fun showEditor(activity: Activity, credits: List<ImageCredit>, onEdit: (String,String)->Unit): EditorSession? =
        showEditor(activity,credits,null,onEdit)

    fun showEditor(activity: Activity, credits: List<ImageCredit>, draft: EditorDraft?,
        onEdit: (String,String)->Unit): EditorSession? = showEditor(activity,credits,draft,onEdit,{})

    fun showEditor(activity: Activity, credits: List<ImageCredit>, draft: EditorDraft?,
        onEdit: (String,String)->Unit, onDismiss: ()->Unit): EditorSession? = try {
        CreditSessionJson.withResources {buildEditor(activity,credits,draft,onEdit,onDismiss)}
    } catch(_: java.io.IOException) {
        LocaleTypography.showMessage(activity,ui(R.string.gallery_credit_could_not_save),Toast.LENGTH_LONG)
        null
    }

    private fun buildEditor(activity: Activity, credits: List<ImageCredit>, draft: EditorDraft?,
        onEdit: (String,String)->Unit, onDismiss: ()->Unit): EditorSession? {
        val entries=credits.associateBy {it.source}.toMutableMap()
        val sources=entries.keys.sorted()
        if(sources.isEmpty()) { LocaleTypography.showMessage(activity,ui(R.string.ui_no_gallery_images_have_been_inserted),Toast.LENGTH_SHORT);return null }
        fun dp(n: Int)=(n*activity.resources.displayMetrics.density+.5f).toInt()
        val body=LinearLayout(activity).apply {orientation=LinearLayout.VERTICAL;setPadding(dp(12),dp(12),dp(12),dp(8));setBackgroundColor(EditorColours.surface)}
        body.addView(TextView(activity).apply {text=ui(R.string.gallery_credit_edit_hint);textSize=13f;setTextColor(EditorColours.onSurface)})
        val picker=Spinner(activity).apply {
            tag="gallery_credit_source"
            adapter=ArrayAdapter(activity,android.R.layout.simple_spinner_dropdown_item,sources.map {Uri.parse(it).lastPathSegment ?: it})
        }
        body.addView(picker)
        val field=EditText(activity).apply {isSaveEnabled=false;isSaveFromParentEnabled=false;tag="gallery_credit_text";minLines=6;maxLines=12;gravity=android.view.Gravity.TOP;setTextColor(EditorColours.onSurface);setSelectAllOnFocus(false)}
        body.addView(field,LinearLayout.LayoutParams(-1,-2))
        val restoredIndex=draft?.source?.let {sources.indexOf(it)} ?: -1
        var selected=restoredIndex.takeIf {it>=0} ?: 0
        fun save(): Boolean {
            val source=sources[selected]
            val text: String
            try {
                // Necessary existing-format check before either the String copy or any caller's
                // prospective history/metadata serialization. It never changes the raw field.
                require(CreditSessionJson.fitsInline(field.text,AutosaveStore.MAX_METADATA_BYTES))
                text=CreditSessionJson.snapshot(source,field.text).text
                CreditSessionJson.withResources {onEdit(source,text)}
            }
            catch(_: IllegalArgumentException) {
                LocaleTypography.showMessage(activity,ui(R.string.gallery_credit_too_large),Toast.LENGTH_LONG,field);return false
            } catch(_: java.io.IOException) {
                LocaleTypography.showMessage(activity,ui(R.string.gallery_credit_could_not_save),Toast.LENGTH_LONG,field);return false
            }
            entries[source]=ImageCredit(source,text)
            return true
        }
        val initialText=if(restoredIndex>=0) draft!!.text else entries.getValue(sources[selected]).text
        CreditSessionJson.checkText(initialText)
        field.setText(initialText)
        // Install the initial choice before the listener, so restoration does not save a field.
        picker.setSelection(selected,false)
        picker.onItemSelectedListener=object: AdapterView.OnItemSelectedListener {
            override fun onNothingSelected(parent: AdapterView<*>?)=Unit
            override fun onItemSelected(parent: AdapterView<*>?,view: android.view.View?,position: Int,id: Long) {
                if(position==selected)return
                if(!save()) {picker.setSelection(selected,false);return}
                selected=position;field.setText(entries.getValue(sources[position]).text)
            }
        }
        val dialog=EditorDialogBuilder(activity).setTitle(ui(R.string.ui_image_credits))
            .setView(ScrollView(activity).apply {addView(body)})
            .setNegativeButton(ui(R.string.gallery_copy_credit),null)
            .setNeutralButton(ui(R.string.ui_save),null)
            .setPositiveButton(ui(R.string.ui_done),null).create()
        dialog.setOnShowListener {
            fun action(which: Int,tagName: String,run: ()->Unit) {
                dialog.getButton(which).apply {tag=tagName;setOnClickListener {run()}}
            }
            action(AlertDialog.BUTTON_NEGATIVE,"gallery_credit_copy") {if(save()) copy(activity,entries.getValue(sources[selected]).text,field)}
            action(AlertDialog.BUTTON_NEUTRAL,"gallery_credit_save") {if(save()) LocaleTypography.showMessage(activity,ui(R.string.gallery_credit_saved),Toast.LENGTH_SHORT,field)}
            action(AlertDialog.BUTTON_POSITIVE,"gallery_credit_done") {if(save()) dialog.dismiss()}
        }
        val session=EditorSession(dialog) {CreditSessionJson.snapshot(sources[selected],field.text)}
        dialog.setOnDismissListener {if(!session.preserving) onDismiss()}
        dialog.show()
        return session
    }
}
