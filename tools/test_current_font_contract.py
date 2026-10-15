"""Current font glyph/licence checks and real byte-level corruption controls."""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import re
import struct
import unittest
from current_font_contract import errors, load, parts, validated_unicode_maps

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


def valid_checksums(data):
    """Mutants retain table and whole-font checksums, plus matching inventory."""
    data=bytearray(data)
    checksum=lambda value:sum(struct.unpack('>'+'I'*((len(value)+3)//4),bytes(value)+b'\0'*(-len(value)%4)))&0xffffffff
    head,_,_=location(data,'head')
    struct.pack_into('>I',data,head+8,0)
    for index in range(struct.unpack_from('>H',data,4)[0]):
        entry=12+16*index
        _,_,offset,length=struct.unpack_from('>4sIII',data,entry)
        struct.pack_into('>I',data,entry+4,checksum(data[offset:offset+length]))
    struct.pack_into('>I',data,head+8,(0xb1b0afba-checksum(data))&0xffffffff)
    assert checksum(data)==0xb1b0afba
    return bytes(data)


def subtable(data,kind):
    offset,_,_=location(data,'cmap')
    for index in range(struct.unpack_from('>H',data,offset+2)[0]):
        platform,encoding,relative=struct.unpack_from('>HHI',data,offset+4+8*index)
        base=offset+relative
        if (platform==0 or platform==3 and encoding in (1,10)) and struct.unpack_from('>H',data,base)[0]==kind:
            return base
    raise AssertionError('missing requested cmap format')


def format4_segments(data):
    base=subtable(data,4)
    count=struct.unpack_from('>H',data,base+6)[0]//2
    starts=base+16+2*count
    deltas=starts+2*count
    offsets=deltas+2*count
    for index in range(count):
        first=struct.unpack_from('>H',data,starts+2*index)[0]
        last=struct.unpack_from('>H',data,base+14+2*index)[0]
        yield first,last,deltas+2*index,offsets+2*index


def format12_groups(data):
    base=subtable(data,12)
    for index in range(struct.unpack_from('>I',data,base+12)[0]):
        at=base+16+12*index
        yield (*struct.unpack_from('>III',data,at),at)


def replace_all_notices(assets,pattern):
    """Remove matching text consistently, including both displayed aggregates."""
    updated=assets.copy()
    for path,data in updated.items():
        updated[path]=re.sub(pattern,'',data.decode('utf-8'),flags=re.DOTALL).encode('utf-8')
    return updated

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
                            struct.pack_into('>I',data,at+8,gid-1)
                self.assert_error(valid_checksums(data),glyph['codepoint']+' cmap identity mismatch')

    def test_inventory_digest_and_ui_role_rejected(self):
        inventory=deepcopy(INVENTORY);row=next(r for r in inventory if r['id']=='anpaintnomui');row['sha256']='0'*64
        self.assert_error(FONT,'inventory digest mismatch',inventory=inventory)
        row['ui_only']=False
        self.assert_error(FONT,'inventory ui_only mismatch',inventory=inventory)

    def test_missing_glyph_or_licence_contract_cannot_make_checks_vacuous(self):
        for mutation in ('glyphs','one-glyph','licences','paragraphs','one-paragraph'):
            fixture=deepcopy(FIXTURE)
            if mutation=='glyphs': fixture['glyphs']=[]
            if mutation=='one-glyph': fixture['glyphs'].pop()
            if mutation=='licences': fixture['distribution']['licence_contracts']=[]
            if mutation=='paragraphs': fixture['distribution']['licence_contracts'][0]['required_paragraphs']=[]
            if mutation=='one-paragraph': fixture['distribution']['licence_contracts'][1]['required_paragraphs'].pop()
            with self.subTest(mutation=mutation):
                self.assertTrue(errors(FONT,INVENTORY,ASSETS,fixture))

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
        self.assert_error(FONT,'MIT required paragraph 4 absent from '+notice,assets=assets)

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

class CmapBoundaryTest(unittest.TestCase):
    def assert_invalid(self,data,reason):
        data=valid_checksums(data)
        found=errors(data,with_matching_inventory(data),ASSETS,FIXTURE)
        self.assertTrue(any(reason in item for item in found),found)
        with self.assertRaisesRegex(AssertionError,re.escape(reason)):
            validated_unicode_maps(data)
        # The retained coverage helper must reject the same malformed font;
        # simply exposing the old unchecked codepoint set is not sufficient.
        from test_locale_font_coverage import mapped_codepoints
        class FontBytes:
            def read_bytes(self):return data
        with self.assertRaisesRegex(AssertionError,re.escape(reason)):
            mapped_codepoints(FontBytes())

    def mutate(self,kind,relative,fmt,value):
        data=bytearray(FONT)
        struct.pack_into(fmt,data,subtable(data,kind)+relative,value)
        return data

    def test_format4_each_protected_mapping_corruption_is_rejected(self):
        for glyph in FIXTURE['glyphs']:
            cp=int(glyph['codepoint'][2:],16)
            if cp > 0xffff:
                continue  # Supplementary mappings exist only in format 12.
            with self.subTest(codepoint=glyph['codepoint']):
                data=bytearray(FONT)
                for first,last,delta_at,offset_at in format4_segments(data):
                    if first<=cp<=last:
                        delta=struct.unpack_from('>H',data,delta_at)[0]
                        offset=struct.unpack_from('>H',data,offset_at)[0]
                        if offset:
                            at=offset_at+offset+2*(cp-first)
                            raw=struct.unpack_from('>H',data,at)[0]
                            struct.pack_into('>H',data,at,(raw-1)&0xffff)
                        else:
                            struct.pack_into('>H',data,delta_at,(delta-1)&0xffff)
                        break
                data=valid_checksums(data)
                self.assertIn(glyph['codepoint']+' cmap identity mismatch',
                              errors(data,with_matching_inventory(data),ASSETS,FIXTURE))

    def test_supplementary_position_glyphs_are_mapped_only_in_format12(self):
        maps=validated_unicode_maps(FONT)
        for cp in (0x2a700,0x2ca20):
            glyph=next(g for g in FIXTURE['glyphs'] if int(g['codepoint'][2:],16)==cp)
            for kind,mapping in maps:
                if kind==12:self.assertEqual(glyph['glyph_id'],mapping.get(cp))
                else:self.assertNotIn(cp,mapping)

    def test_format12_nonexistent_supplementary_glyph_rejected(self):
        data=bytearray(FONT)
        first,last,gid,at=next(group for group in format12_groups(data) if group[0]<=0x2e7b6<=group[1])
        self.assertEqual((0x2e7b6,0x2e7b6,732),(first,last,gid))
        struct.pack_into('>I',data,at+8,65535)
        self.assert_invalid(data,'cmap format 12: glyph ID outside maxp range')

    def test_format12_checks_range_endpoint_before_expansion(self):
        data=bytearray(FONT)
        first,last,gid,at=list(format12_groups(data))[-1]
        count=struct.unpack_from('>H',parts(data)['maxp'],4)[0]
        struct.pack_into('>III',data,at,first,first+10,count-5)
        self.assert_invalid(data,'cmap format 12: glyph ID outside maxp range')

    def test_format4_nonexistent_array_glyph_rejected(self):
        data=bytearray(FONT)
        first,last,delta_at,offset_at=next(s for s in format4_segments(data) if struct.unpack_from('>H',data,s[3])[0])
        delta=struct.unpack_from('>H',data,delta_at)[0]
        offset=struct.unpack_from('>H',data,offset_at)[0]
        count=struct.unpack_from('>H',parts(data)['maxp'],4)[0]
        struct.pack_into('>H',data,offset_at+offset,(count-delta)&0xffff)
        self.assert_invalid(data,'cmap format 4: glyph ID outside maxp range')

    def test_format4_nonexistent_delta_glyph_rejected(self):
        data=bytearray(FONT)
        first,last,delta_at,offset_at=next(s for s in format4_segments(data) if s[1]!=0xffff and not struct.unpack_from('>H',data,s[3])[0])
        count=struct.unpack_from('>H',parts(data)['maxp'],4)[0]
        struct.pack_into('>H',data,delta_at,(count-first)&0xffff)
        self.assert_invalid(data,'cmap format 4: glyph ID outside maxp range')

    def test_format4_declared_lengths_are_enforced(self):
        for length in (0,13,15,16,65535):
            with self.subTest(length=length):
                self.assert_invalid(self.mutate(4,2,'>H',length),'cmap format 4:')

    def test_format12_declared_lengths_are_enforced(self):
        for length in (0,15,16,0xffffffff):
            with self.subTest(length=length):
                self.assert_invalid(self.mutate(12,4,'>I',length),'cmap format 12:')

    def test_format4_length_cannot_claim_the_next_unicode_subtable(self):
        length=struct.unpack_from('>H',FONT,subtable(FONT,4)+2)[0]
        self.assert_invalid(self.mutate(4,2,'>H',length+2),'overlapping Unicode cmap subtables')

    def test_truncated_cmap_headers_cannot_read_other_sfnt_bytes(self):
        for kind,header in ((4,14),(12,16)):
            with self.subTest(kind=kind):
                data=bytearray(FONT)
                base=subtable(data,kind)
                cmap,_,directory=location(data,'cmap')
                struct.pack_into('>I',data,directory+12,base-cmap+header-1)
                self.assert_invalid(data,f'cmap format {kind}: truncated header')

    def test_truncated_format12_group_cannot_read_other_sfnt_bytes(self):
        data=bytearray(FONT)
        _,length,directory=location(data,'cmap')
        struct.pack_into('>I',data,directory+12,length-1)
        self.assert_invalid(data,'cmap format 12: invalid subtable length')

    def test_segment_and_group_counts_are_bounded_before_iteration(self):
        for kind,relative,fmt,value in ((4,6,'>H',0),(4,6,'>H',3),(4,6,'>H',65534),(12,12,'>I',0xffffffff)):
            with self.subTest(kind=kind,value=value):
                self.assert_invalid(self.mutate(kind,relative,fmt,value),f'cmap format {kind}: invalid')

    def test_format4_glyph_offsets_stay_in_its_declared_subtable(self):
        for offset in (1,2,65534):
            with self.subTest(offset=offset):
                data=bytearray(FONT)
                *_,pointer=next(format4_segments(data))
                struct.pack_into('>H',data,pointer,offset)
                self.assert_invalid(data,'cmap format 4: glyph array offset outside subtable')

    def test_format4_overlapping_and_reversed_segments_rejected(self):
        for overlap in (True,False):
            with self.subTest(overlap=overlap):
                data=bytearray(FONT);base=subtable(data,4)
                count=struct.unpack_from('>H',data,base+6)[0]//2
                starts=base+16+2*count
                last=struct.unpack_from('>H',data,base+14)[0]
                struct.pack_into('>H',data,starts+(2 if overlap else 0),last if overlap else last+1)
                self.assert_invalid(data,'cmap format 4: unordered or overlapping ranges')

    def test_format12_unordered_overlapping_and_reversed_groups_rejected(self):
        for change in ('overlap','reverse','unsorted'):
            with self.subTest(change=change):
                data=bytearray(FONT)
                groups=list(format12_groups(data));first,last,gid,at=groups[1]
                if change=='overlap':first=groups[0][1]
                elif change=='reverse':first=last+1
                else:first=last=0
                struct.pack_into('>III',data,at,first,last,gid)
                self.assert_invalid(data,'cmap format 12: unordered or overlapping ranges')

    def test_format12_non_unicode_and_surrogate_ranges_rejected(self):
        for first,last in ((0,0xffffffff),(0x110000,0x110000),(0xd800,0xd800),(0xd7ff,0xe000)):
            with self.subTest(first=first,last=last):
                data=bytearray(FONT);at=next(format12_groups(data))[3]
                struct.pack_into('>III',data,at,first,last,1)
                self.assert_invalid(data,'cmap format 12: range outside Unicode scalar values')

    def test_format4_surrogate_range_rejected(self):
        data=bytearray(FONT);base=subtable(data,4)
        count=struct.unpack_from('>H',data,base+6)[0]//2
        struct.pack_into('>H',data,base+14,0xd800)
        struct.pack_into('>H',data,base+16+2*count,0xd800)
        self.assert_invalid(data,'cmap format 4: range outside Unicode scalar values')

    def test_cmap_record_count_and_offsets_are_bounded(self):
        for relative,fmt,value,reason in ((2,'>H',65535,'invalid cmap header or record count'),(8,'>I',0,'cmap subtable offset outside table'),(8,'>I',0xffffffff,'cmap subtable offset outside table')):
            with self.subTest(relative=relative,value=value):
                data=bytearray(FONT);base,_,_=location(data,'cmap')
                struct.pack_into(fmt,data,base+relative,value)
                self.assert_invalid(data,reason)

    def test_reserved_and_format4_search_fields_rejected(self):
        base=subtable(FONT,4);count=struct.unpack_from('>H',FONT,base+6)[0]//2
        for kind,relative in ((12,2),(4,14+2*count),(4,8),(4,10),(4,12)):
            with self.subTest(kind=kind,relative=relative):
                data=bytearray(FONT);at=subtable(data,kind)+relative
                struct.pack_into('>H',data,at,struct.unpack_from('>H',data,at)[0]^1)
                self.assert_invalid(data,f'cmap format {kind}:')

    def test_zero_glyph_does_not_establish_coverage(self):
        data=bytearray(FONT)
        at=next(g[3] for g in format12_groups(data) if g[0]==g[1]==0x2e7b6)
        struct.pack_into('>I',data,at+8,0)
        data=valid_checksums(data)
        points={cp for _,mapping in validated_unicode_maps(data) for cp in mapping}
        self.assertNotIn(0x2e7b6,points)
        self.assertEqual([],errors(data,with_matching_inventory(data),ASSETS,FIXTURE))

    def test_maxp_count_is_required(self):
        data=bytearray(FONT);base,_,_=location(data,'maxp')
        struct.pack_into('>H',data,base+4,0)
        self.assert_invalid(data,'invalid maxp glyph count')


class CompleteLicenceContractTest(unittest.TestCase):
    def assert_licence_rejected(self,assets,licence):
        found=errors(FONT,INVENTORY,assets,FIXTURE)
        self.assertTrue(any(licence+' required paragraph' in item for item in found),found)

    def test_unrelated_nonempty_source_notices_rejected(self):
        for contract in FIXTURE['distribution']['licence_contracts']:
            with self.subTest(licence=contract['licence']):
                assets=ASSETS.copy();assets[contract['source_notice']]=b'removed\n'
                self.assert_licence_rejected(assets,contract['licence'])

    def test_every_canonical_paragraph_is_independently_required_in_every_copy(self):
        # Mutate each complete permission, condition, disclaimer, definition and
        # attribution consistently across source, combined and aggregate copies.
        # The unchanged fixture is independent of all mutated distribution text.
        for contract in FIXTURE['distribution']['licence_contracts']:
            for paragraph in contract['required_paragraphs']:
                with self.subTest(licence=contract['licence'],paragraph=paragraph[:75]):
                    pattern=r'\s+'.join(re.escape(word) for word in paragraph.split())
                    assets=replace_all_notices(ASSETS,pattern)
                    self.assertNotEqual(ASSETS[contract['source_notice']],assets[contract['source_notice']])
                    self.assertNotEqual(ASSETS[FIXTURE['distribution']['notice']],assets[FIXTURE['distribution']['notice']])
                    self.assert_licence_rejected(assets,contract['licence'])

    def test_entire_ofl_permission_and_conditions_block_removed_consistently(self):
        assets=replace_all_notices(ASSETS,r'PERMISSION & CONDITIONS.*?(?=TERMINATION)')
        self.assert_licence_rejected(assets,'OFL-1.1')

    def test_mit_permission_condition_and_disclaimer_removal_consistently(self):
        for start,end in ((r'Permission is hereby granted, free of charge, to any person obtaining a copy of this software',r'The above copyright notice'),(r'The above copyright notice',r'THE SOFTWARE IS PROVIDED'),(r'THE SOFTWARE IS PROVIDED',r'OTHER DEALINGS IN THE SOFTWARE\.')):
            with self.subTest(start=start):
                assets=replace_all_notices(ASSETS,start+r'.*?'+end)
                self.assert_licence_rejected(assets,'MIT')

    def test_source_only_repository_attribution_retained(self):
        assets=ASSETS.copy();path=FIXTURE['distribution']['source_notices'][0]
        assets[path]=assets[path].replace(b'Repository notice: Copyright (c) 2019 nomfoundation',b'')
        self.assertIn('source attribution absent from '+path,errors(FONT,INVENTORY,assets,FIXTURE))

    def test_semantically_identical_notice_whitespace_is_allowed(self):
        assets={path:(' \n\t '.join(data.decode('utf-8').split())).encode('utf-8') for path,data in ASSETS.items()}
        self.assertEqual([],errors(FONT,INVENTORY,assets,FIXTURE))


if __name__=='__main__':unittest.main(verbosity=2)
