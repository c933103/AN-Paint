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
    fun copy(context: Context, text: String) {
        (context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager)
            .setPrimaryClip(ClipData.newPlainText(ui(R.string.ui_image_credits),text))
        Toast.makeText(context,ui(R.string.gallery_credit_copied),Toast.LENGTH_SHORT).show()
    }

    /** Editing is optional and separate from insertion. Footer stays outside scrolling text. */
    fun showEditor(activity: Activity, credits: List<ImageCredit>, onEdit: (String,String)->Unit) {
        val entries=credits.associateBy {it.source}.toMutableMap()
        val sources=entries.keys.sorted()
        if(sources.isEmpty()) { Toast.makeText(activity,ui(R.string.ui_no_gallery_images_have_been_inserted),Toast.LENGTH_SHORT).show();return }
        fun dp(n: Int)=(n*activity.resources.displayMetrics.density+.5f).toInt()
        val body=LinearLayout(activity).apply {orientation=LinearLayout.VERTICAL;setPadding(dp(12),dp(12),dp(12),dp(8));setBackgroundColor(EditorColours.surface)}
        body.addView(TextView(activity).apply {text=ui(R.string.gallery_credit_edit_hint);textSize=13f;setTextColor(EditorColours.onSurface)})
        val picker=Spinner(activity).apply {
            tag="gallery_credit_source"
            adapter=ArrayAdapter(activity,android.R.layout.simple_spinner_dropdown_item,sources.map {Uri.parse(it).lastPathSegment ?: it})
        }
        body.addView(picker)
        val field=EditText(activity).apply {tag="gallery_credit_text";minLines=6;maxLines=12;gravity=android.view.Gravity.TOP;setTextColor(EditorColours.onSurface);setSelectAllOnFocus(false)}
        body.addView(field,LinearLayout.LayoutParams(-1,-2))
        var selected=0
        fun save() {
            val source=sources[selected];val text=field.text.toString()
            entries[source]=ImageCredit(source,text);onEdit(source,text)
        }
        field.setText(entries.getValue(sources[0]).text)
        picker.onItemSelectedListener=object: AdapterView.OnItemSelectedListener {
            override fun onNothingSelected(parent: AdapterView<*>?)=Unit
            override fun onItemSelected(parent: AdapterView<*>?,view: android.view.View?,position: Int,id: Long) {
                if(position==selected)return
                save();selected=position;field.setText(entries.getValue(sources[position]).text)
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
            action(AlertDialog.BUTTON_NEGATIVE,"gallery_credit_copy") {save();copy(activity,field.text.toString())}
            action(AlertDialog.BUTTON_NEUTRAL,"gallery_credit_save") {save();Toast.makeText(activity,ui(R.string.gallery_credit_saved),Toast.LENGTH_SHORT).show()}
            action(AlertDialog.BUTTON_POSITIVE,"gallery_credit_done") {save();dialog.dismiss()}
        }
        dialog.show()
    }
}
