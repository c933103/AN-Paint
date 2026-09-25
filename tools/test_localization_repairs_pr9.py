"""Keep this PR's five catalogues complete when shared UI strings change."""
import unittest

import translation_catalogues as catalogues


class LocalizationRepairTests(unittest.TestCase):
    def test_this_batch_remains_complete(self):
        for tag in ('jje', 'mnc-Mong', 'ain-Kana', 'ain-Latn', 'ryu'):
            with self.subTest(locale=tag):
                self.assertEqual([], catalogues.validate_catalogue(tag, require_complete=True))
