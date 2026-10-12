from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
transport=json.loads((root/'TRANSPORT.json').read_text())
manifest_raw=(root/'DELIVERY-FILES.json').read_bytes()
if hashlib.sha256(manifest_raw).hexdigest()!=transport['frozen_delivery_manifest_sha256']:raise ValueError('frozen manifest mismatch')
original=next(r for r in json.loads(manifest_raw)['files'] if r['path']=='regression-replay-inputs.zip')
if transport['original_path']!=original['path'] or transport['original_bytes']!=original['bytes'] or transport['original_sha256']!=original['sha256']:raise ValueError('original ZIP binding mismatch')
chunks=[]
for index,row in enumerate(transport['parts'],1):
    if row['path']!=f'parts/regression-replay-inputs.zip.part{index:03d}':raise ValueError('part order/path mismatch')
    data=(root/row['path']).read_bytes()
    if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:raise ValueError('part mismatch')
    chunks.append(data)
data=b''.join(chunks)
if len(data)!=original['bytes'] or hashlib.sha256(data).hexdigest()!=original['sha256']:raise ValueError('reconstructed ZIP mismatch')
target=root/original['path']
if target.exists() and target.read_bytes()!=data:raise ValueError('existing ZIP differs; refusing overwrite')
if not target.exists():target.write_bytes(data)
print('Verified original replay ZIP:',target.name,len(data),original['sha256'])
