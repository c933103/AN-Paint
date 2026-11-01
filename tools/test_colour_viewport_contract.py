"""Structural native-input/evidence controls; runtime tests own layout outcomes."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/AdvancedColourDialog.kt'
INSTALLED = ROOT / 'app/src/androidTest/java/paint/anpaint/android/ColourViewportDeviceTest.kt'

class ColourViewportContractTest(unittest.TestCase):
    def test_native_reveal_keeps_native_input_and_bounded_progress(self):
        source = INSTALLED.read_text()
        helper = source.split('private fun reveal(', 1)[1].split('private fun scrollLimit', 1)[0]
        self.assertNotIn('.scrollTo(', helper)
        for required in ('visibleBounds(view).contains(target())', 'repeat(12)',
                         'seen.add(onMain {geometry(view).toString()})'):
            self.assertIn(required, helper)

    def test_notice_reveal_keeps_native_input_and_bounded_progress(self):
        source = (INSTALLED.parent / 'LocalizedDialogDeviceTest.kt').read_text()
        route = source.split('private fun reveal(', 1)[1].split('private fun scrollLimit', 1)[0]
        for required in ('visibleBounds(view).contains(target())',
                         'swipe(route.first,route.second,route.third);settle(view)',
                         'repeat(12)', 'seen.add(onMain {geometry(view).toString()})',
                         'No native scroll route to full caption'):
            self.assertIn(required, route)
        for forbidden in ('.scrollTo(', '.performClick('):
            self.assertNotIn(forbidden, route)
        self.assertIn('deadline=started+45000', source)

    def test_colour_scroll_uses_native_gutter_input(self):
        source = INSTALLED.read_text()
        for required in ('colour-native-scroll-route', 'val start=Point(x,', 'val end=Point(x,',
                         'device.swipe(', 'if(direction>0) high else low'):
            self.assertIn(required, source)
        self.assertNotIn('.performClick(', source)

    def test_back_and_ime_use_native_input_and_independent_window_observers(self):
        source = INSTALLED.read_text()
        for required in ('awaitNativeImeWindow(true,root,field)', 'awaitNativeImeWindow(false,root,field)',
                         'SystemClock.uptimeMillis()-stableSince>=250',
                         'AccessibilityWindowInfo.TYPE_INPUT_METHOD', 'Settings.Secure.DEFAULT_INPUT_METHOD',
                         'device.pressKeyCode(KeyEvent.KEYCODE_BACK)'):
            self.assertIn(required, source)
        self.assertNotIn('device.pressBack(', source)

    def test_current_fixture_keeps_readiness_and_deadline_failure_semantics(self):
        source = INSTALLED.read_text()
        for required in ('deadline=SystemClock.uptimeMillis()+45000',
                         'activity.startupReady && !activity.busy && activity.paintCanvas.width>0 && activity.window.decorView.hasWindowFocus()',
                         'recordEditorStartup("failed-before-cleanup")',
                         'throw AssertionError("Timed out: $label")'):
            self.assertIn(required, source)

    def test_large_ime_evidence_distinguishes_synthetic_activation_and_native_observation(self):
        source = INSTALLED.read_text()
        body = source.split('private fun largeColourImeLifecycle(', 1)[1].split('private fun ancestors(', 1)[0]
        for required in ('"colour-2x-synthetic-ime-activation"',
                         '"focus_request_returned",focused', '"field_focused",field.hasFocus()',
                         '"ime_request_returned",requested', '"initial_native_field_activation","not-tested"',
                         '"initial_full_hex_visibility","not-accepted"',
                         'awaitNativeImeWindow(true,root,field,"colour-2x-ime-open")',
                         'awaitNativeImeWindow(false,root,field,"colour-2x-ime-hidden")',
                         '"simultaneous_ime_field_footer_fit","not-accepted"',
                         'evidence.capture("colour-2x-failed-before-dismiss")', '.showSoftInput(field,0)'):
            self.assertIn(required, body)
        for forbidden in ('.showSoftInput(field,InputMethodManager.SHOW_IMPLICIT)',
                          '.showSoftInput(field,InputMethodManager.SHOW_FORCED)',
                          'rootWindowInsets', 'tap("2x hex field"'):
            self.assertNotIn(forbidden, body)
        self.assertLess(body.index('evidence.capture("colour-2x-initial")'), body.index('field.requestFocus()'))
        self.assertLess(body.index('"colour-2x-synthetic-ime-activation"'), body.index('awaitNativeImeWindow(true'))
        helper = source.split('private fun largeLifecycleCaption(', 1)[1].split('private fun nativeImePresent(', 1)[0]
        for required in ('transformation?.getTransformation(view.text,view)', 'view.resources.getString(sourceResource)',
                         '"text",rawText', '"raw_text_length",rawText.length', '"expected_text",expectedText',
                         '"transformation_method",transformation?.javaClass?.name', '"transformed_text",transformed',
                         '"caption_length",transformed.length', 'node.text?.toString()',
                         'ancestors(view)', '"parent_id"'):
            self.assertIn(required, helper)
        for forbidden in ('uppercase(', 'lowercase(', 'ignoreCase', 'setAllCaps(', 'transformationMethod='):
            self.assertNotIn(forbidden, helper)
        for forbidden in ('performClick(', 'requestRectangleOnScreen(', 'setTextSize(', 'setSoftInputMode(', 'imeOptions='):
            self.assertNotIn(forbidden, body + helper)

    def test_cleanup_and_number_input_wiring_remain_explicit(self):
        # These are unmapped structural integration guards, not executed cleanup evidence.
        source = PRODUCTION.read_text()
        self.assertIn('removeOnGlobalLayoutListener(layoutListener)', source)
        self.assertIn('LocaleNumberInput.configure(this, decimal = true)', source)
        self.assertNotIn('setTextSize(', source)

if __name__ == '__main__':
    unittest.main()
