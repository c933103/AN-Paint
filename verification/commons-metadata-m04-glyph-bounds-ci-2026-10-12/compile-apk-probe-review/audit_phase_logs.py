#!/usr/bin/env python3
"""Exact failed glyph-bounds run phase receipts; compile failure is not a render failure."""
import argparse,hashlib,json,pathlib,re
from audit_glyph_artifacts import TREE,HEAD,MERGE,RUN,require

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser()
 for k in ('extracted','job-log','output'):p.add_argument('--'+k,type=pathlib.Path,required=True)
 a=p.parse_args();base=a.extracted/'build/reports/ci-phases';job=a.job_log.read_text(encoding='utf-8-sig')
 require(MERGE in job and 'HEAD is now at b750c54 Merge '+HEAD in job,'raw job checkout binding')
 phases={}
 for name,code in [('python',0),('jvm',1),('native',0),('lint',0)]:
  timing=(base/(name+'.time')).read_bytes();log=(base/(name+'.log')).read_bytes()
  fields=dict(x.split('=',1) for x in timing.decode().splitlines());require(int(fields['exit_status'])==code,'phase exit mismatch '+name)
  phases[name]={'exit':code,'timing':fields,'log_sha256':sha(log),'time_sha256':sha(timing),'started_at':(base/(name+'.started-at')).read_text().strip(),'ended_at':(base/(name+'.ended-at')).read_text().strip()}
  if name in ('native','lint'):require('BUILD SUCCESSFUL' in log.decode() and 'BUILD FAILED' not in log.decode(),'phase failure '+name)
 py=(base/'python.log').read_text();require(re.search(r'^Ran 712 tests in 193\.013s\n\nOK \(skipped=2\)$',py,re.M),'host aggregate summary mismatch')
 require(not re.search(r'^(FAIL:|ERROR:|FAILED \()',py,re.M),'host test failure')
 jvm=(base/'jvm.log').read_text();errors=re.findall(r'^e: (.*)$',jvm,re.M)
 require(len(errors)==1 and errors[0].endswith('CommonsMetadataQueryFailureFlowTest.kt:648:86 Val cannot be reassigned'),'unexpected compiler errors')
 require('> Task :Paintroid:compileDebugUnitTestKotlin FAILED' in jvm and 'BUILD FAILED' in jvm,'compiler phase receipt')
 require(not list(a.extracted.rglob('TEST-*.xml')),'unexpected JVM XML: reclassify evidence')
 roots=['commons-metadata-m04','commons-metadata-m04-diagnostic','commons-metadata-m04-painted-ink']
 require(not any((a.extracted/'Paintroid/build/reports'/x).exists() for x in roots),'unexpected native evidence: reclassify')
 result={'review_status':'FAIL_COMPILE_BLOCKER','tree':TREE,'head':HEAD,'merge':MERGE,'run_id':int(RUN),'phases':phases,'compiler_errors':errors,'jvm_execution':'UNRUN: Kotlin test compilation stopped before any JVM identity or render','expected_unrun':{'jvm_identities':892,'success_render_pairs':112,'diagnostic_profiles':28,'strict_ink_triplets':181,'control_summaries':4},'host_aggregate':{'ran':712,'skipped':2,'unittest_seconds':193.013,'exit':0,'limits':'The two skips are reported honestly; compact hosted log does not identify their names. Later negative-control JSON success:false fields are not aggregate failures.'},'job_log_sha256':sha(a.job_log.read_bytes()),'limitation':'Native phase here is library preparation, not JVM or installed raster execution. Installed phase artifacts are independent.'}
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
