#!/usr/bin/env python3
"""One-time final aggregate receipt audit against current unittest discovery."""
import argparse,collections,hashlib,json,pathlib,re,sys,unittest
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--writer-evidence',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();sys.dont_write_bytecode=True
sys.path.insert(0,str(a.repo/'tools'))
def require(ok,why):
 if not ok:raise ValueError(why)
def flatten(suite):
 for item in suite:
  if isinstance(item,unittest.TestSuite):yield from flatten(item)
  else:yield item.id()
expected=list(flatten(unittest.TestLoader().discover(str(a.repo/'tools'),pattern='test_*.py')))
require(len(expected)==len(set(expected)),'duplicate discovered identities')
rows=[]
for mode in ('ordinary','optimized'):
 rp=a.writer_evidence/f'final-host-{mode}.json';lp=a.writer_evidence/f'final-host-{mode}.log';record=json.loads(rp.read_text());raw=lp.read_bytes();text=raw.decode()
 require(hashlib.sha256(raw).hexdigest()==record['log_sha256'],'raw log digest mismatch')
 require(record['exit_code']==0 and record['timeout_seconds']==240,'process result/cap')
 require(record['source_tree_before']==record['source_tree_after']=='592a60877524c5c118695cb45a4d0d5cd257b25a','source binding')
 started=[];passed=[];pending=None
 for line in text.splitlines():
  match=re.match(r'^test_\S+ \(([^)]+)\) \.\.\. (.*)$',line)
  if match:
   require(pending is None,'new method before previous terminal')
   pending=match.group(1);started.append(pending);status=match.group(2)
   if status=='ok':passed.append(pending);pending=None
   elif status.startswith(('FAIL','ERROR','skipped','expected failure','unexpected success')):raise ValueError('non-pass '+line)
  elif pending and line=='ok':passed.append(pending);pending=None
 require(pending is None,'incomplete pending method')
 require(collections.Counter(started)==collections.Counter(expected),'started source inventory mismatch')
 require(collections.Counter(passed)==collections.Counter(expected),'passed source inventory mismatch')
 require(re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$',text,re.M)==[(str(len(expected)),str(record['unittest_summaries'][0]['seconds']))],'unittest summary mismatch')
 require(re.findall(r'^(?:OK(?: \(.*\))?|FAILED \(.*\))$',text,re.M)==['OK'],'terminal summary')
 rows.append({'mode':mode,'status':'PASS','discovered_started_and_passed':len(expected),'exit_code':record['exit_code'],'seconds':record['unittest_summaries'][0]['seconds'],'log_sha256':record['log_sha256'],'receipt_sha256':hashlib.sha256(rp.read_bytes()).hexdigest(),'known_wrapped_status':'Duplicate-name negative-control warning followed by standalone ok is counted once','late_failure_json':'Intentional negative-control result objects after the unittest summary are not failed unittest identities'})
result={'status':'PASS','current_discovered_count':len(expected),'runs':rows,'source_tree':'592a60877524c5c118695cb45a4d0d5cd257b25a','limits':'Host execution only. Does not execute or certify Android/native runtime.'}
a.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS: exact',len(expected),'current identities started and passed in both full modes')
