/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local
import android.app.*
import android.graphics.*
import android.os.Looper
import android.view.*
import android.widget.*
import org.catrobat.paintroid.classic.*
import org.junit.Test
import org.junit.Assert.*
import org.junit.runner.RunWith
import org.robolectric.*
import org.robolectric.annotation.*
import org.robolectric.shadows.ShadowToast
import org.robolectric.util.ReflectionHelpers
import java.io.File
import java.util.*
import kotlin.math.*

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],manifest=Config.NONE,qualifiers="w420dp-h680dp-port-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class VerticalNoticeHostProbe {
    private val directory=File(System.getProperty("probe.dir"))
    private fun settle()=Shadows.shadowOf(Looper.getMainLooper()).idleFor(java.time.Duration.ofMillis(64))
    private fun assets(activity: Activity) {
        ReflectionHelpers.callInstanceMethod<Int>(activity.assets,"addAssetPath",ReflectionHelpers.ClassParameter.from(String::class.java,File(directory,"font-assets.apk").path))
    }

    private fun injectIme(decor: View,height: Int) {
        fun call(target: Any,name: String,vararg parameters: ReflectionHelpers.ClassParameter<*>): Any? = ReflectionHelpers.callInstanceMethod<Any?>(target,name,*parameters)
        val root=call(decor,"getViewRootImpl")!!
        val controller=call(root,"getInsetsController")!!
        val state=call(controller,"getState")!!
        val stateClass=Class.forName("android.view.InsetsState")
        val copy=stateClass.getConstructor(stateClass,Boolean::class.javaPrimitiveType).newInstance(state,true)
        val frame=ReflectionHelpers.getField<Rect>(controller,"mFrame")
        assertTrue(frame.width()>0 && frame.height()>height)
        val source=if(android.os.Build.VERSION.SDK_INT<31) call(copy,"getSource",ReflectionHelpers.ClassParameter.from(Int::class.javaPrimitiveType,13))!!
            else call(copy,"getOrCreateSource",ReflectionHelpers.ClassParameter.from(Int::class.javaPrimitiveType,ReflectionHelpers.getStaticField<Int>(Class.forName("android.view.InsetsSource"),"ID_IME")),ReflectionHelpers.ClassParameter.from(Int::class.javaPrimitiveType,WindowInsets.Type.ime()))!!
        call(source,"setFrame",ReflectionHelpers.ClassParameter.from(Rect::class.java,Rect(frame.left,frame.bottom-height,frame.right,frame.bottom)))
        call(source,"setVisible",ReflectionHelpers.ClassParameter.from(Boolean::class.javaPrimitiveType,height>0))
        @Suppress("UNCHECKED_CAST")
        call(controller,"onStateChanged",ReflectionHelpers.ClassParameter.from(stateClass as Class<Any>,copy))
        call(root,"dispatchApplyInsets",ReflectionHelpers.ClassParameter.from(View::class.java,decor))
        assertEquals(height>0,decor.rootWindowInsets.isVisible(WindowInsets.Type.ime()))
    }
    @Test fun allCurrentPickerRoutesRemainUnchangedOnAnAttachedWindow() {
        val controller=Robolectric.buildActivity(Activity::class.java).setup();val a=controller.get();assets(a)
        a.setContentView(FrameLayout(a));controller.visible().windowFocusChanged(true);settle()
        val previous=Locale.getDefault();val host=a.findViewById<FrameLayout>(android.R.id.content)
        val routes=mutableListOf<String>()
        try {
            assertTrue(host.isAttachedToWindow);assertTrue(host.width>0 && host.height>0)
            val tags=File(directory,"tags.txt").readLines();assertEquals(140,tags.size)
            for(tag in tags) {
                Locale.setDefault(Locale.forLanguageTag(tag));ShadowToast.reset()
                LocaleTypography.showMessage(a,tag,Toast.LENGTH_SHORT);settle()
                val label=host.findViewWithTag<TextView>("locale_notification_text")
                if(tag in setOf("vi-Hani","wuu-Hans")) {
                    assertNotNull(tag,label);assertEquals(tag,label.text.toString());assertNull(ShadowToast.getLatestToast())
                    assertSame(LocaleTypography.typeface(a),label.typeface)
                    Shadows.shadowOf(Looper.getMainLooper()).idleFor(java.time.Duration.ofMillis(2100))
                } else {assertNull(tag,label);assertEquals(tag,ShadowToast.getTextOfLatestToast())}
                routes.add("$tag\t${if(label==null) "system-toast" else "foreground-horizontal"}\t${VerticalText.uiDirection()}\t${LocaleTypography.asset() ?: "default"}")
            }
        } finally {controller.close();Locale.setDefault(previous);File(directory,"routes-api${android.os.Build.VERSION.SDK_INT}.tsv").writeText("tag\troute\tdirection\tconfiguredFace\n"+routes.joinToString("\n")+"\n")}
    }
    @Test fun attachedHostDiagnosticMeasuresTheProposedBodyWithoutChangingProductionRouting() {
        val legalName="😀‍😀‍😀‍😀‍😀‍😀.png"
        assertTrue(ExportNames.valid(legalName,org.catrobat.paintroid.classic.ImageFormat.PNG))
        assertEquals(legalName,ExportNames.withExtension(legalName,org.catrobat.paintroid.classic.ImageFormat.PNG))
        val previous=Locale.getDefault();val originalQualifiers=RuntimeEnvironment.getQualifiers();val originalScale=RuntimeEnvironment.getFontScale()
        val legacyInsetsMode=if(android.os.Build.VERSION.SDK_INT==30) ReflectionHelpers.getStaticField<Int>(Class.forName("android.view.ViewRootImpl"),"sNewInsetsMode") else null
        // Robolectric API30 defaults to legacy mode0, which advertises IME visibility but skips its geometry.
        // Enable the framework's complete inset calculation for test-supplied WM state; restore afterward.
        val out=StringBuilder("sdk\ttag\tkey\tsurface\tscale\tdensity\ttextSizePx\tpaintLocales\thostW\thostH\tbodyW\tbodyH\tsafeW\tsafeH\ttarget\tnominalW\tnominalH\tfits\toutsideBodyPixels\tdrawnInkPixels\tleftInk\ttopInk\trightInk\tbottomInk\n")
        try {
            for(scale in listOf(1f,2f)) for(density in listOf(160,400)) for(surface in System.getProperty("probe.surfaces","portrait,landscape,dialog,ime").split(',')) for(tag in listOf("mn-Mong","mnc-Mong","lzh-Hant","en-XV","qaa-Zsye-XV")) {
                RuntimeEnvironment.setQualifiers("b+${tag.replace('-','+')}-"+(if(surface=="landscape") "w780dp-h180dp-land-${density}dpi" else "w420dp-h680dp-port-${density}dpi"))
                RuntimeEnvironment.setFontScale(scale)
                val controller=Robolectric.buildActivity(Activity::class.java).setup();val a=controller.get();assets(a)
                a.setContentView(FrameLayout(a));controller.visible().windowFocusChanged(true);settle()
                val dialog=if(surface=="dialog") Dialog(a).apply {setContentView(TextView(a));show();window!!.setLayout((280*a.resources.displayMetrics.density).roundToInt(),(320*a.resources.displayMetrics.density).roundToInt());settle()} else null
                val host=(dialog?.window?.decorView ?: a.window.decorView).findViewById<FrameLayout>(android.R.id.content)
                val anchor=if(dialog!=null) host.getChildAt(0) else null
                if(surface=="ime") {
                    if(legacyInsetsMode!=null) ReflectionHelpers.setStaticField(Class.forName("android.view.ViewRootImpl"),"sNewInsetsMode",2)
                    injectIme(host.rootView,(320*a.resources.displayMetrics.density).roundToInt());settle()
                    assertEquals((320*a.resources.displayMetrics.density).roundToInt(),host.rootWindowInsets.getInsets(WindowInsets.Type.ime()).bottom)
                }
                try {
                    assertTrue(host.isAttachedToWindow);assertTrue(host.width>0 && host.height>0)
                        Locale.setDefault(Locale.forLanguageTag(tag))
                        val supplied=File(directory,"fixtures.tsv").readLines().map {it.split('\t')}.filter {it[0]==tag && it[1] in listOf("combined","short-file","mixed-file","long-file","joined-short-file","unsupported-zwj-file")}.map {it[1] to String(Base64.getDecoder().decode(it[2]),Charsets.UTF_8)}
                        val short=File(directory,"fixtures.tsv").readLines().map {it.split('\t')}.first {it[0]==tag && it[1]=="short-file"}
                        val additional="fallback-file" to String(Base64.getDecoder().decode(short[2]),Charsets.UTF_8).replace("𠲎🖌️绘画.png","ᠮ.png")
                        for((key,text) in supplied+additional) {
                            ShadowToast.reset();LocaleTypography.showMessage(a,text,Toast.LENGTH_SHORT,anchor)
                            assertNull(host.findViewWithTag<View>("locale_notification"));assertEquals(text,ShadowToast.getTextOfLatestToast())
                            // Direct helper access is diagnostic only. Production still routes all five tags to Toast.
                            assertTrue(LocaleNotification.show(a,text,Toast.LENGTH_LONG,LocaleTypography.typeface(a) ?: TextView(a).typeface,anchor));settle()
                            val notice=host.findViewWithTag<FrameLayout>("locale_notification")
                            val original=notice.findViewWithTag<TextView>("locale_notification_text")
                            assertEquals(text,original.text.toString());assertEquals(text,original.createAccessibilityNodeInfo().text.toString())
                            assertEquals(Locale.forLanguageTag(tag),a.resources.configuration.locales[0]);assertEquals(scale,a.resources.configuration.fontScale,0f)
                            assertEquals(density/160f,a.resources.displayMetrics.density,0f)
                            val margins=original.layoutParams as FrameLayout.LayoutParams
                            val safeW=notice.width-notice.paddingLeft-notice.paddingRight-margins.leftMargin-margins.rightMargin-original.paddingLeft-original.paddingRight
                            val safeH=notice.height-notice.paddingTop-notice.paddingBottom-margins.topMargin-margins.bottomMargin-original.paddingTop-original.paddingBottom
                            val direction=VerticalText.uiDirection();val renderPaint=android.text.TextPaint(original.paint).apply {color=Color.BLACK}
                            var target=min(240*original.resources.displayMetrics.density,safeH.toFloat())
                            var wrapped=VerticalText.wrapLabel(text,renderPaint,target,direction)
                            var bounds=VerticalText.bounds(wrapped,renderPaint,direction,GlyphOrientation.MIXED,1f)
                            if(ceil(bounds.width())>safeW) {target=safeH.toFloat();wrapped=VerticalText.wrapLabel(text,renderPaint,target,direction);bounds=VerticalText.bounds(wrapped,renderPaint,direction,GlyphOrientation.MIXED,1f)}
                            val fits=safeW>0 && safeH>0 && ceil(bounds.width())<=safeW && ceil(bounds.height())<=safeH
                            val bodyW=original.width;val bodyH=ceil(bounds.height()).toInt()+original.paddingTop+original.paddingBottom
                            val originX=if(direction==TextDirection.VERTICAL_RL) bodyW-original.paddingRight-bounds.width() else original.paddingLeft.toFloat()
                            val originY=original.paddingTop.toFloat();val guard=ceil(renderPaint.textSize*4).toInt()
                            val shiftX=guard-floor(min(0f,originX)).toInt()
                            val referenceW=ceil(max(bodyW.toFloat(),originX+bounds.width())).toInt()+shiftX+guard
                            val ink=Bitmap.createBitmap(referenceW,bodyH+guard*2,Bitmap.Config.ARGB_8888)
                            Canvas(ink).apply {translate(shiftX+originX,guard+originY);VerticalText.draw(this,wrapped,renderPaint,direction,GlyphOrientation.MIXED)}
                            val pixels=IntArray(ink.width*ink.height);ink.getPixels(pixels,0,ink.width,0,0,ink.width,ink.height)
                            var outside=0;var left=Int.MAX_VALUE;var top=Int.MAX_VALUE;var right=Int.MIN_VALUE;var bottom=Int.MIN_VALUE
                            for(i in pixels.indices) if(Color.alpha(pixels[i])!=0) {
                                val x=i%ink.width-shiftX;val y=i/ink.width-guard
                                left=min(left,x);top=min(top,y);right=max(right,x+1);bottom=max(bottom,y+1)
                                if(x<0 || y<0 || x>=bodyW || y>=bodyH) outside++
                            }
                            assertTrue("Unbounded guard: $tag/$key/$surface/$scale/$density fits=$fits ink=$left,$top,$right,$bottom ref=${ink.width}x${ink.height} shift=$shiftX,$guard",left>-shiftX && top>-guard && right<ink.width-shiftX && bottom<bodyH+guard)
                            var drawn=-1
                            if(fits) {
                                val diagnostic=object: TextView(original.context) {
                                    override fun onDraw(canvas: Canvas) {
                                        canvas.save();canvas.translate(originX,originY)
                                        VerticalText.draw(canvas,wrapped,renderPaint,direction,GlyphOrientation.MIXED);canvas.restore()
                                    }
                                }.apply {this.text=text;this.tag="diagnostic_vertical_body";importantForAccessibility=View.IMPORTANT_FOR_ACCESSIBILITY_NO}
                                notice.removeView(original);notice.addView(diagnostic,FrameLayout.LayoutParams(margins).apply {height=bodyH});settle()
                                assertEquals(bodyW,diagnostic.width);assertEquals(bodyH,diagnostic.height);assertTrue(notice.clipChildren)
                                val clipped=Bitmap.createBitmap(notice.width,notice.height,Bitmap.Config.ARGB_8888);notice.draw(Canvas(clipped))
                                val actual=IntArray(clipped.width*clipped.height);clipped.getPixels(actual,0,clipped.width,0,0,clipped.width,clipped.height)
                                drawn=actual.count {Color.alpha(it)!=0}
                                val expected=IntArray(actual.size)
                                for(y in 0 until bodyH) for(x in 0 until bodyW) {
                                    val nx=diagnostic.left+x;val ny=diagnostic.top+y
                                    if(nx in 0 until notice.width && ny in 0 until notice.height) expected[ny*notice.width+nx]=pixels[(y+guard)*ink.width+x+shiftX]
                                }
                                assertArrayEquals("Exact native pixels must equal independently clipped renderer reference",expected,actual)
                                assertEquals("Actual parent clipping must match measured escaped ink",pixels.count {Color.alpha(it)!=0}-outside,drawn)
                                if(outside>0 || (key=="mixed-file" && surface=="portrait" && scale==2f && density==160)) {
                                    val preview=Bitmap.createBitmap(clipped.width,clipped.height,Bitmap.Config.ARGB_8888)
                                    Canvas(preview).apply {drawColor(Color.WHITE);drawBitmap(clipped,0f,0f,null)}
                                    File(directory,"previews/clipped-api${android.os.Build.VERSION.SDK_INT}-$tag-$key-$surface-$scale-$density.png").outputStream().use {preview.compress(Bitmap.CompressFormat.PNG,100,it)};preview.recycle()
                                }
                                clipped.recycle()
                            }
                            out.append("${android.os.Build.VERSION.SDK_INT}\t$tag\t$key\t$surface\t$scale\t${density/160f}\t${renderPaint.textSize}\t${renderPaint.textLocales.toLanguageTags()}\t${host.width}\t${host.height}\t$bodyW\t$bodyH\t$safeW\t$safeH\t$target\t${bounds.width()}\t${bounds.height()}\t$fits\t$outside\t$drawn\t$left\t$top\t$right\t$bottom\n")
                            if(fits && (outside>0 || (key=="mixed-file" && surface=="portrait" && scale==2f && density==160))) {
                                val preview=Bitmap.createBitmap(bodyW+guard*2,bodyH+guard*2,Bitmap.Config.ARGB_8888)
                                Canvas(preview).apply {drawColor(Color.WHITE);drawBitmap(ink,0f,0f,null);drawRect(guard.toFloat(),guard.toFloat(),(guard+bodyW).toFloat(),(guard+bodyH).toFloat(),Paint().apply {color=Color.RED;style=Paint.Style.STROKE;strokeWidth=2f})}
                                File(directory,"previews/host-api${android.os.Build.VERSION.SDK_INT}-$tag-$key-$surface-$scale-$density.png").outputStream().use {preview.compress(Bitmap.CompressFormat.PNG,100,it)};preview.recycle()
                            }
                            ink.recycle();notice.removeAllViews();host.removeView(notice);settle()
                        }
                } finally {dialog?.dismiss();controller.close();settle();if(legacyInsetsMode!=null) ReflectionHelpers.setStaticField(Class.forName("android.view.ViewRootImpl"),"sNewInsetsMode",legacyInsetsMode)}
            }
        } finally {
            if(legacyInsetsMode!=null) ReflectionHelpers.setStaticField(Class.forName("android.view.ViewRootImpl"),"sNewInsetsMode",legacyInsetsMode)
            Locale.setDefault(previous);RuntimeEnvironment.setQualifiers(originalQualifiers);RuntimeEnvironment.setFontScale(originalScale)
            File(directory,"host-api${android.os.Build.VERSION.SDK_INT}.tsv").writeText(out.toString())
        }
    }
}
