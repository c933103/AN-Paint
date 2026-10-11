"""Source contracts for the exact installed Advanced Colour baseline replay.

These are harness checks, not installed Android results.
"""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'verification/advanced-colour-viewport-2026-10-11'
ORIGINAL=EVIDENCE/'original-positive-fixture'
SOURCE=ROOT/'app/src/androidTest/java/paint/anpaint/android/LocalizedDialogDeviceTest.kt'


class ColourBaselineContractTest(unittest.TestCase):
    def test_original_positive_method_remains_verbatim(self):
        original=(ORIGINAL/'normalAdvancedColourKeepsFiniteViewportAndFixedControls.kt.txt').read_bytes()
        self.assertEqual(hashlib.sha256(original).hexdigest(),'08b0efebe1e7a71d03fee557243e47263d22560231fc55cf2b00e693f3a53096')
        self.assertEqual(SOURCE.read_bytes().count(original),1)
        self.assertEqual(re.findall(r'@Test fun (\w+)',SOURCE.read_text()),
                         ['normalAdvancedColourKeepsFiniteViewportAndFixedControls',
                          'retainedColourStateSurvivesRotationImeCancelAndReopen',
                          'hungarianColourCaptionsFitPortraitAndLandscape'])

    def test_fixture_and_native_pointer_helpers_are_original(self):
        original=(ORIGINAL/'LocalizedDialogDeviceTest.df214fee.kt.txt').read_text()
        current=SOURCE.read_text()
        route_start=current.index('        // Colour-surface drags intentionally belong to the colour editor.')
        route_end=current.index('        assertTrue("Native scroll gesture"',route_start)
        self.assertIn('val start=Point(x,if(direction>0) high else low)',current[route_start:route_end])
        self.assertIn('val end=Point(x,start.y-if(direction>0) distance else -distance)',current[route_start:route_end])
        # Both endpoints stay in the visible gutter; restore both original centre
        # coordinates only for comparison with the retained historical helper.
        current=(current[:route_start]
                 +'        val start=Point(bounds.centerX(),if(direction>0) high else low)\n'
                 +'        val end=Point(bounds.centerX(),start.y-if(direction>0) distance else -distance)\n'
                 +current[route_end:])
        for start,end in [('    private fun fixture(', '    private fun openAbout('),
                          ('    private fun orient(', '    private fun intrinsic('),
                          ('    private fun tap(', '    private fun checkDeadline(')]:
            # Diagnostic is inserted immediately before checkDeadline only.
            preserved=original[original.index(start):original.index(end)]
            self.assertIn(preserved,current)
        self.assertIn('recordColourAllocation()\n        throw AssertionError("Timed out: $label")',current)
        self.assertNotIn('performClick(',current)

    def test_baseline_colour_source_identity_and_production_tree_are_pinned(self):
        identity=json.loads((EVIDENCE/'baseline-source-identity.json').read_text())
        self.assertEqual(identity['base_commit'],'691f8870649a1d21d1441f4e3d0e795660b23e9a')
        self.assertEqual(identity['base_tree'],'040a35f40a6e8e143c6a9b2121e804f0704dd5d1')
        colour=ORIGINAL/'AdvancedColourDialog.baseline.kt.txt'
        self.assertEqual(hashlib.sha256(colour.read_bytes()).hexdigest(),
                         '0d26b7eb50028ed9c0cf1698b68c8138ecc02b309b2d439a88ef521b8a902684')
        self.assertEqual(identity['production_changes'],[])

    def test_candidate_retains_colour_math_validation_commit_and_input_configuration(self):
        before=(ORIGINAL/'AdvancedColourDialog.baseline.kt.txt').read_text()
        after=(ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/AdvancedColourDialog.kt').read_text()
        self.assertEqual(before.split('    fun show(): AlertDialog {')[0],after.split('    fun show(): AlertDialog {')[0])
        self.assertEqual(before.split('    private fun refreshCustom() {')[1],after.split('    private fun refreshCustom() {')[1])
        self.assertEqual(before[before.index('        fun field('):before.index('        // Keep the tabs,')],
                         after[after.index('        fun field('):after.index('        // Keep the tabs,')])
        self.assertIn('if (fields.values.any { it.error != null }) return@setOnClickListener',after)
        self.assertIn('accepted=true;commit(value.colour or Color.BLACK);dialog.dismiss()',after)
        self.assertIn('if(!accepted) preview(original);closed()',after)
        self.assertIn('getWindowVisibleDisplayFrame(frame)',after)
        self.assertIn('setPaddingRelative(0,0,dp(32),0)',after)
        self.assertIn('isScrollbarFadingEnabled=false',after)
        self.assertIn('parent?.requestDisallowInterceptTouchEvent(true)',after)
        self.assertIn('Native surface drag',SOURCE.read_text())
        self.assertIn('colour-native-scroll-route',SOURCE.read_text())
        self.assertIn('removeOnGlobalLayoutListener(layoutListener)',after)

    def test_intrinsic_captions_and_native_back_successor_keep_strict_outcomes(self):
        production=(ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/AdvancedColourDialog.kt').read_text()
        source=SOURCE.read_text()
        helper=(EVIDENCE/'native-back-successor-helper.d7f1a958.kt.txt').read_bytes()
        self.assertEqual(hashlib.sha256(helper).hexdigest(),'46c005dee8a443e69daa0fe0297c38023c00e80e86fd9a1aefea721c65b38c0c')
        self.assertEqual(SOURCE.read_bytes().count(helper),1)
        self.assertEqual(production.count('minHeight=dp(44);minimumHeight=dp(44)'),2)
        self.assertIn('val tabs = LinearLayout(activity).apply { isBaselineAligned=false }',production)
        self.assertIn('val advancedTabs = LinearLayout(activity).apply { isBaselineAligned=false }',production)
        self.assertIn('minHeight=dp(48);minimumHeight=dp(48)',production)
        self.assertIn('previewRow.addView(saveCustomButton,LinearLayout.LayoutParams(0,-2,1f))',production)
        self.assertNotIn('device.pressBack(',source)
        self.assertEqual(source.count('device.pressKeyCode(KeyEvent.KEYCODE_BACK)'),1)
        self.assertIn('SystemClock.uptimeMillis()-stableSince>=250',source)
        self.assertIn('AccessibilityWindowInfo.TYPE_INPUT_METHOD',source)
        self.assertIn('Settings.Secure.DEFAULT_INPUT_METHOD',source)
        self.assertIn('awaitNativeImeWindow(true,root,field)',source)
        self.assertIn('awaitNativeImeWindow(false,root,field)',source)
        self.assertIn('"colour-ime-wait-failed-before-dismiss"',source)
        self.assertIn('awaitClipboardOverlayAbsent()',source)
        self.assertIn('it.title?.toString()=="ClipboardOverlay"',source)
        self.assertIn('!reopenedRoot.isAttachedToWindow && activity.window.decorView.hasWindowFocus()',source)
        self.assertIn('commits==0 && closes==2',source)
        self.assertIn('assertEquals(1,commits);assertEquals(3,closes)',source)
        model=(ROOT/'Paintroid/src/test/java/org/catrobat/paintroid/local/AdvancedColourViewportTest.kt').read_text()
        self.assertEqual(model.count('for(tag in listOf("en-US","hu"))'),2)
        self.assertIn('tabTags.forEach {complete(root.findViewWithTag(it));caption(root.findViewWithTag(it))}',model)

    def test_timeout_capture_runs_before_original_dismissal_and_remains_failure(self):
        source=SOURCE.read_text()
        self.assertIn('if(label=="normal Advanced Colour laid out") recordColourAllocation()',source)
        self.assertIn('if(label=="initial editor") recordEditorStartup("failed-before-cleanup")',source)
        self.assertIn('await("initial editor") {activity.startupReady && !activity.busy && activity.paintCanvas.width>0 && activity.window.decorView.hasWindowFocus()}',source)
        self.assertIn('evidence.capture("colour-pre-assert-allocation")',source)
        self.assertIn('finally {onMain {dialog.dismiss()}}',source)
        self.assertIn('assertTrue("Real gesture scrolls the internal colour viewport",inner.scrollY>before)',source)
        shell=(ROOT/'tools/ci_emulator.sh').read_text()
        self.assertIn('if ! collect_colour_evidence; then',shell)
        self.assertIn('if (( status == 0 )); then status=1; fi',shell)
        self.assertIn('--suite app --timeout-seconds 180',shell)


if __name__=='__main__':unittest.main()
