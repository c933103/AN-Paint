#!/usr/bin/env python3
"""A01 source/resource wiring guards only; dialog execution is ImportSelectionTitleTest."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Paintroid/src/main/java/org/catrobat/paintroid/classic/ImportSelection.kt"
RES = ROOT / "Paintroid/src/main/res"

def strings(directory):
    values = {}
    for path in directory.glob("*.xml"):
        values.update((node.attrib["name"], "".join(node.itertext()))
                      for node in ET.parse(path).getroot().findall("string"))
    return values

class AnimationWarningTitleSourceTest(unittest.TestCase):

    def test_existing_catalogue_title_keys_are_nonempty_and_require_no_arguments(self):
        examined = 0
        for folder in RES.glob("values*"):
            values = strings(folder)
            for key in ("formats22_open_still", "formats22_animation_title"):
                if key not in values:
                    continue  # Catalogue absence is not language completeness.
                examined += 1
                self.assertTrue(values[key].strip(), (folder.name, key))
                self.assertNotRegex(values[key], r"%(?:\d+\$)?[a-zA-Z]", (folder.name, key))
        self.assertGreater(examined, 2)

if __name__ == "__main__":
    unittest.main()
