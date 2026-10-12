#!/usr/bin/env python3
"""Read-only independent reconciliation of both exact-source installed matrices."""
import argparse,collections,hashlib,json,pathlib,subprocess,sys,xml.etree.ElementTree as E
from forensic_installed_ink import TREE,HEAD,MERGE,RUN,require,sha

def main():
 p=argparse.ArgumentParser()
 for k in ('repo','artifact-root','output'):p.add_argument('--'+k,type=pathlib.Path,required=True)
 a=p.parse_args()
 for name in ('run_android_instrumentation.py','app_instrumentation_matrix.py','vertical_locale_matrix.py'):
  original=subprocess.check_output(['git','show',TREE+':tools/'+name],cwd=a.repo)
  require(original==(a.repo/'tools'/name).read_bytes(),'imported helper differs from exact tree '+name)
 sys.path.insert(0,str(a.repo/'tools'))
 from run_android_instrumentation import declared_tests,source_tests_sha256,parse_protocol
 from app_instrumentation_matrix import app_partition,report_paths,verify_app_reports,PHASE_TIMEOUTS,SELECTED_PHASES
 require(source_tests_sha256(a.repo/'app/src/androidTest')=='a5dd8b617ce5610378b197e5f5ac5a59748e87e39a592b3198a53e8bb842345f','app source digest changed')
 require(source_tests_sha256(a.repo/'Paintroid/src/androidTest')=='1412fb3f410c439d3543daab499667dd288f720368b958275158edc2a9dd6e0b','library source digest changed')
 out={}
 for sdk in (30,35):
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
   require(summary['timed_out'] is False and 0<=summary['elapsed_seconds']<=summary['timeout_seconds'],'phase timeout')
   require(summary['included_tests']==(sorted(f'{c}#{n}' for c,n in wanted) if phase in SELECTED_PHASES else []),'selector differs')
   require(summary['leave_target_running'] is (phase=='seed'),'target lifetime differs')
   ids=[(x['classname'],x['name']) for x in summary['cases']];require(len(ids)==len(set(ids)) and set(ids)==wanted,'phase identities incomplete/extra')
   xmls=list(path.parent.glob('TEST-*.xml'));require(len(xmls)==1,'XML inventory');xml=E.fromstring(xmls[0].read_bytes());xc=xml.findall('testcase');require(xml.tag=='testsuite' and len(xc)==len(xml.findall('.//testcase')) and int(xml.get('tests'))==len(xc),'XML structure/count')
   require(collections.Counter((x.get('classname'),x.get('name')) for x in xc)==collections.Counter(ids),'XML identities differ')
   statuses={i:(next((tag for tag in ('failure','error','skipped') if x.find(tag) is not None),'passed')) for i,x in zip([(x.get('classname'),x.get('name')) for x in xc],xc)}
   for c in summary['cases']:require(statuses[(c['classname'],c['name'])]==c['status'],'XML/protocol status differs')
   for field,tag in [('failures','failure'),('errors','error'),('skipped','skipped')]:require(int(xml.get(field))==sum(v==tag for v in statuses.values()),'XML status count differs')
   failures=[c for c in summary['cases'] if c['status']!='passed'];cases.extend(summary['cases'])
   phases[phase]={'completed':len(ids),'passed':len(ids)-len(failures),'failures':failures,'raw_sha256':sha(raw.read_bytes()),'summary_sha256':sha(path.read_bytes()),'xml_sha256':sha(xmls[0].read_bytes()),'elapsed_seconds':summary['elapsed_seconds'],'success':summary['success']}
   if phase!='library':appreports[phase]=summary
  allwanted=set.union(*parts.values());allids=[(c['classname'],c['name']) for c in cases];require(len(allids)==len(set(allids)),'matrix duplicates')
  require(len(allwanted)==(95 if sdk==30 else 104),'frozen matrix inventory changed')
  if sdk==30:
   union=verify_app_reports(app,sdk,appreports,source_tests_sha256(appsrc),declared_tests(appsrc)-app)
   for name in ('coverage.json','ordinary-gallery-coverage.json','vertical-coverage.json'):require(json.loads((root/'app'/name).read_bytes())==json.loads(json.dumps(union)),'coverage union differs')
   require(not missing and all(c['status']=='passed' for c in cases),'API30 did not completely pass')
  out[str(sdk)]={'status':'PASS' if not missing and all(c['status']=='passed' for c in cases) else 'FAIL','source_digests':{'app':source_tests_sha256(appsrc),'library':source_tests_sha256(libsrc)},'sdk_eligible_declarations':len(app)+len(lib),'scheduled':len(allwanted),'completed':len(cases),'passed':sum(c['status']=='passed' for c in cases),'failed':sum(c['status']!='passed' for c in cases),'missing_phases':missing,'phases':phases}
 result={'head':HEAD,'merge':MERGE,'tree':TREE,'run_id':RUN,'matrices':out,'scope':'Read-only exact-source selector/digest, raw protocol, summary, XML and matrix reconciliation. ZIP and APK provenance are separate bound reviews; API35 restart missing phases cannot be replaced by other successful phases.'}
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({sdk:{k:v for k,v in d.items() if k not in ('phases','source_digests')} for sdk,d in out.items()},indent=2))
if __name__=='__main__':main()
