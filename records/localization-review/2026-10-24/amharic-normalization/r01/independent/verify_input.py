import json,hashlib,pathlib,xml.etree.ElementTree as ET
p=pathlib.Path('/workspace/scratch/bbca2890f602/amharic-normalization-draft-20261024')
out=pathlib.Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
seal='e89ed5d8ab634f777cabe9bac2c52ec3a2ea27332a13749772e555a9edd0c27a'
mb=(p/'MANIFEST.json').read_bytes();assert sha(mb)==seal
m=json.loads(mb)
file_checks=[{'path':f,'sha256':sha((p/f).read_bytes()),'matches':sha((p/f).read_bytes())==h} for f,h in m['files'].items()]
assert all(c['matches'] for c in file_checks)
bind=json.load(open(p/'source-bindings.json'));prov=json.load(open(p/'fresh-production-provenance.json'))
blob_checks=[]
for f,r in bind.items():
 b=(p/r['local_complete_copy']).read_bytes();h=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 blob_checks.append({'path':f,'computed_git_blob':h,'matches':h==r['git_blob'],'provenance_binding_matches':prov['paths'][f]==r})
assert all(c['matches'] and c['provenance_binding_matches'] for c in blob_checks)
record_checks=[]
for r in json.load(open(p/'lexical-evidence/exact-records.json')):
 if 'source_file' in r:
  t=(p/'lexical-evidence'/r['source_file']).read_text();s='\n'.join(t.splitlines()[r['start_line']-1:r['end_line']]);ok=s.strip()==r['raw_po_record'].strip() and r['raw_po_record'] in t
  record_checks.append({'id':r['id'],'record_and_lines_match':ok,'fuzzy':r['fuzzy'],'obsolete':r['obsolete']})
 else:
  sub=[]
  for lang in ('english_record','amharic_record'):
   rr=r[lang];ls=(p/'lexical-evidence'/rr['source_file']).read_text().splitlines();ok=rr['raw_xml_record'] in '\n'.join(ls[rr['start_line']-1:rr['end_line']]);sub.append(ok)
  record_checks.append({'id':r['id'],'record_and_lines_match':all(sub)})
assert len(record_checks)==27 and all(c['record_and_lines_match'] for c in record_checks)
snaps=json.load(open(p/'lexical-evidence/sources.json'));snapshot_checks=[]
for s in snaps:
 b=(p/'lexical-evidence'/s['file']).read_bytes();snapshot_checks.append({'path':s['file'],'sha256_matches':sha(b)==s['sha256'],'bytes_match':len(b)==s['bytes']})
assert len(snapshot_checks)==10 and all(c['sha256_matches'] and c['bytes_match'] for c in snapshot_checks)
en=ET.parse(p/'source/Paintroid/src/main/res/values/strings.xml').getroot();am=ET.parse(p/'source/Paintroid/src/main/res/values-b+am/strings.xml').getroot();enames={e.attrib['name']:e for e in en};anames={e.attrib['name'] for e in am}
keys=[]
for r in json.load(open(p/'lexical-evidence/draft-candidates.json')):
 k=r['key'].split('/')[1];e=enames[k];xml=f'<string name="{k}">"{r["draft"]}"</string>';parsed=ET.fromstring(xml)
 keys.append({'key':k,'source_text_matches':e.text==r['english'],'source_attributes_match':e.attrib==r['source_attributes'],'draft_xml_parses':parsed.text=='"'+r['draft']+'"','absent_in_production_am':k not in anames,'placeholders_or_units_added':False})
assert all(x['source_text_matches'] and x['source_attributes_match'] and x['draft_xml_parses'] and x['absent_in_production_am'] for x in keys)
report={'input_manifest_sha256':seal,'verified_manifest_files':len(file_checks),'file_checks':file_checks,'verified_source_git_blobs':len(blob_checks),'blob_checks':blob_checks,'verified_snapshots':len(snapshot_checks),'snapshot_checks':snapshot_checks,'verified_exact_records':len(record_checks),'record_checks':record_checks,'key_checks':keys,'coverage':{'canonical_translatable_resource_containers':sum(e.attrib.get('translatable')!='false' for e in en),'present_am':len(am),'missing_am':sum(e.attrib.get('translatable')!='false' and e.attrib['name'] not in anames for e in en)},'limits':['Static evidence verification only, not Android build or application tests.','Fresh production/tree retrieval is supplied dossier provenance, not independently repeated in this review.','No linguistic correctness follows automatically from hash, XML or record validation.']}
(out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('input_manifest_sha256','verified_manifest_files','verified_source_git_blobs','verified_snapshots','verified_exact_records','coverage')},indent=2))
