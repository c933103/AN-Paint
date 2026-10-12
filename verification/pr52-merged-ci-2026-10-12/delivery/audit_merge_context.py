#!/usr/bin/env python3
"""Read-only PR52 merged-head identical-tree/source check; preserve accepted PR55 evidence."""
import argparse, hashlib, json, pathlib, subprocess
from audit_direction_delivery import TREE, HEAD, MERGE, RUN, require, sha
PRIOR_TREE = 'b6bf7626c1d7c4aef669394970046ffc89a5c877'
PRIOR_HEAD = '4a35933ff6b6d0013dac8743cc5eeac1c1033e05'

def audit(repo, prior, output):
    def git(*args): return subprocess.check_output(['git', *args], cwd=repo)
    def leaves(tree):
        result = {}
        for row in git('ls-tree', '-rz', tree).split(b'\0'):
            if not row: continue
            meta, path = row.split(b'\t'); mode, kind, digest = meta.decode().split()
            require(kind == 'blob', 'Unexpected tree leaf')
            result[path.decode()] = (mode, digest)
        return result
    prior_delivery = json.loads((prior/'delivery-result.json').read_bytes())
    require(prior_delivery['status']=='PASS' and prior_delivery['head']==PRIOR_HEAD and prior_delivery['tree']==PRIOR_TREE, 'Accepted prior receipt identity differs')
    a, b = leaves(PRIOR_TREE), leaves(TREE)
    require(len(a) == len(b) == 1094 and a == b, 'Accepted source tree differs')
    for p, (mode, digest) in b.items():
        local = repo / p; raw = local.read_bytes()
        require(not local.is_symlink() and mode in ('100644', '100755'), 'Unexpected file mode')
        require(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == digest, 'Local bytes differ: ' + p)
        require(bool(local.stat().st_mode & 0o111) == (mode == '100755'), 'Local executable mode differs: ' + p)
    frozen = json.loads((pathlib.Path(__file__).parent / 'prior-review-freeze-manifest.json').read_bytes())
    observed = [{'path':p.relative_to(prior).as_posix(), 'bytes':p.stat().st_size, 'sha256':sha(p.read_bytes())} for p in sorted(prior.rglob('*')) if p.is_file()]
    require(frozen['files'] == observed, 'Prior review changed')
    result = {'status':'PASS', 'head_from_parent_receipt':HEAD, 'tree':TREE, 'merge':MERGE, 'run_id':int(RUN), 'prior_head':PRIOR_HEAD, 'prior_tree':PRIOR_TREE, 'tracked_leaves':len(b), 'all_local_bytes_and_executable_modes_exact':True, 'changed_paths':[], 'unchanged_bytes_and_modes':len(b), 'runtime_tests_resources_fonts_workflow_docs_unchanged':True, 'frozen_prior_files':len(observed), 'frozen_prior_review_unchanged':True, 'local_preparation_head':git('rev-parse','HEAD').decode().strip(), 'limit':'Exact Git tree and all local bytes/modes independently checked. Public head/ordered-parent/synthetic-merge identity comes from the parent-verified GitHub receipt. No rereview of unchanged source, linguistic acceptance or app execution claim.'}
    (output/'source-preflight.json').write_text(json.dumps(result,indent=2)+'\n')
    (output/'source-tree-diff.log').write_bytes(git('diff','--name-status',PRIOR_TREE,TREE))
    print('PASS: all 1,094 local source bytes/modes exact; zero changes from accepted PR55 tree; 60-file prior review remains frozen.')

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ('repo','prior-review','output-directory'):p.add_argument('--'+arg,type=pathlib.Path,required=True)
    a=p.parse_args();audit(a.repo,a.prior_review,a.output_directory)
