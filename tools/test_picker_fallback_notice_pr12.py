"""Bounded guards for the Vietnamese and Nôm language-picker notice.

Adjacent recurrence of PR #6 discussion_r4215259754; not the PR #12
API30+ toast-font finding (discussion_r4213756309). The baseline is
fa442b606c206f86e599203aaa9d7367b8429f29. These literal clause guards
detect lost source obligations, not arbitrary semantic equivalence,
native fluency, Android runtime resource selection or visual rendering.
Reviewed rewording should update its clause without dropping its obligation.
"""
from pathlib import Path
import hashlib
import json
import re
import unittest
import xml.etree.ElementTree as ET

from test_locale_font_coverage import mapped_codepoints

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'Paintroid/src/main/res'
KEY = 'language20_translation_note'
TITLE_KEY = 'language20_app_language'
CASES = {
    'vi': {
        'folder': 'values-vi',
        'maintenance': 'Các bản dịch được quản lý trong tài nguyên ngôn ngữ của AN Paint.',
        'fallback': 'Văn bản mới hay chưa được dịch sẽ hiển thị bằng tiếng Anh.',
        'old_coverage': 'bao gồm toàn bộ văn bản giao diện có thể dịch',
    },
    'vi-Hani': {
        'folder': 'values-b+vi+Hani',
        'maintenance': '各 版 譯 得 管理 𥪝 財源 言語 𧵑 AN Paint.',
        'fallback': '文本 㵋 咍 𣗓 得 譯 仕 顯示 憑 㗂 英.',
        'old_coverage': '包 𠁟 全部 文本 交 面 𣎏 体 譯',
    },
}


def strings(folder):
    nodes = ET.parse(RES / folder / 'strings.xml').getroot()
    for key in (KEY, TITLE_KEY):
        if sum(node.tag == 'string' and node.get('name') == key for node in nodes) != 1:
            raise AssertionError(f'{folder}: expected one canonical {key}')
    return {node.get('name'): ''.join(node.itertext()) for node in nodes}


def local_strings(tag):
    return strings(CASES[tag]['folder'])


class PickerFallbackNoticePr12Tests(unittest.TestCase):
    def test_scope_contains_the_two_registered_catalogues(self):
        self.assertEqual({'vi', 'vi-Hani'}, set(CASES))
        tags = {node.text for node in ET.parse(RES / 'values/app_language_tags.xml').findall('.//item')}
        locales = {node.get('{http://schemas.android.com/apk/res/android}name')
                   for node in ET.parse(RES / 'xml/app_locales.xml').getroot()}
        self.assertLessEqual(set(CASES), tags)
        self.assertLessEqual(set(CASES), locales)

    def test_default_message_still_has_the_reviewed_obligations(self):
        values = strings('values')
        self.assertEqual(values[TITLE_KEY] + r'\n\n'
                         + 'Translations are maintained in AN Paint’s language resources. '
                         + 'New or untranslated text appears in English.', values[KEY],
                         'Reassess the local notices if the source obligations change.')

    def test_picker_still_uses_the_notice_as_its_custom_title(self):
        source = (ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/AppLanguage.kt').read_text()
        picker = source.split('fun showPicker(', 1)[1]
        self.assertIn('text = ui(R.string.language20_translation_note)', picker)
        self.assertRegex(picker, r'\.setCustomTitle\([^\n]*\bnote\b[^\n]*\)')

    def test_nom_notice_is_covered_by_the_actual_unchanged_bundled_font(self):
        assets = ROOT / 'Paintroid/src/main/assets'
        font = assets / 'fonts/anpaintnomui.ttf'
        record = next(row for row in json.loads((assets / 'fonts/inventory.json').read_text())
                      if row['id'] == 'anpaintnomui')
        self.assertTrue(record['ui_only'])
        self.assertEqual(record['sha256'], hashlib.sha256(font.read_bytes()).hexdigest())
        note = local_strings('vi-Hani')[KEY].replace(r'\n', '\n')
        required = {ord(c) for c in note if c not in '\n\r\t'}
        self.assertEqual([], [f'U+{cp:04X}' for cp in sorted(required - mapped_codepoints(font))])


def heading_test(tag):
    def test(self):
        values = local_strings(tag)
        self.assertTrue(values[KEY].startswith(values[TITLE_KEY] + r'\n\n'),
                        tag + ': custom title must start with the localized heading')
    return test


def clause_test(tag, field):
    def test(self):
        self.assertIn(CASES[tag][field], local_strings(tag)[KEY],
                      tag + ': missing ' + field + ' obligation')
    return test


def order_test(tag):
    def test(self):
        text = local_strings(tag)[KEY]
        positions = [text.find(CASES[tag][field]) for field in ('maintenance', 'fallback')]
        self.assertTrue(all(position >= 0 for position in positions), tag + ': missing clause')
        self.assertLess(positions[0], positions[1])
    return test


def stale_coverage_test(tag):
    def test(self):
        self.assertNotIn(CASES[tag]['old_coverage'], local_strings(tag)[KEY],
                         'Do not reintroduce an unverified whole-interface coverage claim.')
    return test


for tag in CASES:
    suffix = tag.replace('-', '_')
    setattr(PickerFallbackNoticePr12Tests, 'test_heading_' + suffix, heading_test(tag))
    setattr(PickerFallbackNoticePr12Tests, 'test_maintenance_' + suffix, clause_test(tag, 'maintenance'))
    setattr(PickerFallbackNoticePr12Tests, 'test_fallback_' + suffix, clause_test(tag, 'fallback'))
    setattr(PickerFallbackNoticePr12Tests, 'test_clause_order_' + suffix, order_test(tag))
    setattr(PickerFallbackNoticePr12Tests, 'test_no_stale_coverage_' + suffix, stale_coverage_test(tag))


if __name__ == '__main__':
    unittest.main()
