#!/usr/bin/env python3
"""Independent byte-level diagnostic successor scope audit against reviewed PR55 tree."""
import argparse,hashlib,json,pathlib,re,subprocess
BASE='d80218496e45bbefcaa378d40e5cd9846b7988ee'
FLOW='Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt'
MODIFIED={FLOW,'tools/commons_metadata_m04_composition_scope.py','tools/test_commons_metadata_m04_composition.py','tools/test_localized_dialog_composition.py'}
def sha(b):return hashlib.sha256(b).hexdigest()
def check(v,msg):
    if not v:raise ValueError(msg)
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
    repo=a.repo
    def git(*v):return subprocess.check_output(['git',*v],cwd=repo)
    old={}
    for row in git('ls-tree','-rz',BASE).split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t');mode,kind,blob=meta.decode().split();check(kind=='blob','nonblob leaf');old[path.decode()]=(mode,blob)
    changed=[];unchanged=[];manifest=[]
    for path,(mode,blob) in old.items():
        b=(repo/path).read_bytes();actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        (unchanged if actual==blob else changed).append(path)
        if path in MODIFIED:manifest.append({'path':path,'sha256':sha(b),'bytes':len(b)})
    check(set(changed)==MODIFIED,'modified baseline scope differs: '+str(changed))
    fpath='tools/fixtures/commons_metadata_m04_diagnostic_successor_scope.json';raw=(repo/fpath).read_bytes();fixture=json.loads(raw)
    helper=(repo/'tools/commons_metadata_m04_diagnostic_scope.py').read_text()
    check(re.search(r"SCOPE_PIN = '([0-9a-f]{64})'",helper)[1]==sha(raw),'new fixture pin differs')
    check(fixture['failed_tree']==BASE and fixture['expected_jvm_count']==890,'failed binding/count differs')
    check({e['path'] for e in fixture['entries']}==MODIFIED and len(fixture['entries'])==4,'new scope rows differ')
    endpoints=[]
    for row in fixture['entries']:
        path=row['path'];now=(repo/path).read_bytes();before=git('show',BASE+':'+path)
        check(sha(now)==row['after_sha256'] and sha(before)==row['before_sha256'],'actual endpoint differs: '+path)
        restored=now.decode()
        for edit in reversed(row['edits']):
            check(bool(edit['after']) and restored.count(edit['after'])==1,'nonunique delta '+path)
            restored=restored.replace(edit['after'],edit['before'],1)
        check(restored.encode()==before,'reverse does not recover actual immutable bytes: '+path)
        endpoints.append({'path':path,'before_sha256':sha(before),'after_sha256':sha(now),'edits':len(row['edits'])})
    old_flow=git('show',BASE+':'+FLOW).decode();new_flow=(repo/FLOW).read_text()
    methods=lambda t:re.findall(r'@Test\b.*?\bfun\s+(\w+)\(',t,re.S)
    check(methods(old_flow)==methods(new_flow) and len(methods(new_flow))==16,'flow test identity changed')
    guard='layout.getLineLeft(line)>=-1f && layout.getLineRight(line)<=layout.width+1f'
    check(old_flow.count(guard)==1 and new_flow.count(guard)==2,'original guard not retained plus diagnostic echo')
    check('assertTrue("Readability profile failures:\\n"+failures.joinToString("\\n"),failures.isEmpty())' in new_flow,'aggregate fail missing')
    check('if(!metadataFinished) throw failure' in new_flow,'inflight fail-fast missing')
    check('Capture must follow the completed reading-start layout' in new_flow,'reading-start assertion missing')
    allpaths=set(git('ls-files','--cached','--others','--exclude-standard','-z').decode().split('\0'))-{''}
    newpaths=sorted(allpaths-set(old))
    newsource=[s for s in newpaths if not s.startswith('verification/')]
    allowed={'tools/commons_metadata_m04_diagnostic_scope.py',fpath,'tools/test_commons_metadata_m04_diagnostic.py'}
    check(set(newsource)==allowed,'new source inventory not final/expected: '+str(newsource))
    for path in newsource:
        b=(repo/path).read_bytes();manifest.append({'path':path,'sha256':sha(b),'bytes':len(b)})
    result={'status':'PASS','baseline_tree':BASE,'baseline_leaves':len(old),'unchanged_leaves':len(unchanged),'modified_leaves':len(changed),'exact_reversed_endpoints':endpoints,'new_source_paths':sorted(newsource),'new_evidence_paths':[s for s in newpaths if s.startswith('verification/')],'source_manifest':sorted(manifest,key=lambda r:r['path']),'flow_test_identities':methods(new_flow),'original_guard_retained':True,'jvm_expected_count':890,'limits':['Static source/projection verification and host tests cannot establish Kotlin compilation, actual diagnostic generation or resolution of the original JVM failure.','Historical failed PR55 source and evidence remain bound to baseline tree; new hosted checks must bind the actual successor commit/tree.']}
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('flow_test_identities','source_manifest','new_evidence_paths','exact_reversed_endpoints')},indent=2))
if __name__=='__main__':main()
