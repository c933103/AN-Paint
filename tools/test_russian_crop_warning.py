#!/usr/bin/env python3
"""Bounded Russian crop wording guards; Android selection is tested on the JVM.

These expectations preserve the reviewed warning's affected object and the
existing count cases. They do not certify the rest of the Russian catalogue.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from translation_catalogues import android_string_errors, placeholders

RES = Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"
KEY = "ui_crop_preview_images"
COUNT_FORMS = {'one': '%3$d изображению', 'few': '%3$d изображениям',
               'many': 'Изображений для обрезки: %3$d', 'other': '%3$d изображениям'}

def items(folder):
    resource = ET.parse(RES / folder / "strings.xml").find(f"plurals[@name='{KEY}']")
    return [(item.attrib["quantity"], "".join(item.itertext())) for item in resource]

class RussianCropWarningTest(unittest.TestCase):
    def test_all_four_categories_name_attached_images_as_the_moved_objects(self):
        actual = items("values-ru")
        self.assertEqual(set(COUNT_FORMS), {quantity for quantity, _ in actual})
        self.assertEqual(len(COUNT_FORMS), len(actual))
        for quantity, text in actual:
            with self.subTest(quantity=quantity):
                self.assertIn(COUNT_FORMS[quantity], text)
                self.assertIn('присоединённые к ним изображения', text)
                self.assertIn('могут переместиться', text)

    def test_preview_dimensions_count_newline_and_android_escaping_are_preserved(self):
        expected = placeholders(items("values")[0][1])
        for quantity, text in items("values-ru"):
            with self.subTest(quantity=quantity):
                self.assertEqual(expected, placeholders(text))
                self.assertEqual(1, text.count(r"\n"))
                self.assertEqual([], android_string_errors(text))

if __name__ == "__main__":
    unittest.main()
