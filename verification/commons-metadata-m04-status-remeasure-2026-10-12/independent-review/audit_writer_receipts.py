#!/usr/bin/env python3
"""Bind exact writer receipts and accurately retain the incomplete aggregate."""
import argparse,hashlib,json,pathlib,re,sys,unittest
RECEIPT_SHA='d5f64d65ef4d55b143f7d25e4f625bfdae427c92fd70d4240ae5f5167292e308'
MANIFEST_SHA='4994c68e3929406659e0bafca2d3b9dfd9550d2fc35583c56f8bb4edc391b267'
def check(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def statuses(text):
 done={};started=[];pending=None
 for line in text.splitlines():
  m=re.match(r'^test_\S+ \(([^)]+)\) \.\.\. (.*)$',line)
  if m:pending=m[1];started.append(pending);line=m[2]
  status=line if line in ('ok','FAIL','ERROR') else 'skipped' if line.startswith('skipped ') else None
  if status and pending:check(pending not in done,'duplicate completed identity');done[pending]=status;pending=None
 return done,started,pending

def main():
 p=argparse.ArgumentParser()
 for k in ('repo','writer-root','output'):p.add_argument('--'+k,type=pathlib.Path,required=True)
 a=p.parse_args();root=a.writer_root;raw=(root/'anpaint-pr55-receiver-local-verification.json').read_bytes();check(sha(raw)==RECEIPT_SHA,'writer receipt changed');v=json.loads(raw)
 mraw=(root/'anpaint-pr55-receiver-source-manifest.json').read_bytes();check(sha(mraw)==MANIFEST_SHA==v['source_manifest_sha256'],'source manifest changed');manifest=json.loads(mraw)
 for f in manifest['files']:check(sha((a.repo/f['path']).read_bytes())==f['sha256'],'source changed '+f['path'])
 rows={};full=None
 for label,receipt in v['receipts'].items():
  b=(root/receipt['path']).read_bytes();check(sha(b)==receipt['sha256'],'writer log changed '+label);text=b.decode();done,started,pending=statuses(text)
  check(re.findall(r'^PROCESS_EXIT_CODE=(\d+)$',text,re.M)==[str(receipt['exit_code'])],'raw saved exit differs '+label)
  if label in ('normal','optimized'):
   check(len(done)==135 and set(done.values())=={'ok'} and not pending,'focused status differs')
   check(re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$',text,re.M)==[('135',str(receipt['seconds']))] and re.search(r'^OK$',text,re.M),'focused summary differs')
  elif label=='aggregate':
   check(len(done)==407 and len(started)==408 and set(done.values())=={'ok'},'partial counts differ')
   check(pending=='test_legacy_compatibility.LegacyInventoryTest.test_current_legacy_omission_is_explicit_and_never_a_test_pass','interrupted identity differs')
   check(not re.search(r'^Ran \d+ tests',text,re.M) and receipt['exit_code']==124 and receipt['cap_seconds']==240 and 'real\t4m0.007s' in text,'aggregate timeout receipt differs');full=done
  else:check(label=='launch_unrun' and not started and '/usr/bin/time: No such file or directory' in text and receipt['exit_code']==127,'launch receipt differs')
  rows[label]={'sha256':sha(b),'saved_exit':receipt['exit_code'],'started':len(started),'completed':len(done),'statuses':{x:list(done.values()).count(x) for x in set(done.values())},'pending':pending}
 sys.path.insert(0,str(a.repo/'tools'));suite=unittest.TestLoader().discover(str(a.repo/'tools'),pattern='test_*.py')
 def flatten(s):
  for x in s:
   if isinstance(x,unittest.TestSuite):yield from flatten(x)
   else:yield x.id()
 expected=list(flatten(suite));check(len(expected)==len(set(expected))==719,'discovered host inventory differs');check(set(full)<=set(expected),'completed method not in source inventory')
 result={'status':'INCOMPLETE_FULL_AGGREGATE','writer_receipt_sha256':sha(raw),'writer_source_manifest_sha256':sha(mraw),'source_pins_verified':len(manifest['files']),'receipts':rows,'expected_discovered':719,'aggregate_completed':407,'aggregate_not_completed':312,'aggregate_pass':False,'count_note':'Warning-wrapped duplicate-ZIP test has standalone ok; count includes it. No completed method failed or skipped.','execution_attribution':'Reviewer read/hashed writer logs and discovered identities; reviewer independently executed focused checks are separate.','limits':'No single aggregate pass and no fresh Android/runtime success are claimed.'}
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
