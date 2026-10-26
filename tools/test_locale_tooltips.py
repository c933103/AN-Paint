"""Source wiring guard only. Native behaviour lives in LocaleTooltip*Test.kt."""
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
JAVA=ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic'

class LocaleTooltipSourceTest(unittest.TestCase):
    def test_six_assignments_share_the_native_api_guard(self):
        expected={
            'ToolButton.kt':['LocaleTooltip.set(this,tool.label)'],
            'ToolCategoryButton.kt':['LocaleTooltip.set(this,contentDescription)'],
            'ActionButton.kt':['LocaleTooltip.set(this,icon.label)'],
            'ClassicPaintActivity.kt':['LocaleTooltip.set(this,ui(R.string.ui_pixel_grid_help33))',
                                       'LocaleTooltip.set(this,value)','LocaleTooltip.set(it,it.text)'],
        }
        for name,calls in expected.items():
            source=(JAVA/name).read_text()
            for call in calls:self.assertEqual(1,source.count(call),(name,call))
        assignments=[p.name for p in JAVA.glob('*.kt') if re.search(r'\btooltipText\s*=',p.read_text())]
        self.assertEqual(['LocaleTooltip.kt'],assignments)

    def test_metric_span_preserves_native_ownership_and_measure_draw_font(self):
        source=(JAVA/'LocaleTooltip.kt').read_text()
        for text in ('if(Build.VERSION.SDK_INT<26) return', 'view.tooltipText=format(view.context,value)',
                     'if(VerticalText.uiVertical(context)) null else LocaleTypography.typeface(context)',
                     'MetricAffectingSpan()',
                     'paint.typeface=Typeface.create(font,paint.typeface?.style ?: Typeface.NORMAL)',
                     'override fun updateMeasureState(paint: TextPaint)=apply(paint)',
                     'override fun updateDrawState(paint: TextPaint)=apply(paint)',
                     'previous.forEach {removeSpan(it)}'):
            self.assertIn(text,source)
        for forbidden in ('WindowManager','contentDescription=','TypefaceSpan(font)'):
            self.assertNotIn(forbidden,source)
        for required in ('view.tooltipText=null','if(help?.invoke(target)==true) true else show()',
                         'view.setOnHoverListener(null)','view.setOnLongClickListener(null)',
                         'view.isLongClickable=originalLongClickable',
                         'setAccessibilityDelegate(view,originalDelegate)','handler.removeCallbacks(reveal)',
                         'view.setTag(org.catrobat.paintroid.R.id.locale_tooltip_binding,it)'):
            self.assertIn(required,source)
        self.assertNotIn('PopupWindow',source)
        overlay=(JAVA/'VerticalTooltipOverlay.kt').read_text()
        for required in ('WindowInsets.Type.ime()', 'getWindowVisibleDisplayFrame',
                         'if(!capturingGesture) return false', 'capturingGesture=persistent',
                         'getRecommendedTimeoutMillis', 'handler.post(dismissLater)',
                         'card.layout(x,y,x+card.measuredWidth,y+card.measuredHeight)'):
            self.assertIn(required,overlay)
        self.assertNotIn('LocaleTooltip', (JAVA/'LocaleTypography.kt').read_text())

if __name__=='__main__':unittest.main()
