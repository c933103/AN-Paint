"""Full external-link messages and explicit fallback scope; runtime branches use GalleryExternalLinkTest.

Exact wording fixtures preserve reviewed statements, not certification of whole
catalogues, native idiom, rendered text or installed-device behavior.
"""
from pathlib import Path
import json
import unittest

import current_localization_contracts as contracts
import translation_catalogues as catalogues

ROOT = Path(__file__).resolve().parents[1]
KEY = "gallery_external_link_no_handler"
SOURCE = "Android could not find an app to open this link."


class GalleryExternalLinkWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scope = contracts.fixture("locale_contract_scope.json")
        cls.wording = contracts.fixture("gallery_external_link_current_wording.json")

    def test_only_reviewed_swedish_extends_this_family(self):
        self.assertEqual(['sv'], self.wording['additional_reviewed_tags'])

    def test_complete_independent_wording_and_scope(self):
        expected_tags = {"default", *self.scope["scoped_tags"], *self.wording["additional_reviewed_tags"]}
        contracts.require_wording_shape(self.wording, {KEY}, expected_tags)
        self.assertEqual(SOURCE, self.wording["values"][KEY]["default"])
        catalogues_by_tag = catalogues.catalogue_paths()
        for tag, expected in self.wording["values"][KEY].items():
            with self.subTest(tag=tag):
                path = catalogues.RES / "values/strings.xml" if tag == "default" else catalogues_by_tag[tag]
                contracts.require_string(path.read_text(), KEY, expected, self.wording["constraints"][KEY])

    def test_every_outside_scope_catalogue_keeps_explicit_english_fallback(self):
        offered = set(catalogues.offered_tags())
        scoped = set(self.scope["scoped_tags"])
        fallback = set(self.scope["fallback_tags"])
        self.assertFalse(scoped & fallback)
        self.assertEqual(offered, scoped | fallback)
        paths = catalogues.catalogue_paths()
        for tag in sorted(fallback - set(self.wording["additional_reviewed_tags"])):
            with self.subTest(tag=tag):
                self.assertNotIn(KEY, catalogues.read_strings(paths[tag]))
        self.assertEqual(SOURCE, catalogues.read_strings(catalogues.RES / "values/strings.xml")[KEY])

    def test_gallery_load_error_remains_a_distinct_resource(self):
        source = catalogues.read_strings(catalogues.RES / "values/strings.xml")
        self.assertEqual("The online gallery could not be loaded. Check your connection and try again.",
                         source["ui_the_online_gallery_could_not_be_loaded_check"])
        self.assertNotEqual(source[KEY], source["ui_the_online_gallery_could_not_be_loaded_check"])
        importance = json.loads((ROOT / "translations/string-importance.json").read_text())
        assigned = {key: tier["id"] for tier in importance["tiers"] for key in tier["keys"]}
        self.assertEqual("P2", assigned["string/" + KEY])

    def test_wrong_cause_missing_or_duplicate_resource_is_rejected(self):
        constraint = self.wording["constraints"][KEY]
        for body in (
            "",
            f'<string name="{KEY}">Check your connection.</string>',
            f'<string name="{KEY}">{SOURCE}</string>' * 2,
        ):
            with self.subTest(body=body):
                with self.assertRaises(ValueError):
                    contracts.require_string("<resources>" + body + "</resources>", KEY, SOURCE, constraint)


if __name__ == "__main__":
    unittest.main()
