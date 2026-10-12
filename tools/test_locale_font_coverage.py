"""Check actual bundled cmap coverage, without allowing Android's device fallback."""
import hashlib
import json
from pathlib import Path
from current_font_contract import validated_unicode_maps
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'Paintroid/src/main/assets'
RES = ROOT / 'Paintroid/src/main/res'


def mapped_codepoints(path):
    return {cp for _, mapping in validated_unicode_maps(path.read_bytes()) for cp in mapping}


class LocaleFontCoverageTest(unittest.TestCase):

    def test_every_nom_catalogue_ideograph_is_bundled(self):
        font = ASSETS / 'fonts/anpaintnomui.ttf'
        points = mapped_codepoints(font)
        text = ''.join(ET.parse(RES / 'values-b+vi+Hani/strings.xml').getroot().itertext())
        text += '㗂越（𡨸喃）'
        # Guard punctuation and Latin UI text as well as every Han plane.
        # XML layout line breaks are not glyphs; ordinary spaces remain covered.
        required = {ord(c) for c in text if c not in '\n\r\t'}
        # Retain normalization glyphs and the additive SVG error glyph 豫.
        required.update((0x651D, 0x671D, 0x8C6B))
        self.assertTrue(any(cp > 0xffff for cp in required))
        self.assertEqual([], [f'U+{cp:04X}' for cp in sorted(required - points)])
        # The review's uncommon Extension-F glyph remains a regression sample.
        self.assertIn(0x2e7b6, points)
        record = next(row for row in json.loads((ASSETS / 'fonts/inventory.json').read_text())
                      if row['id'] == 'anpaintnomui')
        self.assertTrue(record['ui_only'])
        self.assertEqual(record['sha256'], hashlib.sha256(font.read_bytes()).hexdigest())

    def test_wu_fallback_covers_its_supplementary_text_without_replacing_ordinary_glyphs(self):
        font = ASSETS / 'fonts/anpaintwuufallback.ttf'
        points = mapped_codepoints(font)
        text = ''.join(ET.parse(RES / 'values-b+wuu+Hans/strings.xml').getroot().itertext())
        required = {ord(c) for c in text if 0x20000 <= ord(c) <= 0x3ffff}
        self.assertEqual({0x20c8e}, required)
        self.assertEqual(required, points)
        record = next(row for row in json.loads((ASSETS / 'fonts/inventory.json').read_text())
                      if row['id'] == 'anpaintwuufallback')
        self.assertTrue(record['ui_only'])
        self.assertEqual(record['sha256'], hashlib.sha256(font.read_bytes()).hexdigest())

    def test_manchu_and_mongolian_use_font_with_all_required_letters(self):
        points = mapped_codepoints(ASSETS / 'fonts/notosansmongolian.ttf')
        for tag in ('mn+Mong', 'mnc+Mong'):
            text = ''.join(ET.parse(RES / f'values-b+{tag}/strings.xml').getroot().itertext())
            required = {ord(c) for c in text if 0x1800 <= ord(c) <= 0x18af}
            self.assertTrue(required)
            self.assertEqual([], [f'U+{cp:04X}' for cp in sorted(required - points)], tag)


if __name__ == '__main__':
    unittest.main()
