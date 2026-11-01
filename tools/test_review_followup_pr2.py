"""Targeted guards for PR #2's October 8 review findings, not fluency approval."""
import json
import re
import unittest

import translation_catalogues as catalogues

MANUAL = "ui_the_arrow_on_the_left_directly_below_the"

class ReviewFollowupPr2Tests(unittest.TestCase):

    def test_regional_english_font_counts_match_bundled_inventory(self):
        inventory = json.loads((catalogues.RES.parent / "assets/fonts/inventory.json").read_text())
        assets = {entry["asset"] for entry in inventory}
        self.assertEqual(len(inventory), len(assets))
        # The manual describes selectable drawing fonts, excluding UI-only subsets.
        drawing_assets = {entry["asset"] for entry in inventory
                          if not entry.get("ui_only", False)}
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
                self.assertEqual(len(drawing_assets), count)

if __name__ == "__main__":
    unittest.main()
