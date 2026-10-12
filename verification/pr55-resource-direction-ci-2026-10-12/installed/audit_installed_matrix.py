#!/usr/bin/env python3
"""Read-only independent reconciliation of both exact-source installed matrices."""
from audit_natural_artifacts import SOURCE_SHA,LIBRARY_SHA
import argparse,collections,hashlib,json,pathlib,subprocess,sys,xml.etree.ElementTree as E
from audit_natural_artifacts import TREE,HEAD,MERGE,RUN,require,sha

def main():
 p=argparse.ArgumentParser()
 for k in ('repo','artifact-root','output'):p.add_argument('--'+k,type=pathlib.Path,required=True)
 p.add_argument('--apis',type=int,nargs='+',choices=(30,35),default=[30,35])
 a=p.parse_args()
 for name in ('run_android_instrumentation.py','app_instrumentation_matrix.py','vertical_locale_matrix.py'):
  original=subprocess.check_output(['git','show',TREE+':tools/'+name],cwd=a.repo)
  require(original==(a.repo/'tools'/name).read_bytes(),'imported helper differs from exact tree '+name)
 sys.path.insert(0,str(a.repo/'tools'))
 from run_android_instrumentation import declared_tests,source_tests_sha256,parse_protocol
 from app_instrumentation_matrix import app_partition,report_paths,verify_app_reports,PHASE_TIMEOUTS,SELECTED_PHASES
 require(source_tests_sha256(a.repo/'app/src/androidTest')==SOURCE_SHA,'app source digest changed')
 require(source_tests_sha256(a.repo/'Paintroid/src/androidTest')==LIBRARY_SHA,'library source digest changed')
 out={}
 for sdk in a.apis:
  root=a.artifact_root/f'api{sdk}';appsrc=a.repo/'app/src/androidTest';libsrc=a.repo/'Paintroid/src/androidTest';app=declared_tests(appsrc,sdk_level=sdk);lib=declared_tests(libsrc,sdk_level=sdk)
  parts=app_partition(app,sdk);paths=report_paths(root,sdk);parts['library']=lib;paths['library']=root/'Paintroid/androidTest-results/summary.json'
  digests={k:source_tests_sha256(libsrc if k=='library' else appsrc) for k in parts};phases={};missing=[];cases=[];appreports={}
  for phase,wanted in parts.items():
   path=paths[phase]
   if not path.exists():missing.append({'phase':phase,'identities':[list(x) for x in sorted(wanted)]});continue
   summary=json.loads(path.read_bytes());raw=path.with_name('instrumentation.log');parsed=parse_protocol(raw.read_text(),wanted,returncode=summary['returncode'],timed_out=summary['timed_out'])
   for k,v in parsed.items():require(json.loads(json.dumps(v))==summary[k],'raw protocol/summary differs '+phase+' '+k)
   require(summary['source_tests_sha256']==digests[phase] and summary['device_sdk']==sdk,'phase source/SDK binding')
   suppressed=declared_tests(libsrc if phase=='library' else appsrc)-declared_tests(libsrc if phase=='library' else appsrc,sdk_level=sdk)
   require(summary['sdk_suppressed_tests']==[list(x) for x in sorted(suppressed)],'SDK suppression differs')
   require(summary['timeout_seconds']==(180 if phase=='library' else PHASE_TIMEOUTS[phase]),'timeout changed')
   require(type(summary['timed_out']) is bool and isinstance(summary['elapsed_seconds'],(int,float)) and summary['elapsed_seconds']>=0,'invalid phase timing')
   require(summary['included_tests']==(sorted(f'{c}#{n}' for c,n in wanted) if phase in SELECTED_PHASES else []),'selector differs')
   require(summary['leave_target_running'] is (phase=='seed'),'target lifetime differs')
   ids=[(x['classname'],x['name']) for x in summary['cases']];require(len(ids)==len(set(ids)) and set(ids)<=wanted,'phase identities duplicate/extra')
   xmls=list(path.parent.glob('TEST-*.xml'));require(len(xmls)==1,'XML inventory');xml=E.fromstring(xmls[0].read_bytes());xc=xml.findall('testcase');require(xml.tag=='testsuite' and len(xc)==len(xml.findall('.//testcase')) and int(xml.get('tests'))==len(xc),'XML structure/count')
   require(collections.Counter((x.get('classname'),x.get('name')) for x in xc)==collections.Counter(ids),'XML identities differ')
   statuses={i:(next((tag for tag in ('failure','error','skipped') if x.find(tag) is not None),'passed')) for i,x in zip([(x.get('classname'),x.get('name')) for x in xc],xc)}
   for c in summary['cases']:require(statuses[(c['classname'],c['name'])]==c['status'],'XML/protocol status differs')
   for field,tag in [('failures','failure'),('errors','error'),('skipped','skipped')]:require(int(xml.get(field))==sum(v==tag for v in statuses.values()),'XML status count differs')
   failures=[c for c in summary['cases'] if c['status']!='passed'];cases.extend(summary['cases'])
   phases[phase]={'completed':len(ids),'passed':len(ids)-len(failures),'failures':failures,'raw_sha256':sha(raw.read_bytes()),'summary_sha256':sha(path.read_bytes()),'xml_sha256':sha(xmls[0].read_bytes()),'elapsed_seconds':summary['elapsed_seconds'],'success':summary['success'],'missing_identities':[list(x) for x in sorted(wanted-set(ids))],'runner_errors':summary['errors'],'returncode':summary['returncode'],'timed_out':summary['timed_out']}
   if phase!='library':appreports[phase]=summary
  allwanted=set.union(*parts.values());allids=[(c['classname'],c['name']) for c in cases];require(len(allids)==len(set(allids)),'matrix duplicates')
  excluded=(app|lib)-allwanted
  require(allwanted <= app|lib,'selected identities outside eligible source')
  require(sum(map(len,parts.values()))==len(allwanted),'overlapping selected phase identities')
  expected_summary_paths=set(paths.values()); actual_summary_paths=set(root.rglob('summary.json'))
  require(actual_summary_paths<=expected_summary_paths,'unexpected phase summaries')
  app_passed=all(k in phases and phases[k]['success'] is True for k in parts if k!='library')
  matrix_passed=not missing and all(x['success'] is True for x in phases.values()) and len(cases)==len(allwanted) and all(c['status']=='passed' for c in cases)
  if app_passed:
   union=verify_app_reports(app,sdk,appreports,source_tests_sha256(appsrc),declared_tests(appsrc)-app)
   for name in ('coverage.json','ordinary-gallery-coverage.json','vertical-coverage.json', *(['accepted-credit-restart/coverage.json'] if sdk==35 else [])):require(json.loads((root/'app'/name).read_bytes())==json.loads(json.dumps(union)),'coverage union differs')
  else:
   require(not any((root/'app'/name).exists() for name in ('coverage.json','ordinary-gallery-coverage.json','vertical-coverage.json','accepted-credit-restart/coverage.json')),'failed matrix retained a successful coverage union')
  out[str(sdk)]={'status':'PASS' if matrix_passed else 'FAIL','source_digests':{'app':source_tests_sha256(appsrc),'library':source_tests_sha256(libsrc)},'sdk_eligible_declarations':len(app)+len(lib),'explicitly_excluded_tests':[list(x) for x in sorted(excluded)],'scheduled_identities':[list(x) for x in sorted(allwanted)],'scheduled':len(allwanted),'completed':len(cases),'passed':sum(c['status']=='passed' for c in cases),'failed':sum(c['status']!='passed' for c in cases),'missing_phases':missing,'phases':phases}
 result={'audit_integrity_status':'PASS','installed_gate_status':'PASS' if all(m['status']=='PASS' for m in out.values()) else 'FAIL','head':HEAD,'merge':MERGE,'tree':TREE,'run_id':RUN,'matrices':out,'scope':'Read-only exact-source selector/digest, raw protocol, summary, XML and matrix reconciliation. ZIP and APK provenance are separate bound reviews; Successful phases cannot substitute for failed or missing methods.'}
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({sdk:{k:v for k,v in d.items() if k not in ('phases','source_digests','scheduled_identities')} for sdk,d in out.items()},indent=2))
if __name__=='__main__':main()
