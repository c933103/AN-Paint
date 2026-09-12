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
}
