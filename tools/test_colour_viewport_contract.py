"""Current colour integration guards; Android layout/input tests remain separate."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/AdvancedColourDialog.kt'
INSTALLED = ROOT / 'app/src/androidTest/java/paint/anpaint/android/ColourViewportDeviceTest.kt'
MODEL = ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local/AdvancedColourViewportTest.kt'


class ColourViewportContractTest(unittest.TestCase):
    def test_native_reveal_uses_exact_scrollview_range_and_forces_last_pixel_regression(self):
        source = INSTALLED.read_text()
        for required in ('candidate,direction)', 'view.height-view.paddingTop-view.paddingBottom',
                         'direction<0 -> view.scrollY>0', 'direction>0 -> view.scrollY<scrollLimit(view)',
                         'else view.canScrollVertically(direction)', 'controls.scrollTo(controls.scrollX,maximum-1)',
                         'assertEquals(limit-1,controls.scrollY)', 'controls.canScrollVertically(1)',
                         'assertEquals("Native gesture reaches the exact endpoint",limit,controls.scrollY)',
                         'assertFalse("No route beyond the endpoint",canRevealVertically(controls,1))',
                         'assertFalse("No route before the top endpoint",canRevealVertically(controls,-1))',
                         'repeat(12)', 'seen.add(onMain {geometry(view).toString()})'):
            self.assertIn(required, source)
        self.assertNotIn('candidate.canScrollVertically(direction)', source)
        setup = source.index('controls.scrollTo(controls.scrollX,maximum-1)')
        before = source.index('"colour-endpoint-before"', setup)
        reveal = source.index('reveal(sample) {rawBounds(sample)}', before)
        after = source.index('"colour-endpoint-after"', reveal)
        self.assertLess(source.index('evidence.capture("colour-large-preview-reached")'), setup)
        self.assertLess(after, source.index('"colour-large-rail-top-reached"'))
        helper = source.split('private fun reveal(', 1)[1].split('private fun scrollLimit', 1)[0]
        self.assertNotIn('.scrollTo(', helper)
        self.assertIn('visibleBounds(view).contains(target())', helper)

    def test_notice_reveal_keeps_the_same_exact_endpoint_route_as_colour(self):
        colour = INSTALLED.read_text()
        notice = (INSTALLED.parent / 'LocalizedDialogDeviceTest.kt').read_text()
        def endpoint(source):
            return source.split('    private fun scrollLimit(', 1)[1].split('    private fun swipe(', 1)[0]
        self.assertIn('private fun scrollLimit(', notice)
        self.assertEqual(endpoint(colour), endpoint(notice))
        route = notice.split('private fun reveal(', 1)[1].split('private fun scrollLimit', 1)[0]
        self.assertIn('canRevealVertically(candidate,direction)', route)
        self.assertNotIn('candidate.canScrollVertically(direction)', route)
        self.assertIn('visibleBounds(view).contains(target())', route)
        self.assertIn('swipe(route.first,route.second,route.third);settle(view)', route)
        self.assertIn('repeat(12)', route)
        self.assertIn('seen.add(onMain {geometry(view).toString()})', route)
        self.assertNotIn('.scrollTo(', route)
        self.assertNotIn('.performClick(', route)
        self.assertIn('deadline=started+45000', notice)
        self.assertIn('No native scroll route to full caption', route)

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
            'largeEnglishColourImeBackAndFooterLifecycle',
            'largeHungarianColourImeBackAndFooterLifecycle',
        ])

    def test_large_ime_lifecycle_keeps_native_oracles_exact_state_and_six_captures(self):
        source = INSTALLED.read_text()
        body = source.split('private fun largeColourImeLifecycle(', 1)[1].split('private fun ancestors(', 1)[0]
        for required in ('fixture(tag,2f)', 'orient(true,scenario)', 'AdvancedColourDialog(',
                         'assertEquals(640,activity.window.decorView.width)',
                         'assertEquals(320,activity.window.decorView.height)',
                         'field.setText("#13579B");field.setSelection(2,5)',
                         'val focused=field.requestFocus()', '"colour-2x-synthetic-ime-activation"',
                         '"focus_request_returned",focused', '"field_focused",field.hasFocus()',
                         '"ime_request_returned",requested', '"initial_native_field_activation","not-tested"',
                         '"initial_full_hex_visibility","not-accepted"',
                         'awaitNativeImeWindow(true,root,field,"colour-2x-ime-open")',
                         'awaitNativeImeWindow(false,root,field,"colour-2x-ime-hidden")',
                         'nativeBack("hide 2x colour IME"', '!nativeImePresent()',
                         'dialog===firstDialog && picker===firstPicker', 'dialog.window!!.decorView===root',
                         'root.findViewWithTag<View>("colour_hex")===field', 'field.selectionStart==2 && field.selectionEnd==5',
                         'nativeBack("close 2x reopened colour"', 'tap("2x Cancel",cancel)',
                         'tap("2x invalid rejected",finalUse)', 'tap("2x valid committed",finalUse)',
                         'assertNotNull(finalField.error)', 'commits==1 && closes==3',
                         'preview==android.graphics.Color.RED', '"simultaneous_ime_field_footer_fit","not-accepted"'):
            self.assertIn(required, body)
        self.assertNotIn('rootWindowInsets', body)
        self.assertNotIn('tap("2x hex field"', body)
        self.assertLess(body.index('evidence.capture("colour-2x-initial")'), body.index('field.requestFocus()'))
        self.assertLess(body.index('"colour-2x-synthetic-ime-activation"'), body.index('awaitNativeImeWindow(true'))
        self.assertEqual(re.findall(r'evidence.capture\("([^"]+)"\)', body), [
            'colour-2x-initial', 'colour-2x-cancel-reached', 'colour-2x-reopened', 'colour-2x-use-reached',
            'colour-2x-failed-before-dismiss'])
        helper = source.split('private fun largeLifecycleCaption(', 1)[1].split('private fun nativeImePresent(', 1)[0]
        for required in ('intrinsic(view)', 'node.text?.toString()', 'getLineStart(line)', 'getLineEnd(line)',
                         'reveal(view) {lineBounds()}', 'ancestors(view)', 'contains(target)', '"parent_id"'):
            self.assertIn(required, helper)
        for required in ('transformation?.getTransformation(view.text,view)', 'view.resources.getString(sourceResource)',
                         '"text",rawText', '"raw_text_length",rawText.length', '"expected_text",expectedText',
                         '"transformation_method",transformation?.javaClass?.name', '"transformed_text",transformed',
                         '"caption_length",transformed.length', '"Exact source caption retained",expectedText,rawText',
                         '"Actual native footer action id"', 'android.R.id.button2', 'android.R.id.button1',
                         '"android.text.method.AllCapsTransformationMethod"',
                         '"Complete transformed layout caption",transformed,view.layout.text.toString()',
                         '"Complete accessible caption",transformed,node.text?.toString()'):
            self.assertIn(required, helper)
        for forbidden in ('uppercase(', 'lowercase(', 'ignoreCase', 'setAllCaps(', 'transformationMethod='):
            self.assertNotIn(forbidden, helper)
        for forbidden in ('performClick(', 'requestRectangleOnScreen(', 'setTextSize(', 'setSoftInputMode(', 'imeOptions='):
            self.assertNotIn(forbidden, body + helper)

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

    def test_large_compact_tabs_share_editor_scroll_without_changing_normal_layout(self):
        source = PRODUCTION.read_text()
        for required in ('val scrollTabs=columns && activity.resources.configuration.fontScale>1f',
                         'if(scrollTabs != (tabs.parent===body))',
                         '(tabs.parent as? ViewGroup)?.removeView(tabs)',
                         '(if(scrollTabs) body else editorPanel).addView(tabs,0,',
                         'LinearLayout.LayoutParams(-1,-2)',
                         'minHeight=dp(44);minimumHeight=dp(44)',
                         'minHeight=dp(48);minimumHeight=dp(48)'):
            self.assertIn(required, source)
        self.assertLess(source.index('val scrollTabs=columns'),
                        source.index('super.onMeasure(widthMeasureSpec,heightMeasureSpec)'))
        model = MODEL.read_text()
        for required in ('largeShortEditorScrollsTabsAndEveryFullCaptionLineWithoutShrinking',
                         'modestlyEnlargedEditorRetainsCaptionsAndIdentityAcrossRepeatedReparenting',
                         '@Config(fontScale=1.3f,qualifiers="w640dp-h320dp-land-mdpi")',
                         'repeat(3)',
                         'val panelHeight=if(tag=="en-US") 109 else 104',
                         'assertSame(body,tabs.parent)', 'assertSame(editor.parent,tabs.parent)',
                         'visible.contains(local)', 'editor.offsetDescendantRectToMyCoords(view,target)',
                         'assertEquals(2,field.selectionStart);assertEquals(5,field.selectionEnd)',
                         'assertSame(field,root.findViewWithTag<EditText>("colour_hex"))'):
            self.assertIn(required, model)


if __name__ == '__main__':
    unittest.main()
