#!/usr/bin/env python3
"""Small synthetic controls for the new review-only image reuse checker."""
import hashlib
import json
import pathlib
import tempfile
import unittest

from audit_natural_artifacts import HEAD, TREE, MERGE, RUN
from audit_visual_continuity import audit


class VisualContinuityTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.prior, self.current = self.root / 'prior', self.root / 'current'
        self.prior.mkdir(); self.current.mkdir()
        self.common = dict(head=HEAD, tree=TREE, merge=MERGE, run_id=int(RUN))
        self.manifest = []

        def frozen(name, data):
            self.write(self.prior / name, data)
            raw = (self.prior / name).read_bytes()
            self.manifest.append(dict(path=name, bytes=len(raw), sha256=self.sha(raw)))

        frozen('ACCEPTANCE.json', dict(head='e19c766eb3eaedc1b3cd3657bb92864f81a9498a',
            tree='dc1ba97dacc573ead73729297eb739ecb244dcf5', run_id=38299305241,
            status='PASS_BOUNDED_INSTALLED_SCOPE_AND_PLATFORM_DISCOVERY'))
        native = self.common | {'devices': {}}
        for api in (30, 35):
            paths = [f'image-{i}.png' for i in range(96)]
            images = []
            for name in paths:
                raw = f'SYNTHETIC-NOT-PNG-{api}-{name}'.encode()
                for path in (self.prior / f'reproduced/native-vertical/native-observed-api{api}' / name,
                             self.current / f'native-vertical/native-observed-api{api}' / name):
                    path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
                images.append(dict(path=name, sha256=self.sha(raw)))
            frozen(f'api{api}-visual-inspection.json', dict(api=api, original_png_count=96,
                status='ACTUALLY_INSPECTED_BOUNDED_NATIVE_FRAMES', sheets=[dict(source_images=images)]))
            native['devices'][str(api)] = {'full_decoded_images': images}
        self.write(self.current / 'native-vertical/result.json', native)
        arabic, routes = [], []
        for route in ('copy', 'insert'):
            images = {}
            for kind in ('actual', 'reference'):
                name = f'{route}-{kind}.png'; raw = ('SYNTHETIC-NOT-PNG-' + name).encode()
                for root in (self.prior, self.current):
                    path = root / 'installed-observed' / name
                    path.parent.mkdir(exist_ok=True); path.write_bytes(raw)
                arabic.append(dict(path='installed-observed/' + name, sha256=self.sha(raw)))
                images[kind] = {'sha256': self.sha(raw)}
            routes.append(dict(route=route, png=images))
        frozen('arabic-visual-inputs.json', dict(status='ACTUALLY_VIEWED_FOUR_ORIGINAL_RGBA_INPUTS', images=arabic))
        self.write(self.prior / 'DELIVERY-FILES.json', dict(files=self.manifest))
        self.write(self.current / 'installed-pixel-result.json', self.common | dict(status='PASS', routes=routes))
        self.write(self.current / 'result.json', dict(audit_integrity_status='PASS', installed_gate_status='PASS',
            native_vertical_status='PASS_BOUNDED_NATIVE_VERTICAL',
            platform_locale_discovery_status='PASS_BOUND_INSTALLED_PLATFORM_LOCALE_DISCOVERY'))
        for name in ('natural-update-result.json', 'platform-locale-binding-result.json'):
            self.write(self.current / name, {})

    @staticmethod
    def sha(data): return hashlib.sha256(data).hexdigest()

    @staticmethod
    def write(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))

    def test_all_identical(self):
        result = audit(self.prior, self.current)
        self.assertEqual(result['exactly_identical_images'], 196)
        self.assertEqual(result['status'], 'PASS_EXACT_IMAGE_BYTE_CONTINUITY')

    def test_changed_current_bytes_require_viewing(self):
        path = self.current / 'native-vertical/native-observed-api30/image-0.png'
        path.write_bytes(b'CHANGED-SYNTHETIC')
        report = self.current / 'native-vertical/result.json'
        value = json.loads(report.read_bytes())
        value['devices']['30']['full_decoded_images'][0]['sha256'] = self.sha(path.read_bytes())
        self.write(report, value)
        result = audit(self.prior, self.current)
        self.assertEqual(result['changed_images'], 1)
        self.assertEqual(result['status'], 'CHANGED_IMAGES_NEED_VISUAL_REVIEW')

    def test_changed_prior_bytes_rejected(self):
        (self.prior / 'installed-observed/copy-actual.png').write_bytes(b'CHANGED')
        with self.assertRaisesRegex(ValueError, 'prior viewed Arabic PNG differs'):
            audit(self.prior, self.current)

    def test_failed_current_gate_rejected(self):
        path = self.current / 'result.json'; value = json.loads(path.read_bytes())
        value['installed_gate_status'] = 'FAIL'; self.write(path, value)
        with self.assertRaisesRegex(ValueError, 'fresh installed diagnostic gates'):
            audit(self.prior, self.current)

    def test_wrong_current_binding_rejected(self):
        path = self.current / 'installed-pixel-result.json'; value = json.loads(path.read_bytes())
        value['head'] = '0' * 40; self.write(path, value)
        with self.assertRaisesRegex(ValueError, 'fresh visual diagnostics binding differs'):
            audit(self.prior, self.current)


if __name__ == '__main__': unittest.main()
