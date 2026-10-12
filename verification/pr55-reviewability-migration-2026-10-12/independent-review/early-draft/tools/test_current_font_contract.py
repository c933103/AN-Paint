"""Current font glyph/licence checks and real byte-level corruption controls."""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import struct
import unittest
from current_font_contract import errors, load, parts

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=json.loads((Path(__file__).parent/'fixtures/current_localization/nom_current_font_contract.json').read_text())
FONT,INVENTORY,ASSETS=load(ROOT,FIXTURE)

def location(data,tag):
    for i in range(struct.unpack_from('>H',data,4)[0]):
        current,_,offset,length=struct.unpack_from('>4sIII',data,12+16*i)
        if current.decode()==tag:
            return offset,length,12+16*i
    raise KeyError(tag)

def with_matching_inventory(data):
    inventory=deepcopy(INVENTORY)
    next(r for r in inventory if r['id']=='anpaintnomui')['sha256']=hashlib.sha256(data).hexdigest()
    return inventory

class CurrentFontContractTest(unittest.TestCase):
    def assert_error(self, data, expected, inventory=None, assets=None, fixture=None):
        found=errors(data,with_matching_inventory(data) if inventory is None else inventory,ASSETS if assets is None else assets,FIXTURE if fixture is None else fixture)
        self.assertIn(expected,found)

    def test_actual_current_font(self):
        self.assertEqual([],errors(FONT,INVENTORY,ASSETS,FIXTURE))

    def test_each_glyph_outline_corruption_rejected_with_updated_inventory(self):
        glyf,_,_=location(FONT,'glyf'); p=parts(FONT)
        for glyph in FIXTURE['glyphs']:
            with self.subTest(codepoint=glyph['codepoint']):
                start,end=struct.unpack_from('>II',p['loca'],4*glyph['glyph_id'])
                data=bytearray(FONT);data[glyf+end-1]^=1
                self.assert_error(data,glyph['codepoint']+' outline digest mismatch')

    def test_each_glyph_metric_corruption_rejected_with_updated_inventory(self):
        hmtx,_,_=location(FONT,'hmtx');p=parts(FONT);count=struct.unpack_from('>H',p['hhea'],34)[0]
        for glyph in FIXTURE['glyphs']:
            with self.subTest(codepoint=glyph['codepoint']):
                gid=glyph['glyph_id']; offset=hmtx+(4*gid+2 if gid<count else 4*count+2*(gid-count))
                data=bytearray(FONT);data[offset+1]^=1
                self.assert_error(data,glyph['codepoint']+' metrics mismatch')

    def test_mapping_mismatch_rejected_independently_of_outline(self):
        offset,_,_=location(FONT,'cmap')
        for glyph in FIXTURE['glyphs']:
            cp=int(glyph['codepoint'][2:],16)
            with self.subTest(codepoint=glyph['codepoint']):
                data=bytearray(FONT)
                for i in range(struct.unpack_from('>H',data,offset+2)[0]):
                    platform,encoding,relative=struct.unpack_from('>HHI',data,offset+4+8*i)
                    base=offset+relative
                    if struct.unpack_from('>H',data,base)[0]!=12:continue
                    for j in range(struct.unpack_from('>I',data,base+12)[0]):
                        at=base+16+12*j;first,last,gid=struct.unpack_from('>III',data,at)
                        if first<=cp<=last:
                            struct.pack_into('>I',data,at+8,gid+1)
                self.assert_error(data,glyph['codepoint']+' cmap identity mismatch')

    def test_inventory_digest_and_ui_role_rejected(self):
        inventory=deepcopy(INVENTORY);row=next(r for r in inventory if r['id']=='anpaintnomui');row['sha256']='0'*64
        self.assert_error(FONT,'inventory digest mismatch',inventory=inventory)
        row['ui_only']=False
        self.assert_error(FONT,'inventory ui_only mismatch',inventory=inventory)

    def test_fixture_duplicates_rejected(self):
        fixture=deepcopy(FIXTURE);fixture['glyphs'].append(fixture['glyphs'][0])
        self.assert_error(FONT,'duplicate codepoint in contract',fixture=fixture)

    def test_missing_notice_and_aggregate_rejected(self):
        for path in [FIXTURE['distribution']['notice'],*FIXTURE['distribution']['source_notices'],*FIXTURE['distribution']['aggregates']]:
            with self.subTest(path=path):
                assets=ASSETS.copy();assets[path]=b''
                self.assertTrue(errors(FONT,INVENTORY,assets,FIXTURE))

    def test_missing_mit_notice_term_rejected(self):
        assets=ASSETS.copy();notice=FIXTURE['distribution']['notice']
        assets[notice]=assets[notice].replace(b'The above copyright notice and this permission notice',b'')
        self.assert_error(FONT,'missing combined notice term: The above copyright notice and this permission notice',assets=assets)

    def test_embedded_name_metadata_change_rejected(self):
        data=FONT.replace('AN Paint Nom UI'.encode('utf-16-be'),'AN Paint Bad UI'.encode('utf-16-be'))
        self.assertNotEqual(FONT,data)
        self.assert_error(data,'embedded name/licence field 1 mismatch')

    def test_semantically_identical_json_reformat_is_allowed(self):
        self.assertEqual([],errors(FONT,json.loads(json.dumps(INVENTORY,separators=(',',':'))),ASSETS,json.loads(json.dumps(FIXTURE,sort_keys=True))))

    def test_new_timestamp_with_valid_checksums_and_inventory_is_allowed(self):
        data=bytearray(FONT);head,length,directory=location(data,'head')
        # Touch the timestamp while keeping a valid sfnt checksum. This protects
        # the intended distinction between current glyph properties and a frozen
        # whole-font byte snapshot.
        data[head+35]^=1
        struct.pack_into('>I',data,head+8,0)
        checksum=lambda value:sum(struct.unpack('>'+'I'*((len(value)+3)//4),value+b'\0'*((-len(value))%4)))&0xffffffff
        struct.pack_into('>I',data,directory+4,checksum(data[head:head+length]))
        struct.pack_into('>I',data,head+8,(0xb1b0afba-checksum(data))&0xffffffff)
        self.assertEqual(0xb1b0afba,checksum(data))
        self.assertNotEqual(FONT,data)
        self.assertEqual([],errors(data,with_matching_inventory(data),ASSETS,FIXTURE))

if __name__=='__main__':unittest.main(verbosity=2)
