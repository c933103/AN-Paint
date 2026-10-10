"""Check structural coverage of PR #8's four scoped catalogues.

Resource presence, placeholders and literal tokens do not establish semantic or
linguistic correctness, review acceptance, or completion of the required recheck.
"""
import unittest

import translation_catalogues as translations


class CatalogueStructurePr8Tests(unittest.TestCase):
    def test_scoped_catalogues_pass_structural_validation(self):
        for tag in ("bo", "dz", "mn-Cyrl-MN", "mn-Mong"):
            with self.subTest(tag=tag):
                self.assertEqual(
                    [], translations.validate_catalogue(tag, require_complete=True),
                )


if __name__ == "__main__":
    unittest.main()
