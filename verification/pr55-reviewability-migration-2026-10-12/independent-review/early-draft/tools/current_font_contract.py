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

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def parts(data):
    result = {}
    count = struct.unpack_from('>H', data, 4)[0]
    for index in range(count):
        tag, _, offset, length = struct.unpack_from('>4sIII', data, 12 + index * 16)
        tag = tag.decode('ascii')
        if tag in result or offset + length > len(data):
            raise AssertionError('invalid or duplicate table ' + tag)
        result[tag] = data[offset:offset + length]
    return result

def unicode_maps(cmap):
    u16 = lambda at: struct.unpack_from('>H', cmap, at)[0]
    u32 = lambda at: struct.unpack_from('>I', cmap, at)[0]
    result = []
    for i in range(u16(2)):
        entry = 4 + 8*i
        platform, encoding = u16(entry), u16(entry+2)
        if platform != 0 and (platform != 3 or encoding not in (1, 10)):
            continue
        base = u32(entry+4)
        kind = u16(base)
        mapping = {}
        if kind == 12:
            for group in range(u32(base+12)):
                first,last,gid = struct.unpack_from('>III',cmap,base+16+12*group)
                for cp in range(first,last+1):
                    if gid+cp-first:
                        mapping[cp] = gid+cp-first
        elif kind == 4:
            count = u16(base+6)//2
            ends = base+14
            starts = ends+2*count+2
            deltas = starts+2*count
            offsets = deltas+2*count
            for j in range(count):
                first,last = u16(starts+2*j),u16(ends+2*j)
                delta,pointer = u16(deltas+2*j),offsets+2*j
                offset = u16(pointer)
                for cp in range(first,min(last,0xfffe)+1):
                    gid = u16(pointer+offset+2*(cp-first)) if offset else cp
                    if offset and not gid:
                        continue
                    gid = (gid+delta)&0xffff
                    if gid:
                        mapping[cp] = gid
        else:
            raise AssertionError('unsupported Unicode cmap format ' + str(kind))
        result.append((kind,mapping))
    if not result:
        raise AssertionError('missing Unicode cmap')
    return result

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
    maps=unicode_maps(p['cmap'])
    count=struct.unpack_from('>H',p['maxp'],4)[0]
    loca_format=struct.unpack_from('>h',p['head'],50)[0]
    long_metrics=struct.unpack_from('>H',p['hhea'],34)[0]
    glyphs=fixture['glyphs']
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
    notice=assets.get(distribution['notice'],b'').decode('utf-8').strip()
    for required in [distribution['name'],sources[0]['copyright'],sources[0]['sha256'],sources[1]['git_blob_sha1'],'Permission is hereby granted, free of charge','The above copyright notice and this permission notice','SIL OPEN FONT LICENSE Version 1.1','Copyright 2014-2021 Adobe',"Reserved Font\nName 'Source'"]:
        check(required in notice,'missing combined notice term: '+required)
    for path in distribution['source_notices']:
        check(bool(assets.get(path,b'').strip()),'missing source notice '+path)
    for path in distribution['aggregates']:
        check(bool(notice) and notice in assets.get(path,b'').decode('utf-8'),'combined notice absent from '+path)
    return result

def load(root, fixture):
    assets_dir=Path(root)/ASSETS_REL
    assets={path:(assets_dir/path).read_bytes() for path in [fixture['distribution']['notice'],*fixture['distribution']['source_notices'],*fixture['distribution']['aggregates']]}
    font=(assets_dir/fixture['font_asset']).read_bytes()
    inventory=json.loads((assets_dir/'fonts/inventory.json').read_text())
    return font,inventory,assets

