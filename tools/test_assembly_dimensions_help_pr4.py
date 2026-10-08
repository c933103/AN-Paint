"""Protect PR #4's reviewed tray-dimension clauses.

The tray uses AssemblyImage.placedSize: crop dimensions when normalization is
unset, otherwise dimensions after Same width / Same height normalization.
Only the first help paragraph describes the tray. Later control descriptions
must not hide an omission there. These are narrow wording/contract regressions,
not a general translation-quality classifier. Android XML remains canonical.
"""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET


RES = Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"
ASSEMBLY = "ui_add_up_to_20_images_with_android_s"
# directory: (obsolete crop-only clause, reviewed crop + normalization clause)
# Resolve captions from each current local catalogue rather than hard-code a
# second set of labels; a control rename requires updating its help reference.
DIMENSION_HELP = {
    "values-sw": (
        "vipimo vya ukataji",
        "vipimo vya picha baada ya ukataji na marekebisho yoyote ya “{width}” au “{height}”",
    ),
    "values-fi": (
        "rajausmitat",
        "kuvien mitat rajauksen ja mahdollisten koonsäätöjen (”{width}” tai ”{height}”) jälkeen",
    ),
    "values-hu": (
        "vágási méreteket",
        "a képek vágás és az esetleges „{width}” vagy „{height}” beállítás utáni méreteit",
    ),
    "values-b+af": (
        "sny-afmetings",
        "beeldafmetings ná sny en enige aanpassing met “{width}” of “{height}”",
    ),
    "values-nl": (
        "uitsnijafmetingen",
        "afbeeldingsafmetingen na het uitsnijden en eventuele aanpassingen met ‘{width}’ of ‘{height}’",
    ),
    "values-b+et": (
        "kärpemõõtmeid",
        "piltide mõõtmeid pärast kärpimist ja võimalikke kohandusi valikutega „{width}” või „{height}”",
    ),
    "values-b+lv": (
        "apgriešanas izmērus",
        "attēlu izmērus pēc apgriešanas un jebkādiem pielāgojumiem ar opciju „{width}” vai „{height}”",
    ),
    "values-lt": (
        "apkirpimo matmenys",
        "vaizdų matmenys po apkirpimo ir bet kokių dydžio pakeitimų naudojant „{width}“ arba „{height}“",
    ),
}


class AssemblyDimensionsHelpPr4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogues = {}
        for directory in DIMENSION_HELP:
            root = ET.parse(RES / directory / "strings.xml").getroot()
            local = {}
            for key in (ASSEMBLY, "ui_same_width", "ui_same_height"):
                nodes = root.findall(f"string[@name='{key}']")
                if len(nodes) != 1:
                    raise AssertionError(f"{directory}: expected exactly one {key}")
                local[key] = "".join(nodes[0].itertext())
            cls.catalogues[directory] = local

    def first_paragraph(self, directory):
        return re.split(r"\\n\\n|\n\s*\n", self.catalogues[directory][ASSEMBLY])[0]

    def test_tray_dimension_clause_includes_crop_and_normalization(self):
        for directory, (_, template) in DIMENSION_HELP.items():
            local = self.catalogues[directory]
            expected = template.format(width=local["ui_same_width"], height=local["ui_same_height"])
            with self.subTest(locale=directory):
                self.assertIn(expected, self.first_paragraph(directory))

    def test_tray_paragraph_names_both_actual_size_controls(self):
        for directory, local in self.catalogues.items():
            for key in ("ui_same_width", "ui_same_height"):
                with self.subTest(locale=directory, control=key):
                    self.assertIn(local[key], self.first_paragraph(directory))

    def test_old_crop_only_dimension_description_does_not_return(self):
        for directory, (old, _) in DIMENSION_HELP.items():
            with self.subTest(locale=directory):
                self.assertNotIn(old, self.first_paragraph(directory))


if __name__ == "__main__":
    unittest.main()
