#!/usr/bin/env python3
"""Bind final and failed writer receipts; distinguish split coverage from an aggregate pass."""
import argparse,hashlib,json,pathlib,re,sys,unittest
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();r=a.repo.resolve();e=r/'verification/commons-metadata-m04-glyph-bounds-2026-10-12'
def check(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def statuses(text):
 completed={};pending=None
 for line in text.splitlines():
  match=re.match(r'^test_\S+ \(([^)]+)\) \.\.\. (.*)$',line)
  if match:
   pending=match[1];line=match[2]
  if line in ('ok','FAIL','ERROR') and pending:
   check(pending not in completed,'duplicate terminal method '+pending);completed[pending]=line;pending=None
 return completed
raw=(e/'local-verification.json').read_bytes();check(sha(raw)=='02cd891a3f6a5b2c39cd1e2b732ea74379cab405178350b8f91e6717340c21f3','unreviewed writer receipt');v=json.loads(raw)
sraw=(e/'supplemental-unexecuted-tail.json').read_bytes();check(sha(sraw)=='9e8e04602ca957219340db03745af80003cbb0768b065e5c9ae57375937be4c2','unreviewed supplemental receipt');supp=json.loads(sraw)
for path,digest in v['source_sha256'].items():check(sha((r/path).read_bytes())==digest,'source changed '+path)
rows=[];by_log={}
for row in v['checks']+v['preserved_development_aggregate_attempts']:
 if 'log' not in row:continue
 b=(e/row['log']).read_bytes();check(sha(b)==row['log_sha256'],'writer log changed '+row['log']);text=b.decode();seen=statuses(text);by_log[row['log']]=seen
 rows.append({'log':row['log'],'sha256':sha(b),'bytes':len(b),'process_exit_code':row['exit_code'],'completed_ok_methods':sum(x=='ok' for x in seen.values()),'failed_methods':[k for k,x in seen.items() if x!='ok'],'terminal_summaries':re.findall(r'^Ran (\d+) tests? in ([0-9.]+)s$',text,re.M)})
full=by_log['all-host.log'];check(len(full)==703 and set(full.values())=={'ok'},'final partial status differs')
for name in ['all-host-timeout-first.log','all-host-timeout-second.log']:check(sum(v!='ok' for v in by_log[name].values())==3,'historical failures not preserved')
b=(e/'supplemental-unexecuted-tail.log').read_bytes();check(sha(b)==supp['log_sha256'],'supplement log changed');tail=statuses(b.decode());check(len(tail)==10 and set(tail.values())=={'ok'},'supplement not 10 passing methods')
check(set(tail)==set(supp['supplemental_identities']),'supplement identities differ')
sys.path.insert(0,str(r/'tools'));suite=unittest.TestLoader().discover(str(r/'tools'),pattern='test_*.py')
def flatten(s):
 for x in s:
  if isinstance(x,unittest.TestSuite):yield from flatten(x)
  else:yield x.id()
expected=list(flatten(suite));check(len(expected)==len(set(expected))==712,'fresh host inventory differs')
check(set(full)|set(tail)==set(expected),'split coverage does not match complete host inventory')
check(len(set(full)&set(tail))==1 and set(full)&set(tail)==set(supp['previously_completed_replayed_identities']),'replayed warning-wrapped method differs')
result={'status':'MIXED: complete split method coverage; full aggregate remains timed out','local_verification_sha256':sha(raw),'supplemental_receipt_sha256':sha(sraw),'source_manifest_sha256':v['source_manifest_sha256'],'source_pins_verified':len(v['source_sha256']),'writer_checks_independently_bound':rows,'final_full_completed':703,'supplemental_passed':10,'supplemental_new':9,'supplemental_replayed':1,'fresh_discovered_host_identities':expected,'split_union_count':712,'full_aggregate_pass':False,'full_aggregate_exit':124,'deadline_seconds':240,'counting_note':'The warning-wrapped test_dialog_evidence_transport method completes with a standalone ok line; it is not missing from the aggregate.','execution_attribution':'Reviewer read/hashed the writer-run logs and independently recomputed method inventory; reviewer-executed focused logs are separate.','limits':'Split coverage is not a passing single aggregate or proof of Android/native/installed behavior.'}
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['fresh_discovered_host_identities','writer_checks_independently_bound']},indent=2))
