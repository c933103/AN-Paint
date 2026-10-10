from pathlib import Path
import zipfile,xml.etree.ElementTree as ET,json,re,sys,hashlib,unittest
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT/'candidate';OUT=ROOT/'independent-review'
sys.path.insert(0,str(REPO/'tools'));from run_android_instrumentation import declared_tests,parse_protocol,verify_restart_reports
expected=json.loads((OUT/'expected-android-tests.json').read_text());result={}
def xml_cases(root):return [(x.attrib.get('classname'),x.attrib.get('name')) for x in root.findall('testcase')]
with zipfile.ZipFile(ROOT/'ci-artifacts/pr42-11666497670.zip') as z:
 assert len(z.namelist())==len(set(z.namelist()))
 xmls=[n for n in z.namelist() if '/test-results/testDebugUnitTest/TEST-' in n and n.endswith('.xml')]
 roots=[ET.fromstring(z.read(n)) for n in xmls]
 totals={k:sum(int(r.attrib.get(k,0)) for r in roots) for k in ['tests','failures','errors','skipped']}
 identities=[identity for r in roots for identity in xml_cases(r)]
 assert totals=={'tests':746,'failures':0,'errors':0,'skipped':0}
 assert len(identities)==len(set(identities))==746
 assert all(len(r.findall('testcase'))==int(r.attrib['tests']) for r in roots)
 assert not any(r.findall('.//'+tag) for r in roots for tag in ['failure','error','skipped'])
 selected=[]
 for path,methods in list(expected.items())[:2]:
  owner=Path(path).stem;class_name='org.catrobat.paintroid.local.'+owner
  member='Paintroid/build/test-results/testDebugUnitTest/TEST-'+class_name+'.xml'
  data=z.read(member);r=ET.fromstring(data);cases=xml_cases(r)
  assert set(cases)=={(class_name,method) for method in methods}
  assert len(cases)==len(methods)
  (OUT/Path(member).name).write_bytes(data)
  selected.append({'class':class_name,'tests':len(cases),'time':r.attrib['time'],'methods':sorted(m for _,m in cases),'all_passed':True})
 lint=ET.fromstring(z.read('app/build/reports/lint-results-debug.xml'));assert len(lint.findall('issue'))==0
 jvm=z.read('build/reports/ci-phases/jvm.log').decode();assert '> Task :Paintroid:compileDebugUnitTestKotlin' in jvm and '> Task :Paintroid:testDebugUnitTest' in jvm and 'BUILD SUCCESSFUL' in jvm
 python=z.read('build/reports/ci-phases/python.log').decode();assert 'Ran 371 tests' in python and 'OK (skipped=2)' in python
 suite=unittest.defaultTestLoader.discover(str(REPO/'tools'),pattern='test_*.py')
 def flat(s):
  for t in s:
   if isinstance(t,unittest.TestSuite):yield from flat(t)
   else:yield t
 ids=[t.id() for t in flat(suite)]
 progress=next(l for l in python.splitlines() if re.fullmatch('[.s]+',l))
 assert len(ids)==len(progress)==371
 skipped=[ids[i] for i,char in enumerate(progress) if char=='s']
 result['jvm']={'suite_count':len(xmls),**totals,'unique_testcase_identities':len(set(identities)),'selected_classes':selected,'compileDebugUnitTestKotlin_observed':True}
 result['lint']={'issues':0}
 result['python']={'total':371,'passed':369,'skipped':2,'skipped_identities_derived_from_exact_source_discovery_order':skipped,'qualification':'CI progress is nonverbose; identities reconstructed by matching all 371 ordered source cases to the progress characters. They are the two optional Pillow checks.'}
 for phase in ['python','jvm','lint']:
  (OUT/('pr42-'+phase+'.log')).write_bytes(z.read('build/reports/ci-phases/'+phase+'.log'))
with zipfile.ZipFile(ROOT/'ci-artifacts/pr42-11665559033.zip') as z:
 assert len(z.namelist())==len(set(z.namelist()))
 native_expected=declared_tests(REPO/'Paintroid/src/androidTest',sdk_level=35)
 app_expected=declared_tests(REPO/'app/src/androidTest',sdk_level=35)
 report_dirs=['Paintroid/androidTest-results','app/androidTest-results','app/accepted-credit-restart/seed','app/accepted-credit-restart/verify']
 summaries=[];xml_inventory=[]
 for directory in report_dirs:
  summary=json.loads(z.read(directory+'/summary.json'));summaries.append(summary)
  assert summary['device_sdk']==35 and summary['success'] and summary['returncode']==0 and not summary['timed_out']
  assert not summary['missing'] and not summary['unexpected'] and not summary['errors'] and not summary['sdk_suppressed_tests']
  allowed=(native_expected if directory.startswith('Paintroid/') else app_expected)
  allowed={x for x in allowed if x[0] not in summary['excluded_classes']}
  text=z.read(directory+'/instrumentation.log').decode()
  parsed=parse_protocol(text,allowed,returncode=0,timed_out=False)
  assert parsed['success'] and parsed['completed_tests']==len(allowed)
  got={(case['classname'],case['name']) for case in summary['cases']}
  assert got==allowed and all(case['status']=='passed' for case in summary['cases'])
  for n in z.namelist():
   if n.startswith(directory+'/TEST-') and n.endswith('.xml'):
    data=z.read(n);xml=ET.fromstring(data)
    assert set(xml_cases(xml))==allowed and len(xml_cases(xml))==len(allowed)
    assert int(xml.attrib['tests'])==len(allowed)
    assert all(int(xml.attrib[k])==0 for k in ['errors','failures','skipped'])
    assert not any(xml.findall('.//'+tag) for tag in ['failure','error','skipped'])
    (OUT/Path(n).name).write_bytes(data)
    xml_inventory.append({'path':n,'tests':len(allowed),'time':xml.attrib['time'],'all_passed':True})
 coverage=verify_restart_reports(app_expected,summaries[1:]);assert json.loads(json.dumps(coverage))==json.loads(z.read('app/accepted-credit-restart/coverage.json'))
 assert len(native_expected)==74 and len(app_expected)==20
 animation={('org.catrobat.paintroid.classic.AnimationImportTest',m) for m in expected['Paintroid/src/androidTest/java/org/catrobat/paintroid/classic/AnimationImportTest.kt']}
 assert animation<=native_expected
 all_cases=[(x['classname'],x['name']) for s in summaries for x in s['cases']]
 assert len(all_cases)==len(set(all_cases))==94
 images=[n for n in z.namelist() if n.lower().endswith(('.png','.jpg','.webp'))]
 result['api35']={'native_import_tests':74,'editor_tests_ordinary':18,'editor_tests_restart_seed':1,'editor_tests_restart_verify':1,'total_unique_passed':94,'all_declared_api35_methods_covered':True,'raw_protocols_reparsed_successfully':True,'animation_decoder_tests':sorted(m for _,m in animation),'junit_suites':xml_inventory,'image_artifacts':images,'title_visual_acceptance':False,'scope':'Installed API35 emulator execution. The four animation tests inspect metadata and decode first/default pixel; they do not display ImportSelection dialogs. Title assertions executed only in API33 Robolectric simulation.'}
(OUT/'pr42-test-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
