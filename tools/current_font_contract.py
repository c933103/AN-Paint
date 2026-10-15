#!/usr/bin/env python3
"""Current bundled glyph, metrics, cmap and licence validator.

This checks product properties, without freezing byte formatting of the fixture,
inventory, source files, or the whole font.
"""
from pathlib import Path
import hashlib
import json
import struct

ASSETS_REL = 'Paintroid/src/main/assets'
# Product glyphs and complete canonical licence paragraph inventories, not source hashes.
REQUIRED_GLYPHS = {'U+651D','U+671D','U+8C6B','U+8FD4','U+3002','U+554F','U+8FFD',
                   'U+4EFD','U+6089','U+6578','U+91CD','U+2A700','U+2CA20'}
LICENCE_PARAGRAPHS = {'MIT': 5, 'OFL-1.1': 21}

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def parts(data):
    require(len(data) >= 12, 'truncated sfnt header')
    result = {}
    count = struct.unpack_from('>H', data, 4)[0]
    directory_end = 12 + 16 * count
    require(directory_end <= len(data), 'truncated sfnt table directory')
    for index in range(count):
        tag, _, offset, length = struct.unpack_from('>4sIII', data, 12 + index * 16)
        tag = tag.decode('ascii')
        if tag in result or offset < directory_end or offset + length > len(data):
            raise AssertionError('invalid or duplicate table ' + tag)
        result[tag] = data[offset:offset + length]
    return result

def require(ok, message):
    if not ok:
        raise AssertionError(message)


def scalar_range(first, last, previous, kind):
    require(first <= last and first > previous,
            f'cmap format {kind}: unordered or overlapping ranges')
    require(last <= 0x10ffff and not (first <= 0xdfff and last >= 0xd800),
            f'cmap format {kind}: range outside Unicode scalar values')


def format12_map(table, num_glyphs):
    _, reserved, length, _, count = struct.unpack_from('>HHIII', table)
    require(reserved == 0, 'cmap format 12: nonzero reserved field')
    require(length == 16 + 12 * count, 'cmap format 12: invalid group count or length')
    groups = []
    previous = -1
    # Validate all bounds and glyph endpoints before expanding any range. A
    # 32-bit count/range cannot cause iteration outside the declared table or
    # beyond the finite Unicode scalar space.
    for index in range(count):
        first, last, gid = struct.unpack_from('>III', table, 16 + 12 * index)
        scalar_range(first, last, previous, 12)
        require(gid + last - first < num_glyphs,
                'cmap format 12: glyph ID outside maxp range')
        groups.append((first, last, gid))
        previous = last
    return {cp: gid + cp - first for first, last, gid in groups
            for cp in range(first, last + 1) if gid + cp - first}


def format4_map(table, num_glyphs):
    _, length, _, count2, search, selector, shift = struct.unpack_from('>7H', table)
    require(count2 > 0 and count2 % 2 == 0, 'cmap format 4: invalid segment count')
    count = count2 // 2
    arrays_end = 16 + 8 * count
    require(length % 2 == 0 and arrays_end <= length,
            'cmap format 4: invalid segment count or length')
    expected_selector = count.bit_length() - 1
    expected_search = 2 * (1 << expected_selector)
    require((search, selector, shift) == (expected_search, expected_selector, count2 - expected_search),
            'cmap format 4: invalid search fields')
    u16 = lambda at: struct.unpack_from('>H', table, at)[0]
    ends = 14
    starts = ends + 2 * count + 2
    deltas = starts + 2 * count
    offsets = deltas + 2 * count
    require(u16(ends + 2 * count) == 0, 'cmap format 4: nonzero reserved pad')
    require(u16(ends + 2 * (count - 1)) == 0xffff, 'cmap format 4: missing final segment')
    segments = []
    previous = -1
    for index in range(count):
        first, last = u16(starts + 2 * index), u16(ends + 2 * index)
        scalar_range(first, last, previous, 4)
        pointer = offsets + 2 * index
        offset, delta = u16(pointer), u16(deltas + 2 * index)
        if offset:
            start = pointer + offset
            stop = start + 2 * (last - first + 1)
            require(offset % 2 == 0 and start >= arrays_end and stop <= length,
                    'cmap format 4: glyph array offset outside subtable')
        else:
            start = None
            highest = ((first + delta) & 0xffff) + last - first
            highest = min(highest, 0xffff)
            require(highest < num_glyphs, 'cmap format 4: glyph ID outside maxp range')
        segments.append((first, last, delta, start))
        previous = last
    mapping = {}
    for first, last, delta, start in segments:
        for cp in range(first, last + 1):
            raw = cp if start is None else u16(start + 2 * (cp - first))
            gid = (raw + delta) & 0xffff if start is None or raw else 0
            require(gid < num_glyphs, 'cmap format 4: glyph ID outside maxp range')
            if gid:
                mapping[cp] = gid
    require(0xffff not in mapping, 'cmap format 4: final sentinel must map to missing glyph')
    return mapping


def unicode_maps(cmap, num_glyphs):
    """Decode bounded format-4/12 Unicode subtables, validating every glyph ID.

    Missing glyph zero contributes no coverage. Shared encoding-record offsets
    are decoded once; non-Unicode subtables do not establish Unicode coverage.
    """
    require(0 < num_glyphs <= 0xffff, 'invalid maxp glyph count')
    require(len(cmap) >= 4, 'truncated cmap header')
    version, count = struct.unpack_from('>HH', cmap)
    records_end = 4 + 8 * count
    require(version == 0 and records_end <= len(cmap), 'invalid cmap header or record count')
    subtables, visited = [], set()
    for index in range(count):
        platform, encoding, base = struct.unpack_from('>HHI', cmap, 4 + 8 * index)
        if platform != 0 and (platform != 3 or encoding not in (1, 10)):
            continue
        require(records_end <= base <= len(cmap) - 2, 'cmap subtable offset outside table')
        if base in visited:
            continue
        visited.add(base)
        kind = struct.unpack_from('>H', cmap, base)[0]
        require(kind in (4, 12), 'unsupported Unicode cmap format ' + str(kind))
        header = 16 if kind == 12 else 14
        require(base + header <= len(cmap), f'cmap format {kind}: truncated header')
        length = struct.unpack_from('>I' if kind == 12 else '>H', cmap, base + (4 if kind == 12 else 2))[0]
        require(header <= length <= len(cmap) - base, f'cmap format {kind}: invalid subtable length')
        subtables.append((base, base + length, kind))
    require(bool(subtables), 'missing Unicode cmap')
    previous_end = records_end
    for start, end, _ in sorted(subtables):
        require(start >= previous_end, 'overlapping Unicode cmap subtables')
        previous_end = end
    return [(kind, (format12_map if kind == 12 else format4_map)(cmap[start:end], num_glyphs))
            for start, end, kind in subtables]


def validated_unicode_maps(font_data):
    tables = parts(font_data)
    require(len(tables['maxp']) >= 6, 'truncated maxp table')
    return unicode_maps(tables['cmap'], struct.unpack_from('>H', tables['maxp'], 4)[0])

def names(table):
    _, count, storage = struct.unpack_from('>HHH',table)
    result = {}
    for i in range(count):
        platform, encoding, language, nameid, size, start = struct.unpack_from('>HHHHHH',table,6+12*i)
        raw = table[storage+start:storage+start+size]
        if platform in (0,3):
            value = raw.decode('utf-16-be')
        elif platform == 1 and encoding == 0:
            value = raw.decode('mac_roman')
        else:
            continue
        result.setdefault(nameid,set()).add(value)
    return result

def errors(font_data, inventory, assets, fixture):
    try:
        return contract_errors(font_data, inventory, assets, fixture)
    except (AssertionError, KeyError, ValueError, struct.error) as exc:
        return ['invalid font or contract: ' + str(exc)]


def contract_errors(font_data, inventory, assets, fixture):
    result=[]
    def check(ok,message):
        if not ok:
            result.append(message)
    records=[r for r in inventory if r['id']==fixture['inventory_id']]
    if len(records)!=1:
        return ['expected one inventory record']
    record=records[0]
    distribution=fixture['distribution']
    check(record['sha256']==sha256(font_data),'inventory digest mismatch')
    check(record['asset']==fixture['font_asset'],'inventory asset mismatch')
    for key in ('name','licence','modified','ui_only'):
        check(record.get(key)==distribution[key],'inventory '+key+' mismatch')
    check(record['licence_file']==distribution['notice'],'inventory notice mismatch')
    sources=fixture['immutable_input_provenance']
    check(record['source']=='https://github.com/nomfoundation/font/releases/tag/'+sources[0]['release'],'primary source attribution mismatch')
    check(record['secondary_source']==sources[1]['url'],'secondary source attribution mismatch')
    p=parts(font_data)
    count=struct.unpack_from('>H',p['maxp'],4)[0]
    maps=unicode_maps(p['cmap'],count)
    loca_format=struct.unpack_from('>h',p['head'],50)[0]
    long_metrics=struct.unpack_from('>H',p['hhea'],34)[0]
    glyphs=fixture['glyphs']
    check({x['codepoint'] for x in glyphs}==REQUIRED_GLYPHS,'required glyph contract inventory differs')
    check(len({x['codepoint'] for x in glyphs})==len(glyphs),'duplicate codepoint in contract')
    check(len({x['glyph_id'] for x in glyphs})==len(glyphs),'duplicate glyph ID in contract')
    for glyph in glyphs:
        cp=int(glyph['codepoint'][2:],16);gid=glyph['glyph_id'];label=glyph['codepoint']
        check(0<gid<count,label+' invalid glyph ID')
        for kind,mapping in maps:
            if kind==12 or cp<=0xffff:
                check(mapping.get(cp)==gid,label+' cmap identity mismatch')
        if loca_format==1:
            start,end=struct.unpack_from('>II',p['loca'],gid*4)
        elif loca_format==0:
            start,end=(v*2 for v in struct.unpack_from('>HH',p['loca'],gid*2))
        else:
            raise AssertionError('invalid loca format')
        outline=p['glyf'][start:end]
        check(len(outline)==glyph['outline_bytes'],label+' outline length mismatch')
        check(sha256(outline)==glyph['outline_sha256'],label+' outline digest mismatch')
        if gid<long_metrics:
            metrics=list(struct.unpack_from('>Hh',p['hmtx'],4*gid))
        else:
            width=struct.unpack_from('>H',p['hmtx'],4*(long_metrics-1))[0]
            bearing=struct.unpack_from('>h',p['hmtx'],4*long_metrics+2*(gid-long_metrics))[0]
            metrics=[width,bearing]
        check(metrics==glyph['metrics'],label+' metrics mismatch')
    metadata=names(p['name'])
    for name_id,expected in [(1,distribution['name']),(4,distribution['name']),(6,distribution['postscript_name']),(13,distribution['embedded_licence']),(14,distribution['embedded_licence_url'])]:
        check(metadata.get(name_id)=={expected},'embedded name/licence field '+str(name_id)+' mismatch')
    normalize=lambda text:' '.join(text.split())
    notice=normalize(assets.get(distribution['notice'],b'').decode('utf-8'))
    for required in [distribution['name'],sources[0]['copyright'],sources[0]['sha256'],sources[1]['url'],sources[1]['git_blob_sha1']]:
        check(required in notice,'missing combined notice term: '+required)
    contracts=distribution['licence_contracts']
    check(len(contracts)==len(LICENCE_PARAGRAPHS) and
          {c['licence'] for c in contracts}==set(LICENCE_PARAGRAPHS),
          'required licence contract inventory differs')
    check({c['source_notice'] for c in contracts}==set(distribution['source_notices']),
          'source notice licence contract mismatch')
    for contract in contracts:
        paragraphs=contract['required_paragraphs']
        check(len(paragraphs)==LICENCE_PARAGRAPHS.get(contract['licence']) and
              all(isinstance(p,str) and p.strip() for p in paragraphs) and len(set(paragraphs))==len(paragraphs),
              'complete canonical licence paragraphs required: '+contract['licence'])
        source_path=contract['source_notice']
        source=normalize(assets.get(source_path,b'').decode('utf-8'))
        # Full canonical paragraphs, copyright and author/RFN attributions are
        # independent of the current copies: consistently truncating all copies
        # cannot satisfy the contract. Whitespace/layout remains unconstrained.
        for index,paragraph in enumerate(contract['required_paragraphs']):
            for path,text in ((source_path,source),(distribution['notice'],notice)):
                check(normalize(paragraph) in text,
                      f"{contract['licence']} required paragraph {index + 1} absent from {path}")
        for attribution in contract.get('source_only_attribution',[]):
            check(normalize(attribution) in source,'source attribution absent from '+source_path)
    for path in distribution['aggregates']:
        check(bool(notice) and notice in normalize(assets.get(path,b'').decode('utf-8')),
              'combined notice absent from '+path)
    return result

def load(root, fixture):
    assets_dir=Path(root)/ASSETS_REL
    assets={path:(assets_dir/path).read_bytes() for path in [fixture['distribution']['notice'],*fixture['distribution']['source_notices'],*fixture['distribution']['aggregates']]}
    font=(assets_dir/fixture['font_asset']).read_bytes()
    inventory=json.loads((assets_dir/'fonts/inventory.json').read_text())
    return font,inventory,assets
