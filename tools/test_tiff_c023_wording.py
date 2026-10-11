"""F01-C023 exact Cyrillic Mongolian oracle and bounded scope composition.

Source/host checks do not establish native-speaker or installed-dialog acceptance.
"""
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import test_commons_copy_credit_errors as copy_credit_scope

ROOT = Path(__file__).resolve().parents[1]
KEY = "formats22_tiff_description"
PATH = "Paintroid/src/main/res/values-b+mn+Cyrl+MN/strings.xml"
FIXTURE = ROOT / "tools/fixtures/tiff_c023_wording_scope.json"
ORIGINAL = "Нэг RGB хуудсыг хадгална. Шахалт нь пикселийг өөрчлөхгүйгээр файлын хэмжээг багасгана; шахалтгүй TIFF хадгалахын тулд унтраана."
EXPECTED = "Нэг RGB хуудсыг хадгална. Шахалт нь пикселийг өөрчлөхгүйгээр файлын хэмжээг багасгаж магадгүй; шахалтгүй TIFF хадгалахын тулд унтраана."
BASE_SHA256 = "cdac186240e12eec3878e3dcbf532ef6f7753d54fae3968abca923e00730493f"


def xml_line(value):
    return f'    <string name="{KEY}">{value}</string>\n'


class TiffC023WordingTests(unittest.TestCase):
    def test_exact_single_definition_and_unchanged_checkbox(self):
        root = ET.parse(ROOT / PATH).getroot()
        nodes = root.findall(f"./string[@name='{KEY}']")
        self.assertEqual(1, len(nodes))
        self.assertEqual({"name": KEY}, nodes[0].attrib)
        self.assertEqual(0, len(nodes[0]))
        self.assertEqual(EXPECTED, nodes[0].text)
        self.assertNotIn("%", nodes[0].text)
        checkbox = root.findall("./string[@name='formats22_tiff_compression']")
        self.assertEqual(1, len(checkbox))
        self.assertEqual("Алдагдалгүй шахалт (Deflate)", checkbox[0].text)

    def test_only_modal_substitution_restores_entire_pinned_source_file(self):
        self.assertEqual(EXPECTED, ORIGINAL.replace("багасгана", "багасгаж магадгүй"))
        data = (ROOT / PATH).read_bytes()
        after, before = xml_line(EXPECTED).encode(), xml_line(ORIGINAL).encode()
        self.assertEqual(1, data.count(after))
        self.assertEqual(0, data.count(before))
        self.assertEqual(BASE_SHA256, hashlib.sha256(data.replace(after, before, 1)).hexdigest())

    def test_extension_fixture_contains_exactly_c023_with_independent_oracles(self):
        fixture = json.loads(FIXTURE.read_text())
        self.assertEqual(1, fixture["schema_version"])
        self.assertEqual("F01-C023", fixture["case_id"])
        self.assertEqual(KEY, fixture["resource_key"])
        self.assertEqual("4f9082aa687a5c36b559061bcc10d0e39331610f", fixture["source_commit"])
        self.assertEqual([{"path": PATH, "before": xml_line(ORIGINAL),
                           "after": xml_line(EXPECTED)}], fixture["entries"])

    def test_original_37_entry_fixture_and_its_scope_are_unchanged(self):
        data = (ROOT / "tools/fixtures/tiff_size_wording_scope.json").read_bytes()
        self.assertEqual("9cead98f8f826c5c853f4b0dc6cd6b80f8760274770a00f600c690d44fba0ac1",
                         hashlib.sha256(data).hexdigest())
        entries = json.loads(data)["entries"]
        self.assertEqual(37, len(entries))
        self.assertNotIn(PATH, {row["path"] for row in entries})

    def _assert_historical_hash(self, text):
        scope = json.loads((copy_credit_scope.EVIDENCE / "source-scope.json").read_text())
        row = next(row for row in scope["catalogues"] if row["path"] == PATH)
        restored = copy_credit_scope.catalogue_before_copy_credit_and_f01(PATH, text)
        self.assertEqual(row["before_sha256"], hashlib.sha256(restored.encode()).hexdigest())

    def test_composed_guard_preserves_original_copy_credit_historical_hash(self):
        self._assert_historical_hash((ROOT / PATH).read_text())

    def test_composed_guard_rejects_reversion_corruption_deletion_and_duplication(self):
        text = (ROOT / PATH).read_text()
        after = xml_line(EXPECTED)
        for bad in (xml_line(ORIGINAL), after.replace("магадгүй", "магадгүй?"), "", after * 2):
            with self.subTest(replacement=bad):
                with self.assertRaises(AssertionError):
                    self._assert_historical_hash(text.replace(after, bad, 1))

    def test_composed_guard_rejects_unrelated_content(self):
        text = (ROOT / PATH).read_text()
        with self.assertRaises(AssertionError):
            self._assert_historical_hash(text.replace("</resources>", "<!-- unrelated -->\n</resources>"))

    def test_extension_pin_rejects_missing_duplicate_or_expanded_fixture(self):
        original_read = Path.read_bytes
        fixture = json.loads(FIXTURE.read_text())
        malformed = []
        missing = json.loads(json.dumps(fixture)); missing["entries"] = []; malformed.append(missing)
        duplicate = json.loads(json.dumps(fixture)); duplicate["entries"] *= 2; malformed.append(duplicate)
        expanded = json.loads(json.dumps(fixture))
        expanded["entries"][0]["after"] += '    <string name="ui_save">unexpected</string>\n'
        malformed.append(expanded)
        text = (ROOT / PATH).read_text()
        for value in malformed:
            altered = json.dumps(value).encode()
            def read_bytes(path):
                return altered if path == FIXTURE else original_read(path)
            with self.subTest(fixture=value), patch.object(Path, "read_bytes", read_bytes):
                with self.assertRaisesRegex(AssertionError, "F01-C023 scope fixture changed"):
                    self._assert_historical_hash(text)

    def test_traditional_mongolian_c024_remains_byte_identical(self):
        path = ROOT / "Paintroid/src/main/res/values-b+mn+Mong/strings.xml"
        self.assertEqual("6c1b22b811b1e3cdce566fc40c5c2c69a942b875beb5631c6e8c1406a15a3821",
                         hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
