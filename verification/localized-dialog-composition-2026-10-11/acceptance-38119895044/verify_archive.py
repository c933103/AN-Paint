#!/usr/bin/env python3
"""Verify deterministic parts, all member bytes and bounded fresh XML/export inventory.
No network, source mutation, APK provenance re-derivation or pixel interpretation.
"""
import argparse,collections,hashlib,io,json,stat,zipfile
from pathlib import Path,PurePosixPath
import xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--extract',type=Path);a=p.parse_args()
def require(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
meta=json.loads((a.directory/'archive.json').read_text());manifest=json.loads((a.directory/'members.json').read_text())['members']
parts=[]
for i,r in enumerate(meta['parts'],1):
 require(r['path']==f'composition-acceptance.zip.part{i:03d}','Part order/name')
 b=(a.directory/r['path']).read_bytes();require(len(b)==r['bytes']<=50000 and sha(b)==r['sha256'],'Part digest/size');parts.append(b)
b=b''.join(parts);require(len(b)==meta['archive']['bytes'] and sha(b)==meta['archive']['sha256'],'Archive digest/size')
z=zipfile.ZipFile(io.BytesIO(b));names=z.namelist();expected={r['path']:r for r in manifest}
require(len(names)==len(set(names))==meta['members']==len(manifest) and set(names)==set(expected),'Exact member inventory')
for info in z.infolist():
 name=PurePosixPath(info.filename);mode=info.external_attr>>16
 require(not name.is_absolute() and '..' not in name.parts and not stat.S_ISLNK(mode) and not info.is_dir(),'Unsafe member')
 require(info.date_time==(1980,1,1,0,0,0),'Deterministic member date')
 data=z.read(info);r=expected[info.filename]
 require(len(data)==r['bytes'] and sha(data)==r['sha256'],'Member digest/size: '+info.filename)
held=meta['held_historical_object_check']['sha256'];require(not any(r['sha256']==held for r in manifest+meta['parts']),'Excluded historical object')
xmls=[n for n in names if n.startswith('regression/') and '/test-results/' in n and n.endswith('.xml')]
ids=[]
for n in xmls:
 root=ET.fromstring(z.read(n));require(not any(root.findall('.//'+t) for t in ('failure','error','skipped')),'Failed/skipped JVM XML')
 ids += [(r.attrib['classname'],r.attrib['name']) for r in root.findall('.//testcase')]
wanted={tuple(r) for r in json.loads(z.read('receipts/expected-jvm-identities.json'))['expected']}
require(len(xmls)==90 and len(ids)==len(set(ids))==853 and set(ids)==wanted,'Exact 853 JVM identities')
installed_xml=[n for n in names if n.startswith('emulator/') and '/TEST-' in n and n.endswith('.xml')]
installed=[]
for n in installed_xml:
 root=ET.fromstring(z.read(n));require(not any(root.findall('.//'+t) for t in ('failure','error','skipped')),'Failed/skipped installed XML')
 installed.extend((r.attrib['classname'],r.attrib['name']) for r in root.findall('.//testcase'))
require(len(installed_xml)==8 and len(installed)==len(set(installed))==104,'Exact 104 installed XML identities')
exports=[n for n in names if n.startswith('emulator/dialog-export/')];require(len(exports)==5,'Five native exports')
replay=json.loads(z.read('receipts/dialog-replay.json'));png=0
for c in replay['cases']:
 data=z.read('emulator/dialog-export/'+c['method']+'.zip');require(len(data)==c['zip_bytes'] and sha(data)==c['zip_sha256'],'Export digest')
 inner=zipfile.ZipFile(io.BytesIO(data));rows={r['path']:r for r in c['files']};require(len(inner.namelist())==len(set(inner.namelist())) and set(inner.namelist())==set(rows)|{'manifest.json'},'Export exact members');require(json.loads(inner.read('manifest.json'))['files']==c['files'],'Export manifest records')
 for n,r in rows.items():
  data=inner.read(n);require(len(data)==r['bytes'] and sha(data)==r['sha256'],'Export member digest');png+=n.endswith('.png')
require(png==10,'Ten installed PNG originals')
require(sum(n.startswith('scoped-originals/') for n in names)==126,'C05/M02 original count')
require(sum(n.startswith('localized-dialog-layout/') for n in names)==42,'Changed HU model original count')
if a.extract:
 require(not a.extract.exists(),'Extraction target must be new')
 a.extract.mkdir(parents=True)
 for n in names:
  target=a.extract/n;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(n))
print(json.dumps(dict(success=True,archive_sha256=sha(b),members=len(names),parts=len(parts),jvm_suites=90,jvm=853,installed_phases=8,installed=104,installed_exports=5,installed_png=10,scoped_originals=126,changed_hu_model_originals=42,held_historical_object_matches=0),indent=2))
