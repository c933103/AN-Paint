#!/usr/bin/env python3
"""Read-only audit of terminal writer logs against current host discovery."""
import argparse,collections,hashlib,json,pathlib,re,sys,unittest

def require(v,m):
    if not v: raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def flatten(s):
    for test in s:
        if isinstance(test,unittest.TestSuite):yield from flatten(test)
        else:yield test.id()
def parse(text):
    pending=None;started=[];done=[];problems=[]
    for line in text.splitlines():
        m=re.match(r'^\S+ \(([^)]+)\) \.\.\. (.*)$',line)
        if m:
            if pending:problems.append('new method before terminal status: '+pending)
            pending=m.group(1);started.append(pending);status=m.group(2)
        elif pending and (line=='ok' or line.startswith(('FAIL','ERROR','skipped '))):status=line
        else:continue
        if status=='ok' or status.startswith(('FAIL','ERROR','skipped ')):
            done.append((pending,status));pending=None
    require(not pending,'interrupted method '+str(pending));require(not problems,str(problems))
    return started,done

def audit(repo,writer):
    sys.path.insert(0,str(repo/'tools'))
    expected=list(flatten(unittest.defaultTestLoader.discover(str(repo/'tools'),pattern='test_*.py')))
    require(not any('_FailedTest' in t for t in expected),'source discovery import error')
    expected_counter=collections.Counter(expected);require(all(v==1 for v in expected_counter.values()),'duplicate current identities')
    rows=[]
    for mode in ('ordinary','optimized'):
        receipt=writer/('final-host-'+mode+'.json');log=writer/('final-host-'+mode+'.log')
        r=json.loads(receipt.read_text());b=log.read_bytes();s=b.decode();started,done=parse(s)
        require(r['log_sha256']==sha(b) and r['log_bytes']==len(b),'log binding '+mode)
        require(r['source_tree_before']==r['source_tree_after']=='d2379b932cc976bb5347515887ecdfc4729ee70d','source tree '+mode)
        require(r['timeout_seconds']==240 and r['exit_code']==0,'cap/exit '+mode)
        require(collections.Counter(started)==expected_counter and collections.Counter(t for t,v in done)==expected_counter,'current identity coverage '+mode)
        require(all(v=='ok' for t,v in done),'non-passing method '+mode)
        summaries=re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$',s,re.M)
        require(len(summaries)==1 and int(summaries[0][0])==len(expected),'summary count '+mode)
        require(re.search(r'^OK$',s,re.M) is not None,'terminal OK '+mode)
        rows.append({'mode':mode,'status':'PASS','receipt_file':receipt.name,'receipt_sha256':sha(receipt.read_bytes()),'log_file':log.name,'log_sha256':sha(b),'bytes':len(b),'started':len(started),'passed':len(done),'missing':[],'unexpected':[],'skipped':0,'failed_or_error':0,'unittest_seconds':float(summaries[0][1]),'wrapper_seconds':r['elapsed_seconds'],'process_exit_code':r['exit_code'],'timeout_seconds':r['timeout_seconds']})
    return {'status':'PASS','candidate_tree':'d2379b932cc976bb5347515887ecdfc4729ee70d','current_source_discovered_identities':len(expected),'sorted_identity_list_sha256':sha(('\n'.join(sorted(expected))+'\n').encode()),'aggregate_checks':rows,'scope':'Terminal Python host logs independently reconciled against current source discovery. Deliberate negative-control JSON success:false outputs are not test failures. No Android execution claimed.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--writer-dir',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();r=audit(a.repo,a.writer_dir);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'current_identities':r['current_source_discovered_identities']}))
