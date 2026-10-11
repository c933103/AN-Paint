#!/usr/bin/env python3
"""Replay durable packets. The optional original build archive enables fresh APK/source replay."""
import argparse,base64,hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--directory',type=Path,required=True);p.add_argument('--build-archive',type=Path);a=p.parse_args();root=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verify',root/'verify_ci.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
a.directory.mkdir(parents=True,exist_ok=False);m.safe_extract(root/'host-raw-evidence.zip',a.directory)
manifest=json.loads((a.directory/'manifest.json').read_text())['candidate']
for name,meta in manifest.items():
 f=a.source/name;m.require(f.is_file(),'Missing source file '+name);b=f.read_bytes();actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();m.require(actual==meta.split()[2],'Source mismatch '+name)
 m.require(bool(f.stat().st_mode&0o111)==(meta.split()[0]=='100755'),'Source mode mismatch '+name)
parts=json.loads((root/'retained-parts.json').read_text())
for name,archive in parts['archives'].items():
 chunks=[]
 for row in archive['parts']:
  data=(root/row['path']).read_bytes();gitsha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();m.require(gitsha==row['git_blob_sha1'],'Stored part mismatch '+row['path'])
  if row['encoding']=='base64-utf8':
   data=base64.b64decode(b''.join(data.split()),validate=True);size=row['raw_bytes'];sha=row['raw_sha256']
  else:size=row['bytes'];sha=row['sha256']
  m.require(len(data)==size and m.digest(data)==sha,'Raw part mismatch '+row['path']);chunks.append(data)
 data=b''.join(chunks);m.require(len(data)==archive['bytes'] and m.digest(data)==archive['sha256'],'Archive mismatch '+name)
 dest=a.directory/name;dest.write_bytes(data);m.safe_extract(dest,a.directory)
sys.path.insert(0,str(a.source/'tools'))
from vertical_evidence_transport import extract
results={'generator':m.generator(a.directory/'generator',a.source),'regression':m.regression(a.directory/'regression',a.source)}
for sdk in [30,35]:
 d=a.directory/f'device{sdk}';extract(d/'vertical-locale-export',d/'app/vertical-locale-evidence',sdk);results[f'device{sdk}']=m.device(d,a.source,sdk)
subprocess.run([sys.executable,str(a.directory/'verify_compiled_resources.py'),'--source',str(a.source),'--dump',str(a.directory/'compiled-resources.txt'),'--output',str(a.directory/'replayed-compiled.json')],check=True)
m.require(json.loads((a.directory/'replayed-compiled.json').read_text())==json.loads((a.directory/'compiled-resources-receipt.json').read_text()),'Compiled receipt mismatch')
results['compiled_resources']='pass'
if a.build_archive:results['build']=m.build(a.build_archive,manifest)
else:results['build']='Not replayed: supply the original --build-archive. Published prior build receipt remains separate.'
(a.directory/'replayed-results.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS: retained host, generator, both complete device/transport/image/trace sets and compiled resources. Actual-pixel review is recorded separately. '+('APK/source replay also passed.' if a.build_archive else 'APK/source bytes were not replayed.'))
