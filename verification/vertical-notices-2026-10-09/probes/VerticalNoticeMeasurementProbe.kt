/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.graphics.*
import android.view.View
import android.widget.*
import org.catrobat.paintroid.classic.*
import org.junit.Test
import org.junit.Assert.*
import org.junit.runner.RunWith
import org.robolectric.*
import org.robolectric.annotation.*
import org.robolectric.util.ReflectionHelpers
import java.io.File
import java.util.*
import kotlin.math.*

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],manifest=Config.NONE,qualifiers="w420dp-h680dp-port-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class VerticalNoticeMeasurementProbe {
    private val root=File(System.getProperty("probe.dir"))
    @Test fun measureRealMessagesAtNormalSizeAgainstInsetAwareHost() {
        val controller=Robolectric.buildActivity(Activity::class.java).setup()
        val activity=controller.get(); val previous=Locale.getDefault()
        ReflectionHelpers.callInstanceMethod<Int>(activity.assets,"addAssetPath",ReflectionHelpers.ClassParameter.from(String::class.java,File(root,"font-assets.apk").path))
        activity.setContentView(FrameLayout(activity));controller.visible().windowFocusChanged(true)
        Shadows.shadowOf(android.os.Looper.getMainLooper()).idleFor(java.time.Duration.ofMillis(32))
        val host=activity.findViewById<FrameLayout>(android.R.id.content)
        assertTrue(host.isAttachedToWindow);assertTrue(host.width>0);assertTrue(host.height>0)
        data class Size(val name:String,val width:Int,val height:Int,val x:Int=0,val y:Int=0,val iw:Int=0,val it:Int=24,val ir:Int=0,val ib:Int=24,val ww:Int=width,val wh:Int=height)
        val sizes=listOf(Size("portrait",420,680),Size("landscape",780,180,it=0,ib=24),Size("dialog",280,320,it=0,ib=0),Size("ime",420,680,ib=360),Size("cutout",420,680,iw=40,it=24,ib=24),Size("already-fitted",420,272,y=24,it=24,ib=384,ww=420,wh=680))
        val out=StringBuilder("sdk\ttag\tkey\tviewport\tscale\tdensity\tsafeW\tsafeH\ttextSizePx\tpaintLocales\ttarget\twidth\theight\tfits\tinkLeft\tinkTop\tinkRight\tinkBottom\tinkContained\n")
        try {
            for(row in File(root,"fixtures.tsv").readLines()) {
                val fields=row.split('\t');val tag=fields[0];val key=fields[1];val text=String(Base64.getDecoder().decode(fields[2]),Charsets.UTF_8)
                Locale.setDefault(Locale.forLanguageTag(tag));val direction=VerticalText.uiDirection();assertNotEquals(TextDirection.HORIZONTAL,direction)
                for(size in sizes) for(scale in listOf(1f,1.3f,2f)) for(density in listOf(1f,2.5f)) {
                    fun px(dp:Int)=round(dp*density).toInt()
                    val padding=LocaleNotification.insetPadding(Insets.of(px(size.iw),px(size.it),px(size.ir),px(size.ib)),px(size.x),px(size.y),px(size.width),px(size.height),px(size.ww),px(size.wh))
                    val safeW=px(size.width)-padding.left-padding.right-px(64)
                    val safeH=px(size.height)-padding.top-padding.bottom-px(56)
                    val configured=activity.createConfigurationContext(android.content.res.Configuration(activity.resources.configuration).apply {fontScale=scale;densityDpi=round(160*density).toInt();setLocale(Locale.forLanguageTag(tag))})
                    val label=TextView(configured).apply {textSize=14f;typeface=LocaleTypography.typeface(activity) ?: typeface}
                    assertEquals(scale,configured.resources.configuration.fontScale,0f)
                    assertEquals(density,configured.resources.displayMetrics.density,0f)
                    val paint=android.text.TextPaint(label.paint).apply {color=Color.BLACK}
                    val targets=listOf(min(240f*density,safeH.toFloat()),safeH.toFloat()).distinct()
                    for(target in targets) {
                        val wrapped=VerticalText.wrapLabel(text,paint,target,direction)
                        val bounds=VerticalText.bounds(wrapped,paint,direction,GlyphOrientation.MIXED,1f)
                        val fits=ceil(bounds.width())<=safeW && ceil(bounds.height())<=safeH
                        // Render uncropped with a guard area; record actual ink, not only nominal advances.
                        val guard=ceil(4*paint.textSize).toInt()
                        val bitmap=Bitmap.createBitmap(ceil(bounds.width()).toInt()+guard*2,ceil(bounds.height()).toInt()+guard*2,Bitmap.Config.ARGB_8888)
                        val canvas=Canvas(bitmap);canvas.translate(guard.toFloat(),guard.toFloat())
                        VerticalText.draw(canvas,wrapped,paint,direction,GlyphOrientation.MIXED)
                        var l=bitmap.width;var t=bitmap.height;var r=0;var b=0
                        val pixels=IntArray(bitmap.width*bitmap.height);bitmap.getPixels(pixels,0,bitmap.width,0,0,bitmap.width,bitmap.height)
                        for(i in pixels.indices) if(Color.alpha(pixels[i])!=0) {val x=i%bitmap.width;val y=i/bitmap.width;l=min(l,x);t=min(t,y);r=max(r,x+1);b=max(b,y+1)}
                        assertTrue("Reference must not crop ink: $tag/$key/${size.name}/$scale/$density",l>0 && t>0 && r<bitmap.width && b<bitmap.height)
                        val ink=Rect(l-guard,t-guard,r-guard,b-guard)
                        val contained=ink.left>=0 && ink.top>=0 && ink.right<=ceil(bounds.width()) && ink.bottom<=ceil(bounds.height())
                        out.append("${android.os.Build.VERSION.SDK_INT}\t$tag\t$key\t${size.name}\t$scale\t$density\t$safeW\t$safeH\t${paint.textSize}\t${paint.textLocales.toLanguageTags()}\t$target\t${bounds.width()}\t${bounds.height()}\t$fits\t${ink.left}\t${ink.top}\t${ink.right}\t${ink.bottom}\t$contained\n")
                        if(size.name=="portrait" && scale==1f && density==1f && target==240f && key in listOf("combined","short-file","ui_undo")) {
                            val preview=Bitmap.createBitmap(bitmap.width,bitmap.height,Bitmap.Config.ARGB_8888)
                            Canvas(preview).apply {drawColor(Color.WHITE);drawBitmap(bitmap,0f,0f,null)}
                            File(root,"previews/${android.os.Build.VERSION.SDK_INT}-$tag-$key.png").outputStream().use {preview.compress(Bitmap.CompressFormat.PNG,100,it)}
                            preview.recycle()
                        }
                        bitmap.recycle()
                    }
                }
            }
        } finally {controller.close();Locale.setDefault(previous);File(root,"measurements-api${android.os.Build.VERSION.SDK_INT}.tsv").writeText(out.toString())}
    }
}
