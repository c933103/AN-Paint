"""Current note obligations; accepted prose records remain in source history."""
import unittest
from current_localization_contracts import current_display

KEY = 'language20_translation_note'

class LanguageTranslationNoteTest(unittest.TestCase):
    def test_source_keeps_maintenance_and_english_fallback(self):
        value = current_display('default', KEY)
        for boundary in ('maintained', 'language resources', 'New or untranslated', 'English'):
            self.assertIn(boundary, value)

    def test_current_notes_start_with_their_actual_localized_heading(self):
        for tag in ('yue-Hant', 'zh-HK', 'sw', 'zh-CN', 'vi', 'vi-Hani', 'nan-Hant-TW', 'nan-Latn-TW', 'wuu-Hans'):
            with self.subTest(tag=tag):
                self.assertTrue(current_display(tag, KEY).startswith(current_display(tag, 'language20_app_language')))

if __name__ == '__main__': unittest.main()
