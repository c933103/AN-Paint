#!/usr/bin/env python3
"""Explicit test-only correction rebind; never silently accept a moving branch."""
from pathlib import Path
import argparse,json,hashlib,re
from coverage_common import read,require,verify_tree,git,sha
ROOT=Path(__file__).resolve().parent
OLD_HEAD='d8312ccd9907b90746731efb68a290489f29afbc'
OLD_TREE='813e0b88a5de6c2de110c41688c63168216c1315'
BASE='e1e5433e63d45f5b76d39ce1a31ffc11fd7cd79d'
BASE_TREE='98b89d126533df3c0dbaeb729c74e4bcb44a3a8a'
ALLOWED={'Paintroid/src/test/java/org/catrobat/paintroid/local/NumericDisplayLocaleTest.kt','tools/test_serbian_p0_wording.py'}

def run(a):
 require(re.fullmatch('[0-9a-f]{40}',a.head) and re.fullmatch('[0-9a-f]{40}',a.tree),'exact immutable head/tree required')
 require(a.head!=OLD_HEAD and a.tree!=OLD_TREE,'correction must be a distinct source head/tree')
 state=read(a.publication_state);require(state['head']==a.head and state['tree']==a.tree and state['pr']==180 and state['source_base']==BASE,'verified publication identity')
 original=ROOT.parent/'coverage-original-head-d8312ccd';hm=read(original/'historical-manifest.json')
 require(hm['head']==OLD_HEAD and hm['tree']==OLD_TREE,'historical identity')
 for e in hm['files']:
  p=Path(e['path']);require(not p.is_absolute() and '..' not in p.parts,'safe historical path');b=(original/p).read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'historical preview changed')
 old=verify_tree(read(original/'inputs/source-head-tree.json'),OLD_TREE);newraw=a.tree_file.read_bytes();nt=json.loads(newraw);new=verify_tree(nt,a.tree)
 require(set(old)<=set(new),'test-only correction must not remove tracked files')
 delta={p for p in new if p not in old or any(new[p][k]!=old[p][k] for k in ('sha','mode','type'))}
 require(bool(delta) and delta<=ALLOWED,'correction exceeds reviewed two-test-path scope')
 for p,e in new.items():
  f=a.source_root/p;b=f.read_bytes();require(git(b)==e['sha'],'new source bytes: '+p);require(('100755' if f.stat().st_mode&0o111 else '100644')==e['mode'],'new source mode: '+p)
 base=verify_tree(read(ROOT/'inputs/base-source-tree.json'),BASE_TREE)
 changed=[p for p,e in new.items() if p not in base or any(e[k]!=base[p][k] for k in ('sha','mode','type'))]
 require({p for p in changed if '/src/main/' in p}=={'Paintroid/src/main/res/values-b+sr+Cyrl/strings.xml','Paintroid/src/main/res/values-b+sr+Latn/strings.xml'},'production delta boundary')
 identity=read(ROOT/'inputs/identity.json');require(identity['reviewed_head']==OLD_HEAD and identity['reviewed_tree']==OLD_TREE,'rebind only once from original head')
 identity.update(reviewed_head=a.head,reviewed_tree=a.tree,original_head=OLD_HEAD,original_tree=OLD_TREE,correction_scope=sorted(delta),correction_kind='test-only missing Serbian numeric-caption expectations; production strings and reviews unchanged')
 p=ROOT/'recompute_coverage.py';s=p.read_text();require(s.count("HEAD='"+OLD_HEAD+"';TREE='"+OLD_TREE+"'")==1,'frozen script identity')
 s=s.replace("HEAD='"+OLD_HEAD+"';TREE='"+OLD_TREE+"'","HEAD='"+a.head+"';TREE='"+a.tree+"'")
 s=s.replace('len(head)==1385 and len(old)==1382',f'len(head)=={len(new)} and len(old)==1382')
 s=s.replace('len(changes)==16 and len(set(head)-set(old))==3',f'len(changes)=={len(changed)} and len(set(head)-set(old))=={len(set(new)-set(base))}')
 s=s.replace('selected78','selected74').replace('missing-only78','missing-only74')
 # Validate everything before any current-preview input is changed.
 (ROOT/'inputs/source-head-tree.json').write_bytes(newraw)
 (ROOT/'inputs/identity.json').write_text(json.dumps(identity,indent=2)+'\n')
 p.write_text(s)
 result={'source_head':a.head,'source_tree':a.tree,'source_files':len(new),'base_source_files':len(base),'base_delta_files':len(changed),'test_only_correction_paths':sorted(delta),'original_preview_preserved':True,'production_and_linguistic_values_changed':False,'fresh_preview_still_required':True}
 (ROOT/'rebind-receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--head',required=True);p.add_argument('--tree',required=True);p.add_argument('--tree-file',type=Path,required=True);p.add_argument('--source-root',type=Path,required=True);p.add_argument('--publication-state',type=Path,required=True);run(p.parse_args())
