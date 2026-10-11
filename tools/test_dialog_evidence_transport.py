"""Synthetic archive contracts; these are not installed-device test results."""
import copy
import hashlib
import json
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
                source_tests_sha256=DIGEST,
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
    return dict(schema=1, test_class=TEST_CLASS, test_method=method, device_sdk=35,
                package=OWNER, outcome='passed', source_tests_sha256=DIGEST,
                source_binding='runner-supplied-needs-host-comparison',
                screenshots=METHOD_SCREENS[method], observations=observations)


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
                '--ordinary-summary', str(self.summary), '--output', str(self.output), '--receipt', str(destination)],
                capture_output=True, text=True, timeout=5)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(destination.exists())
            self.assertFalse(self.output.exists())


if __name__ == '__main__':
    unittest.main()
