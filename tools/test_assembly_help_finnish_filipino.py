"""Complete accepted Finnish/Filipino Help drift guards.

The fixture is independent accepted wording, not production-generated translation.
These guards do not certify linguistic meaning, native review, Android rendering,
or whole-language completion. unittest methods and explicit exceptions survive -O.
"""
import copy
import hashlib
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "Paintroid/src/main/res"
FIXTURE_PATH = ROOT / "tools/fixtures/current_localization/assembly_help_finnish_filipino.json"
HELP = "ui_add_up_to_20_images_with_android_s"
DIRECTORIES = ("values-fi", "values-b+fil")
ACCEPTED_VALUES = {
    "values-fi": "e87cd3c33f0f1d61dcc1ee34e07b9be82076d73f655d0527f6110aef037d21c3",
    "values-b+fil": "1050b9769bd8c1965a52c30f67d9f0021a8e7ea4afb7817314de994a830002aa",
}
FORMAT = re.compile(r"%(?:[1-9]\d*\$)?[-#+ 0,(<]*\d*(?:\.\d+)?(?:[tT])?[A-Za-z%]")
CAPTIONS = {
    0: ("ui_same_width", "ui_same_height"),
    1: ("ui_crop_image", "ui_batch_crop", "ui_reset_crop"),
    3: ("ui_assembly_exact_position",),
    4: ("ui_same_width", "ui_same_height", "ui_pixels", "ui_percent",
        "ui_smallest", "ui_largest", "ui_restore_original_sizes"),
    5: ("ui_unplace", "ui_remove", "ui_undo", "ui_redo", "ui_show_all"),
    6: ("ui_save_png", "ui_edit_in_paint"),
    7: ("ui_menu_file", "ui_about_credits23"),
}

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate fixture key: " + key)
        result[key] = value
    return result

def only_string(root, key):
    nodes = root.findall(f"string[@name='{key}']")
    if len(nodes) != 1:
        raise AssertionError(f"Expected one {key}, found {len(nodes)}")
    if len(nodes[0]):
        raise AssertionError("Unexpected child markup: " + key)
    return nodes[0]

def check_complete_help(test, root, expected):
    node = only_string(root, HELP)
    text = "".join(node.itertext())
    test.assertEqual({"name": HELP}, node.attrib)
    test.assertEqual(expected["attributes"], node.attrib)
    test.assertEqual(expected["value"], text)
    paragraphs = text.split(r"\n\n")
    test.assertEqual(8, len(paragraphs))
    test.assertTrue(all(paragraphs))
    test.assertEqual(14, text.count(r"\n"))
    test.assertNotIn("\n", text)
    test.assertNotIn("\r", text)
    test.assertEqual([], FORMAT.findall(text))
    for index, keys in CAPTIONS.items():
        for key in keys:
            caption = "".join(only_string(root, key).itertext())
            test.assertEqual(expected["captions"][key], caption)
            test.assertTrue(caption)
            test.assertIn(caption, paragraphs[index])
    for clause in expected["required_clauses"]:
        test.assertIn(clause["text"], paragraphs[clause["paragraph_index"]])
    for sentence in expected["memory_sentences"]:
        test.assertEqual(1, paragraphs[6].count(sentence))
        test.assertEqual(1, text.count(sentence))


class FinnishFilipinoAssemblyHelpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"),
                                 object_pairs_hook=unique_object)
        cls.catalogues = {
            directory: ET.parse(RES / directory / "strings.xml").getroot()
            for directory in DIRECTORIES
        }

    def test_fixture_is_exactly_two_independently_accepted_values(self):
        self.assertEqual(1, self.fixture["schema_version"])
        self.assertEqual(HELP, self.fixture["resource_key"])
        self.assertEqual(8, self.fixture["paragraph_count"])
        self.assertEqual(6, self.fixture["output_paragraph_index"])
        self.assertEqual(set(DIRECTORIES), set(self.fixture["locales"]))
        for directory in DIRECTORIES:
            with self.subTest(locale=directory):
                expected = self.fixture["locales"][directory]
                self.assertEqual(ACCEPTED_VALUES[directory],
                                 hashlib.sha256(expected["value"].encode("utf-8")).hexdigest())
                self.assertEqual(ACCEPTED_VALUES[directory],
                                 expected["provenance"]["accepted_value_sha256"])
                self.assertEqual({"name": HELP}, expected["attributes"])
                self.assertEqual({key for keys in CAPTIONS.values() for key in keys},
                                 set(expected["captions"]))
                self.assertEqual(2, len(expected["memory_sentences"]))
                self.assertEqual(2, len(set(expected["memory_sentences"])))
                self.assertEqual({
                    "snap origin qualification", "snap overlap qualification",
                    "parent crop optional movement", "exact whole-pixel zero origin",
                    "exact other positions and overlap", "unplace optional movement",
                    "unplace other images stay placed", "crop normalization independence",
                    "tray crop and normalization dimensions",
                }, {clause["name"] for clause in expected["required_clauses"]})
                self.assertEqual(9, len(expected["required_clauses"]))

    def test_complete_values_structure_captions_and_both_memory_clauses(self):
        for directory, root in self.catalogues.items():
            with self.subTest(locale=directory):
                check_complete_help(self, root, self.fixture["locales"][directory])

    def test_guard_rejects_missing_and_duplicate_resource(self):
        for directory, original in self.catalogues.items():
            expected = self.fixture["locales"][directory]
            for mutation in ("missing", "duplicate"):
                with self.subTest(locale=directory, mutation=mutation):
                    root = copy.deepcopy(original)
                    node = only_string(root, HELP)
                    if mutation == "missing":
                        root.remove(node)
                    else:
                        root.append(copy.deepcopy(node))
                    with self.assertRaises(AssertionError):
                        check_complete_help(self, root, expected)

    def test_guard_rejects_attributes_and_child_markup(self):
        for directory, original in self.catalogues.items():
            expected = self.fixture["locales"][directory]
            for mutation in ("formatted false", "translatable false", "child markup"):
                with self.subTest(locale=directory, mutation=mutation):
                    root = copy.deepcopy(original)
                    node = only_string(root, HELP)
                    if mutation == "formatted false":
                        node.set("formatted", "false")
                    elif mutation == "translatable false":
                        node.set("translatable", "false")
                    else:
                        ET.SubElement(node, "b").text, node.text = node.text, None
                    with self.assertRaises(AssertionError):
                        check_complete_help(self, root, expected)

    def test_guard_rejects_missing_duplicated_reordered_or_truncated_paragraphs(self):
        for directory, original in self.catalogues.items():
            expected = self.fixture["locales"][directory]
            paragraphs = expected["value"].split(r"\n\n")
            mutations = {
                "missing exact position": r"\n\n".join(paragraphs[:3] + paragraphs[4:]),
                "duplicate exact position": r"\n\n".join(paragraphs[:4] + [paragraphs[3]] + paragraphs[4:]),
                "output wrong index": r"\n\n".join(paragraphs[:5] + [paragraphs[6], paragraphs[5]] + paragraphs[7:]),
                "truncated value": expected["value"][:-1],
                "physical newline": expected["value"].replace(r"\n\n", "\n\n", 1),
                "format argument": expected["value"] + " %1$s",
            }
            for mutation, value in mutations.items():
                with self.subTest(locale=directory, mutation=mutation):
                    self.assertNotEqual(value, expected["value"])
                    root = copy.deepcopy(original)
                    only_string(root, HELP).text = value
                    with self.assertRaises(AssertionError):
                        check_complete_help(self, root, expected)

    def test_guard_rejects_lost_mode_movement_and_independence_clauses(self):
        for directory, original in self.catalogues.items():
            expected = self.fixture["locales"][directory]
            for clause in expected["required_clauses"]:
                with self.subTest(locale=directory, clause=clause["name"]):
                    self.assertIn(clause["text"], expected["value"])
                    value = expected["value"].replace(clause["text"], "", 1)
                    self.assertNotEqual(value, expected["value"])
                    root = copy.deepcopy(original)
                    only_string(root, HELP).text = value
                    with self.assertRaises(AssertionError):
                        check_complete_help(self, root, expected)

    def test_guard_rejects_each_missing_or_duplicated_memory_sentence(self):
        for directory, original in self.catalogues.items():
            expected = self.fixture["locales"][directory]
            for index, sentence in enumerate(expected["memory_sentences"]):
                for mutation, replacement in (("missing", ""), ("duplicate", sentence + " " + sentence)):
                    with self.subTest(locale=directory, sentence=index, mutation=mutation):
                        self.assertEqual(1, expected["value"].count(sentence))
                        value = expected["value"].replace(sentence, replacement, 1)
                        root = copy.deepcopy(original)
                        only_string(root, HELP).text = value
                        with self.assertRaises(AssertionError):
                            check_complete_help(self, root, expected)

    def test_guard_rejects_changed_caption_in_help_or_actual_control(self):
        for directory, original in self.catalogues.items():
            expected = self.fixture["locales"][directory]
            for key, caption in expected["captions"].items():
                for mutation in ("help caption", "control caption"):
                    with self.subTest(locale=directory, key=key, mutation=mutation):
                        root = copy.deepcopy(original)
                        if mutation == "help caption":
                            self.assertIn(caption, expected["value"])
                            only_string(root, HELP).text = expected["value"].replace(caption, "[changed caption]", 1)
                        else:
                            only_string(root, key).text = "[changed caption]"
                        with self.assertRaises(AssertionError):
                            check_complete_help(self, root, expected)

    def test_fixture_parser_rejects_duplicate_json_keys(self):
        with self.assertRaises(ValueError):
            json.loads('{"value": "first", "value": "second"}', object_pairs_hook=unique_object)


if __name__ == "__main__":
    unittest.main()
