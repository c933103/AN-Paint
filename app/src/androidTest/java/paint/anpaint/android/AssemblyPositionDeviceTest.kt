/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.AlertDialog
import android.app.LocaleManager
import android.content.Intent
import android.content.pm.ActivityInfo
import android.content.res.Configuration
import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Point
import android.graphics.Rect
import android.os.Build
import android.os.LocaleList
import android.os.Looper
import android.os.SystemClock
import android.text.Spanned
import android.text.style.ReplacementSpan
import android.view.KeyEvent
import android.view.View
import android.view.ViewGroup
import android.view.WindowInsets
import android.widget.EditText
import android.widget.HorizontalScrollView
import android.widget.ScrollView
import android.widget.TextView
import androidx.test.core.app.ActivityScenario
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.SdkSuppress
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.uiautomator.UiDevice
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AssemblyActivity
import org.catrobat.paintroid.classic.AssemblyImage
import org.catrobat.paintroid.classic.AssemblyPositionDialog
import org.catrobat.paintroid.classic.FlowTextView
import org.catrobat.paintroid.classic.ImageAssembly
import org.catrobat.paintroid.classic.ImageDimensions
import org.catrobat.paintroid.classic.ImagePosition
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.util.Locale
import java.util.concurrent.atomic.AtomicReference

/** Installed native layout/input for the changed exact-position dialog only.
 * Locale, image metadata and opening the public production dialog are fixtures.
 * Every field edit, Apply, Cancel, Back and reveal gesture uses injected input.
 * Layout/column bounds and accessibility are checked, not pixel-level glyph ink,
 * linguistic quality, the language picker, assembly import or file export.
 */
@RunWith(AndroidJUnit4::class)
@SdkSuppress(minSdkVersion=30)
class AssemblyPositionDeviceTest {
    private val instrumentation=InstrumentationRegistry.getInstrumentation()
    private val context get()=instrumentation.targetContext
    private val device get()=UiDevice.getInstance(instrumentation)
    private var deadline=Long.MAX_VALUE

    @Test fun ainuKanaPositionTextAndNativeEditing()=checkLocale("ain-Kana")
    @Test fun ainuLatinPositionTextAndNativeEditing()=checkLocale("ain-Latn")
    @Test fun manchuPositionColumnsAndNativeEditing()=checkLocale("mnc-Mong")
    @Test fun tibetanPositionTextAndNativeEditing()=checkLocale("bo")
    @Test fun dzongkhaPositionTextAndNativeEditing()=checkLocale("dz")
    @Test fun jejuPositionTextAndNativeEditing()=checkLocale("jje")
    @Test fun nomPositionTextAndNativeEditing()=checkLocale("vi-Hani")

    private fun checkLocale(tag: String) {
        val preferences=context.getSharedPreferences("app-language",0)
        val oldTag=preferences.getString("language-tag",null)
        val hadTag=preferences.contains("language-tag")
        val oldInitialized=preferences.getBoolean("platform-initialized",false)
        val hadInitialized=preferences.contains("platform-initialized")
        val oldLocale=Locale.getDefault()
        val oldPlatform=if(Build.VERSION.SDK_INT>=33)
            context.getSystemService(LocaleManager::class.java).applicationLocales else null
        val directory=File.createTempFile("position-device-","",context.cacheDir).apply {
            check(delete());check(mkdir())
        }
        var scenario: ActivityScenario<AssemblyActivity>?=null
        var activity: AssemblyActivity?=null
        var dialog: AlertDialog?=null
        var failure: Throwable?=null
        try {
            onMain {
                preferences.edit().putString("language-tag",tag).putBoolean("platform-initialized",true).commit()
                if(Build.VERSION.SDK_INT>=33)
                    context.getSystemService(LocaleManager::class.java).applicationLocales=LocaleList.forLanguageTags(tag)
            }
            instrumentation.waitForIdleSync()
            val launched=ActivityScenario.launch<AssemblyActivity>(Intent(context,AssemblyActivity::class.java)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
            scenario=launched
            launched.onActivity {activity=it;it.onConfigurationChanged(Configuration(it.resources.configuration))}
            val owner=checkNotNull(activity)
            await("fixture activity layout") {owner.window.decorView.width>0 && !owner.busy}
            val assembly=onMain {
                assertEquals(tag,owner.resources.configuration.locales[0].toLanguageTag())
                ImageAssembly(directory).apply {
                    fun imageFile(name: String,width: Int,height: Int): File {
                        val bitmap=Bitmap.createBitmap(width,height,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.RED)}
                        return File(directory,name).also {file ->
                            try {file.outputStream().use {check(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))}}
                            finally {bitmap.recycle()}
                        }
                    }
                    // Independent dialog fixture; no import or thumbnail worker.
                    add(listOf(AssemblyImage("selected",imageFile("fixture.png",12,20),"fixture.png",null,ImageDimensions(12,20)),
                        AssemblyImage("other",imageFile("other.png",8,9),"other.png",null,ImageDimensions(8,9))))
                    position("selected",24,0);position("other",0,0)
                }
            }
            val before=onMain {assembly.layout()}
            val beforeSaved=File(directory,"project.json").readBytes()
            deadline=SystemClock.uptimeMillis()+45000
            orient(owner,false)
            fun open(): AlertDialog {
                val current=onMain {AssemblyPositionDialog(owner,assembly,"selected").show()}
                dialog=current
                await("localized position dialog") {
                    current.isShowing && current.window!!.decorView.hasWindowFocus() &&
                        current.window!!.decorView.findViewWithTag<EditText>("assembly_position_x")?.layout!=null &&
                        (tag!="mnc-Mong" || current.window!!.decorView.findViewWithTag<View>("vertical_dialog")!=null)
                }
                return current
            }
            var current=open()
            hideIme(onMain {current.window!!.decorView})
            checkTextAndColumns(owner,current,tag)
            var root=onMain {current.window!!.decorView}
            val x=onMain {root.findViewWithTag<EditText>("assembly_position_x")}
            val y=onMain {root.findViewWithTag<EditText>("assembly_position_y")}
            onMain {assertEquals("24",x.text.toString());assertEquals("0",y.text.toString())}
            replace(x,"")
            hideIme(root)
            tap(onMain {current.getButton(AlertDialog.BUTTON_POSITIVE)})
            await("localized validation remains open") {
                current.isShowing && root.findViewWithTag<TextView>("assembly_position_error").text.toString()==
                    owner.getString(R.string.ui_assembly_position_nonnegative)
            }
            revealText(onMain {root.findViewWithTag("assembly_position_error")})
            onMain {assertEquals(before,assembly.layout())}
            assertArrayEquals("Invalid native input cannot save",beforeSaved,File(directory,"project.json").readBytes())
            replace(x,"5")
            replace(y,"4")
            hideIme(root)
            tap(onMain {current.getButton(AlertDialog.BUTTON_POSITIVE)})
            await("native Apply commits and dismisses") {!current.isShowing}
            val expected=before.toMutableMap().apply {put("selected",Rect(5,4,17,24))}
            onMain {
                assertEquals(expected,assembly.layout())
                assertEquals(ImagePosition(5,4),assembly.image("selected").position)
                assertEquals("Native Apply survives project reload",expected,ImageAssembly(directory).layout())
            }
            val accepted=File(directory,"project.json").readBytes()
            orient(owner,true)
            current=open()
            hideIme(onMain {current.window!!.decorView})
            checkTextAndColumns(owner,current,tag)
            root=onMain {current.window!!.decorView}
            onMain {
                assertEquals("5",root.findViewWithTag<EditText>("assembly_position_x").text.toString())
                assertEquals("4",root.findViewWithTag<EditText>("assembly_position_y").text.toString())
            }
            replace(onMain {root.findViewWithTag("assembly_position_y")},"9")
            hideIme(root)
            tap(onMain {current.getButton(AlertDialog.BUTTON_NEGATIVE)})
            await("native Cancel dismisses") {!current.isShowing}
            onMain {assertEquals(expected,assembly.layout())}
            assertArrayEquals("Cancelled edit cannot change saved project",accepted,File(directory,"project.json").readBytes())
            current=open()
            hideIme(onMain {current.window!!.decorView})
            assertTrue("Inject one native dialog Back",device.pressKeyCode(KeyEvent.KEYCODE_BACK))
            await("Back dismisses the reopened dialog") {!current.isShowing && owner.window.decorView.hasWindowFocus()}
            assertArrayEquals("Back cannot change saved project",accepted,File(directory,"project.json").readBytes())
            checkDeadline()
        } catch(error: Throwable) {failure=error}
        finally {
            deadline=Long.MAX_VALUE
            fun cleanup(action: ()->Unit) {try {action()} catch(error: Throwable) {
                if(failure==null) failure=error else failure!!.addSuppressed(error)
            }}
            cleanup {onMain {dialog?.dismiss();activity?.takeUnless {it.isDestroyed}?.finish()}}
            cleanup {await("fixture activity destroyed") {activity?.isDestroyed!=false}}
            cleanup {scenario?.close()}
            cleanup {onMain {
                if(Build.VERSION.SDK_INT>=33)
                    context.getSystemService(LocaleManager::class.java).applicationLocales=checkNotNull(oldPlatform)
            };instrumentation.waitForIdleSync()}
            cleanup {onMain {
                preferences.edit().apply {
                    if(hadTag) putString("language-tag",oldTag) else remove("language-tag")
                    if(hadInitialized) putBoolean("platform-initialized",oldInitialized) else remove("platform-initialized")
                }.commit()
                Locale.setDefault(oldLocale)
            }}
            cleanup {check(directory.deleteRecursively())}
        }
        failure?.let {throw it}
    }

    private fun checkTextAndColumns(owner: AssemblyActivity,dialog: AlertDialog,tag: String) {
        val root=onMain {dialog.window!!.decorView}
        onMain {android.util.Log.i("AssemblyPositionDeviceTest","locale=$tag orientation=${owner.resources.configuration.orientation} " +
            "window=${root.width}x${root.height} fontScale=${owner.resources.configuration.fontScale}")}
        if(tag=="mnc-Mong") onMain {
            val columns=root.findViewWithTag<HorizontalScrollView>("vertical_dialog_columns")
            assertNotNull("Manchu uses the production vertical shell",columns)
            assertEquals("Manchu starts at the left reading column",0,columns.scrollX)
            assertEquals(View.LAYOUT_DIRECTION_LTR,columns.getChildAt(0).layoutDirection)
        }
        for(key in listOf(R.string.ui_assembly_exact_position,R.string.ui_assembly_position_help,
                R.string.ui_assembly_target_x,R.string.ui_assembly_target_y)) {
            val expected=onMain {owner.getString(key)}
            val caption=onMain {descendants(root).filterIsInstance<TextView>()
                .single {it !is EditText && it.text.toString()==expected}}
            onMain {
                val info=caption.createAccessibilityNodeInfo()
                try {assertEquals("Complete accessible caption",expected,info.text?.toString())} finally {info.recycle()}
                if(tag=="mnc-Mong" && caption !is FlowTextView) {
                    val value=caption.text as? Spanned ?: throw AssertionError("Manchu caption lacks vertical span")
                    val span=value.getSpans(0,value.length,ReplacementSpan::class.java).single()
                    assertEquals(0,value.getSpanStart(span));assertEquals(expected.length,value.getSpanEnd(span))
                }
            }
            revealText(caption)
        }
        for((field,key) in listOf("assembly_position_x" to R.string.ui_assembly_target_x,
                "assembly_position_y" to R.string.ui_assembly_target_y)) {
            val input=onMain {root.findViewWithTag<EditText>(field)}
            onMain {assertEquals(owner.getString(key),input.contentDescription.toString())}
            reveal(input) {rawBounds(input)}
        }
        revealText(onMain {dialog.getButton(AlertDialog.BUTTON_NEGATIVE)})
        revealText(onMain {dialog.getButton(AlertDialog.BUTTON_POSITIVE)})
    }

    private fun replace(field: EditText,value: String) {
        // A previous edit can leave the keyboard over the next field. Native
        // view clipping does not subtract IME occlusion; dismiss it before
        // measuring/revealing the next touch target, just as before Apply.
        hideIme(onMain {field.rootView})
        tap(field)
        try {
            await("native field focus: ${field.tag}") {field.hasFocus() && field.hasWindowFocus()}
        } catch(error: AssertionError) {
            throw AssertionError(onMain {"${error.message}; raw=${rawBounds(field)} visible=${visibleBounds(field)} " +
                "focused=${field.rootView.findFocus()?.tag} windowFocus=${field.hasWindowFocus()} " +
                "ime=${field.rootWindowInsets?.isVisible(WindowInsets.Type.ime())}"},error)
        }
        assertTrue(device.pressKeyCode(KeyEvent.KEYCODE_A,KeyEvent.META_CTRL_ON))
        assertTrue(device.pressKeyCode(KeyEvent.KEYCODE_DEL))
        if(value.isNotEmpty()) instrumentation.sendStringSync(value)
        await("native field input: ${field.tag}") {field.text.toString()==value}
    }
    private fun hideIme(root: View) {
        await("window insets available") {root.rootWindowInsets!=null}
        if(onMain {root.rootWindowInsets!!.isVisible(WindowInsets.Type.ime())}) {
            assertTrue("Native Back closes the visible IME",device.pressKeyCode(KeyEvent.KEYCODE_BACK))
            await("IME closed without dismissing dialog") {root.isAttachedToWindow && root.hasWindowFocus() &&
                root.rootWindowInsets?.isVisible(WindowInsets.Type.ime())==false}
        }
    }
    private fun orient(owner: AssemblyActivity,landscape: Boolean) {
        onMain {owner.requestedOrientation=if(landscape) ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE else ActivityInfo.SCREEN_ORIENTATION_PORTRAIT}
        await("real orientation") {
            val root=owner.window.decorView
            owner.resources.configuration.orientation==(if(landscape) Configuration.ORIENTATION_LANDSCAPE else Configuration.ORIENTATION_PORTRAIT) &&
                root.width>0 && root.height>0 && (root.width>root.height)==landscape && !root.isLayoutRequested
        }
    }

    private fun revealText(view: TextView) {
        settle(view)
        val regions=onMain {
            assertTrue("Shown finite text view",view.isShown && view.width>0 && view.height>0)
            if(view is FlowTextView) {
                // FlowTextView bypasses native Layout. Independently retain the
                // complete source string and check the production renderer's
                // full measured extent, then visit every part of that extent.
                val renderer=Class.forName("org.catrobat.paintroid.classic.VerticalText")
                val instance=renderer.getField("INSTANCE").get(null)
                val height=view.javaClass.getDeclaredField("columnHeight").apply {isAccessible=true}.getInt(view)
                val direction=renderer.getMethod("uiDirection",android.content.Context::class.java).invoke(instance,view.context)
                val wrapped=renderer.methods.single {it.name=="wrapLabel" && it.parameterTypes.size==4}
                    .invoke(instance,view.text.toString(),view.paint,height.toFloat().coerceAtLeast(view.paint.fontSpacing),direction) as String
                assertEquals("Every vertical word survives wrapping",view.text.toString().split(' '),wrapped.replace('\n',' ').split(' '))
                val orientation=Class.forName("org.catrobat.paintroid.classic.GlyphOrientation").enumConstants.single {it.toString()=="MIXED"}
                val box=renderer.methods.single {it.name=="bounds"}.invoke(instance,wrapped,view.paint,direction,orientation,1f) as android.graphics.RectF
                assertTrue("Complete vertical width fits",box.width()<=view.width-view.paddingLeft-view.paddingRight)
                assertTrue("Complete vertical height fits",box.height()<=view.height-view.paddingTop-view.paddingBottom)
                listOf(Rect(view.paddingLeft,view.paddingTop,view.width-view.paddingRight,view.height-view.paddingBottom))
            } else {
                val layout=checkNotNull(view.layout)
                val transformed=view.transformationMethod?.getTransformation(view.text,view)?.toString() ?: view.text.toString()
                assertTrue(layout.lineCount>0)
                assertEquals("Full UTF-16 caption laid out",transformed.length,layout.getLineEnd(layout.lineCount-1))
                assertTrue("Text fits intrinsic height",layout.height<=view.height-view.totalPaddingTop-view.totalPaddingBottom)
                (0 until layout.lineCount).map {line ->
                    assertEquals("No caption ellipsis",0,layout.getEllipsisCount(line))
                    assertTrue("Text fits intrinsic width",layout.getLineLeft(line)>=0 && layout.getLineRight(line)<=layout.width)
                    Rect(view.totalPaddingLeft,view.totalPaddingTop+layout.getLineTop(line),
                        view.width-view.totalPaddingRight,view.totalPaddingTop+layout.getLineBottom(line))
                }
            }
        }
        // A vertical caption can span many horizontal columns. Requiring one
        // giant rectangle to fit simultaneously would mistake scrolling for loss.
        val tile=onMain {(64*view.resources.displayMetrics.density).toInt().coerceAtLeast(1)}
        for(region in regions) {
            var top=region.top
            while(top<region.bottom) {
                var left=region.left
                while(left<region.right) {
                    val piece=Rect(left,top,minOf(left+tile,region.right),minOf(top+tile,region.bottom))
                    reveal(view) {rawBounds(view).let {raw ->Rect(piece).apply {offset(raw.left,raw.top)}}}
                    left+=tile
                }
                top+=tile
            }
        }
    }
    private fun tap(view: TextView) {
        revealText(view)
        reveal(view) {rawBounds(view).let {raw ->val half=(12*view.resources.displayMetrics.density).toInt()
            Rect(raw.centerX()-half,raw.centerY()-half,raw.centerX()+half,raw.centerY()+half)}}
        val bounds=onMain {assertTrue(view.isEnabled);visibleBounds(view)}
        assertTrue("Native dialog tap",device.click(bounds.centerX(),bounds.centerY()))
        instrumentation.waitForIdleSync()
    }
    private data class Gesture(val bounds: Rect,val horizontal: Boolean,val direction: Int,val hidden: Int)
    private fun reveal(view: View,target: ()->Rect) {
        repeat(24) {
            checkDeadline()
            if(onMain {visibleBounds(view).contains(target())}) return
            val gesture=onMain {
                val wanted=target();var parent=view.parent as? View;var found: Gesture?=null
                while(parent!=null && found==null) {
                    val candidate=parent;val bounds=visibleBounds(candidate)
                    if(!bounds.isEmpty) {
                        val horizontal=candidate is HorizontalScrollView
                        if(horizontal || candidate is ScrollView) {
                            val low=if(horizontal) wanted.left-bounds.left else wanted.top-bounds.top
                            val high=if(horizontal) wanted.right-bounds.right else wanted.bottom-bounds.bottom
                            val direction=if(low<0) -1 else if(high>0) 1 else 0
                            if(direction!=0 && (if(horizontal) candidate.canScrollHorizontally(direction) else candidate.canScrollVertically(direction)))
                                found=Gesture(bounds,horizontal,direction,if(direction<0) -low else high)
                        }
                    }
                    parent=candidate.parent as? View
                }
                found ?: throw AssertionError("No native scroll route: wanted=$wanted visible=${visibleBounds(view)}")
            }
            val bounds=gesture.bounds
            val low=if(gesture.horizontal) bounds.left+bounds.width()/5 else bounds.top+bounds.height()/5
            val high=if(gesture.horizontal) bounds.right-bounds.width()/5 else bounds.bottom-bounds.height()/5
            val distance=(gesture.hidden+android.view.ViewConfiguration.get(context).scaledTouchSlop+2).coerceIn(1,high-low)
            val start=if(gesture.direction>0) high else low
            val end=start-gesture.direction*distance
            val first=if(gesture.horizontal) Point(start,bounds.centerY()) else Point(bounds.centerX(),start)
            val last=if(gesture.horizontal) Point(end,bounds.centerY()) else Point(bounds.centerX(),end)
            assertTrue("Native caption reveal",device.swipe(arrayOf(first,last,last,last),16))
            settle(view)
        }
        throw AssertionError("Native caption scrolling exceeded gesture bound")
    }
    private fun settle(view: View) {
        var previous="";var changed=SystemClock.uptimeMillis()
        await("layout settled") {
            val state="${rawBounds(view)}:${visibleBounds(view)}"
            if(state!=previous || view.isLayoutRequested) {previous=state;changed=SystemClock.uptimeMillis();false}
            else SystemClock.uptimeMillis()-changed>=100
        }
    }
    private fun rawBounds(view: View): Rect {
        val location=IntArray(2);view.getLocationOnScreen(location)
        return Rect(location[0],location[1],location[0]+view.width,location[1]+view.height)
    }
    private fun visibleBounds(view: View): Rect {
        val bounds=Rect();if(!view.getGlobalVisibleRect(bounds)) return Rect()
        val location=IntArray(2);view.rootView.getLocationOnScreen(location);bounds.offset(location[0],location[1]);return bounds
    }
    private fun descendants(view: View): List<View> = listOf(view)+if(view is ViewGroup)
        (0 until view.childCount).flatMap {descendants(view.getChildAt(it))} else emptyList()
    private fun checkDeadline() {assertTrue("Position dialog exceeded 45-second interaction budget",SystemClock.uptimeMillis()<deadline)}
    private fun await(label: String,condition: ()->Boolean) {
        val until=minOf(deadline,SystemClock.uptimeMillis()+8000)
        while(SystemClock.uptimeMillis()<until) {if(onMain(condition)) return;SystemClock.sleep(25)}
        throw AssertionError("Timed out: $label")
    }
    private fun <T> onMain(action: ()->T): T {
        if(Looper.myLooper()==Looper.getMainLooper()) return action()
        val result=AtomicReference<T>();val failure=AtomicReference<Throwable?>()
        instrumentation.runOnMainSync {try {result.set(action())} catch(error: Throwable) {failure.set(error)}}
        failure.get()?.let {throw it};return result.get()
    }
}
