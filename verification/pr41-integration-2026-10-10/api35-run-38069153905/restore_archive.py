#!/usr/bin/env python3
"""Restore the exact original Actions emulator ZIP from verified encoded parts."""
import argparse,base64,hashlib,json
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('original-device.zip'));args=p.parse_args()
    root=Path(__file__).resolve().parent;m=json.loads((root/'original-artifact-parts.json').read_text());chunks=[]
    for row in m['parts']:
        encoded=(root/row['path']).read_bytes()
        if len(encoded)!=row['encoded_bytes'] or hashlib.sha256(encoded).hexdigest()!=row['encoded_sha256']:raise ValueError('Encoded part differs: '+row['path'])
        raw=base64.b64decode(encoded,validate=True)
        if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('Decoded part differs: '+row['path'])
        chunks.append(raw)
    raw=b''.join(chunks)
    if len(raw)!=m['original_bytes'] or hashlib.sha256(raw).hexdigest()!=m['original_sha256']:raise ValueError('Original archive checksum mismatch')
    with args.output.open('xb') as f:f.write(raw)
    print(str(args.output)+': '+m['original_sha256'])

if __name__=='__main__':main()
