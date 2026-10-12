import pathlib,re,json,zipfile,io,urllib.parse,argparse
p=argparse.ArgumentParser();p.add_argument('--root',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
findings=[];files=[]
def scan(name,b,depth=0):
 if len(b)>128*1024*1024:raise ValueError('bounded input limit '+name)
 if name.endswith('.zip') and depth<3:
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   if sum(x.file_size for x in z.infolist())>256*1024*1024:raise ValueError('expanded limit')
   for n in z.namelist():
    if not n.endswith('/'):scan(name+'!'+n,z.read(n),depth+1)
  return
 if name.endswith(('.png','.apk','.jar','.so')):return
 if b'\0' in b:return
 try:s=b.decode('utf-8-sig')
 except UnicodeDecodeError:return
 files.append({'path':name,'bytes':len(b)})
 for no,line in enumerate(s.splitlines(),1):
  fields=[];hosts=[]
  for label,pat in [('Set-Cookie',r'(?i)\bset-?cookie\s*[:=]' ),('Authorization',r'(?i)\bauthorization\s*[:=]\s*(?:bearer|basic)\s+\S+'),('Bearer',r'\bBearer\s+[A-Za-z0-9._~+/=-]{12,}'),('private-key',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),('credential-token',r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16}|AIza[0-9A-Za-z_-]{30,})\b'),('cookie',r'(?i)\bcookie\s*:\s*[^\s;]+='),('sensitive-assignment',r'(?i)\b(?:access_token|refresh_token|client_secret|api_key|password|sessionid|session_id)\s*[:=]\s*[\x22\x27]?[A-Za-z0-9._~+/=-]{10,}')]:
   if re.search(pat,line):
    if label=='Authorization':
     credential=re.search(r'(?i)authorization\s*[:=]\s*(?:bearer|basic)\s+([^\s]+)',line)[1]
     if re.fullmatch(r'\*+[\x27\x22]?',credential):continue
    fields.append(label)
  for m in re.finditer(r'https?://[^\s<>\x22\x27]+',line):
   try:
    u=urllib.parse.urlsplit(m[0]);q=urllib.parse.parse_qsl(u.query)
    signed=[k for k,v in q if re.search(r'(?i)^(?:sig|signature|token|access_token|key|api_key|x-amz-.+|x-goog-.+|se|sv|sp|sr|skoid|sktid|skt|ske|sks|skv)$',k)]
    if signed:fields.extend('query:'+k for k in signed);hosts.append(u.hostname)
    if u.username or u.password:fields.append('URL-userinfo');hosts.append(u.hostname)
   except ValueError:pass
  if fields:findings.append({'path':name,'line':no,'fields':sorted(set(fields)),'hosts':sorted(set(h for h in hosts if h))})
for f in sorted(a.root.rglob('*')):
 if not f.is_file() or '.part' in f.name:continue
 rel=f.relative_to(a.root).as_posix()
 if rel not in ('api30.zip','api35.zip','api30-job.log','api35-job.log','build-job.log','source-publication.json','api30-metadata.json','api35-metadata.json','apk-and-source-metadata.json'):continue
 if rel.startswith('api') and '/' in rel:continue # scan exact complete outer ZIP once
 scan(rel,f.read_bytes())
r={'status':'HOLD' if findings else 'PASS_BOUNDED_CONTENT_SCREEN','scope':'Complete selected emulator archives including nested export archives; complete job logs and metadata; excludes APK/source build payloads, historical inputs and incomplete .part files. Fields/hosts only for suspected content, never values or value hashes. Bounded credential-pattern screen, not a guarantee of absence.','files':files,'findings':findings};a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('status','findings')}));print('text inputs',len(files))
