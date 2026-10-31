"""Current pidgin option registration; historical empty-catalogue approval is archived."""
import json
import unittest
from language_option_additions import SECOND_ADDITIONS_PATH
import translation_catalogues as catalogues


class PidginTokPisinOptionSuccessorsTest(unittest.TestCase):
    def test_registered_pidgin_options_keep_public_identity_and_valid_resources(self):
        rows = {row['tag']: row for row in json.loads(SECOND_ADDITIONS_PATH.read_text())['languages']}
        for tag in ('pcm', 'tpi'):
            with self.subTest(tag=tag):
                self.assertIn(tag, catalogues.offered_tags())
                self.assertEqual(catalogues.ROOT / rows[tag]['catalogue'], catalogues.catalogue_paths()[tag])
                self.assertEqual([], catalogues.validate_catalogue(tag))


if __name__ == '__main__':
    unittest.main()
