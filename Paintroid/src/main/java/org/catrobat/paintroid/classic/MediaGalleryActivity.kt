/* AN Paint, 2026-09-10. AGPL-3.0-or-later.
 * Online gallery: Catrobat. Media retain the publisher's individual credits;
 * Catrobat's own non-software works are CC BY-SA 4.0, except its names/logos.
 */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.app.Activity
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
        fun allowed(uri: Uri)=uri.scheme=="https" && uri.host in setOf("catrobat.org","www.catrobat.org","catrobatblog.files.wordpress.com","catrobatblog.wpcomstaging.com")
    }
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
            tag="gallery_description";text=ui(R.string.gallery_description);textSize=13f
            setTextColor(EditorColours.onSurface);setPadding(dp(12),dp(8),dp(12),dp(8))
        }
        root.addView(ScrollView(this).apply {addView(description)},LinearLayout.LayoutParams(-1,dp(104)))
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
        action(ui(R.string.ui_credits_terms),"gallery_terms") {startActivity(Intent(Intent.ACTION_VIEW,Uri.parse(LICENCE)))}
        action(ui(R.string.ui_done),"gallery_done") {finish()};root.addView(row)
        web=WebView(this).apply {
            settings.javaScriptEnabled=true;settings.allowFileAccess=false;settings.allowContentAccess=false
            settings.domStorageEnabled=true;settings.mixedContentMode=WebSettings.MIXED_CONTENT_NEVER_ALLOW
            setDownloadListener {url,_,_,_,_ -> insert(Uri.parse(url))}
            webViewClient=object: WebViewClient() {
                override fun shouldOverrideUrlLoading(view: WebView,url: String): Boolean {
                    val uri=Uri.parse(url)
                    if(uri.scheme==GalleryPage.CREDIT_SCHEME) {
                        if(!uri.isHierarchical || uri.host!="copy")return true
                        val source=uri.getQueryParameter("source")?.let {Uri.parse(it)}
                        if(source!=null && allowed(source)) GalleryCredits.copy(this@MediaGalleryActivity,
                            GalleryCredits.credit(source.toString(),uri.getQueryParameter("title").orEmpty().take(512)))
                        return true
                    }
                    if(!allowed(uri)) {if(uri.scheme=="https") startActivity(Intent(Intent.ACTION_VIEW,uri));return true}
                    if(uri.path.orEmpty().lowercase().matches(Regex(".*\\.(png|jpe?g|webp|gif|jxl|bmp|dib|ico|tiff?|heic|avif)$"))) {insert(uri);return true}
                    return false
                }
                override fun onPageFinished(view: WebView,url: String) {
                    if(allowed(Uri.parse(url))) view.evaluateJavascript(GalleryPage.script(ui(R.string.gallery_use_image),ui(R.string.gallery_copy_credit)),null)
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
        if(state==null) web.loadUrl(GALLERY,mapOf("Accept-Language" to AppLanguage.locale(this).toLanguageTag())) else web.restoreState(state)
    }
    private fun showStatus(message: String) {status.text=message;status.visibility=View.VISIBLE}
    private fun insert(uri: Uri) {
        if(downloading || isFinishing || isDestroyed)return
        if(!allowed(uri)) {showStatus(ui(R.string.ui_this_image_is_outside_the_supported_catrobat_gallery));return}
        download(uri)
    }
    private fun download(uri: Uri) {
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
                    require(allowed(Uri.parse(url.toString()))) {ui(R.string.ui_the_gallery_redirected_outside_its_supported_hosts)}
                    val current=openConnection(url);activeConnection=current
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
                ImportedImage(file,uri.lastPathSegment ?: ui(R.string.ui_gallery_image)) // Validate before returning.
                runOnUiThread {
                    // Closing the gallery cancels insertion even if it happens after
                    // the worker posts this result but before Android delivers it.
                    if(isFinishing || isDestroyed) file.delete() else {
                        setResult(RESULT_OK,Intent().putExtra("gallery_file",file.name).putExtra("gallery_source",uri.toString()))
                        finish()
                    }
                }
                temporary=null // UI callback owns the validated file from here.
            } catch(error: Exception) {failure(ui(R.string.ui_could_not_load_gallery_image, error.message))}
              catch(error: OutOfMemoryError) {failure(ui(R.string.ui_not_enough_memory_to_inspect_the_gallery_image))}
              catch(error: LinkageError) {failure(ui(R.string.ui_could_not_load_gallery_image,ui(R.string.colour_converter_unavailable)))}
            finally {activeConnection?.disconnect();activeConnection=null;temporary?.delete();downloading=false}
        }
    }
    override fun onSaveInstanceState(outState: Bundle) {web.saveState(outState);super.onSaveInstanceState(outState)}
    override fun onDestroy() {web.destroy();worker.shutdownNow();activeConnection?.disconnect();super.onDestroy()}
}
