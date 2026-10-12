#!/usr/bin/env python3
import argparse,gzip,hashlib,json,pathlib
p=argparse.ArgumentParser();p.add_argument('--log',type=pathlib.Path,required=True);p.add_argument('--binding',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();raw=a.log.read_bytes();data=gzip.decompress(raw) if a.log.suffix=='.gz' else raw;s=data.decode('utf-8-sig');lines=s.splitlines();b=json.loads(a.binding.read_text())
fragments=[f"fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +{b['merge']}:refs/remotes/pull/52/merge",f"HEAD is now at {b['merge'][:7]} Merge {b['head']} into {b['base']}",'> Task :Paintroid:compileDebugUnitTestKotlin','> Task :Paintroid:testDebugUnitTest',f"Final size is {b['regression_artifact_bytes']} bytes. Artifact ID is {b['regression_artifact_id']}",f"https://github.com/c933103/AN-Paint/actions/runs/{b['run_id']}/artifacts/{b['regression_artifact_id']}",b['regression_artifact_sha256']]
rows=[]
for f in fragments:
 hits=[{'line':i+1,'text':v} for i,v in enumerate(lines) if f in v]
 if len(hits)!=1:raise ValueError('expected unique job receipt '+f)
 rows.extend(hits)
compile_line=next(x['line'] for x in rows if ':compileDebugUnitTestKotlin' in x['text']);test_line=next(x['line'] for x in rows if ':testDebugUnitTest' in x['text']);success=[{'line':i+1,'text':v} for i,v in enumerate(lines) if i+1>test_line and 'BUILD SUCCESSFUL' in v]
if not success or not compile_line<test_line<success[0]['line']:raise ValueError('missing successful native test completion')
rows.append(success[0]);r={'status':'PASS_LOG_SOURCE_AND_UPLOAD_BINDING','run_id':b['run_id'],'source_merge':b['merge'],'artifact_id':b['regression_artifact_id'],'log_sha256':hashlib.sha256(data).hexdigest(),'log_bytes':len(data),'evidence_lines':sorted(rows,key=lambda x:x['line']),'limits':['Remote log/run authenticity is provided by parent verified GitHub receipt.','Full source-derived JUnit and phase audit separately establishes exact executed identities and exit status.']};a.output.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
