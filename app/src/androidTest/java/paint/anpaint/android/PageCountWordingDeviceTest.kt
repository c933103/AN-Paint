/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.AlertDialog
import android.app.LocaleManager
import android.content.Intent
import android.content.res.Configuration
import android.graphics.pdf.PdfDocument
import android.os.SystemClock
import android.os.Build
import android.os.LocaleList
import android.util.Base64
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.TextView
import androidx.test.core.app.ActivityScenario
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.SdkSuppress
import androidx.test.platform.app.InstrumentationRegistry
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.util.Locale
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicReference

/** Real PDF/TIFF inspection -> chooser -> selected page, including single-page native TIFF. */
@RunWith(AndroidJUnit4::class)
@SdkSuppress(minSdkVersion = 30)
class PageCountWordingDeviceTest {
    private val instrumentation = InstrumentationRegistry.getInstrumentation()
    private val context get() = instrumentation.targetContext

    @Test fun oneAndTwoPagePdfAndTiffRetainCountsNamesControlsAndSelectionInEnglishAndFrench() {
        val oldTag = if (Build.VERSION.SDK_INT >= 33)
            context.getSystemService(LocaleManager::class.java).applicationLocales.toLanguageTags()
            else context.getSharedPreferences("app-language", 0).getString("language-tag", "").orEmpty()
        val oldLocale = Locale.getDefault()
        val worker = Executors.newSingleThreadExecutor()
        val launch = Intent(context, AssemblyActivity::class.java).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        try {
            ActivityScenario.launch<AssemblyActivity>(launch).use { scenario ->
                try {
                    for (tag in listOf("", "en-001", "en-AU", "en-CA", "en-GB", "en-IN", "en-SG", "en-US", "en-XV", "fr")) {
                        languageFixture(tag)
                        scenario.onActivity { activity ->
                            // Exercise production configuration/resource routing. The fixture seeds the
                            // language preference; it does not claim to test the language-picker UI.
                            activity.onConfigurationChanged(Configuration(activity.resources.configuration))
                            val actual = activity.resources.configuration.locales[0]
                            if (tag.isEmpty()) assertEquals("Controlled emulator device language", "en", actual.language)
                            else assertEquals(tag, actual.toLanguageTag())
                        }
                        for (kind in listOf("PDF", "TIFF")) for (count in 1..2) {
                            val file = fixture(kind, count)
                            var selection: ImportSelection? = null
                            val selected = AtomicReference<ImportedImage>()
                            val failure = AtomicReference<Throwable>()
                            try {
                                scenario.onActivity { activity ->
                                    selection = ImportSelection(activity, worker, { 0L }, { selected.set(it) },
                                        { fail("Unexpected cancellation") }, { failure.set(it) })
                                    selection!!.start(file, "scan.$kind")
                                }
                                var dialog: AlertDialog? = null
                                await("page chooser", failure) {
                                    scenario.onActivity {
                                        dialog = ImportSelection::class.java.getDeclaredField("dialog").apply { isAccessible = true }.get(selection) as? AlertDialog
                                    }
                                    dialog?.isShowing == true
                                }
                                scenario.onActivity {
                                    val root = dialog!!.window!!.decorView
                                    val expected = "$kind · scan.$kind\n" + if (tag == "fr")
                                        "Nombre de pages : $count. Choisissez une page à modifier comme image."
                                        else "Number of pages: $count. Choose one page to edit as an image."
                                    assertTrue("$tag / $kind / $count", texts(root).contains(expected))
                                    assertFalse(root.findViewWithTag<View>("import_previous_page").isEnabled)
                                    assertEquals(count > 1, root.findViewWithTag<View>("import_next_page").isEnabled)
                                    assertEquals("1", root.findViewWithTag<EditText>("import_page_number").text.toString())
                                    if (count == 2) root.findViewWithTag<View>("import_next_page").performClick()
                                    assertEquals(count.toString(), root.findViewWithTag<EditText>("import_page_number").text.toString())
                                    assertFalse(root.findViewWithTag<View>("import_next_page").isEnabled)
                                    assertTrue(dialog!!.getButton(AlertDialog.BUTTON_POSITIVE).performClick())
                                }
                                await("selected page", failure) { selected.get() != null }
                                assertEquals(count - 1, selected.get().pageIndex)
                                assertEquals(file, selected.get().file)
                                assertTrue(selected.get().dimensions.width > 0)
                                assertTrue(file.exists())
                            } finally {
                                scenario.onActivity { selection?.dispose() }
                                worker.submit {}.get(10, TimeUnit.SECONDS)
                                file.delete()
                            }
                        }
                    }
                } finally {
                    languageFixture(oldTag)
                    scenario.onActivity { it.onConfigurationChanged(Configuration(it.resources.configuration)) }
                }
            }
        } finally {
            Locale.setDefault(oldLocale)
            worker.shutdownNow()
            assertTrue(worker.awaitTermination(10, TimeUnit.SECONDS))
        }
    }

    private fun languageFixture(tag: String) {
        instrumentation.runOnMainSync {
            context.getSharedPreferences("app-language", 0).edit().putString("language-tag", tag)
                .putBoolean("platform-initialized", true).commit()
            if (Build.VERSION.SDK_INT >= 33)
                context.getSystemService(LocaleManager::class.java).applicationLocales = LocaleList.forLanguageTags(tag)
        }
        instrumentation.waitForIdleSync()
    }

    private fun fixture(kind: String, count: Int): File = File.createTempFile("page-count-", ".bin", context.cacheDir).apply {
        if (kind == "PDF") {
            val document = PdfDocument()
            try {
                repeat(count) {
                    val page = document.startPage(PdfDocument.PageInfo.Builder(24, 32, it + 1).create())
                    document.finishPage(page)
                }
                outputStream().use { document.writeTo(it) }
            } finally { document.close() }
            assertEquals(count, PdfCodec.pageCount(this))
        } else {
            val name = if (count == 1) "one" else "two"
            val encoded = instrumentation.context.assets.open("count-wording/$name.tif.b64").bufferedReader().use { it.readText() }
            writeBytes(Base64.decode(encoded, Base64.DEFAULT))
            assertEquals(count, TiffCodec.pageCount(this))
        }
    }

    private fun texts(view: View): List<String> = buildList {
        if (view is TextView) add(view.text.toString())
        if (view is ViewGroup) for (index in 0 until view.childCount) addAll(texts(view.getChildAt(index)))
    }

    private fun await(label: String, failure: AtomicReference<Throwable>, ready: () -> Boolean) {
        val deadline = SystemClock.uptimeMillis() + 10_000
        while (SystemClock.uptimeMillis() < deadline) {
            failure.get()?.let { throw AssertionError(label, it) }
            if (ready()) return
            SystemClock.sleep(20)
        }
        throw AssertionError("Timed out waiting for $label", failure.get())
    }
}
