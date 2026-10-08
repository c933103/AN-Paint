/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.*
import org.catrobat.paintroid.R
import java.io.IOException
import java.util.concurrent.Executors

/** Saved earlier credits stay separate until the user chooses one exact record to attach. */
class LegacyImageCreditsActivity : Activity() {
    companion object {
        const val EXTRA_SELECTED_TOKEN = "legacy_image_credit_token"
        const val EXPORT_TEXT = 1
    }
    override fun attachBaseContext(base: Context) {super.attachBaseContext(AppLanguage.wrap(base))}
    private var records: List<ImageCreditArchive.Record> = emptyList()
    private var selected=0
    private var page=0
    private var pendingExportToken: String?=null
    private val worker=Executors.newSingleThreadExecutor()
    private lateinit var status: TextView

    override fun onCreate(state: Bundle?) {
        super.onCreate(state)
        val archive=ImageCreditArchive.contents(this)
        records=archive.records
        val restored=records.indexOfFirst {it.token==state?.getString("selected_token")}
        selected=restored.takeIf {it>=0} ?: 0
        page=if(restored>=0) state?.getInt("page",0) ?: 0 else 0
        pendingExportToken=state?.getString("export_token")
        fun dp(n: Int)=(n*resources.displayMetrics.density+.5f).toInt()
        val body=LinearLayout(this).apply {
            orientation=LinearLayout.VERTICAL;fitsSystemWindows=true
            setPadding(dp(12),dp(12),dp(12),dp(12));setBackgroundColor(EditorColours.surface)
        }
        body.addView(TextView(this).apply {
            text=ui(R.string.legacy_credits_title);textSize=20f;setTextColor(EditorColours.onSurface)
        })
        body.addView(TextView(this).apply {
            text=ui(R.string.legacy_credits_hint);setTextColor(EditorColours.onSurface)
        })
        val creditText=TextView(this).apply {
            tag="legacy_credit_text";textDirection=View.TEXT_DIRECTION_FIRST_STRONG
            setTextColor(EditorColours.onSurface)
            // Text selection can send arbitrary text through ClipboardManager/Binder.
            // Display bounded pages and offer a complete streamed text export.
            setTextIsSelectable(false);isSaveEnabled=false;freezesText=false
        }
        val creditScroll=ScrollView(this).apply {addView(creditText)}
        var pages=ImageCreditTextPages(records.getOrNull(selected)?.credit?.text.orEmpty())
        val pageCounter=TextView(this).apply {tag="legacy_credit_page";setTextColor(EditorColours.onSurface)}
        val previous=Button(this).apply {text=ui(R.string.formats22_previous_page);tag="legacy_credit_previous";isAllCaps=false}
        val next=Button(this).apply {text=ui(R.string.formats22_next_page);tag="legacy_credit_next";isAllCaps=false}
        val navigation=LinearLayout(this).apply {
            addView(previous,LinearLayout.LayoutParams(0,-2,1f))
            addView(pageCounter,LinearLayout.LayoutParams(-2,-2))
            addView(next,LinearLayout.LayoutParams(0,-2,1f))
        }
        fun updatePage() {
            page=page.coerceIn(0,pages.count-1)
            creditText.text=if(records.isEmpty()) "" else pages.text(page)
            pageCounter.text="${page+1} / ${pages.count}"
            previous.isEnabled=page>0;next.isEnabled=page+1<pages.count
            navigation.visibility=if(pages.count>1)View.VISIBLE else View.GONE
            creditScroll.scrollTo(0,0)
        }
        previous.setOnClickListener {page--;updatePage()}
        next.setOnClickListener {page++;updatePage()}
        val picker=Spinner(this).apply {
            tag="legacy_credit_source";isSaveEnabled=false
            adapter=ArrayAdapter(this@LegacyImageCreditsActivity,
                android.R.layout.simple_spinner_dropdown_item,records.map {it.credit.source})
            setSelection(selected,false)
            onItemSelectedListener=object: AdapterView.OnItemSelectedListener {
                override fun onNothingSelected(parent: AdapterView<*>?)=Unit
                override fun onItemSelected(parent: AdapterView<*>?,view: View?,position: Int,id: Long) {
                    if(position==selected)return
                    selected=position;page=0;pages=ImageCreditTextPages(records[position].credit.text);updatePage()
                }
            }
        }
        body.addView(picker)
        updatePage()
        body.addView(creditScroll,LinearLayout.LayoutParams(-1,0,1f));body.addView(navigation)
        status=TextView(this).apply {
            tag="legacy_credit_status";setTextColor(EditorColours.onSurface)
            if(archive.unreadableSnapshots>0)text=ui(R.string.legacy_credits_unreadable)
        }
        body.addView(status)
        fun action(label: String, tagName: String, run: ()->Unit) {
            body.addView(Button(this).apply {
                text=label;tag=tagName;isAllCaps=false;setOnClickListener {run()}
                isEnabled=records.isNotEmpty() || tagName=="legacy_credit_done"
            },LinearLayout.LayoutParams(-1,-2))
        }
        action(ui(R.string.legacy_credits_add),"legacy_credit_add") {
            records.getOrNull(selected)?.let {record ->
                setResult(RESULT_OK,Intent().putExtra(EXTRA_SELECTED_TOKEN,record.token))
                finish()
            }
        }
        action(ui(R.string.legacy_credits_save_text),"legacy_credit_export") {
            records.getOrNull(selected)?.let {record ->
                pendingExportToken=record.token
                try {
                    startActivityForResult(Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
                        addCategory(Intent.CATEGORY_OPENABLE);type="text/plain"
                        putExtra(Intent.EXTRA_TITLE,"AN-Paint-legacy-credit.txt")
                    },EXPORT_TEXT)
                } catch(_: Exception) {
                    pendingExportToken=null;status.text=ui(R.string.ui_android_could_not_find_a_file_picker_enable)
                }
            }
        }
        action(ui(R.string.ui_done),"legacy_credit_done") {finish()}
        setContentView(body);LocaleTypography.install(body)
    }

    public override fun onActivityResult(requestCode: Int,resultCode: Int,data: Intent?) {
        super.onActivityResult(requestCode,resultCode,data)
        if(requestCode!=EXPORT_TEXT)return
        val token=pendingExportToken;pendingExportToken=null
        if(resultCode!=RESULT_OK)return
        val uri=data?.data ?: return
        // ACTION_CREATE_DOCUMENT returns a provider destination. Never let a
        // returned file: URI truncate this app's private draft/archive files.
        // Our own FileProvider is for sharing cache/images, not SAF destinations;
        // strip Android's optional user-id prefix before rejecting that authority.
        if(uri.scheme!="content" || uri.authority.isNullOrEmpty() ||
            uri.authority?.substringAfterLast('@')=="$packageName.fileprovider") {
            status.text=ui(R.string.ui_could_not_complete_the_operation);return
        }
        val credit=records.singleOrNull {it.token==token}?.credit ?: ImageCreditArchive.find(this,token)
        if(credit==null) {status.text=ui(R.string.ui_could_not_complete_the_operation);return}
        status.text=ui(R.string.ui_working)
        worker.execute {
            val failure=try {
                val stream=contentResolver.openOutputStream(uri,"wt") ?: throw IOException("No output stream")
                stream.writer(Charsets.UTF_8).use {it.write(credit.text)}
                null
            } catch(error: Exception) {error}
            runOnUiThread {if(!isDestroyed) status.text=ui(if(failure==null)
                R.string.gallery_credit_saved else R.string.ui_could_not_complete_the_operation)}
        }
    }

    override fun onSaveInstanceState(state: Bundle) {
        state.putString("selected_token",records.getOrNull(selected)?.token);state.putInt("page",page)
        state.putString("export_token",pendingExportToken)
        super.onSaveInstanceState(state)
    }
    override fun onDestroy() {worker.shutdown();super.onDestroy()}
}
