"""Complete bounded crop-family values, quantity forms and edge-caption contracts.

The Esperanto dormant normalization value is guarded only as its accepted
spelling-only text; the existing semantics are not newly accepted. The dormant
legacy manual and memory-warning package are excluded. These are drift checks,
not linguistic proof, Android plural selection, rendered UI or TTS verification.
Checks remain active under optimized Python; no bare assert statements are used.
"""
import copy
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "Paintroid/src/main/res"
FIXTURE = "crop_followon_wording.json"
PREVIEW = "ui_crop_preview_images"
FORMAT = re.compile(r"%(?:[1-9]\d*\$)?[-#+ 0,(<]*\d*(?:\.\d+)?(?:[tT])?[A-Za-z%]")
ESPERANTO_KEYS = {
    "ui_batch_crop", "ui_batch_crop_images", "ui_could_not_decode_the_cropped_region_of",
    "ui_cropped_thumbnail", "ui_drag_out_to_expand_in_to_trim_drag",
    "ui_give_all_images_the_same_each_image_keeps", "ui_image_shown_in_crop_preview",
    "ui_trim_from_the_original_edges_drag_the_handles", "ui_trim_in_pixels",
    "ui_trim_in_percent", "formats22_pdf_crop",
}


def only_node(root, tag, key):
    nodes = root.findall(f"{tag}[@name='{key}']")
    if len(nodes) != 1:
        raise AssertionError(f"Expected exactly one {tag} {key}, got {len(nodes)}")
    return nodes[0]


def check_string(test, root, key, expected):
    node = only_node(root, "string", key)
    test.assertEqual(0, len(node))
    test.assertEqual({"name": key}, node.attrib)
    test.assertEqual(expected["attributes"], node.attrib)
    text = "".join(node.itertext())
    test.assertEqual(expected["value"], text)
    test.assertEqual(expected["placeholders"], FORMAT.findall(text))


def check_preview(test, root, expected):
    node = only_node(root, "plurals", PREVIEW)
    test.assertEqual({"name": PREVIEW}, node.attrib)
    test.assertEqual(expected["attributes"], node.attrib)
    items = list(node)
    test.assertEqual(2, len(items))
    test.assertEqual({"one", "other"}, set(expected["items"]))
    test.assertEqual({"one", "other"}, {item.get("quantity") for item in items})
    for item in items:
        test.assertEqual("item", item.tag)
        test.assertEqual({"quantity": item.get("quantity")}, item.attrib)
        test.assertEqual(0, len(item))
        text = "".join(item.itertext())
        test.assertEqual(expected["items"][item.get("quantity")], text)
        test.assertEqual(["%1$d", "%2$d", "%3$d"], FORMAT.findall(text))
        test.assertEqual(1, text.count(r"\n"))
        test.assertIn(" × ", text)
        test.assertNotIn("\n", text)


class CropFollowonWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = fixture(FIXTURE)
        cls.catalogues = {
            directory: ET.parse(RES / directory / "strings.xml").getroot()
            for directory in cls.fixture["locales"]
        }

    def test_reviewed_fixture_scope_is_exact(self):
        self.assertEqual({"values-b+eo", "values-b+et"}, set(self.fixture["locales"]))
        self.assertEqual(ESPERANTO_KEYS, set(self.fixture["locales"]["values-b+eo"]["strings"]))
        self.assertEqual({}, self.fixture["locales"]["values-b+et"]["strings"])
        for expected in self.fixture["locales"].values():
            self.assertEqual({PREVIEW}, set(expected["plurals"]))

    def test_complete_reviewed_strings_and_placeholder_order(self):
        for directory, expected in self.fixture["locales"].items():
            for key, value in expected["strings"].items():
                with self.subTest(locale=directory, key=key):
                    check_string(self, self.catalogues[directory], key, value)

    def test_typed_arguments_match_the_current_english_source(self):
        english = ET.parse(RES / "values/strings.xml").getroot()
        for directory, expected in self.fixture["locales"].items():
            for key in expected["strings"]:
                with self.subTest(locale=directory, key=key):
                    source = "".join(only_node(english, "string", key).itertext())
                    local = "".join(only_node(self.catalogues[directory], "string", key).itertext())
                    self.assertEqual(FORMAT.findall(source), FORMAT.findall(local))

    def test_complete_quantity_forms_dimensions_and_selection_count(self):
        for directory, expected in self.fixture["locales"].items():
            with self.subTest(locale=directory):
                check_preview(self, self.catalogues[directory], expected["plurals"][PREVIEW])

    def test_all_four_actual_edge_captions_with_both_unit_templates(self):
        root = self.catalogues["values-b+eo"]
        expected = self.fixture["esperanto_edges"]
        self.assertEqual({"ui_left", "ui_top", "ui_right", "ui_bottom"}, set(expected))
        for key, row in expected.items():
            caption = "".join(only_node(root, "string", key).itertext())
            with self.subTest(edge=key):
                self.assertEqual(row["caption"], caption)
                for unit, resource in (("pixels", "ui_trim_in_pixels"), ("percent", "ui_trim_in_percent")):
                    template = "".join(only_node(root, "string", resource).itertext())
                    self.assertEqual(["%1$s"], FORMAT.findall(template))
                    self.assertEqual(row[unit], template.replace("%1$s", caption))
                pixel = "".join(only_node(root, "string", "ui_trim_in_pixels").itertext())
                self.assertEqual(1, pixel.count(":"))

    def test_guard_rejects_missing_duplicate_or_unexpected_quantity_forms(self):
        for directory, original in self.catalogues.items():
            expected = self.fixture["locales"][directory]["plurals"][PREVIEW]
            for mutation in ("missing", "duplicate", "unexpected"):
                root = copy.deepcopy(original)
                node = only_node(root, "plurals", PREVIEW)
                if mutation == "missing":
                    node.remove(node[1])
                elif mutation == "duplicate":
                    node[1].set("quantity", "one")
                else:
                    node[1].set("quantity", "few")
                with self.subTest(locale=directory, mutation=mutation):
                    with self.assertRaises(AssertionError):
                        check_preview(self, root, expected)

    def test_guard_rejects_truncated_warning_or_changed_placeholder(self):
        for directory, original in self.catalogues.items():
            expected = self.fixture["locales"][directory]["plurals"][PREVIEW]
            for quantity in ("one", "other"):
                for mutation in ("warning removed", "placeholder type changed", "placeholder omitted"):
                    root = copy.deepcopy(original)
                    item = only_node(root, "plurals", PREVIEW).find(f"item[@quantity='{quantity}']")
                    if mutation == "warning removed":
                        item.text = item.text.split(". ", 1)[0] + "."
                    elif mutation == "placeholder type changed":
                        item.text = item.text.replace("%3$d", "%3$s")
                    else:
                        item.text = item.text.replace("%2$d", "")
                    with self.subTest(locale=directory, quantity=quantity, mutation=mutation):
                        with self.assertRaises(AssertionError):
                            check_preview(self, root, expected)

    def test_guard_rejects_missing_esperanto_pixel_delimiter(self):
        root = copy.deepcopy(self.catalogues["values-b+eo"])
        key = "ui_trim_in_pixels"
        only_node(root, "string", key).text = "%1$s stuco en bilderoj"
        expected = self.fixture["locales"]["values-b+eo"]["strings"][key]
        with self.assertRaises(AssertionError):
            check_string(self, root, key, expected)


if __name__ == "__main__":
    unittest.main()
