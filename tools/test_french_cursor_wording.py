"""Bounded French cursor wording; Android interaction evidence is in the JVM tests."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "ui_cursor_help31": "Faites glisser pour positionner le curseur. Touchez le bouton de dessin à l’écran, puis faites glisser pour dessiner. Touchez-le à nouveau pour arrêter. Choisissez le pinceau et les réglages du trait sous Dessiner → Dessin.",
    "ui_cursor_pan_draw32": "Faites glisser pour commencer à dessiner. Touchez à nouveau pour arrêter.",
    "ui_cursor_pan_move32": "Faites glisser pour positionner le curseur. Touchez le bouton de dessin pour commencer.",
}


class FrenchCursorWordingTest(unittest.TestCase):
    def test_complete_values_keep_metadata_and_alias(self):
        resources = ET.parse(ROOT / "Paintroid/src/main/res/values-fr/strings.xml").getroot()
        strings = {item.get("name"): item for item in resources.findall("string")}
        for key, expected in EXPECTED.items():
            with self.subTest(key=key):
                self.assertEqual(expected, strings[key].text)
                self.assertEqual("false", strings[key].get("formatted"))
        self.assertEqual("@string/ui_cursor_help31", strings["ui_cursor_help29"].text)


if __name__ == "__main__":
    unittest.main()
