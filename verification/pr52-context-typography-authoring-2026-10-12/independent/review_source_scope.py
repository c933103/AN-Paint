#!/usr/bin/env python3
"""One-time reviewer scope/inventory check, outside source/CI; no compilation claim."""
import pathlib,sys,subprocess,re,json,hashlib,argparse

def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,message):
    if not ok:raise AssertionError(message)
def current_inventory(repo,tree):
    from run_android_instrumentation import ANNOTATIONS
    expected=[];sources=[]
    for relative in sorted(subprocess.check_output(['git','ls-tree','-r','--name-only',tree,'Paintroid/src/test'],cwd=repo,text=True).splitlines()):
        if not relative.endswith('.kt'):continue
        p=repo/relative
        source=subprocess.check_output(['git','show',tree+':'+str(p.relative_to(repo))],cwd=repo).decode()
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

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=pathlib.Path,required=True);parser.add_argument('--tree',required=True);parser.add_argument('--output',type=pathlib.Path,required=True);args=parser.parse_args()
    repo=args.repo.resolve();sys.path.insert(0,str(repo/'tools'));base='b6bf7626c1d7c4aef669394970046ffc89a5c877'
    require(not subprocess.check_output(['git','diff','--name-only'],cwd=repo).strip(),'unstaged edits')
    require(subprocess.check_output(['git','write-tree'],cwd=repo,text=True).strip()==args.tree,'staged tree mismatch')
    names=subprocess.check_output(['git','diff','--name-only',base,args.tree],cwd=repo,text=True).splitlines()
    prod=[p for p in names if '/src/main/' in p]
    wanted=['FontCatalog.kt','LocaleTooltip.kt','LocaleTypography.kt','VerticalText.kt']
    require(sorted(pathlib.Path(p).name for p in prod)==wanted,'production scope expanded')
    require(not any('/res/' in p or '/assets/' in p or '/androidTest/' in p or p.endswith(('.yml','.gradle','.md')) for p in names),'resource/font/installed/workflow/doc changed')
    old=current_inventory(repo,base);new=current_inventory(repo,args.tree)
    removed=set(map(tuple,old['expected']))-set(map(tuple,new['expected'])); added=set(map(tuple,new['expected']))-set(map(tuple,old['expected']))
    require(not removed,'prior JVM identities removed')
    result={'baseline':base,'candidate_tree':args.tree,'scope':'One-time review only; no Android/Kotlin execution or permanent source gate','changed_paths':names,'production_paths':prod,'source_hashes':{p:sha((repo/p).read_bytes()) for p in names},'prior_jvm_count':len(old['expected']),'current_jvm_count':len(new['expected']),'added_executions':sorted(added),'removed_executions':sorted(removed),'current_inventory':new}
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['candidate_tree','prior_jvm_count','current_jvm_count','added_executions','removed_executions']},indent=2))
if __name__=='__main__':main()
