"""Current colour integration guards; Android layout/input tests remain separate."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/AdvancedColourDialog.kt'
INSTALLED = ROOT / 'app/src/androidTest/java/paint/anpaint/android/ColourViewportDeviceTest.kt'
MODEL = ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local/AdvancedColourViewportTest.kt'


class ColourViewportContractTest(unittest.TestCase):
    def test_all_direction_decisions_use_the_rendering_context(self):
        source = PRODUCTION.read_text()
        self.assertEqual(re.findall(r'VerticalText.uiVertical\(([^)]*)\)', source), ['activity'] * 4)
        model = MODEL.read_text()
        for expected in ('horizontalColumnsAndWindowResizeFollowResourcesDespiteVerticalProcessDefault',
                         'verticalColourFormFollowsResourcesDespiteHorizontalProcessDefault',
                         'Locale.setDefault(Locale.forLanguageTag(it))', 'LinearLayout.HORIZONTAL',
                         'dialog.window!!.attributes.width', 'vertical_dialog_columns'):
            self.assertIn(expected, model)
        self.assertLess(model.index('processTag?.let'), model.index('val dialog=AdvancedColourDialog'))

    def test_original_positive_assertions_stay_positive_and_use_native_gutter_input(self):
        source = INSTALLED.read_text()
        body = source.split('@Test fun normalAdvancedColourKeepsFiniteViewportAndFixedControls()', 1)[1].split('@Test fun', 1)[0]
        for expected in ('inner.height>0', 'inner.getChildAt(0).height>inner.height',
                         'inner.scrollY>before', 'fixed.map {assertComplete(it);rawBounds(it)}',
                         'tap("colour cancel"', 'assertEquals(0,committed);assertEquals(1,closed)'):
            self.assertIn(expected, body)
        for expected in ('colour-native-scroll-route', 'val start=Point(x,', 'val end=Point(x,',
                         'device.swipe(', 'if(direction>0) high else low'):
            self.assertIn(expected, source)
        self.assertNotIn('.performClick(', source)
        self.assertNotIn('unchangedAdvancedColourReportsShortLandscapeLimitation', source)

    def test_retained_state_and_native_back_outcomes_remain_required(self):
        source = INSTALLED.read_text()
        for expected in ('assertSame(root,dialog.window!!.decorView)', 'assertSame(field,root.findViewWithTag',
                         'assertEquals(2,field.selectionStart);assertEquals(5,field.selectionEnd)',
                         'assertEquals(slots,(0 until 16)', 'beforeDrag.second,inner.scrollY',
                         'awaitNativeImeWindow(true,root,field)', 'awaitNativeImeWindow(false,root,field)',
                         'SystemClock.uptimeMillis()-stableSince>=250',
                         'AccessibilityWindowInfo.TYPE_INPUT_METHOD', 'Settings.Secure.DEFAULT_INPUT_METHOD',
                         '!reopenedRoot.isAttachedToWindow && activity.window.decorView.hasWindowFocus()',
                         'assertEquals(0,commits);assertEquals(2,closes)',
                         'assertTrue(dialog.isShowing);assertEquals(0,commits);assertNotNull(finalField.error)',
                         'assertEquals(1,commits);assertEquals(3,closes)'):
            self.assertIn(expected, source)
        self.assertEqual(source.count('device.pressKeyCode(KeyEvent.KEYCODE_BACK)'), 1)
        self.assertNotIn('device.pressBack(', source)

    def test_hungarian_portrait_and_landscape_keep_complete_caption_and_cancel_checks(self):
        source = INSTALLED.read_text()
        body = source.split('@Test fun hungarianColourCaptionsFitPortraitAndLandscape()', 1)[1].split('private fun backWindowState', 1)[0]
        for expected in ('fixture("hu",1f)', 'for(landscape in listOf(true,false))',
                         'intrinsic(view);assertComplete(view)', 'Hungarian colour Cancel',
                         '!root.isAttachedToWindow', 'commits==0 && closes==1'):
            self.assertIn(expected, body)
        diagnostic = (MODEL.parent / 'AdvancedColourLayoutDiagnosticTest.kt').read_text()
        self.assertIn('@Config(fontScale=2f)', diagnostic)
        self.assertIn('recordLargeShortLandscapeWithoutClaimingAcceptance', diagnostic)

    def test_current_fixture_keeps_readiness_and_deadline_failure_semantics(self):
        source = INSTALLED.read_text()
        self.assertIn('deadline=SystemClock.uptimeMillis()+45000', source)
        self.assertIn('activity.startupReady && !activity.busy && activity.paintCanvas.width>0 && activity.window.decorView.hasWindowFocus()', source)
        self.assertIn('recordEditorStartup("failed-before-cleanup")', source)
        self.assertIn('throw AssertionError("Timed out: $label")', source)
        self.assertEqual(re.findall(r'@Test fun (\w+)', source), [
            'normalAdvancedColourKeepsFiniteViewportAndFixedControls',
            'retainedColourStateSurvivesRotationImeCancelAndReopen',
            'hungarianColourCaptionsFitPortraitAndLandscape',
            'largeEnglishColourCaptionsAndPreviewRemainReachable',
            'largeHungarianColourCaptionsAndPreviewRemainReachable',
        ])

    def test_validation_and_callbacks_are_not_replaced_by_layout_changes(self):
        source = PRODUCTION.read_text()
        for expected in ('if (fields.values.any { it.error != null }) return@setOnClickListener',
                         'accepted=true;commit(value.colour or Color.BLACK);dialog.dismiss()',
                         'if(!accepted) preview(original);closed()',
                         'removeOnGlobalLayoutListener(layoutListener)',
                         'LocaleNumberInput.configure(this, decimal = true)',
                         'setPaddingRelative(0,0,dp(32),0)',
                         'parent?.requestDisallowInterceptTouchEvent(true)'):
            self.assertIn(expected, source)
        self.assertNotIn('setTextSize(', source)

    def test_large_rail_reserves_scaled_width_before_measurement_without_shrinking(self):
        source = PRODUCTION.read_text()
        self.assertIn('activity.resources.configuration.fontScale.coerceAtLeast(1f)', source)
        self.assertIn('sampleColumn.layoutParams.width=if(columns) dp(76)*railWidth/dp(220) else dp(76)', source)
        self.assertLess(source.index('val railWidth=if(columns)'), source.index('super.onMeasure(widthMeasureSpec,heightMeasureSpec)'))
        self.assertIn('controls.width>220', INSTALLED.read_text())
        self.assertIn('editor.width>=controls.width', INSTALLED.read_text())
        model = MODEL.read_text()
        for required in ('largePreviewRailReflowsWithinTheInstalledShortViewport',
                         'editor.width>=controls.width', 'editor.height>0',
                         'caption(view);complete(view)', 'controls.isSmoothScrollingEnabled=false'):
            self.assertIn(required, model)


if __name__ == '__main__':
    unittest.main()
