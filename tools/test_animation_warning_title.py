#!/usr/bin/env python3
"""A01 source/resource wiring guards only; dialog execution is ImportSelectionTitleTest."""
from pathlib import Path
import re
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
    def test_real_dialog_uses_count_threshold_and_existing_localized_title_keys(self):
        source = SOURCE.read_text()
        animation = source.split("private fun showAnimation(info: AnimationInfo) {", 1)[1].split("private fun showPages", 1)[0]
        compact = re.sub(r"\s+", "", animation)
        self.assertEqual(1, compact.count(
            ".setTitle(ui(if(info.frameCount<2)R.string.formats22_open_stillelseR.string.formats22_animation_title))"))
        self.assertNotIn('"Open still image"', animation)
        self.assertNotIn('"Animated image"', animation)

    def test_body_count_apng_action_and_null_probe_routes_remain_present(self):
        source = re.sub(r"\s+", "", SOURCE.read_text())
        for expected in (
            "valframes=if(info.frameCountExact)info.frameCount.toString()elseui(R.string.formats22_at_least_frames,info.frameCount)",
            "valmessage=if(info.frameCount<2)ui(R.string.formats22_animation_unknown,info.format)else",
            "ui(if(info.pngDefaultImageSeparate)R.string.formats22_animation_posterelseR.string.formats22_animation_still)",
            ".setPositiveButton(ui(R.string.formats22_open_still)){_,_->finishSelection(0)}",
            ".setNegativeButton(ui(R.string.ui_cancel)){_,_->cancel()}.setOnCancelListener{cancel()}",
            "elseif(animation!=null)showAnimation(animation)elsefinishSelection(0)",
        ):
            self.assertIn(expected, source)

    def test_english_and_portuguese_titles_have_independent_wording_oracles(self):
        for folder, expected in (
            ("values", ("Open still image", "Animated image")),
            ("values-pt-rBR", ("Abrir imagem estática", "Imagem animada")),
        ):
            values = strings(RES / folder)
            self.assertEqual(expected[0], values["formats22_open_still"])
            self.assertEqual(expected[1], values["formats22_animation_title"])

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

    def test_welsh_fixture_exercises_real_default_resource_fallback(self):
        values = strings(RES / "values-b+cy")
        for key in ("formats22_open_still", "formats22_animation_title", "formats22_animation_unknown"):
            self.assertNotIn(key, values)
            self.assertIn(key, strings(RES / "values"))
        arrays = ET.parse(RES / "values/app_language_tags.xml").getroot()
        offered = arrays.find("string-array[@name='app_language_tags']")
        self.assertIn("cy", [node.text for node in offered])


if __name__ == "__main__":
    unittest.main()
