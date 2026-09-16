/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.json.JSONArray
import org.json.JSONTokener
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicReference

/** Real WebView DOM, using the verified WordPress markup without a live network dependency. */
@RunWith(AndroidJUnit4::class)
class GalleryPageDeviceTest {
    @Test fun galleryDownloadButtonsUseAppLabelsAndPreserveArtworkTitlesAndUnrelatedLinks() {
        val instrumentation=InstrumentationRegistry.getInstrumentation()
        val completed=CountDownLatch(1)
        val result=AtomicReference<String>()
        var web: WebView?=null
        instrumentation.runOnMainSync {
            web=WebView(instrumentation.targetContext).apply {
                settings.javaScriptEnabled=true
                webViewClient=object: WebViewClient() {
                    override fun onPageFinished(view: WebView,url: String) {
                        view.evaluateJavascript(GalleryPage.script("Use image","Copy credit")) {
                            // Reapplying after a language change must update, not duplicate, controls.
                            view.evaluateJavascript(GalleryPage.script("画像を使う","クレジットをコピー")) {
                                view.evaluateJavascript("JSON.stringify([document.getElementById('use').textContent,document.getElementById('title').textContent,document.querySelector('[data-anpaint-credit]').textContent,document.querySelector('[data-anpaint-credit]').getAttribute('href'),document.querySelectorAll('[data-anpaint-credit]').length,document.getElementById('other').textContent])") {
                                    result.set(it);completed.countDown()
                                }
                            }
                        }
                    }
                }
                loadDataWithBaseURL(MediaGalleryActivity.GALLERY,"""
                    <html><body><div class="wp-block-file">
                    <a id="title" href="https://catrobat.org/wp-content/uploads/2025/01/Needle_Yellow.png">Needle_Yellow</a>
                    <a id="use" href="https://catrobat.org/wp-content/uploads/2025/01/Needle_Yellow.png" class="wp-block-file__button wp-element-button" download aria-describedby="title">Herunterladen</a>
                    </div><div class="wp-block-file"><a id="other" class="wp-block-file__button" download href="https://example.org/private.png">Herunterladen</a></div></body></html>
                """.trimIndent(),"text/html","UTF-8",null)
            }
        }
        try {
            assertTrue("WebView did not finish the gallery fixture",completed.await(15,TimeUnit.SECONDS))
            val values=JSONArray(JSONTokener(result.get()).nextValue() as String)
            assertEquals("画像を使う",values.getString(0));assertEquals("Needle_Yellow",values.getString(1))
            assertEquals("クレジットをコピー",values.getString(2));assertEquals(1,values.getInt(4))
            val credit=android.net.Uri.parse(values.getString(3))
            assertEquals(GalleryPage.CREDIT_SCHEME,credit.scheme)
            assertEquals("Needle_Yellow",credit.getQueryParameter("title"))
            assertEquals("https://catrobat.org/wp-content/uploads/2025/01/Needle_Yellow.png",credit.getQueryParameter("source"))
            assertEquals("Herunterladen",values.getString(5))
        } finally {instrumentation.runOnMainSync {web?.destroy()}}
    }
    @Test fun irasutoyaAddsLocalizedUseButtonsToFullArtworkWithoutTouchingThumbnailsOrAds() {
        val result=adaptIllustration(IllustrationSource.IRASUTOYA,"https://www.irasutoya.com/2026/06/typhoon.html","""
            <html><body><div class="entry"><div class="separator">
            <a id="art" href="https://blogger.googleusercontent.com/img/b/art/s740/character_typhoon.png"><img alt="Original artwork title" src="https://blogger.googleusercontent.com/img/b/art/s400/character_typhoon.png"></a>
            </div><a href="https://example.org/ad.png"><img src="https://example.org/ad.png"></a></div>
            <a href="https://blogger.googleusercontent.com/img/b/art/s72/thumbnail.png"><img src="https://blogger.googleusercontent.com/img/b/art/s72/thumbnail.png"></a></body></html>
        """.trimIndent())
        assertEquals(1,result.getInt(0));assertEquals("Use image",result.getString(1));assertEquals("Copy credit",result.getString(2))
        val link=android.net.Uri.parse(result.getString(3))
        assertEquals("https://blogger.googleusercontent.com/img/b/art/s740/character_typhoon.png",link.getQueryParameter("source"))
        assertEquals("Original artwork title",link.getQueryParameter("title"))
        assertEquals("https://www.irasutoya.com/2026/06/typhoon.html",link.getQueryParameter("page"))
    }
    @Test fun openclipartUsesItsLargePngAndDoesNotTreatTheVectorLinkAsABitmap() {
        val result=adaptIllustration(IllustrationSource.OPENCLIPART,"https://openclipart.org/detail/250963/public-domain","""
            <html><body><h2>Public Domain</h2><div class="btn-group">
            <a href="/download/250963/public-domain.svg">Download SVG</a>
            <a href="/image/400px/250963">Small</a><a href="/image/800px/250963">Medium</a>
            <a href="/image/2000px/250963">Large</a></div></body></html>
        """.trimIndent())
        assertEquals(1,result.getInt(0))
        assertEquals("https://openclipart.org/image/2000px/250963",android.net.Uri.parse(result.getString(3)).getQueryParameter("source"))
    }
    private fun adaptIllustration(provider: IllustrationSource,url: String,html: String): JSONArray {
        val instrumentation=InstrumentationRegistry.getInstrumentation();val done=CountDownLatch(1)
        val result=AtomicReference<String>();var web: WebView?=null
        instrumentation.runOnMainSync {
            web=WebView(instrumentation.targetContext).apply {
                settings.javaScriptEnabled=true
                webViewClient=object: WebViewClient() {
                    override fun onPageFinished(view: WebView,loaded: String) {
                        val script=IllustrationPage.script(provider,"Use image","Copy credit")
                        view.evaluateJavascript(script) {view.evaluateJavascript(script) {
                            view.evaluateJavascript("JSON.stringify([document.querySelectorAll('[data-anpaint-actions]').length,document.querySelector('[data-anpaint-actions]').children[0].textContent,document.querySelector('[data-anpaint-actions]').children[1].textContent,document.querySelector('[data-anpaint-actions]').children[0].href])") {
                                result.set(it);done.countDown()
                            }
                        }}
                    }
                }
                loadDataWithBaseURL(url,html,"text/html","UTF-8",null)
            }
        }
        try {assertTrue("Illustration DOM adaptation timed out",done.await(15,TimeUnit.SECONDS));return JSONArray(JSONTokener(result.get()).nextValue() as String)}
        finally {instrumentation.runOnMainSync {web?.destroy()}}
    }

}
