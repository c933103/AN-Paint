"""Host checks for provenance, the selected shared vocabulary, and locale declarations."""
import json
import unittest
from unittest import mock
import pathlib
import xml.etree.ElementTree as ET
import reuse_upstream_translations as translations


class TranslationTests(unittest.TestCase):
    def test_generated_translations_match_verified_upstream_bytes(self):
        for path, text in translations.generate().items():
            self.assertEqual(text, path.read_text(), str(path))

    def test_generation_is_independent_of_filesystem_enumeration_order(self):
        expected = translations.generate()
        original = pathlib.Path.glob
        def reversed_glob(path, pattern):
            return iter(reversed(list(original(path, pattern))))
        with mock.patch.object(pathlib.Path, "glob", reversed_glob):
            self.assertEqual(expected, translations.generate())

    def test_every_mapped_resource_exists_in_default_catalogue(self):
        names = set()
        for path in (translations.RES / "values").glob("*.xml"):
            names.update(node.get("name") for node in ET.parse(path).getroot())
        mapping = json.loads((translations.DATA / "common-terms.json").read_text())
        self.assertTrue(set(mapping) <= names, set(mapping) - names)

    def test_picker_and_android_locale_list_agree_and_coverage_accounts_for_every_option(self):
        tags = [node.text for node in ET.parse(translations.RES / "values/app_language_tags.xml").findall(".//item")]
        platform = [node.get("{http://schemas.android.com/apk/res/android}name")
                    for node in ET.parse(translations.RES / "xml/app_locales.xml").getroot()]
        self.assertEqual(tags, platform)
        self.assertEqual(len(tags), len(set(tags)))
        self.assertEqual(tags[0], "en-001")
        self.assertEqual(tags[1:], sorted(tags[1:], key=str.casefold))
        self.assertNotIn("zh-Hant", tags)
        for tag in ("zh-TW", "zh-HK", "mn-Cyrl-MN", "mn-Mong"):
            self.assertIn(tag, tags)
        self.assertIn("en-US", tags)
        self.assertNotIn("en", tags)
        self.assertIn("ja", tags)
        self.assertIn("ar", tags)
        self.assertIn("sr-Latn", tags)
        self.assertIn("sr-Cyrl", tags)
        coverage = json.loads((translations.DATA / "coverage.json").read_text())
        accounted = []
        for row in coverage["coverage"]:
            accounted.extend(row["offered_tags"])
            if row["offered_in_app"]:
                self.assertTrue((translations.ROOT / row["generated_resource"]).is_file())
            if row["offered_in_app"] and not row.get("name_only") and not row["language_tag"].startswith("en-"):
                self.assertGreater(row["entries_different_from_upstream_english"], 0)
        self.assertCountEqual(tags, accounted)
        self.assertEqual(["ain", "tai"], coverage["name_only_options"])
        names = ET.parse(translations.RES / "values/app_language_names.xml")
        labels = names.findall(".//string-array[@name='app_language_names']/item")
        self.assertEqual(len(tags), len(labels))
        self.assertTrue(all(item.text and item.text.strip() for item in labels))

    def test_unsaved_prompt_never_reuses_the_discard_label_for_keep_editing(self):
        def normalized(value):
            return value.strip().strip('"').casefold()
        for path in translations.RES.glob("values*/strings.xml"):
            strings = translations.read_strings(path)
            if "ui_discard_changes23" in strings:
                self.assertNotEqual(normalized(strings["ui_discard_changes23"]), normalized(strings["ui_keep_editing23"]), str(path))
        for qualifier in ("values-b+lzh+Hant", "values-b+mn+Mong", "values-zh-rHK", "values-b+mn+Cyrl+MN"):
            strings = translations.read_strings(translations.RES / qualifier / "strings.xml")
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

    def test_every_offered_language_has_exactly_one_string_catalogue(self):
        basic = json.loads((translations.DATA / "basic-translations.json").read_text())
        for tag in basic:
            self.assertTrue((translations.RES / translations.qualifier_for_tag(tag) / "strings.xml").is_file(), tag)
        for folder in translations.RES.glob("values*"):
            self.assertLessEqual(len(list(folder.glob("strings*.xml"))), 1, str(folder))

    def test_starter_save_translation_is_shared_with_the_unsaved_prompt(self):
        basic = json.loads((translations.DATA / "basic-translations.json").read_text())
        for tag, terms in basic.items():
            strings = translations.read_strings(translations.RES / translations.qualifier_for_tag(tag) / "strings.xml")
            if terms:
                self.assertEqual("@string/ui_save", strings["ui_save_a5d0d9"], tag)
            else:
                self.assertEqual({}, strings, tag)
