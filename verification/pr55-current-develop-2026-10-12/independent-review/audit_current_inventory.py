#!/usr/bin/env python3
"""One-time current JVM identity comparison; no normal-CI historical snapshot gate."""
import argparse,collections,hashlib,json,pathlib,re,subprocess,sys
TREE=None
def sha(b):return hashlib.sha256(b).hexdigest()

def read_source(repo,path):return subprocess.check_output(['git','show',TREE+':'+path],cwd=repo)

def current_inventory(repo):
    from run_android_instrumentation import ANNOTATIONS
    expected=[];sources=[]
    for p in sorted((repo/'Paintroid/src/test').rglob('*.kt')):
        source=read_source(repo,str(p.relative_to(repo))).decode()
        package=re.search(r'^package\s+([\w.]+)',source,re.M)
        owners=list(re.finditer(r'^[ \t]*(?P<annotations>'+ANNOTATIONS+r')?(?:(?:internal|public|open|abstract)\s+)*class\s+(?P<owner>\w+)',source,re.M))
        owner=next((o for o in owners if o.group('owner')==p.stem),None)
        matches=list(re.finditer(r'(?P<annotations>'+ANNOTATIONS+r')(?:(?:public|internal|suspend)\s+)*fun\s+(?P<method>`[^`]+`|\w+)\s*\(',source))
        methods=[m for m in matches if re.search(r'@Test\b',m.group('annotations'))]
        require(len(methods)==len(re.findall(r'@Test\b',source)),'unparsed source tests '+str(p))
        if not methods:continue
        require(package and owner and '@Ignore' not in source,'unsupported class/ignored test '+str(p))
        def sdks(annotations):
            configs=re.findall(r'@Config\(([^)]*)\)',annotations)
            values=[re.search(r'\bsdk\s*=\s*\[([^]]+)\]',c) for c in configs if re.search(r'\bsdk\s*=',c)]
            require(all(values) and len(values)<=1,'unparsed SDK config')
            if not values:return None
            require(re.fullmatch(r'[\d,\s]+',values[0].group(1)),'nonliteral SDK config')
            return [int(x.strip()) for x in values[0].group(1).split(',')]
        default=sdks(owner.group('annotations') or '') or [None]
        for method in methods:
            sdk=sdks(method.group('annotations')) or default
            name=method.group('method').strip('`')
            expected.extend((package.group(1)+'.'+owner.group('owner'),name+(f'[{v}]' if i<len(sdk)-1 else '')) for i,v in enumerate(sdk))
        sources.append({'path':str(p.relative_to(repo)),'sha256':sha(source.encode()),'declared_methods':len(methods)})
    require(len(set(expected))==len(expected),'duplicate source execution identities')
    return {'expected':expected,'sources':sources,'scope':'Current Kotlin @Test declarations expanded by literal class/method @Config SDK lists; final selected SDK uses the unsuffixed Robolectric identity. No historical inventory fixture.'}

def require(v,message):
    if not v:raise ValueError(message)
def main():
 global TREE
 p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--base-tree',required=True);p.add_argument('--candidate-tree',required=True);p.add_argument('--writer-inventory',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();a.repo=a.repo.resolve();sys.path.insert(0,str(a.repo/'tools'))
 TREE=a.base_tree;base=current_inventory(a.repo);TREE=a.candidate_tree;current=current_inventory(a.repo);old=set(map(tuple,base['expected']));new=set(map(tuple,current['expected']));writer=json.loads(a.writer_inventory.read_text());require(json.loads(json.dumps(current))==writer,'writer current source inventory differs')
 removed=old-new;added=new-old;renames=[]
 patterns={'remaining81OfferedTagsExplicitlyResolveTheDefaultEnglishFallback':'remainingOfferedTagsExplicitlyResolveTheDefaultEnglishFallback','other81OfferedTagsUseTheGenuineDefaultHelpFallback':'otherOfferedTagsUseTheGenuineDefaultHelpFallback','all140TagsResolveTheirExplicitMessageOrDocumentedFallbackWithAsciiStatus':'allOfferedTagsResolveTheirExplicitMessageOrDocumentedFallbackWithAsciiStatus','all140TagsResolveTheirExplicitMessageOrDocumentedFallbackWithAsciiLimit':'allOfferedTagsResolveTheirExplicitMessageOrDocumentedFallbackWithAsciiLimit','all140TagsResolveTheirExplicitMessageOrDocumentedFallback':'allOfferedTagsResolveTheirExplicitMessageOrDocumentedFallback'}
 for owner,name in sorted(removed):
  found=[(owner,new_name+name[len(old_name):]) for old_name,new_name in patterns.items() if name==old_name or name.startswith(old_name+'[')]
  require(len(found)==1 and found[0] in added,'unaccounted removed or renamed execution '+owner+'.'+name);renames.append({'owner':owner,'before':name,'after':found[0][1]});added.remove(found[0])
 require(len(added)==4 and all(x[0].endswith('.AppLanguageTest') for x in added),'unexpected net addition')
 r={'status':'PASS_CURRENT_SOURCE_INVENTORY','base_tree':a.base_tree,'candidate_tree':a.candidate_tree,'base_count':len(old),'candidate_count':len(new),'truthful_renames':renames,'new_executions':[list(x) for x in sorted(added)],'unaccounted_removed':[],'writer_inventory_equal':True,'candidate_identity_set_sha256':sha(json.dumps(sorted(new),separators=(',',':')).encode()),'scope':'One-time integration review; fresh hosted XML must reconcile the new identities, and no past count is promoted into permanent CI.'};a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
if __name__=='__main__':main()
