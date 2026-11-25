"""Protect Batch Crop's selected count and conditional attached-image warning."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from translation_catalogues import android_string_errors, placeholders

RES = Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"
# Quantities, then minimal meaning markers: selected (before the count),
# attachment and possibility (in the warning). Do not copy the prose.
CASES = {
    "b+ia": (("one", "other"), "selig", "attach", "pote"),
    "b+ast": (("one", "other"), "escoy", "xuní", "pue"),
    "gl": (("one", "other"), "seleccion", "anex", "pode"),
    "ca": (("one", "other"), "seleccion", "connect", "pot"),
    "b+ca+ES+valencia": (("one", "many", "other"), "seleccion", "adjunt", "pot"),
    "b+oc": (("other",), "seleccion", "estac", "pòt"),
    "ro": (("one", "few", "other"), "select", "ataș", "poate"),
    "ru": (("one", "few", "many", "other"), "выбран", "присоедин", "могут"),
}


class CropSelectionStatusCompanionsTest(unittest.TestCase):
    def test_quantities_keep_dimensions_selected_count_and_bounded_warning(self):
        for tag, (forms, selected, attached, possible) in CASES.items():
            with self.subTest(locale=tag):
                root = ET.parse(RES / f"values-{tag}" / "strings.xml")
                items = root.findall("plurals[@name='ui_crop_preview_images']/item")
                self.assertCountEqual(forms, [item.attrib["quantity"] for item in items])
                for item in items:
                    text = item.text.strip('"')
                    preview, detail = text.casefold().split(r"\n")
                    status, warning = detail.split("%3$d")
                    self.assertCountEqual(placeholders("%1$d %2$d"), placeholders(preview))
                    self.assertCountEqual(placeholders("%1$d %2$d %3$d"), placeholders(text))
                    self.assertIn(selected, status)
                    self.assertIn(attached, warning)
                    self.assertIn(possible, warning)
                    self.assertEqual([], android_string_errors(text))
