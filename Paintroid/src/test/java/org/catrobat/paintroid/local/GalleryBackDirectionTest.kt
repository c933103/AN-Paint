/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.LocaleManager
import android.content.Context
import android.content.Intent
import android.content.res.Configuration
import android.content.res.Resources
import android.graphics.Bitmap
import android.graphics.Canvas
import android.os.Build
import android.os.Bundle
import android.text.Spanned
import android.text.style.ReplacementSpan
import android.view.View
import android.webkit.WebView
import android.widget.EditText
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
import org.robolectric.android.controller.ActivityController
import org.robolectric.util.ReflectionHelpers
import java.io.File
import java.util.Locale

/** Real production Activity/views; WebView history is Robolectric's offline model, not Chromium. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="en-rUS-w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class GalleryBackDirectionTest {
    // Independent script-direction oracle for the current picker, not the production expression.
    private val rtlTags=setOf("ar","ckb","fa","fa-IR","he","ps","sd","ug","ur","yi")
    private val captureTags=setOf("en-001","ar","he","mn-Mong","mnc-Mong","lzh-Hant","qaa-Zsye-XV")
    private val app get()=RuntimeEnvironment.getApplication() as Context

    @Test @Config(fontScale=2f)
    fun everyOfferedLocaleUsesAccessibleBackAndKeepsBothNavigationBranches()=withLanguageState {
        val tags=AppLanguage.tags(app)
        assertEquals(140,tags.size)
        assertTrue(tags.containsAll(rtlTags))
        val records=JSONArray()
        try {
            for((index,tag) in tags.withIndex()) {
                select(tag)
                val provider=IllustrationSource.values()[index % IllustrationSource.values().size]
                val controller=open(provider)
                try {
                    val activity=controller.get()
                    assertEquals(tag,activity.resources.configuration.locales[0].toLanguageTag())
                    val expected=if(tag in rtlTags) "→" else "←"
                    val button=assertBack(activity,expected)
                    val web=ReflectionHelpers.getField<WebView>(activity,"web")
                    val browser=shadowOf(web)
                    val search=activity.window.decorView.findViewWithTag<EditText>("gallery_search")
                    search.setText("retained query नदी 山")
                    assertFalse(web.canGoBack())
                    assertTrue(button.performClick())
                    assertEquals(provider.home,browser.lastLoadedUrl)
                    assertEquals(0,browser.goBackInvocations)
                    // Only this test's shadow history changes; neither URL is requested on a network.
                    browser.pushEntryToHistory("https://example.invalid/gallery-first")
                    browser.pushEntryToHistory("https://example.invalid/gallery-second")
                    assertTrue(web.canGoBack())
                    assertTrue(button.performClick())
                    assertEquals(1,browser.goBackInvocations)
                    assertEquals("https://example.invalid/gallery-first",web.url)
                    assertEquals("History Back must not issue another home load",provider.home,browser.lastLoadedUrl)
                    assertFalse(web.canGoBack())
                    assertTrue(button.performClick())
                    assertEquals(provider.home,web.url)
                    assertEquals(1,browser.goBackInvocations)
                    assertEquals("retained query नदी 山",search.text.toString())
                    assertFalse(activity.isFinishing)
                    val navigation=activity.window.decorView.findViewWithTag<View>("gallery_navigation")
                    records.put(JSONObject().put("locale",tag).put("arrow",button.text.toString())
                        .put("app_layout_direction",activity.resources.configuration.layoutDirection)
                        .put("row_layout_direction",navigation.layoutDirection)
                        .put("accessible_description",button.contentDescription.toString())
                        .put("provider",provider.name).put("history_back_calls",browser.goBackInvocations))
                    if(tag in captureTags) capture(activity,tag)
                } finally {close(controller)}
            }
        } finally {
            val folder=File("build/reports/gallery-back-direction").apply {mkdirs()}
            File(folder,"api${Build.VERSION.SDK_INT}-locales.json").writeText(JSONObject()
                .put("evidence_kind","Robolectric NATIVE production views; offline ShadowWebView history; not installed-device execution")
                .put("expected_locales",tags.size).put("completed_locales",records.length())
                .put("locales",records).toString(2)+"\n")
        }
        assertEquals(tags.size,records.length())
    }

    @Test @Config(qualifiers="ar-w320dp-h640dp-port-xhdpi")
    fun explicitAppOverridesAndDeviceDefaultUseTheEffectiveActivityLocale()=withLanguageState {
        assertEquals("ar",Resources.getSystem().configuration.locales[0].language)
        for((tag,expected) in listOf("en-001" to "←","" to "→","he" to "→","en-001" to "←")) {
            select(tag)
            val controller=open(IllustrationSource.COMMONS)
            try {
                assertEquals(if(tag.isEmpty()) "ar" else tag,
                    controller.get().resources.configuration.locales[0].toLanguageTag())
                assertBack(controller.get(),expected)
            } finally {close(controller)}
        }
    }

    @Test fun localeSwitchRecreationUpdatesArrowAndRestoresBrowserHistory()=withLanguageState {
        select("en-001")
        var controller=open(IllustrationSource.COMMONS)
        try {
            assertBack(controller.get(),"←")
            val initialWeb=ReflectionHelpers.getField<WebView>(controller.get(),"web")
            shadowOf(initialWeb).pushEntryToHistory("https://example.invalid/first")
            shadowOf(initialWeb).pushEntryToHistory("https://example.invalid/second")
            for((tag,expected) in listOf("ar" to "→","en-001" to "←","he" to "→","en-001" to "←")) {
                val previous=controller.get()
                val state=Bundle()
                // configurationChange() mutates cached old Resources in Robolectric. Replay the
                // save/destroy/create lifecycle with fresh wrapping, without rewriting that cache.
                // This does not establish delivery of a real OS-triggered locale recreation.
                controller.pause().stop().saveInstanceState(state).destroy()
                select(tag)
                controller=open(IllustrationSource.COMMONS,state)
                assertTrue(previous.isDestroyed)
                assertNotSame("Recreation constructs fresh locale-aware gallery views",previous,controller.get())
                val button=assertBack(controller.get(),expected)
                val web=ReflectionHelpers.getField<WebView>(controller.get(),"web")
                assertNotSame(initialWeb,web)
                assertEquals("https://example.invalid/second",web.url)
                assertTrue(web.canGoBack())
                assertTrue(button.performClick())
                assertEquals("https://example.invalid/first",web.url)
                assertEquals(1,shadowOf(web).goBackInvocations)
                shadowOf(web).pushEntryToHistory("https://example.invalid/second")
            }
        } finally {close(controller)}
    }

    /** Negative fixture control: a synthetic Resources mutation can poison its old locale key. */
    @Test @Suppress("DEPRECATION")
    fun syntheticResourceMutationKeepsTheOldLocaleCacheKey()=withLanguageState {
        select("en-001")
        val cached=AppLanguage.wrap(app).resources
        val original=Configuration(cached.configuration)
        try {
            cached.updateConfiguration(Configuration(original).apply {
                val locale=Locale.forLanguageTag("ar");setLocale(locale);setLayoutDirection(locale)
            },cached.displayMetrics)
            val reopened=AppLanguage.wrap(app).resources
            assertEquals("The selected preference is still English","en-001",AppLanguage.selectedTag(app))
            assertSame("Host reuses Resources under the original English override key",cached,reopened)
            assertEquals("The synthetic mutation remains under that stale key","ar",reopened.configuration.locales[0].language)
            assertEquals(View.LAYOUT_DIRECTION_RTL,reopened.configuration.layoutDirection)
        } finally {
            cached.updateConfiguration(original,cached.displayMetrics)
            assertEquals("en-001",cached.configuration.locales[0].toLanguageTag())
            assertEquals(View.LAYOUT_DIRECTION_LTR,cached.configuration.layoutDirection)
        }
    }

    private fun select(tag: String) {
        AppLanguage.select(app,tag)
        // Match the production application resource refresh before the new gallery attaches.
        PaintApplication.currentResources=AppLanguage.wrap(app).resources
    }

    private fun open(provider: IllustrationSource,state: Bundle?=null)=Robolectric.buildActivity(MediaGalleryActivity::class.java,
        Intent(app,MediaGalleryActivity::class.java).putExtra("gallery_provider",provider.name))
        .let {if(state==null) it.setup() else it.setup(state)}.visible().windowFocusChanged(true)

    private fun close(controller: ActivityController<MediaGalleryActivity>) {
        controller.get().finish();controller.close()
    }

    private fun assertBack(activity: MediaGalleryActivity,expected: String): TextView {
        val root=activity.window.decorView
        val metrics=activity.resources.displayMetrics;val config=activity.resources.configuration
        val width=(config.screenWidthDp*metrics.density+.5f).toInt()
        val height=(config.screenHeightDp*metrics.density+.5f).toInt()
        root.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),
            View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.EXACTLY))
        root.layout(0,0,width,height)
        val button=root.findViewWithTag<TextView>("gallery_back")
        assertTrue(button.isAttachedToWindow)
        assertEquals(expected,button.text.toString())
        assertEquals(if(expected=="→") View.LAYOUT_DIRECTION_RTL else View.LAYOUT_DIRECTION_LTR,config.layoutDirection)
        assertEquals(activity.getString(R.string.ui_gallery_back34),button.contentDescription.toString())
        val node=button.createAccessibilityNodeInfo()
        try {
            assertEquals("android.widget.Button",node.className.toString())
            assertEquals(button.contentDescription.toString(),node.contentDescription.toString())
            assertTrue(node.isClickable)
        } finally {node.recycle()}
        val minimum=(48*metrics.density+.5f).toInt()
        assertTrue(button.width>=minimum);assertTrue(button.height>=minimum)
        GalleryControlsLayoutTest.assertFullLayout("gallery back",button)
        assertTrue("The arrow must stay horizontal for vertical scripts",(button.text as? Spanned)
            ?.getSpans(0,button.text.length,ReplacementSpan::class.java).isNullOrEmpty())
        if(VerticalText.uiVertical()) {
            val row=root.findViewWithTag<View>("gallery_navigation")
            assertEquals(if(VerticalText.uiDirection()==TextDirection.VERTICAL_RL) View.LAYOUT_DIRECTION_RTL
                else View.LAYOUT_DIRECTION_LTR,row.layoutDirection)
            assertEquals("←",button.text.toString())
        }
        return button
    }

    private fun capture(activity: MediaGalleryActivity,tag: String) {
        val root=activity.window.decorView
        val button=root.findViewWithTag<View>("gallery_back")
        button.requestRectangleOnScreen(android.graphics.Rect(0,0,button.width,button.height),true)
        val visible=android.graphics.Rect()
        assertTrue(button.getLocalVisibleRect(visible))
        assertEquals(button.width,visible.width());assertEquals(button.height,visible.height())
        val bitmap=Bitmap.createBitmap(root.width,root.height,Bitmap.Config.ARGB_8888)
        try {
            root.draw(Canvas(bitmap))
            val folder=File("build/reports/gallery-back-direction").apply {mkdirs()}
            File(folder,"api${Build.VERSION.SDK_INT}-$tag.png").outputStream().use {
                assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))
            }
        } finally {bitmap.recycle()}
    }

    private fun withLanguageState(check: ()->Unit) {
        val originalLocale=Locale.getDefault()
        val originalResources=PaintApplication.currentResources
        val preferences=app.getSharedPreferences("app-language",Context.MODE_PRIVATE)
        val originalTag=preferences.getString("language-tag",null)
        val hadInitialized=preferences.contains("platform-initialized")
        val originalInitialized=preferences.getBoolean("platform-initialized",false)
        val manager=if(Build.VERSION.SDK_INT>=33) app.getSystemService(LocaleManager::class.java) else null
        val originalPlatform=manager?.applicationLocales
        try {check()} finally {
            if(originalPlatform!=null) manager.applicationLocales=originalPlatform
            val edit=preferences.edit()
            if(originalTag==null) edit.remove("language-tag") else edit.putString("language-tag",originalTag)
            if(hadInitialized) edit.putBoolean("platform-initialized",originalInitialized) else edit.remove("platform-initialized")
            assertTrue(edit.commit())
            PaintApplication.currentResources=originalResources
            Locale.setDefault(originalLocale)
        }
    }
}
