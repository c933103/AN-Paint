"""Bounded complete-value Help guards for eo, es-419 and et.

The fixture contains independently reviewed values, not generated translations.
Exact values, paragraph placement and live caption references are drift contracts,
not linguistic proof or Android/device coverage. Existing memory/tray tests remain
independent and unchanged except for their reviewed narrow dependency alignments.
All checks use unittest or explicit exceptions, so Python -O does not erase them.
"""
import copy
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "Paintroid/src/main/res"
FIXTURE = "assembly_help_followon.json"
HELP = "ui_add_up_to_20_images_with_android_s"
DIRECTORIES = ("values-b+eo", "values-b+es+419", "values-b+et")
FORMAT = re.compile(r"%(?:[1-9]\d*\$)?[-#+ 0,(<]*\d*(?:\.\d+)?(?:[tT])?[A-Za-z%]")


def only_string(root, key):
    nodes = root.findall(f"string[@name='{key}']")
    if len(nodes) != 1:
        raise AssertionError(f"Expected exactly one string {key}, got {len(nodes)}")
    if len(nodes[0]):
        raise AssertionError(f"Unexpected child markup in {key}")
    return nodes[0]


def check_complete_help(test, root, expected):
    node = only_string(root, HELP)
    test.assertEqual({"name": HELP}, node.attrib)
    test.assertEqual(expected["attributes"], node.attrib)
    test.assertEqual(expected["value"], "".join(node.itertext()))


class AssemblyHelpFollowonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = fixture(FIXTURE)
        cls.catalogues = {
            directory: ET.parse(RES / directory / "strings.xml").getroot()
            for directory in DIRECTORIES
        }

    def test_reviewed_fixture_scope_is_exact(self):
        self.assertEqual(set(DIRECTORIES), set(self.fixture["locales"]))
        self.assertEqual(HELP, self.fixture["resource_key"])
        self.assertEqual(8, self.fixture["paragraph_count"])
        self.assertEqual(6, self.fixture["output_paragraph_index"])

    def test_complete_reviewed_values(self):
        for directory, root in self.catalogues.items():
            with self.subTest(locale=directory):
                check_complete_help(self, root, self.fixture["locales"][directory])

    def test_plain_eight_paragraph_help_without_format_arguments(self):
        for directory, root in self.catalogues.items():
            text = "".join(only_string(root, HELP).itertext())
            with self.subTest(locale=directory):
                self.assertEqual(8, len(text.split(r"\n\n")))
                self.assertTrue(all(text.split(r"\n\n")))
                self.assertEqual([], FORMAT.findall(text))
                self.assertNotIn("\n", text)
                self.assertNotIn("\r", text)

    def test_references_use_actual_captions_in_their_help_paragraph(self):
        for directory, root in self.catalogues.items():
            paragraphs = "".join(only_string(root, HELP).itertext()).split(r"\n\n")
            for index, keys in self.fixture["caption_keys_by_paragraph"].items():
                for key in keys:
                    with self.subTest(locale=directory, paragraph=index, caption=key):
                        caption = "".join(only_string(root, key).itertext())
                        self.assertTrue(caption)
                        self.assertIn(caption, paragraphs[int(index)])

    def test_guard_rejects_deleted_reordered_or_truncated_help(self):
        for directory, original in self.catalogues.items():
            expected = self.fixture["locales"][directory]
            paragraphs = expected["value"].split(r"\n\n")
            mutations = {
                "missing exact position": r"\n\n".join(paragraphs[:3] + paragraphs[4:]),
                "output in wrong paragraph": r"\n\n".join(paragraphs[:5] + [paragraphs[6], paragraphs[5]] + paragraphs[7:]),
                "truncated final sentence": expected["value"][:-1],
                "introduced format argument": expected["value"] + " %1$s",
            }
            for mutation, value in mutations.items():
                with self.subTest(locale=directory, mutation=mutation):
                    root = copy.deepcopy(original)
                    only_string(root, HELP).text = value
                    with self.assertRaises(AssertionError):
                        check_complete_help(self, root, expected)

    def test_guard_rejects_duplicate_help_resource(self):
        for directory, original in self.catalogues.items():
            with self.subTest(locale=directory):
                root = copy.deepcopy(original)
                root.append(copy.deepcopy(only_string(root, HELP)))
                with self.assertRaises(AssertionError):
                    check_complete_help(self, root, self.fixture["locales"][directory])


if __name__ == "__main__":
    unittest.main()
