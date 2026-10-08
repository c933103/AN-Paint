/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.net.Uri
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.json.JSONArray
import org.json.JSONObject
import org.json.JSONTokener
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicReference

/** Native WebView/HTML-parser tests with local fixtures; no Commons requests or artwork downloads. */
@RunWith(AndroidJUnit4::class)
class CommonsCreditDeviceTest {
    @Test fun svgOriginalAndCreditActionsAreStableAndDoNotUseThePreview() {
        val source="https://upload.wikimedia.org/wikipedia/commons/a/ab/Test_map.svg"
        val page="https://commons.wikimedia.org/wiki/File:Test_map.svg"
        val result=adapt(page,source)
        assertEquals(1,result.getInt(0));assertEquals(2,result.getInt(1))
        assertEquals("Use image",result.getString(2));assertEquals("Copy credit",result.getString(3))
        val use=Uri.parse(result.getString(4));val credit=Uri.parse(result.getString(5))
        assertEquals(IllustrationPage.USE_SCHEME,use.scheme)
        assertEquals(GalleryPage.CREDIT_SCHEME,credit.scheme)
        assertEquals(source,use.getQueryParameter("source"));assertEquals(source,credit.getQueryParameter("source"))
        assertEquals(page,credit.getQueryParameter("page"));assertEquals("File:Test map",credit.getQueryParameter("title"))
    }

    @Test fun rasterOriginalHasCreditActionsOnIndexPhpFilePagesToo() {
        val source="https://upload.wikimedia.org/wikipedia/commons/a/ab/Test_map.png"
        val page="https://commons.wikimedia.org/w/index.php?title=File%3ATest_map.png"
        val result=adapt(page,source)
        assertEquals(1,result.getInt(0));assertEquals(2,result.getInt(1))
        assertEquals(source,Uri.parse(result.getString(5)).getQueryParameter("source"))
        assertEquals(page,Uri.parse(result.getString(5)).getQueryParameter("page"))
    }

    @Test fun nativeMetadataParsingAndRetentionPreserveCreatorsLinksAndTheActualLicence() {
        val context=InstrumentationRegistry.getInstrumentation().targetContext
        val source="https://upload.wikimedia.org/wikipedia/commons/a/ab/Native_credit_fixture.svg"
        val page="https://commons.wikimedia.org/wiki/File:Native_credit_fixture.svg"
        // A repeated installed run must not mistake a previous test fixture for a real insertion.
        context.getSharedPreferences("image-credits",0).edit()
            .putStringSet("sources",GalleryCredits.sources(context)-source)
            .remove("text:$source").remove("generated:$source").commit()
        val metadata=JSONObject()
        fun field(key: String,value: String) {metadata.put(key,JSONObject().put("value",value))}
        field("Artist","<a href=\"/wiki/User:Mapper\">Mapper A</a> &amp; Mapper B")
        field("LicenseShortName","CC BY-SA 3.0")
        field("LicenseUrl","https://creativecommons.org/licenses/by-sa/3.0/")
        field("Attribution","Custom required attribution")
        val image=JSONObject().put("url",source).put("descriptionurl",page).put("extmetadata",metadata)
        val file=JSONObject().put("ns",6).put("title","File:Native_credit_fixture.svg")
            .put("imageinfo",JSONArray().put(image))
        val query=JSONObject().put("pages",JSONArray().put(file))
        val json=JSONObject().put("query",query).toString()
        val record=CommonsAttribution.parse(json,source)
        CommonsAttribution.cache(context,record)
        assertEquals(record,CommonsAttribution.cached(context,source))
        assertFalse(GalleryCredits.sources(context).contains(source))
        GalleryCredits.remember(context,source,IllustrationSource.COMMONS,page,"Native fixture")
        val retained=GalleryCredits.text(context)
        for(text in listOf("Mapper A & Mapper B","https://commons.wikimedia.org/wiki/User:Mapper",
            "CC BY-SA 3.0","https://creativecommons.org/licenses/by-sa/3.0/","Custom required attribution","antiAlias=false"))
            assertTrue("Missing attribution: $text",retained.contains(text))
        assertFalse(record.text(false).contains("antiAlias=false"))
    }

    private fun adapt(page: String,source: String): JSONArray {
        val instrumentation=InstrumentationRegistry.getInstrumentation();val done=CountDownLatch(1)
        val result=AtomicReference<String>();var web: WebView?=null
        instrumentation.runOnMainSync {
            web=WebView(instrumentation.targetContext).apply {
                settings.javaScriptEnabled=true;settings.blockNetworkLoads=true
                settings.allowFileAccess=false;settings.allowContentAccess=false
                webViewClient=object: WebViewClient() {
                    override fun onPageFinished(view: WebView,loaded: String) {
                        val script=IllustrationPage.script(IllustrationSource.COMMONS,"Use image","Copy credit")
                        view.evaluateJavascript(script) {view.evaluateJavascript(script) {
                            view.evaluateJavascript("JSON.stringify((function(){var r=document.getElementById('anpaint-commons-actions');return r?[document.querySelectorAll('#anpaint-commons-actions').length,r.children.length,r.children[0].textContent,r.children[1].textContent,r.children[0].href,r.children[1].href]:[]})())") {
                                result.set(it);done.countDown()
                            }
                        }}
                    }
                }
                loadDataWithBaseURL(page,"""<html><head><title>File:Test map - Wikimedia Commons</title></head><body>
                    <a href="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Test_map.svg/800px-Test_map.svg.png">Preview</a>
                    <div class="fullMedia"><a class="internal" href="$source">Original file</a></div>
                    </body></html>""".trimIndent(),"text/html","UTF-8",null)
            }
        }
        try {
            assertTrue("Commons DOM adaptation timed out",done.await(15,TimeUnit.SECONDS))
            return JSONArray(JSONTokener(result.get()).nextValue() as String)
        } finally {instrumentation.runOnMainSync {web?.destroy()}}
    }
}
