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
        val preferences = context.getSharedPreferences("app-language", 0)
        val hadLanguage = preferences.contains("language-tag")
        val oldPreference = preferences.getString("language-tag", null)
        val hadInitialization = preferences.contains("platform-initialized")
        val oldInitialization = preferences.getBoolean("platform-initialized", false)
        val oldPlatform = if (Build.VERSION.SDK_INT >= 33)
            context.getSystemService(LocaleManager::class.java).applicationLocales else null
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
                    restoreConfiguredLanguage(oldPreference, oldPlatform)
                    scenario.onActivity { it.onConfigurationChanged(Configuration(it.resources.configuration)) }
                }
            }
            if (Build.VERSION.SDK_INT == 35) exerciseCzechAssemblyPdfImport(launch)
        } finally {
            try {
                // Settle platform callbacks with migration guarded, then restore each
                // original preference independently, including absent keys.
                restoreConfiguredLanguage(oldPreference, oldPlatform)
            } finally {
                instrumentation.runOnMainSync {
                    preferences.edit().apply {
                        if (hadLanguage) putString("language-tag", oldPreference) else remove("language-tag")
                        if (hadInitialization) putBoolean("platform-initialized", oldInitialization)
                        else remove("platform-initialized")
                    }.commit()
                    Locale.setDefault(oldLocale)
                }
                worker.shutdownNow()
                assertTrue(worker.awaitTermination(10, TimeUnit.SECONDS))
            }
        }
    }


    // The locale is configured by the same harness as the English/French cases.
    // This verifies Assembly's real Add Images route, not the system Files UI.
    @androidx.annotation.RequiresApi(35)
    private fun exerciseCzechAssemblyPdfImport(launch: Intent) {
        languageFixture("cs")
        val cs = context.createConfigurationContext(Configuration().apply {
            setLocales(LocaleList.forLanguageTags("cs"))
        })
        val en = context.createConfigurationContext(Configuration().apply {
            setLocales(LocaleList.forLanguageTags("en-US"))
        })
        val directory = File(context.cacheDir, "images").apply { mkdirs() }
        val file = File.createTempFile("czech-assembly-", ".pdf", directory)
        val fixtureUri = androidx.core.content.FileProvider.getUriForFile(context,
            "${context.packageName}.fileprovider", file)
        val intercepted = java.util.concurrent.atomic.AtomicInteger()
        val monitor = object : android.app.Instrumentation.ActivityMonitor() {
            override fun onStartActivity(intent: Intent): android.app.Instrumentation.ActivityResult? {
                if (intent.action != Intent.ACTION_OPEN_DOCUMENT ||
                    !intent.hasCategory(Intent.CATEGORY_OPENABLE) ||
                    !intent.getBooleanExtra(Intent.EXTRA_ALLOW_MULTIPLE, false)) return null
                intercepted.incrementAndGet()
                return android.app.Instrumentation.ActivityResult(android.app.Activity.RESULT_OK,
                    Intent().setData(fixtureUri).addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION))
            }
        }
        val failure = AtomicReference<Throwable>()
        val pdf = PdfDocument()
        try {
            try {
                for ((index, size) in listOf(24 to 32, 40 to 28).withIndex()) {
                    val page = pdf.startPage(PdfDocument.PageInfo.Builder(size.first, size.second, index + 1).create())
                    pdf.finishPage(page)
                }
                file.outputStream().use { pdf.writeTo(it) }
            } finally { pdf.close() }
            assertEquals(2, PdfCodec.pageCount(file))
            instrumentation.addMonitor(monitor)
            ActivityScenario.launch<AssemblyActivity>(launch).use { scenario ->
                var original = emptySet<String>()
                var capturedOriginal = false
                val device = androidx.test.uiautomator.UiDevice.getInstance(instrumentation)
                fun chooserRoot(): View? =
                    android.view.inspector.WindowInspector.getGlobalWindowViews().asReversed().firstOrNull {
                        it.findViewWithTag<EditText>("import_page_number")?.isShown == true
                    }
                fun pressLabel(label: String) {
                    val action = device.findObject(androidx.test.uiautomator.UiSelector().text(label).clickable(true))
                    assertTrue("Visible action: $label", action.waitForExists(5_000L))
                    assertTrue("Tapped action: $label", action.click())
                }

                fun tapChooserButton(id: Int, label: String) {
                    val screen = android.graphics.Rect()
                    scenario.onActivity {
                        val root = requireNotNull(chooserRoot())
                        val button = requireNotNull(root.findViewById<android.widget.Button>(id))
                        val local = android.graphics.Rect()
                        val location = IntArray(2)
                        button.getLocationOnScreen(location)
                        android.util.Log.i("CzechAssemblyPdfTest",
                            "footer id=$id label=${button.text} shown=${button.isShown} enabled=${button.isEnabled} screen=${location.toList()}")
                        assertEquals("Native footer label", label, button.text.toString())
                        assertTrue("Native footer action is enabled and fully visible",
                            button.isShown && button.isEnabled && button.width > 0 && button.height > 0 &&
                                button.getLocalVisibleRect(local) &&
                                local.contains(0, 0, button.width, button.height))
                        screen.set(location[0], location[1], location[0] + button.width, location[1] + button.height)
                    }
                    assertTrue("Injected native footer tap: $label", device.click(screen.centerX(), screen.centerY()))
                }
                fun openChooser() {
                    pressLabel(cs.getString(org.catrobat.paintroid.R.string.ui_add_images))
                    await("Assembly PDF chooser", failure) {
                        var ready = false
                        scenario.onActivity { ready = chooserRoot() != null }
                        ready
                    }
                }
                try {
                    await("initial Czech assembly", failure) {
                        var ready = false
                        scenario.onActivity { ready = !it.busy && it.window.decorView.hasWindowFocus() }
                        ready
                    }
                    scenario.onActivity {
                        original = it.assembly.images.map { item -> item.id }.toSet()
                        capturedOriginal = true
                        assertEquals("cs", it.resources.configuration.locales[0].toLanguageTag())
                        assertTrue("The fixture needs one free assembly slot", original.size < 20)
                    }
                    val range = cs.getString(org.catrobat.paintroid.R.string.formats22_page_range, 2)
                    val open = cs.getString(org.catrobat.paintroid.R.string.formats22_open_page)
                    assertNotEquals(en.getString(org.catrobat.paintroid.R.string.formats22_page_range, 2), range)
                    assertNotEquals(en.getString(org.catrobat.paintroid.R.string.formats22_open_page), open)
                    openChooser()
                    scenario.onActivity {
                        val root = requireNotNull(chooserRoot())
                        val page = root.findViewWithTag<EditText>("import_page_number")
                        page.setText("3") // Exercise the real input watcher, not an injected validation state.
                        assertEquals(range, root.findViewWithTag<TextView>("import_page_status").text.toString())
                        val openButton = root.findViewById<android.widget.Button>(android.R.id.button1)
                        assertEquals(open, openButton.text.toString())
                        assertFalse("An invalid page cannot be opened", openButton.isEnabled)
                    }
                    tapChooserButton(android.R.id.button2, cs.getString(org.catrobat.paintroid.R.string.ui_cancel))
                    await("cancelled import leaves Assembly idle", failure) {
                        var ready = false
                        scenario.onActivity { ready = !it.busy && chooserRoot() == null }
                        ready
                    }
                    scenario.onActivity { assertEquals(original, it.assembly.images.map { item -> item.id }.toSet()) }
                    openChooser()
                    scenario.onActivity {
                        requireNotNull(chooserRoot()).findViewWithTag<EditText>("import_page_number").setText("2")
                    }
                    val secondPage = cs.getString(org.catrobat.paintroid.R.string.formats22_page_dimensions, 2, 2, 80, 56)
                    await("second PDF page decoded", failure) {
                        var ready = false
                        scenario.onActivity {
                            ready = chooserRoot()?.findViewWithTag<TextView>("import_page_status")?.text?.toString() == secondPage
                        }
                        ready
                    }
                    tapChooserButton(android.R.id.button1, open)
                    await("selected PDF page committed to Assembly", failure) {
                        var ready = false
                        scenario.onActivity { ready = !it.busy && it.assembly.images.size == original.size + 1 }
                        ready
                    }
                    scenario.onActivity { activity ->
                        val inserted = activity.assembly.images.single { it.id !in original }
                        assertEquals(file.name, inserted.name)
                        assertEquals(1, inserted.pageIndex)
                        assertEquals(80, inserted.dimensions.width)
                        assertEquals(56, inserted.dimensions.height)
                        assertNotNull(activity.window.decorView.findViewWithTag<View>("assembly_item_${inserted.id}"))
                        val stored = ImageAssembly(activity.assembly.directory).images.single { it.id == inserted.id }
                        assertEquals(inserted.pageIndex, stored.pageIndex)
                        assertEquals(inserted.dimensions, stored.dimensions)
                    }
                    assertEquals("Both imports used Assembly's external picker contract", 2, intercepted.get())
                    android.util.Log.i("CzechAssemblyPdfTest", "range, cancel and persisted second PDF page passed")
                } finally {
                    if (capturedOriginal) scenario.onActivity { activity ->
                        activity.assembly.images.filter { it.id !in original && it.name == file.name }
                            .forEach { activity.assembly.remove(it.id) }
                    }
                }
            }
        } finally {
            instrumentation.removeMonitor(monitor)
            file.delete()
        }
    }

    private fun restoreConfiguredLanguage(preference: String?, platform: LocaleList?) {
        instrumentation.runOnMainSync {
            context.getSharedPreferences("app-language", 0).edit().putString("language-tag", preference)
                .putBoolean("platform-initialized", true).commit()
            if (Build.VERSION.SDK_INT >= 33)
                context.getSystemService(LocaleManager::class.java).applicationLocales = requireNotNull(platform)
        }
        instrumentation.waitForIdleSync()
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
