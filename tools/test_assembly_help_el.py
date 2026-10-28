"""Complete source-bound Greek Help guard, not linguistic or runtime certification.

Independent full-value acceptance: PR56 comment 6329612253, against
b12c1ce79e2683d5cc841f218c1d19d74e9fd699. A relevant source/text change requires
review, not blind hash regeneration. Separate warning resources, PR118's four
keys, position-control fixtures and English-only suites are not extended here.
"""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

RES = Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"
KEY = "ui_add_up_to_20_images_with_android_s"
SOURCE_SHA256 = "6ae12f86846110a7573a5c608b8561b0c03b037454f1905d3b5bf8342fb26aac"
ACCEPTED_SHA256 = "5a9f23a9fcfe8a8220a68734a14d751538278f81070530409c8b0a56778eccd6"
CAPTIONS = {
    0: ("ui_same_width", "ui_same_height"),
    1: ("ui_crop_image", "ui_batch_crop", "ui_reset_crop"),
    3: ("ui_assembly_exact_position",),
    4: ("ui_same_width", "ui_same_height", "ui_smallest", "ui_largest",
        "ui_restore_original_sizes"),
    5: ("ui_unplace", "ui_remove", "ui_undo", "ui_redo", "ui_show_all"),
    6: ("ui_save_png", "ui_edit_in_paint"),
    7: ("ui_menu_file", "ui_about_credits23"),
}
# Deliberate corruptions of the accepted wording, not alternative translations.
# Needles are scoped to paragraphs so repeated modal wording is not ambiguous.
MUTATIONS = (
    ("crop-only-dimensions", 0,
     "μετά την περικοπή και τυχόν προσαρμογή με «Ίδιο πλάτος» ή «Ίδιο ύψος»",
     "μετά την περικοπή"),
    ("unscoped-origin", 2, "Κατά την προσκόλληση, η πρώτη εικόνα", "Η πρώτη εικόνα"),
    ("unscoped-overlap", 2, " κατά την προσκόλληση.", "."),
    ("guaranteed-attached-movement", 2, "ενδέχεται να μετακινηθούν", "μετακινούνται"),
    ("wrong-position-caption", 3, "«Ακριβής θέση»", "«Exact position»"),
    ("wrong-coordinate-origin", 3, "ξεκινώντας από το μηδέν", "ξεκινώντας από το ένα"),
    ("missing-whole-pixels", 3, "σε ακέραιο αριθμό εικονοστοιχείων", "σε εικονοστοιχεία"),
    ("missing-other-position-preservation", 3,
     "Οι άλλες εικόνες διατηρούν τις θέσεις τους και ", ""),
    ("reject-exact-overlap", 3, "οι επικαλύψεις επιτρέπονται", "οι επικαλύψεις απορρίπτονται"),
    ("lost-per-image-aspect-ratio", 4,
     "για κάθε εικόνα τη δική της αναλογία διαστάσεων", "μια κοινή αναλογία διαστάσεων"),
    ("reset-discards-crops", 4, "και διατηρεί τις περικοπές", "και αφαιρεί τις περικοπές"),
    ("guaranteed-gap-movement", 5, "ενδέχεται να μετακινηθούν", "μετακινούνται"),
    ("unconditional-size-chooser", 6, ", εφόσον προσφέρεται αυτή η επιλογή", ""),
    ("missing-tiny-output-warning", 6,
     "Αν ακόμη και μια εικόνα εξόδου πολύ μικρών διαστάσεων υπερβαίνει το όριο, "
     "η εφαρμογή εμφανίζει προειδοποίηση για τη μνήμη αντί για παράθυρο επιλογής μεγέθους. ", ""),
)


def plain_help(root):
    nodes = root.findall(f"./*[@name='{KEY}']")
    if (len(nodes) != 1 or nodes[0].tag != "string" or
            nodes[0].attrib != {"name": KEY} or len(nodes[0])):
        raise ValueError("Expected one plain Help string with unchanged attributes")
    return nodes[0].text or ""


def require_bound_help(source_root, greek_root):
    source, value = plain_help(source_root), plain_help(greek_root)
    if sha256(source.encode("utf-8")).hexdigest() != SOURCE_SHA256:
        raise ValueError("English Help changed; source-bound re-review required")
    if sha256(value.encode("utf-8")).hexdigest() != ACCEPTED_SHA256:
        raise ValueError("Complete Greek Help differs from the independently accepted value")
    return value


class AssemblyHelpGreekTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ET.parse(RES / "values/strings.xml").getroot()
        cls.greek = ET.parse(RES / "values-el/strings.xml").getroot()

    def test_complete_value_source_shape_and_current_captions(self):
        value = require_bound_help(self.source, self.greek)
        paragraphs = value.split(r"\n\n")
        self.assertEqual(8, len(paragraphs))
        self.assertEqual(14, value.count(r"\n"))
        self.assertFalse(any(c in value for c in ("\n", "\r", "\ufffd")))
        for index, keys in CAPTIONS.items():
            for key in keys:
                with self.subTest(paragraph=index, key=key):
                    nodes = self.greek.findall(f"./string[@name='{key}']")
                    self.assertEqual(1, len(nodes))
                    self.assertTrue(nodes[0].text)
                    self.assertIn(nodes[0].text, paragraphs[index])
        route = [self.greek.find(f"./string[@name='{key}']").text
                 for key in CAPTIONS[7]]
        self.assertIn("«" + " > ".join(route) + "»", paragraphs[7])
        self.assertIn("Catrobat/AGPL", paragraphs[7])

    def test_scoped_mode_memory_and_normalization_regressions_are_rejected(self):
        original = require_bound_help(self.source, self.greek)
        for name, index, before, after in MUTATIONS:
            with self.subTest(mutation=name):
                parts = original.split(r"\n\n")
                self.assertEqual(1, parts[index].count(before))
                parts[index] = parts[index].replace(before, after, 1)
                broken = deepcopy(self.greek)
                node = broken.find(f"./string[@name='{KEY}']")
                node.text = r"\n\n".join(parts)
                self.assertNotEqual(original, node.text)
                with self.assertRaisesRegex(ValueError, "Complete Greek Help differs"):
                    require_bound_help(self.source, broken)

    def test_each_paragraph_is_required_including_exact_position_crop_and_credits(self):
        parts = require_bound_help(self.source, self.greek).split(r"\n\n")
        for index in range(8):
            with self.subTest(missing_paragraph=index):
                broken = deepcopy(self.greek)
                broken.find(f"./string[@name='{KEY}']").text = r"\n\n".join(parts[:index] + parts[index + 1:])
                with self.assertRaisesRegex(ValueError, "Complete Greek Help differs"):
                    require_bound_help(self.source, broken)

    def test_source_and_target_corruption_are_rejected(self):
        require_bound_help(self.source, self.greek)
        for target in ("source", "greek"):
            for mutation in ("truncated", "duplicate", "missing", "attribute", "markup", "tag"):
                with self.subTest(target=target, mutation=mutation):
                    source, greek = deepcopy(self.source), deepcopy(self.greek)
                    broken = source if target == "source" else greek
                    node = broken.find(f"./string[@name='{KEY}']")
                    if mutation == "truncated":
                        node.text = node.text[:-1]
                    elif mutation == "duplicate":
                        broken.append(deepcopy(node))
                    elif mutation == "missing":
                        broken.remove(node)
                    elif mutation == "attribute":
                        node.set("formatted", "false")
                    elif mutation == "markup":
                        ET.SubElement(node, "b")
                    elif mutation == "tag":
                        node.tag = "plurals"
                    with self.assertRaises(ValueError):
                        require_bound_help(source, greek)


if __name__ == "__main__":
    unittest.main()

