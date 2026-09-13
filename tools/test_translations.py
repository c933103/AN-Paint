"""Host checks for provenance, the selected shared vocabulary, and locale declarations."""
import json
import unittest
import xml.etree.ElementTree as ET
import reuse_upstream_translations as translations


class TranslationTests(unittest.TestCase):
    def test_generated_translations_match_verified_upstream_bytes(self):
        for path, text in translations.generate().items():
            self.assertEqual(text, path.read_text(), str(path))

    def test_every_mapped_resource_exists_in_default_catalogue(self):
        names = set()
        for path in (translations.RES / "values").glob("*.xml"):
            names.update(node.get("name") for node in ET.parse(path).getroot())
        mapping = json.loads((translations.DATA / "common-terms.json").read_text())
        self.assertTrue(set(mapping) <= names, set(mapping) - names)

    def test_picker_and_android_locale_list_agree_and_exclude_empty_translations(self):
        tags = [node.text for node in ET.parse(translations.RES / "values/app_language_tags.xml").findall(".//item")]
        platform = [node.get("{http://schemas.android.com/apk/res/android}name")
                    for node in ET.parse(translations.RES / "xml/app_locales.xml").getroot()]
        self.assertEqual(tags, platform)
        self.assertEqual(len(tags), len(set(tags)))
        self.assertIn("en", tags)
        self.assertIn("ja", tags)
        self.assertIn("ar", tags)
        self.assertIn("sr-Latn", tags)
        self.assertIn("sr-Cyrl", tags)
        coverage = json.loads((translations.DATA / "coverage.json").read_text())
        for row in coverage["coverage"]:
            if row["language_tag"] in tags and not row["language_tag"].startswith("en-"):
                self.assertGreater(row["entries_different_from_upstream_english"], 0)

    def test_unsaved_prompt_never_reuses_the_discard_label_for_keep_editing(self):
        def normalized(value):
            return value.strip().strip('"').casefold()
        for path in translations.RES.glob("values*/strings_upstream.xml"):
            strings = translations.read_strings(path)
            self.assertNotEqual(normalized(strings["ui_discard_changes23"]), normalized(strings["ui_keep_editing23"]), str(path))
        for qualifier in ("values-b+lzh+Hant", "values-b+mn+Mong", "values-b+zh+Hant"):
            strings = translations.read_strings(translations.RES / qualifier / "strings23.xml")
            self.assertNotEqual(strings["ui_discard_changes23"], strings["ui_keep_editing23"])
            self.assertTrue(strings["ui_cut"].strip())

    def test_no_locale_duplicates_resources_across_generated_and_reviewed_catalogues(self):
        for folder in translations.RES.glob("values*"):
            seen = set()
            for path in folder.glob("*.xml"):
                for node in ET.parse(path).getroot():
                    if node.tag != "string":
                        continue
                    key = node.get("name")
                    self.assertNotIn(key, seen, str(path) + "/" + key)
                    seen.add(key)
        offered = [node.text for node in ET.parse(translations.RES / "values/app_language_tags.xml").findall(".//item")]
        self.assertIn("lzh-Hant", offered)
        self.assertIn("mn-Mong", offered)
