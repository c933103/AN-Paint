#!/usr/bin/env python3
"""One-time exact current-tree preflight and existing licence-reference observation."""
import argparse, hashlib, json, pathlib, subprocess
from audit_direction_delivery import TREE, HEAD, require, sha

PRIOR_TREE='ab6f5497e147e81d4c50f4954ea87f364be087aa'
CHANGED={
 'Paintroid/src/test/java/org/catrobat/paintroid/local/LocalizedDialogLayoutTest.kt',
 'Paintroid/src/test/java/org/catrobat/paintroid/local/UiDirectionContextTest.kt',
}
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
    require(len(current)==1062,'current leaf count changed')
    for path,(mode,digest) in current.items():
        local=repo/path;raw=local.read_bytes()
        require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==digest,'local blob mismatch: '+path)
        require(mode in ('100644','100755') and not local.is_symlink(),'unexpected mode: '+path)
        require(bool(local.stat().st_mode&0o111)==(mode=='100755'),'local executable mismatch: '+path)
    changed=set(p for p in current.keys()|prior.keys() if current.get(p)!=prior.get(p))
    require(changed==CHANGED,'unexpected changed source paths')
    summary={'status':'PASS','head_from_parent_receipt':HEAD,'tree':TREE,'prior_tree':PRIOR_TREE,'tracked_leaves':len(current),'all_local_bytes_and_executable_modes_exact':True,'changed_paths':sorted(changed),'local_head':git('rev-parse','HEAD').decode().strip(),'note':'Exact tree object is the audit input. Local preparation commit differs from public head; remote head/merge identity comes from the parent receipt.'}
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
    observation={'observation':'Ten individual licence_file references already do not resolve in the prior tree. Inventory and aggregate notices are unchanged; this is an existing metadata-reference issue, not evidence of missing aggregate notices or licence removal by the fixture changes. Actual APK asset presence is checked separately.','current_tree':TREE,'prior_tree':PRIOR_TREE,'missing_notice_paths':missing,'all_already_absent_from_prior_tree':True,'inventory_and_aggregate_bindings':bindings,'limitation':'One-time contextual comparison only; not a normal CI gate or independent legal conclusion. Separate tracking is outside this audit.'}
    (output/'preexisting-inventory-observation.json').write_text(json.dumps(observation,indent=2)+'\n')
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output-directory',type=pathlib.Path,required=True);a=p.parse_args()
    audit(a.repo,a.output_directory)
    print('PASS: all 1,062 local bytes/modes match the exact tree; only two JVM tests changed; ten stale licence paths remain pre-existing with unchanged aggregates.')
