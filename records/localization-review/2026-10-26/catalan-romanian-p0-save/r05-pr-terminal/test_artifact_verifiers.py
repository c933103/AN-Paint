#!/usr/bin/env python3
"""Synthetic verifier plumbing controls only; never hosted build/runtime evidence."""
import argparse, contextlib, copy, hashlib, io, json, re, runpy, sys, tempfile, types, zipfile
from pathlib import Path
from unittest.mock import patch
import xml.etree.ElementTree as E

PIN='a365f4b552448803c0bb48b3c44cdf508550eaf9'
TREE='65afa7b96a83c08e0ae08365166dec0520694356'
SYNTHETIC='1'*40
CLASSES=['CatalanRomanianSaveWordingTest','DanishNorwegianP0Test','NynorskRemainingP0Test','NynorskSaveWordingTest','DerivedExportStateTest','ImportSelectionTitleTest','TaggedColourImportTest']
EXCLUDED=['.gitignore','.idea/codeStyles/Project.xml','colorpicker/.gitignore']
PROBES=['01-clean','02-clean-debug-release','03-unchanged','04-1-input-change-and-stale-output','05-1-restored-input-release','04-2-input-change-and-stale-output','05-2-restored-input-release','05-source-change-and-stale-output','05-source-companion-added','05-source-companion-removed','06-reserved-app-variant-rejected','06-second-clean','07-release-first-after-clean']
def need(ok,msg):
 if not ok:raise ValueError(msg)
def h(b):return hashlib.sha256(b).hexdigest()
def git(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def js(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
def zipbytes(entries):
 b=io.BytesIO()
 with zipfile.ZipFile(b,'w',zipfile.ZIP_DEFLATED) as z:
  for n,v in entries.items():z.writestr(n,v)
 return b.getvalue()
def invoke(script,args,run_mock=None,modules=None):
 oldpath=list(sys.path)
 try:
  with patch.object(sys,'argv',[str(script)]+[str(x) for x in args]),contextlib.redirect_stdout(io.StringIO()),patch.dict(sys.modules,modules or {}):
   if run_mock:
    with patch('subprocess.run',run_mock):runpy.run_path(str(script),run_name='__main__')
   else:runpy.run_path(str(script),run_name='__main__')
 finally:sys.path[:]=oldpath

def main():
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--tree-file',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();scripts=Path(__file__).parent;controls=[]
 tree=json.loads(a.tree_file.read_bytes());need(tree['sha']==TREE and tree.get('truncated') is False,'pinned tree');blobs=[x for x in tree['tree'] if x['type']=='blob'];need(len(blobs)==1373 and len({x['path'] for x in blobs})==1373,'actual tracked source count')
 for x in blobs:need(git((a.source_root/x['path']).read_bytes())==x['sha'],'actual source byte binding')
 methods={};source_files={}
 for cls in CLASSES:
  path=f'Paintroid/src/test/java/org/catrobat/paintroid/local/{cls}.kt';raw=(a.source_root/path).read_bytes();source_files[path]=raw;matches=re.findall(r'@Test\s+(?:@[\w.]+(?:\([^()]*\))?\s+)*fun\s+([A-Za-z0-9_]+)\s*\(',raw.decode());need(len(set(matches))==len(matches)==len(re.findall(r'@Test\b',raw.decode())),'test source method parsing');methods[cls]=matches
 need(len(methods['CatalanRomanianSaveWordingTest'])==2 and len(methods['DerivedExportStateTest'])==7,'new test scope')
 expectations={tag:{} for tag in ('ca','ro','da','no','nn')}
 fixtures={'catalan_romanian_save_wording.json':('ca','ro'),'danish_norwegian_p0_wording.json':('da','no'),'nynorsk_p0_remaining_wording.json':('nn',),'nynorsk_save_wording.json':('nn',)}
 for name,tags in fixtures.items():
  path='tools/fixtures/current_localization/'+name;raw=(a.source_root/path).read_bytes();source_files[path]=raw
  for key,values in json.loads(raw)['values'].items():
   for tag in tags:
    value=values[tag];need(value[0]==value[-1]=='"' and '\\' not in value and key not in expectations[tag],'fixture display scope');expectations[tag][key]=value[1:-1]
 counts={k:len(v) for k,v in expectations.items()};need(counts=={'ca':10,'ro':10,'da':78,'no':78,'nn':80},'compiled fixture counts')
 def record(suite,name,fn,negative=False):
  try:fn()
  except (ValueError,KeyError,TypeError,AssertionError,FileNotFoundError,E.ParseError) as e:
   if not negative:raise
   controls.append({'suite':suite,'case':name,'expected':'reject','outcome':'rejected','reason':str(e).splitlines()[0] if not isinstance(e,FileNotFoundError) else 'required member/file missing'});return
  need(not negative,'incorrectly accepted synthetic negative: '+suite+'/'+name)
  controls.append({'suite':suite,'case':name,'expected':'accept synthetic fixture','outcome':'accepted synthetic fixture'})

 with tempfile.TemporaryDirectory() as td:
  root=Path(td);src=root/'source';src.mkdir()
  for n,b in source_files.items():q=src/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
  for n in EXCLUDED:q=src/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b'synthetic exclusion\n')
  for i in range(1373-len(source_files)-len(EXCLUDED)):
   q=src/f'synthetic/item-{i:04d}.txt';q.parent.mkdir(exist_ok=True);q.write_bytes(f'synthetic source {i}\n'.encode())
  synthetic_blobs=[{'path':str(q.relative_to(src)),'type':'blob','sha':git(q.read_bytes())} for q in sorted(src.rglob('*')) if q.is_file()];need(len(synthetic_blobs)==1373,'synthetic source inventory')
  treefile=root/'tree.json';treefile.write_bytes(js({'sha':SYNTHETIC,'truncated':False,'tree':synthetic_blobs}))
  toolroot=root/'tools';toolroot.mkdir();(toolroot/'aapt2').write_bytes(b'synthetic tool, not executable');(toolroot/'apksigner.jar').write_bytes(b'synthetic signer, not executable')
  def resources(values):
   lines=[]
   for i,key in enumerate(sorted({k for v in values.values() for k in v})):
    lines.append(f'  resource 0x7f{i:06x} string/{key}')
    for tag,v in values.items():
     if key in v:lines.append('    ('+tag+') '+json.dumps(v[key],ensure_ascii=False))
   return '\n'.join(lines)+'\n'
  def apk_case(change=None):
   d=root/'apk-case';d.mkdir(exist_ok=True);packaged={'AN-Paint/'+x['path']:(src/x['path']).read_bytes() for x in synthetic_blobs if x['path'] not in EXCLUDED};values=copy.deepcopy(expectations);conf={'tree':SYNTHETIC,'digest':None,'signature':True,'duplicate':False,'count':1373}
   if change:change(packaged,values,conf)
   sourcezip=zipbytes(packaged);apk=zipbytes({'assets/local-source/AN-Paint-source.zip':sourcezip});info={'commit':SYNTHETIC,'run_id':0,'apk_sha256':h(apk),'source_sha256':h(sourcezip)};archive=zipbytes({'app/build/outputs/apk/debug/app-debug.apk':apk,'build/delivery/AN-Paint-source.zip':sourcezip,'build/delivery/build-info.json':js(info)});(d/'apk-and-source.zip').write_bytes(archive)
   treefile.write_bytes(js({'sha':SYNTHETIC,'truncated':False,'tree':synthetic_blobs[:conf['count']]}))
   def fake_run(cmd,stdout,**kw):
    if cmd[0]==str(toolroot/'aapt2'):
     out=resources(values)
     if conf['duplicate']:out+='  resource 0x7ff00000 string/'+next(iter(values['ca']))+'\n    (ca) '+json.dumps(next(iter(values['ca'].values())))+'\n'
     stdout.write(out)
    else:stdout.write('Verifies\nVerified using v1 scheme (JAR signing): true\nVerified using v2 scheme (APK Signature Scheme v2): '+str(conf['signature']).lower()+'\nSigner #1 certificate SHA-256 digest: '+'0'*64+'\n')
   invoke(scripts/'verify_apk_artifact.py',['--directory',d,'--source-root',src,'--tree-file',treefile,'--tools',toolroot,'--expected-commit',SYNTHETIC,'--head',SYNTHETIC,'--expected-tree',conf['tree'],'--run-id',0,'--artifact-id',0,'--archive-sha256',conf['digest'] or h(archive)],fake_run)
   receipt=json.loads((d/'compiled-resource-verification.json').read_bytes());binding=json.loads((d/'artifact-source-binding.json').read_bytes());need(len(receipt['entries'])==256 and receipt['reviewed_entries_by_locale']==counts and receipt['new_reviewed_entries']==20 and receipt['prior_reviewed_entries']==236,'compiled receipt scope');need(binding['tracked_files']==1373 and binding['packaged_tracked_source_files_exact']==1370,'packaged receipt counts')
  record('apk','256 exact reviewed displays and 1370 packaged synthetic files',apk_case)
  for tag in expectations:
   record('apk',tag+' compiled value mismatch',lambda tag=tag:apk_case(lambda p,v,c:v[tag].__setitem__(next(iter(v[tag])),'changed synthetic wording')),True)
  record('apk','missing Catalan compiled value',lambda:apk_case(lambda p,v,c:v['ca'].pop(next(iter(v['ca'])))),True)
  for label,change in [('wrong archive digest',lambda p,v,c:c.update(digest='0'*64)),('wrong source tree',lambda p,v,c:c.update(tree='0'*40)),('wrong tracked count',lambda p,v,c:c.update(count=1372)),('missing tracked source file',lambda p,v,c:p.pop(next(iter(p)))),('changed packaged bytes',lambda p,v,c:p.__setitem__(next(iter(p)),b'changed')),('duplicate compiled locale value',lambda p,v,c:c.update(duplicate=True)),('missing v2 signature',lambda p,v,c:c.update(signature=False))]:record('apk',label,lambda change=change:apk_case(change),True)

  def regression_case(change=None):
   d=root/'regression-case';d.mkdir(exist_ok=True);entries={}
   for cls,tests in methods.items():
    doc=E.Element('testsuite',tests=str(len(tests)),failures='0',errors='0',skipped='0')
    for test in tests:E.SubElement(doc,'testcase',classname='org.catrobat.paintroid.local.'+cls,name=test,time='0.01')
    entries['app/build/test-results/testDebugUnitTest/TEST-org.catrobat.paintroid.local.'+cls+'.xml']=E.tostring(doc)
   entries['app/build/reports/lint-results-debug.xml']=b'<issues><issue severity="Warning"/></issues>'
   entries['build/reports/ci-phases/python.log']=b'\nRan 101 tests in 1.250s\n\nOK (skipped=2)\n'
   for phase in ['python','jvm','native','lint']:entries['build/reports/ci-phases/'+phase+'.time']=b'exit_status=0\n'
   conf={'digest':None}
   if change:change(entries,conf)
   raw=zipbytes(entries);(d/'regression-and-lint.zip').write_bytes(raw);invoke(scripts/'verify_regression_artifact.py',['--directory',d,'--source-root',src,'--head',SYNTHETIC,'--tested-commit',SYNTHETIC,'--run-id',0,'--artifact-id',0,'--sha256',conf['digest'] or h(raw)])
   receipt=json.loads((d/'hosted-regression-verification.json').read_bytes());need({x['class']:x['source_test_methods'] for x in receipt['focused_suites']}=={k:len(v) for k,v in methods.items()},'source driven suite counts');need(receipt['hosted_python']['run']==101 and receipt['hosted_python']['passed']==99 and receipt['hosted_python']['skipped']==2 and receipt['hosted_python']['skipped_identities'].startswith('Not named'),'explicit synthetic Python skips')
  record('regression','source-derived focused suites and explicit hosted Python skips',regression_case)
  first='app/build/test-results/testDebugUnitTest/TEST-org.catrobat.paintroid.local.CatalanRomanianSaveWordingTest.xml'
  def status(entries,conf,kind):
   doc=E.fromstring(entries[first]);E.SubElement(doc.find('testcase'),kind);doc.set({'failure':'failures','skipped':'skipped'}[kind],'1');entries[first]=E.tostring(doc)
  for label,change in [('wrong digest',lambda e,c:c.update(digest='0'*64)),('missing new suite',lambda e,c:e.pop(first)),('failed method',lambda e,c:status(e,c,'failure')),('skipped method',lambda e,c:status(e,c,'skipped')),('failed phase',lambda e,c:e.__setitem__('build/reports/ci-phases/jvm.time',b'exit_status=1\n')),('ambiguous Python summary',lambda e,c:e.__setitem__('build/reports/ci-phases/python.log',e['build/reports/ci-phases/python.log']*2))]:record('regression',label,lambda change=change:regression_case(change),True)
  def bad_method(e,c):
   doc=E.fromstring(e[first]);doc.find('testcase').set('name','notDeclared');e[first]=E.tostring(doc)
  record('regression','method not declared in source',lambda:regression_case(bad_method),True)

  def exact_case(change=None):
   d=root/'exact-case';d.mkdir(exist_ok=True);entries={};probes=[]
   for n in PROBES:
    log=('synthetic '+n+'\n').encode();entries[n+'.log']=log;negative=n=='06-reserved-app-variant-rejected';probes.append({'name':n,'exit_code':1 if negative else 0,'expected_success':not negative,'log_sha256':h(log)})
   summary={'commit':SYNTHETIC,'tree':SYNTHETIC,'success':True,'probes':probes};conf={'digest':None}
   if change:change(entries,summary,conf)
   entries['summary.json']=js(summary);raw=zipbytes(entries);(d/'exact-script.zip').write_bytes(raw);invoke(scripts/'verify_exact_script_artifact.py',['--directory',d,'--commit',SYNTHETIC,'--tree',SYNTHETIC,'--reviewed-pr-head',SYNTHETIC,'--run-id',0,'--artifact-id',0,'--sha256',conf['digest'] or h(raw)])
   need(json.loads((d/'exact-script-verification.json').read_bytes())['probe_count']==13,'exact receipt count')
  record('exact-script','13 synthetic probes including expected rejection',exact_case)
  for label,change in [('wrong digest',lambda e,s,c:c.update(digest='0'*64)),('wrong commit',lambda e,s,c:s.update(commit='0'*40)),('missing probe',lambda e,s,c:s['probes'].pop()),('unexpected exit',lambda e,s,c:s['probes'][0].update(exit_code=1)),('corrupt log',lambda e,s,c:e.__setitem__(PROBES[0]+'.log',b'corrupt'))]:record('exact-script',label,lambda change=change:exact_case(change),True)

  def api_case(change=None):
   d=root/'api-case';d.mkdir(exist_ok=True);extracted=d/'api35-revalidated'
   if extracted.exists():
    import shutil;shutil.rmtree(extracted)
   app_apk=b'synthetic app apk';sourcezip=b'synthetic source archive';testapk=b'synthetic test apk';(d/'app-debug.apk').write_bytes(app_apk);(d/'AN-Paint-source.zip').write_bytes(sourcezip);testzip=zipbytes({'app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk':testapk});(d/'instrumentation-apks.zip').write_bytes(testzip)
   identity={'commit':SYNTHETIC,'run_id':'0','build_variant':'debug','device_sdk':35,'source_tests_sha256':'2'*64,'apk_sha256':h(app_apk),'source_sha256':h(sourcezip),'test_apk_sha256':h(testapk),'group_run_attempts':{'core':1,'position':1},'composed_in_run_attempt':1}
   coverage={'selected_tests':1,'completed_tests':1,'completed':['synthetic-app-case'],'phases':['synthetic']};native={'cases':[{'classname':'synthetic.Native','name':'case','status':'passed'}],'expected_tests':1,'completed_tests':1,'source_tests_sha256':'2'*64,'success':True,'returncode':0,'timed_out':False,'device_sdk':35,'missing':[],'unexpected':[],'errors':[]};selection={'workflow_head':SYNTHETIC};conf={'digest':None,'testdigest':None}
   if change:change(identity,native,selection,conf)
   entries={'app/coverage.json':js(dict(coverage,device_identity=identity)),'composed-device-identity.json':js(identity),'Paintroid/androidTest-results/summary.json':js(native),'artifact-selection.json':js(selection)};raw=zipbytes(entries);(d/'api35-composed.zip').write_bytes(raw)
   appmod=types.ModuleType('app_instrumentation_matrix');appmod.verify_reports=lambda *args:copy.deepcopy(coverage);native_mod=types.ModuleType('run_android_instrumentation');native_mod.declared_tests=lambda *args,**kw:{('synthetic.Native','case')};native_mod.source_tests_sha256=lambda *args:'2'*64
   invoke(scripts/'verify_api35_artifact.py',['--directory',d,'--source-root',src,'--head',SYNTHETIC,'--tested-commit',SYNTHETIC,'--tree',SYNTHETIC,'--run-id',0,'--artifact-id',0,'--sha256',conf['digest'] or h(raw),'--test-apks-sha256',conf['testdigest'] or h(testzip)],modules={'app_instrumentation_matrix':appmod,'run_android_instrumentation':native_mod})
   need(json.loads((d/'api35-terminal-verification.json').read_bytes())['native_source_bound_completed']==1,'synthetic API receipt')
  record('api35','synthetic identity/case plumbing with stub coverage validators',api_case)
  for label,change in [('wrong digest',lambda i,n,s,c:c.update(digest='0'*64)),('wrong app APK hash',lambda i,n,s,c:i.update(apk_sha256='0'*64)),('wrong tested commit',lambda i,n,s,c:i.update(commit='0'*40)),('wrong workflow head',lambda i,n,s,c:s.update(workflow_head='0'*40)),('unexpected native case',lambda i,n,s,c:n['cases'][0].update(name='other')),('failed native case',lambda i,n,s,c:n['cases'][0].update(status='failed')),('wrong test APK archive',lambda i,n,s,c:c.update(testdigest='0'*64))]:record('api35',label,lambda change=change:api_case(change),True)

 a.out.mkdir(parents=True,exist_ok=True)
 script_hashes={n:h((scripts/n).read_bytes()) for n in ['verify_apk_artifact.py','verify_regression_artifact.py','verify_api35_artifact.py','verify_exact_script_artifact.py','test_artifact_verifiers.py']}
 receipt={'schema_version':1,'record_kind':'Synthetic artifact-verifier sanity controls; not hosted result evidence','source_head':PIN,'source_tree':TREE,'actual_source_blob_identities_verified':1373,'expected_packaged_tracked_count':1370,'packager_exclusions':EXCLUDED,'compiled_review_scope_by_locale':counts,'new_reviewed_scope':{'ca':10,'ro':10},'prior_reviewed_scope':{'da':78,'no':78,'nn':80},'total_compiled_review_scope':256,'source_derived_focused_method_counts':{k:len(v) for k,v in methods.items()},'scripts_sha256':script_hashes,'positive_controls':sum(x['outcome']=='accepted synthetic fixture' for x in controls),'negative_controls_rejected':sum(x['outcome']=='rejected' for x in controls),'controls':controls,'limits':['All archive contents, run/artifact IDs, APK/signature output and execution outcomes in these controls are synthetic.','API35 source-validator calls are stubbed here only to test artifact identity/case plumbing; actual artifact verification must call the real exact-head source validators.','No Android compilation, JVM/emulator execution, APK authenticity, hosted success or release acceptance is established by synthetic controls.','Hosted Python skip counts are carried explicitly, not promoted to passed or inferred from local tests.','No new linguistic acceptance or whole-locale/native-human/device/layout certification.']}
 raw=js(receipt);need(not re.search(rb'/tmp/|/workspace/|/root/|/home/agent/',raw),'public receipt path');(a.out/'artifact-verifier-sanity.json').write_bytes(raw);print(json.dumps({'positive':receipt['positive_controls'],'negative_rejected':receipt['negative_controls_rejected'],'receipt_sha256':h(raw),'scripts_sha256':script_hashes},indent=2))
if __name__=='__main__':main()
