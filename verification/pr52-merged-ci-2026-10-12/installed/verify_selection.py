#!/usr/bin/env python3
"""Verify this frozen selected packet; does not authenticate origin on its own."""
import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parent;m=json.loads((root/'DELIVERY-FILES.json').read_bytes());seen=set()
for x in m['files']:
 p=pathlib.PurePosixPath(x['path'])
 if p.is_absolute() or '..' in p.parts or '\\' in x['path'] or x['path'] in seen:raise ValueError('unsafe/duplicate selected path')
 seen.add(x['path']);b=(root/x['path']).read_bytes()
 if len(b)!=x['bytes'] or hashlib.sha256(b).hexdigest()!=x['sha256']:raise ValueError('selected bytes differ '+x['path'])
if len(seen)!=m['file_count']:raise ValueError('selected file count differs')
print(json.dumps({'status':'PASS_EXACT_SELECTED_BYTES','file_count':len(seen),'kind':m['kind'],'run_id':m['run_id']},indent=2))
