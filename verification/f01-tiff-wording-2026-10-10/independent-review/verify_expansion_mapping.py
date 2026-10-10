#!/usr/bin/env python3
"""Independent, read-only F01 expansion scope and proposal equivalence check."""
import collections, hashlib, json, re, subprocess, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CAND=ROOT/'expansion-candidate'
EVID=ROOT/'evidence'
BASE='d9858229f98068bef9c6194c90d77610c5ecceec'
TREE='b81391fb46dd9ee1bdb86c3faf693462e1316232'
KEY='formats22_tiff_description'
EXPECTED_MAP='632a49918015f150d2514e9d146f10e2c11aae9a8de81edc1ee13d518603a5d6'
def git(*args): return subprocess.check_output(['git','-C',str(CAND),*args])
def listing(tree):
    out={}
    for raw in git('ls-tree','-rz',tree).split(b'\0'):
        if not raw: continue
        meta,path=raw.split(b'\t',1); mode,kind,sha=meta.decode().split()
        assert kind=='blob'
        out[path.decode()]=(mode,sha)
    return out
def blob_sha(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def xml_value(data):
    nodes=ET.fromstring(data).findall(f"./string[@name='{KEY}']")
    assert len(nodes)==1
    return ''.join(nodes[0].itertext())
def han(text):return ''.join(c for c in text if '\u3400'<=c<='\u9fff' or '\uf900'<=c<='\ufaff')
map_bytes=(EVID/'linguistic-proposals-26.json').read_bytes()
assert hashlib.sha256(map_bytes).hexdigest()==EXPECTED_MAP
proposals=json.loads(map_bytes)
entries=proposals['entries']
assert len(entries)==26
assert len({e['locale'] for e in entries})==26
assert len({e['resource_path'] for e in entries})==26
base=listing(BASE);candidate=listing(TREE)
assert len(base)==len(candidate)==1290
assert base.keys()==candidate.keys()
changed={p for p in base if base[p]!=candidate[p]}
assert changed=={e['resource_path'] for e in entries}
base_manifest=json.loads((ROOT/'base-manifest.json').read_text())
assert base=={e['path']:(e['mode'],e['sha']) for e in base_manifest['files']}
exp_manifest=json.loads((EVID/'expansion-manifest.json').read_text())
assert exp_manifest['candidate_tree']==TREE
assert exp_manifest['linguistic_map_sha256']==EXPECTED_MAP
assert exp_manifest['changed_existing']==26 and exp_manifest['new_files']==0 and exp_manifest['removed']==[]
assert {e['path'] for e in exp_manifest['changes']}==changed
for p,(mode,sha) in candidate.items():
    f=CAND/p
    assert f.is_file(),p
    assert blob_sha(f.read_bytes())==sha,p
    assert ('100755' if f.stat().st_mode & 0o111 else '100644')==mode,p
for e in exp_manifest['changes']:
    data=(CAND/e['path']).read_bytes()
    assert e['candidate_blob']==candidate[e['path']][1]
    assert e['sha256']==hashlib.sha256(data).hexdigest()
results=[]
for e in entries:
    p=e['resource_path'];orig=git('cat-file','blob',base[p][1]);new=(CAND/p).read_bytes()
    assert Path(p).parent.name==e['qualifier']
    assert e['resource_key']==KEY
    assert xml_value(orig)==e['original'],e['locale']
    assert xml_value(new)==e['proposal'],e['locale']
    oldpart=e['replacement']['original'];newpart=e['replacement']['proposal']
    assert e['original'].count(oldpart)==1
    assert e['original'].replace(oldpart,newpart,1)==e['proposal']
    # Full-file equivalence is stronger than XML-tree equivalence: no encoding,
    # whitespace, comments, newline, qualifiers or other resource changes.
    oldvalue=e['original'].encode();newvalue=e['proposal'].encode()
    assert orig.count(oldvalue)==1
    assert orig.replace(oldvalue,newvalue,1)==new,e['locale']
    assert base[p][0]==candidate[p][0]
    assert han(e['original'])==han(e['proposal'])
    assert e['original'].count('RGB')==e['proposal'].count('RGB')==1
    assert e['original'].count('TIFF')==e['proposal'].count('TIFF')==1
    line=orig[:orig.index(oldvalue)].count(b'\n')+1
    assert line==e['source_line']
    results.append({'locale':e['locale'],'path':p,'base_blob':base[p][1],
        'candidate_blob':candidate[p][1],'sha256':hashlib.sha256(new).hexdigest(),
        'original_matches_base':True,'proposal_matches_candidate':True,
        'replacement_map_exact':True,'other_file_bytes_identical':True,
        'resource_qualifier_unchanged':True,'existing_han_characters_preserved':True,
        'original':e['original'],'proposal':e['proposal'],
        'replacement':e['replacement'],'result':'pass'})
report={'review_scope':'Only independent 26-language proposal equivalence and byte-scope validation; no source or test modification, no tests executed, no publication.',
 'base_tree':BASE,'isolated_tree':TREE,'proposal_map_sha256':EXPECTED_MAP,
 'result':'pass','base_files':len(base),'candidate_files':len(candidate),'changed_files':len(changed),
 'unchanged_files':len(base)-len(changed),'added':[],'removed':[],
 'checks':['Every base-manifest path/mode/blob agrees with base tree.',
 'Every candidate file byte hash and executable mode agrees with isolated tree.',
 'Exactly 26 existing resource files change and each equals one exact reviewed value replacement.',
 'Every proposal applies exactly its declared original-to-modal substitution.',
 'Every original agrees with the exact base blob and source line.',
 'All per-file candidate blob and SHA-256 manifest identities agree.',
 'Hanja/Han text, locale qualifier, RGB and TIFF tokens remain preserved.'],
 'limits':['Model reading of narrow modal changes, not native-speaker attestation or full-locale acceptance.',
 'No independent re-fetch of linguistic source citations or remote GitHub tree; local tree objects and source bytes were verified.',
 'Android compilation, resource resolution, runtime/rendered behavior and test adequacy belong to primary reviewer.',
 'Combined candidate and final inventory pending separate bookkeeping review.'],
 'entries':results}
out=ROOT/'independent-review/expansion-map-review.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('entries','checks','limits')},indent=2))
print('Review evidence SHA-256:',hashlib.sha256(out.read_bytes()).hexdigest())
