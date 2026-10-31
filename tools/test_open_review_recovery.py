"""Current ordered processed-count composition; runtime progress has its own regression."""
import unittest
import translation_catalogues as catalogues


class OpenReviewRecoveryTest(unittest.TestCase):
    def test_progress_remains_an_ordered_processed_count(self):
        for tag in ('ms', 'id', 'ja', 'zh-HK'):
            value = catalogues.read_strings(catalogues.catalogue_paths()[tag])['ui_rendering_images']
            self.assertEqual({'%1$s': 1, '%2$s': 1}, catalogues.placeholders(value))
            self.assertLess(value.index('%1$s'), value.index('%2$s'))
            self.assertTrue(value.endswith('…'))


if __name__ == '__main__':
    unittest.main()
