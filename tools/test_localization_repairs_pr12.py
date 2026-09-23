"""Shared resource safety and this PR batch’s completeness regression gates."""
import unittest
import translation_catalogues as catalogues

class LocalizationRepairTests(unittest.TestCase):
    def test_all_existing_catalogues_remain_structurally_valid(self):
        self.assertEqual([], catalogues.validate_all(require_complete=False))

    def test_this_batch_remains_complete(self):
        for tag in ('ko-KR', 'ko-KP', 'ko-Kore-KR', 'vi', 'vi-Hani'):
            with self.subTest(locale=tag):
                self.assertEqual([], catalogues.validate_catalogue(tag, require_complete=True))
