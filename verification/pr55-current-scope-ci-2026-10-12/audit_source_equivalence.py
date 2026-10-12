#!/usr/bin/env python3
"""One-time docs-successor input equivalence and current identity derivation."""
import argparse,hashlib,json,pathlib,subprocess,sys
import audit_platform_artifacts as audit
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--previous-repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
OLD='dc1ba97dacc573ead73729297eb739ecb244dcf5';NEW=audit.TREE
DOCS={'AGENTS.md','README.md','TRANSLATING.md'}
def tree(repo,ref):
 out={}
 for row in subprocess.check_output(['git','ls-tree','-rz',ref],cwd=repo).split(b'\0'):
  if not row:continue
  meta,path=row.split(b'\t',1);mode,kind,oid=meta.decode().split();out[path.decode()]={'mode':mode,'kind':kind,'git_oid':oid}
 return out
old=tree(a.previous_repo,OLD);new=tree(a.repo,NEW)
if old.keys()!=new.keys():raise ValueError('path inventory changed')
changed=sorted(k for k in old if old[k]!=new[k]);audit.require(set(changed)==DOCS,'unexpected input delta')
for k in new:
 b=subprocess.check_output(['git','show',NEW+':'+k],cwd=a.repo)
 audit.require((a.repo/k).read_bytes()==b,'working file differs from source '+k)
sys.path.insert(0,str(a.repo/'tools'));inventory=audit.current_inventory(a.repo)
rows=[]
for k in changed:
 b=subprocess.check_output(['git','show',OLD+':'+k],cwd=a.previous_repo);n=(a.repo/k).read_bytes()
 rows.append({'path':k,'previous':old[k],'current':new[k],'previous_sha256':hashlib.sha256(b).hexdigest(),'current_sha256':hashlib.sha256(n).hexdigest()})
r={'status':'PASS','prior_runtime_head':'e19c766eb3eaedc1b3cd3657bb92864f81a9498a','prior_tree':OLD,'current_head':audit.HEAD,'current_tree':NEW,'run':audit.RUN,'total_leaves':len(new),'unchanged_leaves_and_modes':len(new)-len(changed),'changed_docs':rows,'runtime_test_resource_workflow_font_inputs':'BYTE_AND_MODE_IDENTICAL','current_jvm_expanded_identities':len(inventory['expected']),'jvm_identity_sha256':hashlib.sha256(json.dumps(inventory['expected'],sort_keys=True).encode()).hexdigest(),'limits':['Per-run source binding, not a permanent snapshot gate.','Bundled source includes all three changed Markdown files; old APK/source proof remains attributed to e19.','No new local Android or application-test execution.']}
a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
