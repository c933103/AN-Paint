#!/usr/bin/env python3
"""Reproduce exact PR43/C023 source composition against the frozen partition tree."""
import hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path(sys.argv[1]).resolve()
OUT=pathlib.Path(__file__).resolve().parent
BASE='5703a61394791f18e9f2597272d908d9840599af'
PR43='4f9082aa687a5c36b559061bcc10d0e39331610f'
C023='13edc0e81af1ca1561ee2dabedc17959cd85adc0'
PARTITION='7ca1d8df95d1fe7dd0fe1647c792391f90db118e'
TIFF='c9894b1d5d930e0350e07a1083add82a77c42095'
FINAL='2ced71de3ec31e88650015a53748a65cefda2975'
def git(*args,env=None):return subprocess.check_output(['git','-C',str(ROOT),*args],env=env)
def require(x,why):
 if not x:raise ValueError(why)
def entries(ref):
 out={}
 for line in git('ls-tree','-r','-z',ref).split(b'\0'):
  if line:
   info,p=line.split(b'\t',1);mode,typ,sha=info.decode().split();out[p.decode()]={'mode':mode,'type':typ,'blob':sha}
 return out
def digest(ref,p):return hashlib.sha256(git('show',f'{ref}:{p}')).hexdigest()
trees={k:entries(v) for k,v in dict(base=BASE,pr43=PR43,c023=C023,partition=PARTITION,tiff=TIFF,final=FINAL).items()}
def changed(a,b):return sorted(p for p in set(a)|set(b) if a.get(p)!=b.get(p))
first=changed(trees['base'],trees['pr43']);second=changed(trees['pr43'],trees['c023'])
require(len(first)==43,'Original PR43 delta is not43 paths')
require(len(second)==14,'C023 delta is not14 paths')
for label,start,end,original_before,original_after,delta in [('pr43',trees['partition'],trees['tiff'],trees['base'],trees['pr43'],first),('c023',trees['tiff'],trees['final'],trees['pr43'],trees['c023'],second)]:
 require(set(end)==set(start)|set(original_after)-set(original_before),'Path union mismatch '+label)
 require(changed(start,end)==delta,'Delta path mismatch '+label)
 for p in delta:
  require(start.get(p)==original_before.get(p),'Preimage mismatch '+p)
  require(end.get(p)==original_after.get(p),'Output mismatch '+p)
 for p in set(start)-set(delta):require(start[p]==end[p],'Unrelated path changed '+p)
source_delta=changed(trees['partition'],trees['final'])
rows=[]
for p in sorted(trees['final']):
 origin='c023' if p in second else 'pr43' if p in first else 'partition'
 rows.append({'path':p,'origin':origin,**trees['final'][p]})
(OUT/'composition-manifest.json').write_text(json.dumps({'refs':dict(base=BASE,pr43=PR43,c023=C023,partition=PARTITION,tiff=TIFF,final=FINAL),'paths':rows},ensure_ascii=False,indent=2)+'\n')
fixture='tools/fixtures/tiff_size_wording_scope.json'; cfixture='tools/fixtures/tiff_c023_wording_scope.json'
require(digest(FINAL,fixture)=='9cead98f8f826c5c853f4b0dc6cd6b80f8760274770a00f600c690d44fba0ac1','Original37 pin differs')
require(digest(FINAL,cfixture)=='d2dcbbeaef13c80ae9dfe4d1ec9595c8ba82cbe92d057479f5b25e4deba3d6c4','C023 pin differs')
for p in trees['partition']:
 if p.startswith(('app/src/androidTest/','Paintroid/src/androidTest/')) or p in ['.github/workflows/android.yml','tools/verify_exact_script_generation.py','tools/test_exact_script_generation.py','tools/test_exact_script_resource_routing.py','tools/run_android_instrumentation.py']:
  require(trees['partition'][p]==trees['final'][p],'Inherited Android/packaged-resource assertion changed '+p)
for p in trees['partition']:
 if p.startswith('verification/') and p in trees['final']:require(trees['partition'][p]==trees['final'][p],'Historical evidence changed '+p)
patches={}
for name,before,after in [('pr43-on-partition',PARTITION,TIFF),('c023-on-pr43-partition',TIFF,FINAL),('combined-on-partition',PARTITION,FINAL),('combined-from-original-pr43',PR43,FINAL)]:
 data=git('diff','--binary',before,after);path=OUT/f'{name}.patch';path.write_bytes(data)
 index=OUT/f'{name}.index'
 if index.exists():index.unlink()
 env=dict(os.environ,GIT_INDEX_FILE=str(index));git('read-tree',before,env=env);git('apply','--cached',str(path),env=env)
 replay=git('write-tree',env=env).decode().strip();require(replay==after,'Patch replay mismatch '+name)
 patches[name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'replayed_tree':replay}
require(git('diff','--name-only')==b'','Worktree/index differs')
require(git('write-tree').decode().strip()==FINAL,'Final index changed')
summary={'success':True,'conflicts':0,'source_semantic_changes_during_composition':False,'partition_tree':PARTITION,'pr43_only_tree':TIFF,'with_c023_tree':FINAL,'counts':{k:len(v) for k,v in trees.items()},'original_pr43_delta_paths':len(first),'c023_delta_paths':len(second),'final_delta_paths':len(source_delta),'inherited_partition_paths_unchanged':len(trees['partition'])-sum(p in trees['partition'] for p in source_delta),'removed_paths':sorted(set(trees['partition'])-set(trees['final'])),'mode_changes': [p for p in set(trees['partition'])&set(trees['final']) if trees['partition'][p]['mode']!=trees['final'][p]['mode']],'original37_sha256':digest(FINAL,fixture),'separate_c023_sha256':digest(FINAL,cfixture),'historical_scope_sha256':digest(FINAL,'verification/commons-copy-credit-errors-2026-10-09/source-scope.json'),'patches':patches}
(OUT/'composition-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
