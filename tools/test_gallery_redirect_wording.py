"""Complete redirect-policy diagnostic values and explicit fallback scope.

Actual redirect-loop checks live in GalleryRedirectTest. Matching these resource
contracts does not certify native idiom, device rendering or live-provider behavior.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import current_localization_contracts as contracts
import translation_catalogues as catalogues

ROOT = Path(__file__).resolve().parents[1]
KEY = "ui_the_gallery_redirected_outside_its_supported_hosts"
SOURCE = "The gallery redirected to an unsupported image URL."


class GalleryRedirectWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scope = contracts.fixture("locale_contract_scope.json")
        cls.wording = contracts.fixture("gallery_redirect_current_wording.json")

    def test_only_reviewed_czech_and_swedish_extend_this_family(self):
        self.assertEqual(['cs', 'sv'], self.wording['additional_reviewed_tags'])

    def test_complete_values_and_exact_existing_locale_scope(self):
        contracts.require_wording_shape(self.wording, {KEY}, {"default", *self.scope["scoped_tags"], *self.wording["additional_reviewed_tags"]})
        self.assertEqual(SOURCE, self.wording["values"][KEY]["default"])
        paths = {"default": catalogues.RES / "values/strings.xml", **catalogues.catalogue_paths()}
        for tag, expected in self.wording["values"][KEY].items():
            with self.subTest(tag=tag):
                contracts.require_string(paths[tag].read_text(), KEY, expected, self.wording["constraints"][KEY])

    def test_all_xml_definitions_are_accounted_for_and_open_fallbacks_remain_absent(self):
        paths = catalogues.catalogue_paths()
        expected_paths = {catalogues.RES / "values/strings.xml", *(paths[tag] for tag in [*self.scope["scoped_tags"], *self.wording["additional_reviewed_tags"]])}
        actual_paths = {path for path in catalogues.RES.glob("values*/*.xml")
                        if ET.parse(path).getroot().find(f"./string[@name='{KEY}']") is not None}
        self.assertEqual(expected_paths, actual_paths)
        contracts.require_locale_scope(self.scope, set(self.scope["scoped_tags"]), catalogues.offered_tags())
        for tag in set(self.scope["fallback_tags"]) - set(self.wording["additional_reviewed_tags"]):
            with self.subTest(tag=tag):
                self.assertNotIn(KEY, catalogues.read_strings(paths[tag]))

    def test_host_only_missing_duplicate_or_detail_leaking_value_is_rejected(self):
        constraint = self.wording["constraints"][KEY]
        for body in (
            "",
            f'<string name="{KEY}">The gallery redirected outside its supported hosts.</string>',
            f'<string name="{KEY}">Unsupported image URL: %1$s</string>',
            f'<string name="{KEY}">{SOURCE}</string>' * 2,
        ):
            with self.subTest(body=body), self.assertRaises(ValueError):
                contracts.require_string("<resources>" + body + "</resources>", KEY, SOURCE, constraint)

    def test_every_locale_rejects_an_unsupported_full_value_mutation(self):
        constraint = self.wording["constraints"][KEY]
        for tag, expected in self.wording["values"][KEY].items():
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                contracts.require_string(f'<resources><string name="{KEY}">Unsupported host.</string></resources>',
                                         KEY, expected, constraint)


if __name__ == "__main__":
    unittest.main()
