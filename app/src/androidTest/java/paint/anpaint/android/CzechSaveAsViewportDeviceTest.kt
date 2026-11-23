/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.Activity
import android.app.Instrumentation
import android.app.LocaleManager
import android.content.Intent
import android.content.pm.ActivityInfo
import android.content.res.Configuration
import android.graphics.Color
import android.graphics.Rect
import android.os.Build
import android.os.LocaleList
import android.os.SystemClock
import android.provider.Settings
import android.view.View
import android.view.ViewGroup
import android.view.inspector.WindowInspector
import android.view.inputmethod.InputMethodManager
import android.widget.Button
import android.widget.EditText
import android.widget.Spinner
import androidx.test.core.app.ActivityScenario
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.SdkSuppress
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.uiautomator.UiDevice
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.ImageFormat
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.util.Locale
import java.util.concurrent.atomic.AtomicInteger
import java.util.concurrent.atomic.AtomicReference

@RunWith(AndroidJUnit4::class)
@SdkSuppress(minSdkVersion=35,maxSdkVersion=35)
class CzechSaveAsViewportDeviceTest {
    private val instrumentation=InstrumentationRegistry.getInstrumentation()
    private val context get()=instrumentation.targetContext
    private val device get()=UiDevice.getInstance(instrumentation)

    @Test fun czechSaveAsRetainsDraftAtDoubleTextAcrossRotation() {
        assertTrue("Font scale is changed only on a disposable emulator",
            Build.FINGERPRINT.contains("generic") || Build.MODEL.contains("sdk",ignoreCase=true) ||
                Build.MODEL.contains("Emulator"))
        val manager=context.getSystemService(LocaleManager::class.java)
        val previousLocales=manager.applicationLocales
        val oldJavaLocale=Locale.getDefault()
        val prefs=context.getSharedPreferences("app-language",0)
        val oldTag=prefs.getString("language-tag",null)
        val hadInitialization=prefs.contains("platform-initialized")
        val oldInitialization=prefs.getBoolean("platform-initialized",false)
        val oldScale=Settings.System.getFloat(context.contentResolver,Settings.System.FONT_SCALE,1f)
        val font=GalleryViewportDeviceTest()
        val cs=context.createConfigurationContext(Configuration().apply {setLocales(LocaleList.forLanguageTags("cs"))})
        val en=context.createConfigurationContext(Configuration().apply {setLocales(LocaleList.forLanguageTags("en-US"))})
        val requests=AtomicInteger()
        val monitor=object: Instrumentation.ActivityMonitor() {
            override fun onStartActivity(intent: Intent): Instrumentation.ActivityResult? {
                if (intent.action!=Intent.ACTION_CREATE_DOCUMENT) return null
                requests.incrementAndGet()
                return Instrumentation.ActivityResult(Activity.RESULT_CANCELED,null)
            }
        }
        instrumentation.addMonitor(monitor)
        try {
            main {
                prefs.edit().putString("language-tag","cs").putBoolean("platform-initialized",true).commit()
                manager.applicationLocales=LocaleList.forLanguageTags("cs")
            }
            // Changing font scale is a separate configuration change. Apply it
            // before opening Save As; the live dialog is then only rotated.
            font.transitionFontScale(2f)
            val launch=checkNotNull(context.packageManager.getLaunchIntentForPackage(context.packageName))
            ActivityScenario.launch<ClassicPaintActivity>(launch).use {scenario ->
                lateinit var editor: ClassicPaintActivity
                scenario.onActivity {editor=it;it.requestedOrientation=ActivityInfo.SCREEN_ORIENTATION_PORTRAIT}
                await("Czech editor portrait at double text") {
                    editor.startupReady && !editor.busy && editor.window.decorView.hasWindowFocus() &&
                        profile(editor,false)
                }
                val drawing=IntArray(120*80) {if (it%120 in 12..21 && it/120 in 30..44) Color.MAGENTA else Color.WHITE}
                main {
                    editor.document.newImage(120,80)
                    editor.document.bitmap.setPixels(drawing,0,120,0,0,120,80)
                    editor.document.edited()
                    editor.paintCanvas.fit()
                }
                val command=cs.getString(R.string.save20_title)
                assertNotEquals(en.getString(R.string.save20_title),command)
                tap("File") {editor.window.decorView.findViewWithTag<View>("menu_File")}
                tap("Czech Save As") {
                    buttons(editor.window.decorView).firstOrNull {
                        it.text.toString()==command && it.tag?.toString()?.startsWith("command_File_")==true
                    }
                }
                await("real filename and format controls") {
                    optionsRoot()?.findViewWithTag<EditText>("export_filename")?.isShown==true
                }
                val root=main {checkNotNull(optionsRoot())}
                val field=main {root.findViewWithTag<EditText>("export_filename")}
                val spinner=main {root.findViewWithTag<Spinner>("export_format")}
                main {
                    val position=(0 until spinner.count).single {spinner.getItemAtPosition(it).toString()==ImageFormat.JPEG.label}
                    spinner.setSelection(position)
                }
                await("JPEG quality becomes active") {
                    spinner.selectedItem?.toString()==ImageFormat.JPEG.label &&
                        root.findViewWithTag<View>("export_quality").isShown
                }
                val draft="czech-unsaved-rotation.jpg"
                main {
                    field.setText(draft)
                    editor.getSystemService(InputMethodManager::class.java).hideSoftInputFromWindow(field.windowToken,0)
                }
                for (landscape in listOf(false,true,false)) {
                    main {editor.requestedOrientation=if (landscape) ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
                        else ActivityInfo.SCREEN_ORIENTATION_PORTRAIT}
                    await("mounted Czech Save As orientation landscape=$landscape") {
                        profile(editor,landscape) && optionsRoot()===root && root.hasWindowFocus() && !root.isLayoutRequested
                    }
                    scenario.onActivity {assertSame("orientation retains the editor",editor,it)}
                    main {
                        assertSame("live filename field survives rotation",field,root.findViewWithTag<EditText>("export_filename"))
                        assertEquals(draft,field.text.toString())
                        assertEquals(ImageFormat.JPEG.label,spinner.selectedItem.toString())
                        assertTrue(root.findViewWithTag<View>("export_quality").isShown)
                        assertEquals(cs.getString(R.string.save20_file_name),field.contentDescription.toString())
                        assertEquals(cs.getString(R.string.save20_file_format),spinner.contentDescription.toString())
                        val location=root.findViewById<Button>(android.R.id.button1)
                        val cancel=root.findViewById<Button>(android.R.id.button2)
                        for ((button,key) in listOf(location to R.string.ui_choose_location,cancel to R.string.ui_cancel)) {
                            assertEquals(cs.getString(key),button.text.toString())
                            assertNotEquals(en.getString(key),button.text.toString())
                            val bounds=Rect()
                            val shown=button.getGlobalVisibleRect(bounds)
                            val geometry="${button.width}x${button.height}, visible=$bounds, shown=$shown, enabled=${button.isEnabled}"
                            assertTrue("enabled and visible Czech footer: ${button.text}, landscape=$landscape, $geometry",
                                button.isEnabled && hitBounds(button,full=true)!=null)
                        }
                        assertDrawing(editor,drawing)
                        android.util.Log.i("CzechSaveAsViewport","scale=${editor.resources.configuration.fontScale} landscape=$landscape draft=true format=${spinner.selectedItem}")
                    }
                }
                tap("Czech Cancel") {optionsRoot()?.findViewById<View>(android.R.id.button2)}
                await("Cancel returns to the dirty Czech canvas") {
                    optionsRoot()==null && editor.window.decorView.hasWindowFocus() && !editor.busy
                }
                main {assertDrawing(editor,drawing);assertNull(editor.lastIoError);editor.document.markSaved()}
                assertEquals("Rotation and Cancel must not request a destination",0,requests.get())
            }
        } finally {
            instrumentation.removeMonitor(monitor)
            try {
                main {manager.applicationLocales=previousLocales}
                instrumentation.waitForIdleSync()
                font.transitionFontScale(oldScale)
            } finally {
                main {
                    prefs.edit().apply {
                        if (oldTag==null) remove("language-tag") else putString("language-tag",oldTag)
                        if (hadInitialization) putBoolean("platform-initialized",oldInitialization)
                        else remove("platform-initialized")
                    }.commit()
                    Locale.setDefault(oldJavaLocale)
                }
            }
        }
    }

    private fun assertDrawing(editor: ClassicPaintActivity,drawing: IntArray) {
        val bitmap=editor.document.bitmap
        assertEquals(120,bitmap.width);assertEquals(80,bitmap.height)
        val actual=IntArray(drawing.size)
        bitmap.getPixels(actual,0,120,0,0,120,80)
        assertArrayEquals(drawing,actual)
        assertTrue("the unsaved drawing is still dirty",editor.document.dirty)
    }

    private fun profile(editor: ClassicPaintActivity,landscape: Boolean): Boolean {
        val config=editor.resources.configuration
        val root=editor.window.decorView
        return config.locales[0].toLanguageTag()=="cs" && config.fontScale==2f &&
            config.orientation==(if (landscape) Configuration.ORIENTATION_LANDSCAPE else Configuration.ORIENTATION_PORTRAIT) &&
            root.width>0 && root.height>0 && (root.width>root.height)==landscape
    }

    private fun optionsRoot()=WindowInspector.getGlobalWindowViews().lastOrNull {
        it.isShown && it.findViewWithTag<View>("export_filename")!=null
    }
    private fun buttons(view: View): Sequence<Button> = sequence {
        if (view is Button) yield(view)
        if (view is ViewGroup) for(i in 0 until view.childCount) yieldAll(buttons(view.getChildAt(i)))
    }
    private fun hitBounds(view: View,full: Boolean=false): Rect? {
        val visible=Rect()
        if (!view.isShown || !view.getGlobalVisibleRect(visible) || visible.width()<1 || visible.height()<1) return null
        if (full && (visible.width()!=view.width || visible.height()!=view.height)) return null
        val root=IntArray(2)
        view.rootView.getLocationOnScreen(root)
        visible.offset(root[0],root[1])
        return visible
    }
    private fun tap(label: String,find: ()->View?) {
        await(label) {find()?.let {hitBounds(it)}!=null}
        val bounds=main {checkNotNull(find()?.let {hitBounds(it)})}
        assertTrue("native tap: $label",device.click(bounds.centerX(),bounds.centerY()))
        instrumentation.waitForIdleSync()
    }
    private fun await(label: String,check: ()->Boolean) {
        val until=SystemClock.uptimeMillis()+8000
        do {
            if (main(check)) return
            Thread.sleep(40)
        } while (SystemClock.uptimeMillis()<until)
        fail("Timed out waiting for $label")
    }
    private fun <T> main(block: ()->T): T {
        val result=AtomicReference<Result<T>>()
        instrumentation.runOnMainSync {result.set(runCatching(block))}
        return checkNotNull(result.get()).getOrThrow()
    }
}
