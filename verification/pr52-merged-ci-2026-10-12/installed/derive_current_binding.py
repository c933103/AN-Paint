#!/usr/bin/env python3
"""Derive current API35-only identity/source selection; never borrow execution data."""
import argparse,json,pathlib,sys,subprocess,xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--artifacts',type=pathlib.Path,required=True);p.add_argument('--job-id',type=int);a=p.parse_args();here=pathlib.Path(__file__).resolve().parent
pub=json.loads((a.artifacts/'source-publication.json').read_bytes());tree=pub.get('tree',pub['head_tree'])
if tree!=pub['merge_tree'] or pub['merge_parents']!=[pub['base'],pub['head']]:raise ValueError('merge identity differs')
sys.path.insert(0,str(a.repo/'tools'))
for path in ('tools/run_android_instrumentation.py','tools/app_instrumentation_matrix.py'):
 if subprocess.check_output(['git','show',tree+':'+path],cwd=a.repo)!=(a.repo/path).read_bytes():raise ValueError('current helper differs '+path)
from run_android_instrumentation import declared_tests,source_tests_sha256
from app_instrumentation_matrix import app_partition,PHASE_TIMEOUTS
b={k:pub[k] for k in ('head','base','merge','merge_tree','merge_parents','run_id')};b.update(schema=1,tree=tree,ordered_parents=pub['head_parents'],remote_source_verification=pub['remote_provenance_verified'],review_request='Fresh natural merged PR52 API35 installed review only',run_attempt=pub['run_attempt'],selected_apis=[35],unselected_apis={'30':'NOT_SELECTED_IN_CURRENT_RUN; no current artifact or execution credit'})
b['source_digests']={k:source_tests_sha256(a.repo/v) for k,v in [('app','app/src/androidTest'),('library','Paintroid/src/androidTest')]};b['source_matrix']={}
for sdk in (35,):
 app=declared_tests(a.repo/'app/src/androidTest',sdk_level=sdk);lib=declared_tests(a.repo/'Paintroid/src/androidTest',sdk_level=sdk);parts=app_partition(app,sdk);parts['library']=lib;scheduled=set.union(*parts.values())
 b['source_matrix'][str(sdk)]={'eligible':len(app)+len(lib),'scheduled':len(scheduled),'phases':{k:len(v) for k,v in parts.items()},'explicit_omissions':[list(x) for x in sorted((app|lib)-scheduled)],'timeouts':{k:180 if k=='library' else PHASE_TIMEOUTS[k] for k in parts},'eligible_identities':[list(x) for x in sorted(app|lib)],'selected_identities_by_phase':{k:[list(x) for x in sorted(v)] for k,v in parts.items()}}
def xml(path):return {n.get('name'):''.join(n.itertext()) for n in ET.fromstring(subprocess.check_output(['git','show',tree+':'+path],cwd=a.repo)) if n.tag=='string'}
d=xml('Paintroid/src/main/res/values/strings.xml')|xml('Paintroid/src/main/res/values-ar/strings.xml');b['arabic_messages']={route:d[key].replace('%1$s',d['commons_metadata_query_failed']).replace("\\'","'") for route,key in [('copy','commons_credit_copy_failed_reason'),('insert','ui_could_not_load_gallery_image')]}
b['provenance_note']='Source digests, SDK eligibility, identities and selectors freshly derived from current exact tree. Remote commit/merge verification supplied by coordinator. No prior run results supply current execution credit.'
(here/'binding.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
ar={k:b[k] for k in ('head','tree','merge','run_id')};ar['emulators']={};ar['downloads']={}
for name in ('apk-and-source','instrumentation-apks','api35'):
 f=a.artifacts/(name+'.metadata.json')
 matches=[x for x in pub.get('artifacts',[]) if x['name']==(('emulator-api-35' if name=='api35' else name)+'-'+b['merge'])]
 if f.exists():item=json.loads(f.read_bytes())
 elif len(matches)==1:item=matches[0]
 else:continue
 if matches and (len(matches)!=1 or matches[0]!=item):raise ValueError('artifact metadata sources disagree '+name)
 expected=('emulator-api-35' if name=='api35' else name)+'-'+b['merge']
 if item['name']!=expected or item['workflow_run']['id']!=b['run_id'] or item['workflow_run']['head_sha']!=b['head']:raise ValueError('official metadata binding differs '+name)
 row={'artifact_id':item['id'],'sha256':item['digest'].removeprefix('sha256:')}
 if name=='api35':
  if a.job_id is None:raise ValueError('exact actual API35 job ID required')
  row.update(job_id=a.job_id,execution_attempt=1);ar['emulators']['35']=row
 else:ar['downloads'][name]=row
(here/'artifact-binding.json').write_text(json.dumps(ar,indent=2)+'\n')
print(json.dumps({'source_digests':b['source_digests'],'selected_apis':b['selected_apis'],'scheduled':b['source_matrix']['35']['scheduled'],'phases':b['source_matrix']['35']['phases'],'artifact_binding_ready':bool(ar['emulators'])},indent=2))
