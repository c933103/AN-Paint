#!/usr/bin/env python3
"""Bind the platform-discovery receipt to this source, method, complete protocol and run."""
import argparse,json,pathlib,re,sys,xml.etree.ElementTree as ET
from audit_natural_artifacts import BINDING,HEAD,TREE,MERGE,RUN,SOURCE_SHA,require,sha,read_source
from audit_platform_locale_receipt import check,MARKER
from audit_success_protocol import verify_success_sequence
IDENTITY=('paint.anpaint.android.EditorDeviceTest','deviceLanguageRowKeepsTheSystemLabelAcrossRealAppLanguageSwitches')
LINE=re.compile(r'^\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}\s+(\d+)\s+(\d+)\s+I\s+(TestRunner|LanguagePickerTest)\s*:\s*(.*)$')

def bind_method(text,tags,sdk=35):
 receipt=check(text,tags,sdk);lines=text.splitlines();events=[]
 target=IDENTITY[1]+'('+IDENTITY[0]+')'
 for no,line in enumerate(lines,1):
  m=LINE.fullmatch(line)
  if m and m[3]=='TestRunner' and m[4] in ('started: '+target,'finished: '+target):events.append((no,m[1],m[2],m[4].split(':',1)[0]))
 require(len(events)==2 and [e[3] for e in events]==['started','finished'],'missing, duplicate or reversed exact method boundary')
 start,finish=events;require(start[1:3]==finish[1:3],'method runner process/thread changed')
 require(start[0]<receipt['line']<finish[0],'receipt outside exact method window')
 observed=LINE.fullmatch(lines[receipt['line']-1]);require(observed is not None and observed[3]=='LanguagePickerTest','receipt logger or line format differs')
 require((observed[1],observed[2])==start[1:3],'platform receipt process/thread differs from method')
 for no,line in enumerate(lines[start[0]:finish[0]-1],start[0]+1):
  m=LINE.fullmatch(line)
  if m and m[3]=='TestRunner':require(not m[4].startswith(('started:','finished:','failed:')),'interleaved or failed method in platform window')
 labels=[]
 for no,line in enumerate(lines[start[0]:finish[0]-1],start[0]+1):
  m=LINE.fullmatch(line)
  if m and m[3]=='LanguagePickerTest' and m[4].startswith('device='):
   require(m[1]==start[1],'device-label receipt process differs');labels.append((no,m[4]))
 require([x[1] for x in labels]==['device=en-US app='+tag+' first=0 label=Use device language' for tag in ('ja','ar','en-001')],'successful method locale-switch labels differ')
 return receipt|{'method_identity':list(IDENTITY),'runner_pid':start[1],'runner_tid':start[2],'started_line':start[0],'finished_line':finish[0],'label_receipt_lines':[n for n,_ in labels]}

def audit(repo,artifacts,matrix_path,provenance_path):
 source_paths=['app/src/androidTest/java/paint/anpaint/android/EditorDeviceTest.kt','app/src/main/AndroidManifest.xml','Paintroid/src/main/res/values/app_language_tags.xml','Paintroid/src/main/res/xml/app_locales.xml']
 sources={p:read_source(repo,p) for p in source_paths}
 for p,raw in sources.items():require(raw==(repo/p).read_bytes(),'platform source differs from frozen tree '+p)
 source=sources[source_paths[0]].decode();needle='    @Test @SdkSuppress(minSdkVersion=33)\n    fun '+IDENTITY[1]+'() {';require(source.count(needle)==1,'method eligibility/source identity differs');body=source.split(needle,1)[1].split('\n    @Test',1)[0]
 for token in ('private val context get()=instrumentation.targetContext','import android.app.LocaleConfig'):require(token in source,'platform target context/import differs')
 for token in ('val expected=context.resources.getStringArray(R.array.app_language_tags).toList()','if(Build.VERSION.SDK_INT>=34) LocaleConfig.fromContextIgnoringOverride(context)','else LocaleConfig(context)','LocaleConfig.STATUS_SUCCESS,config.status','expected.size,actual.size','expected.toSet(),actual.toSet()'):
  require(token in body,'platform method implementation differs '+token)
 require(source.count(MARKER)==1,'platform marker outside unique current method')
 android='{http://schemas.android.com/apk/res/android}'
 app=ET.fromstring(sources[source_paths[1]]).find('application');require(app is not None and app.get(android+'localeConfig')=='@xml/app_locales','application localeConfig binding differs')
 arr=ET.fromstring(sources[source_paths[2]]).find("string-array[@name='app_language_tags']");require(arr is not None,'current tag array absent');tags=[x.text for x in arr];require(len(tags)==167 and len(set(tags))==167 and all(tags),'current exact 167 inventory differs')
 config_tags=[n.get(android+'name') for n in ET.fromstring(sources[source_paths[3]])];require(config_tags==tags,'locale resource/picker inventory differs')
 sys.path.insert(0,str(repo/'tools'));from run_android_instrumentation import declared_tests,source_tests_sha256
 from app_instrumentation_matrix import app_partition
 require(source_tests_sha256(repo/'app/src/androidTest')==SOURCE_SHA,'current test digest differs')
 require(IDENTITY not in declared_tests(repo/'app/src/androidTest',sdk_level=30),'platform method incorrectly selected for API30')
 wanted=app_partition(declared_tests(repo/'app/src/androidTest',sdk_level=35),35)['ordinary'];require(IDENTITY in wanted,'platform method missing from API35 ordinary source schedule')
 matrix=json.loads(matrix_path.read_bytes());prov=json.loads(provenance_path.read_bytes())
 for kind,r in [('matrix',matrix),('prebuilt',prov)]:
  require(r['head']==HEAD and r['tree']==TREE and r['merge']==MERGE and str(r['run_id'])==RUN,'platform '+kind+' run/source differs')
 require(matrix['installed_gate_status']=='PASS','platform receipt cannot substitute for failed installed matrix')
 require(prov['status'] in ('PASS_BOUNDED_PREBUILT_PROVENANCE','PASS_RECEIPT_ONLY_PREBUILT_PROVENANCE') and {j['api'] for j in prov['jobs']}=={30,35},'both prebuilt install receipts required')
 raw=(artifacts/'api35/app/androidTest-results/instrumentation.log').read_bytes();serial=verify_success_sequence(raw.decode(),wanted)
 target_events=[e for e in serial['events'] if e['identity']==list(IDENTITY)];require([e['code'] for e in target_events]==[1,0],'platform exact method did not succeed')
 require(matrix['matrices']['35']['phases']['ordinary']['raw_sha256']==sha(raw),'matrix raw-method binding differs')
 log=(artifacts/'api35/logcat.txt').read_bytes();receipt=bind_method(log.decode(),tags)
 api30log=(artifacts/'api30/logcat.txt').read_bytes();require(MARKER not in api30log.decode() and ('started: '+IDENTITY[1]+'(') not in api30log.decode(),'ineligible platform method/receipt unexpectedly ran on API30')
 return receipt|{'status':'PASS_BOUND_INSTALLED_PLATFORM_LOCALE_DISCOVERY','head':HEAD,'tree':TREE,'merge':MERGE,'run_id':int(RUN),'source_tests_sha256':SOURCE_SHA,'source_inputs':[{'path':p,'sha256':sha(raw)} for p,raw in sources.items()],'logcat_sha256':sha(log),'api30_logcat_sha256':sha(api30log),'ordinary_protocol_sha256':sha(raw),'method_protocol_events':target_events,'matrix_result_sha256':sha(matrix_path.read_bytes()),'prebuilt_result_sha256':sha(provenance_path.read_bytes()),'api30_status':'EXCLUDED_BY_CURRENT_SOURCE_API33_MINIMUM; NO_RECEIPT','api33_constructor_status':'UNRUN_BY_NORMAL_API30_API35_MATRIX','limits':['Framework manifest/resource discovery ignores overrides on exercised API35. No Android Settings UI visibility or translation-completeness observation.','API33 constructor fallback reviewed in exact source but never run in this matrix.','Full raw phase/JUnit and same-run prebuilt checks are required; there is no independent on-device APK hash.']}

if __name__=='__main__':
 p=argparse.ArgumentParser();[p.add_argument('--'+k,type=pathlib.Path,required=True) for k in ('repo','artifacts','matrix','provenance','output')];a=p.parse_args();r=audit(a.repo,a.artifacts,a.matrix,a.provenance);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('status','sdk','expected_count','actual_count','started_line','line','finished_line','api30_status','api33_constructor_status')},indent=2))
