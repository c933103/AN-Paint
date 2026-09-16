/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.Activity
import android.app.Dialog
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.net.Uri
import android.view.Window
import android.widget.*
import org.catrobat.paintroid.R

/** Publisher attribution is not a claim that every hosted asset has the same author. */
internal object GalleryCredits {
    const val CC_BY_SA = "https://creativecommons.org/licenses/by-sa/4.0/"
    private fun preferences(context: Context) = context.getSharedPreferences("image-credits",Context.MODE_PRIVATE)
    fun sources(context: Context): Set<String> = preferences(context).getStringSet("sources",emptySet()).orEmpty().toSet()
    fun remember(context: Context, source: String,provider: IllustrationSource=IllustrationSource.CATROBAT,page: String="",title: String="") {
        val edit=preferences(context).edit().putStringSet("sources",sources(context)+source)
        if(provider!=IllustrationSource.CATROBAT || title.isNotBlank()) edit.putString("generated:$source",credit(source,title,provider,page))
        edit.apply()
    }
    fun credit(source: String, title: String = Uri.parse(source).lastPathSegment.orEmpty().substringBeforeLast('.'),provider: IllustrationSource=IllustrationSource.CATROBAT,page: String=""): String = if(provider==IllustrationSource.CATROBAT) listOf(
        ui(R.string.gallery_credit_title,title.ifBlank { ui(R.string.ui_gallery_image) }),
        ui(R.string.gallery_credit_publisher),
        ui(R.string.gallery_credit_source,source),
        ui(R.string.gallery_credit_gallery,MediaGalleryActivity.GALLERY),
        ui(R.string.gallery_credit_licence,CC_BY_SA)
    ).joinToString("\n")
    else listOf(ui(R.string.gallery_credit_title,title.ifBlank {ui(R.string.ui_gallery_image)}),
        if(provider==IllustrationSource.IRASUTOYA) "Irasutoya — Takashi Mifune" else "Openclipart — "+ui(R.string.ui_creator_on_source34),
        ui(R.string.gallery_credit_source,page.takeIf {provider.isArtworkPage(Uri.parse(it))} ?: provider.home),
        ui(R.string.gallery_credit_source,source),
        if(provider==IllustrationSource.IRASUTOYA) ui(R.string.ui_irasutoya_credit34) else "CC0 1.0 — https://creativecommons.org/publicdomain/zero/1.0/",
        provider.terms).joinToString("\n")
    private fun sourceText(context: Context, source: String): String = preferences(context).getString("text:$source",null)
        ?: preferences(context).getString("generated:$source",null) ?: credit(source)
    fun text(context: Context): String = sources(context).sorted().map { sourceText(context,it) }.filter {it.isNotBlank()}.joinToString("\n\n")
    fun copy(context: Context, text: String) {
        (context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager)
            .setPrimaryClip(ClipData.newPlainText(ui(R.string.ui_image_credits),text))
        Toast.makeText(context,ui(R.string.gallery_credit_copied),Toast.LENGTH_SHORT).show()
    }

    /** Editing is optional and separate from insertion. Footer stays outside scrolling text. */
    fun showEditor(activity: Activity) {
        val sources=sources(activity).sorted()
        if(sources.isEmpty()) { Toast.makeText(activity,ui(R.string.ui_no_gallery_images_have_been_inserted),Toast.LENGTH_SHORT).show();return }
        fun dp(n: Int)=(n*activity.resources.displayMetrics.density+.5f).toInt()
        val dialog=Dialog(activity).apply {requestWindowFeature(Window.FEATURE_NO_TITLE)}
        val body=LinearLayout(activity).apply {orientation=LinearLayout.VERTICAL;setPadding(dp(12),dp(12),dp(12),dp(8));setBackgroundColor(EditorColours.surface)}
        body.addView(TextView(activity).apply {text=ui(R.string.gallery_credit_edit_hint);textSize=13f;setTextColor(EditorColours.onSurface)})
        val picker=Spinner(activity).apply {
            tag="gallery_credit_source"
            adapter=ArrayAdapter(activity,android.R.layout.simple_spinner_dropdown_item,sources.map {Uri.parse(it).lastPathSegment ?: it})
        }
        body.addView(picker)
        val field=EditText(activity).apply {tag="gallery_credit_text";gravity=android.view.Gravity.TOP;setTextColor(EditorColours.onSurface);setSelectAllOnFocus(false)}
        body.addView(field,LinearLayout.LayoutParams(-1,0,1f))
        var selected=0
        fun save() {preferences(activity).edit().putString("text:${sources[selected]}",field.text.toString()).apply()}
        field.setText(sourceText(activity,sources[0]))
        picker.onItemSelectedListener=object: AdapterView.OnItemSelectedListener {
            override fun onNothingSelected(parent: AdapterView<*>?)=Unit
            override fun onItemSelected(parent: AdapterView<*>?,view: android.view.View?,position: Int,id: Long) {
                if(position==selected)return
                save();selected=position;field.setText(sourceText(activity,sources[position]))
            }
        }
        val actions=LinearLayout(activity)
        fun action(label: String,tagName: String,run: ()->Unit) {
            actions.addView(Button(activity).apply {text=label;tag=tagName;isAllCaps=false;minWidth=0;setOnClickListener {run()}},LinearLayout.LayoutParams(0,dp(48),1f))
        }
        action(ui(R.string.gallery_copy_credit),"gallery_credit_copy") {save();copy(activity,field.text.toString())}
        action(ui(R.string.ui_save),"gallery_credit_save") {save();Toast.makeText(activity,ui(R.string.gallery_credit_saved),Toast.LENGTH_SHORT).show()}
        action(ui(R.string.ui_done),"gallery_credit_done") {save();dialog.dismiss()}
        body.addView(actions)
        dialog.setContentView(body)
        dialog.window?.setLayout(-1,(activity.resources.displayMetrics.heightPixels*.85f).toInt())
        dialog.show()
        dialog.window?.setLayout(-1,(activity.resources.displayMetrics.heightPixels*.85f).toInt())
    }
}
