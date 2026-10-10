"""PR #12 Vietnamese assembly-help regressions, limited to two repaired spans.

Finding: https://github.com/c933103/AN-Paint/pull/12#discussion_r4216899726
Source inspected at e9d930abd51cb7c051b0b2c999aeaff1579bb3e7. The first
paragraph describes placedSize; paragraph six must make a smaller-copy chooser
conditional and preserve the warning-only memory-floor path.

Literal guards detect these omissions, not arbitrary semantic equivalence,
native fluency, Android resource selection, glyph shape or runtime layout.
Update the bounded expectations if a future reviewed paraphrase replaces them.
"""
from pathlib import Path
import hashlib
import json
import unittest
import xml.etree.ElementTree as ET

from test_assembly_help_pr8 import code_locations, kotlin_block, kotlin_tokens
from test_locale_font_coverage import mapped_codepoints

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'Paintroid/src/main/res'
CLASSIC = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
KEY = 'ui_add_up_to_20_images_with_android_s'
CASES = {
    'vi': {
        'folder': 'values-vi',
        'quotes': ('«', '»'),
        'tray': 'kích thước ảnh sau khi cắt xén và điều chỉnh bằng «Cùng chiều rộng» hoặc «Cùng chiều cao»',
        'choice': 'Nếu đầu ra vượt quá giới hạn bộ nhớ và ứng dụng hiển thị trình chọn kích thước, hãy chọn một bản sao đầu ra nhỏ hơn.',
        'floor': 'Nếu ngay cả đầu ra rất nhỏ vẫn vượt quá giới hạn, ứng dụng sẽ thông báo không đủ bộ nhớ và không hiển thị trình chọn kích thước.',
        'stale_tray': 'kích thước cắt xén',
        'stale_choice': 'Nếu đầu ra vượt quá giới hạn bộ nhớ, hãy chọn một bản sao đầu ra nhỏ hơn.',
    },
    'vi-Hani': {
        'folder': 'values-b+vi+Hani',
        'quotes': ('「', '」'),
        'tray': '戟 𡱩 影 𡢐 欺 割 釧 吧 調整 憑 「共 朝 𢌌」 惑 「共 朝 高」',
        'choice': '裊 頭 𠚢 越 過 界限 部𢖵 吧 應用 顯示 呈 譔 戟 𡱩, 唉 譔 𠬠 版 抄 頭 𠚢 𡮈 欣.',
        'floor': '裊 𣦍 𪥘 頭 𠚢 窒 𡮈 吻 越 過 界限, 應用 仕 通 報 空 𨁥 部𢖵 吧 空 顯示 呈 譔 戟 𡱩.',
        'stale_tray': '戟 𡱩 割 釧',
        'stale_choice': '裊 頭 𠚢 越 過 界限 部𢖵, 唉 譔 𠬠 版 抄 頭 𠚢 𡮈 欣.',
    },
}


def catalogue(folder):
    nodes = ET.parse(RES / folder / 'strings.xml').getroot()
    if sum(node.tag == 'string' and node.get('name') == KEY for node in nodes) != 1:
        raise AssertionError(f'{folder}: expected one canonical assembly-help key')
    values = {node.get('name'): ''.join(node.itertext()) for node in nodes if node.tag == 'string'}
    paragraphs = values[KEY].split(r'\n\n')
    if len(paragraphs) != 7:
        raise AssertionError(f'{folder}: expected seven assembly-help paragraphs')
    return values, paragraphs


class AssemblyHelpPr12Tests(unittest.TestCase):
    def test_scope_is_two_registered_canonical_vietnamese_catalogues(self):
        self.assertEqual({'vi', 'vi-Hani'}, set(CASES))
        offered = {node.text for node in ET.parse(RES / 'values/app_language_tags.xml').findall('.//item')}
        locales = {node.get('{http://schemas.android.com/apk/res/android}name')
                   for node in ET.parse(RES / 'xml/app_locales.xml').getroot()}
        self.assertLessEqual(set(CASES), offered)
        self.assertLessEqual(set(CASES), locales)

    def test_default_contract_still_requires_both_repairs(self):
        _, paragraphs = catalogue('values')
        self.assertIn('image dimensions after cropping and any Same width or Same height adjustment', paragraphs[0])
        self.assertIn('choose a smaller output copy if offered', paragraphs[5])
        self.assertIn('If even a tiny output exceeds the budget, the app shows a memory warning instead of a size chooser.', paragraphs[5])

    def test_live_tray_uses_crop_and_normalization_with_the_named_controls(self):
        activity = (CLASSIC / 'AssemblyActivity.kt').read_text()
        model = (CLASSIC / 'ImageAssembly.kt').read_text()
        tray = kotlin_block(activity, 'private fun renderTray() {')
        self.assertTrue(code_locations(tray, 'item.placedSize.width, item.placedSize.height'))
        self.assertTrue(code_locations(tray, 'card.addView(text("${item.placedSize.width} × ${item.placedSize.height}${if (item.attachment == null) "" else " · " + ui(R.string.ui_placed)}",10f))'))
        placed = kotlin_block(model, 'val placedSize: ImageDimensions get() {')
        self.assertTrue(code_locations(placed, 'val n = normalization ?: return croppedSize'))
        self.assertTrue(code_locations(model, 'val croppedSize get() = ImageDimensions(crop.width(),crop.height())'))
        self.assertTrue(code_locations(placed, 'val base = if (n.axis == NormalizeAxis.WIDTH) crop.width() else crop.height()'))
        self.assertTrue(code_locations(placed, 'return if (n.axis == NormalizeAxis.WIDTH) ImageDimensions(n.pixels,scaled.toInt()) else ImageDimensions(scaled.toInt(),n.pixels)'))
        for suffix, axis in (('width', 'WIDTH'), ('height', 'HEIGHT')):
            self.assertTrue(code_locations(activity,
                f'button(ui(R.string.ui_same_{suffix}),"assembly_same_{suffix}") {{ normalize(NormalizeAxis.{axis}) }}'))
        self.assertTrue(code_locations(activity, 'private fun showHelp() = message(ui(R.string.' + KEY + '))'))

    def test_memory_floor_warns_and_returns_before_size_chooser_construction(self):
        activity = (CLASSIC / 'AssemblyActivity.kt').read_text()
        renderer = (CLASSIC / 'AssemblyRenderer.kt').read_text()
        suggested = kotlin_block(renderer, 'fun suggested(previous: ImageDimensions? = null): ImageDimensions? {')
        self.assertTrue(code_locations(suggested, 'if (!fits(ImageDimensions(1,1))) return null'))
        dialog = kotlin_block(activity,
            'private fun outputSizeDialog(renderer: AssemblyRenderer,toPaint: Boolean,previous: ImageDimensions? = null) {')
        self.assertTrue(code_locations(dialog, 'val suggested = renderer.suggested(previous)'))
        warning = kotlin_block(dialog, 'if (suggested == null) {')
        self.assertEqual(kotlin_tokens('message(ui(R.string.ui_assembly_source_memory_floor)) return'), warning)
        chooser = code_locations(dialog, 'val sizing = DimensionControls(this,renderer.original,suggested,"assembly_size",true)')
        self.assertEqual(1, len(chooser))
        self.assertLess(code_locations(dialog, 'if (suggested == null) {')[0], chooser[0])

    def test_nom_repaired_paragraphs_have_bundled_glyph_coverage(self):
        font = ROOT / 'Paintroid/src/main/assets/fonts/anpaintnomui.ttf'
        inventory = json.loads((font.parent / 'inventory.json').read_text())
        record = next(row for row in inventory if row['id'] == 'anpaintnomui')
        self.assertTrue(record['ui_only'])
        self.assertEqual(record['sha256'], hashlib.sha256(font.read_bytes()).hexdigest())
        _, paragraphs = catalogue(CASES['vi-Hani']['folder'])
        # Check actual resource text, including punctuation and supplementary Han,
        # rather than only the expected clauses or Android's fallback font.
        required = {ord(c) for c in paragraphs[0] + paragraphs[5] if c not in '\n\r\t'}
        self.assertTrue(any(cp > 0xffff for cp in required))
        self.assertEqual([], [f'U+{cp:04X}' for cp in sorted(required - mapped_codepoints(font))])


def tray_test(tag):
    def test(self):
        case = CASES[tag]
        values, paragraphs = catalogue(case['folder'])
        # Paragraph four already mentions normalization. It cannot satisfy this
        # first-paragraph tray obligation, which was the original omission.
        self.assertIn(case['tray'], paragraphs[0])
        self.assertNotIn(case['stale_tray'], paragraphs[0])
        left, right = case['quotes']
        for key in ('ui_same_width', 'ui_same_height'):
            self.assertIn(left + values[key] + right, paragraphs[0])
    return test


def output_test(tag, obligation):
    def test(self):
        case = CASES[tag]
        _, paragraphs = catalogue(case['folder'])
        self.assertIn(case[obligation], paragraphs[5], tag + ': missing ' + obligation)
        self.assertNotIn(case['stale_choice'], paragraphs[5])
    return test


for tag in CASES:
    suffix = tag.replace('-', '_')
    setattr(AssemblyHelpPr12Tests, 'test_tray_dimensions_' + suffix, tray_test(tag))
    setattr(AssemblyHelpPr12Tests, 'test_conditional_chooser_' + suffix, output_test(tag, 'choice'))
    setattr(AssemblyHelpPr12Tests, 'test_warning_without_chooser_' + suffix, output_test(tag, 'floor'))


if __name__ == '__main__':
    unittest.main()
