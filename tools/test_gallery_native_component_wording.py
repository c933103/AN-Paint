"""Complete generic gallery component diagnostic and precise converter controls.

Runtime routing belongs to GalleryNativeComponentFailureTest and the real-device
codec controls. These resource checks do not execute Kotlin, JNI or a provider.
"""
from pathlib import Path
import json
import unittest
import xml.etree.ElementTree as ET

import current_localization_contracts as contracts
import translation_catalogues as catalogues

ROOT = Path(__file__).resolve().parents[1]
KEY = "gallery_image_component_unavailable"
SPECIFIC = "colour_converter_unavailable"
SOURCE = "A required image component is unavailable. The image was not imported."


class GalleryNativeComponentWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scope = contracts.fixture("locale_contract_scope.json")
        cls.wording = contracts.fixture("gallery_native_component_current_wording.json")

    def test_only_reviewed_swedish_extends_this_family(self):
        self.assertEqual(['sv'], self.wording['additional_reviewed_tags'])

    def test_complete_values_match_scoped_catalogues(self):
        contracts.require_wording_shape(self.wording, {KEY}, {"default", *self.scope["scoped_tags"], *self.wording["additional_reviewed_tags"]})
        self.assertEqual(SOURCE, self.wording["values"][KEY]["default"])
        paths = {"default": catalogues.RES / "values/strings.xml", **catalogues.catalogue_paths()}
        for tag, expected in self.wording["values"][KEY].items():
            with self.subTest(tag=tag):
                contracts.require_string(paths[tag].read_text(), KEY, expected, self.wording["constraints"][KEY])

    def test_every_definition_is_accounted_for_and_open_fallbacks_remain_absent(self):
        paths = catalogues.catalogue_paths()
        expected = {catalogues.RES / "values/strings.xml", *(paths[tag] for tag in [*self.scope["scoped_tags"], *self.wording["additional_reviewed_tags"]])}
        actual = {path for path in catalogues.RES.glob("values*/*.xml")
                  if ET.parse(path).getroot().find(f"./string[@name='{KEY}']") is not None}
        self.assertEqual(expected, actual)
        contracts.require_locale_scope(self.scope, set(self.scope["scoped_tags"]), catalogues.offered_tags())
        for tag in set(self.scope["fallback_tags"]) - set(self.wording["additional_reviewed_tags"]):
            with self.subTest(tag=tag):
                self.assertNotIn(KEY, catalogues.read_strings(paths[tag]))

    def test_specific_converter_message_remains_distinct_in_every_catalogue(self):
        paths = {"default": catalogues.RES / "values/strings.xml", **catalogues.catalogue_paths()}
        for tag in self.wording["values"][KEY]:
            with self.subTest(tag=tag):
                values = catalogues.read_strings(paths[tag])
                self.assertIn(SPECIFIC, values)
                self.assertNotEqual(values[KEY], values[SPECIFIC])
                with self.assertRaises(ValueError):
                    contracts.require_string(f'<resources><string name="{KEY}">{values[SPECIFIC]}</string></resources>',
                                             KEY, self.wording["values"][KEY][tag], self.wording["constraints"][KEY])
        self.assertEqual("The image colour converter could not start. The image was not imported.",
                         catalogues.read_strings(paths["default"])[SPECIFIC])

    def test_missing_duplicate_wrong_cause_and_detail_exposure_are_rejected(self):
        constraint = self.wording["constraints"][KEY]
        for body in (
            "",
            f'<string name="{KEY}">The colour converter could not start.</string>',
            f'<string name="{KEY}">The gallery provider is unavailable.</string>',
            f'<string name="{KEY}">A component is unavailable: %1$s</string>',
            f'<string name="{KEY}">{SOURCE}</string>' * 2,
        ):
            with self.subTest(body=body), self.assertRaises(ValueError):
                contracts.require_string("<resources>" + body + "</resources>", KEY, SOURCE, constraint)

    def test_generic_import_diagnostic_has_explicit_importance(self):
        importance = json.loads((ROOT / "translations/string-importance.json").read_text())
        assigned = {key: tier["id"] for tier in importance["tiers"] for key in tier["keys"]}
        self.assertEqual("P2", assigned["string/" + KEY])


if __name__ == "__main__":
    unittest.main()
