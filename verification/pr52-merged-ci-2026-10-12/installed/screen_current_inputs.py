#!/usr/bin/env python3
"""Screen current textual CI inputs without printing or value-hashing secret material."""
import argparse,json,pathlib,re,hashlib
p=argparse.ArgumentParser();p.add_argument('--artifacts',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
patterns={
 'set_cookie_header':re.compile(rb'(?i)(?:set-cookie\s*[:=]|\\u0053et-\\u0043ookie)'),
 'cookie_request_header':re.compile(rb'(?i)(?:^|\s|[,{])cookie\s*[:=]'),
 'authorization_value':re.compile(rb'(?i)authorization\s*[:=]\s*(?:bearer|basic)\s+[^\s*]'),
 'github_token_shape':re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})'),
 'private_key_marker':re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
 'aws_access_key_shape':re.compile(rb'AKIA[A-Z0-9]{16}'),
}
rows=[];hits=[];classified=[]
for f in sorted(a.artifacts.rglob('*')):
 if not f.is_file() or '.part' in f.name or f.suffix.lower() in ('.zip','.apk','.png','.jar','.aar','.so','.ttf','.otf'):continue
 if not (f.suffix in ('.txt','.log','.json','.xml') or f.name.endswith('-status.txt')):continue
 rel=f.relative_to(a.artifacts).as_posix()
 if not (rel.startswith('api35/') or rel in ('api35-job.log','build-job.log','source-publication.json','api35.metadata.json','apk-and-source.metadata.json','instrumentation-apks.metadata.json','apk-and-source/build/delivery/build-info.json')):continue
 raw=f.read_bytes();found=[]
 for num,line in enumerate(raw.splitlines(),1):
  for category,regex in patterns.items():
   if regex.search(line):
    if category=='cookie_request_header' and re.match(rb'^\S+\s+\S+\s+\d+\s+\d+\s+\w\s+(?:BiometricScheduler|BiometricService/Sensor|BiometricStateCallback|Biometrics/InternalCleanupClient|BiometricSchedulerOperation|BiometricService)\s*:',line) and re.search(rb'(?i)(?:^|\s|[,{])cookie\s*[:=]\s*\d+(?=[,})\s]|$)',line):
     classified.append({'path':rel,'line':num,'category':'NUMERIC_ANDROID_BIOMETRIC_FRAMEWORK_FIELD_NOT_HTTP_COOKIE'})
    else:found.append({'line':num,'category':category})
 rows.append({'path':rel,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'matches':found})
 hits.extend({'path':rel,**x} for x in found)
r={'schema':1,'status':'REVIEW_REQUIRED' if hits else 'NO_UNRESOLVED_MATCHES_IN_SCREENED_CURRENT_TEXT','run_id':38308218307,'files':rows,'findings':hits,'classified_non_sensitive_markers':classified,'screening_scope':'Current textual artifacts/job logs only; candidate markers, not universal secret absence. Values and value hashes are never output. Whole-file digests bind exact screened inputs. Archives and binary payloads require their separate content inventory. No prior API30 held originals read or copied.'}
a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'files':len(rows),'findings':hits,'classified_numeric_biometric_markers':len(classified)},indent=2))
