/* AN Paint, 2026-09-10. AGPL-3.0-or-later.
 * Online illustrations retain their publisher's individual credits and terms.
 * Catrobat, Irasutoya and Openclipart media are not bundled in the application.
 */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.app.Activity
import android.app.AlertDialog
import android.graphics.Bitmap
import android.text.InputType
import kotlin.math.roundToInt
import android.content.Intent
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
        const val GALLERY="https://catrobat.org/figures-download/"
        const val LICENCE="https://developer.catrobat.org/pages/legal/licenses/catrobat/"
        fun allowed(uri: Uri)=IllustrationSource.CATROBAT.allowsPage(uri)
    }
    private val provider by lazy {IllustrationSource.fromId(intent.getStringExtra("gallery_provider"))}
    private var pendingSearch: String?=null
    private var pendingVector: File?=null
    private var vectorDialog: AlertDialog?=null
    private lateinit var web: WebView
    private lateinit var status: TextView
    private val worker=Executors.newSingleThreadExecutor()
    internal var openConnection: (URL)->HttpURLConnection = { it.openConnection() as HttpURLConnection }
    @Volatile private var activeConnection: HttpURLConnection?=null
    @Volatile internal var downloading=false; private set
    override fun onCreate(state: Bundle?) {
        super.onCreate(state)
        fun dp(n: Int)=(n*resources.displayMetrics.density+.5f).toInt()
        val root=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL;fitsSystemWindows=true;setBackgroundColor(EditorColours.surface)}
        val description=TextView(this).apply {
            tag="gallery_description";text=provider.label+"\n"+ui(provider.descriptionId);textSize=13f
            setTextColor(EditorColours.onSurface);setPadding(dp(12),dp(8),dp(12),dp(8))
        }
        root.addView(ScrollView(this).apply {addView(description)},LinearLayout.LayoutParams(-1,dp(if(resources.configuration.orientation==android.content.res.Configuration.ORIENTATION_LANDSCAPE) 56 else 88)))
        status=TextView(this).apply {tag="gallery_status";visibility=View.GONE;setTextColor(EditorColours.onSurface);setPadding(dp(12),0,dp(12),dp(4))}
        root.addView(status)
        val row=LinearLayout(this)
        fun action(label: String,tagName: String,run: ()->Unit) {row.addView(Button(this).apply {text=label;tag=tagName;isAllCaps=false;minWidth=0;minimumWidth=0;textSize=12f;setOnClickListener {run()}},LinearLayout.LayoutParams(0,dp(48),1f))}
        action(ui(R.string.ui_copy_all),"gallery_copy_credits") {
            val credits=GalleryCredits.text(this)
            if(credits.isBlank()) Toast.makeText(this,ui(R.string.ui_no_gallery_images_have_been_inserted),Toast.LENGTH_SHORT).show()
            else GalleryCredits.copy(this,credits)
        }
        action(ui(R.string.gallery_edit_credits),"gallery_edit_credits") {GalleryCredits.showEditor(this)}
        action(ui(R.string.ui_credits_terms),"gallery_terms") {openExternal(Uri.parse(provider.terms))}
        action(ui(R.string.ui_done),"gallery_done") {finish()};root.addView(row)
        val navigation=LinearLayout(this)
        navigation.addView(Button(this).apply {text="←";contentDescription=ui(R.string.ui_gallery_back34);tag="gallery_back";setOnClickListener {if(web.canGoBack()) web.goBack() else web.loadUrl(provider.home)}},LinearLayout.LayoutParams(dp(52),dp(48)))
        val search=EditText(this).apply {tag="gallery_search";setSingleLine(true);hint=ui(if(provider==IllustrationSource.IRASUTOYA) R.string.ui_search_english34 else R.string.ui_search34);textSize=14f}
        navigation.addView(search,LinearLayout.LayoutParams(0,dp(48),1f))
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
        navigation.addView(Button(this).apply {text=ui(R.string.ui_search34);isAllCaps=false;tag="gallery_search_go";setOnClickListener {searchNow()}},LinearLayout.LayoutParams(-2,dp(48)))
        search.setOnEditorActionListener {_,_,_->searchNow();true}
        root.addView(navigation)
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
                            if(uri.scheme==GalleryPage.CREDIT_SCHEME) GalleryCredits.copy(this@MediaGalleryActivity,GalleryCredits.credit(source.toString(),title,provider,page))
                            else insert(source,page,title)
                        }
                        return true
                    }
                    if(provider.allowsImage(uri)) {insert(uri);return true}
                    if(!provider.allowsPage(uri)) {if(uri.scheme=="https") openExternal(uri);return true}
                    return false
                }
                override fun onPageFinished(view: WebView,url: String) {
                    if(provider.allowsPage(Uri.parse(url))) {
                        view.evaluateJavascript(IllustrationPage.script(provider,ui(R.string.gallery_use_image),ui(R.string.gallery_copy_credit)),null)
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
        root.addView(web,LinearLayout.LayoutParams(-1,0,1f));setContentView(root)
        if(state==null) web.loadUrl(provider.home,mapOf("Accept-Language" to AppLanguage.locale(this).toLanguageTag())) else web.restoreState(state)
    }
    private fun showStatus(message: String) {status.text=message;status.visibility=View.VISIBLE}
    private fun openExternal(uri: Uri) {
        try {startActivity(Intent(Intent.ACTION_VIEW,uri))} catch(_: android.content.ActivityNotFoundException) {showStatus(ui(R.string.ui_the_online_gallery_could_not_be_loaded_check))}
    }
    private fun insert(uri: Uri,page: String=web.url.orEmpty(),title: String=web.title.orEmpty()) {
        if(downloading || pendingVector!=null || isFinishing || isDestroyed)return
        if(!provider.allowsImage(uri)) {showStatus(ui(R.string.ui_gallery_unsupported34));return}
        if(provider!=IllustrationSource.CATROBAT && !provider.isArtworkPage(Uri.parse(page))) {showStatus(ui(R.string.ui_open_artwork34));return}
        download(uri,page.take(4096),title.take(512))
    }
    private fun download(uri: Uri,page: String,title: String) {
        if(downloading || isFinishing || isDestroyed)return
        downloading=true;showStatus(ui(R.string.ui_downloading_image))
        worker.execute {
            var temporary: File?=null
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
                checkActive()
                if(provider==IllustrationSource.COMMONS && uri.path.orEmpty().endsWith(".svg",true)) {
                    check(file.length()<=32L*1024*1024) {ui(R.string.commons_svg_too_large)}
                    val ratio=BlankMapSvg.aspectRatio(file)
                    temporary=null
                    runOnUiThread {if(isFinishing || isDestroyed) file.delete() else askVectorSize(file,uri,page,title,ratio)}
                } else {
                    ImportedImage(file,uri.lastPathSegment ?: ui(R.string.ui_gallery_image)) // Validate before returning.
                    temporary=null
                    runOnUiThread {returnDownloaded(file,uri,page,title)}
                }
            } catch(error: Exception) {failure(ui(R.string.ui_could_not_load_gallery_image, error.message))}
              catch(error: OutOfMemoryError) {failure(ui(R.string.ui_not_enough_memory_to_inspect_the_gallery_image))}
              catch(error: LinkageError) {failure(ui(R.string.ui_could_not_load_gallery_image,ui(R.string.colour_converter_unavailable)))}
            finally {activeConnection?.disconnect();activeConnection=null;temporary?.delete();downloading=false}
        }
    }
    private fun returnDownloaded(file: File, uri: Uri, page: String, title: String) {
        if(isFinishing || isDestroyed) {file.delete();return}
        setResult(RESULT_OK,Intent().putExtra("gallery_file",file.name)
            .putExtra("gallery_source",uri.toString()).putExtra("gallery_provider",provider.name)
            .putExtra("gallery_page",page).putExtra("gallery_title",title))
        finish()
    }

    /** SVG resolution is chosen before rendering. Non-SVG downloads use existing full-resolution import. */
    private fun askVectorSize(file: File,uri: Uri,page: String,title: String,ratio: Double) {
        pendingVector=file
        val initialWidth=intent.getIntExtra("gallery_canvas_width",2000).coerceIn(1,10000)
        val initialHeight=(initialWidth/ratio).roundToInt().coerceIn(1,10000)
        val padding=(16*resources.displayMetrics.density).toInt()
        val body=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL;setPadding(padding,padding,padding,padding)}
        body.addView(TextView(this).apply {text=ui(R.string.commons_svg_render_help)})
        fun dimension(label: String,value: Int,tagName: String): EditText {
            body.addView(TextView(this).apply {text=label})
            return EditText(this).apply {
                tag=tagName;inputType=InputType.TYPE_CLASS_NUMBER;setSingleLine(true);setText(value.toString())
                body.addView(this)
            }
        }
        val width=dimension(ui(R.string.commons_width_px),initialWidth,"commons_svg_width")
        val height=dimension(ui(R.string.commons_height_px),initialHeight,"commons_svg_height")
        val chooser=AlertDialog.Builder(this).setTitle(ui(R.string.commons_svg_resolution)).setView(body)
            .setPositiveButton(ui(R.string.gallery_use_image),null)
            .setNegativeButton(ui(R.string.ui_cancel)) {_,_->file.delete();pendingVector=null}
            .setOnCancelListener {file.delete();pendingVector=null}.create()
        vectorDialog=chooser
        chooser.setOnShowListener {
            chooser.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
                val w=width.text.toString().toIntOrNull();val h=height.text.toString().toIntOrNull()
                if(w==null || w<=0) {width.error=ui(R.string.ui_enter_positive_dimensions);return@setOnClickListener}
                if(h==null || h<=0) {height.error=ui(R.string.ui_enter_positive_dimensions);return@setOnClickListener}
                try {
                    ImageMemoryPolicy.forDevice(this).check(w,h,intent.getLongExtra("gallery_resident_pixels",0L))
                } catch(error: Exception) {height.error=error.message;showStatus(error.message.orEmpty());return@setOnClickListener}
                pendingVector=null;vectorDialog=null;chooser.dismiss()
                renderVector(file,uri,page,title,w,h)
            }
        }
        chooser.show()
    }

    private fun renderVector(file: File,uri: Uri,page: String,title: String,width: Int,height: Int) {
        if(downloading || isFinishing || isDestroyed) {file.delete();return}
        downloading=true;showStatus(ui(R.string.commons_svg_rendering))
        worker.execute {
            var output: File?=null
            try {
                val destination=File.createTempFile("gallery-", ".png",cacheDir);output=destination
                BlankMapSvg.render(file,destination,width,height)
                if(Thread.currentThread().isInterrupted) throw InterruptedIOException()
                output=null
                runOnUiThread {returnDownloaded(destination,uri,page,title)}
            } catch(error: Exception) {
                runOnUiThread {if(!isFinishing && !isDestroyed)showStatus(ui(R.string.ui_could_not_load_gallery_image,error.message))}
            } catch(error: OutOfMemoryError) {
                runOnUiThread {if(!isFinishing && !isDestroyed)showStatus(ui(R.string.ui_not_enough_memory_to_inspect_the_gallery_image))}
            } finally {file.delete();output?.delete();downloading=false}
        }
    }

    @Deprecated("Android legacy activity back callback")
    override fun onBackPressed() {if(web.canGoBack()) web.goBack() else super.onBackPressed()}
    override fun onSaveInstanceState(outState: Bundle) {web.saveState(outState);super.onSaveInstanceState(outState)}
    override fun onDestroy() {vectorDialog?.dismiss();pendingVector?.delete();pendingVector=null;web.destroy();worker.shutdownNow();activeConnection?.disconnect();super.onDestroy()}
}
