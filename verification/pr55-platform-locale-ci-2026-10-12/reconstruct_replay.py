from pathlib import Path
import hashlib, json
root=Path(__file__).resolve().parent
m=json.loads((root/'TRANSPORT.json').read_text())
chunks=[]
for row in m['parts']:
    b=(root/row['path']).read_bytes()
    if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:
        raise SystemExit('Part verification failed: '+row['path'])
    chunks.append(b)
b=b''.join(chunks)
if len(b)!=m['original_bytes'] or hashlib.sha256(b).hexdigest()!=m['original_sha256']:
    raise SystemExit('Full archive verification failed')
(root/m['original_path']).write_bytes(b)
print('Verified',m['original_path'],len(b),m['original_sha256'])
