"""Input-path safety checks use temporary files only; no font dependency needed."""
from pathlib import Path
import tempfile
import unittest

from extend_nom_ui_font import extend


class NomFontInputPreservationTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.primary = self.root / 'primary.ttf'
        self.base = self.root / 'base.ttf'
        # Deliberately not fonts: alias rejection must precede input validation.
        self.primary.write_bytes(b'pinned source fixture')
        self.base.write_bytes(b'pinned subset fixture')
        self.before = {path: path.read_bytes() for path in (self.primary, self.base)}

    def assert_rejected_without_changes(self, output):
        try:
            with self.assertRaisesRegex(ValueError, '^Output must not overwrite either pinned input$'):
                extend(self.primary, self.base, output)
        finally:
            for path, original in self.before.items():
                self.assertEqual(original, path.read_bytes(), path.name)

    def test_rejects_hard_link_to_primary_without_changing_either_input(self):
        output = self.root / 'output.ttf'
        output.hardlink_to(self.primary)
        self.assertNotEqual(output.resolve(), self.primary.resolve())
        self.assertTrue(output.samefile(self.primary))
        self.assert_rejected_without_changes(output)
        self.assertEqual(self.before[self.primary], output.read_bytes())

    def test_rejects_hard_link_to_base_without_changing_either_input(self):
        output = self.root / 'output.ttf'
        output.hardlink_to(self.base)
        self.assertNotEqual(output.resolve(), self.base.resolve())
        self.assertTrue(output.samefile(self.base))
        self.assert_rejected_without_changes(output)
        self.assertEqual(self.before[self.base], output.read_bytes())

    def test_rejects_direct_input_paths_without_changing_either_input(self):
        for output in (self.primary, self.base):
            with self.subTest(output=output.name):
                self.assert_rejected_without_changes(output)

    def test_rejects_symlink_to_either_input_without_changing_either_input(self):
        for target in (self.primary, self.base):
            with self.subTest(target=target.name):
                output = self.root / ('symlink-' + target.name)
                output.symlink_to(target)
                self.assert_rejected_without_changes(output)

    def test_distinct_output_paths_reach_input_validation_without_changes(self):
        for existing in (False, True):
            with self.subTest(existing=existing):
                output = self.root / ('existing.ttf' if existing else 'new.ttf')
                if existing:
                    output.write_bytes(b'unrelated existing output')
                try:
                    with self.assertRaisesRegex(ValueError, '^Unexpected Nom Na Tong v5.18 source$'):
                        extend(self.primary, self.base, output)
                finally:
                    for path, original in self.before.items():
                        self.assertEqual(original, path.read_bytes(), path.name)
                    if existing:
                        self.assertEqual(b'unrelated existing output', output.read_bytes())
                    else:
                        self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
