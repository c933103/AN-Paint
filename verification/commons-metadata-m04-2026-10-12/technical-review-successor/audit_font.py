#!/usr/bin/env python3
"""Independent font audit against local exact-content baseline and pinned source."""
import argparse, hashlib, io, json, pathlib, struct, subprocess
from fontTools.ttLib import TTFont
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo',type=pathlib.Path,required=True)
parser.add_argument('--source',type=pathlib.Path,required=True)
parser.add_argument('--output',type=pathlib.Path,required=True)
args=parser.parse_args()
ROOT=args.repo.resolve();OUT=args.output.resolve();OUT.mkdir(parents=True,exist_ok=True)
BASE='4231edaac45d89c52f51e2b77d0f94a1176ad88c'
assert subprocess.check_output(['git','rev-parse',BASE+'^{tree}'],cwd=ROOT,text=True).strip()=='c1d65b3f0f89a8af12a9dbe69eb1824ef19e28c1'
P='Paintroid/src/main/assets/fonts/anpaintnomui.ttf'
SOURCE=args.source.resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
def baseline(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def tables(b):
 result={}
 for i in range(struct.unpack_from('>H',b,4)[0]):
  tag,checksum,offset,length=struct.unpack_from('>4sIII',b,12+i*16)
  result[tag.decode()]=b[offset:offset+length]
 return result
oldraw,newraw,srcraw=baseline(P),(ROOT/P).read_bytes(),SOURCE.read_bytes()
assert sha(oldraw)=='4ae4cab599622f6c9d66b8a99074f2a291ffc32000a78ba69f241fc12eb64e05'
assert sha(newraw)=='6b70d3c5c146c9d11503e5dff7ade5e7ccb3ae5a70c511f71902d4a75f7a3006'
assert sha(srcraw)=='37bd8506257d0905d499395e7f0bc2b6a2ae619dbb635a82ea0905b75b2ff5f3'
old,new,src=(TTFont(io.BytesIO(b),recalcBBoxes=False,recalcTimestamp=False) for b in (oldraw,newraw,srcraw))
additions=(0x3002,0x554F,0x8FFD)
oldorder,neworder=old.getGlyphOrder(),new.getGlyphOrder()
assert neworder==oldorder+[src.getBestCmap()[cp] for cp in additions]
assert len(oldorder)==737 and len(neworder)==740
for name in oldorder:
 assert old['glyf'][name].compile(old['glyf'])==new['glyf'][name].compile(new['glyf']),name
 assert old['hmtx'].metrics[name]==new['hmtx'].metrics[name],name
assert len(old['cmap'].tables)==len(new['cmap'].tables)
cmap_report=[]
for before,after in zip(old['cmap'].tables,new['cmap'].tables):
 assert (before.platformID,before.platEncID,before.format,before.language)==(after.platformID,after.platEncID,after.format,after.language)
 expected=dict(before.cmap)
 if before.isUnicode() and before.format in (4,12):expected.update({cp:src.getBestCmap()[cp] for cp in additions})
 assert after.cmap==expected
 cmap_report.append(dict(platform=before.platformID,encoding=before.platEncID,format=before.format,old_count=len(before.cmap),new_count=len(after.cmap)))
bt,nt=tables(oldraw),tables(newraw)
assert bt.keys()==nt.keys()
for tag in ('OS/2','hhea','name','post'):assert bt[tag]==nt[tag],tag
for tag,start,end in [('head',8,12),('maxp',4,6)]:assert bt[tag][:start]+bt[tag][end:]==nt[tag][:start]+nt[tag][end:],tag
for tag in ('glyf','loca','hmtx'):assert nt[tag].startswith(bt[tag]),tag
for tag in bt.keys()-{'OS/2','hhea','name','post','head','maxp','glyf','loca','hmtx','cmap'}:assert bt[tag]==nt[tag],tag
added=[]
for cp in additions:
 name=new.getBestCmap()[cp];source_name=src.getBestCmap()[cp]
 glyph=new['glyf'][name];assert not glyph.isComposite() and glyph.numberOfContours>0
 assert glyph.compile(new['glyf'])==src['glyf'][source_name].compile(src['glyf'])
 assert new['hmtx'].metrics[name]==src['hmtx'].metrics[source_name]
 added.append(dict(codepoint=f'U+{cp:04X}',name=name,glyph_id=new.getGlyphID(name),outline_sha256=sha(glyph.compile(new['glyf'])),metrics=new['hmtx'].metrics[name]))
notice='Paintroid/src/main/assets/legal/fonts/anpaintnomui-NOTICE.txt'
assert (ROOT/notice).read_bytes()==baseline(notice)
assert b'MIT License' in (ROOT/notice).read_bytes() and b'SIL OPEN FONT LICENSE Version 1.1' in (ROOT/notice).read_bytes()
inventory='Paintroid/src/main/assets/fonts/inventory.json'
assert (ROOT/inventory).read_bytes().replace(sha(newraw).encode(),sha(oldraw).encode())==baseline(inventory)
(OUT/'baseline-m03.ttf').write_bytes(oldraw)
result=dict(status='PASS',baseline_tree=subprocess.check_output(['git','rev-parse',BASE+'^{tree}'],cwd=ROOT,text=True).strip(),baseline_font_sha256=sha(oldraw),source_font_sha256=sha(srcraw),current_font_sha256=sha(newraw),old_glyphs_preserved=len(oldorder),old_codepoints_preserved=len(old.getBestCmap()),cmap_subtables=cmap_report,additions=added,raw_global_tables_preserved=['OS/2','hhea','name','post'],licence_notice_unchanged_sha256=sha((ROOT/notice).read_bytes()),inventory_only_font_hash_changed=True)
(OUT/'font-independent-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
