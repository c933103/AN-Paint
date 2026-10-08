"""Targeted guards for PR #2's October 8 review findings, not fluency approval."""
import json
import re
import unittest

import translation_catalogues as catalogues


ASSEMBLY = "ui_add_up_to_20_images_with_android_s"
MANUAL = "ui_the_arrow_on_the_left_directly_below_the"
ASSEMBLY_CLAUSES = {
    "ja": ("トリミングと［同じ幅］または［同じ高さ］の調整を反映した画像寸法",
           "サイズの選択画面の代わりにメモリ警告が表示されます",
           "出力がメモリ上限を超える場合は、小さい出力コピーを選択してください。"),
    "zh-CN": ("裁剪及「相同宽度」或「相同高度」调整后的图片尺寸",
              "应用会显示内存警告，而不会显示尺寸选择界面",
              "如果输出超出内存上限，请选择较小的输出副本。"),
    "zh-HK": ("裁剪及「相同闊度」或「相同高度」調整後的圖片尺寸",
              "應用程式會顯示記憶體警告，而不會顯示尺寸選擇畫面",
              "如果輸出超出記憶體上限，請選擇較小的輸出副本。"),
    "zh-TW": ("裁切及「相同寬度」或「相同高度」調整後的圖片尺寸",
              "應用程式會顯示記憶體警告，而不會顯示尺寸選擇畫面",
              "如果輸出超出記憶體上限，請選擇較小的輸出副本。"),
    "yue-Hant": ("裁剪同「一樣闊度」或者「一樣高度」調整後嘅圖片尺寸",
                 "程式會顯示記憶體警告，唔會顯示尺寸選擇畫面",
                 "如果輸出超出記憶體上限，請揀較小嘅輸出副本。"),
    "yue-Latn": ("coi4 zin2 tung4 “Jat1 joeng6 fut3 dou6” waak6 ze2 “Jat1 joeng6 gou1 dou6” tiu4 zing2 hau6 ge3 tou4 pin2 cek3 cyun3",
                 "cing4 sik1 wui5 hin2 si6 gei3 jik1 tai2 ging2 gou3, m4 wui5 hin2 si6 cek3 cyun3 syun2 zaak6 waa2 min6",
                 "jyu4 gwo2 syu1 ceot1 ciu1 ceot1 gei3 jik1 tai2 soeng6 haan6, cing2 gaan2 gaau3 siu2 ge3 syu1 ceot1 fu3 bun2."),
}


class ReviewFollowupPr2Tests(unittest.TestCase):
    def test_scoped_assembly_help_describes_normalization(self):
        paths = catalogues.catalogue_paths()
        for tag, (dimension, _, _) in ASSEMBLY_CLAUSES.items():
            with self.subTest(locale=tag):
                self.assertIn(dimension, catalogues.read_strings(paths[tag])[ASSEMBLY])

    def test_scoped_assembly_help_describes_warning_without_chooser(self):
        paths = catalogues.catalogue_paths()
        for tag, (_, warning, unconditional) in ASSEMBLY_CLAUSES.items():
            text = catalogues.read_strings(paths[tag])[ASSEMBLY]
            with self.subTest(locale=tag):
                self.assertIn(warning, text)
                self.assertNotIn(unconditional, text)

    def test_regional_english_font_counts_match_bundled_inventory(self):
        inventory = json.loads((catalogues.RES.parent / "assets/fonts/inventory.json").read_text())
        assets = {entry["asset"] for entry in inventory}
        self.assertEqual(len(inventory), len(assets))
        words = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()
        counts = {word: count for count, word in enumerate(words)}
        paths = catalogues.catalogue_paths()
        sources = {"default": catalogues.RES / "values/strings.xml"}
        sources.update({tag: paths[tag] for tag in ("en-001", "en-IN", "en-SG", "en-US")})
        for tag, path in sources.items():
            with self.subTest(locale=tag):
                text = catalogues.read_strings(path)[MANUAL]
                match = re.search(r"\b(\w+) additional fonts are bundled;", text)
                self.assertIsNotNone(match)
                value = match.group(1).lower()
                count = int(value) if value.isdecimal() else counts.get(value)
                self.assertEqual(len(assets), count)


if __name__ == "__main__":
    unittest.main()
