#!/usr/bin/env python3
"""Independent F01 resource union, manifest identity and inventory accounting."""
from pathlib import Path
import collections, hashlib, json, re, subprocess, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
CAND=ROOT/'combined-candidate';EVID=ROOT/'combined-evidence';OUT=ROOT/'independent-review'
BASE='d9858229f98068bef9c6194c90d77610c5ecceec'
ELEVEN='89e43725c5b7c2f01827cfa06510c21f5268314c'
EXPANSION='b81391fb46dd9ee1bdb86c3faf693462e1316232'
COMBINED='bde13ca4bbd9a45198ab4da9cadd85d900aaa594'
KEY='formats22_tiff_description'
def git(where,*args):return subprocess.check_output(['git','-C',str(where),*args])
def listing(where,tree):
 result={}
 for row in git(where,'ls-tree','-rz',tree).split(b'\0'):
  if row:
   meta,p=row.split(b'\t',1);mode,kind,sha=meta.decode().split();assert kind=='blob'
   result[p.decode()]=(mode,sha)
 return result
def blob(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def source(where,sha):return git(where,'cat-file','blob',sha)
def descriptions(data):return [''.join(n.itertext()) for n in ET.fromstring(data).findall(f"./string[@name='{KEY}']")]
def tag_for(folder):
 if folder=='values':return 'default'
 if folder.startswith('values-b+'):return folder[len('values-b+'):].replace('+','-')
 raw=folder[len('values-'):]
 raw=re.sub(r'-r([A-Z]{2}|[0-9]{3})',r'-\1',raw)
 return {'in':'id','iw':'he'}.get(raw,raw)
base=listing(CAND,BASE);combined=listing(CAND,COMBINED)
eleven=listing(ROOT/'candidate',ELEVEN)
expansion=listing(ROOT/'expansion-candidate',EXPANSION)
manifest=json.loads((EVID/'candidate-manifest.json').read_text())
inv=json.loads((EVID/'all-language-inventory.json').read_text())
oldinv=json.loads((ROOT/'evidence/all-language-inventory.json').read_text())
proposals=json.loads((ROOT/'evidence/linguistic-proposals-26.json').read_text())
changed={p for p in base if p in combined and base[p]!=combined[p]}
added=set(combined)-set(base);removed=set(base)-set(combined)
assert len(combined)==1294 and len(base)==1290
assert len(changed)==37 and len(added)==4 and not removed
assert changed=={p for p in base if base[p]!=eleven[p]}|{p for p in base if base[p]!=expansion[p]}
changed11={p for p in base if base[p]!=eleven[p]};changed26={p for p in base if base[p]!=expansion[p]}
assert len(changed11)==11 and len(changed26)==26 and not(changed11&changed26)
for p in changed11:assert combined[p]==eleven[p]
for p in changed26:assert combined[p]==expansion[p]
assert all(p.endswith('.xml') and '/res/values' in p for p in changed)
assert all(p.startswith('tools/test_') or p.startswith('Paintroid/src/test/') for p in added)
assert manifest['candidate_tree']==inv['candidate_tree']==COMBINED
assert manifest['initial_eleven_tree']==inv['initial_eleven_tree']==ELEVEN
assert manifest['isolated_26_tree']==inv['isolated_26_tree']==EXPANSION
assert manifest['source_files']==1294 and manifest['changed_resources']==37 and manifest['added_test_files']==4
assert manifest['unchanged_base_files']==1253 and manifest['removed']==[]
assert {e['path'] for e in manifest['changes']}==changed|added
for p,(mode,sha) in combined.items():
 f=CAND/p;assert blob(f.read_bytes())==sha,p
 assert ('100755' if f.stat().st_mode&0o111 else '100644')==mode,p
for e in manifest['changes']:
 p=e['path'];data=(CAND/p).read_bytes()
 assert e['base_blob']==(base[p][1] if p in base else None)
 assert e['candidate_blob']==combined[p][1]
 assert e['sha256']==hashlib.sha256(data).hexdigest() and e['bytes']==len(data)
# Independently enumerate the key from every main values* XML, including defaults and unoffered catalogues.
actual={};catalogues={}
for f in sorted((CAND/'Paintroid/src/main/res').glob('values*/*.xml')):
 p=str(f.relative_to(CAND));nodes=descriptions(f.read_bytes())
 if f.name=='strings.xml':catalogues[tag_for(f.parent.name)]=p
 if nodes:
  assert len(nodes)==1
  actual[p]={'tag':tag_for(f.parent.name),'text':nodes[0]}
assert len(actual)==60
explicit=inv['explicit'];assert len(explicit)==60
assert len({e['id'] for e in explicit})==60
assert len({e['tag'] for e in explicit})==60
assert {e['path'] for e in explicit}==set(actual)
old_by_path={e['path']:e for e in oldinv['explicit']}
entry_results=[]
for e in explicit:
 p=e['path'];b=source(CAND,base[p][1]);c=(CAND/p).read_bytes()
 assert e['tag']==actual[p]['tag']
 assert e['base_blob']==base[p][1]
 assert descriptions(b)==[e['base_text']]
 assert actual[p]['text']==e['candidate_text']
 assert e['line']==b[:b.index(e['base_text'].encode())].count(b'\n')+1
 for k in ('id','tag','path','line','base_blob','base_text','category','assessment','closure'):
  assert e[k]==old_by_path[p][k],(e['tag'],k)
 assert e['closure']=='Not closed'
 if p in changed:
  assert e['category']=='unqualified-high'
  assert b.replace(e['base_text'].encode(),e['candidate_text'].encode(),1)==c
  assert b.count(e['base_text'].encode())==1
 else:
  assert b==c and e['base_text']==e['candidate_text']
 entry_results.append({'id':e['id'],'tag':e['tag'],'path':p,'base_category':e['category'],
  'candidate_changed':p in changed,'base_and_candidate_text_match':True,'other_bytes_identical':True,
  'closure_unchanged':True})
for e in proposals['entries']:
 assert actual[e['resource_path']]['text']==e['proposal']
# Every offered tag receives exactly one explicit or fallback record; fallback remains source-only inference.
offered=[n.text for n in ET.parse(CAND/'Paintroid/src/main/res/values/app_language_tags.xml').findall("./string-array[@name='app_language_tags']/item")]
assert len(offered)==len(set(offered))==140
offered=set(offered);present={e['tag'] for e in explicit if e['tag'] in offered}
fallback=inv['fallback'];assert len(fallback)==81
assert len({e['id'] for e in fallback})==81
assert {e['tag'] for e in fallback}==offered-present
assert len(present)==59
assert inv['fallback']==oldinv['fallback']
for e in fallback:
 assert e['path']==catalogues[e['tag']]
 assert e['path'] not in actual
 assert not descriptions((CAND/e['path']).read_bytes())
 assert not e['key_present'] and not e['same_language_alternative_present']
 assert all(t.split('-')[0]!=e['tag'].split('-')[0] for t in present)
legacy={tag for tag,p in catalogues.items() if tag!='default' and tag not in offered and p not in actual}
assert legacy==set(inv['legacy_unoffered_missing'])=={'es','ko'}
counts=collections.Counter(e['category'] for e in explicit)
assert counts=={'unqualified-high':37,'unqualified-or-reductive-probable':12,'capability-qualified':7,'linguistically-uncertain':4}
expected_counts={'explicit':60,'offered_explicit':59,'offered_total':140,'unqualified_high':37,
 'unqualified_probable':12,'qualified':7,'uncertain':4,'no_claim_confident':0,'candidate_entries':37,
 'fallback_offered':81,'unchanged_probable':12,'unchanged_uncertain':4,'unchanged_already_qualified':7}
assert inv['counts']==expected_counts
assert inv['parent_state']['total']==475 and inv['parent_state']['structural_complete']==3 and inv['parent_state']['pending']==472
# The entire pre-existing record is byte-identical to base; no row closure was written in source.
assert all(combined[p]==base[p] for p in base if p.startswith('verification/'))
report={'review_scope':'Combined F01 resource-union equivalence and inventory bookkeeping only.',
 'result':'pass','base_tree':BASE,'initial_eleven_tree':ELEVEN,'isolated_26_tree':EXPANSION,'candidate_tree':COMBINED,
 'candidate_manifest_sha256':hashlib.sha256((EVID/'candidate-manifest.json').read_bytes()).hexdigest(),
 'inventory_sha256':hashlib.sha256((EVID/'all-language-inventory.json').read_bytes()).hexdigest(),
 'source_files':1294,'unchanged_base_files':1253,'changed_existing_resources':37,'added_test_files':4,
 'removed':[],'counts':expected_counts,'parent_state':inv['parent_state'],
 'checks':['37 resource changes are the disjoint exact blob union of revised 11-entry and isolated 26-entry candidates.',
 'All 1,294 combined source bytes/modes match the frozen Git tree; all 41 manifest entries match blob/SHA-256/length.',
 'Every explicit base/current string, base blob, line, tag and inherited classification agrees with source; no resource bytes outside the one value changed.',
 'All 37 originally high-confidence unqualified descriptions receive modal edits; 12 probable, 4 uncertain and 7 already-qualified entries stay byte-identical.',
 '140 unique offered tags partition into 59 explicit and 81 missing definitions, plus default gives 60 explicit records.',
 'Each fallback entry still lacks the key and a same-language explicit definition; legacy unoffered es and ko also remain missing.',
 'All existing verification files remain byte-identical; 475/3/472 is preserved and every explicit item remains Not closed.'],
 'limits':['Category counts describe the base-text classification, not remaining categorical assertions in the corrected candidate.',
 'No native-speaker/full-locale acceptance or fresh review of the 12 probable/4 uncertain/7 qualified entries.',
 'Fallback remains source-predicted; no runtime proof for 81 locales.',
 'No host tests, test adequacy review, Kotlin compilation, Android runtime or rendered acceptance performed in this bounded role.',
 'Git tree objects and local bytes were verified; no remote fetch/publication/dispatch occurred.'],
 'entries':entry_results}
out=OUT/'combined-inventory-review.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('entries','checks','limits')},ensure_ascii=False,indent=2))
print('Review SHA-256:',hashlib.sha256(out.read_bytes()).hexdigest())
