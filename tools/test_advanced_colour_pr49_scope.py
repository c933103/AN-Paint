"""Historical PR49 endpoint guard, restored through the explicit PR51 composition."""
import hashlib
import json
from pathlib import Path
import unittest
from dialog_colour_composition_scope import before_colour_composition

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tools/fixtures/advanced_colour_pr49_scope.json'


def baseline_bytes(current, row):
    if hashlib.sha256(current).hexdigest() != row['after_sha256']:
        raise ValueError('Current source exceeds the pinned PR49 scope: '+row['path'])
    if 'after_fragment' in row:
        fragment = row['after_fragment'].encode()
        if current.count(fragment) != row['count']:
            raise ValueError('Exact About-only fragment required')
        current = current.replace(fragment, row['before_fragment'].encode())
    if hashlib.sha256(current).hexdigest() != row['before_sha256']:
        raise ValueError('Source no longer reconstructs the unchanged develop endpoint')
    return current


class AdvancedColourPr49Scope(unittest.TestCase):
    def test_native_colour_path_reconstructs_the_exact_baseline(self):
        raw = FIXTURE.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         '0d9882a696872dc1d2b4388cb356e3c13446fa8156dd1d3b582fbdfaba09885a')
        data = json.loads(raw)
        self.assertEqual(data['base_commit'], '691f8870649a1d21d1441f4e3d0e795660b23e9a')
        self.assertEqual({Path(row['path']).name for row in data['files']},
                         {'AdvancedColourDialog.kt', 'VerticalUi.kt', 'ClassicPaintActivity.kt'})
        for row in data['files']:
            with self.subTest(path=row['path']):
                baseline_bytes(before_colour_composition(row['path'], (ROOT / row['path']).read_bytes()), row)

    def test_unrelated_source_changes_and_endpoint_changes_fail_closed(self):
        for row in json.loads(FIXTURE.read_bytes())['files']:
            current = before_colour_composition(row['path'], (ROOT / row['path']).read_bytes())
            with self.subTest(path=row['path']), self.assertRaises(ValueError):
                baseline_bytes(current+b'\n', row)
            with self.assertRaises(ValueError):
                baseline_bytes(current, {**row, 'before_sha256': '0'*64})


if __name__ == '__main__':
    unittest.main()
