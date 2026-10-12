#!/usr/bin/env python3
"""Derive current immutable binding, eligible identities and selectors from source."""
import argparse, json, pathlib, subprocess, sys, xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--artifacts',type=pathlib.Path,required=True);a=p.parse_args();here=pathlib.Path(__file__).resolve().parent
pub=json.loads((a.artifacts/'source-publication.json').read_bytes());sys.path.insert(0,str(a.repo/'tools'))
for path in ('tools/run_android_instrumentation.py','tools/app_instrumentation_matrix.py'):
 if subprocess.check_output(['git','show',pub['tree']+':'+path],cwd=a.repo)!=(a.repo/path).read_bytes():raise ValueError('current source helper differs '+path)
from run_android_instrumentation import declared_tests, source_tests_sha256
from app_instrumentation_matrix import app_partition, PHASE_TIMEOUTS
b={k:pub[k] for k in ('head','tree','base','merge','merge_tree','merge_parents','run_id','remote_source_verification','review_request')};b['schema']=1;b['ordered_parents']=(pub.get('ordered_parents') or [pub['parent']]);b['source_digests']={k:source_tests_sha256(a.repo/v) for k,v in [('app','app/src/androidTest'),('library','Paintroid/src/androidTest')]};b['source_matrix']={}
for sdk in (30,35):
 app=declared_tests(a.repo/'app/src/androidTest',sdk_level=sdk);lib=declared_tests(a.repo/'Paintroid/src/androidTest',sdk_level=sdk);parts=app_partition(app,sdk);parts['library']=lib;scheduled=set.union(*parts.values())
 b['source_matrix'][str(sdk)]={'eligible':len(app)+len(lib),'scheduled':len(scheduled),'phases':{k:len(v) for k,v in parts.items()},'explicit_omissions':[list(x) for x in sorted((app|lib)-scheduled)],'timeouts':{k:180 if k=='library' else PHASE_TIMEOUTS[k] for k in parts},'eligible_identities':[list(x) for x in sorted(app|lib)],'selected_identities_by_phase':{k:[list(x) for x in sorted(v)] for k,v in parts.items()}}
def xml(path):return {n.get('name'):''.join(n.itertext()) for n in ET.fromstring(subprocess.check_output(['git','show',b['tree']+':'+path],cwd=a.repo)) if n.tag=='string'}
d=xml('Paintroid/src/main/res/values/strings.xml')|xml('Paintroid/src/main/res/values-ar/strings.xml');b['arabic_messages']={route:d[key].replace('%1$s',d['commons_metadata_query_failed']).replace("\\'","'") for route,key in [('copy','commons_credit_copy_failed_reason'),('insert','ui_could_not_load_gallery_image')]};b['provenance_note']='Coordinator independently remotely verified publication commit/tree and ordered merge parents. This review freshly derives all source digests, exact SDK eligibility, identities, selectors and phase schedules from the current tree; no prior run results carry acceptance credit.'
(here/'binding.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
ar={k:b[k] for k in ('head','tree','merge','run_id')};ar['emulators']={};ar['downloads']={}
for item in pub.get('artifacts',[]):
 for prefix in ('apk-and-source','instrumentation-apks'):
  if item['name']==prefix+'-'+b['merge']: ar['downloads'][prefix]={'artifact_id':item['id'],'sha256':item['digest'].removeprefix('sha256:')}
for sdk in (30,35):
 artifacts=[item for item in pub.get('artifacts',[]) if item['name']==f'emulator-api-{sdk}-'+b['merge']]
 metadata=a.artifacts/f'api{sdk}.metadata.json'
 if metadata.exists():
  item=json.loads(metadata.read_bytes())
  if item['name']!=f'emulator-api-{sdk}-'+b['merge'] or item['workflow_run']['id']!=b['run_id'] or item['workflow_run']['head_sha']!=b['head']:raise ValueError('local official emulator metadata binding differs')
  if artifacts and artifacts[0]!=item:raise ValueError('published/local official artifact metadata differs')
  if not artifacts:artifacts=[item]
 jobs=[job for job in pub.get('jobs',[]) if job['name']==f'Emulator API {sdk}']
 if len(artifacts)>1 or len(jobs)>1:raise ValueError('duplicate emulator artifact/job metadata')
 if artifacts and jobs:
  item=artifacts[0];job=jobs[0];display_job=job;execution_attempt=pub.get('run_attempt',1)
  # GitHub gives carried-forward successful jobs new attempt-two display IDs.
  # Bind the API35 log/artifact to its actual attempt-one execution, retaining
  # the later display alias separately rather than calling it a second run.
  if pub.get('run_attempt')==2:
   first=json.loads((a.artifacts/'attempt1-final-jobs.json').read_bytes())['jobs']
   second=json.loads((a.artifacts/'attempt2-jobs-initial.json').read_bytes())['jobs']
   old=[j for j in first if j['name']==job['name']]
   alias=[j for j in second if j['id']==job['id']]
   if len(old)!=1 or len(alias)!=1:raise ValueError('missing exact attempt-history job identity')
   if any(j['run_id']!=b['run_id'] or j['head_sha']!=b['head'] for j in old+alias):raise ValueError('attempt-history source/run differs')
   if sdk==35:
    if old[0]['conclusion']!='success' or old[0]['run_attempt']!=1 or alias[0]['run_attempt']!=2:raise ValueError('API35 execution attempt differs')
    if any(old[0][key]!=alias[0][key] for key in ('started_at','completed_at','steps')):raise ValueError('API35 was not an exact carried-forward execution')
    job=old[0];execution_attempt=1
   else:
    if old[0]['conclusion']!='failure' or alias[0]['run_attempt']!=2 or old[0]['id']==alias[0]['id']:raise ValueError('API30 retry history differs')
    execution_attempt=2
  if job['run_id']!=b['run_id']:raise ValueError('emulator job belongs to another run')
  ar['emulators'][str(sdk)]={'artifact_id':item['id'],'sha256':item['digest'].removeprefix('sha256:'),'job_id':job['id'],'execution_attempt':execution_attempt,'current_display_job_id':display_job['id'],'display_id_is_execution_alias':display_job['id']!=job['id']}
(here/'artifact-binding.json').write_text(json.dumps(ar,indent=2)+'\n');print(json.dumps({'source_digests':b['source_digests'],'matrices':{k:{kk:vv for kk,vv in v.items() if kk not in ('eligible_identities','selected_identities_by_phase')} for k,v in b['source_matrix'].items()}},indent=2))
