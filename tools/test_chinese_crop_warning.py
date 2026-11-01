"""Sinitic crop object/modality and typed-dimension boundaries, not prose approval."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from translation_catalogues import android_string_errors, placeholders

RES = Path(__file__).resolve().parents[1] / 'Paintroid/src/main/res'
KEY = 'ui_crop_preview_images'
# Independently meaningful attached-object and possibility markers, not complete warnings.
SEMANTICS = {
    'values-zh-rTW': ('連接到它們的圖片', '可能會移動'),
    'values-zh-rCN': ('连接到它们的图片', '可能会移动'),
    'values-b+yue+Hant': ('連住佢哋嘅圖片', '可能會移動'),
    'values-b+yue+Latn': ('lin4 zyu6 keoi5 dei6 ge3 tou4 pin2', 'ho2 nang4 wui5 ji4 dung6'),
    'values-b+lzh+Hant': ('所連諸圖', '或因之而移'),
    'values-b+nan+Hant+TW': ('接佇怹的圖片', '可能會移動'),
}

class ChineseCropWarningTest(unittest.TestCase):
    def test_attached_images_are_the_objects_that_may_move(self):
        for folder, clauses in SEMANTICS.items():
            items = ET.parse(RES / folder / 'strings.xml').findall(f"./plurals[@name='{KEY}']/item")
            self.assertEqual(['other'], [n.get('quantity') for n in items])
            for clause in clauses:
                self.assertIn(clause, items[0].text)

    def test_dimensions_quantity_newline_and_android_escaping_are_preserved(self):
        source = ET.parse(RES / 'values/strings.xml').find(f"plurals[@name='{KEY}']/item").text
        for folder in (*SEMANTICS, 'values-b+nan+Latn+TW'):
            actual = ET.parse(RES / folder / 'strings.xml').find(f"plurals[@name='{KEY}']/item").text
            with self.subTest(folder=folder):
                self.assertEqual(placeholders(source), placeholders(actual))
                self.assertEqual(1, actual.count(r'\n'))
                self.assertEqual([], android_string_errors(actual))

    def test_nan_warning_names_attached_images_and_qualifies_possible_movement(self):
        root = ET.parse(RES / 'values-b+nan+Latn+TW/strings.xml').getroot()
        plural = root.find(f"./plurals[@name='{KEY}']")
        self.assertIsNotNone(plural)
        self.assertEqual(['other'], [node.get('quantity') for node in plural])
        value = plural[0].text
        # The independently specified distinction is attached OTHER images that MAY move,
        # not a copied complete approval sentence or predecessor binding.
        for clause in ('chi̍t tiuⁿ khǹg-hó ê tô͘-phìⁿ', 'chiap tī hit tiuⁿ tô͘-phìⁿ',
                       'kî-tha tô͘-phìⁿ', 'khó-lêng ē î-tōng'):
            self.assertIn(clause, value)
        self.assertNotIn('lóng ē', value)

if __name__ == "__main__":
    unittest.main()
