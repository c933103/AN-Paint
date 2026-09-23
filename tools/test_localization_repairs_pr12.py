"""Shared resource safety and this PR batch’s completeness regression gates."""
import unittest
import unicodedata
import translation_catalogues as catalogues

class LocalizationRepairTests(unittest.TestCase):
    def test_all_existing_catalogues_remain_structurally_valid(self):
        self.assertEqual([], catalogues.validate_all(require_complete=False))

    def test_this_batch_remains_complete(self):
        for tag in ('ko-KR', 'ko-KP', 'ko-Kore-KR', 'vi', 'vi-Hani'):
            with self.subTest(locale=tag):
                self.assertEqual([], catalogues.validate_catalogue(tag, require_complete=True))

    def test_credit_help_uses_the_actual_localized_file_about_breadcrumbs(self):
        routes = {
            'ui_catrobat_s_own_artwork_uses_cc_by_sa': ('ui_menu_file', 'ui_about_credits23', 'ui_image_credits'),
            'ui_the_arrow_on_the_left_directly_below_the': ('ui_menu_file', 'ui_about_credits23', 'ui_image_credits'),
            'ui_add_up_to_20_images_with_android_s': ('ui_menu_file', 'ui_about_credits23'),
        }
        def displayed(value):
            return unicodedata.normalize('NFC', value.strip('"').replace(r"\'", "'").replace(r'\"', '"')).casefold()
        defaults = catalogues.default_resources()[0]
        for tag in ('ko-KR', 'ko-KP', 'ko-Kore-KR', 'vi', 'vi-Hani'):
            rendered = {**defaults, **catalogues.read_strings(catalogues.catalogue_paths()[tag])}
            for key, labels in routes.items():
                for label in labels:
                    with self.subTest(locale=tag, key=key, label=label):
                        label_text = displayed(rendered[label]).rstrip(' \t\r\n.,;:!?…。！？；：།༎')
                        self.assertTrue(label_text)
                        self.assertIn(label_text, displayed(rendered[key]))
