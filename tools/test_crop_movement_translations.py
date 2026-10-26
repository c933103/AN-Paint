"""Complete crop-warning quantity oracles for four reviewed resources.

These checks retain every XML form, including forms not selected by Android's
integer quantity API. They do not certify other catalogue text or rendered UI.
"""
import pathlib
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED = {
    "lt": {
        "one": "Peržiūra: %1$d × %2$d px\\nTaikyti %3$d vaizdui. Apkirpus išdėstytą vaizdą, prie jo prijungti vaizdai gali pasislinkti.",
        "few": "Peržiūra: %1$d × %2$d px\\nTaikyti %3$d vaizdams. Apkirpus išdėstytus vaizdus, prie jų prijungti vaizdai gali pasislinkti.",
        "other": "Peržiūra: %1$d × %2$d px\\nTaikyti %3$d vaizdų. Apkirpus išdėstytus vaizdus, prie jų prijungti vaizdai gali pasislinkti.",
    },
    "ar": {
        "zero": "المعاينة: %1$d × %2$d px\\nعدد الصور التي سيُطبَّق عليها القص: %3$d. قد يؤدي قص الصور الموضوعة إلى تحريك الصور المتصلة بها.",
        "one": "المعاينة: %1$d × %2$d px\\nعدد الصور التي سيُطبَّق عليها القص: %3$d. قد يؤدي قص الصور الموضوعة إلى تحريك الصور المتصلة بها.",
        "two": "المعاينة: %1$d × %2$d px\\nعدد الصور التي سيُطبَّق عليها القص: %3$d. قد يؤدي قص الصور الموضوعة إلى تحريك الصور المتصلة بها.",
        "few": "المعاينة: %1$d × %2$d px\\nتُطبق على %3$d صور. قد يؤدي قص الصور الموضوعة إلى تحريك الصور المتصلة بها.",
        "many": "المعاينة: %1$d × %2$d px\\nتُطبق على %3$d صورة. قد يؤدي قص الصور الموضوعة إلى تحريك الصور المتصلة بها.",
        "other": "المعاينة: %1$d × %2$d px\\nتُطبق على %3$d صورة. قد يؤدي قص الصور الموضوعة إلى تحريك الصور المتصلة بها.",
    },
    "ru": {
        "one": "Предпросмотр: %1$d × %2$d px\\nПрименить к %3$d изображению. При обрезке размещённых изображений присоединённые к ним изображения могут переместиться.",
        "few": "Предпросмотр: %1$d × %2$d px\\nПрименить к %3$d изображениям. При обрезке размещённых изображений присоединённые к ним изображения могут переместиться.",
        "many": "Предпросмотр: %1$d × %2$d px\\nИзображений для обрезки: %3$d. При обрезке размещённых изображений присоединённые к ним изображения могут переместиться.",
        "other": "Предпросмотр: %1$d × %2$d px\\nПрименить к %3$d изображениям. При обрезке размещённых изображений присоединённые к ним изображения могут переместиться.",
    },
    "ja": {
        "other": "プレビュー: %1$d × %2$d px\\n%3$d 枚の画像に適用します。配置済み画像をトリミングすると、接続された画像が移動する場合があります。",
    },
}


class CropMovementTranslationTests(unittest.TestCase):
    def test_complete_warning_forms_preserve_dimensions_count_and_optional_image_movement(self):
        for tag, expected in EXPECTED.items():
            with self.subTest(tag=tag):
                path = ROOT / "Paintroid/src/main/res" / ("values-" + tag) / "strings.xml"
                nodes = ET.parse(path).getroot().findall("./plurals[@name='ui_crop_preview_images']")
                self.assertEqual(1, len(nodes))
                items = list(nodes[0])
                self.assertEqual(len(expected), len(items))
                actual = {item.attrib["quantity"]: "".join(item.itertext()) for item in items}
                self.assertEqual(expected, actual)
                for quantity, text in actual.items():
                    with self.subTest(tag=tag, quantity=quantity):
                        self.assertEqual(["%1$d", "%2$d", "%3$d"], re.findall(r"%[1-9]\d*\$d", text))
                        self.assertEqual(1, text.count(r"\n"))
                        self.assertIn(" × ", text)
                        self.assertNotIn("\n", text)


if __name__ == "__main__":
    unittest.main()
