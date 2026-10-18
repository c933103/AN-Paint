"""Complete bounded TW/CN crop warnings, not whole-catalogue acceptance."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from translation_catalogues import android_string_errors, placeholders

RES = Path(__file__).resolve().parents[1] / 'Paintroid/src/main/res'
KEY = 'ui_crop_preview_images'
EXPECTED = {
    'values-zh-rTW': r'預覽：%1$d × %2$d px\n套用至 %3$d 張圖片。裁切已放置圖片時，連接到它們的圖片可能會移動。',
    'values-zh-rCN': r'预览：%1$d × %2$d px\n应用到 %3$d 张图片。裁剪已放置图片时，连接到它们的图片可能会移动。',
}


def require_warning(root, expected):
    nodes = root.findall(f"./plurals[@name='{KEY}']")
    if len(nodes) != 1:
        raise ValueError('Missing or duplicated crop warning')
    items = list(nodes[0])
    if len(items) != 1 or items[0].tag != 'item' or items[0].attrib != {'quantity': 'other'}:
        raise ValueError('Expected exactly one Chinese other form')
    if ''.join(items[0].itertext()) != expected:
        raise ValueError('Complete warning changed')


class ChineseCropWarningTest(unittest.TestCase):
    def test_complete_values_name_attached_images_and_qualify_movement(self):
        for folder, expected in EXPECTED.items():
            with self.subTest(folder=folder):
                require_warning(ET.parse(RES / folder / 'strings.xml').getroot(), expected)

    def test_dimensions_quantity_newline_and_android_escaping_are_preserved(self):
        source = ET.parse(RES / 'values/strings.xml').find(f"plurals[@name='{KEY}']/item").text
        for folder in EXPECTED:
            actual = ET.parse(RES / folder / 'strings.xml').find(f"plurals[@name='{KEY}']/item").text
            with self.subTest(folder=folder):
                self.assertEqual(placeholders(source), placeholders(actual))
                self.assertEqual(1, actual.count(r'\n'))
                self.assertEqual([], android_string_errors(actual))

    def test_full_value_guard_rejects_old_categorical_and_damaged_messages(self):
        mutations = {
            'values-zh-rTW': ('連接到它們的圖片可能會移動。', '連接圖片的位置也會重新調整。'),
            'values-zh-rCN': ('连接到它们的图片可能会移动。', '连接图片的位置也会重新调整。'),
        }
        for folder, expected in EXPECTED.items():
            old = expected.replace(*mutations[folder])
            for damaged in (old, expected.replace('%3$d', '%3$s'), expected.split(r'\n')[1],
                            expected.replace('可能會', '').replace('可能会', '')):
                with self.subTest(folder=folder, damaged=damaged):
                    root = ET.Element('resources')
                    plural = ET.SubElement(root, 'plurals', name=KEY)
                    ET.SubElement(plural, 'item', quantity='other').text = damaged
                    with self.assertRaises(ValueError):
                        require_warning(root, expected)

    def test_full_value_guard_rejects_missing_and_duplicate_forms(self):
        for expected in EXPECTED.values():
            root = ET.Element('resources')
            with self.assertRaises(ValueError):
                require_warning(root, expected)
            plural = ET.SubElement(root, 'plurals', name=KEY)
            with self.assertRaises(ValueError):
                require_warning(root, expected)
            ET.SubElement(plural, 'item', quantity='other').text = expected
            require_warning(root, expected)
            ET.SubElement(plural, 'item', quantity='one').text = expected
            with self.assertRaises(ValueError):
                require_warning(root, expected)


if __name__ == '__main__':
    unittest.main()
