#!/usr/bin/env python3
"""Bind all current source leaves to the frozen context-typography authoring review."""
import argparse, hashlib, json, pathlib, subprocess
from audit_direction_delivery import TREE, HEAD, MERGE, RUN, require, sha
PRIOR_TREE='b6bf7626c1d7c4aef669394970046ffc89a5c877'
def file_rows(root):
    return [{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(root.rglob('*')) if p.is_file()]
def audit(repo, historical, authoring, output):
    def git(*args): return subprocess.check_output(['git',*args],cwd=repo)
    def leaves(tree):
        rows={}
        for row in git('ls-tree','-rz',tree).split(b'\0'):
            if not row:continue
            meta,path=row.split(b'\t');mode,kind,digest=meta.decode().split()
            require(kind=='blob' and mode in ('100644','100755'),'unsupported leaf')
            rows[path.decode()]=(mode,digest)
        return rows
    previous,current=leaves(PRIOR_TREE),leaves(TREE)
    require(len(previous)==1094 and len(current)==1095,'unexpected source inventory')
    for path,(mode,digest) in current.items():
        p=repo/path;require(not p.is_symlink(),'unexpected symlink: '+path);data=p.read_bytes()
        require(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==digest,'local source differs: '+path)
        require((p.stat().st_mode & 0o777)==(int(mode,8)&0o777),'local mode differs: '+path)
    for label,root in [('historical',historical),('authoring',authoring)]:
        require(file_rows(root)==json.loads((pathlib.Path(__file__).parent/(label+'-review-freeze.json')).read_bytes())['files'],label+' review changed')
    scope=json.loads((authoring/'final-source-scope.json').read_bytes())
    review=json.loads((authoring/'REVIEW-RESULT.json').read_bytes())
    changed=sorted(p for p in set(previous)|set(current) if previous.get(p)!=current.get(p))
    require(scope['baseline']==PRIOR_TREE and scope['candidate_tree']==TREE,'authoring scope identity differs')
    require(review['status']=='PASS_BOUNDED_SOURCE_AND_HOST_REVIEW' and review['reviewed_staged_tree']==TREE,'authoring review identity differs')
    require(changed==scope['changed_paths'] and len(changed)==15,'authoring changed paths differ')
    require(sorted(scope['source_hashes'])==changed,'authoring source hash inventory differs')
    for path,digest in scope['source_hashes'].items(): require(sha((repo/path).read_bytes())==digest,'authoring source hash differs: '+path)
    require(scope['current_jvm_count']==932 and scope['prior_jvm_count']==910 and scope['removed_executions']==[],'authoring JVM inventory receipt differs')
    require(len(scope['added_executions'])==22,'authoring addition receipt count differs')
    result={'status':'PASS','head_from_parent_receipt':HEAD,'tree':TREE,'merge':MERGE,'run_id':int(RUN),'prior_tree':PRIOR_TREE,'tracked_leaves':len(current),'all_local_content_and_full_permission_modes_exact':True,'changed_paths':changed,'authoring_source_hashes_exact':True,'authoring_expected_jvm_executions':932,'historical_review_files':len(file_rows(historical)),'authoring_review_files':len(file_rows(authoring)),'frozen_reviews_unchanged':True,'local_preparation_head':git('rev-parse','HEAD').decode().strip(),'limits':['Public commit and ordered-parent identity are supplied parent-verified provenance; public commit objects are not in this local repository. Exact tree objects and all local content/modes are independently checked.','Current JVM count is a source-review receipt, not execution evidence. No source rereview, Android run or linguistic acceptance is claimed.']}
    (output/'source-preflight.json').write_text(json.dumps(result,indent=2)+'\n')
    (output/'source-tree-diff.log').write_bytes(git('diff','--name-status',PRIOR_TREE,TREE))
    print('PASS: all 1,095 leaves and modes exact; 15 changed paths bound to frozen authoring review; historical and authoring reviews unchanged.')
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('repo','historical-review','authoring-review','output-directory'):p.add_argument('--'+k,type=pathlib.Path,required=True)
    a=p.parse_args();audit(a.repo,a.historical_review,a.authoring_review,a.output_directory)
