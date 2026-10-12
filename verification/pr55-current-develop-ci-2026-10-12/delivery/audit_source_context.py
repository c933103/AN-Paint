#!/usr/bin/env python3
"""Read-only current-tree preflight and existing licence-reference observation."""
import argparse, hashlib, json, pathlib, subprocess
from audit_direction_delivery import TREE, HEAD, require, sha

PRIOR_TREE='d2379b932cc976bb5347515887ecdfc4729ee70d'
PREFIX='Paintroid/src/main/assets/'

def audit(repo,output):
    def git(*args): return subprocess.check_output(['git',*args],cwd=repo)
    def source(tree,path): return git('show',tree+':'+path)
    def leaves(tree):
        result={}
        for row in git('ls-tree','-rz',tree).split(b'\0'):
            if not row: continue
            meta,path=row.split(b'\t');mode,kind,digest=meta.decode().split()
            require(kind=='blob','unexpected non-blob')
            result[path.decode()]=(mode,digest)
        return result
    current=leaves(TREE);prior=leaves(PRIOR_TREE)
    require(len(current)==1094,'current leaf count changed')
    for path,(mode,digest) in current.items():
        local=repo/path;raw=local.read_bytes()
        require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==digest,'local blob mismatch: '+path)
        require(mode in ('100644','100755') and not local.is_symlink(),'unexpected mode: '+path)
        require(bool(local.stat().st_mode&0o111)==(mode=='100755'),'local executable mismatch: '+path)
    changed=set(p for p in current.keys()|prior.keys() if current.get(p)!=prior.get(p))
    unchanged_prefixes=('.github/workflows/','Paintroid/src/main/java/','Paintroid/src/main/assets/','gradle/')
    require(not any(p.startswith(unchanged_prefixes) for p in changed),'unexpected workflow/production code/font/wrapper change')
    for path in ('build.gradle','Paintroid/build.gradle','tools/verify_exact_script_generation.py'):
        require(path not in changed,'probe/build implementation changed: '+path)
    require(len(changed)==60,'integration path change count differs')
    summary={'status':'PASS','head_from_parent_receipt':HEAD,'tree':TREE,'prior_tree':PRIOR_TREE,'tracked_leaves':len(current),'all_local_bytes_and_executable_modes_exact':True,'changed_paths':sorted(changed),'workflow_production_java_assets_wrapper_build_probe_implementation_unchanged':True,'local_head':git('rev-parse','HEAD').decode().strip(),'note':'Exact tree object is the audit input. Local preparation commit differs from public head; remote head/merge identity comes from the coordinator receipt.'}
    (output/'source-preflight.json').write_text(json.dumps(summary,indent=2)+'\n')
    (output/'source-tree-diff.log').write_bytes(git('diff','--name-status',PRIOR_TREE,TREE))
    inventory=json.loads(source(TREE,PREFIX+'fonts/inventory.json'))
    missing=[row['licence_file'] for row in inventory if PREFIX+row['licence_file'] not in current]
    require(len(missing)==10,'existing licence-path issue count differs')
    require(all(PREFIX+p not in prior for p in missing),'licence path newly absent')
    bindings={}
    for path in ('fonts/inventory.json','legal/FONT_NOTICES.txt','legal/THIRD_PARTY_NOTICES.txt'):
        raw=source(TREE,PREFIX+path)
        require(raw==source(PRIOR_TREE,PREFIX+path),'inventory/aggregate changed: '+path)
        bindings[path]={'bytes':len(raw),'sha256':sha(raw),'unchanged_from_prior_tree':True}
    observation={'observation':'Ten individual licence_file references already do not resolve in the prior tree. Inventory and aggregate notices are unchanged; this is an existing metadata-reference issue, not evidence of missing aggregate notices or licence removal by this integration. Actual APK asset presence is checked separately.','current_tree':TREE,'prior_tree':PRIOR_TREE,'missing_notice_paths':missing,'all_already_absent_from_prior_tree':True,'inventory_and_aggregate_bindings':bindings,'limitation':'One-time contextual comparison only; not a normal CI gate or independent legal conclusion. Separate tracking is outside this audit.'}
    (output/'preexisting-inventory-observation.json').write_text(json.dumps(observation,indent=2)+'\n')
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output-directory',type=pathlib.Path,required=True);a=p.parse_args()
    audit(a.repo,a.output_directory)
    print('PASS: all 1,094 local bytes/modes match the exact tree; integration changes are recorded; ten stale licence paths remain pre-existing with unchanged aggregate notices.')
