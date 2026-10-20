"""One complete empty-credit diagnostic in every affected canonical catalogue.

These source/resource contracts complement CommonsCreditFlowTest's offline
Android UI flow; they do not execute it or certify whole-language fluency.
"""
from pathlib import Path
import unittest

import current_localization_contracts as contracts
import translation_catalogues as catalogues

ROOT = Path(__file__).resolve().parents[1]
KEY = "ui_no_gallery_images_have_been_inserted"
SOURCE = "No image credit text is available."


class GalleryEmptyCreditWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scope = contracts.fixture("locale_contract_scope.json")
        cls.wording = contracts.fixture("gallery_empty_credit_current_wording.json")

    def test_only_reviewed_swedish_extends_this_family(self):
        self.assertEqual(['sv'], self.wording['additional_reviewed_tags'])

    def test_every_complete_affected_resource_matches_its_reviewed_text(self):
        tags = {"default", *self.scope["scoped_tags"], *self.wording["additional_reviewed_tags"]}
        contracts.require_wording_shape(self.wording, {KEY}, tags)
        self.assertEqual(SOURCE, self.wording["values"][KEY]["default"])
        paths = {"default": catalogues.RES / "values/strings.xml", **catalogues.catalogue_paths()}
        present = {tag for tag, path in paths.items() if KEY in catalogues.read_strings(path)}
        self.assertEqual(tags, present)
        for tag, expected in self.wording["values"][KEY].items():
            with self.subTest(tag=tag):
                contracts.require_string(paths[tag].read_text(), KEY, expected,
                                         self.wording["constraints"][KEY])

    def test_untranslated_picker_locales_keep_default_english_fallback(self):
        scoped = set(self.scope["scoped_tags"])
        fallback = set(self.scope["fallback_tags"])
        self.assertFalse(scoped & fallback)
        self.assertEqual(set(catalogues.offered_tags()), scoped | fallback)
        paths = catalogues.catalogue_paths()
        for tag in fallback - set(self.wording["additional_reviewed_tags"]):
            with self.subTest(tag=tag):
                self.assertNotIn(KEY, catalogues.read_strings(paths[tag]))
        self.assertEqual(SOURCE, catalogues.read_strings(catalogues.RES / "values/strings.xml")[KEY])

    def test_missing_duplicate_old_cause_or_format_argument_is_rejected(self):
        for body in (
            "",
            f'<string name="{KEY}">No gallery images have been inserted.</string>',
            f'<string name="{KEY}">{SOURCE}</string>' * 2,
            f'<string name="{KEY}">{SOURCE} %1$s</string>',
        ):
            with self.subTest(body=body), self.assertRaises(ValueError):
                contracts.require_string("<resources>" + body + "</resources>", KEY, SOURCE,
                                         self.wording["constraints"][KEY])

    def test_english_variants_and_emoji_keep_the_same_neutral_diagnosis(self):
        values = self.wording["values"][KEY]
        for tag in self.scope["scoped_tags"]:
            if tag.startswith("en-"):
                self.assertEqual(SOURCE, values[tag], tag)
        self.assertEqual("🖼️ " + SOURCE, values["qaa-Zsye-XV"])


if __name__ == "__main__":
    unittest.main()
