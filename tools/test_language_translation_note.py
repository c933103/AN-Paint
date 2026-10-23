#!/usr/bin/env python3
"""Narrow source regression guards for the two independently accepted notes.
Prepared only, NOT RUN. No generator, build, or Android runtime is invoked.
Place under tools/ in the eventual reviewed source tree before running.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'Paintroid/src/main/res'
KEY = 'language20_translation_note'
SOURCE = 'App language\\n\\nTranslations are maintained in AN Paint’s language resources. New or untranslated text appears in English.'
ACCEPTED = {
    'values-sw': 'Lugha ya programu\\n\\nTafsiri hutunzwa katika rasilimali za lugha za AN Paint. Maandishi mapya au ambayo hayajatafsiriwa huonekana kwa Kiingereza.',
    'values-zh-rCN': '应用语言\\n\\n翻译内容在 AN Paint 的语言资源中维护。新增或尚未翻译的文字会以英语显示。',
}
OLD = {
    'values-sw': 'Toleo hili la lugha lina maandishi yote ya kiolesura cha AN Paint yanayoweza kutafsiriwa.',
    'values-zh-rCN': '此语言版本已包含 AN Paint 所有可翻译的界面文字。',
}

class LanguageTranslationNoteTest(unittest.TestCase):
    def read_note(self, folder):
        root = ET.parse(RES / folder / 'strings.xml').getroot()
        nodes = root.findall(f"string[@name='{KEY}']")
        self.assertEqual(len(nodes), 1)
        return ''.join(nodes[0].itertext())

    def test_source_keeps_maintenance_and_english_fallback(self):
        self.assertEqual(self.read_note('values'), SOURCE)

    def test_accepted_complete_notes_replace_false_completeness(self):
        for folder, expected in ACCEPTED.items():
            with self.subTest(folder=folder):
                actual = self.read_note(folder)
                self.assertEqual(actual, expected)
                self.assertNotEqual(actual, OLD[folder])
                self.assertEqual(actual.count('\\n'), 2)
                self.assertNotIn('\n', actual)
                self.assertNotIn('%', actual)

if __name__ == '__main__':
    unittest.main()
