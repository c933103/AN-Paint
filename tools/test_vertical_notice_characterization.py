"""Independent format boundaries for current vertical-notice resources.

Wording lives in canonical XML; runtime tests bind that text to actual cards.
The retired JSON prose mirror is preserved in Git history, not replayed here.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TAGS = {"mn-Mong", "mnc-Mong", "lzh-Hant", "en-XV", "qaa-Zsye-XV"}
KEYS = {"ui_cursor_pan_move32", "ui_cursor_tap_hint37", "ui_saved"}

class VerticalNoticeCharacterizationContractTest(unittest.TestCase):

    def test_current_exact_catalogues_keep_notice_format_boundaries(self):
        for tag in sorted(TAGS):
            with self.subTest(tag=tag):
                path = ROOT / "Paintroid/src/main/res" / ("values-b+" + tag.replace("-", "+")) / "strings.xml"
                nodes = [e for e in ET.parse(path).getroot().findall("string")
                         if e.get("name") in KEYS]
                self.assertEqual(len(KEYS), len(nodes), "Exactly one definition per notice key")
                values = {e.get("name"): "".join(e.itertext()).replace("\\n", "\n")
                          .replace("\\'", "'").replace('\\"', '"') for e in nodes}
                self.assertEqual(KEYS, set(values))
                self.assertTrue(all(value.strip() for value in values.values()))
                self.assertEqual(1, (values["ui_cursor_pan_move32"] + "\n"
                                     + values["ui_cursor_tap_hint37"]).count("\n"))
                self.assertEqual(1, values["ui_saved"].count("%1$s"))
                self.assertNotIn("%", values["ui_saved"].replace("%1$s", ""),
                                 "Only the filename placeholder belongs in a saved notice")

if __name__ == "__main__":
    unittest.main(verbosity=2)
