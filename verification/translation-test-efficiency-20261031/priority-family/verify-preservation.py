import ast,hashlib,json,pathlib,re,subprocess
r=pathlib.Path('/workspace/scratch/bbca2890f602/priority-family-cleanup-20261031'); originals=json.load(open('/tmp/priority-family-originals.json')); e=pathlib.Path('/tmp/priority-family-evidence')
assert len(originals)==41
py_callers=[p for p in originals if p.startswith('tools/') and not p.endswith('priority_cohort_checks.py')]
kt_callers=[p for p in originals if p.endswith('.kt') and not p.endswith('/PriorityWordingExpectations.kt')]
assert len(py_callers)==7 and len(kt_callers)==32
aststr=lambda n:ast.dump(n,include_attributes=False)
def fun(s,name):return next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name==name)
shared=(r/'tools/priority_cohort_checks.py').read_text();n=fun(shared,'current_row');ns=ast.get_source_segment(shared,n).replace('def current_row(tag, key, name, tags, fixture):','def current_row(tag,key):').replace('fixture(name)','fixture(NAME)').replace('tag not in tags','tag not in TAGS')
for p in py_callers:
 old=originals[p];new=(r/p).read_text();n=fun(new,'current_row');assert aststr(n.body[0])==aststr(ast.parse('return _cohort_checks.current_row(tag, key, NAME, TAGS, fixture)').body[0]);assert aststr(fun(old,'current_row'))==aststr(ast.parse(ns).body[0])
 lines=new.splitlines(True);lines[n.lineno-1:n.end_lineno]=[ast.get_source_segment(old,fun(old,'current_row'))+'\n'];restored=''.join(lines).replace('import priority_cohort_checks as _cohort_checks\n','');assert aststr(ast.parse(restored))==aststr(ast.parse(old))
np=ast.parse(shared);np.body=[x for x in np.body if not (isinstance(x,ast.FunctionDef) and x.name=='current_row')];assert aststr(np)==aststr(ast.parse(originals['tools/priority_cohort_checks.py']))
normalize=lambda s:re.sub(r'\s+','',re.sub(r'//[^\n]*','',s))
shared_kt=(r/'Paintroid/src/test/java/org/catrobat/paintroid/local/PriorityWordingExpectations.kt').read_text();loop=shared_kt.split('    fun forEachLocale(',1)[1].split('    ) {\n',1)[1][:-2]
identities=[];assertions=0
for p in kt_callers:
 old=originals[p];new=(r/p).read_text();mo=re.search(r'    private fun forEachLocale\(.*?(?=\n    @Test)',old,re.S);mn=re.search(r'    private fun forEachLocale\(.*?(?=\n    @Test)',new,re.S);sig,body=mo.group().split(' {\n',1)
 assert normalize(body)==normalize(loop)
 expected=sig+' =\n        PriorityWordingExpectations.forEachLocale(\n            tags, previousResources, previousLocale, previousTag, check)\n'
 assert mn.group()==expected
 assert new[:mn.start()]+mo.group()+new[mn.end():]==old
 methods=re.findall(r'@Test\s+fun\s+(\w+)',old);identities.extend(p+'#'+m for m in methods);assertions+=len(re.findall(r'\b(?:assert\w*|require|check)\s*\(',old))
 assert len(re.findall(r'previous(?:Resources|Locale|Tag)\s*=',old))==3
# Existing shared Kotlin object is unchanged except explicit imports and appended helper.
p='Paintroid/src/test/java/org/catrobat/paintroid/local/PriorityWordingExpectations.kt';prefix=shared_kt.split('\n    /** Shared unchanged activity lifecycle;',1)[0]+'\n}\n';old=originals[p]
newimports=set(re.findall(r'^import .+$',prefix,re.M))-set(re.findall(r'^import .+$',old,re.M))
for line in newimports:prefix=prefix.replace(line+'\n','')
assert prefix.replace('    }\n\n}\n', '    }\n}\n')==old
changed=subprocess.check_output(['git','diff','--name-only'],cwd=r,text=True).splitlines();assert set(changed)==set(originals)
assert not subprocess.check_output(['git','diff','--name-only','--','tools/fixtures','Paintroid/src/main'],cwd=r,text=True)
subprocess.run(['git','diff','--check'],cwd=r,check=True)
receipt={'base_commit':'f3d617d0ec83dcab20d9fd5287272207c17c8d51','base_tree':subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=r,text=True).strip(),'changed_file_count':41,'python_exact_body_callers':7,'kotlin_exact_lifecycle_callers':32,'kotlin_existing_test_methods':len(identities),'kotlin_original_assertion_and_require_calls':assertions,'checks':['Every Python caller AST restores exactly after reversing wrapper/import','Shared Python body AST equals all seven originals after dependency-name substitution','Shared Kotlin lifecycle equals all 32 originals after only whitespace/comment normalization','Every Kotlin caller restores byte-for-byte after reversing single method replacement','Every existing test body, locale list, alias, decoder, Before/After and diagnostic unchanged','Historical fixtures and all production paths unchanged','Exactly 41 intended existing files; no added/deleted files','git diff --check passed'],'files':sorted(originals),'jvm_test_identities':sorted(identities)}
(e/'preservation.json').write_text(json.dumps(receipt,indent=2)+'\n');(e/'change.patch').write_bytes(subprocess.check_output(['git','diff'],cwd=r));print(json.dumps({k:v for k,v in receipt.items() if k not in ('files','jvm_test_identities')},indent=2))
