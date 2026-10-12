"""M04 three-glyph preservation, strict historical reversal and coverage."""
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

from commons_metadata_m04_font_scope import before_m04_font, before_m04_inventory, font_fixture
from test_locale_font_coverage import mapped_codepoints
from test_commons_metadata_m03_font import tables

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / 'Paintroid/src/main/assets/fonts/anpaintnomui.ttf'
EVIDENCE = ROOT / 'verification/commons-metadata-m04-2026-10-12/nom-font-extension.json'


class CommonsMetadataM04FontContracts(unittest.TestCase):
    def test_exact_three_glyph_delta_restores_the_unchanged_m03_font(self):
        after = FONT.read_bytes(); scope = font_fixture(); before = before_m04_font(after)
        self.assertEqual(['U+3002','U+554F','U+8FFD'], scope['additions'])
        self.assertEqual('4ae4cab599622f6c9d66b8a99074f2a291ffc32000a78ba69f241fc12eb64e05', hashlib.sha256(before).hexdigest())
        self.assertEqual('6b70d3c5c146c9d11503e5dff7ade5e7ccb3ae5a70c511f71902d4a75f7a3006', hashlib.sha256(after).hexdigest())
        with tempfile.TemporaryDirectory() as folder:
            baseline = Path(folder)/'pre-m04.ttf'; baseline.write_bytes(before)
            self.assertEqual({0x3002,0x554F,0x8FFD}, mapped_codepoints(FONT)-mapped_codepoints(baseline))
            self.assertLessEqual(mapped_codepoints(baseline), mapped_codepoints(FONT))
        self.assertEqual(737, struct.unpack_from('>H', tables(before)['maxp'],4)[0])
        self.assertEqual(740, struct.unpack_from('>H', tables(after)['maxp'],4)[0])

    def test_all_old_outlines_metrics_and_name_licence_global_tables_are_preserved(self):
        raw = FONT.read_bytes(); before, after = tables(before_m04_font(raw)), tables(raw)
        self.assertEqual(set(before),set(after))
        for tag in ('OS/2','hhea','name','post'): self.assertEqual(before[tag],after[tag],tag)
        for tag in ('glyf','hmtx','loca'): self.assertTrue(after[tag].startswith(before[tag]),tag)
        for tag,start,end in [('head',8,12),('maxp',4,6)]:
            self.assertEqual(before[tag][:start]+before[tag][end:],after[tag][:start]+after[tag][end:],tag)
        self.assertEqual(1,struct.unpack_from('>h',after['head'],50)[0])
        self.assertEqual(12,len(after['loca'])-len(before['loca']))

    def test_added_outlines_metrics_inventory_and_licence_match_pinned_evidence(self):
        record=json.loads(EVIDENCE.read_text());raw=FONT.read_bytes();parts=tables(raw)
        self.assertEqual('37bd8506257d0905d499395e7f0bc2b6a2ae619dbb635a82ea0905b75b2ff5f3',record['source']['sha256'])
        self.assertEqual(['U+3002','U+554F','U+8FFD'],[a['codepoint'] for a in record['additions']])
        for i,addition in enumerate(record['additions']):
            gid=737+i;self.assertEqual(gid,addition['glyph_id']);self.assertTrue(addition['identical_to_pinned_source'])
            start,end=struct.unpack_from('>II',parts['loca'],gid*4)
            self.assertEqual(addition['outline_sha256'],hashlib.sha256(parts['glyf'][start:end]).hexdigest())
            full_metrics=struct.unpack_from('>H',parts['hhea'],34)[0]
            width=struct.unpack_from('>H',parts['hmtx'],(full_metrics-1)*4)[0]
            bearing=struct.unpack_from('>h',parts['hmtx'],full_metrics*4+(gid-full_metrics)*2)[0]
            self.assertEqual(addition['metrics'],[width,bearing])
        inventory_text=(FONT.parent/'inventory.json').read_text()
        self.assertEqual(record['inventory']['after_sha256'],hashlib.sha256(inventory_text.encode()).hexdigest())
        self.assertEqual(record['inventory']['before_sha256'],hashlib.sha256(before_m04_inventory(inventory_text).encode()).hexdigest())
        font=next(row for row in json.loads(inventory_text) if row['id']=='anpaintnomui')
        self.assertTrue(font['ui_only']);self.assertEqual(record['output']['sha256'],font['sha256'])
        self.assertEqual(record['licence']['unchanged_notice_sha256'],hashlib.sha256((ROOT/record['licence']['unchanged_notice_path']).read_bytes()).hexdigest())

    def test_reversal_rejects_old_font_damage_missing_and_duplicated_extensions(self):
        data=FONT.read_bytes()
        for bad in [before_m04_font(data),data[:-1],data+b'\0',data[:100]+bytes([data[100]^1])+data[101:]]:
            with self.subTest(length=len(bad)),self.assertRaises(AssertionError):before_m04_font(bad)
        raw=(ROOT/'tools/fixtures/commons_metadata_m04_font_scope.json').read_bytes()
        with patch.object(Path,'read_bytes',return_value=raw+b' '),self.assertRaises(AssertionError):font_fixture()
        text=(FONT.parent/'inventory.json').read_text();digest=font_fixture()['after_sha256']
        for wrong in [text.replace(digest,'0'*64),text+digest]:
            with self.assertRaises(AssertionError):before_m04_inventory(wrong)

    def test_builder_uses_only_the_reviewed_glyphs_and_existing_licensed_source(self):
        text=(ROOT/'tools/extend_nom_m04_ui_font.py').read_text()
        self.assertIn("BASE_SHA = '4ae4cab599622f6c9d66b8a99074f2a291ffc32000a78ba69f241fc12eb64e05'",text)
        self.assertIn('ADDITIONS = (0x3002, 0x554F, 0x8FFD)',text)
        self.assertIn('from extend_nom_ui_font import extend',text)
        self.assertNotIn('urllib',text);self.assertNotIn('requests.',text)


if __name__ == '__main__':unittest.main()
