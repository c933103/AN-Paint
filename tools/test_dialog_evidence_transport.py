"""Synthetic archive contracts; these are not installed-device test results."""
import copy
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from dialog_evidence_transport import (METHOD_SCREENS, OWNER, TEST_CLASS, PNG,
    extract, inspect_archive, source_binding, verify_receipt)

DIGEST = 'a' * 64


def summary():
    return dict(success=True, device_sdk=35, timed_out=False, returncode=0,
                source_tests_sha256=DIGEST, expected_tests=3, completed_tests=3, missing=[], unexpected=[], errors=[],
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
        value.update(case_classification=classification, positive_viewport_accepted=False, untouched_baseline_installed='pending')
        def geometry(width, height, tag=None):
            return dict(width=width, height=height, measured_width=width, measured_height=height,
                        raw=[0, 0, width, height], visible=[0, 0, width, height],
                        layout_width=-1, layout_height=-2, tag=tag)
        observations.extend([
            dict(kind='colour-limitation-characterization', classification=classification,
                 positive_viewport_accepted=False, untouched_baseline_installed='pending', device_sdk=35, font_scale=1,
                 display=geometry(640, 320), dialog=geometry(384, 240), holder=geometry(360, 120),
                 holder_parent=geometry(360, 120), inner=geometry(360, 0), inner_content=geometry(360, 700),
                 fixed=[geometry(100, 40, tag) for tag in ('colour_advanced_tab', 'custom_colours_panel', 'add_custom_colour')]),
            dict(kind='colour-limitation-cancelled', commit_callbacks=0, closed_callbacks=1, dialog_showing=False,
                 positive_viewport_accepted=False, untouched_baseline_installed='pending')])
    return value


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

    def test_exact_source_bound_three_case_export_and_atomic_extraction(self):
        result = extract(self.exports, self.output, self.summary)
        self.assertTrue(result['success'])
        self.assertEqual(result['source_tests_sha256'], DIGEST)
        self.assertEqual(len(result['cases']), 3)
        self.assertEqual(len(list(self.output.rglob('*.png'))), 10)
        self.assertEqual(len(list(self.output.rglob('receipt.json'))), 3)
        self.assertEqual(result['large_text_short_landscape_advanced_colour'], 'not-accepted-diagnostic-only')
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
        changes = [lambda d: d['observations'][0].update(layout_height=31),
                   lambda d: d['observations'][0]['line_metrics'][0].update(ellipsis=1),
                   lambda d: d['observations'][0]['line_metrics'][0].update(right=102),
                   lambda d: d['observations'][1].update(line_rect=[0, 0, 200, 20]),
                   lambda d: d['observations'][1].update(line_rect=[0, 0, True, 20]),
                   lambda d: d['observations'][2].update(tap=[100, 100]),
                   lambda d: d['observations'].pop(3)]
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
                     lambda r: r['observations'][-2].update(font_scale=2),
                     lambda r: r['observations'][-2].update(font_scale=True),
                     lambda r: r['observations'][-2].update(device_sdk=30),
                     lambda r: r['observations'][-2]['display'].update(height=321),
                     lambda r: r['observations'][-2]['inner'].update(height=10),
                     lambda r: r['observations'][-2].update(fixed=[]),
                     lambda r: r['observations'][-1].update(commit_callbacks=1),
                     lambda r: r['observations'][-1].update(closed_callbacks=2),
                     lambda r: r['observations'][-1].update(closed_callbacks=True),
                     lambda r: r['observations'][-1].update(dialog_showing=True)]
        for mutate in mutations:
            data = receipt(self.method)
            mutate(data)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                verify_receipt(data, self.method, DIGEST)

    def test_collector_requires_exact_separate_three_method_phase(self):
        data = summary()
        data['cases'].append(dict(classname='paint.anpaint.android.EditorDeviceTest', name='extra', status='passed'))
        with self.assertRaises(ValueError):
            source_binding(data)
        for field, value in [('expected_tests', 19), ('completed_tests', 2), ('included_tests', []),
                             ('missing', ['missing']), ('unexpected', ['extra']), ('errors', ['error'])]:
            data = summary(); data[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                source_binding(data)

    def test_original_positive_method_and_whole_source_are_preserved_verbatim(self):
        directory = Path(__file__).resolve().parents[1] / 'verification/localized-dialog-layout-2026-10-11/colour-separate-scope'
        identity = json.loads((directory / 'source-identity.json').read_text())
        full = (directory / identity['whole_source_file']).read_bytes()
        positive = (directory / identity['positive_method_file']).read_bytes()
        self.assertEqual(hashlib.sha256(full).hexdigest(), identity['whole_source_sha256'])
        self.assertEqual(hashlib.sha1(('blob %s\0' % len(full)).encode() + full).hexdigest(), identity['original_source_git_blob'])
        self.assertEqual(identity['whole_source_sha256'], 'f148f27864f050efde8ef6815bdd49c40ba0470d165f4fe37e5db5e204a98440')
        self.assertEqual(hashlib.sha256(positive).hexdigest(), identity['positive_method_sha256'])
        start = full.index(b'    @Test fun normalAdvancedColourKeepsFiniteViewportAndFixedControls()')
        end = full.index(b'\n    }\n', start) + len(b'\n    }\n')
        self.assertEqual(start, identity['positive_method_byte_start'])
        self.assertEqual(end, identity['positive_method_byte_end'])
        self.assertEqual(positive, full[start:end])
        self.assertIn(b'assertTrue(inner.height>0)', positive)
        self.assertIn(b'inner.scrollY>before', positive)
        self.assertIn(b'fixed.map {assertComplete(it);rawBounds(it)}', positive)
        self.assertEqual(identity['original_source_commit'], 'df214fee4f106c4365325412b4f9d3c8530232d5')
        self.assertFalse(identity['positive_viewport_accepted'])
        self.assertEqual(identity['untouched_baseline_installed'], 'pending')

    def test_current_characterization_emits_geometry_before_known_limitation_assertion(self):
        source = (Path(__file__).resolve().parents[1] / 'app/src/androidTest/java/paint/anpaint/android/LocalizedDialogDeviceTest.kt').read_text()
        block = source.split('fun unchangedAdvancedColourReportsShortLandscapeLimitation()', 1)[1].split('private fun colourGeometry', 1)[0]
        self.assertLess(block.index('"colour-limitation-characterization"'), block.index('0,inner.height)'))
        for text in ('640,display.width', '320,display.height', '1f,activity.resources.configuration.fontScale',
                     '"holder_parent",colourGeometry(holder.parent as View)', '"inner_content",colourGeometry(inner.getChildAt(0))',
                     'evidence.capture("colour-limitation")', 'evidence.capture("colour-cancelled")',
                     'tap("colour cancel"', 'assertEquals(0,committed);assertEquals(1,closed)',
                     '"positive_viewport_accepted",false', '"untouched_baseline_installed","pending"'):
            self.assertIn(text, block)
        self.assertNotIn('@Test fun normalAdvancedColourKeepsFiniteViewportAndFixedControls()', source)


if __name__ == '__main__':
    unittest.main()
