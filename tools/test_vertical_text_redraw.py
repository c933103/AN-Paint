"""Source guard for explicit custom-vertical redraw; not installed pixel evidence."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]


class VerticalTextRedrawContractTest(unittest.TestCase):
    def test_both_custom_renderers_schedule_layout_and_invalidation_on_text_change(self):
        source=(ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/RibbonWidgets.kt').read_text()
        for start,end in [('open class FlowButton(', '/** Original square tool tiles'),
                          ('class FlowTextView(', '/** Start at the first reading column')]:
            with self.subTest(widget=start):
                widget=source.split(start,1)[1].split(end,1)[0]
                change=widget.split('override fun onTextChanged(',1)[1].split('private fun caption',1)[0]
                def check(text):
                    self.assertIn('super.onTextChanged(text,start,lengthBefore,lengthAfter)',text)
                    self.assertIn('if(VerticalText.uiVertical()) {requestLayout();invalidate()}',text)
                check(change)
                for deleted in ('requestLayout();','invalidate()','super.onTextChanged(text,start,lengthBefore,lengthAfter)'):
                    with self.assertRaises(AssertionError):check(change.replace(deleted,''))

    def test_regression_checks_real_missing_native_layout_and_each_observed_failure(self):
        source=(ROOT/'Paintroid/src/test/java/org/catrobat/paintroid/local/VerticalTextRedrawTest.kt').read_text()
        for required in ('sdk=[30,35]','en-XV','mnc-Mong','lzh-Hant','qaa-Zsye-XV',
                         'Untitled.png','Untitled.jpg','listOf(76,1,100,1,100)',
                         'view.layout)','clearWasInvalidated()','setDidRequestLayout(false)',
                         'wasInvalidated()','didRequestLayout()','view.isLayoutRequested'):
            self.assertIn(required,source)
        self.assertNotIn('.draw(',source)
        self.assertNotIn('.invalidate(',source)
        self.assertNotIn('.requestLayout(',source)


if __name__=='__main__':unittest.main()
