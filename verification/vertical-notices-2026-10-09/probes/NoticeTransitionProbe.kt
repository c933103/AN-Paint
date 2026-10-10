/* Diagnostic of unchanged host behavior; does not implement a vertical route or a fallback switch. */
package org.catrobat.paintroid.local
import android.app.*
import android.content.Context
import android.graphics.*
import android.os.Looper
import android.view.*
import android.view.accessibility.AccessibilityManager
import android.widget.*
import org.catrobat.paintroid.classic.*
import org.junit.Test
import org.junit.Assert.*
import org.junit.runner.RunWith
import org.robolectric.*
import org.robolectric.annotation.*
import org.robolectric.shadows.ShadowToast
import org.robolectric.util.ReflectionHelpers as R
import java.io.File
import java.util.*
import kotlin.math.*
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],manifest=Config.NONE,qualifiers="w420dp-h680dp-port-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class NoticeTransitionProbe {
 @Test fun existingHorizontalNodeReflowsWithoutReplayThroughImeResizeAndAccessibilityTimeout() {
  val dir=File(System.getProperty("probe.dir"));val prev=Locale.getDefault();val quals=RuntimeEnvironment.getQualifiers()
  val mode=if(android.os.Build.VERSION.SDK_INT==30) R.getStaticField<Int>(Class.forName("android.view.ViewRootImpl"),"sNewInsetsMode") else null
  val out=StringBuilder("sdk\ttag\tphase\thostW\thostH\tnoticeBottomPadding\thorizontalMeasuredH\thorizontalCompleteH\thorizontalFits\tverticalNominalW\tverticalNominalH\tverticalNominalFits\n")
  fun settle()=Shadows.shadowOf(Looper.getMainLooper()).idleFor(java.time.Duration.ofMillis(64))
  try {
   for(tag in listOf("mn-Mong","mnc-Mong","lzh-Hant","en-XV","qaa-Zsye-XV")) {
    RuntimeEnvironment.setQualifiers("b+${tag.replace('-','+')}-w420dp-h680dp-port-mdpi");Locale.setDefault(Locale.forLanguageTag(tag))
    val controller=Robolectric.buildActivity(Activity::class.java).setup();val a=controller.get()
    R.callInstanceMethod<Int>(a.assets,"addAssetPath",R.ClassParameter.from(String::class.java,File(dir,"font-assets.apk").path))
    var touches=0;a.setContentView(View(a).apply {setOnTouchListener {_,_->touches++;true}})
    controller.visible().windowFocusChanged(true);settle()
    val host=a.findViewById<FrameLayout>(android.R.id.content)
    if(mode!=null) R.setStaticField(Class.forName("android.view.ViewRootImpl"),"sNewInsetsMode",2)
    val accessibility=a.getSystemService(Context.ACCESSIBILITY_SERVICE) as AccessibilityManager
    val oldTimeout=R.getField<Int>(accessibility,"mNonInteractiveUiTimeout");R.setField(accessibility,"mNonInteractiveUiTimeout",8000)
    try {
     val row=File(dir,"fixtures.tsv").readLines().map {it.split('\t')}.first {it[0]==tag && it[1]=="combined"}
     val text=String(Base64.getDecoder().decode(row[2]),Charsets.UTF_8);ShadowToast.reset()
     assertTrue(LocaleNotification.show(a,text,Toast.LENGTH_SHORT,LocaleTypography.typeface(a) ?: TextView(a).typeface,null));settle()
     val notice=host.findViewWithTag<FrameLayout>("locale_notification");val label=host.findViewWithTag<TextView>("locale_notification_text")
     for(phase in listOf("initial","ime","restored","resized")) {
      if(phase=="ime") R.callInstanceMethod<Any?>(VerticalNoticeHostProbe(),"injectIme",R.ClassParameter.from(View::class.java,host.rootView),R.ClassParameter.from(Int::class.javaPrimitiveType,320))
      if(phase=="restored") R.callInstanceMethod<Any?>(VerticalNoticeHostProbe(),"injectIme",R.ClassParameter.from(View::class.java,host.rootView),R.ClassParameter.from(Int::class.javaPrimitiveType,0))
      if(phase=="resized") a.window.setLayout(420,180)
      settle()
      if(phase=="ime") assertEquals(320,host.rootWindowInsets.getInsets(WindowInsets.Type.ime()).bottom)
      if(phase=="restored") assertEquals(0,host.rootWindowInsets.getInsets(WindowInsets.Type.ime()).bottom)
      if(phase=="resized") assertEquals(180,host.rootView.height)
      assertSame(notice,host.findViewWithTag<View>("locale_notification"));assertSame(label,host.findViewWithTag<View>("locale_notification_text"))
      assertEquals(text,label.text.toString());assertEquals(text,label.createAccessibilityNodeInfo().text.toString());assertEquals(View.ACCESSIBILITY_LIVE_REGION_POLITE,label.accessibilityLiveRegion)
      assertNull(ShadowToast.getLatestToast())
      val margins=label.layoutParams as FrameLayout.LayoutParams
      val safeW=notice.width-notice.paddingLeft-notice.paddingRight-margins.leftMargin-margins.rightMargin-label.paddingLeft-label.paddingRight
      val safeH=notice.height-notice.paddingTop-notice.paddingBottom-margins.topMargin-margins.bottomMargin-label.paddingTop-label.paddingBottom
      val direction=VerticalText.uiDirection();var wrapped=VerticalText.wrapLabel(text,label.paint,min(240f,safeH.toFloat()),direction)
      var box=VerticalText.bounds(wrapped,label.paint,direction,GlyphOrientation.MIXED,1f)
      if(ceil(box.width())>safeW) {wrapped=VerticalText.wrapLabel(text,label.paint,safeH.toFloat(),direction);box=VerticalText.bounds(wrapped,label.paint,direction,GlyphOrientation.MIXED,1f)}
      val fullH=label.layout.height+label.compoundPaddingTop+label.compoundPaddingBottom
      out.append("${android.os.Build.VERSION.SDK_INT}\t$tag\t$phase\t${host.width}\t${host.height}\t${notice.paddingBottom}\t${label.height}\t$fullH\t${fullH<=label.height}\t${box.width()}\t${box.height()}\t${safeW>0 && safeH>0 && ceil(box.width())<=safeW && ceil(box.height())<=safeH}\n")
     }
     val event=MotionEvent.obtain(0,0,MotionEvent.ACTION_DOWN,30f,20f,0);try {assertTrue(host.dispatchTouchEvent(event))}finally {event.recycle()};assertEquals(1,touches)
     Shadows.shadowOf(Looper.getMainLooper()).idleFor(java.time.Duration.ofMillis(3500));assertSame(notice,host.findViewWithTag<View>("locale_notification"))
     Shadows.shadowOf(Looper.getMainLooper()).idleFor(java.time.Duration.ofMillis(5000));assertNull(host.findViewWithTag<View>("locale_notification"));assertNull(ShadowToast.getLatestToast())
    } finally {R.setField(accessibility,"mNonInteractiveUiTimeout",oldTimeout);controller.close();settle();if(mode!=null) R.setStaticField(Class.forName("android.view.ViewRootImpl"),"sNewInsetsMode",mode)}
   }
  } finally {
   if(mode!=null) R.setStaticField(Class.forName("android.view.ViewRootImpl"),"sNewInsetsMode",mode)
   Locale.setDefault(prev);RuntimeEnvironment.setQualifiers(quals);File(dir,"transitions-api${android.os.Build.VERSION.SDK_INT}.tsv").writeText(out.toString())
  }
 }
}
