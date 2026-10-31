"""Complete bounded Sinitic crop warnings, not whole-catalogue acceptance."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from translation_catalogues import android_string_errors, placeholders

RES = Path(__file__).resolve().parents[1] / 'Paintroid/src/main/res'
KEY = 'ui_crop_preview_images'
EXPECTED = {
    'values-zh-rTW': r'預覽：%1$d × %2$d px\n套用至 %3$d 張圖片。裁切已放置圖片時，連接到它們的圖片可能會移動。',
    'values-zh-rCN': r'预览：%1$d × %2$d px\n应用到 %3$d 张图片。裁剪已放置图片时，连接到它们的图片可能会移动。',
    'values-b+yue+Hant': r'預覽：%1$d × %2$d px\n套用去 %3$d 張圖片。裁剪已經擺好嘅圖片時，連住佢哋嘅圖片可能會移動。',
    'values-b+yue+Latn': r'Jyu6 laam5: %1$d × %2$d px\nTou3 jung6 heoi3 %3$d zoeng1 tou4 pin2. Coi4 zin2 ji5 ging1 baai2 hou2 ge3 tou4 pin2 si4, lin4 zyu6 keoi5 dei6 ge3 tou4 pin2 ho2 nang4 wui5 ji4 dung6.',
    'values-b+lzh+Hant': r'預覽：%1$d × %2$d px\n施於 %3$d 圖。裁已置之圖，所連諸圖或因之而移。',
    'values-b+nan+Hant+TW': r'預覽：%1$d × %2$d px\n套用佇 %3$d 張圖片。裁囥好的圖片時，接佇怹的圖片可能會移動。',
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
                root=ET.parse(RES / folder / 'strings.xml').getroot()
                require_warning(root,expected)

    def test_dimensions_quantity_newline_and_android_escaping_are_preserved(self):
        source = ET.parse(RES / 'values/strings.xml').find(f"plurals[@name='{KEY}']/item").text
        for folder in (*EXPECTED, 'values-b+nan+Latn+TW'):
            actual = ET.parse(RES / folder / 'strings.xml').find(f"plurals[@name='{KEY}']/item").text
            with self.subTest(folder=folder):
                self.assertEqual(placeholders(source), placeholders(actual))
                self.assertEqual(1, actual.count(r'\n'))
                self.assertEqual([], android_string_errors(actual))

    def test_full_value_guard_rejects_old_categorical_and_damaged_messages(self):
        mutations = {
            'values-zh-rTW': ('連接到它們的圖片可能會移動。', '連接圖片的位置也會重新調整。'),
            'values-zh-rCN': ('连接到它们的图片可能会移动。', '连接图片的位置也会重新调整。'),
            'values-b+yue+Hant': (EXPECTED['values-b+yue+Hant'], r'預覽：%1$d × %2$d px\n套用去 %3$d 張圖片。裁剪已擺位嘅圖片時，連接圖片嘅位置都會再調整。'),
            'values-b+yue+Latn': (EXPECTED['values-b+yue+Latn'], r'Jyu6 laam5:%1$d ×%2$d px\ntou3 jung6 heoi3%3$d zoeng1 tou4 pin2. coi4 zin2 ji5 baai2 wai6 ge3 tou4 pin2 si4, lin4 zip3 tou4 pin2 ge3 wai6 zi3 dou1 wui5 zoi3 diu6 zing2.'),
            'values-b+lzh+Hant': (EXPECTED['values-b+lzh+Hant'], r'預覽：%1$d × %2$d px\n施於 %3$d 圖。裁已置之圖，所連諸圖亦隨之移。'),
            'values-b+nan+Hant+TW': (EXPECTED['values-b+nan+Hant+TW'], r'預覽：%1$d × %2$d px\n套用佇 %3$d 張圖片。裁揀著的圖片時，連咧的圖片位置嘛會閣調整。'),
        }
        for folder, expected in EXPECTED.items():
            old = expected.replace(*mutations[folder])
            for damaged in (old, expected.replace('%3$d', '%3$s'), expected.split(r'\n')[1],
                            expected.replace('可能會', '').replace('可能会', '').replace('ho2 nang4 ', '').replace('或因之', '因之').replace('khó-lêng ', '')):
                with self.subTest(folder=folder, damaged=damaged):
                    self.assertNotEqual(expected, damaged)
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


if __name__ == '__main__':
    unittest.main()
