#!/usr/bin/env python3
"""One-time authoring scope review; not an application snapshot gate."""
import argparse,hashlib,json,pathlib,subprocess
BASE='ab6f5497e147e81d4c50f4954ea87f364be087aa';TREE='d2379b932cc976bb5347515887ecdfc4729ee70d'
FILES={'Paintroid/src/test/java/org/catrobat/paintroid/local/LocalizedDialogLayoutTest.kt':'d7afe409fa63970b64940a122eef6a8702bf7ef7a2f146c76d2cb66e153dc012','Paintroid/src/test/java/org/catrobat/paintroid/local/UiDirectionContextTest.kt':'65cd766a4e7c60b3677881ee20af2019943ad50692461f679db76ea2892efd06'}
def require(v,m):
 if not v:raise ValueError(m)
def audit(repo):
 def git(*args):return subprocess.check_output(['git',*args],cwd=repo)
 require(git('write-tree').decode().strip()==TREE,'candidate tree');require(not git('diff','--name-only'),'unstaged changes')
 require(set(git('diff','--name-only',BASE,TREE).decode().splitlines())==set(FILES),'changed scope')
 git('diff','--check',BASE,TREE);rows=[]
 for p,h in FILES.items():
  b=(repo/p).read_bytes();require(hashlib.sha256(b).hexdigest()==h and git('show',TREE+':'+p)==b,'file binding '+p)
  rows.append({'path':p,'sha256':h,'bytes':len(b),'mode':git('ls-tree',TREE,'--',p).decode().split()[0]})
 p='Paintroid/src/test/java/org/catrobat/paintroid/local/UiDirectionContextTest.kt';old=git('show',BASE+':'+p).decode();new=(repo/p).read_text().replace('import android.os.Build\n','');start='    @Test @Config(sdk=[21,24]) @GraphicsMode(GraphicsMode.Mode.LEGACY)\n';end='    private fun awaitUi('
 require(old.split(start)[0]==new.split(start)[0] and old[old.index(end):]==new[new.index(end):],'native cases/helpers changed')
 return {'status':'PASS','baseline_tree':BASE,'candidate_tree':TREE,'files':rows,'native_twelve_bodies_and_shared_helpers_unchanged':True,'other_tracked_paths_unchanged':True,'scope':'One-time independent review, never a permanent CI source snapshot gate.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();r=audit(a.repo);a.output.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
