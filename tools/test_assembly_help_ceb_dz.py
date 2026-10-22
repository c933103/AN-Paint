"""Source-bound complete Help guards for independently reviewed Cebuano/Dzongkha.

Acceptance: PR56 comments 6328703092 (ceb) and 6329217439 (dz), against
b12c1ce79e2683d5cc841f218c1d19d74e9fd699. These preserve exact reviewed wording,
not arbitrary equivalent prose, linguistic quality or Android runtime behavior.
Changed English requires re-review, not blind regeneration. Separate coordinate,
TIFF, warning and English-only mode contracts are not extended by this module.
"""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

RES = Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"
KEY = "ui_add_up_to_20_images_with_android_s"
SOURCE_SHA256 = "6ae12f86846110a7573a5c608b8561b0c03b037454f1905d3b5bf8342fb26aac"
ACCEPTED = {
    "values-b+ceb": "9ddaae9e0ac2f7d4f4db5e364f51c31a70e39c663c648e733cad674258cb0894",
    "values-b+dz": "6e0e81a82611585e661dab08c64ab433cdd382fe14c0d608ec2be506e341a7f6",
}
CAPTIONS = {
    0: ("ui_same_width", "ui_same_height"),
    1: ("ui_crop_image", "ui_batch_crop", "ui_reset_crop"),
    3: ("ui_assembly_exact_position",),
    4: ("ui_same_width", "ui_same_height", "ui_smallest", "ui_largest", "ui_restore_original_sizes"),
    5: ("ui_unplace", "ui_remove", "ui_show_all"),
    6: ("ui_save_png", "ui_edit_in_paint"),
    7: ("ui_menu_file", "ui_about_credits23"),
}
# Each exact needle belongs in the indicated paragraph. Mutations deliberately
# corrupt the accepted text; they are not proposed alternative translations.
MUTATIONS = {
    "values-b+ceb": (
        ("unscoped-origin", 2, "Sa pagdugtong sa mga kilid, ang unang hulagway", "Ang unang hulagway"),
        ("unscoped-overlap", 2, " sa pagdugtong sa mga kilid.", "."),
        ("guaranteed-crop-movement", 2, "Mahimong molihok", "Molihok"),
        ("wrong-position-caption", 3, "Eksaktong posisyon", "Exact position"),
        ("wrong-coordinate-origin", 3, "sugod sa zero", "sugod sa 1"),
        ("missing-whole-pixels", 3, "tibuok nga gidaghanon sa pixel", "gidaghanon sa pixel"),
        ("missing-other-position-preservation", 3, "Ang ubang mga hulagway magpabilin sa ilang mga posisyon, ug ", ""),
        ("missing-exact-overlap-permission", 3, "gitugotan ang pagsapaw", ""),
        ("guaranteed-gap-movement", 5, "mahimong molihok", "molihok"),
        ("missing-size-offer-condition", 6, " kon adunay maong kapilian", ""),
    ),
    "values-b+dz": (
        ("unscoped-origin", 2, "མཐའ་ལུ་སྦྱར་ཏེ་བཞག་ནིའི་ཐབས་ལམ་ལག་ལེན་འཐབ་པའི་སྐབས་ གཟུགས་བརྙན་དང་པ་", "གཟུགས་བརྙན་དང་པ་"),
        ("unscoped-overlap", 2, "མཐའ་ལུ་སྦྱར་ཏེ་བཞག་ནིའི་ཐབས་ལམ་ལག་ལེན་འཐབ་པའི་སྐབས་ གཟུགས་བརྙན་ཚུ་", "གཟུགས་བརྙན་ཚུ་"),
        ("guaranteed-crop-movement", 2, "སྤོ་འོང་།", "སྤོཝ་ཨིན།"),
        ("wrong-position-caption", 3, "«ས་གནས་ཏག་ཏག»", "«Exact position»"),
        ("wrong-coordinate-origin", 3, " 0 ལས་", " 1 ལས་"),
        ("missing-whole-pixels", 3, "ཧྲིལ་གྲངས་སྦེ་ ", ""),
        ("missing-other-position-preservation", 3, "གཟུགས་བརྙན་གཞན་ཚུ་ རང་རང་གི་ད་ལྟོའི་ས་གནས་ནང་རང་སྡོདཔ་ཨིན། ", ""),
        ("missing-exact-overlap-permission", 3, "ནཱ་ལུ་གཟུགས་བརྙན་ཚུ་གཅིག་གི་ཐོག་ཁར་གཅིག་བཞག་ཆོག།", ""),
        ("guaranteed-gap-movement", 5, "སྤོ་འོང་།", "སྤོཝ་ཨིན།"),
        ("missing-size-offer-condition", 6, "གདམ་ཁ་བྱིན་པ་ཅིན་", ""),
    ),
}


def plain_help(root):
    nodes = root.findall(f"./*[@name='{KEY}']")
    if (len(nodes) != 1 or nodes[0].tag != "string" or
            nodes[0].attrib != {"name": KEY} or len(nodes[0])):
        raise ValueError("Expected one plain Help string with unchanged attributes")
    return nodes[0].text or ""


def require_bound_help(source_root, local_root, directory):
    source, value = plain_help(source_root), plain_help(local_root)
    if sha256(source.encode("utf-8")).hexdigest() != SOURCE_SHA256:
        raise ValueError("English Help changed; independent source-bound re-review required")
    if sha256(value.encode("utf-8")).hexdigest() != ACCEPTED[directory]:
        raise ValueError("Complete Help differs from the independently accepted value")
    return value


class AssemblyHelpCebuanoDzongkhaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ET.parse(RES / "values/strings.xml").getroot()
        cls.roots = {d: ET.parse(RES / d / "strings.xml").getroot() for d in ACCEPTED}

    def test_complete_values_source_shape_and_current_captions(self):
        self.assertEqual({"values-b+ceb", "values-b+dz"}, set(ACCEPTED))
        for directory, root in self.roots.items():
            with self.subTest(directory=directory):
                value = require_bound_help(self.source, root, directory)
                paragraphs = value.split(r"\n\n")
                self.assertEqual(8, len(paragraphs))
                self.assertEqual(14, value.count(r"\n"))
                self.assertFalse(any(c in value for c in ("\n", "\r", "\ufffd")))
                for index, keys in CAPTIONS.items():
                    for key in keys:
                        nodes = root.findall(f"./string[@name='{key}']")
                        self.assertEqual(1, len(nodes), key)
                        self.assertTrue(nodes[0].text, key)
                        self.assertIn(nodes[0].text, paragraphs[index], key)
                self.assertIn("Catrobat/AGPL", paragraphs[7])

    def test_mode_and_offer_mutations_are_rejected(self):
        for directory, root in self.roots.items():
            original = require_bound_help(self.source, root, directory)
            for name, index, before, after in MUTATIONS[directory]:
                with self.subTest(directory=directory, mutation=name):
                    parts = original.split(r"\n\n")
                    self.assertEqual(1, parts[index].count(before))
                    parts[index] = parts[index].replace(before, after, 1)
                    broken = deepcopy(root)
                    broken.find(f"./string[@name='{KEY}']").text = r"\n\n".join(parts)
                    with self.assertRaises(ValueError):
                        require_bound_help(self.source, broken, directory)

    def test_every_paragraph_is_required_including_inherited_material(self):
        for directory, root in self.roots.items():
            parts = require_bound_help(self.source, root, directory).split(r"\n\n")
            for index in range(8):
                with self.subTest(directory=directory, missing_paragraph=index):
                    broken = deepcopy(root)
                    broken.find(f"./string[@name='{KEY}']").text = r"\n\n".join(parts[:index] + parts[index + 1:])
                    with self.assertRaises(ValueError):
                        require_bound_help(self.source, broken, directory)

    def test_source_and_target_corruption_are_rejected(self):
        for directory, root in self.roots.items():
            for target in ("source", "localized"):
                for mutation in ("truncated", "duplicate", "missing", "attribute", "markup", "tag"):
                    source, local = deepcopy(self.source), deepcopy(root)
                    broken = source if target == "source" else local
                    node = broken.find(f"./string[@name='{KEY}']")
                    if mutation == "truncated": node.text = node.text[:-1]
                    elif mutation == "duplicate": broken.append(deepcopy(node))
                    elif mutation == "missing": broken.remove(node)
                    elif mutation == "attribute": node.set("formatted", "false")
                    elif mutation == "markup": ET.SubElement(node, "b")
                    elif mutation == "tag": node.tag = "plurals"
                    with self.subTest(directory=directory, target=target, mutation=mutation):
                        with self.assertRaises(ValueError):
                            require_bound_help(source, local, directory)


if __name__ == "__main__":
    unittest.main()
