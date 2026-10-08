"""Canonical normalization resources for this translation PR's scoped locales."""
import unittest
import translation_catalogues as translations

KEYS = {'ui_normalize_height_info', 'ui_normalize_height_input_percent', 'ui_normalize_height_intro', 'ui_normalize_width_info', 'ui_normalize_width_input_percent', 'ui_normalize_width_intro'}
SCOPE = ('sw', 'fi', 'hu', 'af', 'nl', 'et', 'lv', 'lt')


class NormalizationScopePr4Test(unittest.TestCase):
    def test_six_messages_are_in_canonical_catalogues(self):
        source = translations.read_strings(translations.RES / "values/strings.xml")
        self.assertLessEqual(KEYS, set(source))
        paths = translations.catalogue_paths()
        for tag in SCOPE:
            with self.subTest(tag=tag):
                self.assertLessEqual(KEYS, set(translations.read_strings(paths[tag])))


if __name__ == "__main__":
    unittest.main()
