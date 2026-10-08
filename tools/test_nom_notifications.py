"""Mechanical source/cmap guards only; not Android execution or glyph acceptance."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from test_locale_font_coverage import mapped_codepoints

ROOT=Path(__file__).resolve().parents[1]
JAVA=ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic'

class NomNotificationSourceTest(unittest.TestCase):
    def test_current_api_nom_route_does_not_use_a_system_toast_in_a_visible_window(self):
        text=(JAVA/'LocaleTypography.kt').read_text()
        self.assertIn('fun showMessage(',text)
        self.assertIn('Build.VERSION.SDK_INT>=30 && asset()=="fonts/anpaintnomui.ttf"',text)
        self.assertIn('if(font!=null && LocaleNotification.show(context,text,duration,font,anchor)) return',text)
        self.assertIn('if(Build.VERSION.SDK_INT<30) toast.view?.let {install(it)}',text)

    def test_surface_is_an_in_app_view_with_explicit_font_and_visibility_boundaries(self):
        text=(JAVA/'LocaleNotification.kt').read_text()
        for expected in ('host.addView(notice,FrameLayout.LayoutParams(-1,-1))','typeface=font',
                         'owner.isFinishing || owner.isDestroyed','host.isAttachedToWindow',
                         'host.isShown','host.windowVisibility!=View.VISIBLE',
                         'while(current is ContextWrapper)','if(next===current) return null',
                         'override fun dispatchTouchEvent(event: MotionEvent)=false'):
            self.assertIn(expected,text)
        for forbidden in ('WindowManager','PopupWindow','Toast.makeText','Toast(context)','setView('):
            self.assertNotIn(forbidden,text)

    def test_replacement_detach_and_hidden_window_remove_own_timeout(self):
        text=(JAVA/'LocaleNotification.kt').read_text()
        self.assertIn('host.findViewWithTag<Notice>(TAG)?.dismiss()',text)
        self.assertIn('private val expire=Runnable {dismiss()}',text)
        self.assertGreaterEqual(text.count('removeCallbacks(expire)'),2)
        self.assertIn('(parent as? ViewGroup)?.removeView(this)',text)
        self.assertIn('callbackHandler.post(dismissLater)',text)
        self.assertIn('if(visibility!=View.VISIBLE) dismissAfterDispatch()',text)
        self.assertNotIn('hasWindowFocus()',text)

    def test_lifecycle_dismissal_is_guarded_and_hierarchy_mutation_is_deferred(self):
        text=(JAVA/'LocaleNotification.kt').read_text()
        self.assertIn('private fun dismissAfterDispatch()',text)
        dismiss=text.split('        fun dismiss() {',1)[1].split('        private fun dismissAfterDispatch()',1)[0]
        self.assertLess(dismiss.index('if(dismissed) return'),dismiss.index('dismissed=true'))
        self.assertLess(dismiss.index('dismissed=true'),dismiss.index('removeView(this)'))
        queued=text.split('private fun dismissAfterDispatch()',1)[1].split('override fun onDetachedFromWindow()',1)[0]
        self.assertIn('callbackHandler.removeCallbacks(expire)',queued)
        self.assertIn('callbackHandler.removeCallbacks(dismissLater)',queued)
        self.assertIn('if(!dismissed) callbackHandler.post(dismissLater)',queued)
        self.assertNotIn('removeView(',queued)
        self.assertIn('private val callbackHandler=Handler(Looper.getMainLooper())',text)
        lifecycle=text.split('override fun onDetachedFromWindow()',1)[1]
        self.assertIn('dismissAfterDispatch()',lifecycle)
        self.assertNotIn('removeView(',lifecycle)
        self.assertNotIn(' dismiss()',lifecycle)
        self.assertNotIn('dismissed=true',lifecycle)

    def test_window_insets_and_accessibility_timeout_are_preserved(self):
        text=(JAVA/'LocaleNotification.kt').read_text()
        for expected in ('WindowInsets.Type.systemBars()','WindowInsets.Type.displayCutout()',
                         'WindowInsets.Type.ime()','getLocationInWindow(location)',
                         'getRecommendedTimeoutMillis','ACCESSIBILITY_LIVE_REGION_POLITE'):
            self.assertIn(expected,text)

    def test_existing_dialogs_supply_their_own_notification_anchor(self):
        checks={
            'AdvancedColourDialog.kt':'Toast.LENGTH_SHORT,saveCustomButton)',
            'GalleryCredits.kt':'Toast.LENGTH_SHORT,field)',
            'LegalInfo.kt':'Toast.LENGTH_SHORT,button)',
        }
        for name,expected in checks.items():
            self.assertIn(expected,(JAVA/name).read_text(),name)
        self.assertIn('copy(activity,entries.getValue(sources[selected]).text,field)',(JAVA/'GalleryCredits.kt').read_text())

    def test_exact_cursor_resources_are_covered_by_the_bundled_font(self):
        values={e.attrib['name']:e.text or '' for e in ET.parse(ROOT/'Paintroid/src/main/res/values-b+vi+Hani/strings.xml').getroot()}
        cmap=mapped_codepoints(ROOT/'Paintroid/src/main/assets/fonts/anpaintnomui.ttf')
        for key in ('ui_cursor_pan_move32','ui_cursor_pan_draw32','ui_cursor_tap_hint37'):
            text=values[key]
            self.assertIn(0x2ABBB,{ord(c) for c in text},key)
            self.assertEqual([],sorted({ord(c) for c in text if not c.isspace()}-cmap),key)

if __name__=='__main__':unittest.main()
