"""Keep the four completed Himalayan/Mongolian catalogues complete."""
import unittest

import translation_catalogues as translations


class CompletedCatalogueTests(unittest.TestCase):
    def test_completed_catalogues_follow_the_current_english_resources(self):
        for tag in ("bo", "dz", "mn-Cyrl-MN", "mn-Mong"):
            with self.subTest(tag=tag):
                self.assertEqual(
                    [], translations.validate_catalogue(tag, require_complete=True),
                )


if __name__ == "__main__":
    unittest.main()
