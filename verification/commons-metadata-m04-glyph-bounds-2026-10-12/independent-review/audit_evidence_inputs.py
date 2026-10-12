#!/usr/bin/env python3
"""Independent inventory arithmetic and historical-copy verification."""
import argparse,hashlib,json,pathlib,sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();r=a.repo
sys.path.insert(0,str(r/'tools'))
from run_android_instrumentation import declared_tests,source_tests_sha256
from app_instrumentation_matrix import app_partition
def check(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
e=r/'verification/commons-metadata-m04-glyph-bounds-2026-10-12'
j=json.loads((e/'expected-jvm-identities.json').read_bytes());old=(r/j['frozen_inventory_path']).read_bytes();oi=json.loads(old)
check(sha(old)==j['frozen_inventory_sha256'],'frozen JVM input differs')
check(j['expected']==oi['expected'] and len(j['expected'])==len(set(map(tuple,j['expected'])))==892,'JVM identity change')
check(j['added_execution_identities']==j['removed_execution_identities']==[],'JVM identity delta')
check(sha((r/'Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt').read_bytes())==j['flow_source_sha256'],'JVM flow binding')
d=json.loads((e/'expected-installed-identities.json').read_bytes());app=declared_tests(r/'app/src/androidTest',sdk_level=35);lib=declared_tests(r/'Paintroid/src/androidTest',sdk_level=35)
check(set(map(tuple,d['app_expected']))==app and set(map(tuple,d['library_expected']))==lib,'installed identity mismatch')
check(len(app)==30 and len(lib)==74 and d['api35_count']==104,'installed identity counts')
for key,path in [('app','app/src/androidTest'),('library','Paintroid/src/androidTest')]:
 check(d[key+'_source_tests_sha256']==source_tests_sha256(r/path),'installed source mismatch '+key)
ordinary=app_partition(app,35)['ordinary'];check(len(ordinary)==16,'ordinary partition changed')
d30=json.loads((e/'expected-api30-identities.json').read_bytes())
a30=declared_tests(r/'app/src/androidTest',sdk_level=30);l30=declared_tests(r/'Paintroid/src/androidTest',sdk_level=30)
parts30=app_partition(a30,30);scheduled30=set().union(*parts30.values())
check(len(a30)==24 and len(l30)==73 and len(scheduled30)==22,'API30 inventory counts')
check(set(map(tuple,d30['app_declared']))==a30 and set(map(tuple,d30['app_scheduled']))==scheduled30 and set(map(tuple,d30['library_scheduled']))==l30,'API30 inventory identities')
check(d30['declared_count']==97 and d30['scheduled_count']==95,'API30 declarations are not scheduled identities')
check(set(map(tuple,d30['explicit_api35_restart_omissions']))==a30-scheduled30 and len(a30-scheduled30)==2,'API30 explicit restart exclusions')
for key in ['app_source_tests_sha256','library_source_tests_sha256']:check(d30[key]==d[key],'API30 source digest differs '+key)
ex=json.loads((e/'native-artifact-expectations.json').read_bytes());stems=set()
horizontal=['en-GB','ain-Kana','ain-Latn','bo','ryu','fr','ar','ja','vi-Hani'];controls=['en-GB','ain-Kana','bo','ar','ja','vi-Hani'];mutants=['left-overflow','right-overflow','wholly-left-of-view','wholly-right-of-view','clip-first-spatial-ink','clip-last-spatial-ink'];resets=['width','font','mixed-paragraphs','short-message','restored']
for scale in ['1.0','2.0']:
 for tag in horizontal:
  for action in ['copy','insert']:stems.add(f'api35-{tag}-640x320-font{scale}-{action}')
 for tag in controls:
  prefix=f'api35-{tag}-640x320-font{scale}-negative-controls-'
  stems.add(prefix+'intact');stems.update(prefix+x for x in mutants);stems.update(prefix+'reset-'+x for x in resets)
stems.add('api35-ar-640x320-font2.0-negative-controls-original-plain-before')
check(len(stems)==181 and len(ex['stems'])==181 and set(ex['stems'])==stems,'native frame identity mismatch')
check(ex['expected_raster_pairs']==181 and ex['expected_rejected_mutations']==72,'native totals')
h=e/'failed-painted-ink-run';manifest=(h/'DELIVERY-FILES.json').read_bytes();check(sha(manifest)=='0508da090e90ebeea5dc6a57f5cc56852c71f95659b09599ab248fc4eda4131e','historical manifest changed')
hist=json.loads(manifest);check(len(hist['files'])==39,'historical deliverable inventory')
for row in hist['files']:
 b=(h/row['path']).read_bytes();check(sha(b)==row['sha256'] and len(b)==row['bytes'],'historical deliverable changed '+row['path'])
result={'status':'PASS','jvm_identities_unchanged':892,'api35_installed':{'library':74,'app':30,'ordinary_app':16,'total':104},'api30_installed':{'library':73,'app_scheduled':22,'app_declared':24,'explicit_restart_omissions':2,'scheduled_total':95,'declared_total':97},'app_test_source_sha256':d['app_source_tests_sha256'],'library_test_source_sha256':d['library_source_tests_sha256'],'native_triplets':{'live':36,'intact':12,'mutants':72,'reset_reflow':60,'original_plain_before':1,'total':181},'native_aggregate_summaries':4,'historical_artifact_review_files_exact':39,'historical_delivery_manifest_sha256':sha(manifest),'limits':'Inventory expectations and preserved history are not current native or installed execution evidence.'}
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
