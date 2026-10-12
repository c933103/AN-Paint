#!/usr/bin/env python3
"""Portable independent byte-level oracle-successor audit; no project imports."""
import argparse, hashlib, json, os, pathlib, re, subprocess
BASE='4ff7f479ffc73964fa8756b6c7e3202f624ad0f1'
FLOW='Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt'
MODIFIED={FLOW,'tools/commons_metadata_m04_diagnostic_scope.py','tools/test_commons_metadata_m04_diagnostic.py'}
FIXTURE='tools/fixtures/commons_metadata_m04_painted_ink_successor_scope.json'
NEW={'tools/commons_metadata_m04_painted_ink_scope.py',FIXTURE,'tools/test_commons_metadata_m04_painted_ink.py'}
EVIDENCE='verification/commons-metadata-m04-painted-ink-2026-10-12/'
ADDED={'paintedInkOracleRejectsNativeOverflowAndClippedEdgeGlyphsAtNormalScale','paintedInkOracleRejectsNativeOverflowAndClippedEdgeGlyphsAtDoubleScale'}
FLOW_SHA='44651d7001dcc01ba37a7c7ff0b650785fa9b4204f4bcc75e6fcabd7e67e8816'
FIXTURE_SHA='3e7fb249d1334ee1bb9b0ecbe647a9a34b83452e248e772854a40e7721a9efdf'
def sha(b):return hashlib.sha256(b).hexdigest()
def check(v,msg):
    if not v:raise ValueError(msg)
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();repo=a.repo
    def git(*v):return subprocess.check_output(['git',*v],cwd=repo)
    old={}
    for row in git('ls-tree','-rz',BASE).split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t');mode,kind,blob=meta.decode().split();check(kind=='blob','nonblob leaf');old[path.decode()]=(mode,blob)
    check(len(old)==1975,'wrong baseline inventory')
    changed=[];unchanged=[]
    for path,(mode,blob) in old.items():
        file=repo/path;check(file.is_file() and not file.is_symlink(),'missing/nonregular leaf '+path)
        b=file.read_bytes();actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        check(bool(file.stat().st_mode&0o111)==(mode=='100755'),'executable mode changed '+path)
        (unchanged if actual==blob else changed).append(path)
    check(set(changed)==MODIFIED,'baseline scope differs: '+str(changed))
    raw=(repo/FIXTURE).read_bytes();check(sha(raw)==FIXTURE_SHA,'not reviewed fixture');scope=json.loads(raw)
    check(sha((repo/FLOW).read_bytes())==FLOW_SHA,'not reviewed flow')
    check(re.search(r"SCOPE_PIN = '([0-9a-f]{64})'",(repo/'tools/commons_metadata_m04_painted_ink_scope.py').read_text())[1]==FIXTURE_SHA,'fixture pin differs')
    check(scope['diagnostic_tree']==BASE and scope['expected_jvm_count']==892,'base/count differs')
    check({r['path'] for r in scope['entries']}==MODIFIED and len(scope['entries'])==3,'inverse scope differs')
    endpoints=[]
    for row in scope['entries']:
        path=row['path'];before=git('show',BASE+':'+path);now=(repo/path).read_bytes()
        check(sha(before)==row['before_sha256'] and sha(now)==row['after_sha256'],'endpoint hash mismatch '+path)
        text=now.decode()
        for edit in reversed(row['edits']):
            check(edit['after'] and text.count(edit['after'])==1,'nonunique inverse '+path)
            text=text.replace(edit['after'],edit['before'],1)
        check(text.encode()==before,'inverse differs from actual immutable Git blob '+path)
        endpoints.append({'path':path,'before_sha256':sha(before),'after_sha256':sha(now),'exact_reverse_edits':len(row['edits'])})
    methods=lambda t:re.findall(r'@Test\b(?:(?!\bfun\b).)*\bfun\s+(\w+)\s*\(',t,re.S)
    old_methods=methods(git('show',BASE+':'+FLOW).decode());new_methods=methods((repo/FLOW).read_text())
    check(len(old_methods)==16 and len(new_methods)==18 and set(new_methods)-set(old_methods)==ADDED and set(old_methods)<=set(new_methods),'Kotlin identity delta differs')
    allpaths=set(git('ls-files','--cached','--others','--exclude-standard','-z').decode().split('\0'))-{''}
    added=sorted(allpaths-set(old));newsource={p for p in added if not p.startswith('verification/')}
    check(newsource==NEW,'new source inventory differs: '+str(newsource))
    check(all(p.startswith(EVIDENCE) for p in added if p.startswith('verification/')),'unexpected new evidence root')
    invpath=EVIDENCE+'expected-jvm-identities.json';inv=json.loads((repo/invpath).read_bytes());oldinv=(repo/inv['frozen_inventory_path']).read_bytes();oi=json.loads(oldinv)
    check(sha(oldinv)==inv['frozen_inventory_sha256'] and inv['flow_source_sha256']==FLOW_SHA,'JVM binding differs')
    oldset=set(map(tuple,oi['expected']));newset=set(map(tuple,inv['expected']));delta=set(map(tuple,inv['added_execution_identities']))
    check(len(oi['expected'])==len(oldset)==890 and len(inv['expected'])==len(newset)==892 and newset==oldset|delta and len(delta)==2 and inv['removed_execution_identities']==[],'JVM inventory differs')
    check({row[1] for row in delta}==ADDED,'new JUnit method identities differ')
    failurepath=EVIDENCE+'historical-failure-binding.json';failure=json.loads((repo/failurepath).read_bytes())
    for row in failure['files']:check(sha((repo/row['path']).read_bytes())==row['sha256'],'historical failure copy changed '+row['path'])
    original=failure['distinct_original_failed_checkpoint'];receipt=(repo/original['receipt_path']).read_bytes();check(sha(receipt)==original['receipt_sha256'],'first-run receipt differs');r=json.loads(receipt)
    for akey,bkey in [('head','head'),('tree','source_tree'),('run','run'),('synthetic_merge','synthetic_merge')]:check(original[akey]==r[bkey],'first-run binding differs '+akey)
    source=[]
    for path in sorted(MODIFIED|NEW|{invpath,failurepath}):
        b=(repo/path).read_bytes();source.append({'path':path,'sha256':sha(b),'bytes':len(b)})
    result={'status':'PASS','reviewed_baseline_tree':BASE,'baseline_leaves':len(old),'unchanged_leaves':len(unchanged),'modified_leaves':len(changed),'exact_inverse_endpoints':endpoints,'new_source_paths':sorted(NEW),'new_evidence_paths':[p for p in added if p.startswith('verification/')],'source_binding':source,'jvm_count':892,'added_jvm_identities':sorted(delta),'old_fixture_and_evidence_preservation':'All existing baseline bytes and executable modes unchanged except the three enumerated inverse-exact files','limits':['Static review and host tests do not establish Kotlin compilation or native execution.','Fresh source-bound hosted acceptance requires 892 exact successful identities, 112 success PNG/JSON pairs, 28 diagnostics, 120 paired ink frames and two control receipts.']}
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['new_evidence_paths','source_binding','exact_inverse_endpoints']},indent=2))
if __name__=='__main__':main()
