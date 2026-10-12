import argparse,pathlib,json,subprocess,sys,xml.etree.ElementTree as ET,re,hashlib
sys.dont_write_bytecode=True
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--artifacts',type=pathlib.Path,required=True);a=p.parse_args();here=pathlib.Path(__file__).resolve().parent
pub=json.loads((a.artifacts/'source-publication.json').read_bytes());b=dict(head=pub['head'],tree=pub['head_tree'],base=pub['base'],merge=pub['synthetic_merge'],merge_tree=pub['synthetic_merge_tree'],merge_parents=pub['synthetic_merge_parents'],run_id=pub['run_id'],ordered_parents=pub['head_parents'],schema=1)
for path in ('tools/run_android_instrumentation.py','tools/app_instrumentation_matrix.py'):
 if subprocess.check_output(['git','show',b['tree']+':'+path],cwd=a.repo)!=(a.repo/path).read_bytes():raise ValueError('current helper differs')
sys.path.insert(0,str(a.repo/'tools'));from run_android_instrumentation import declared_tests,source_tests_sha256
from app_instrumentation_matrix import app_partition,PHASE_TIMEOUTS
b['source_digests']={k:source_tests_sha256(a.repo/v) for k,v in [('app','app/src/androidTest'),('library','Paintroid/src/androidTest')]};b['source_matrix']={}
for sdk in (30,35):
 app=declared_tests(a.repo/'app/src/androidTest',sdk_level=sdk);lib=declared_tests(a.repo/'Paintroid/src/androidTest',sdk_level=sdk);parts=app_partition(app,sdk);parts['library']=lib;scheduled=set.union(*parts.values())
 b['source_matrix'][str(sdk)]={'eligible':len(app)+len(lib),'scheduled':len(scheduled),'phases':{k:len(v) for k,v in parts.items()},'explicit_omissions':[list(x) for x in sorted((app|lib)-scheduled)],'timeouts':{k:180 if k=='library' else PHASE_TIMEOUTS[k] for k in parts},'eligible_identities':[list(x) for x in sorted(app|lib)],'selected_identities_by_phase':{k:[list(x) for x in sorted(v)] for k,v in parts.items()}}
def xml(path):return {n.get('name'):''.join(n.itertext()) for n in ET.fromstring(subprocess.check_output(['git','show',b['tree']+':'+path],cwd=a.repo)) if n.tag=='string'}
d=xml('Paintroid/src/main/res/values/strings.xml')|xml('Paintroid/src/main/res/values-ar/strings.xml');b['arabic_messages']={route:d[key].replace('%1$s',d['commons_metadata_query_failed']).replace("\\'","'") for route,key in [('copy','commons_credit_copy_failed_reason'),('insert','ui_could_not_load_gallery_image')]}
b['provenance_note']='Coordinator independently verified remote source publication and ordered parents. All eligible identities, digests and phases freshly derived from frozen source; no historical outcomes reused.'
(here/'binding.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
ar={k:b[k] for k in ('head','tree','merge','run_id')};ar['emulators']={};ar['downloads']={}
for sdk,jid in [(30,115046988312),(35,115046988385)]:
 m=a.artifacts/f'api{sdk}-metadata.json'
 if not m.exists():continue
 item=json.loads(m.read_bytes())
 if item['name']!=f'emulator-api-{sdk}-'+b['merge'] or item['workflow_run']['id']!=b['run_id'] or item['workflow_run']['head_sha']!=b['head']:raise ValueError('official emulator metadata differs')
 ar['emulators'][str(sdk)]={'artifact_id':item['id'],'sha256':item['digest'].removeprefix('sha256:'),'job_id':jid,'execution_attempt':1,'job_identity_source':'coordinator verified exact run job'}
item=json.loads((a.artifacts/'apk-and-source-metadata.json').read_bytes());ar['downloads']['apk-and-source']={'artifact_id':item['id'],'sha256':item['digest'].removeprefix('sha256:')}
s=(a.artifacts/'build-job.log').read_text('utf-8-sig');m=re.search(r'SHA256 digest of uploaded artifact is ([0-9a-f]{64})\n[^\n]*Finalizing artifact upload\n[^\n]*Artifact instrumentation-apks-'+b['merge']+r' successfully finalized\. Artifact ID (\d+)',s)
if not m:raise ValueError('unique build instrumentation upload receipt missing')
ar['downloads']['instrumentation-apks']={'artifact_id':int(m[2]),'sha256':m[1],'binding_source':'full build upload receipt and independent emulator download receipt; no local test APK archive'}
(here/'artifact-binding.json').write_text(json.dumps(ar,indent=2)+'\n');print(json.dumps({'source_digests':b['source_digests'],'source_counts':{k:(v['eligible'],v['scheduled']) for k,v in b['source_matrix'].items()}},indent=2))
