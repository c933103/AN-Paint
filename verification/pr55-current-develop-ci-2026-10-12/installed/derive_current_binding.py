#!/usr/bin/env python3
"""Derive current immutable binding, eligible identities and selectors from source."""
import argparse, json, pathlib, subprocess, sys, xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--artifacts',type=pathlib.Path,required=True);a=p.parse_args();here=pathlib.Path(__file__).resolve().parent
pub=json.loads((a.artifacts/'source-publication.json').read_bytes());sys.path.insert(0,str(a.repo/'tools'))
from run_android_instrumentation import declared_tests, source_tests_sha256
from app_instrumentation_matrix import app_partition, PHASE_TIMEOUTS
b={k:pub[k] for k in ('head','tree','base','merge','merge_tree','merge_parents','run_id','remote_source_verification','review_request')};b['schema']=1;b['ordered_parents']=pub['ordered_parents'];b['source_digests']={k:source_tests_sha256(a.repo/v) for k,v in [('app','app/src/androidTest'),('library','Paintroid/src/androidTest')]};b['source_matrix']={}
for sdk in (30,35):
 app=declared_tests(a.repo/'app/src/androidTest',sdk_level=sdk);lib=declared_tests(a.repo/'Paintroid/src/androidTest',sdk_level=sdk);parts=app_partition(app,sdk);parts['library']=lib;scheduled=set.union(*parts.values())
 b['source_matrix'][str(sdk)]={'eligible':len(app)+len(lib),'scheduled':len(scheduled),'phases':{k:len(v) for k,v in parts.items()},'explicit_omissions':[list(x) for x in sorted((app|lib)-scheduled)],'timeouts':{k:180 if k=='library' else PHASE_TIMEOUTS[k] for k in parts},'eligible_identities':[list(x) for x in sorted(app|lib)],'selected_identities_by_phase':{k:[list(x) for x in sorted(v)] for k,v in parts.items()}}
def xml(path):return {n.get('name'):''.join(n.itertext()) for n in ET.fromstring(subprocess.check_output(['git','show',b['tree']+':'+path],cwd=a.repo)) if n.tag=='string'}
d=xml('Paintroid/src/main/res/values/strings.xml')|xml('Paintroid/src/main/res/values-ar/strings.xml');b['arabic_messages']={route:d[key].replace('%1$s',d['commons_metadata_query_failed']).replace("\\'","'") for route,key in [('copy','commons_credit_copy_failed_reason'),('insert','ui_could_not_load_gallery_image')]};b['provenance_note']='Coordinator independently remotely verified publication commit/tree and ordered merge parents. This review freshly derives all source digests, exact SDK eligibility, identities, selectors and phase schedules from the current tree; no prior run results carry acceptance credit.'
(here/'binding.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
ar={k:b[k] for k in ('head','tree','merge','run_id')};ar['emulators']={};ar['downloads']={}
for item in pub['artifacts']:
 for prefix in ('apk-and-source','instrumentation-apks'):
  if item['name']==prefix+'-'+b['merge']: ar['downloads'][prefix]={'artifact_id':item['id'],'sha256':item['digest'].removeprefix('sha256:')}
(here/'artifact-binding.json').write_text(json.dumps(ar,indent=2)+'\n');print(json.dumps({'source_digests':b['source_digests'],'matrices':{k:{kk:vv for kk,vv in v.items() if kk not in ('eligible_identities','selected_identities_by_phase')} for k,v in b['source_matrix'].items()}},indent=2))
