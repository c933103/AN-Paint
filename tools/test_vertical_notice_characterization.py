"""Compatibility of retained vertical resource fixture with current canonical XML."""
from pathlib import Path
import json
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "Paintroid/src/test/resources/vertical-notice-resize/expected-resources.json"
TAGS = {"mn-Mong", "mnc-Mong", "lzh-Hant", "en-XV", "qaa-Zsye-XV"}
KEYS = {"ui_cursor_pan_move32", "ui_cursor_tap_hint37", "ui_saved"}

class VerticalNoticeCharacterizationContractTest(unittest.TestCase):

    def test_resource_oracle_matches_five_current_exact_catalogues(self):
        oracle = json.loads(ORACLE.read_text())
        self.assertEqual(TAGS, set(oracle["locales"]))
        for tag, values in oracle["locales"].items():
            with self.subTest(tag=tag):
                path = ROOT / "Paintroid/src/main/res" / ("values-b+" + tag.replace("-", "+")) / "strings.xml"
                entries = {e.get("name"): "".join(e.itertext()).replace("\\n", "\n")
                           .replace("\\'", "'").replace('\\"', '"')
                           for e in ET.parse(path).getroot().findall("string")}
                self.assertEqual(KEYS, set(values))
                self.assertEqual(values, {key: entries[key] for key in KEYS})
                self.assertEqual(1, (values["ui_cursor_pan_move32"] + "\n"
                                     + values["ui_cursor_tap_hint37"]).count("\n"))
                self.assertEqual(1, values["ui_saved"].count("%1$s"))

if __name__ == "__main__":
    unittest.main(verbosity=2)
