#!/usr/bin/env python3
"""Current artifact phase receipts and the four repaired fixture executions."""
import argparse,hashlib,json,pathlib,re,xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument('--artifact-root',type=pathlib.Path,required=True);p.add_argument('--binding',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
base=a.artifact_root/'build/reports/ci-phases';phases={}
for name in ('python','jvm','native','lint'):
 files={suffix:base/(name+'.'+suffix) for suffix in ('log','time','started-at','ended-at')}
 times=dict(line.split('=',1) for line in files['time'].read_text().splitlines() if '=' in line)
 phases[name]={'exit_status':int(times['exit_status']),'real_seconds':float(times['real_seconds']),'started_at':files['started-at'].read_text().strip(),'ended_at':files['ended-at'].read_text().strip(),'files':[{'path':str(f.relative_to(a.artifact_root)),'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files.values()]}
s=(base/'python.log').read_text();matches=re.findall(r'Ran (\d+) tests in ([0-9.]+)s',s)
if len(matches)!=1:raise ValueError('expected one Python summary')
count,seconds=matches[0];skipped=re.search(r'OK \(skipped=(\d+)\)',s);skipped=int(skipped.group(1)) if skipped else 0
if not re.search(r'^OK(?: \(skipped=\d+\))?$',s,re.M):raise ValueError('Python summary is not OK')
phases['python']['unittest']={'total':int(count),'passed':int(count)-skipped,'skipped':skipped,'seconds':float(seconds),'skipped_identity_limit':'Compact hosted output may not name skipped methods.'}
fixed=[('LocalizedDialogLayoutTest','retainedVerticalNoticeKeepsReadingOffsetAcrossRotation'+suffix) for suffix in ('[30]','')]+[('UiDirectionContextTest','legacyResourceContextsDoNotNeedProcessDefaultOrApi24LocaleList'+suffix) for suffix in ('[21]','')]
all_cases=[];files=[]
for owner in ('LocalizedDialogLayoutTest','UiDirectionContextTest','AppLanguageTest'):
 path=a.artifact_root/('Paintroid/build/test-results/testDebugUnitTest/TEST-org.catrobat.paintroid.local.'+owner+'.xml');files.append({'path':str(path.relative_to(a.artifact_root)),'sha256':sha(path.read_bytes())})
 for c in ET.parse(path).getroot().iter('testcase'):
  states=[x.tag for x in c if x.tag in ('failure','error','skipped')]
  all_cases.append({'name':c.get('name'),'classname':c.get('classname'),'status':'PASS' if not states else '/'.join(states).upper(),'seconds':float(c.get('time')),'repaired_fixture':(owner,c.get('name')) in fixed})
selected=[c for c in all_cases if c['repaired_fixture']]
if len(selected)!=len(fixed):raise ValueError('missing or duplicate repaired fixture identities')
binding=json.loads(a.binding.read_text());r={'run_id':binding['run_id'],'source_tree':binding['tree'],'phases':phases,'xml':files,'repaired_fixture_executions':selected,'direction_executions':[c for c in all_cases if c['classname'].endswith('.UiDirectionContextTest')],'new_option_executions':[c for c in all_cases if c['classname'].endswith('.AppLanguageTest') and (c['name'].startswith('sixNewOptionsKeepTheirIdentityAndExplicitEnglishFallback') or c['name'].startswith('furtherOptionsIncludingPrincipalVarietiesKeepTheirExactIdentityAndFallback'))],'phase_receipts_pass':all(v['exit_status']==0 for v in phases.values()),'repaired_fixture_pass':all(c['status']=='PASS' for c in selected),'limits':['Phase exits and the four repaired fixtures complement the independent complete source-derived JUnit inventory; they do not replace it.','Python skipped methods receive no pass credit.']};
if len(r['new_option_executions'])!=4:raise ValueError('new option execution inventory')
a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('phase_receipts_pass','repaired_fixture_pass','repaired_fixture_executions')},indent=2));print(json.dumps(phases['python']['unittest'],indent=2))
