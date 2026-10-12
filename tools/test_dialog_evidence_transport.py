"""Synthetic archive contracts; these are not installed-device test results."""
import copy
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest
import zipfile

from dialog_evidence_transport import (METHOD_SCREENS, NOTICE_METHODS, BASELINE_INSTALLED, BASELINE_EVIDENCE, OWNER, TEST_CLASS, PNG,
    extract, inspect_archive, source_binding, verify_receipt)

DIGEST = 'a' * 64


def summary():
    return dict(success=True, device_sdk=35, timed_out=False, returncode=0,
                source_tests_sha256=DIGEST, expected_tests=5, completed_tests=5, missing=[], unexpected=[], errors=[],
                included_tests=sorted(TEST_CLASS + '#' + name for name in METHOD_SCREENS),
                cases=[dict(classname=TEST_CLASS, name=m, status='passed') for m in METHOD_SCREENS])


def receipt(method):
    labels = ['notice copy', 'other terms', 'notice done', 'credit save', 'credit copy', 'credit done', 'colour cancel']
    geometry = dict(visible=[0, 0, 100, 100], raw=[0, 0, 100, 100])
    observations = [dict(kind='intrinsic-caption', lines=1, layout_height=20, available_text_height=30,
                         caption_length=5, layout_width=100, line_metrics=[dict(end=5, ellipsis=0, left=0, right=99)]),
                    dict(kind='caption-line-reached', geometry=geometry, line_rect=[1, 1, 90, 20])]
    for label in labels:
        observations.extend([dict(kind='pointer-before', label=label, tap=[50, 50], geometry=geometry),
                             dict(kind='pointer-injected', label=label)])
    value = dict(schema=1, test_class=TEST_CLASS, test_method=method, device_sdk=35,
                 package=OWNER, outcome='passed', source_tests_sha256=DIGEST,
                 source_binding='runner-supplied-needs-host-comparison',
                 screenshots=METHOD_SCREENS[method], observations=observations)
    if method == 'unchangedAdvancedColourReportsShortLandscapeLimitation':
        classification = 'baseline-identical-source-limitation-characterization'
        value.update(case_classification=classification, positive_viewport_accepted=False, untouched_baseline_installed=BASELINE_INSTALLED, baseline_evidence=copy.deepcopy(BASELINE_EVIDENCE))
        def geometry(width, height, tag=None):
            return dict(width=width, height=height, measured_width=width, measured_height=height,
                        raw=[0, 0, width, height], visible=[0, 0, width, height],
                        layout_width=-1, layout_height=-2, tag=tag)
        observations.extend([
            dict(kind='colour-limitation-characterization', classification=classification,
                 positive_viewport_accepted=False, untouched_baseline_installed=BASELINE_INSTALLED, baseline_evidence=copy.deepcopy(BASELINE_EVIDENCE), device_sdk=35, font_scale=1,
                 display=geometry(640, 320), dialog=geometry(384, 240), holder=geometry(360, 120),
                 holder_parent=geometry(360, 120), inner=geometry(360, 0), inner_content=geometry(360, 700),
                 fixed=[geometry(100, 40, tag) for tag in ('colour_advanced_tab', 'custom_colours_panel', 'add_custom_colour')]),
            dict(kind='colour-limitation-cancelled', commit_callbacks=0, closed_callbacks=1, dialog_showing=False,
                 positive_viewport_accepted=False, untouched_baseline_installed=BASELINE_INSTALLED, baseline_evidence=copy.deepcopy(BASELINE_EVIDENCE))])
    back_labels = ([f'notice-{NOTICE_METHODS[method]}-{action}' for action in ('nested', 'close')]
                   if method in NOTICE_METHODS else
                   ['credit-discard'] if method == 'retainedCreditDialogKeepsDraftSelectionAndNativeListenersAcrossRotation' else [])
    for label in back_labels:
        before = dict(target_attached=True, target_showing=True, target_focused=True)
        after = dict(target_attached=False, target_showing=False, target_focused=False)
        if label.endswith('-nested'):
            before.update(notice_retained=True, notice_focused=False)
            after.update(notice_retained=True, notice_focused=True)
        elif label.endswith('-close'):
            before.update(notice_present=True, editor_focused=False)
            after.update(notice_present=False, editor_focused=True)
        else:
            before.update(dialog_showing=True, save_calls=4, dismiss_calls=1, saved_draft_unchanged=True)
            after.update(dialog_showing=False, save_calls=4, dismiss_calls=2, saved_draft_unchanged=True)
        before.update(target_insets_available=True, target_ime_visible=False, focused_app_window_present=True,
                      focused_app_window_is_target=True, focused_app_window_is_editor=False,
                      focused_insets_available=True, focused_app_window_ime_visible=False)
        after.update(target_insets_available=False, target_ime_visible=None, focused_app_window_present=True,
                     focused_app_window_is_target=False, focused_app_window_is_editor=not label.endswith('-nested'),
                     focused_insets_available=True, focused_app_window_ime_visible=False)
        observations.extend([
            dict(kind='native-back-before', label=label, state=before, postcondition_met=False),
            dict(kind='native-back-injected', label=label, state=copy.deepcopy(after),
                 route='UiDevice.pressKeyCode(KEYCODE_BACK)', keycode=4, injection_count=1, injected=True),
            dict(kind='native-back-after', label=label, state=after, injected=True, completed=True, postcondition_met=True)])
    observations.insert(0, dict(kind='interaction-start', started_uptime_ms=2000, deadline_uptime_ms=47000, budget_ms=45000))
    observations.append(dict(kind='interaction-end', started_uptime_ms=2000, ended_uptime_ms=5000,
                             deadline_uptime_ms=47000, elapsed_ms=3000, budget_ms=45000,
                             block_completed=True, within_deadline=True))
    value.update(fixture_started_uptime_ms=1000, fixture_ended_uptime_ms=6000, fixture_elapsed_ms=5000,
                 fixture_setup_elapsed_ms=1000, fixture_teardown_elapsed_ms=1000,
                 fixture_elapsed_scope='setup+interaction+teardown; excludes export')
    return value


def observation(data, kind):
    return next(o for o in data['observations'] if o['kind'] == kind)


def write_archive(root, method, *, change_receipt=None, change_manifest=None, extra=None, corrupt=False):
    data = receipt(method)
    if change_receipt:
        change_receipt(data)
    files = {'receipt.json': json.dumps(data).encode()}
    files.update({name: PNG + b'synthetic test payload' for name in METHOD_SCREENS[method]})
    manifest = dict(schema=1, owner=OWNER, method=method, device_sdk=35, test_passed=True,
                    files=[dict(path=name, bytes=len(value), sha256=hashlib.sha256(value).hexdigest())
                           for name, value in files.items()])
    if change_manifest:
        change_manifest(manifest)
    if corrupt:
        files['receipt.json'] += b' '
    with zipfile.ZipFile(root / (method + '.zip'), 'w', zipfile.ZIP_DEFLATED) as zipped:
        for name, value in files.items():
            zipped.writestr(name, value)
        zipped.writestr('manifest.json', json.dumps(manifest))
        if extra:
            zipped.writestr(*extra)


class DialogEvidenceTransportTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.exports = self.root / 'exports'
        self.exports.mkdir()
        self.output = self.root / 'output'
        self.summary = self.root / 'summary.json'
        self.summary.write_text(json.dumps(summary()))
        for method in METHOD_SCREENS:
            write_archive(self.exports, method)
        self.method = next(iter(METHOD_SCREENS))

    def test_exact_source_bound_five_case_export_and_atomic_extraction(self):
        result = extract(self.exports, self.output, self.summary)
        self.assertTrue(result['success'])
        self.assertEqual(result['source_tests_sha256'], DIGEST)
        self.assertEqual(len(result['cases']), 5)
        self.assertEqual(len(list(self.output.rglob('*.png'))), 10)
        self.assertEqual(len(list(self.output.rglob('receipt.json'))), 5)
        self.assertEqual(result['large_text_short_landscape_advanced_colour'], 'not-accepted-diagnostic-only')
        self.assertEqual(result['untouched_baseline_installed'], BASELINE_INSTALLED)
        self.assertEqual(result['baseline_evidence'], BASELINE_EVIDENCE)
        self.assertIs(result['positive_colour_viewport_accepted'], False)
        with self.assertRaises(ValueError):
            extract(self.exports, self.output, self.summary)

    def test_missing_extra_or_partial_exports_fail_without_output(self):
        path = self.exports / (self.method + '.zip')
        original = path.read_bytes()
        path.unlink()
        with self.assertRaises(ValueError):
            extract(self.exports, self.output, self.summary)
        path.write_bytes(original)
        (self.exports / 'unexpected.zip').write_bytes(original)
        with self.assertRaises(ValueError):
            extract(self.exports, self.output, self.summary)
        (self.exports / 'unexpected.zip').unlink()
        write_archive(self.exports, self.method, change_manifest=lambda m: m.update(test_passed=False))
        with self.assertRaises(ValueError):
            extract(self.exports, self.output, self.summary)
        self.assertFalse(self.output.exists())

    def test_source_summary_rejects_failed_wrong_sdk_missing_duplicate_and_unbound(self):
        changes = [lambda d: d.update(success=False), lambda d: d.update(device_sdk=30),
                   lambda d: d.update(timed_out=True), lambda d: d.update(returncode=1),
                   lambda d: d.update(source_tests_sha256=None), lambda d: d['cases'].pop(),
                   lambda d: d['cases'].append(copy.deepcopy(d['cases'][0])),
                   lambda d: d['cases'][0].update(status='skipped')]
        for change in changes:
            data = summary()
            change(data)
            with self.subTest(change=change), self.assertRaises(ValueError):
                source_binding(data)

    def test_receipt_rejects_failure_wrong_identity_source_and_missing_screens(self):
        changes = [lambda d: d.update(outcome='failed'), lambda d: d.update(failure='hidden'),
                   lambda d: d.update(device_sdk=30), lambda d: d.update(package='foreign'),
                   lambda d: d.update(test_class='foreign'), lambda d: d.update(test_method='foreign'),
                   lambda d: d.update(source_tests_sha256='b' * 64),
                   lambda d: d.update(source_binding='unbound-needs-host-summary'),
                   lambda d: d.update(screenshots=[]), lambda d: d.update(observations=[])]
        for change in changes:
            data = receipt(self.method)
            change(data)
            with self.subTest(change=change), self.assertRaises(ValueError):
                verify_receipt(data, self.method, DIGEST)

    def test_caption_clipping_bad_geometry_and_offscreen_or_unpaired_pointer_fail(self):
        changes = [lambda d: observation(d, 'intrinsic-caption').update(layout_height=31),
                   lambda d: observation(d, 'intrinsic-caption')['line_metrics'][0].update(ellipsis=1),
                   lambda d: observation(d, 'intrinsic-caption')['line_metrics'][0].update(right=102),
                   lambda d: observation(d, 'caption-line-reached').update(line_rect=[0, 0, 200, 20]),
                   lambda d: observation(d, 'caption-line-reached').update(line_rect=[0, 0, True, 20]),
                   lambda d: observation(d, 'pointer-before').update(tap=[100, 100]),
                   lambda d: d['observations'].remove(observation(d, 'pointer-injected'))]
        for change in changes:
            data = receipt(self.method)
            change(data)
            with self.subTest(change=change), self.assertRaises(ValueError):
                verify_receipt(data, self.method, DIGEST)

    def test_zip_traversal_duplicate_digest_length_and_foreign_records_fail(self):
        changes = [dict(extra=('../escape', b'not extracted')),
                   dict(extra=('receipt.json', b'duplicate')),
                   dict(corrupt=True),
                   dict(change_manifest=lambda m: m['files'][0].update(sha256='0' * 64)),
                   dict(change_manifest=lambda m: m['files'][0].update(bytes=999)),
                   dict(change_manifest=lambda m: m['files'][0].update(path='../escape')),
                   dict(change_manifest=lambda m: m.update(owner='foreign'))]
        for options in changes:
            write_archive(self.exports, self.method, **options)
            with self.subTest(options=options), self.assertRaises(ValueError):
                inspect_archive(self.exports / (self.method + '.zip'), self.method, DIGEST)
        self.assertFalse((self.root / 'escape').exists())

    def test_optimized_cli_rejects_partial_and_clears_stale_receipt(self):
        write_archive(self.exports, self.method, change_manifest=lambda m: m.update(test_passed=False))
        destination = self.root / 'receipt.json'
        script = Path(__file__).with_name('dialog_evidence_transport.py')
        for optimized in ([], ['-O']):
            destination.write_text('{"success":true}')
            result = subprocess.run([sys.executable, *optimized, str(script), str(self.exports),
                '--dialog-summary', str(self.summary), '--output', str(self.output), '--receipt', str(destination)],
                capture_output=True, text=True, timeout=5)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(destination.exists())
            self.assertFalse(self.output.exists())


class NoticeFlowPartitionContractTest(unittest.TestCase):
    """Partition, not weaker acceptance: preserve the original complete loop body.

    The old combined method on head1783e798/run38114313848 remains FAILED:
    interaction elapsed45715 ms, block_completed=false, within_deadline=false.
    Original whole source SHA256:
    651454e20b5bf1b29746ba2616140ce9d2af0f8a2e3f050adf3adf2018a01067
    Original runner source_tests_sha256:
    2891e328738baa1719c9780f4b42d99cc3f96ca8640de9abf5515ad86d2ba356
    Original aboutRowsOpenThreeNoticesWithReachableNativeFooters receipt SHA256:
    289adcf0ca7ce11cdc6814ffd2cbe16b81909ea2a582ac9d40b706f26836ff74
    The normalized original loop-body SHA below excludes only common indentation
    and its outer for-loop wrapper. It retains every original assertion verbatim.
    """
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.source = (cls.root / 'app/src/androidTest/java/paint/anpaint/android/LocalizedDialogDeviceTest.kt').read_text()
        cls.flow = cls.source.split('private fun noticeFlow(index: Int)', 1)[1].split(
            '@Test fun retainedCreditDialogKeepsDraftSelectionAndNativeListenersAcrossRotation()', 1)[0]

    def test_exact_three_index_resource_title_asset_tuples_and_five_sdk35_methods(self):
        expected = {
            'aboutThirdPartyNoticeRetainsRotationAndNativeFooterFlow': 0,
            'aboutArtworkNoticeCompletesNativeFooterFlow': 1,
            'aboutGimpTranslationNoticeCompletesNativeFooterFlow': 2,
        }
        self.assertEqual(NOTICE_METHODS, expected)
        bindings = re.findall(r'@Test fun (\w+)\(\)=noticeFlow\((\d+)\)', self.source)
        self.assertEqual({name: int(index) for name, index in bindings}, expected)
        tuples = re.findall(r'Triple\(R.string.(\w+),R.string.(\w+),"([^"]+)"\)', self.flow)
        self.assertEqual(tuples, [
            ('ui_third_party_notices', 'ui_open_source_credits_and_notices', 'legal/THIRD_PARTY_NOTICES.txt'),
            ('ui_icons_fonts_artwork_credits', 'ui_icons_fonts_artwork_credits', 'legal/ASSET_CREDITS.txt'),
            ('ui_gimp_translations31', 'ui_gimp_translations31', 'legal/GIMP_TRANSLATION_NOTICES.txt')])
        self.assertIn('=fixture("fr",2f)', self.flow)
        self.assertIn('val entry=cases[index]', self.flow)
        self.assertEqual(set(re.findall(r'@Test fun (\w+)\(', self.source)), set(METHOD_SCREENS))
        rule = (self.root / 'app/src/androidTest/java/paint/anpaint/android/DialogEvidenceExportRule.kt').read_text()
        whitelist = rule.split('val METHODS=setOf(', 1)[1].split(')', 1)[0]
        self.assertEqual(set(re.findall(r'"(\w+)"', whitelist)), set(METHOD_SCREENS))
        from run_android_instrumentation import declared_tests
        directory = self.root / 'app/src/androidTest'
        self.assertEqual({name for owner, name in declared_tests(directory, sdk_level=35) if owner == TEST_CLASS}, set(METHOD_SCREENS))
        self.assertFalse({name for owner, name in declared_tests(directory, sdk_level=30) if owner == TEST_CLASS})

    def test_complete_original_notice_flow_and_first_case_rotations_are_preserved(self):
        body = self.flow.split('        openAbout()', 1)[1].rsplit('\n    }', 1)[0]
        normalized = textwrap.dedent('        openAbout()' + body) + '\n'
        self.assertEqual(hashlib.sha256(normalized.encode()).hexdigest(),
            'a04a779411a0bfbefaaa37e8af1ffabb2d5235895becb43bc24d15b299c4bc04')
        # Cases 1/2 formerly inherited landscape from case 0. Each new independent
        # fixture establishes the same orientation before opening its real menu.
        self.assertLess(self.flow.index('if(index!=0) orient(true,scenario)'), self.flow.index('openAbout()'))
        self.assertEqual(normalized.count('if(index==0)'), 2)
        self.assertEqual(normalized.count('orient(true,scenario)'), 2)
        self.assertEqual(normalized.count('orient(false,scenario)'), 1)
        for required in ('Retain the real About chooser across rotation', 'Keep the same legal dialog after real rotation',
                         'tap("notice copy"', 'tap("other terms"', 'tap("notice done"',
                         'nativeBack("notice-$index-nested"', 'nativeBack("notice-$index-close"',
                         'openAbout();tapRow(', 'assertEquals(expected,clipboard.primaryClip',
                         'assertEquals("Actual menu callback loaded the bundled notice",expected,'):
            self.assertIn(required, normalized)

    def test_exact_ten_pngs_keep_original_states_with_per_method_capture_indices(self):
        self.assertEqual([METHOD_SCREENS[name] for name in NOTICE_METHODS], [
            ['0-about-portrait.png', '1-about-landscape.png', '2-notice-0-initial.png', '3-notice-0-portrait.png'],
            ['0-notice-1-initial.png'], ['0-notice-2-initial.png']])
        self.assertEqual(len(METHOD_SCREENS), 5)
        self.assertEqual(sum(map(len, METHOD_SCREENS.values())), 10)
        self.assertEqual(len(METHOD_SCREENS['retainedCreditDialogKeepsDraftSelectionAndNativeListenersAcrossRotation']), 2)
        self.assertEqual(len(METHOD_SCREENS['unchangedAdvancedColourReportsShortLandscapeLimitation']), 2)

    def test_each_notice_requires_its_own_copy_nested_back_done_reopen_and_close_back(self):
        for method, index in NOTICE_METHODS.items():
            verify_receipt(receipt(method), method, DIGEST)
            mutations = [lambda r: observation(r, 'native-back-after').update(label='notice-99-nested'),
                         lambda r: r['observations'].remove(observation(r, 'native-back-after')),
                         lambda r: r.update(screenshots=METHOD_SCREENS[next(m for m in NOTICE_METHODS if m != method)]),
                         lambda r: r.update(test_method='aboutRowsOpenThreeNoticesWithReachableNativeFooters')]
            for mutate in mutations:
                data = receipt(method); mutate(data)
                with self.subTest(method=method, mutate=mutate), self.assertRaises(ValueError):
                    verify_receipt(data, method, DIGEST)
            for label in ('notice copy', 'other terms', 'notice done'):
                data = receipt(method)
                data['observations'] = [o for o in data['observations'] if o.get('label') != label]
                with self.subTest(method=method, label=label), self.assertRaises(ValueError):
                    verify_receipt(data, method, DIGEST)
        data = summary()
        data['cases'][0]['name'] = 'aboutRowsOpenThreeNoticesWithReachableNativeFooters'
        with self.assertRaises(ValueError):
            source_binding(data)


class NativeBackAndInteractionBudgetContractTest(unittest.TestCase):
    """Source contracts + synthetic receipts, not proof of installed key delivery.

    Primary source: Google Maven androidx.test.uiautomator:uiautomator:2.2.0.
    https://dl.google.com/dl/android/maven2/androidx/test/uiautomator/uiautomator/2.2.0/uiautomator-2.2.0-sources.jar
    JAR SHA256 e1f438106ac0d26b80ecf4fd6ffe6d36f60e12bdcd6316903f802ed24d00be99
    UiDevice.java SHA256 19a43983f6b75bb1690cb6b196873c24155cda3d6723d2d2df947896cefd8ffe
    InteractionController.java SHA256 a549156dafb4e9fd6d5fea605e7f8945a066e45b0f7a5f0539b6e6077e48afe1
    UiDevice.pressBack350 -> sendKeyAndWaitForEvent188 waits for content-change;
    pressKeyCode458 -> sendKey578 returns true only if native DOWN and UP inject.
    Exact original run38112218904 logcat timeout lines (the bodies remained failed):
    10-11 04:53:24.646  5673  5738 W InteractionController: runAndwaitForEvents timed out waiting for events
    10-11 04:53:45.534  5673  5738 W InteractionController: runAndwaitForEvents timed out waiting for events
    """
    @classmethod
    def setUpClass(cls):
        cls.source = (Path(__file__).resolve().parents[1] /
            'app/src/androidTest/java/paint/anpaint/android/LocalizedDialogDeviceTest.kt').read_text()

    def test_single_native_key_pair_has_before_and_finally_state_before_cleanup(self):
        source = self.source
        helper = source.split('private fun nativeBack(', 1)[1].split('/** Same native SystemUI', 1)[0]
        self.assertEqual(helper.count('device.pressKeyCode(KeyEvent.KEYCODE_BACK)'), 1)
        self.assertNotIn('device.pressBack()', source)
        for forbidden in ('repeat(', 'while(', 'performClick(', 'onBackPressed(', '.dismiss()', 'sendKeyDownUpSync', 'executeShellCommand'):
            self.assertNotIn(forbidden, helper)
        for required in ('"native-back-before"', '"native-back-injected"', '"native-back-after"',
                         'assertTrue("Native Back DOWN/UP injection succeeded",injected==true)',
                         'await("native Back outcome: $label",condition)', '.put("injection_count",1)',
                         'assertFalse("Back must establish a new app outcome",onMain(condition))'):
            self.assertIn(required, helper)
        self.assertLess(helper.index('"native-back-before"'), helper.index('device.pressKeyCode'))
        self.assertLess(helper.index('device.pressKeyCode'), helper.index('"native-back-injected"'))
        self.assertLess(helper.index('} finally {'), helper.index('"native-back-after"'))
        self.assertIn('!nested.isAttachedToWindow && termsRoot()===root && root.hasWindowFocus()', source)
        self.assertIn('WindowInspector.getGlobalWindowViews().lastOrNull {it.hasWindowFocus()}', source)
        self.assertIn('targetInsets?.isVisible(WindowInsets.Type.ime()) ?: JSONObject.NULL', source)
        self.assertIn('focusedInsets?.isVisible(WindowInsets.Type.ime()) ?: JSONObject.NULL', source)
        self.assertIn('hideSoftInputFromWindow(next.windowToken,0)', source)
        credit = source.split('nativeBack("credit-discard"', 1)[1].split('} finally {onMain {reopened.dismiss()}}', 1)[0]
        self.assertIn('calls==4 && dismissed==2 && saved==draft', credit)
        self.assertIn('assertEquals(4,calls);assertEquals(2,dismissed);assertEquals(draft,saved)', credit)

    def test_back_receipt_requires_one_injection_and_positive_pre_cleanup_outcome(self):
        methods = [next(iter(NOTICE_METHODS)), 'retainedCreditDialogKeepsDraftSelectionAndNativeListenersAcrossRotation']
        mutations = [lambda r: observation(r, 'native-back-injected').update(injected=False),
                     lambda r: observation(r, 'native-back-injected').update(injection_count=2),
                     lambda r: observation(r, 'native-back-injected').update(injection_count=True),
                     lambda r: observation(r, 'native-back-injected').update(route='UiDevice.pressBack()'),
                     lambda r: observation(r, 'native-back-before').update(postcondition_met=True),
                     lambda r: observation(r, 'native-back-before')['state'].update(target_focused=False),
                     lambda r: observation(r, 'native-back-after').update(completed=False),
                     lambda r: observation(r, 'native-back-after').update(postcondition_met=False),
                     lambda r: observation(r, 'native-back-after')['state'].update(target_attached=True),
                     lambda r: r['observations'].remove(observation(r, 'native-back-after')),
                     lambda r: r['observations'].append(copy.deepcopy(observation(r, 'native-back-injected')))]
        for method in methods:
            verify_receipt(receipt(method), method, DIGEST)
            for mutate in mutations:
                data = receipt(method); mutate(data)
                with self.subTest(method=method, mutate=mutate), self.assertRaises(ValueError):
                    verify_receipt(data, method, DIGEST)
        for field, value in [('save_calls', 5), ('dismiss_calls', 1), ('dismiss_calls', 3),
                             ('saved_draft_unchanged', False), ('dialog_showing', True)]:
            data = receipt(methods[1]); observation(data, 'native-back-after')['state'][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                verify_receipt(data, methods[1], DIGEST)
        data = receipt(methods[0]); observation(data, 'native-back-after')['state']['notice_focused'] = False
        with self.assertRaises(ValueError):
            verify_receipt(data, methods[0], DIGEST)

    def test_ime_diagnostics_do_not_substitute_for_positive_dialog_cancellation(self):
        method = 'retainedCreditDialogKeepsDraftSelectionAndNativeListenersAcrossRotation'
        # One Back can close the IME while leaving the credit dialog open. Record
        # that honestly and reject it; never inject another Back as a fallback.
        data = receipt(method)
        observation(data, 'native-back-before')['state'].update(target_ime_visible=True, focused_app_window_ime_visible=True)
        observation(data, 'native-back-after')['state'].update(target_attached=True, target_showing=True,
            dialog_showing=True, dismiss_calls=1, focused_app_window_is_target=True, focused_app_window_is_editor=False)
        observation(data, 'native-back-after').update(completed=False, postcondition_met=False)
        with self.assertRaises(ValueError):
            verify_receipt(data, method, DIGEST)
        for field in ('target_ime_visible', 'focused_app_window_ime_visible', 'focused_app_window_present'):
            data = receipt(method); observation(data, 'native-back-before')['state'].pop(field)
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_receipt(data, method, DIGEST)

    def test_back_cleanup_state_or_duplicate_late_event_cannot_supply_acceptance(self):
        method = 'retainedCreditDialogKeepsDraftSelectionAndNativeListenersAcrossRotation'
        data = receipt(method)
        after = observation(data, 'native-back-after')
        data['observations'].remove(after)
        data['observations'].append(after)
        with self.assertRaises(ValueError):
            verify_receipt(data, method, DIGEST)

    def test_whole_interval_boundaries_separate_setup_and_teardown(self):
        method = next(iter(METHOD_SCREENS))
        for elapsed in (0, 44999, 45000):
            data = receipt(method)
            observation(data, 'interaction-end').update(ended_uptime_ms=2000 + elapsed, elapsed_ms=elapsed)
            data.update(fixture_ended_uptime_ms=3000 + elapsed, fixture_elapsed_ms=2000 + elapsed)
            verify_receipt(data, method, DIGEST)
        # Even a fully successful final action one millisecond late must fail;
        # there is deliberately no await/checkDeadline after that synthetic action.
        for elapsed in (45001, 50000):
            data = receipt(method)
            observation(data, 'interaction-end').update(ended_uptime_ms=2000 + elapsed, elapsed_ms=elapsed)
            data.update(fixture_ended_uptime_ms=3000 + elapsed, fixture_elapsed_ms=2000 + elapsed)
            with self.subTest(elapsed=elapsed), self.assertRaises(ValueError):
                verify_receipt(data, method, DIGEST)

    def test_unfinished_malformed_or_inconsistent_timing_fails_closed(self):
        method = next(iter(METHOD_SCREENS))
        mutations = [lambda r: observation(r, 'interaction-end').update(block_completed=False),
                     lambda r: observation(r, 'interaction-end').update(within_deadline=False),
                     lambda r: observation(r, 'interaction-end').update(elapsed_ms=1),
                     lambda r: observation(r, 'interaction-end').update(ended_uptime_ms=True),
                     lambda r: observation(r, 'interaction-end').update(deadline_uptime_ms=99999),
                     lambda r: observation(r, 'interaction-start').update(budget_ms=60000),
                     lambda r: r['observations'].remove(observation(r, 'interaction-end')),
                     lambda r: r['observations'].append(copy.deepcopy(observation(r, 'interaction-end'))),
                     lambda r: r.update(fixture_elapsed_ms=3000),
                     lambda r: r.update(fixture_setup_elapsed_ms=True),
                     lambda r: r.update(fixture_teardown_elapsed_ms=0),
                     lambda r: r.update(fixture_elapsed_scope='interaction only')]
        for mutate in mutations:
            data = receipt(method); mutate(data)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                verify_receipt(data, method, DIGEST)

    def test_kotlin_records_and_asserts_final_whole_interval_before_reset(self):
        source = self.source
        fixture = source.split('private fun fixture(', 1)[1].split('private fun interaction(', 1)[0]
        self.assertLess(fixture.index('interaction {'), fixture.index('await("initial editor")'))
        self.assertLess(fixture.index('block(launched)'), fixture.index('deadline=Long.MAX_VALUE'))
        helper = source.split('private fun interaction(', 1)[1].split('private fun backWindowState', 1)[0]
        self.assertIn('deadline=started+45000', helper)
        self.assertIn('try {block();completed=true} finally {', helper)
        self.assertLess(helper.index('ended=SystemClock.uptimeMillis()'), helper.index('"interaction-end"'))
        self.assertLess(helper.index('"interaction-end"'), helper.index('assertTrue("Entire dialog interaction'))
        self.assertIn('ended<=deadline)', helper)
        self.assertNotIn('deadline=Long.MAX_VALUE', helper)
        rule = (Path(__file__).resolve().parents[1] /
            'app/src/androidTest/java/paint/anpaint/android/DialogEvidenceExportRule.kt').read_text()
        self.assertIn('"fixture_setup_elapsed_ms"', rule)
        self.assertIn('"fixture_teardown_elapsed_ms"', rule)
        self.assertIn('"setup+interaction+teardown; excludes export"', rule)


class EvidenceCachePathContractTest(unittest.TestCase):
    """Host filesystem model + exact Kotlin source contracts, not Android execution."""
    @staticmethod
    def confined(root, candidate):
        expected = candidate.absolute()
        actual = candidate.resolve()
        if candidate.is_symlink() or actual != expected or actual == root or not actual.is_relative_to(root):
            raise ValueError(f'Linked or escaping child: expected={expected} actual={actual} root={root}')

    @classmethod
    def case_directory(cls, supplied_cache, method):
        if method not in METHOD_SCREENS:
            raise ValueError('Unknown method')
        # Mirrors the narrow trust boundary: only the platform cache root may alias.
        root = supplied_cache.resolve(strict=True)
        if not root.is_dir():
            raise ValueError('Missing cache')
        container = root / 'dialog-evidence'
        case = container / method
        cls.confined(root, container)
        cls.confined(root, case)
        return root, case

    @classmethod
    def files(cls, root, directory):
        cls.confined(root, root / 'dialog-evidence')
        cls.confined(root, directory)
        files = sorted(directory.iterdir())
        if len(files) > 21 or sum(f.stat().st_size for f in files if f.exists()) > 24 * 1024 * 1024:
            raise ValueError('Unbounded evidence')
        for file in files:
            if file.name != 'receipt.json' and not re.fullmatch(r'[0-9]+-[A-Za-z0-9_-]+\.png', file.name):
                raise ValueError('Unknown evidence file')
            cls.confined(root, file)
            if not file.is_file() or file.stat().st_size > 2 * 1024 * 1024:
                raise ValueError('Nonregular or oversized child')
        return files

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.cache = self.root / 'actual-cache'
        self.cache.mkdir()
        self.alias = self.root / 'platform-cache-alias'
        self.alias.symlink_to(self.cache, target_is_directory=True)
        self.method = next(iter(METHOD_SCREENS))

    def test_platform_root_alias_is_normalized_before_private_children(self):
        # This is the old guard's false positive, reproduced on a real host symlink.
        old = self.alias / 'dialog-evidence' / self.method
        self.assertNotEqual(old.absolute(), old.resolve())
        root, directory = self.case_directory(self.alias, self.method)
        self.assertEqual(root, self.cache)
        self.assertEqual(directory, self.cache / 'dialog-evidence' / self.method)
        directory.mkdir(parents=True)
        (directory / 'receipt.json').write_text('{}')
        (directory / '0-fixture.png').write_bytes(b'synthetic image')
        self.assertEqual(len(self.files(root, directory)), 2)
        self.assertEqual(self.case_directory(self.cache, self.method), (root, directory))

    def test_attacker_container_or_method_symlink_fails_inside_outside_and_dangling(self):
        inside = self.cache / 'other-owned-directory'
        outside = self.root / 'unrelated'
        inside.mkdir(); outside.mkdir()
        for position in ('container', 'method'):
            for target in (inside, outside, self.root / 'missing'):
                with self.subTest(position=position, target=target):
                    container = self.cache / 'dialog-evidence'
                    if position == 'method':
                        container.mkdir()
                    link = container if position == 'container' else container / self.method
                    link.symlink_to(target, target_is_directory=True)
                    try:
                        with self.assertRaises(ValueError):
                            self.case_directory(self.alias, self.method)
                    finally:
                        link.unlink()
                        if position == 'method':
                            container.rmdir()

    def test_attacker_evidence_file_symlink_cannot_be_read_or_cleaned(self):
        root, directory = self.case_directory(self.alias, self.method)
        directory.mkdir(parents=True)
        sentinel = self.root / 'unrelated-sentinel'
        sentinel.write_text('must survive')
        inside = self.cache / 'other-file'
        inside.write_text('also unrelated')
        for target in (sentinel, inside, self.root / 'missing'):
            link = directory / 'receipt.json'
            link.symlink_to(target)
            try:
                with self.subTest(target=target), self.assertRaises(ValueError):
                    self.files(root, directory)
            finally:
                link.unlink()
        self.assertEqual(sentinel.read_text(), 'must survive')
        self.assertEqual(inside.read_text(), 'also unrelated')

    def test_bounded_flat_inventory_rejects_nested_directory_and_extra_files(self):
        root, directory = self.case_directory(self.alias, self.method)
        directory.mkdir(parents=True)
        nested = directory / '0-nested.png'
        nested.mkdir()
        (nested / 'sentinel').write_text('never recurse')
        with self.assertRaises(ValueError):
            self.files(root, directory)
        self.assertEqual((nested / 'sentinel').read_text(), 'never recurse')
        (nested / 'sentinel').unlink(); nested.rmdir()
        for index in range(22):
            (directory / f'{index}-fixture.png').write_text('synthetic')
        with self.assertRaises(ValueError):
            self.files(root, directory)
        self.assertEqual(len(list(directory.iterdir())), 22)

    def test_kotlin_normalizes_only_trusted_root_and_keeps_all_confinement_guards(self):
        source = (Path(__file__).resolve().parents[1] /
            'app/src/androidTest/java/paint/anpaint/android/DialogEvidenceExportRule.kt').read_text()
        self.assertLess(source.index('cacheRoot=requestedCache.canonicalFile'),
                        source.index('directory=File(cacheRoot,"dialog-evidence/${description.methodName}")'))
        self.assertIn('check(!Files.isSymbolicLink(file.toPath()) && actual==expected &&', source)
        self.assertIn('actual.toPath().startsWith(cacheRoot.toPath()) && actual!=cacheRoot', source)
        self.assertIn('checkConfined(File(cacheRoot,"dialog-evidence"));checkConfined(directory)', source)
        self.assertIn('return File(directory,name).also {checkConfined(it)}', source)
        self.assertIn('files.size<=21 && files.sumOf {it.length()}<=MAX_CASE', source)
        self.assertIn('file==evidenceFile(file.name) && file.isFile && file.length() in 0..MAX_FILE', source)
        self.assertIn('expected=$expected actual=$actual root=$cacheRoot', source)
        self.assertIn('val file=evidenceFile(name)', source)
        self.assertIn('evidenceFile("receipt.json").writeText', source)
        self.assertNotIn('deleteRecursively', source)
        cleanup = source.split('private fun clearEvidenceDirectory()', 1)[1].split('private fun export', 1)[0]
        self.assertLess(cleanup.index('val files=evidenceFiles()'), cleanup.index('files.forEach'))
        # Root normalization must not weaken provenance or permit alternate methods.
        self.assertIn('check(description.methodName in METHODS)', source)
        self.assertIn('getString("anpaint_source_tests_sha256")', source)
        self.assertIn('"source_tests_sha256",supplied ?: JSONObject.NULL', source)


class ClipboardOverlayFixtureContractTest(unittest.TestCase):
    """Source-bound fixture contracts, not a substitute for actual input delivery."""
    @classmethod
    def setUpClass(cls):
        cls.source = (Path(__file__).resolve().parents[1] /
            'app/src/androidTest/java/paint/anpaint/android/LocalizedDialogDeviceTest.kt').read_text()

    def test_sentinel_preview_is_dismissed_before_the_original_native_copy(self):
        source = self.source
        start = source.index('setPrimaryClip(ClipData.newPlainText("Synthetic dialog test","copy has not run"))')
        dismiss = source.index('dismissClipboardOverlay("notice-sentinel",waitForAppearance=true)', start)
        tap = source.index('tap("notice copy"', start)
        exact_clip = source.index('assertEquals(expected,clipboard.primaryClip!!.getItemAt(0).text.toString())', tap)
        after_copy = source.index('dismissClipboardOverlay("notice-copy",waitForAppearance=true)', tap)
        more = source.index('tap("other terms"', tap)
        self.assertLess(start, dismiss)
        self.assertLess(dismiss, tap)
        self.assertLess(tap, exact_clip)
        self.assertLess(exact_clip, after_copy)
        self.assertLess(after_copy, more)

    def test_real_credit_copy_assertions_precede_preview_dismissal_and_original_done(self):
        source = self.source
        copy = source.index('tap("credit copy"')
        check = source.index('assertEquals(3,calls);assertEquals(draft,saved)', copy)
        dismiss = source.index('dismissClipboardOverlay("credit-copy",waitForAppearance=true)', copy)
        done = source.index('tap("credit done"', copy)
        self.assertLess(copy, check)
        self.assertLess(check, dismiss)
        self.assertLess(dismiss, done)
        self.assertIn('assertEquals(4,calls);assertEquals(2,dismissed);assertEquals(draft,saved)', source)
        self.assertIn('assertEquals(3,field.selectionStart);assertEquals(8,field.selectionEnd)', source)

    def test_dismissal_uses_systemui_only_and_waits_for_both_content_and_input_window(self):
        helper = self.source.split('private fun dismissClipboardOverlay(', 1)[1].split('private fun openAbout()', 1)[0]
        for required in ('minOf(deadline,SystemClock.uptimeMillis()+10000)',
                         'By.res("com.android.systemui","clipboard_ui")',
                         'By.res("com.android.systemui","dismiss_button")',
                         'device.click(bounds.centerX(),bounds.centerY())',
                         'device.wait(Until.gone(selector),remaining())',
                         'assertFalse("Clipboard input window disappears",showing())',
                         '"clipboard-overlay-before"', '"clipboard-overlay-native-dismiss"',
                         '"clipboard-overlay-after"'):
            self.assertIn(required, helper)
        for forbidden in ('performClick(', 'dispatchTouchEvent(', 'executeShellCommand',
                          'settings put', 'device_config', 'pressBack(', 'setPrimaryClip(', 'clearPrimaryClip('):
            self.assertNotIn(forbidden, helper)
        # Fixture setup/restoration may create previews too; neither alters the
        # acceptance test's application behavior or the real clipboard contents.
        self.assertIn('dismissClipboardOverlay("fixture-ready")', self.source)
        self.assertIn('dismissClipboardOverlay("fixture-restored",waitForAppearance=clipboardSnapshotted && originalClip!=null)', self.source)

    def test_system_window_can_cover_an_app_visible_target(self):
        # The app rectangle/tap are exact receipt values; the overlay rectangle
        # below is an illustrative occlusion model, not measured SystemUI bounds.
        # App-local visibility cannot account for a separate system input window.
        app_copy = [47, 224, 180, 272]
        illustrative_overlay_region = [0, 200, 264, 300]
        tap = [113, 248]
        def inside(bounds, point):
            return bounds[0] <= point[0] < bounds[2] and bounds[1] <= point[1] < bounds[3]
        self.assertTrue(inside(app_copy, tap))
        self.assertTrue(inside(illustrative_overlay_region, tap))


class ColourLimitationScopeContractTest(unittest.TestCase):
    method = 'unchangedAdvancedColourReportsShortLandscapeLimitation'

    def test_collector_rejects_positive_or_baseline_claims_and_wrong_observed_limitation(self):
        mutations = [lambda r: r.update(positive_viewport_accepted=True),
                     lambda r: r.update(untouched_baseline_installed='passed'),
                     lambda r: r.update(case_classification='repaired'),
                     lambda r: observation(r, 'colour-limitation-characterization').update(font_scale=2),
                     lambda r: observation(r, 'colour-limitation-characterization').update(font_scale=True),
                     lambda r: observation(r, 'colour-limitation-characterization').update(device_sdk=30),
                     lambda r: observation(r, 'colour-limitation-characterization')['display'].update(height=321),
                     lambda r: observation(r, 'colour-limitation-characterization')['inner'].update(height=10),
                     lambda r: observation(r, 'colour-limitation-characterization').update(fixed=[]),
                     lambda r: observation(r, 'colour-limitation-cancelled').update(commit_callbacks=1),
                     lambda r: observation(r, 'colour-limitation-cancelled').update(closed_callbacks=2),
                     lambda r: observation(r, 'colour-limitation-cancelled').update(closed_callbacks=True),
                     lambda r: observation(r, 'colour-limitation-cancelled').update(dialog_showing=True)]
        for mutate in mutations:
            data = receipt(self.method)
            mutate(data)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                verify_receipt(data, self.method, DIGEST)

    def test_current_verified_baseline_evidence_is_exact_and_shared_by_kotlin_exporter(self):
        self.assertEqual(BASELINE_INSTALLED, 'verified-original-positive-failure')
        self.assertEqual(BASELINE_EVIDENCE['run_id'], 38112708313)
        self.assertEqual(BASELINE_EVIDENCE['source_commit'], 'cecce0626dc730ba89120936b66de88e1c990335')
        self.assertEqual(BASELINE_EVIDENCE['production_commit'], '691f8870649a1d21d1441f4e3d0e795660b23e9a')
        self.assertIn('/8096234be003cd6a287660d32884c2541c518e65/', BASELINE_EVIDENCE['evidence_url'])
        self.assertEqual(BASELINE_EVIDENCE['source_binding_sha256'],
                         'd4072ad9c2b72403663e50ed6205f35c53ce7aaab2133d538f02f577d6835ea3')
        self.assertEqual(BASELINE_EVIDENCE['receipt_sha256'],
                         '03f20e26ac1d33be758bccc161c11e27a549bf917217ec7d4edcad23778080c2')
        root = Path(__file__).resolve().parents[1]
        rule = (root / 'app/src/androidTest/java/paint/anpaint/android/DialogEvidenceExportRule.kt').read_text()
        metadata = rule.split('fun verifiedColourBaseline()=JSONObject()', 1)[1].split('const val OWNER=', 1)[0]
        kotlin = dict(re.findall(r'\.put\("([^"]+)","([^"]+)"\)', metadata))
        kotlin['run_id'] = int(re.search(r'\.put\("run_id",(\d+)L\)', metadata)[1])
        self.assertEqual(kotlin, BASELINE_EVIDENCE)
        self.assertIn('const val BASELINE_INSTALLED="verified-original-positive-failure"', rule)
        source = (root / 'app/src/androidTest/java/paint/anpaint/android/LocalizedDialogDeviceTest.kt').read_text()
        self.assertEqual(source.count('.put("baseline_evidence",DialogEvidenceExportRule.verifiedColourBaseline())'), 2)
        self.assertIn('.put("baseline_evidence",verifiedColourBaseline())', rule)
        data = receipt(self.method)
        verify_receipt(data, self.method, DIGEST)
        self.assertIs(data['positive_viewport_accepted'], False)

    def test_stale_missing_foreign_or_changed_baseline_provenance_is_rejected_everywhere(self):
        for kind in (None, 'colour-limitation-characterization', 'colour-limitation-cancelled'):
            def target(data):
                return data if kind is None else observation(data, kind)
            for marker in ('pending', 'passed', True, None):
                data = receipt(self.method); target(data)['untouched_baseline_installed'] = marker
                with self.subTest(kind=kind, marker=marker), self.assertRaises(ValueError):
                    verify_receipt(data, self.method, DIGEST)
            for field in BASELINE_EVIDENCE:
                data = receipt(self.method)
                target(data)['baseline_evidence'][field] = 'foreign'
                with self.subTest(kind=kind, field=field), self.assertRaises(ValueError):
                    verify_receipt(data, self.method, DIGEST)
            for evidence in (None, {}, {**BASELINE_EVIDENCE, 'extra': 'unverified'},
                             {**BASELINE_EVIDENCE, 'run_id': float(BASELINE_EVIDENCE['run_id'])}):
                data = receipt(self.method); target(data)['baseline_evidence'] = evidence
                with self.subTest(kind=kind, evidence=evidence), self.assertRaises(ValueError):
                    verify_receipt(data, self.method, DIGEST)

    def test_collector_requires_exact_separate_five_method_phase(self):
        data = summary()
        data['cases'].append(dict(classname='paint.anpaint.android.EditorDeviceTest', name='extra', status='passed'))
        with self.assertRaises(ValueError):
            source_binding(data)
        for field, value in [('expected_tests', 19), ('completed_tests', 2), ('included_tests', []),
                             ('missing', ['missing']), ('unexpected', ['extra']), ('errors', ['error'])]:
            data = summary(); data[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                source_binding(data)


    def test_current_characterization_emits_geometry_before_known_limitation_assertion(self):
        source = (Path(__file__).resolve().parents[1] / 'app/src/androidTest/java/paint/anpaint/android/LocalizedDialogDeviceTest.kt').read_text()
        block = source.split('fun unchangedAdvancedColourReportsShortLandscapeLimitation()', 1)[1].split('private fun colourGeometry', 1)[0]
        self.assertLess(block.index('"colour-limitation-characterization"'), block.index('0,inner.height)'))
        for text in ('640,display.width', '320,display.height', '1f,activity.resources.configuration.fontScale',
                     '"holder_parent",colourGeometry(holder.parent as View)', '"inner_content",colourGeometry(inner.getChildAt(0))',
                     'evidence.capture("colour-limitation")', 'evidence.capture("colour-cancelled")',
                     'tap("colour cancel"', 'assertEquals(0,committed);assertEquals(1,closed)',
                     '"positive_viewport_accepted",false', '"untouched_baseline_installed",DialogEvidenceExportRule.BASELINE_INSTALLED'):
            self.assertIn(text, block)
        self.assertNotIn('@Test fun normalAdvancedColourKeepsFiniteViewportAndFixedControls()', source)


if __name__ == '__main__':
    unittest.main()
