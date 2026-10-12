#!/usr/bin/env python3
import argparse,gzip,hashlib,json,pathlib
p=argparse.ArgumentParser();p.add_argument('--log',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();raw=a.log.read_bytes();data=gzip.decompress(raw) if a.log.suffix=='.gz' else raw;s=data.decode('utf-8-sig');lines=s.splitlines()
fragments=['fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +daab4b4f2c87bc6475ba6a0d2c0f9b35ea36b7e0:refs/remotes/pull/55/merge','HEAD is now at daab4b4 Merge da4b40bd47a5d76d45b21d86fdc59368b4b52fd2 into 71f4d288669858e7975ec4c094b7f47a9a1ff145','> Task :Paintroid:compileDebugUnitTestKotlin','906 tests completed, 4 failed','Final size is 78306620 bytes. Artifact ID is 11764101989','https://github.com/c933103/AN-Paint/actions/runs/38285607590/artifacts/11764101989','459d6ddd95b4ae8f3126477cf8d45d8c01182bf4b342ddb3f1e77e68abae9e7e']
rows=[]
for f in fragments:
 hits=[{'line':i+1,'text':v} for i,v in enumerate(lines) if f in v]
 if len(hits)!=1:raise ValueError('expected unique job receipt '+f)
 rows.extend(hits)
r={'status':'PASS_LOG_SOURCE_AND_UPLOAD_BINDING','run_id':38285607590,'source_merge':'daab4b4f2c87bc6475ba6a0d2c0f9b35ea36b7e0','artifact_id':11764101989,'log_sha256':hashlib.sha256(data).hexdigest(),'log_bytes':len(data),'evidence_lines':rows,'limits':['Remote log/run authenticity is provided by parent verified GitHub receipt.','This confirms the failed exact-source JVM run; it does not relabel its four assertions as passed.']};a.output.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
