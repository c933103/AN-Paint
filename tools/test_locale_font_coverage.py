"""Check actual bundled cmap coverage, without allowing Android's device fallback."""
import hashlib
import json
from pathlib import Path
import struct
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'Paintroid/src/main/assets'
RES = ROOT / 'Paintroid/src/main/res'


def mapped_codepoints(path):
    data = path.read_bytes()
    u16 = lambda at: struct.unpack_from('>H', data, at)[0]
    u32 = lambda at: struct.unpack_from('>I', data, at)[0]
    tables = {data[12 + i * 16:16 + i * 16]: u32(20 + i * 16)
              for i in range(u16(4))}
    base = tables[b'cmap']
    points = set()
    for index in range(u16(base + 2)):
        entry = base + 4 + index * 8
        platform, encoding = u16(entry), u16(entry + 2)
        if platform != 0 and (platform != 3 or encoding not in (1, 10)):
            continue
        start = base + u32(entry + 4)
        kind = u16(start)
        if kind == 12:
            for group in range(u32(start + 12)):
                lower, upper, glyph = struct.unpack_from('>III', data, start + 16 + group * 12)
                points.update(range(lower + (glyph == 0), upper + 1))
        elif kind == 4:
            segments = u16(start + 6) // 2
            ends = start + 14
            starts = ends + segments * 2 + 2
            deltas = starts + segments * 2
            ranges = deltas + segments * 2
            for segment in range(segments):
                lower, upper = u16(starts + segment * 2), u16(ends + segment * 2)
                delta = u16(deltas + segment * 2)
                pointer = ranges + segment * 2
                offset = u16(pointer)
                for cp in range(lower, min(upper, 0xfffe) + 1):
                    glyph = u16(pointer + offset + (cp - lower) * 2) if offset else cp
                    if offset and not glyph:
                        continue
                    if (glyph + delta) & 0xffff:
                        points.add(cp)
    return points


class LocaleFontCoverageTest(unittest.TestCase):
    def test_every_nom_catalogue_ideograph_is_bundled(self):
        font = ASSETS / 'fonts/anpaintnomui.ttf'
        points = mapped_codepoints(font)
        text = ''.join(ET.parse(RES / 'values-b+vi+Hani/strings.xml').getroot().itertext())
        text += '㗂越（𡨸喃）'
        required = {ord(c) for c in text if 0x3400 <= ord(c) <= 0x9fff or 0x20000 <= ord(c) <= 0x3ffff}
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
