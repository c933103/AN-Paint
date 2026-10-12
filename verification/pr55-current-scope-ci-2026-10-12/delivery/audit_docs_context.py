#!/usr/bin/env python3
"""Read-only exact docs successor check; freeze predecessor without rerunning it."""
import argparse, hashlib, json, pathlib, subprocess
from audit_direction_delivery import TREE, HEAD, require, sha

PRIOR_TREE = 'dc1ba97dacc573ead73729297eb739ecb244dcf5'
PRIOR_HEAD = 'e19c766eb3eaedc1b3cd3657bb92864f81a9498a'
DOCS = {'AGENTS.md', 'README.md', 'TRANSLATING.md'}

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
    a, b = leaves(PRIOR_TREE), leaves(TREE)
    require(len(a) == len(b) == 1094 and a.keys() == b.keys(), 'Tree path inventory differs')
    changed = {p for p in a if a[p] != b[p]}
    require(changed == DOCS, 'Docs-only change inventory differs')
    for p, (mode, digest) in b.items():
        local = repo / p; raw = local.read_bytes()
        require(not local.is_symlink() and mode in ('100644', '100755'), 'Unexpected file mode')
        require(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == digest, 'Local bytes differ: ' + p)
        require(bool(local.stat().st_mode & 0o111) == (mode == '100755'), 'Local executable mode differs: ' + p)
    frozen = json.loads((pathlib.Path(__file__).parent / 'prior-review-freeze-manifest.json').read_bytes())
    observed = [{'path':p.relative_to(prior).as_posix(), 'bytes':p.stat().st_size, 'sha256':sha(p.read_bytes())} for p in sorted(prior.rglob('*')) if p.is_file()]
    require(frozen['files'] == observed, 'Prior review changed')
    result = {'status':'PASS', 'head_from_parent_receipt':HEAD, 'tree':TREE, 'prior_head':PRIOR_HEAD, 'prior_tree':PRIOR_TREE, 'tracked_leaves':len(b), 'all_local_bytes_and_executable_modes_exact':True, 'changed_paths':sorted(changed), 'unchanged_bytes_and_modes':len(b)-len(changed), 'runtime_tests_resources_fonts_workflow_unchanged':True, 'frozen_prior_files':len(observed), 'frozen_prior_review_unchanged':True, 'local_preparation_head':git('rev-parse','HEAD').decode().strip(), 'docs':[{ 'path':p, 'old_blob':a[p][1], 'new_blob':b[p][1], 'old_mode':a[p][0], 'new_mode':b[p][0], 'current_sha256':sha((repo/p).read_bytes())} for p in sorted(changed)], 'limit':'Exact Git tree and local bytes/modes independently checked. Public head/merge identity is supplied by the parent GitHub receipt; no new source/linguistic acceptance or app execution claim.'}
    (output/'source-preflight.json').write_text(json.dumps(result,indent=2)+'\n')
    (output/'source-tree-diff.log').write_bytes(git('diff','--name-status',PRIOR_TREE,TREE))
    print('PASS: 1,094 local bytes/modes exact; precisely three Markdown changes; other 1,091 leaves unchanged; prior review frozen.')

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ('repo','prior-review','output-directory'):p.add_argument('--'+arg,type=pathlib.Path,required=True)
    a=p.parse_args();audit(a.repo,a.prior_review,a.output_directory)
