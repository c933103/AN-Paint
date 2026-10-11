"""Shared-dialog source scope and complete applicability inventory contracts."""
import unittest
from pathlib import Path
import localized_dialog_applicability as scope
import translation_catalogues as catalogues

ROOT=Path(__file__).resolve().parents[1]
JAVA=ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic'

class LocalizedDialogLayoutContracts(unittest.TestCase):
    def test_every_catalogue_and_offered_language_has_a_shared_layout_disposition(self):
        report=scope.inventory()
        self.assertEqual(set(catalogues.catalogue_paths())|{'default'}, {row['tag'] for row in report['rows']})
        self.assertEqual(set(catalogues.offered_tags()), {row['tag'] for row in report['rows'] if row['offered']})
        for row in report['rows']:
            self.assertTrue(set(row['exact_override_keys'])<=set(scope.KEYS))
            self.assertEqual([],row['missing_effective_keys'])
        self.assertEqual(set(),set(scope.RUNTIME)-set(catalogues.offered_tags()))
        self.assertEqual(set(),set(scope.VERTICAL)-set(catalogues.offered_tags()))

    def test_shared_dialogs_use_intrinsic_text_and_independently_bounded_regions(self):
        terms=(JAVA/'LegalInfo.kt').read_text()
        shared=(JAVA/'ResponsiveDialog.kt').read_text()
        builder=(JAVA/'VerticalUi.kt').read_text()
        for forbidden in ('maxLines=2','dp(52)','dp(48),1f'):
            self.assertNotIn(forbidden,terms)
        self.assertIn('ResponsiveDialogLayout(activity)',terms)
        self.assertIn('ResponsiveDialogColumns(activity).apply {addView(heading)}',terms)
        self.assertIn('ResponsiveDialogColumns(activity).apply {addView(actions)}',terms)
        self.assertIn('fun setScrollableTitle(title: CharSequence)',builder)
        self.assertIn('setCustomTitle(ResponsiveDialogTitle(context,title))',builder)
        self.assertNotIn('mountHorizontal',builder)
        self.assertNotIn('WrappingDialogChoices',builder)
        self.assertIn('EditorDialogBuilder(this).setScrollableTitle(ui(R.string.ui_about_credits23))',(JAVA/'ClassicPaintActivity.kt').read_text())
        self.assertIn('button.maxLines=Int.MAX_VALUE;button.ellipsize=null',shared)
        self.assertIn('windowLimit=available',shared)
        self.assertIn('LayoutParams(-1,-2,1f)',shared)

    def test_notice_column_resize_is_scoped_and_preserves_the_reader_offset(self):
        shared=(JAVA/'ResponsiveDialog.kt').read_text()
        columns=shared[shared.index('internal class ResponsiveDialogColumns'):]
        self.assertLess(columns.index('val offset='),columns.index('super.onLayout'))
        self.assertIn('(it-scrollX).coerceAtLeast(0)',columns)
        self.assertIn('range-offset else offset',columns)
        self.assertIn('previousRange=range',columns)
        self.assertIn('focused==null || focused===this',columns)
        self.assertIn('previousRange==null || previousRange!=range',columns)
        original=(JAVA/'RibbonWidgets.kt').read_text()
        self.assertIn('private var positioned=false',original)
        test=(ROOT/'Paintroid/src/test/java/org/catrobat/paintroid/local/LocalizedDialogLayoutTest.kt').read_text()
        self.assertIn('retainedVerticalNoticeKeepsReadingOffsetAcrossRotation',test)
        self.assertIn('noticeColumnsClampOffsetsAcrossContentAndViewportChanges',test)

    def test_runtime_oracles_do_not_substitute_direct_click_for_pointer_reachability(self):
        test=(ROOT/'Paintroid/src/test/java/org/catrobat/paintroid/local/LocalizedDialogLayoutTest.kt').read_text()
        self.assertIn('root.dispatchTouchEvent(event)',test)
        self.assertIn('visible.contains(lineRect)',test)
        self.assertIn('layout.getEllipsisCount(line)',test)
        self.assertNotIn('.performClick()',test)
        self.assertNotIn('.performItemClick(',test)
        self.assertIn('fontScale=2f',test)
        self.assertIn('w640dp-h320dp-land',test)
        self.assertIn('sdk=[30,35]',test)

if __name__=='__main__': unittest.main()
