/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.content.Intent
import android.content.res.Configuration
import android.content.res.Resources
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Rect
import android.net.Uri
import android.os.Looper
import android.text.Spanned
import android.text.style.ReplacementSpan
import android.view.ContextThemeWrapper
import android.view.View
import android.webkit.WebView
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.LooperMode
import org.robolectric.shadows.ShadowToast
import org.robolectric.util.ReflectionHelpers
import java.io.ByteArrayInputStream
import java.io.File
import java.net.HttpURLConnection
import java.net.URL
import java.util.Locale
import java.util.concurrent.TimeUnit

/** Real Activity/resources/failure path with native-rendered host pixels, not device screenshots. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class CommonsSvgErrorReadabilityTest {
    // Configure scale before PaintApplication and any locale-derived Resources
    // exist. setFontScale inside a loop leaves cached wrapped contexts stale.
    @Test @Config(fontScale=1f)
    fun verticalGalleryErrorsProduceNormalTextDiagnosticCapturesWithoutLayoutAcceptance()=checkVertical(1f)

    @Test @Config(fontScale=2f)
    fun verticalGalleryErrorsProduceLargeTextDiagnosticCapturesWithoutLayoutAcceptance()=checkVertical(2f)

    @Test @Config(fontScale=1f)
    fun horizontalGalleryErrorsWrapWithoutClippingAtNormalText()=checkHorizontal(1f)

    @Test @Config(fontScale=2f)
    fun horizontalGalleryErrorsWrapWithoutClippingAtLargeText()=checkHorizontal(2f)

    private fun checkVertical(scale: Float) {
        // AN-W04 owns the missing vertical status renderer. A successful capture
        // is NOT a vertical readability or clipping pass.
        GallerySvgReadabilityFixture.check(listOf("mn-Mong","mnc-Mong"),scale) {_,_ -> Unit}
    }

    private fun checkHorizontal(scale: Float) {
        // Long Latin, mixed RTL/Latin, supplementary Nôm, Tibetan and Dzongkha.
        GallerySvgReadabilityFixture.check(listOf("fr","hak-Latn-TW","ar","vi-Hani","bo","dz"),scale) {
                tag,status ->
            GallerySvgReadabilityFixture.assertEntireMessageVisible(status)
            if(tag=="ar") assertEquals("Arabic status must inherit RTL layout",View.LAYOUT_DIRECTION_RTL,status.layoutDirection)
            if(tag=="vi-Hani") {
                assertSame("Nôm status must retain its bundled UI font",LocaleTypography.typeface(status.context),status.typeface)
                status.text.toString().codePoints().filter {it>0xffff}.forEach {point ->
                    assertTrue("Missing displayed Nôm U+${point.toString(16)}",status.paint.hasGlyph(String(Character.toChars(point))))
                }
            }
        }
    }
}

/** Also reusable by the isolated AN-W04 vertical regression candidate in verification/. */
internal object GallerySvgReadabilityFixture {
    private const val source="https://upload.wikimedia.org/wikipedia/commons/a/ab/Readability.svg"
    private const val page="https://commons.wikimedia.org/wiki/File:Readability.svg"
    private val cases=listOf(
        R.string.commons_svg_original_size_unavailable to """<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 40 24"/>""",
        R.string.commons_svg_original_size_too_large to """<svg xmlns="http://www.w3.org/2000/svg" width="2147483648" height="1"/>"""
    )
    private class Connection(url: URL,svg: String): HttpURLConnection(url) {
        private val input=ByteArrayInputStream(svg.toByteArray(Charsets.UTF_8))
        override fun connect()=Unit
        override fun disconnect() {input.close()}
        override fun usingProxy()=false
        override fun getResponseCode()=200
        override fun getInputStream()=input
    }
    private fun await(done: ()->Boolean) {
        val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(8)
        while(!done() && System.nanoTime()<deadline) {
            shadowOf(Looper.getMainLooper()).idle();Thread.sleep(5)
        }
        shadowOf(Looper.getMainLooper()).idle()
        assertTrue("The real gallery failure must finish within 8 seconds",done())
    }
    fun check(tags: List<String>,scale: Float=RuntimeEnvironment.getFontScale(),reportDirectory: String="svg-error-readability",assertReadability: (String,TextView)->Unit) {
        val context=RuntimeEnvironment.getApplication() as Context
        val originalTag=AppLanguage.selectedTag(context)
        val originalLocale=Locale.getDefault()
        val originalResources=PaintApplication.currentResources
        val failures=mutableListOf<String>()
        try {
            assertEquals("Robolectric must establish system scale before app creation",scale,Resources.getSystem().configuration.fontScale,0f)
            assertEquals("PaintApplication wrapping must preserve system scale",scale,context.resources.configuration.fontScale,0f)
            for(tag in tags) {
                AppLanguage.select(context,tag)
                val wrapped=AppLanguage.wrap(context).resources
                assertEquals("Language wrapping must preserve inherited system scale for $tag",scale,wrapped.configuration.fontScale,0f)
                PaintApplication.currentResources=wrapped
                val controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,
                    Intent(context,MediaGalleryActivity::class.java)
                        .putExtra("gallery_provider",IllustrationSource.COMMONS.name))
                    .setup().visible().windowFocusChanged(true)
                val activity=controller.get()
                try {
                    assertEquals("The real Activity must receive the requested font scale",scale,activity.resources.configuration.fontScale,0f)
                    val status=activity.window.decorView.findViewWithTag<TextView>("gallery_status")
                    // Only the independent normal-size reference uses an override.
                    // Never mutate the Activity/resources/status being measured.
                    val normalContext=activity.createConfigurationContext(Configuration().apply {fontScale=1f})
                    val theme=activity.packageManager.getActivityInfo(activity.componentName,0).themeResource
                    val normalTextSize=TextView(ContextThemeWrapper(normalContext,theme)).textSize
                    assertEquals("Reference construction must not change the measured Activity",scale,activity.resources.configuration.fontScale,0f)
                    val web=ReflectionHelpers.getField<WebView>(activity,"web")
                    for((key,svg) in cases) {
                        val name=activity.resources.getResourceEntryName(key)
                        val label="api${RuntimeEnvironment.getApiLevel()}-$tag-font$scale-$name"
                        try {
                            val reason=activity.getString(key)
                            val expected=activity.getString(R.string.ui_could_not_load_gallery_image,reason)
                            activity.openConnection={url ->
                                assertEquals("Size rejection must precede attribution requests",source,url.toString())
                                Connection(url,svg)
                            }
                            ShadowToast.reset()
                            val link=Uri.Builder().scheme(IllustrationPage.USE_SCHEME).authority("insert")
                                .appendQueryParameter("source",source).appendQueryParameter("page",page).build()
                            assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,link.toString()))
                            await {!activity.downloading && status.text.toString()==expected}
                            layout(activity.window.decorView)
                            // Persist pixels and geometry before assertions, including any clipping.
                            record(activity.window.decorView,status,tag,scale,label,reportDirectory)
                            assertEquals(expected,status.text.toString())
                            if(scale>1f) assertTrue("Large system text must enlarge the actual status glyphs",status.textSize>normalTextSize)
                            assertTrue(status.isAttachedToWindow)
                            assertNull("SVG failures must not rely on a system Toast",ShadowToast.getLatestToast())
                            assertFalse(activity.isFinishing)
                            assertReadability(tag,status)
                            // A persistent gallery message must survive longer than a text Toast.
                            shadowOf(Looper.getMainLooper()).idleFor(5,TimeUnit.SECONDS)
                            assertEquals(View.VISIBLE,status.visibility)
                            assertEquals(expected,status.text.toString())
                        } catch(error: AssertionError) {
                            // Retain all representative screenshots instead of stopping at the first failure.
                            failures.add("$label: ${error.message}")
                        }
                    }
                } finally {
                    activity.finish();controller.pause().stop().destroy()
                    ShadowToast.reset()
                }
            }
        } finally {
            AppLanguage.select(context,originalTag)
            PaintApplication.currentResources=originalResources
            Locale.setDefault(originalLocale)
        }
        assertTrue(failures.joinToString("\n"),failures.isEmpty())
    }
    private fun layout(root: View) {
        val metrics=root.resources.displayMetrics
        val config=root.resources.configuration
        val width=(config.screenWidthDp*metrics.density+.5f).toInt()
        val height=(config.screenHeightDp*metrics.density+.5f).toInt()
        root.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),
            View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.EXACTLY))
        root.layout(0,0,width,height)
    }
    fun assertEntireMessageVisible(status: TextView) {
        assertTrue("Persistent message must be displayed",status.isShown)
        assertNull("Do not ellipsize the rejection reason",status.ellipsize)
        val textLayout=requireNotNull(status.layout)
        assertTrue("Message must have laid-out lines",textLayout.lineCount>0)
        assertTrue("Text layout must fit the status content width",textLayout.width<=status.width-status.compoundPaddingLeft-status.compoundPaddingRight)
        assertEquals("Final characters must be present in the layout",status.text.length,textLayout.getLineEnd(textLayout.lineCount-1))
        assertTrue("Measured height must include the final line",textLayout.height<=status.height-status.totalPaddingTop-status.totalPaddingBottom)
        for(line in 0 until textLayout.lineCount) {
            assertEquals("Line $line must not be ellipsized",0,textLayout.getEllipsisCount(line))
            assertTrue("Line $line must fit horizontally",textLayout.getLineLeft(line)>=-1f && textLayout.getLineRight(line)<=textLayout.width+1f)
        }
        val visible=Rect()
        assertTrue("A parent must not hide the status",status.getGlobalVisibleRect(visible))
        assertEquals("A parent must not clip status width",status.width,visible.width())
        assertEquals("A parent must not clip status height",status.height,visible.height())
    }
    fun hasVerticalRenderer(status: TextView)=status is FlowTextView ||
        status.getTag(R.id.vertical_caption_installed)==true

    private fun record(root: View,status: TextView,tag: String,scale: Float,label: String,reportDirectory: String) {
        val folder=File("build/reports/$reportDirectory").apply {mkdirs()}
        val bitmap=Bitmap.createBitmap(root.width,root.height,Bitmap.Config.ARGB_8888)
        try {
            root.draw(Canvas(bitmap))
            File(folder,"$label.png").outputStream().use {assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))}
        } finally {bitmap.recycle()}
        val visible=Rect();val intersectsVisibleArea=status.getGlobalVisibleRect(visible)
        val textLayout=requireNotNull(status.layout)
        val lines=JSONArray()
        for(line in 0 until textLayout.lineCount) lines.put(JSONObject()
            .put("start",textLayout.getLineStart(line)).put("end",textLayout.getLineEnd(line))
            .put("left",textLayout.getLineLeft(line)).put("right",textLayout.getLineRight(line))
            .put("bottom",textLayout.getLineBottom(line)).put("ellipsis_count",textLayout.getEllipsisCount(line)))
        val spans=(status.text as? Spanned)?.getSpans(0,status.text.length,ReplacementSpan::class.java).orEmpty()
        val vertical=VerticalText.uiDirection(Locale.forLanguageTag(tag))!=TextDirection.HORIZONTAL
        val report=JSONObject().put("evidence_kind","Robolectric NATIVE host rendering; not a device capture")
            .put("api",RuntimeEnvironment.getApiLevel()).put("locale",tag).put("font_scale",scale)
            .put("activity_font_scale",root.resources.configuration.fontScale)
            .put("application_font_scale",RuntimeEnvironment.getApplication().resources.configuration.fontScale)
            .put("system_font_scale",Resources.getSystem().configuration.fontScale)
            .put("viewport_width",root.width).put("viewport_height",root.height)
            .put("message",status.text.toString()).put("view_class",status.javaClass.name)
            .put("text_size_px",status.textSize).put("status_width",status.width).put("status_height",status.height)
            .put("visible_bounds",visible.toShortString()).put("text_layout_height",textLayout.height)
            .put("status_is_shown",status.isShown)
            .put("entire_status_visible",intersectsVisibleArea && visible.width()==status.width && visible.height()==status.height)
            .put("all_characters_laid_out",textLayout.lineCount>0 && textLayout.getLineEnd(textLayout.lineCount-1)==status.text.length)
            .put("layout_fits_content_height",textLayout.height<=status.height-status.totalPaddingTop-status.totalPaddingBottom)
            .put("content_height",status.height-status.totalPaddingTop-status.totalPaddingBottom)
            .put("layout_direction",status.layoutDirection).put("vertical_expected",vertical)
            .put("vertical_renderer_present",hasVerticalRenderer(status)).put("replacement_span_count",spans.size)
            .put("vertical_acceptance",if(!vertical) "not applicable" else if(reportDirectory=="gallery-vertical-status")
                "Consult exact-head GalleryVerticalStatusTest JUnit result; capture alone is not acceptance"
                else "pending separate AN-W04 regression; this capture is not acceptance")
            .put("lines",lines)
        File(folder,"$label.json").writeText(report.toString(2)+"\n")
    }
}
