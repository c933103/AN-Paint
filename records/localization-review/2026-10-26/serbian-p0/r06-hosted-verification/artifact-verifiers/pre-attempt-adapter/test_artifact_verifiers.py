#!/usr/bin/env python3
"""Synthetic verifier plumbing controls only; never hosted build/runtime evidence."""
import argparse, collections, contextlib, copy, hashlib, io, json, re, runpy, sys, tempfile, types, zipfile
from pathlib import Path
from prepare_source_expectations import tree_hash
from unittest.mock import patch
import xml.etree.ElementTree as E

SYNTHETIC='1'*40
CLASSES=['SerbianP0WordingTest','SlovakSlovenianP0WordingTest','NumericDisplayLocaleTest','CatalanRomanianCompletionWordingTest','CatalanRomanianImportWordingTest','CatalanRomanianSaveWordingTest','DanishNorwegianP0Test','NynorskRemainingP0Test','NynorskSaveWordingTest','DerivedExportStateTest','ImportSelectionTitleTest','TaggedColourImportTest']
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
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--tree-file',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--expected-tree',required=True);p.add_argument('--source-head');a=p.parse_args();scripts=Path(__file__).parent;controls=[]
 tree=json.loads(a.tree_file.read_bytes());need(tree['sha']==a.expected_tree and tree.get('truncated') is False,'pinned tree');blobs=[x for x in tree['tree'] if x['type']=='blob'];need(bool(blobs) and len({x['path'] for x in blobs})==len(blobs) and tree_hash(blobs)[0]==a.expected_tree,'actual tracked source inventory/tree hash');tracked_count=len(blobs)
 for x in blobs:need(git((a.source_root/x['path']).read_bytes())==x['sha'],'actual source byte binding')
 methods={};source_files={}
 for rel in ['gradle/wrapper/gradle-wrapper.properties','build.gradle']:
  source_files[rel]=(a.source_root/rel).read_bytes()
 for folder in ['Paintroid/src/main/res/values-b+ko+Kore+KR','Paintroid/src/main/res/values-b+qaa+Zsye+XV']:
  for path in (a.source_root/folder).glob('*.xml'):source_files[path.relative_to(a.source_root).as_posix()]=path.read_bytes()
 for cls in CLASSES:
  path=f'Paintroid/src/test/java/org/catrobat/paintroid/local/{cls}.kt';raw=(a.source_root/path).read_bytes();source_files[path]=raw;matches=re.findall(r'@Test\s+(?:@[\w.]+(?:\([^()]*\))?\s+)*fun\s+([A-Za-z0-9_]+)\s*\(',raw.decode());need(len(set(matches))==len(matches)==len(re.findall(r'@Test\b',raw.decode())),'test source method parsing');methods[cls]=matches
 need(len(methods['SerbianP0WordingTest'])==8 and len(methods['SlovakSlovenianP0WordingTest'])==8 and len(methods['NumericDisplayLocaleTest'])==6 and len(methods['CatalanRomanianCompletionWordingTest'])==5 and len(methods['CatalanRomanianImportWordingTest'])==2 and len(methods['CatalanRomanianSaveWordingTest'])==2 and len(methods['DerivedExportStateTest'])==7 and len(methods['ImportSelectionTitleTest'])==12,'new test scope')
 expectations={tag:{} for tag in ('ca','ro','da','no','nn','sk','sl','sr-Cyrl','sr-Latn')}
 fixtures={'serbian_p0_wording.json':('sr-Cyrl','sr-Latn'),'slovak_slovenian_p0_wording.json':('sk','sl'),'catalan_romanian_completion_wording.json':('ca','ro'),'catalan_romanian_import_wording.json':('ca','ro'),'catalan_romanian_save_wording.json':('ca','ro'),'danish_norwegian_p0_wording.json':('da','no'),'nynorsk_p0_remaining_wording.json':('nn',),'nynorsk_save_wording.json':('nn',)}
 for name,tags in fixtures.items():
  path='tools/fixtures/current_localization/'+name;raw=(a.source_root/path).read_bytes();source_files[path]=raw
  for key,values in json.loads(raw)['values'].items():
   for tag in tags:
    value=values[tag];need(value[0]==value[-1]=='"' and '\\' not in value and key not in expectations[tag],'fixture display scope');expectations[tag][key]=value[1:-1]
 for fname in ('slovak_slovenian_p0_wording.json','serbian_p0_wording.json'):
  for tag,values in json.loads(source_files['tools/fixtures/current_localization/'+fname])['preserved_values'].items():
   for key,value in values.items():
    text=value['value'];need('\\' not in text and key not in expectations[tag],'inherited fixture display/overlap')
    expectations[tag][key]=text[1:-1] if text.startswith('"') and text.endswith('"') else text
 counts={k:len(v) for k,v in expectations.items()};need(counts=={'ca':78,'ro':78,'da':78,'no':78,'nn':80,'sk':205,'sl':205,'sr-Cyrl':244,'sr-Latn':242},'compiled fixture counts')
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
  for i in range(tracked_count-len(source_files)-len(EXCLUDED)):
   q=src/f'synthetic/item-{i:04d}.txt';q.parent.mkdir(exist_ok=True);q.write_bytes(f'synthetic source {i}\n'.encode())
  synthetic_blobs=[{'path':str(q.relative_to(src)),'type':'blob','mode':'100644','sha':git(q.read_bytes())} for q in sorted(src.rglob('*')) if q.is_file()];need(len(synthetic_blobs)==tracked_count,'synthetic source inventory');synthetic_tree=tree_hash(synthetic_blobs)[0]
  treefile=root/'tree.json';treefile.write_bytes(js({'sha':synthetic_tree,'truncated':False,'tree':synthetic_blobs}))
  toolroot=root/'tools';toolroot.mkdir();(toolroot/'aapt2').write_bytes(b'synthetic tool, not executable');(toolroot/'apksigner.jar').write_bytes(b'synthetic signer, not executable')
  def resources(values,aliases=None):
   lines=[]
   for i,key in enumerate(sorted({k for v in values.values() for k in v})):
    lines.append(f'  resource 0x7f{i:06x} string/{key}')
    for tag,v in values.items():
     if key in v:
      qualifier=(aliases or {}).get(tag,{'sr-Cyrl':'b+sr+Cyrl','sr-Latn':'b+sr+Latn'}.get(tag,tag))
      value=v[key];compiled=value['quoted_literal'] if isinstance(value,dict) else value
      rendered=json.dumps(compiled,ensure_ascii=False) if isinstance(value,dict) or not compiled.startswith('@string/') else compiled
      lines.append('    ('+qualifier+') '+rendered)
    if key in values.get('sr-Cyrl',{}):lines.append('    (sr) '+json.dumps('generic library Serbian is not the project script catalogue'))
   return '\n'.join(lines)+'\n'
  def apk_case(change=None):
   d=root/'apk-case';d.mkdir(exist_ok=True);packaged={'AN-Paint/'+x['path']:(src/x['path']).read_bytes() for x in synthetic_blobs if x['path'] not in EXCLUDED};values=copy.deepcopy(expectations);conf={'tree':synthetic_tree,'digest':None,'signature':True,'duplicate':False,'count':tracked_count,'badmode':False,'config_aliases':{},'duplicate_serbian':False}
   if change:change(packaged,values,conf)
   sourcezip=zipbytes(packaged)
   if conf['badmode']:
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w') as changed:
     for n,b in packaged.items():
      info=zipfile.ZipInfo(n);info.external_attr=0o100755<<16;changed.writestr(info,b)
    sourcezip=buffer.getvalue()
   apk=zipbytes({'assets/local-source/AN-Paint-source.zip':sourcezip});info={'commit':SYNTHETIC,'run_id':0,'apk_sha256':h(apk),'source_sha256':h(sourcezip)};archive=zipbytes({'app/build/outputs/apk/debug/app-debug.apk':apk,'build/delivery/AN-Paint-source.zip':sourcezip,'build/delivery/build-info.json':js(info)});(d/'apk-and-source.zip').write_bytes(archive)
   treefile.write_bytes(js({'sha':synthetic_tree,'truncated':False,'tree':synthetic_blobs[:conf['count']]}))
   def fake_run(cmd,stdout,**kw):
    if cmd[0]==str(toolroot/'aapt2'):
     out=resources(values,conf['config_aliases'])
     if conf['duplicate_serbian']:
      key=next(iter(values['sr-Cyrl']));out+='  resource 0x7ff00001 string/'+key+'\n    (b+sr+Cyrl) '+json.dumps(values['sr-Cyrl'][key],ensure_ascii=False)+'\n'
     if conf['duplicate']:out+='  resource 0x7ff00000 string/'+next(iter(values['ca']))+'\n    (ca) '+json.dumps(next(iter(values['ca'].values())))+'\n'
     stdout.write(out)
    else:stdout.write('Verifies\nVerified using v1 scheme (JAR signing): true\nVerified using v2 scheme (APK Signature Scheme v2): '+str(conf['signature']).lower()+'\nSigner #1 certificate SHA-256 digest: '+'0'*64+'\n')
   invoke(scripts/'verify_apk_artifact.py',['--directory',d,'--source-root',src,'--tree-file',treefile,'--tools',toolroot,'--expected-commit',SYNTHETIC,'--head',SYNTHETIC,'--expected-tree',conf['tree'],'--run-id',0,'--artifact-id',0,'--archive-sha256',conf['digest'] or h(archive)],fake_run)
   receipt=json.loads((d/'compiled-resource-verification.json').read_bytes());binding=json.loads((d/'artifact-source-binding.json').read_bytes());need(len(receipt['entries'])==1288 and receipt['compiled_entries_by_locale']==counts and receipt['new_reviewed_entries']==148 and receipt['prior_reviewed_entries']==548 and receipt['inherited_entries']==592 and receipt['SK_SL_new_inherited_keys_disjoint'] is True and receipt['new_reviewed_entries_by_locale']=={'sr-Cyrl':74,'sr-Latn':74} and receipt['prior_reviewed_entries_by_locale']=={'ca':78,'ro':78,'da':78,'no':78,'nn':80,'sk':78,'sl':78},'compiled receipt scope');need(collections.Counter(e['scope'] for e in receipt['entries'])=={'new bounded Serbian review':148,'prior bounded review':548,'inherited preservation only':592},'compiled per-entry scope classification');need([(e['locale'],e['identity'],e['compiled_reference']) for e in receipt['entries'] if e['compiled_reference']] == [('sr-Cyrl','string/ui_save_a5d0d9','ui_save'),('sr-Latn','string/ui_save_a5d0d9','ui_save')],'exact inherited Serbian aliases');need(binding['tracked_files']==tracked_count and binding['packaged_tracked_source_files_exact']==tracked_count-3 and binding['tracked_executable_modes_match'] is True,'packaged receipt counts/modes')
  record('apk','1288 exact new/prior/inherited displays with generic Serbian deliberately ignored and tree-bound packaged synthetic files',apk_case)
  for tag in expectations:
   record('apk',tag+' compiled value mismatch',lambda tag=tag:apk_case(lambda p,v,c:v[tag].__setitem__(next(iter(v[tag])),'changed synthetic wording')),True)
  for tag in ('sk','sl','sr-Cyrl','sr-Latn'):
   fname='serbian_p0_wording.json' if tag.startswith('sr-') else 'slovak_slovenian_p0_wording.json'
   prior_key=next(iter(json.loads(source_files['tools/fixtures/current_localization/'+fname])['preserved_values'][tag]))
   record('apk',tag+' inherited display mismatch',lambda tag=tag,key=prior_key:apk_case(lambda p,v,c:v[tag].__setitem__(key,'forged inherited wording')),True)
  for label,change in [
   ('generic sr must not substitute for explicit Cyrillic',lambda p,v,c:c['config_aliases'].update({'sr-Cyrl':'sr'})),
   ('generic sr must not substitute for explicit Latin',lambda p,v,c:c['config_aliases'].update({'sr-Latn':'sr'})),
   ('Cyrillic and Latin configuration swap',lambda p,v,c:c['config_aliases'].update({'sr-Cyrl':'b+sr+Latn','sr-Latn':'b+sr+Cyrl'})),
   ('missing explicit Cyrillic configuration',lambda p,v,c:v['sr-Cyrl'].clear()),
   ('missing explicit Latin configuration',lambda p,v,c:v['sr-Latn'].clear()),
   ('duplicate explicit Serbian configuration value',lambda p,v,c:c.update(duplicate_serbian=True))]:
   record('apk',label,lambda change=change:apk_case(change),True)
  for label,change in [
   ('Serbian symbolic alias target changed',lambda p,v,c:v['sr-Cyrl'].__setitem__('ui_save_a5d0d9','@string/ui_cancel')),
   ('Serbian alias replaced by quoted literal lookalike',lambda p,v,c:v['sr-Cyrl'].__setitem__('ui_save_a5d0d9',{'quoted_literal':'@string/ui_save'})),
   ('Serbian alias target omitted',lambda p,v,c:v['sr-Latn'].pop('ui_save')),
   ('Serbian alias changed to direct display',lambda p,v,c:v['sr-Latn'].__setitem__('ui_save_a5d0d9',v['sr-Latn']['ui_save'])),
   ('Serbian alias cycle rejected',lambda p,v,c:v['sr-Cyrl'].__setitem__('ui_save','@string/ui_save_a5d0d9'))]:
   record('apk',label,lambda change=change:apk_case(change),True)
  record('apk','missing Catalan compiled value',lambda:apk_case(lambda p,v,c:v['ca'].pop(next(iter(v['ca'])))),True)
  for label,change in [('wrong archive digest',lambda p,v,c:c.update(digest='0'*64)),('wrong source tree',lambda p,v,c:c.update(tree='0'*40)),('wrong tracked count',lambda p,v,c:c.update(count=tracked_count-1)),('missing tracked source file',lambda p,v,c:p.pop(next(iter(p)))),('changed packaged bytes',lambda p,v,c:p.__setitem__(next(iter(p)),b'changed')),('duplicate compiled locale value',lambda p,v,c:c.update(duplicate=True)),('missing v2 signature',lambda p,v,c:c.update(signature=False)),('wrong packaged executable modes',lambda p,v,c:c.update(badmode=True))]:record('apk',label,lambda change=change:apk_case(change),True)

  def overlap_case():
   # Isolate the same production expectation builder without invoking artifact main.
   import ast
   tree=ast.parse((scripts/'verify_apk_artifact.py').read_text())
   definitions=ast.Module(body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef))],type_ignores=[])
   namespace={};exec(compile(definitions,'synthetic-expectation-helper','exec'),namespace)
   path=src/'tools/fixtures/current_localization/catalan_romanian_import_wording.json';original=path.read_bytes();data=json.loads(original)
   save=json.loads((src/'tools/fixtures/current_localization/catalan_romanian_save_wording.json').read_bytes())
   data['values'][next(iter(save['values']))]=data['values'].pop(next(iter(data['values'])))
   try:
    path.write_bytes(js(data));namespace['reviewed_expectations'](src)
   finally:path.write_bytes(original)
  record('apk','overlapping CA/RO import and prior Save keys',overlap_case,True)

  def completion_overlap_case():
   import ast
   tree=ast.parse((scripts/'verify_apk_artifact.py').read_text())
   definitions=ast.Module(body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef))],type_ignores=[])
   namespace={};exec(compile(definitions,'synthetic-completion-expectation-helper','exec'),namespace)
   path=src/'tools/fixtures/current_localization/catalan_romanian_completion_wording.json';original=path.read_bytes();data=json.loads(original)
   prior=json.loads((src/'tools/fixtures/current_localization/catalan_romanian_import_wording.json').read_bytes())
   data['values'][next(iter(prior['values']))]=data['values'].pop(next(iter(data['values'])))
   try:
    path.write_bytes(js(data));namespace['reviewed_expectations'](src)
   finally:path.write_bytes(original)
  record('apk','overlapping CA/RO completion and prior import keys',completion_overlap_case,True)

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
  first='app/build/test-results/testDebugUnitTest/TEST-org.catrobat.paintroid.local.SerbianP0WordingTest.xml'
  def status(entries,conf,kind):
   doc=E.fromstring(entries[first]);E.SubElement(doc.find('testcase'),kind);doc.set({'failure':'failures','skipped':'skipped'}[kind],'1');entries[first]=E.tostring(doc)
  for label,change in [('wrong digest',lambda e,c:c.update(digest='0'*64)),('missing new suite',lambda e,c:e.pop(first)),('failed method',lambda e,c:status(e,c,'failure')),('skipped method',lambda e,c:status(e,c,'skipped')),('failed phase',lambda e,c:e.__setitem__('build/reports/ci-phases/jvm.time',b'exit_status=1\n')),('ambiguous Python summary',lambda e,c:e.__setitem__('build/reports/ci-phases/python.log',e['build/reports/ci-phases/python.log']*2))]:record('regression',label,lambda change=change:regression_case(change),True)
  def bad_method(e,c):
   doc=E.fromstring(e[first]);doc.find('testcase').set('name','notDeclared');e[first]=E.tostring(doc)
  record('regression','method not declared in source',lambda:regression_case(bad_method),True)
  record('regression','missing completion suite',lambda:regression_case(lambda e,c:e.pop('app/build/test-results/testDebugUnitTest/TEST-org.catrobat.paintroid.local.CatalanRomanianCompletionWordingTest.xml')),True)
  record('regression','missing numeric display suite',lambda:regression_case(lambda e,c:e.pop('app/build/test-results/testDebugUnitTest/TEST-org.catrobat.paintroid.local.NumericDisplayLocaleTest.xml')),True)

  def exact_case(change=None):
   d=root/'exact-case';d.mkdir(exist_ok=True);entries={};probes=[]
   mirrors={};mutated={}
   for i,(folder,qualifier) in enumerate([('Paintroid/src/main/res/values-b+ko+Kore+KR','values-b+ko+Kore+KR+anpaint'),('Paintroid/src/main/res/values-b+qaa+Zsye+XV','values-b+en+Zsye+XV+anpaint')],1):
    paths=sorted((src/folder).glob('*.xml'))
    for path in paths:mirrors[qualifier+'/'+path.name]=h(path.read_bytes())
    mutated[i]=(qualifier+'/'+paths[0].name,h(paths[0].read_bytes()+b'\n<!-- isolated incremental resource probe -->\n'))
   fallback_hashes={'values/source_text.xml':'3'*64,'values/source_text_contracts.xml':'4'*64}
   for n in PROBES:
    negative=n=='06-reserved-app-variant-rejected';tasks=[];extra={};gen=':Paintroid:generateExactScriptResources';fallback=':Paintroid:generateSourceTextResources';debug=':Paintroid:mergeDebugResources';release=':Paintroid:mergeReleaseResources'
    if n=='03-unchanged':tasks=[[gen,' UP-TO-DATE'],[fallback,' UP-TO-DATE']]
    elif negative:tasks=[[fallback,' FAILED']]
    elif n in ['01-clean','06-second-clean']:tasks=[[':Paintroid:clean','']]
    else:
     consumers=[debug,release] if n=='02-clean-debug-release' else [release if ('release' in n or n=='05-source-companion-removed') else debug]
     if not n.startswith('05-source-'):
      hashes=dict(mirrors)
      if n.startswith('04-'):
       key,value=mutated[int(n[3])];hashes[key]=value
      extra['generated_sha256']=hashes;tasks.append([gen,''])
     if n in ['02-clean-debug-release','07-release-first-after-clean'] or n.startswith('05-source-'):
      extra['source_text_sha256']=dict(fallback_hashes) if n!='05-source-companion-added' else {k:'5'*64 for k in fallback_hashes};tasks.append([fallback,''])
     tasks.extend([[c,''] for c in consumers])
    log=(''.join('> Task '+name+state+'\n' for name,state in tasks)+('Reserved source-text name source_namespace_probe.xml\n' if negative else '')).encode();entries[n+'.log']=log
    probes.append(dict(name=n,exit_code=1 if negative else 0,expected_success=not negative,log_sha256=h(log),tasks=tasks,**extra))
   summary={'commit':SYNTHETIC,'tree':SYNTHETIC,'success':True,'probes':probes,'wrapper_sha256':h((src/'gradle/wrapper/gradle-wrapper.properties').read_bytes()),'root_build_sha256':h((src/'build.gradle').read_bytes()),'excluded_task':':Paintroid:bundleCorrespondingSource'};conf={'digest':None}
   if change:change(entries,summary,conf)
   entries['summary.json']=js(summary);raw=zipbytes(entries);(d/'exact-script.zip').write_bytes(raw);invoke(scripts/'verify_exact_script_artifact.py',['--source-root',src,'--directory',d,'--commit',SYNTHETIC,'--tree',SYNTHETIC,'--reviewed-pr-head',SYNTHETIC,'--run-id',0,'--artifact-id',0,'--sha256',conf['digest'] or h(raw)])
   need(json.loads((d/'exact-script-verification.json').read_bytes())['probe_count']==13,'exact receipt count')
  record('exact-script','13 synthetic probes including expected rejection',exact_case)
  for label,change in [('wrong digest',lambda e,s,c:c.update(digest='0'*64)),('wrong commit',lambda e,s,c:s.update(commit='0'*40)),('missing probe',lambda e,s,c:s['probes'].pop()),('unexpected exit',lambda e,s,c:s['probes'][0].update(exit_code=1)),('corrupt log',lambda e,s,c:e.__setitem__(PROBES[0]+'.log',b'corrupt')),('forged wrapper source hash',lambda e,s,c:s.update(wrapper_sha256='0'*64)),('forged generated mirror hash',lambda e,s,c:s['probes'][1]['generated_sha256'].update({'forged.xml':'0'*64})),('forged restored fallback hash',lambda e,s,c:s['probes'][-1]['source_text_sha256'].update({'values/source_text.xml':'0'*64})),('forged task ordering receipt',lambda e,s,c:s['probes'][1]['tasks'].reverse())]:record('exact-script',label,lambda change=change:exact_case(change),True)

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
 script_hashes={n:h((scripts/n).read_bytes()) for n in ['verify_apk_artifact.py','verify_regression_artifact.py','verify_api35_artifact.py','verify_exact_script_artifact.py','exact_generation_contract.py','prepare_source_expectations.py','test_artifact_verifiers.py']}
 receipt={'schema_version':1,'record_kind':'Synthetic artifact-verifier sanity controls; not hosted result evidence','source_head':a.source_head,'source_tree':a.expected_tree,'source_head_binding_status':'explicit head argument' if a.source_head else 'staged source tree only; no published head supplied','actual_source_blob_identities_verified':tracked_count,'expected_packaged_tracked_count':tracked_count-3,'packager_exclusions':EXCLUDED,'compiled_review_scope_by_locale':counts,'new_reviewed_scope':{'sr-Cyrl':74,'sr-Latn':74},'prior_reviewed_scope':{'ca':78,'ro':78,'da':78,'no':78,'nn':80,'sk':78,'sl':78},'inherited_preservation_scope':{'sk':127,'sl':127,'sr-Cyrl':170,'sr-Latn':168},'SK_SL_new_inherited_keys_disjoint':True,'Serbian_new_inherited_keys_disjoint':True,'explicit_Serbian_configuration_qualifiers':{'sr-Cyrl':'b+sr+Cyrl','sr-Latn':'b+sr+Latn'},'total_compiled_check_scope':1288,'source_derived_focused_method_counts':{k:len(v) for k,v in methods.items()},'scripts_sha256':script_hashes,'positive_controls':sum(x['outcome']=='accepted synthetic fixture' for x in controls),'negative_controls_rejected':sum(x['outcome']=='rejected' for x in controls),'controls':controls,'limits':['All archive contents, run/artifact IDs, APK/signature output and execution outcomes in these controls are synthetic.','API35 source-validator calls are stubbed here only to test artifact identity/case plumbing; actual artifact verification must call the real exact-head source validators.','No Android compilation, JVM/emulator execution, APK authenticity, hosted success or release acceptance is established by synthetic controls.','Hosted Python skip counts are carried explicitly, not promoted to passed or inferred from local tests.','No new linguistic acceptance or whole-locale/native-human/device/layout certification.']}
 raw=js(receipt);need(not re.search(rb'/tmp/|/workspace/|/root/|/home/agent/',raw),'public receipt path');(a.out/'artifact-verifier-sanity.json').write_bytes(raw);print(json.dumps({'positive':receipt['positive_controls'],'negative_rejected':receipt['negative_controls_rejected'],'receipt_sha256':h(raw),'scripts_sha256':script_hashes},indent=2))
if __name__=='__main__':main()
