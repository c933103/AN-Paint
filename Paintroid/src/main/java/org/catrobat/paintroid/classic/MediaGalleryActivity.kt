/* AN Paint, 2026-09-10. AGPL-3.0-or-later.
 * Online illustrations retain their publisher's individual credits and terms.
 * Catrobat, Irasutoya, Openclipart and Wikimedia Commons media are not bundled in the application.
 */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.app.Activity
import android.content.Intent
import android.content.res.Configuration
import android.net.Uri
import android.os.Bundle
import android.view.View
import android.webkit.*
import android.widget.*
import java.io.File
import java.net.HttpURLConnection
import java.net.URL
import java.io.InterruptedIOException
import java.util.concurrent.Executors

class MediaGalleryActivity : Activity() {
    override fun attachBaseContext(base: android.content.Context) { super.attachBaseContext(AppLanguage.wrap(base)) }
    companion object {
        private const val LEGACY_CREDITS=1
        const val GALLERY="https://catrobat.org/figures-download/"
        const val LICENCE="https://developer.catrobat.org/pages/legal/licenses/catrobat/"
        fun allowed(uri: Uri)=IllustrationSource.CATROBAT.allowsPage(uri)
    }
    private val provider by lazy {IllustrationSource.fromId(intent.getStringExtra("gallery_provider"))}
    private var documentCredits: List<ImageCredit> = emptyList()
    private lateinit var creditSession: CreditEditSession
    private var creditsEdited=false
    private var sessionHandedBack=false
    private var creditEditor: GalleryCredits.EditorSession?=null
    private var creditSessionError: android.app.AlertDialog?=null
    private var unrestoredSessionToken: String?=null
    private var pendingSearch: String?=null
    private lateinit var web: WebView
    private lateinit var status: TextView
    private lateinit var statusHost: View
    private lateinit var controlsScroll: GalleryControlsScroll
    private val worker=Executors.newSingleThreadExecutor()
    internal var openConnection: (URL)->HttpURLConnection = { it.openConnection() as HttpURLConnection }
    @Volatile private var activeConnection: HttpURLConnection?=null
    @Volatile internal var downloading=false; private set
    override fun onCreate(state: Bundle?) {
        super.onCreate(state)
        val sessionToken=state?.getString(CreditEditSession.EXTRA_SESSION) ?: intent.getStringExtra(CreditEditSession.EXTRA_SESSION)
        unrestoredSessionToken=sessionToken
        try {
            creditSession=if(sessionToken!=null) CreditEditSession.open(filesDir,sessionToken) else {
                val credits=ImageCredit.read(org.json.JSONArray(state?.getString("document_image_credits")
                    ?: intent.getStringExtra("document_image_credits") ?: "[]"))
                CreditEditSession.create(filesDir,credits,CreditEditContext.ledgerOnly(credits))
            }
        } catch(_: Exception) {
            // Keep the explanation visible until dismissed. Finishing immediately would
            // detach the app-window Nôm notice before the user could read it.
            creditSessionError=EditorDialogBuilder(this).setMessage(ui(R.string.gallery_credit_could_not_save))
                .setPositiveButton(ui(R.string.ui_done)) {_,_->finish()}
                .setOnCancelListener {finish()}.show()
            return // Keep the original file/intent unchanged for explicit recovery.
        }
        unrestoredSessionToken=null
        documentCredits=creditSession.credits
        creditsEdited=creditSession.accepted || state?.getBoolean("document_image_credits_edited")==true
        if(creditsEdited) returnEditedCredits()
        fun dp(n: Int)=(n*resources.displayMetrics.density+.5f).toInt()
        val root=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL;fitsSystemWindows=true;setBackgroundColor(EditorColours.surface)}
        val controls=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL;tag="gallery_controls"}
        controlsScroll=GalleryControlsScroll(this).apply {tag="gallery_controls_scroll";addView(controls)}
        root.addView(controlsScroll,LinearLayout.LayoutParams(-1,-2))
        val description=TextView(this).apply {
            tag="gallery_description";text=provider.label+"\n"+ui(provider.descriptionId);textSize=13f
            setTextColor(EditorColours.onSurface);setPadding(dp(12),dp(8),dp(12),dp(8))
            VerticalUi.caption(this,64)
        }
        val descriptionContent=if(VerticalText.uiVertical()) ColumnScrollView(this).apply {
            tag="gallery_description_columns";addView(description)
        } else description
        controls.addView(descriptionContent,LinearLayout.LayoutParams(-1,-2))
        status=TextView(this).apply {
            tag="gallery_status";visibility=View.GONE;setTextColor(EditorColours.onSurface);setPadding(dp(12),0,dp(12),dp(4))
            accessibilityLiveRegion=View.ACCESSIBILITY_LIVE_REGION_POLITE
            VerticalUi.caption(this,144)
        }
        statusHost=if(VerticalText.uiVertical()) ColumnScrollView(this).apply {
            tag="gallery_status_columns";visibility=View.GONE;addView(status)
        } else status
        controls.addView(statusHost)
        val row=GalleryActions(this).apply {tag="gallery_actions"}
        fun action(label: String,tagName: String,run: ()->Unit) {
            row.addView(galleryButton(this,label,tagName,12f,run=run))
        }
        fun actionRow(actions: GalleryActions): View=if(VerticalText.uiVertical()) ColumnScrollView(this).apply {
            addView(actions)
        } else actions
        action(ui(R.string.ui_copy_all),"gallery_copy_credits") {
            val credits=ImageCredit.text(documentCredits)
            if(credits.isBlank()) LocaleTypography.showMessage(this,ui(R.string.ui_no_gallery_images_have_been_inserted),Toast.LENGTH_SHORT)
            else GalleryCredits.copy(this,credits)
        }
        action(ui(R.string.gallery_edit_credits),"gallery_edit_credits") {showCreditEditor()}
        action(ui(R.string.ui_credits_terms),"gallery_terms") {openExternal(Uri.parse(provider.terms))}
        action(ui(R.string.ui_done),"gallery_done") {finish()};controls.addView(actionRow(row))
        if(ImageCreditArchive.hasRecords(this)) {
            val legacy=GalleryActions(this).apply {
                addView(galleryButton(this@MediaGalleryActivity,ui(R.string.legacy_credits_title),"gallery_legacy_credits") {
                    startActivityForResult(Intent(this@MediaGalleryActivity,LegacyImageCreditsActivity::class.java),LEGACY_CREDITS)
                })
            }
            controls.addView(actionRow(legacy))
        }
        val navigation=GalleryActions(this).apply {tag="gallery_navigation"}
        navigation.addView(galleryButton(this,"←","gallery_back",verticalCaption=false) {
            if(web.canGoBack()) web.goBack() else web.loadUrl(provider.home)
        }.apply {contentDescription=ui(R.string.ui_gallery_back34)})
        val searchLabel=ui(if(provider==IllustrationSource.IRASUTOYA) R.string.ui_search_english34 else R.string.ui_search34)
        val search=gallerySearchField(this,searchLabel)
        if(VerticalText.uiVertical()) {
            // Keep editing in Android's native field; the label uses the same
            // script-aware columns as the rest of the surrounding app controls.
            val caption=TextView(this).apply {
                text=searchLabel;labelFor=search.id;tag="gallery_search_label"
                setTextColor(EditorColours.onSurface);setPadding(dp(12),0,dp(12),0)
                VerticalUi.caption(this,96)
            }
            search.hint=null
            controls.addView(ColumnScrollView(this).apply {addView(caption)})
        }
        controls.addView(search,LinearLayout.LayoutParams(-1,-2))
        fun searchNow() {
            val query=search.text.toString().trim().take(512);if(query.isEmpty())return
            when(provider) {
                IllustrationSource.IRASUTOYA-> {
                    if(provider.allowsPage(Uri.parse(web.url ?: "")) && Uri.parse(web.url ?: "").host!="cse.google.com") {
                        web.evaluateJavascript(IllustrationPage.searchIrasutoya(query)) {result ->
                            if(result!="true") {pendingSearch=query;web.loadUrl(provider.home)}
                        }
                    } else {pendingSearch=query;web.loadUrl(provider.home)}
                }
                IllustrationSource.OPENCLIPART->web.loadUrl(Uri.parse(provider.home+"search/").buildUpon().appendQueryParameter("query",query).build().toString())
                IllustrationSource.CATROBAT->web.findAllAsync(query)
                IllustrationSource.COMMONS->web.loadUrl(Uri.parse("https://commons.wikimedia.org/w/index.php")
                    .buildUpon().appendQueryParameter("search",query+" incategory:\"Blank maps\"")
                    .appendQueryParameter("title","Special:MediaSearch").build().toString())
            }
        }
        navigation.addView(galleryButton(this,ui(R.string.ui_search34),"gallery_search_go") {searchNow()})
        search.setOnEditorActionListener {_,_,_->searchNow();true}
        controls.addView(actionRow(navigation))
        web=WebView(this).apply {
            settings.javaScriptEnabled=true;settings.allowFileAccess=false;settings.allowContentAccess=false
            settings.domStorageEnabled=true;settings.mixedContentMode=WebSettings.MIXED_CONTENT_NEVER_ALLOW
            setDownloadListener {url,_,_,_,_ -> insert(Uri.parse(url))}
            webViewClient=object: WebViewClient() {
                override fun shouldOverrideUrlLoading(view: WebView,url: String): Boolean {
                    val uri=Uri.parse(url)
                    // Older artwork pages and the search home link still publish HTTP URLs.
                    // Upgrade only this provider's supported destinations before navigating.
                    if(uri.scheme=="http") {
                        val https=uri.buildUpon().scheme("https").build()
                        if(provider.allowsImage(https)) {insert(https);return true}
                        if(provider.allowsPage(https)) {view.loadUrl(https.toString());return true}
                    }
                    if(uri.scheme in setOf(GalleryPage.CREDIT_SCHEME,IllustrationPage.USE_SCHEME)) {
                        if(!uri.isHierarchical || uri.host !in setOf("copy","insert")) return true
                        val source=uri.getQueryParameter("source")?.let {Uri.parse(it)}
                        val page=uri.getQueryParameter("page")?.takeIf {provider.isArtworkPage(Uri.parse(it))} ?: web.url.orEmpty()
                        if(source!=null && provider.allowsImage(source) && (provider==IllustrationSource.CATROBAT || provider.isArtworkPage(Uri.parse(page)))) {
                            val title=uri.getQueryParameter("title").orEmpty().take(512)
                            val author=uri.getQueryParameter("author").orEmpty().take(1024)
                            val licence=uri.getQueryParameter("licence").orEmpty().take(4096)
                            val authorUrl=uri.getQueryParameter("author_url").orEmpty().take(4096)
                            if(uri.scheme==GalleryPage.CREDIT_SCHEME) {
                                if(provider==IllustrationSource.COMMONS) copyCommonsCredit(source,page)
                                else GalleryCredits.copy(this@MediaGalleryActivity,GalleryCredits.credit(source.toString(),title,provider,page,author,licence,authorUrl))
                            } else insert(source,page,title,author,licence,authorUrl)
                        }
                        return true
                    }
                    if(provider.allowsImage(uri)) {insert(uri);return true}
                    if(!provider.allowsPage(uri)) {if(uri.scheme=="https") openExternal(uri);return true}
                    return false
                }
                override fun onPageFinished(view: WebView,url: String) {
                    if(provider.allowsPage(Uri.parse(url))) {
                        view.evaluateJavascript(GalleryTypography.script(this@MediaGalleryActivity,AppLanguage.locale(this@MediaGalleryActivity))+IllustrationPage.script(provider,ui(R.string.gallery_use_image),ui(R.string.gallery_copy_credit)),null)
                        pendingSearch?.let {query ->pendingSearch=null;view.evaluateJavascript(IllustrationPage.searchIrasutoya(query),null)}
                    }
                }
                override fun onReceivedError(view: WebView,request: WebResourceRequest,error: WebResourceError) {
                    if(request.isForMainFrame) showStatus(ui(R.string.ui_the_online_gallery_could_not_be_loaded_check))
                }
            }
            setOnLongClickListener {
                val hit=hitTestResult
                if(hit.type in listOf(WebView.HitTestResult.IMAGE_TYPE,WebView.HitTestResult.SRC_IMAGE_ANCHOR_TYPE)) {
                    hit.extra?.let {insert(Uri.parse(it))};true
                } else false
            }
        }
        root.addView(web,LinearLayout.LayoutParams(-1,0,1f));setContentView(root);LocaleTypography.install(root)
        if(state==null) web.loadUrl(provider.home,mapOf("Accept-Language" to AppLanguage.locale(this).toLanguageTag())) else web.restoreState(state)
        val editorSource=state?.getString("image_credit_editor_source")
        val editorText=state?.getString("image_credit_editor_draft")
        val restoredDraft=if(sessionToken!=null) creditSession.draft
            else if(editorSource!=null && editorText!=null) GalleryCredits.EditorDraft(editorSource,editorText) else creditSession.draft
        restoredDraft?.let {showCreditEditor(it)}
    }
    public override fun onActivityResult(requestCode: Int,resultCode: Int,data: Intent?) {
        super.onActivityResult(requestCode,resultCode,data)
        if(requestCode!=LEGACY_CREDITS || resultCode!=RESULT_OK || !::creditSession.isInitialized)return
        val token=data?.getStringExtra(LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN)
        if(token==null || !token.matches(Regex("[0-9a-f]{64}")))return
        // Return only the selected archive identifier. The editor owns atomic validation
        // against its current complete draft and must not overwrite a modern source.
        sessionHandedBack=true
        setResult(RESULT_OK,creditSession.result()
            .putExtra(LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN,token))
        finish()
    }

    private fun showCreditEditor(draft: GalleryCredits.EditorDraft?=null) {
        if(creditEditor?.dialog?.isShowing==true)return
        creditEditor=GalleryCredits.showEditor(this,documentCredits,draft,onEdit={source,text ->
            creditSession.edit(source,text) {ImageCreditArchive.retainAccepted(this,it)}
            documentCredits=creditSession.credits
            creditsEdited=true;returnEditedCredits()
        },onDismiss={
            try {creditSession.saveDraft(null)} catch(_: Exception) {
                LocaleTypography.showMessage(this,ui(R.string.gallery_credit_could_not_save),Toast.LENGTH_LONG)
            }
        })
    }
    private fun returnEditedCredits() {
        setResult(RESULT_OK,creditSession.result())
    }
    private fun commonsCredit(uri: Uri,page: String,checkActive: ()->Unit): CommonsAttribution.Record {
        val record=CommonsAttribution.fetch(this,uri.toString(),page,openConnection,checkActive) {activeConnection=it}
        checkActive()
        CommonsAttribution.cache(this,record)
        return record
    }

    /** Copying source credit fetches metadata only, not image bytes, and does not register an insertion. */
    private fun copyCommonsCredit(uri: Uri,page: String) {
        if(downloading || isFinishing || isDestroyed) return
        downloading=true;showStatus(ui(R.string.ui_image_credits)+"…")
        worker.execute {
            try {
                val record=commonsCredit(uri,page) {
                    if(isFinishing || isDestroyed || Thread.currentThread().isInterrupted) throw InterruptedIOException()
                }
                runOnUiThread {
                    if(!isFinishing && !isDestroyed) {GalleryCredits.copy(this,record.text(imported=false));hideStatus()}
                }
            } catch(error: Exception) {
                runOnUiThread {if(!isFinishing && !isDestroyed) showStatus(ui(R.string.ui_could_not_load_gallery_image,error.message))}
            } catch(_: OutOfMemoryError) {
                runOnUiThread {if(!isFinishing && !isDestroyed) showStatus(ui(R.string.ui_not_enough_memory_to_inspect_the_gallery_image))}
            } catch(_: LinkageError) {
                runOnUiThread {if(!isFinishing && !isDestroyed) showStatus(ui(R.string.colour_converter_unavailable))}
            } finally {activeConnection?.disconnect();activeConnection=null;downloading=false}
        }
    }

    private fun showStatus(message: String) {
        status.text=message;status.visibility=View.VISIBLE;statusHost.visibility=View.VISIBLE
        (statusHost as? ColumnScrollView)?.resetToReadingStart()
        controlsScroll.revealStart(statusHost)
    }
    private fun hideStatus() {status.visibility=View.GONE;statusHost.visibility=View.GONE}
    private fun openExternal(uri: Uri) {
        try {startActivity(Intent(Intent.ACTION_VIEW,uri))} catch(_: android.content.ActivityNotFoundException) {showStatus(ui(R.string.ui_the_online_gallery_could_not_be_loaded_check))}
    }
    private fun insert(uri: Uri,page: String=web.url.orEmpty(),title: String=web.title.orEmpty(),author: String="",licence: String="",authorUrl: String="") {
        if(downloading || isFinishing || isDestroyed)return
        if(!provider.allowsImage(uri)) {showStatus(ui(R.string.ui_gallery_unsupported34));return}
        if(provider!=IllustrationSource.CATROBAT && !provider.isArtworkPage(Uri.parse(page))) {showStatus(ui(R.string.ui_open_artwork34));return}
        download(uri,page.take(4096),title.take(512),author,licence,authorUrl)
    }
    private fun download(uri: Uri,page: String,title: String,author: String,licence: String,authorUrl: String) {
        if(downloading || isFinishing || isDestroyed)return
        downloading=true;showStatus(ui(R.string.ui_downloading_image))
        worker.execute {
            var temporary: File?=null
            var rendered: File?=null
            fun checkActive() {
                if(isFinishing || isDestroyed || Thread.currentThread().isInterrupted) throw InterruptedIOException()
            }
            fun failure(message: String) = runOnUiThread {
                if(!isFinishing && !isDestroyed) showStatus(message)
            }
            try {
                var url=URL(uri.toString());var connection: HttpURLConnection?=null
                for(i in 0..5) {
                    checkActive()
                    require(provider.allowsDownload(Uri.parse(url.toString()))) {ui(R.string.ui_the_gallery_redirected_outside_its_supported_hosts)}
                    val current=openConnection(url);activeConnection=current
                    current.setRequestProperty("Referer",page.takeIf {provider.allowsPage(Uri.parse(it))} ?: provider.home)
                    if(provider==IllustrationSource.COMMONS) current.setRequestProperty("User-Agent","AN-Paint/0.0.38 (https://github.com/c933103/AN-Paint) Android")
                    current.connectTimeout=15000;current.readTimeout=30000;current.instanceFollowRedirects=false
                    if(current.responseCode in 300..399) {
                        val redirect=current.getHeaderField("Location");current.disconnect();activeConnection=null
                        require(redirect!=null);url=URL(url,redirect)
                    } else {connection=current;break}
                }
                val source=connection ?: error(ui(R.string.ui_too_many_gallery_redirects))
                check(source.responseCode in 200..299) {ui(R.string.ui_the_image_could_not_be_downloaded)}
                if(provider==IllustrationSource.COMMONS) require(CommonsAttribution.sameOriginal(uri.toString(),url.toString())) {
                    "The Commons download redirected to a different original file."
                }
                val file=File.createTempFile("gallery-",".image",cacheDir);temporary=file
                source.inputStream.use {input -> file.outputStream().use {out ->
                    val buffer=ByteArray(65536);var total=0L
                    while(true) {
                        checkActive()
                        val n=input.read(buffer);if(n<0)break;total+=n
                        check(total<=128L*1024*1024) {ui(R.string.ui_the_gallery_download_is_too_large)}
                        out.write(buffer,0,n)
                    }
                }}
                source.disconnect();activeConnection=null
                checkActive()
                val resultFile: File
                if(provider==IllustrationSource.COMMONS && uri.path.orEmpty().endsWith(".svg",true)) {
                    check(file.length()<=32L*1024*1024) {ui(R.string.commons_svg_too_large)}
                    val destination=File.createTempFile("gallery-",".png",cacheDir);rendered=destination
                    // The SVG declares its own original size. No size dialog, canvas-width default or clamp.
                    BlankMapSvg.renderOriginal(file,destination,ImageMemoryPolicy.forDevice(this),
                        intent.getLongExtra("gallery_resident_pixels",0L))
                    resultFile=destination
                } else {
                    ImportedImage(file,uri.lastPathSegment ?: ui(R.string.ui_gallery_image)) // Validate before returning.
                    resultFile=file
                }
                checkActive()
                // Retain metadata without changing the document ledger. The editor associates
                // this snapshot with the image only after insertion succeeds.
                if(provider==IllustrationSource.COMMONS) commonsCredit(uri,page,::checkActive)
                checkActive()
                runOnUiThread {returnDownloaded(resultFile,uri,page,title,author,licence,authorUrl)}
                // The callback owns only the returned file. Always remove a downloaded SVG after rendering.
                if(resultFile===file) temporary=null else rendered=null
            } catch(error: Exception) {
                val reason=if(error is SvgOriginalSize.SizeException) ui(when(error.reason) {
                    SvgOriginalSize.Reason.UNUSABLE_ORIGINAL_SIZE -> R.string.commons_svg_original_size_unavailable
                    SvgOriginalSize.Reason.EXCEEDS_BITMAP_DIMENSIONS -> R.string.commons_svg_original_size_too_large
                }) else error.message
                failure(ui(R.string.ui_could_not_load_gallery_image,reason))
            }
              catch(error: OutOfMemoryError) {failure(ui(R.string.ui_not_enough_memory_to_inspect_the_gallery_image))}
              catch(error: LinkageError) {failure(ui(R.string.ui_could_not_load_gallery_image,ui(R.string.colour_converter_unavailable)))}
            finally {activeConnection?.disconnect();activeConnection=null;temporary?.delete();rendered?.delete();downloading=false}
        }
    }
    private fun returnDownloaded(file: File,uri: Uri,page: String,title: String,author: String,licence: String,authorUrl: String) {
        // Closing the gallery cancels insertion even after the worker has posted its result.
        if(isFinishing || isDestroyed) {file.delete();return}
        sessionHandedBack=true
        setResult(RESULT_OK,creditSession.result().putExtra("gallery_file",file.name)
            .putExtra("gallery_source",uri.toString()).putExtra("gallery_provider",provider.name)
            .putExtra("gallery_page",page).putExtra("gallery_title",title)
            .putExtra("gallery_author",author).putExtra("gallery_licence",licence).putExtra("gallery_author_url",authorUrl))
        finish()
    }

    @Deprecated("Android legacy activity back callback")
    override fun onBackPressed() {if(::web.isInitialized && web.canGoBack()) web.goBack() else super.onBackPressed()}
    private fun preserveCreditDraft() {
        if(!::creditSession.isInitialized)return
        try {
            val draft=creditEditor?.takeIf {it.dialog.isShowing}?.snapshot?.invoke() ?: return
            creditSession.saveDraft(draft)
        } catch(_: Exception) {
            LocaleTypography.showMessage(this,ui(R.string.gallery_credit_could_not_save),Toast.LENGTH_LONG,
                creditEditor?.dialog?.window?.decorView)
        }
    }
    override fun onSaveInstanceState(outState: Bundle) {
        preserveCreditDraft()
        if(::creditSession.isInitialized) creditSession.saveState(outState)
        else unrestoredSessionToken?.let {outState.putString(CreditEditSession.EXTRA_SESSION,it)}
        if(::web.isInitialized) web.saveState(outState)
        super.onSaveInstanceState(outState)
    }
    override fun onStop() {preserveCreditDraft();super.onStop()}
    override fun onConfigurationChanged(newConfig: Configuration) {
        super.onConfigurationChanged(newConfig)
        // Retain the active download/render, WebView and open credit field across rotation.
        // The editor remains a draft; only its explicit Save/Copy/Done actions accept edits.
        // The controls use the live window bounds; no orientation-specific
        // fixed rectangle remains. Keep the existing native search/editor views.
        if(::controlsScroll.isInitialized) controlsScroll.requestLayout()
    }
    override fun onDestroy() {
        // Dismiss the old window without invoking a save action. A saved draft is restored separately.
        creditEditor?.dismissForRecreation();creditEditor=null
        creditSessionError?.dismiss();creditSessionError=null
        if(::web.isInitialized) web.destroy()
        if(isFinishing && !sessionHandedBack && ::creditSession.isInitialized && !creditSession.accepted && creditSession.draft==null) creditSession.discard()
        worker.shutdownNow();activeConnection?.disconnect();super.onDestroy()
    }
}
