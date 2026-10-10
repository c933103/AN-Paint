"""F01 wording/resource guards; dialog execution is TiffDescriptionDialogTest.

These exact oracles cover only the eleven reviewed entries, not language acceptance.
"""
from pathlib import Path
import unittest
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


if __name__ == "__main__":
    unittest.main()
