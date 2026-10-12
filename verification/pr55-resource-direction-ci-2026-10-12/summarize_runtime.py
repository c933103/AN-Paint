#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,re,xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument('--artifact-root',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
base=a.artifact_root/'build/reports/ci-phases';phases={}
for name in ('python','jvm','native','lint'):
 files={suffix:base/(name+'.'+suffix) for suffix in ('log','time','started-at','ended-at')}
 times=dict(line.split('=',1) for line in files['time'].read_text().splitlines() if '=' in line)
 phases[name]={'exit_status':int(times['exit_status']),'real_seconds':float(times['real_seconds']),'started_at':files['started-at'].read_text().strip(),'ended_at':files['ended-at'].read_text().strip(),'files':[{'path':str(f.relative_to(a.artifact_root)),'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files.values()]}
s=(base/'python.log').read_text();m=re.search(r'Ran (\d+) tests in ([0-9.]+)s',s);skipped=int(re.search(r'OK \(skipped=(\d+)\)',s).group(1));count=int(m.group(1));phases['python']['unittest']={'total':count,'passed':count-skipped,'skipped':skipped,'seconds':float(m.group(2)),'skipped_identity_limit':'Compact hosted output does not name skipped methods.'}
path=a.artifact_root/'Paintroid/build/test-results/testDebugUnitTest/TEST-org.catrobat.paintroid.local.UiDirectionContextTest.xml';cases=[]
for c in ET.parse(path).getroot().iter('testcase'):
 states=[x.tag for x in c if x.tag in ('failure','error','skipped')];cases.append({'name':c.get('name'),'classname':c.get('classname'),'status':'PASS' if not states else '/'.join(states).upper(),'seconds':float(c.get('time'))})
r={'run_id':38285607590,'source_tree':'ab6f5497e147e81d4c50f4954ea87f364be087aa','phases':phases,'new_direction_test_xml_sha256':sha(path.read_bytes()),'new_direction_test_cases':cases,'new_direction_native_passes':sum(c['status']=='PASS' for c in cases),'new_direction_legacy_failures':sum(c['status']=='FAILURE' for c in cases),'overall':'FAIL: exact JVM gate has four assertion failures; phase summaries are not substituted for complete identity audit.'}
a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'phase_exits':{k:v['exit_status'] for k,v in phases.items()},'hosted_python':phases['python']['unittest'],'new_direction_cases':len(cases),'native_passes':r['new_direction_native_passes'],'legacy_failures':r['new_direction_legacy_failures']},indent=2))
