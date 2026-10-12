#!/usr/bin/env python3
"""One-time review receipt; never a normal CI snapshot/reconstruction gate."""
import argparse,hashlib,json,pathlib,subprocess
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
def git(*args):return subprocess.check_output(['git',*args],cwd=a.repo)
def require(x,m):
 if not x:raise ValueError(m)
base='3dcc1a82f878ad7e0e708cff25ec8d493b88bbc6';candidate='592a60877524c5c118695cb45a4d0d5cd257b25a'
require(git('rev-parse','HEAD^{tree}').decode().strip()==base,'unexpected baseline tree')
require(not git('diff','--name-only'),'unstaged source/evidence changes')
require(not git('ls-files','--others','--exclude-standard'),'untracked delivery paths')
entries=[]
for raw in git('ls-files','--stage','-z').split(b'\0'):
 if not raw:continue
 meta,path=raw.split(b'\t',1);mode,blob,stage=meta.decode().split();path=path.decode()
 require(stage=='0','unmerged index');entries.append((mode,blob,path))
# Exact tree construction is verified without adding a new object to this checkout.
require(git('diff','--cached','--name-only',candidate)==b'','candidate tree/index differs')
rename_aware=git('diff','--cached','--name-status',base).decode().splitlines()
changed=git('diff','--cached','--no-renames','--name-status',base).decode().splitlines();rows=[];removed=[];categories={}
for line in changed:
 kind,path=line.split('\t',1);category=path.split('/')[0];categories[category]=categories.get(category,0)+1
 if kind=='D':removed.append(path)
 elif not path.startswith('verification/'):
  data=(a.repo/path).read_bytes();rows.append({'path':path,'change':kind,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
result={'schema_version':1,'purpose':'One-time independent review source binding, kept outside normal application CI','base_public_commit':'04b128889a4ff9159f199d1737bd07d41e22162d','base_tree':base,'candidate_staged_tree':candidate,'local_HEAD_is_temporary_snapshot':True,'tracked_candidate_leaves':len(entries),'changed_paths_no_renames':len(changed),'changed_paths_rename_aware':len(rename_aware),'renames':[x for x in rename_aware if x.startswith('R')],'changed_by_top_directory':categories,'deleted_paths':len(removed),'deleted_verification_paths':sum(x.startswith('verification/') for x in removed),'nonverification_current_changed_inputs':rows,'removed_paths':removed,'working_tree_matches_index':True,'public_successor_head_run_binding':'UNRUN: writer has not published this reviewed candidate'}
a.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS source binding',candidate,len(entries),'leaves',len(changed),'changes')
