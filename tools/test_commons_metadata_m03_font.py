"""M03 glyph preservation and strict reversal; not native-language acceptance."""
import base64
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

from commons_metadata_m03_font_scope import before_m03_font, font_fixture
from test_locale_font_coverage import mapped_codepoints

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / 'Paintroid/src/main/assets/fonts/anpaintnomui.ttf'
EVIDENCE = ROOT / 'verification/commons-metadata-m03-2026-10-11/nom-font-extension.json'


def tables(data):
    return {tag.decode(): data[offset:offset+length] for tag, _, offset, length in
            (struct.unpack_from('>4sIII', data, 12+i*16)
             for i in range(struct.unpack_from('>H', data, 4)[0]))}


class CommonsMetadataM03FontContracts(unittest.TestCase):
    def test_exact_one_glyph_delta_restores_the_unchanged_historical_font(self):
        after = FONT.read_bytes(); scope = font_fixture(); before = before_m03_font(after)
        self.assertEqual('U+8FD4', scope['addition'])
        self.assertEqual('797ac4ef00f0dd8a982d5216dbd78db3edda07b578b9f8642d0156add90bd526', hashlib.sha256(before).hexdigest())
        self.assertEqual('4ae4cab599622f6c9d66b8a99074f2a291ffc32000a78ba69f241fc12eb64e05', hashlib.sha256(after).hexdigest())
        with tempfile.TemporaryDirectory() as folder:
            baseline = Path(folder)/'pre-m03.ttf'; baseline.write_bytes(before)
            self.assertEqual({0x8FD4}, mapped_codepoints(FONT)-mapped_codepoints(baseline))
            self.assertLessEqual(mapped_codepoints(baseline), mapped_codepoints(FONT))
        self.assertEqual(736, struct.unpack_from('>H', tables(before)['maxp'], 4)[0])
        self.assertEqual(737, struct.unpack_from('>H', tables(after)['maxp'], 4)[0])

    def test_all_old_outlines_metrics_and_name_licence_global_tables_are_preserved(self):
        raw = FONT.read_bytes(); before, after = tables(before_m03_font(raw)), tables(raw)
        self.assertEqual(set(before), set(after))
        for tag in ('OS/2', 'hhea', 'name', 'post'):
            self.assertEqual(before[tag], after[tag], tag)
        for tag in ('glyf', 'hmtx', 'loca'):
            self.assertTrue(after[tag].startswith(before[tag]), tag)
        for tag, start, end in [('head',8,12), ('maxp',4,6)]:
            self.assertEqual(before[tag][:start]+before[tag][end:], after[tag][:start]+after[tag][end:], tag)
        # Old long-loca entries and glyph data are identical, so all old compiled outlines remain identical.
        self.assertEqual(1, struct.unpack_from('>h', after['head'], 50)[0])
        self.assertEqual(4, len(after['loca'])-len(before['loca']))

    def test_added_outline_metrics_inventory_and_licence_match_pinned_evidence(self):
        record = json.loads(EVIDENCE.read_text()); raw = FONT.read_bytes(); parts = tables(raw)
        self.assertEqual('U+8FD4', record['addition']['codepoint'])
        self.assertEqual(736, record['addition']['glyph_id'])
        self.assertTrue(record['addition']['identical_to_pinned_source'])
        self.assertEqual('37bd8506257d0905d499395e7f0bc2b6a2ae619dbb635a82ea0905b75b2ff5f3',record['source']['sha256'])
        start, end = struct.unpack_from('>II',parts['loca'],736*4)
        self.assertEqual(record['addition']['outline_sha256'], hashlib.sha256(parts['glyf'][start:end]).hexdigest())
        full_metrics = struct.unpack_from('>H',parts['hhea'],34)[0]
        width = struct.unpack_from('>H',parts['hmtx'],(full_metrics-1)*4)[0]
        bearing = struct.unpack_from('>h',parts['hmtx'],len(parts['hmtx'])-2)[0]
        self.assertEqual(record['addition']['metrics'],[width,bearing])
        inventory = json.loads((FONT.parent/'inventory.json').read_text())
        font = next(r for r in inventory if r['id']=='anpaintnomui')
        self.assertTrue(font['ui_only']); self.assertEqual(record['output']['sha256'],font['sha256'])
        notice = ROOT / record['licence']['unchanged_notice_path']
        self.assertEqual(record['licence']['unchanged_notice_sha256'],hashlib.sha256(notice.read_bytes()).hexdigest())
        # Inventory changes only this digest; sources and licensing are unchanged.
        inventory_text=(FONT.parent/'inventory.json').read_text()
        restored=inventory_text.replace(record['output']['sha256'],record['base']['sha256'])
        self.assertEqual(INVENTORY_BEFORE_SHA,hashlib.sha256(restored.encode()).hexdigest())

    def test_reversal_rejects_old_font_unrelated_damage_missing_and_duplicated_extension(self):
        data = FONT.read_bytes()
        for bad in [before_m03_font(data), data[:-1], data+b'\0', data[:100]+bytes([data[100]^1])+data[101:]]:
            with self.subTest(length=len(bad)), self.assertRaises(AssertionError): before_m03_font(bad)
        raw=(ROOT/'tools/fixtures/commons_metadata_m03_font_scope.json').read_bytes()
        with patch.object(Path,'read_bytes',return_value=raw+b' '):
            with self.assertRaises(AssertionError):font_fixture()

    def test_builder_is_pinned_to_one_existing_licensed_source_and_does_not_download(self):
        text=(ROOT/'tools/extend_nom_m03_ui_font.py').read_text()
        self.assertIn("BASE_SHA = '797ac4ef00f0dd8a982d5216dbd78db3edda07b578b9f8642d0156add90bd526'",text)
        self.assertIn('ADDITIONS = (0x8FD4,)',text)
        self.assertIn('from extend_nom_ui_font import extend',text)
        self.assertNotIn('urllib',text);self.assertNotIn('requests.',text)


INVENTORY_BEFORE_SHA = '7ed694cdf582b716b930d159751139256e1faaeca15cdfafb63f3efc77931bf5'
if __name__ == '__main__': unittest.main()
