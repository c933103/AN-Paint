#!/usr/bin/env python3
"""Verify this independent review and, optionally, its sealed input."""
from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((root/'MANIFEST.json').read_text())
for n,h in m['files'].items():
    assert sha(root/n)==h,n
if len(sys.argv)>1:
    inp=Path(sys.argv[1]);assert sha(inp/'MANIFEST.json')==m['input_manifest_sha256']
    for n,h in json.loads((inp/'MANIFEST.json').read_text())['files'].items():assert sha(inp/n)==h,n
print(json.dumps({'review_files_verified':len(m['files']),'manifest_sha256':sha(root/'MANIFEST.json'),'input_checked':len(sys.argv)>1},indent=2))
