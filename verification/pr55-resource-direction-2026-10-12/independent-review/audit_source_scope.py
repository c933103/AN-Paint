#!/usr/bin/env python3
"""One-time review binding, never an application CI snapshot gate."""
import argparse, hashlib, json, pathlib, re, subprocess

def git(repo,*args): return subprocess.check_output(['git',*args],cwd=repo)
def digest(b): return hashlib.sha256(b).hexdigest()
def check(v,m):
    if not v: raise ValueError(m)
def audit(repo,manifest):
    base='592a60877524c5c118695cb45a4d0d5cd257b25a'
    candidate='ab6f5497e147e81d4c50f4954ea87f364be087aa'
    data=json.loads(manifest.read_text()); paths={r['path'] for r in data}
    check(len(paths)==len(data)==23,'manifest path cardinality')
    check(git(repo,'write-tree').decode().strip()==candidate,'staged tree differs')
    check(not git(repo,'diff','--name-only'),'unstaged tracked source changes')
    diffpaths=set(git(repo,'diff','--name-only','--no-renames',base,candidate).decode().splitlines())
    check(diffpaths==paths,'manifest and actual changed paths differ')
    git(repo,'diff','--check',base,candidate)
    rows=[]
    for r in sorted(data,key=lambda r:r['path']):
        p=r['path']; b=(repo/p).read_bytes(); staged=git(repo,'show',candidate+':'+p)
        check(b==staged,'worktree/tree differ '+p)
        check(digest(b)==r['sha256'] and len(b)==r['bytes'],'writer file binding differs '+p)
        rows.append({'path':p,'bytes':len(b),'sha256':digest(b),'git_mode':git(repo,'ls-tree',candidate,'--',p).decode().split()[0]})
    prod=[p for p in sorted(paths) if '/src/main/' in p]
    check(len(prod)==15 and all(p.endswith('.kt') for p in prod),'production scope')
    excluded=['Paintroid/src/main/res','Paintroid/src/main/assets','app/src/main/res','.github/workflows',
              'Paintroid/src/main/java/org/catrobat/paintroid/classic/LocaleTypography.kt',
              'Paintroid/src/main/java/org/catrobat/paintroid/classic/LocaleTooltip.kt',
              'Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt',
              'Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt',
              'app/src/androidTest/java/paint/anpaint/android/GalleryViewportDeviceTest.kt']
    for p in excluded: check(not git(repo,'diff','--name-only',base,candidate,'--',p),'excluded path changed '+p)
    newtest=repo/'Paintroid/src/test/java/org/catrobat/paintroid/local/UiDirectionContextTest.kt'
    s=newtest.read_text(); names=re.findall(r'\bfun\s+(\w+)\s*\(',s)
    declared=re.findall(r'@Test\s+(?:@Config\([^\n]*\)\s+@GraphicsMode\([^\n]*\)\s+)?fun\s+(\w+)\s*\(',s)
    check(len(declared)==7,'new source test discovery')
    ids=[]
    for name in declared:
        sdks=[21,24] if name.startswith('legacyResourceContexts') else [30,35]
        for i,sdk in enumerate(sdks): ids.append({'classname':'org.catrobat.paintroid.local.UiDirectionContextTest','name':name+(f'[{sdk}]' if i==0 else ''),'sdk':sdk})
    return {'status':'PASS','kind':'One-time authoring review; no Android execution claim','baseline_public_head':'43ab6622cdf6aac957a8d31cf2c5c20009e71d6e','baseline_tree':base,'candidate_staged_tree':candidate,'changed_files':rows,'production_files':prod,'unchanged_excluded_paths':excluded,'new_declared_test_methods':len(declared),'new_expected_jvm_executions':ids,'writer_manifest_sha256':digest(manifest.read_bytes()),'review_diff_sha256':digest(git(repo,'diff','--binary','--no-renames',base,candidate))}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--manifest',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
    result=audit(a.repo,a.manifest);a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'changed_paths':len(result['changed_files']),'new_jvm_executions':len(result['new_expected_jvm_executions'])}))
