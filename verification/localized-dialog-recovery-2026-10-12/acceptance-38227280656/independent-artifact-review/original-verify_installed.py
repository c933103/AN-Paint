if not __debug__:
 raise RuntimeError('Acceptance verification requires ordinary Python; optimized mode is rejected')
import argparse,hashlib,json,sys
from pathlib import Path
import xml.etree.ElementTree as E
p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();R=Path(__file__).parent;checkout=R/'checkout';sys.path.insert(0,str(checkout/'tools'))
from run_android_instrumentation import declared_tests,source_tests_sha256,parse_protocol
from app_instrumentation_matrix import read_app_reports,report_paths,app_partition,verify_app_reports
source=checkout/'app/src/androidTest';expected=declared_tests(source,sdk_level=35);suppressed=declared_tests(source)-expected;digest=source_tests_sha256(source);reports=read_app_reports(a.root,35);union=verify_app_reports(expected,35,reports,digest,suppressed);parts=app_partition(expected,35);paths=report_paths(a.root,35)
ns=checkout/'Paintroid/src/androidTest';parts['native']=declared_tests(ns,sdk_level=35);paths['native']=a.root/'Paintroid/androidTest-results/summary.json';reports['native']=json.loads(paths['native'].read_text());native=reports['native'];assert native['source_tests_sha256']==source_tests_sha256(ns);assert native['device_sdk']==35 and native['timeout_seconds']==180;assert native['sdk_suppressed_tests']==[] and native['excluded_classes']==[] and native['included_tests']==[] and native['leave_target_running'] is False
plain=lambda v:json.loads(json.dumps(v));facts={}
for phase,path in paths.items():
 report=reports[phase];raw=path.with_name('instrumentation.log');parsed=parse_protocol(raw.read_text(),parts[phase],returncode=report['returncode'],timed_out=report['timed_out']);assert parsed['success'],(phase,parsed['errors'])
 for k,v in parsed.items():assert plain(v)==report[k],(phase,k)
 xml=list(path.parent.glob('TEST-*.xml'));assert len(xml)==1;root=E.parse(xml[0]).getroot();cases=root.findall('.//testcase');ids=[(c.attrib['classname'],c.attrib['name']) for c in cases];assert len(ids)==len(set(ids));assert set(ids)==parts[phase];assert not any(root.findall('.//'+t) for t in ['failure','error','skipped']);assert float(report['elapsed_seconds'])<=report['timeout_seconds']
 facts[phase]=dict(completed=len(ids),elapsed_seconds=report['elapsed_seconds'],timeout_seconds=report['timeout_seconds'],protocol_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),xml_sha256=hashlib.sha256(xml[0].read_bytes()).hexdigest())
assert sum(x['completed'] for x in facts.values())==104
for name in ['app/coverage.json','app/ordinary-gallery-coverage.json','app/vertical-coverage.json','app/accepted-credit-restart/coverage.json']:assert json.loads((a.root/name).read_text())==plain(union),name
out=dict(success=True,head='71f4d288669858e7975ec4c094b7f47a9a1ff145',ci_merge='f008d110f83cb6390db941b9177062edb8ea212c',tree='815e265af5387111dcdaef66efac5d2091bbb56d',run_id=38227280656,exact_total=104,app_union=union,phases=facts,source_tests_sha256=digest,native_source_tests_sha256=source_tests_sha256(ns),scope='Original raw protocol, XML and source-digest-bound phase union. Screenshots, export manifests and build identity are separate gates.')
(R/'candidate-installed-verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(success=True,total=104,phases={k:v['completed'] for k,v in facts.items()})))
