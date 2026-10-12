import copy,hashlib,json,os,pathlib,shutil,subprocess,sys,xml.etree.ElementTree as E
R=pathlib.Path(__file__).parent;checkout=R/'checkout';sys.path.insert(0,str(checkout/'tools'))
from run_android_instrumentation import declared_tests,source_tests_sha256,parse_protocol
from app_instrumentation_matrix import app_partition,report_paths,verify_app_reports,PHASE_TIMEOUTS,SELECTED_PHASES
source=checkout/'app/src/androidTest';expected=declared_tests(source,sdk_level=35);parts=app_partition(expected,35);digest=source_tests_sha256(source);parts['native']=declared_tests(checkout/'Paintroid/src/androidTest',sdk_level=35)
fixture=R/'installed-positive';fixture.mkdir(exist_ok=True);paths=report_paths(fixture,35);paths['native']=fixture/'Paintroid/androidTest-results/summary.json';reports={}
for phase,wanted in parts.items():
 path=paths[phase];path.parent.mkdir(parents=True,exist_ok=True);raw=''
 for c,m in sorted(wanted):
  for code in [1,0]:raw+=f'INSTRUMENTATION_STATUS: class={c}\nINSTRUMENTATION_STATUS: test={m}\nINSTRUMENTATION_STATUS: numtests={len(wanted)}\nINSTRUMENTATION_STATUS_CODE: {code}\n'
 raw+='INSTRUMENTATION_CODE: -1\n';(path.parent/'instrumentation.log').write_text(raw)
 report=parse_protocol(raw,wanted);report.update(device_sdk=35,source_tests_sha256=source_tests_sha256(checkout/'Paintroid/src/androidTest') if phase=='native' else digest,sdk_suppressed_tests=[],excluded_classes=[],included_tests=sorted(f'{c}#{m}' for c,m in wanted) if phase in SELECTED_PHASES else [],timeout_seconds=PHASE_TIMEOUTS.get(phase,180),leave_target_running=phase=='seed',elapsed_seconds=1.0)
 path.write_text(json.dumps(report));reports[phase]=report
 xml=E.Element('testsuite',tests=str(len(wanted)),errors='0',failures='0',skipped='0',time='1.0')
 for c,m in sorted(wanted):E.SubElement(xml,'testcase',classname=c,name=m,time='0.01')
 (path.parent/'TEST-synthetic.xml').write_bytes(E.tostring(xml))
union=verify_app_reports(expected,35,{k:v for k,v in reports.items() if k!='native'},digest,set())
for name in ['app/coverage.json','app/ordinary-gallery-coverage.json','app/vertical-coverage.json','app/accepted-credit-restart/coverage.json']:(fixture/name).write_text(json.dumps(union))
controls=[]
for case in ['positive-protocol-xml','malformed-xml-root','xml-count-mismatch','negative-elapsed','raw-protocol-failure','wrong-coverage','optimized-mode']:
 root=R/('installed-'+case)
 if root.exists():shutil.rmtree(root)
 shutil.copytree(fixture,root)
 target=root/'Paintroid/androidTest-results/TEST-synthetic.xml'
 if case in ['malformed-xml-root','xml-count-mismatch']:
  tree=E.parse(target);x=tree.getroot()
  if case=='malformed-xml-root':x.tag='not-a-junit-report'
  else:x.set('tests','0');x.set('errors','999')
  tree.write(target)
 if case=='negative-elapsed':
  path=root/'Paintroid/androidTest-results/summary.json';data=json.loads(path.read_text());data['elapsed_seconds']=-100.0;path.write_text(json.dumps(data))
 if case=='raw-protocol-failure':
  path=root/'Paintroid/androidTest-results/instrumentation.log';path.write_text(path.read_text().replace('INSTRUMENTATION_STATUS_CODE: 0','INSTRUMENTATION_STATUS_CODE: -2',1))
 if case=='wrong-coverage':(root/'app/coverage.json').write_text('{}')
 output=R/'candidate-installed-verification.json';output.unlink(missing_ok=True);env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
 cmd=[sys.executable,*(['-O'] if case=='optimized-mode' else []),str(R/'original-verify_installed.py'),str(root)]
 run=subprocess.run(cmd,capture_output=True,text=True,env=env);(R/('installed-'+case+'.stdout.log')).write_text(run.stdout);(R/('installed-'+case+'.stderr.log')).write_text(run.stderr)
 if output.exists():shutil.copy2(output,R/('installed-'+case+'.json'))
 controls.append(dict(case=case,command=cmd,exit=run.returncode,output_created=output.exists()))
print(json.dumps(controls,indent=2));(R/'installed-negative-control-results.json').write_text(json.dumps(dict(helper_sha256=hashlib.sha256((R/'original-verify_installed.py').read_bytes()).hexdigest(),controls=controls),indent=2)+'\n')
