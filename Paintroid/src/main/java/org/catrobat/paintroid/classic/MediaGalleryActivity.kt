/* AN Paint, 2026-09-10. AGPL-3.0-or-later.
 * Online gallery: Catrobat. Media retain the publisher's individual credits;
 * Catrobat's own non-software works are CC BY-SA 4.0, except its names/logos.
 */
package org.catrobat.paintroid.classic

import android.app.Activity
import android.app.AlertDialog
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.View
import android.webkit.*
import android.widget.*
import java.io.File
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.Executors

class MediaGalleryActivity : Activity() {
    companion object {
        const val GALLERY="https://catrobat.org/figures-download/"
        const val LICENCE="https://developer.catrobat.org/pages/legal/licenses/catrobat/"
        fun allowed(uri: Uri)=uri.scheme=="https" && uri.host in setOf("catrobat.org","www.catrobat.org","catrobatblog.files.wordpress.com","catrobatblog.wpcomstaging.com")
    }
    private lateinit var web: WebView
    private lateinit var status: TextView
    private val worker=Executors.newSingleThreadExecutor()
    private var downloading=false
    override fun onCreate(state: Bundle?) {
        super.onCreate(state)
        val root=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL;fitsSystemWindows=true}
        status=TextView(this).apply {text="Catrobat online gallery · artwork by its credited creators";setPadding(16,12,16,12)}
        root.addView(status)
        val row=LinearLayout(this)
        fun action(label: String,run: ()->Unit) {row.addView(Button(this).apply {text=label;isAllCaps=false;setOnClickListener {run()}},LinearLayout.LayoutParams(0,-2,1f))}
        action("Credits & terms") {startActivity(Intent(Intent.ACTION_VIEW,Uri.parse(LICENCE)))}
        action("Done") {finish()};root.addView(row)
        web=WebView(this).apply {
            settings.javaScriptEnabled=true;settings.allowFileAccess=false;settings.allowContentAccess=false
            settings.domStorageEnabled=true;settings.mixedContentMode=WebSettings.MIXED_CONTENT_NEVER_ALLOW
            setDownloadListener {url,_,_,_,_ -> insert(Uri.parse(url))}
            webViewClient=object: WebViewClient() {
                override fun shouldOverrideUrlLoading(view: WebView,url: String): Boolean {
                    val uri=Uri.parse(url)
                    if(!allowed(uri)) {if(uri.scheme=="https") startActivity(Intent(Intent.ACTION_VIEW,uri));return true}
                    if(uri.path.orEmpty().lowercase().matches(Regex(".*\\.(png|jpe?g|webp|gif|jxl)$"))) {insert(uri);return true}
                    return false
                }
                override fun onReceivedError(view: WebView,request: WebResourceRequest,error: WebResourceError) {
                    if(request.isForMainFrame) status.text="The online gallery could not be loaded. Check your connection and try again."
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
        if(state==null) web.loadUrl(GALLERY) else web.restoreState(state)
    }
    private fun insert(uri: Uri) {
        if(downloading)return
        if(!allowed(uri)) {status.text="This image is outside the supported Catrobat gallery.";return}
        AlertDialog.Builder(this).setTitle("Insert gallery image?")
            .setMessage("Catrobat's own artwork uses CC BY-SA 4.0. Keep the creator credit and share adaptations under that licence. Check the source page for any separate attribution. The source URL will be kept under Help > Image credits.")
            .setNegativeButton("Cancel",null).setPositiveButton("Insert") {_,_ -> download(uri)}.show()
    }
    private fun download(uri: Uri) {
        downloading=true;status.text="Downloading image…"
        worker.execute {
            var temporary: File?=null
            try {
                var url=URL(uri.toString());var connection: HttpURLConnection?=null
                for(i in 0..5) {
                    require(allowed(Uri.parse(url.toString()))) {"The gallery redirected outside its supported hosts."}
                    val current=url.openConnection() as HttpURLConnection
                    current.connectTimeout=15000;current.readTimeout=30000;current.instanceFollowRedirects=false
                    if(current.responseCode in 300..399) {val redirect=current.getHeaderField("Location");current.disconnect();require(redirect!=null);url=URL(url,redirect)}
                    else {connection=current;break}
                }
                val source=connection ?: error("Too many gallery redirects.")
                val file=File.createTempFile("gallery-",".image",cacheDir);temporary=file
                try {
                    check(source.responseCode in 200..299) {"The image could not be downloaded."}
                    source.inputStream.use {input -> file.outputStream().use {out ->
                        val buffer=ByteArray(65536);var total=0L
                        while(true) {val n=input.read(buffer);if(n<0)break;total+=n;check(total<=128L*1024*1024) {"The gallery download is too large."};out.write(buffer,0,n)}
                    }}
                } finally {source.disconnect()}
                ImportedImage(file,uri.lastPathSegment ?: "Gallery image") // Validate before returning.
                if(isDestroyed) file.delete() else {
                    temporary=null
                    runOnUiThread {setResult(RESULT_OK,Intent().putExtra("gallery_file",file.name).putExtra("gallery_source",uri.toString()));finish()}
                }
            } catch(error: Exception) {runOnUiThread {downloading=false;status.text="Could not load gallery image: ${error.message}"}}
              catch(error: OutOfMemoryError) {runOnUiThread {downloading=false;status.text="Not enough memory to inspect the gallery image."}}
            finally {temporary?.delete()}
        }
    }
    override fun onSaveInstanceState(outState: Bundle) {web.saveState(outState);super.onSaveInstanceState(outState)}
    override fun onDestroy() {web.destroy();worker.shutdown();super.onDestroy()}
}
