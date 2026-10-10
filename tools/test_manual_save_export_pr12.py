"""Bounded adjacent Save/Export correction in the dormant Vietnamese long manual.

The active Help action uses ui_help23; this is not a live-screen acceptance test.
XML is canonical. These anchors protect reviewed clauses and menu-caption
agreement, not whole-language accuracy, Nôm glyph shape or Android layout.
"""
from pathlib import Path
import re
import unicodedata
import unittest
import xml.etree.ElementTree as ET

from test_locale_font_coverage import mapped_codepoints

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'Paintroid/src/main/res'
MANUAL = 'ui_the_arrow_on_the_left_directly_below_the'
CAPTIONS = {
    'save_as': 'save20_title',
    'save': 'ui_save',
    'export': 'ui_export_as23',
    'share': 'ui_save_and_share',
}
CLAUSES = {
    'values-vi': (
        '「{save_as}」 cho phép chọn định dạng ảnh, thiết lập và vị trí;',
        '「{save}」 ghi lại vào vị trí đó.',
        '「{export}」 và 「{share}」 ghi một bản sao mà không thay đổi vị trí 「{save}」 hiện tại và không đánh dấu bản vẽ là đã lưu.',
        '「{share}」 sau đó mở chia sẻ Android.',
        'Dấu sao cạnh tên tệp nghĩa là bản vẽ hiện tại có thay đổi chưa lưu.',
    ),
    'values-b+vi+Hani': (
        '「{save_as}」 朱 法 譔 定 樣 影, 設立 吧 位置;',
        '「{save}」 𥱬 來 𠓨 位置 妬.',
        '「{export}」 吧 「{share}」 𥱬 𠬠 版 抄 𣻕 空 𠊝 𢷮 位置 「{save}」 現在 吧 空 打 𨁪 版 𡳒 纙 㐌 留.',
        '「{share}」 𡢐 妬 𢲫 𢺹 𢩿 Android.',
        '𨁪 𣇟 𧣲 𠸜 𣜿 義 纙 版 𡳒 現在 𣎏 𠊝 𢷮 𣗓 留.',
    ),
}
STALE_SUBJECTS = {'values-vi': 'tệp đã xuất', 'values-b+vi+Hani': '𣜿 㐌 出'}


def read_catalogue(directory):
    return {node.get('name'): ''.join(node.itertext())
            for path in sorted((RES / directory).glob('*.xml'))
            for node in ET.parse(path).getroot() if node.tag == 'string'}


def text(value):
    value = value.replace(r"\'", "'").replace(r'\"', '"')
    value = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m[1], 16)), value)
    return ' '.join(unicodedata.normalize('NFC', value).split())


def captions(rendered):
    result = {}
    for role, key in CAPTIONS.items():
        seen = set()
        while True:
            if key in seen:
                raise AssertionError(f'Cyclic caption reference: {key}')
            seen.add(key)
            value = rendered[key]
            if not value.startswith('@string/'):
                break
            key = value.removeprefix('@string/')
        # Only terminal dialog punctuation is omitted when naming a menu command.
        result[role] = text(value).rstrip('.…')
    return result


def save_paragraph(manual):
    paragraphs = re.split(r'\\n\\n|\n\s*\n', manual)
    if len(paragraphs) <= 3:
        raise AssertionError('Manual has no fourth (Save/Export) paragraph')
    return text(paragraphs[3])


def check_clause(case, directory, local, rendered, index):
    expected = CLAUSES[directory][index].format(**captions(rendered))
    case.assertIn(text(expected), save_paragraph(local[MANUAL]))


def check_nom_glyphs(case, manual, points):
    # Check every rendered character, including punctuation, Latin product text,
    # spaces and supplementary-plane Nôm. No platform fallback or font rewriting.
    required = {ord(c) for c in save_paragraph(manual)}
    case.assertTrue(any(cp > 0xffff for cp in required))
    case.assertEqual([], [f'U+{cp:04X}' for cp in sorted(required - points)])


class ManualSaveExportPr12Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.default = read_catalogue('values')
        cls.locales = {directory: read_catalogue(directory) for directory in CLAUSES}

    def check_all(self, index):
        for directory, local in self.locales.items():
            with self.subTest(locale=directory):
                self.assertIn(MANUAL, local, 'Missing canonical localized manual')
                check_clause(self, directory, local, {**self.default, **local}, index)

    def test_save_as_chooses_format_settings_and_location(self):
        self.check_all(0)

    def test_save_reuses_that_destination(self):
        self.check_all(1)

    def test_both_exports_copy_without_changing_destination_or_saved_state(self):
        self.check_all(2)

    def test_save_and_share_then_opens_android_sharing(self):
        self.check_all(3)

    def test_filename_star_describes_current_drawing_changes(self):
        self.check_all(4)

    def test_stale_exported_file_subject_does_not_return(self):
        for directory, local in self.locales.items():
            with self.subTest(locale=directory):
                self.assertNotIn(text(STALE_SUBJECTS[directory]), save_paragraph(local[MANUAL]))

    def test_nom_save_paragraph_characters_are_in_bundled_font(self):
        points = mapped_codepoints(ROOT / 'Paintroid/src/main/assets/fonts/anpaintnomui.ttf')
        check_nom_glyphs(self, self.locales['values-b+vi+Hani'][MANUAL], points)


if __name__ == '__main__':
    unittest.main()
