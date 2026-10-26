#!/usr/bin/env python3
"""Independent Git CLI / ElementTree check; imports neither validation helper."""
import argparse,collections,hashlib,json,re,subprocess
from pathlib import Path
import xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--tree-file',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
def require(x,m):
 if not x:raise ValueError(m)
def digest(b):return hashlib.sha256(b).hexdigest()
def readjson(p):return json.loads(p.read_bytes())
pin='ce796879f4568a27b9d905a8e8db639dd0a93a30';tree_sha='f7c5f2fca54eb06b4a0c55df25a0b80b2ac4c12c'
tree=readjson(a.tree_file);blobs=[x for x in tree['tree'] if x['type']=='blob'];require(tree['sha']==tree_sha and tree.get('truncated') is False and len(blobs)==1376,'tree inventory')
# git hash-object without -w is read-only and does not need a repository.
paths=''.join(str((a.source_root/x['path']).resolve())+'\n' for x in blobs)
result=subprocess.run(['git','hash-object','--stdin-paths'],input=paths,text=True,capture_output=True,check=True)
require(result.stdout.splitlines()==[x['sha'] for x in blobs],'independent Git CLI source identity')
source_raw={x['path']:(a.source_root/x['path']).read_bytes() for x in blobs}
production=[p for p in source_raw if '/src/main/' in p and Path(p).suffix in ('.kt','.java','.xml')];require(len(production)==322,'production inventory')
scope=readjson(a.packet/'scope-and-source-context.json');terms=readjson(a.packet/'terminology-foundations.json');require(scope['source_commit']==terms['source_commit']==pin,'pin')
require(digest((a.packet/'scope-and-source-context.json').read_bytes())=='8dd3dd99b633bbec8254639797ddc81000ce4d8bfa9c037503663123587399d5','scope identity')
require(digest((a.packet/'terminology-foundations.json').read_bytes())=='bc6217e58573463929f8f0ba84815db06b41da809af8365c96bb1b824a11829b','foundation identity')
def rows(raw):return {n.tag+'/'+n.attrib['name']:(''.join(n.itertext()),n.attrib) for n in ET.fromstring(raw)}
base=rows(source_raw['Paintroid/src/main/res/values/strings.xml']);p0=set(next(x['keys'] for x in json.loads(source_raw['translations/string-importance.json'])['tiers'] if x['id']=='P0'));require(len(p0)==92,'P0 denominator')
selected={x['identity'] for x in scope['entries']};held={x['identity'] for x in scope['held_entries']};require(len(selected)==55 and len(held)==5 and not selected&held,'scope partition')
windows=0
for entry in scope['entries']:
 require(base[entry['identity']]==(entry['source'],entry['attributes']),'English pair')
 for c in entry['consumer_contexts']:
  lines=source_raw[c['path']].decode().splitlines();require('\n'.join(lines[c['start_line']-1:c['end_line']])==c['text'],'window bytes');windows+=1
require(windows==98 and len(scope['source_bindings'])==22,'window/binding count')
for b in scope['source_bindings']:require(digest(source_raw[b['path']])==b['sha256'] and len(source_raw[b['path']])==b['bytes'],'source SHA-256')
counts={};formatted=[];empty=0;candidate_hashes={}
for tag in ('ca','ro'):
 actual=rows(source_raw[f'Paintroid/src/main/res/values-{tag}/strings.xml']);require(len(actual)==150 and len(p0&actual.keys())==32 and p0-actual.keys()==selected|held,'inherited/missing partition')
 for identity,x in terms['locales'][tag]['values'].items():require(actual[identity]==(x['value'],x['attributes']),'inherited full pair')
 values=[];groups={}
 for file in sorted(a.packet.glob(tag+'-*-candidates.json')):
  d=readjson(file);candidate_hashes[file.name]=digest(file.read_bytes());groups[d['group']]=len(d['candidates'])
  for x in d['candidates']:
   require(x['identity'] not in actual and x['current_target'] is None and x['absence_is_defect'] is False,'missing-only')
   require(base[x['identity']]==(x['source'],x['attributes']),'complete source pair')
   require(x['candidate_value_sha256_utf8']==digest(x['candidate_display_text'].encode()),'candidate hash')
   require(x['candidate_xml_text_sha256_utf8']==digest(x['candidate_xml_text'].encode()),'XML hash')
   if x['attributes'].get('formatted')=='false':formatted.append(tag+'/'+x['identity'])
   empty+=not x['author_uncertainties'];values.append(x['identity'])
 require(len(values)==len(set(values))==55 and set(values)==selected and groups=={2:28,3:16,4:11},'locale candidate grain')
 counts[tag]={'candidates':len(values),'inherited':len(actual),'P0_present':32,'P0_total':92,'held_absent':5,'groups':groups}
require(len(formatted)==2 and empty==85,'actual attribute/uncertainty inventories')
receipt={'schema_version':1,'source_commit':pin,'source_tree':tree_sha,'result':'passed','method':'Independent read-only git hash-object CLI and ElementTree; no import from either validator/test helper.','raw_git_blob_identities_verified':1376,'production_files_counted':322,'source_binding_sha256_verified':22,'consumer_windows_compared':98,'candidate_values_counted':110,'unique_candidate_identities':55,'per_locale':counts,'actual_formatted_false_locale_values':formatted,'explicit_empty_author_uncertainty_rows':empty,'candidate_sha256':candidate_hashes,'limitations':['No independent linguistic, native, device, layout or whole-locale acceptance.','The separate primary validator derives and checks the complete recursive Git tree and exercises mutation controls.','No source bytes modified; candidate packet is pending review, not implementation.']}
a.out.mkdir(parents=True,exist_ok=True);out=a.out/'independent-crosscheck.json';out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');print(digest(out.read_bytes()))
