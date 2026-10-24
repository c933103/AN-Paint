#!/usr/bin/env python3
"""Read-only checksum, resource and exact-record audit. Not an app test."""
import collections, hashlib, json, re, sys, xml.etree.ElementTree as ET
from pathlib import Path
p=Path(sys.argv[1])
expected='c907b7a1ce4cae2896437e8b3092eff4f789978552ac2e4f27b28f304f91e9b5'
manifest_data=(p/'MANIFEST.json').read_bytes();manifest=json.loads(manifest_data)
assert hashlib.sha256(manifest_data).hexdigest()==expected
assert len(manifest['files'])==40
for name,digest in manifest['files'].items(): assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest,name
bindings=json.loads((p/'source-bindings.json').read_text())
assert len(bindings)==20
for name,x in bindings.items():
 d=(p/x['local_complete_copy']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()==x['git_blob'],name
 assert hashlib.sha256(d).hexdigest()==x['sha256'],name
records=json.loads((p/'lexical-evidence/exact-records.json').read_text())
assert len(records)==32
for x in records:
 if 'raw_block' in x:
  lines=(p/'lexical-evidence'/x['file']).read_text().splitlines();s='\n'.join(lines[x['line_start']-1:x['line_end']])
  assert s==x['raw_block'],x['id']
  assert x['fuzzy']==bool(re.search(r'^#,.*\bfuzzy\b',s,re.M)),x['id']
 else:
  for lang,y in x['pair'].items(): assert (p/'lexical-evidence'/y['file']).read_text().splitlines()[y['line']-1]==y['raw_line'],x['id']
keys=['ui_save','ui_save_a5d0d9','save20_title','save20_file_name','save20_file_format'];occ=[]
for f in (p/'source').rglob('*.kt'):
 for i,l in enumerate(f.read_text().splitlines(),1):
  for m in re.finditer(r'R\.string\.('+'|'.join(sorted(keys,key=len,reverse=True))+r')\b',l):occ.append({'key':m[1],'path':str(f.relative_to(p/'source')),'line':i,'source_line':l})
norm=lambda rows:sorted(json.dumps(x,sort_keys=True,ensure_ascii=False) for x in rows)
assert norm(occ)==norm(json.loads((p/'direct-consumer-occurrences.json').read_text())['occurrences'])
e=ET.parse(p/'source/Paintroid/src/main/res/values/strings.xml').getroot();a=ET.parse(p/'source/Paintroid/src/main/res/values-b+am/strings.xml').getroot()
en={x.attrib['name'] for x in e if x.attrib.get('translatable')!='false'};am={x.attrib['name'] for x in a}
assert len(en)==717 and len(en&am)==12 and len(en-am)==705
assert not set(keys)&am
print(json.dumps({'input_manifest_sha256':expected,'manifest_files_verified':40,'source_git_blobs_verified':20,'primary_snapshots':7,'exact_records_verified':32,'bounded_direct_occurrences':len(occ),'bounded_direct_files':len({x['path'] for x in occ}),'direct_count_by_key':dict(collections.Counter(x['key'] for x in occ)),'translatable_containers':717,'present':12,'missing':705,'all_five_absent_from_production':True,'source_xml_elements':len(e),'excluded_nontranslatable_containers':len(e)-len(en),'result':'PASS','limits':'Snapshot-only read-only audit. Not a new remote head check, exhaustive repository search, app build or runtime test.'},ensure_ascii=False,indent=2))
