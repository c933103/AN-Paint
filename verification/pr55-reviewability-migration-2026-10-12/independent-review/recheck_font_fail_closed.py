#!/usr/bin/env python3
"""Independent in-memory recheck of the original review gaps; no source writes."""
import argparse,copy,hashlib,json,pathlib,re,struct,sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
sys.dont_write_bytecode=True;sys.path.insert(0,str(a.repo/'tools'))
from current_font_contract import errors,load
from test_locale_font_coverage import mapped_codepoints
fixture=json.loads((a.repo/'tools/fixtures/current_localization/nom_current_font_contract.json').read_text())
font,inventory,assets=load(a.repo,fixture)
def check(ok,why):
 if not ok:raise ValueError(why)
def table(data,name):
 for i in range(struct.unpack_from('>H',data,4)[0]):
  at=12+16*i;tag,_,off,size=struct.unpack_from('>4sIII',data,at)
  if tag.decode()==name:return off,size,at
 raise ValueError(name)
def subtables(data):
 off,_,_=table(data,'cmap')
 for i in range(struct.unpack_from('>H',data,off+2)[0]):
  plat,enc,rel=struct.unpack_from('>HHI',data,off+4+8*i);base=off+rel
  yield struct.unpack_from('>H',data,base)[0],base
def checksum(data):
 d=bytes(data)+b'\0'*(-len(data)%4)
 return sum(struct.unpack('>'+'I'*(len(d)//4),d))&0xffffffff
def corrected(data):
 head,_,_=table(data,'head');struct.pack_into('>I',data,head+8,0)
 for i in range(struct.unpack_from('>H',data,4)[0]):
  at=12+16*i;_,_,off,size=struct.unpack_from('>4sIII',data,at)
  struct.pack_into('>I',data,at+4,checksum(data[off:off+size]))
 struct.pack_into('>I',data,head+8,(0xb1b0afba-checksum(data))&0xffffffff)
 check(checksum(data)==0xb1b0afba,'mutant checksum')
 inv=copy.deepcopy(inventory);next(r for r in inv if r['id']==fixture['inventory_id'])['sha256']=hashlib.sha256(data).hexdigest()
 return bytes(data),inv
rows=[]
for kind in ('zero-format4-length','nonexistent-supplementary-glyph'):
 data=bytearray(font)
 if kind=='zero-format4-length':
  base=next(base for fmt,base in subtables(data) if fmt==4);struct.pack_into('>H',data,base+2,0)
 else:
  for fmt,base in subtables(data):
   if fmt!=12:continue
   for i in range(struct.unpack_from('>I',data,base+12)[0]):
    at=base+16+12*i;lo,hi,gid=struct.unpack_from('>III',data,at)
    if lo<=0x2e7b6<=hi:
     check(lo==hi==0x2e7b6,'isolated supplementary test point');struct.pack_into('>I',data,at+8,65535)
 data,inv=corrected(data);found=errors(data,inv,assets,fixture);check(bool(found),'font contract accepted '+kind)
 class FontBytes:
  def read_bytes(self):return data
 try:mapped_codepoints(FontBytes())
 except AssertionError as exc:coverage=str(exc)
 else:raise ValueError('coverage accepted '+kind)
 rows.append({'mutation':kind,'contract_errors':found,'coverage_rejection':coverage,'checksums_and_inventory_corrected':True})
for kind in ('unrelated-source-notices','all-ofl-permission-and-conditions-removed'):
 changed=assets.copy()
 if kind=='unrelated-source-notices':
  for path in fixture['distribution']['source_notices']:changed[path]=b'removed\n'
 else:
  changed={path:re.sub(r'PERMISSION & CONDITIONS.*?(?=TERMINATION)','',data.decode(),flags=re.S).encode() for path,data in changed.items()}
 found=errors(font,inventory,changed,fixture);check(bool(found),'licence contract accepted '+kind)
 rows.append({'mutation':kind,'contract_errors':found})
check(errors(font,inventory,assets,fixture)==[],'unmodified font rejected')
result={'status':'PASS','scope':'Four originally accepted malformed-font/licence cases now rejected in memory; original font passes. No product files changed.','cases':rows}
a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print('PASS: original plus four non-vacuous fail-closed cases')
