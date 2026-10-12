#!/usr/bin/env python3
"""Independent local redaction check; never emits cookie values or value hashes."""
import argparse,gzip,hashlib,io,json,pathlib,re,tarfile,zipfile
p=argparse.ArgumentParser();p.add_argument('--original',type=pathlib.Path,required=True);p.add_argument('--sanitized',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,s):
 if not v:raise ValueError(s)
def selection(root):
 m=root/'DELIVERY-FILES.json';d=json.loads(m.read_text());seen=set()
 for row in d['files']:
  name=row['path'];pp=pathlib.PurePosixPath(name);require(not pp.is_absolute() and '..' not in pp.parts and '\\' not in name and name not in seen,'selection path');seen.add(name)
  f=root/name;require(not f.is_symlink(),'selection symlink');b=f.read_bytes();require(len(b)==row['bytes'] and sha(b)==row['sha256'],'selection integrity')
 return d,sha(m.read_bytes())
def members(root):
 with tarfile.open(root/'supporting-evidence.tar.gz') as t:
  items=t.getmembers();names=[i.name for i in items];require(len(names)==len(set(names)) and all(i.isfile() for i in items),'TAR member type/uniqueness');return {i.name:t.extractfile(i).read() for i in items}
o,oh=selection(a.original);n,nh=selection(a.sanitized);old,new=members(a.original),members(a.sanitized)
require(old.keys()==new.keys(),'support inventory changed');changed=[k for k in old if old[k]!=new[k]];name='current-inputs/api30/logcat.txt';require(changed==[name],'unexpected support member change')
x,y=old[name].splitlines(keepends=True),new[name].splitlines(keepends=True);require(len(x)==len(y)==38173,'line count');changed_lines=[i for i,(u,v) in enumerate(zip(x,y),1) if u!=v];require(changed_lines==[20476],'unexpected line change')
line=x[20475];require(b'NetworkMonitor/101: PROBE_FALLBACK http://www.google.com/gen_204 ' in line,'probe context');start=line.index(b'headers={');end=line.rindex(b'}')+1
require(y[20475]==line[:start]+b'headers={[REDACTED: third-party response headers]}'+line[end:],'outside-field bytes changed')
values=[]
for field in (b'__Secure-STRP',b'SEARCH_SAMESITE'):
 found=re.findall(re.escape(field)+rb'=([^;\s,\]]+)',line[start:end]);require(len(found)==1 and bool(found[0]),'cookie classification');values+=found
leaves=0
def scan(b,depth=0):
 global leaves
 require(depth<=6,'nested depth');require(not any(v in b for v in values),'original field value remains in derivative')
 if b[:4] in (b'PK\x03\x04',b'PK\x05\x06'):
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   for i in z.infolist():
    if not i.is_dir():scan(z.read(i),depth+1)
 elif b[:2]==b'\x1f\x8b':
  raw=gzip.decompress(b)
  if len(raw)>265 and raw[257:262]==b'ustar':
   with tarfile.open(fileobj=io.BytesIO(raw),mode='r:') as t:
    for i in t.getmembers():
     if i.isfile():scan(t.extractfile(i).read(),depth+1)
  else:scan(raw,depth+1)
 else:leaves+=1
for row in n['files']:scan((a.sanitized/row['path']).read_bytes())
require((a.original/'ACCEPTANCE.json').read_bytes()==(a.sanitized/'ACCEPTANCE.json').read_bytes(),'historical acceptance changed')
r={'status':'PASS_INDEPENDENT_LOCAL_SANITIZED_DERIVATIVE_CHECK','original_selection_sha256':oh,'sanitized_selection_sha256':nh,'support_members':len(old),'unchanged_support_members':len(old)-1,'changed_member':name,'changed_line':20476,'line_count_preserved':38173,'all_bytes_outside_response_headers_field_identical':True,'original_whole_log_sha256':sha(old[name]),'sanitized_whole_log_sha256':sha(new[name]),'original_cookie_field_names':['__Secure-STRP','SEARCH_SAMESITE'],'original_field_values_found_in_recursive_sanitized_selection':0,'recursively_checked_leaf_members':leaves,'historical_acceptance_unchanged':True,'limits':['No cookie values or cookie-value hashes emitted. No network requests or publication.','Original support remains held and unchanged.','This is a deliberately sanitized derivative, not byte-identical raw artifact replay.','Broad candidate/content/privacy scan and independent sanitized test-protocol replay are separate supporting checks.']}
a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
