"""F01 wording/resource guards; dialog execution is TiffDescriptionDialogTest.

These exact oracles cover only the eleven reviewed entries, not language acceptance.
"""
from pathlib import Path
import hashlib
import json
import re
import test_commons_copy_credit_errors as copy_credit_scope
import test_tiff_additional_locale_wording as additional_tiff
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "Paintroid/src/main/res"
KEY = "formats22_tiff_description"
ENGLISH = ("Saves one RGB page. Compression may reduce file size without changing "
           "pixels; turn it off for uncompressed TIFF.")
PORTUGUESE = ("Salva uma página RGB. A compressão pode reduzir o tamanho do arquivo "
              "sem alterar os pixels; desative-a para criar um TIFF sem compressão.")
ENGLISH_VARIANTS = (
    "values-b+en+001", "values-en-rAU", "values-en-rCA", "values-en-rGB",
    "values-en-rIN", "values-en-rSG", "values-en-rUS",
)


def strings(folder):
    entries = {}
    for path in (RES / folder).glob("*.xml"):
        for node in ET.parse(path).getroot().findall("string"):
            name = node.get("name")
            if name in entries:
                raise AssertionError(f"Duplicate string in {folder}: {name}")
            entries[name] = "".join(node.itertext())
    return entries


class TiffDescriptionWordingTests(unittest.TestCase):
    def test_default_source_qualifies_size_but_keeps_pixels_and_unchecked_instruction(self):
        self.assertEqual(ENGLISH, strings("values")[KEY])

    def test_each_separate_english_catalogue_uses_the_reviewed_qualification(self):
        for folder in ENGLISH_VARIANTS:
            with self.subTest(folder=folder):
                self.assertEqual(ENGLISH, strings(folder)[KEY])

    def test_brazilian_portuguese_qualifies_size_and_preserves_its_own_wording(self):
        self.assertEqual(PORTUGUESE, strings("values-pt-rBR")[KEY])
        self.assertEqual("Compressão sem perdas (Deflate)",
                         strings("values-pt-rBR")["formats22_tiff_compression"])

    def test_vertical_layout_fixtures_retain_english_meaning_and_emoji_prefix(self):
        self.assertEqual(ENGLISH, strings("values-b+en+XV")[KEY])
        self.assertEqual("💾 " + ENGLISH, strings("values-b+qaa+Zsye+XV")[KEY])

    def test_all_eleven_descriptions_remain_argument_free(self):
        folders = ("values", *ENGLISH_VARIANTS, "values-b+en+XV",
                   "values-b+qaa+Zsye+XV", "values-pt-rBR")
        self.assertEqual(11, len(set(folders)))
        for folder in folders:
            with self.subTest(folder=folder):
                self.assertNotIn("%", strings(folder)[KEY])

    def test_welsh_dialog_fixture_exercises_a_missing_key_not_a_new_translation(self):
        self.assertNotIn(KEY, strings("values-b+cy"))
        self.assertEqual(ENGLISH, strings("values")[KEY])
        offered = ET.parse(RES / "values/app_language_tags.xml").findall(
            "./string-array[@name='app_language_tags']/item")
        self.assertIn("cy", [node.text for node in offered])


    def test_composition_fixture_allows_exactly_the_37_reviewed_single_resource_lines(self):
        fixture = json.loads((ROOT / "tools/fixtures/tiff_size_wording_scope.json").read_text())
        self.assertEqual(1, fixture["schema_version"])
        self.assertEqual(KEY, fixture["resource_key"])
        expected = {folder: ENGLISH for folder in ("values", *ENGLISH_VARIANTS, "values-b+en+XV")}
        expected["values-b+qaa+Zsye+XV"] = "💾 " + ENGLISH
        expected["values-pt-rBR"] = PORTUGUESE
        expected.update(additional_tiff.EXPECTED)
        paths = {f"Paintroid/src/main/res/{folder}/strings.xml": value
                 for folder, value in expected.items()}
        self.assertEqual(37, len(fixture["entries"]))
        self.assertEqual(set(paths), {row["path"] for row in fixture["entries"]})
        for row in fixture["entries"]:
            with self.subTest(path=row["path"]):
                for field in ("before", "after"):
                    line = row[field]
                    self.assertIsNotNone(re.fullmatch(
                        r'    <string name="formats22_tiff_description">[^\n]*</string>\n', line))
                    node = ET.fromstring(line)
                    self.assertEqual({"name": KEY}, node.attrib)
                    self.assertEqual(0, len(node))
                self.assertNotEqual(row["before"], row["after"])
                self.assertEqual(paths[row["path"]], ET.fromstring(row["after"]).text)

    def _assert_composed_historical_hash(self, row, text):
        restored = copy_credit_scope.catalogue_before_copy_credit_and_f01(row["path"], text)
        self.assertEqual(row["before_sha256"], hashlib.sha256(restored.encode()).hexdigest())

    def test_composed_scope_guard_rejects_unrelated_strings_in_all_60_catalogues(self):
        scope = json.loads((copy_credit_scope.EVIDENCE / "source-scope.json").read_text())
        self.assertEqual(60, len(scope["catalogues"]))
        for row in scope["catalogues"]:
            with self.subTest(path=row["path"]):
                text = (ROOT / row["path"]).read_text()
                self._assert_composed_historical_hash(row, text)
                mutated, count = re.subn(r'(<string\b[^>]*\bname="ui_save"[^>]*>)([^\n]*)(</string>)',
                                         r'\1\2 [unrelated negative control]\3', text)
                self.assertEqual(1, count)
                with self.assertRaises(AssertionError):
                    self._assert_composed_historical_hash(row, mutated)

    def test_composed_scope_guard_rejects_tiff_reversions_corruption_and_prefix_loss(self):
        fixture = json.loads((ROOT / "tools/fixtures/tiff_size_wording_scope.json").read_text())
        scope = json.loads((copy_credit_scope.EVIDENCE / "source-scope.json").read_text())
        rows = {row["path"]: row for row in scope["catalogues"]}
        for change in fixture["entries"]:
            with self.subTest(path=change["path"]):
                text = (ROOT / change["path"]).read_text()
                self.assertEqual(1, text.count(change["after"]))
                for bad in (change["before"], change["after"].replace("</string>", "? </string>"),
                            "", change["after"] * 2):
                    with self.assertRaises(AssertionError):
                        self._assert_composed_historical_hash(rows[change["path"]],
                            text.replace(change["after"], bad, 1))
        emoji = next(row for row in fixture["entries"] if "+qaa+Zsye+XV/" in row["path"])
        text = (ROOT / emoji["path"]).read_text()
        with self.assertRaises(AssertionError):
            self._assert_composed_historical_hash(rows[emoji["path"]],
                text.replace(emoji["after"], emoji["after"].replace("💾 ", ""), 1))


    def test_composed_scope_fixture_pin_rejects_missing_duplicate_or_extra_xml(self):
        fixture = json.loads((ROOT / "tools/fixtures/tiff_size_wording_scope.json").read_text())
        row = fixture["entries"][0]
        text = (ROOT / row["path"]).read_text()
        malformed = []
        missing = json.loads(json.dumps(fixture)); missing["entries"].pop(); malformed.append(missing)
        duplicate = json.loads(json.dumps(fixture))
        duplicate["entries"][-1] = duplicate["entries"][0]; malformed.append(duplicate)
        extra = json.loads(json.dumps(fixture))
        extra["entries"][0]["after"] += '    <string name="ui_save">unexpected</string>\n'
        malformed.append(extra)
        for value in malformed:
            with self.subTest(fixture=value):
                with patch.object(Path, "read_bytes", return_value=json.dumps(value).encode()):
                    with self.assertRaises(AssertionError):
                        copy_credit_scope.catalogue_before_copy_credit_and_f01(row["path"], text)


if __name__ == "__main__":
    unittest.main()
