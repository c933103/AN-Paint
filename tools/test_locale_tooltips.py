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

    def test_legacy_native_tooltip_api_guard_remains_structural(self):
        source = (JAVA / 'LocaleTooltip.kt').read_text()
        self.assertIn('if(Build.VERSION.SDK_INT<26) return', source)

if __name__=='__main__':unittest.main()
