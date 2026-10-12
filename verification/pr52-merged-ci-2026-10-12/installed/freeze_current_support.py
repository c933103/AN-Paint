#!/usr/bin/env python3
"""Freeze compact current API35 evidence after input screening, omitting payloads/duplicates."""
import argparse,gzip,hashlib,io,json,pathlib,tarfile
from audit_natural_artifacts import HEAD,TREE,MERGE,RUN,require
p=argparse.ArgumentParser();p.add_argument('--artifacts',type=pathlib.Path,required=True);p.add_argument('--screen',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);p.add_argument('--review-root',type=pathlib.Path,required=True);a=p.parse_args()
screen=json.loads(a.screen.read_bytes());require(screen['status']=='NO_UNRESOLVED_MATCHES_IN_SCREENED_CURRENT_TEXT','unresolved textual input marker; do not freeze raw support')
checked={x['path']:x for x in screen['files']};selected={}
def sha(b):return hashlib.sha256(b).hexdigest()
def add(name,path):
 require(name not in selected and path.is_file(),'missing/duplicate input '+name);raw=path.read_bytes()
 if path.suffix in ('.txt','.log','.json','.xml'):
  rel=path.relative_to(a.artifacts).as_posix();require(rel in checked and checked[rel]['sha256']==sha(raw),'input not screened or changed '+rel)
 selected[name]=raw
for name in ('build-job.log','api35-job.log','source-publication.json','api35.metadata.json','apk-and-source.metadata.json','apk-and-source/build/delivery/build-info.json'):
 add('current-inputs/'+name,a.artifacts/name)
root=a.artifacts/'api35'
for path in sorted(root.rglob('*')):
 if not path.is_file():continue
 rel=path.relative_to(root)
 use=(path.name in ('summary.json','instrumentation.log','install.log','logcat.txt') or path.name.startswith('TEST-') and path.suffix=='.xml' or rel.parts[0]=='vertical-locale-export' or rel.as_posix() in ('vertical-locale-export.json','vertical-locale-screenshots.json','vertical-control-reachability.json','app/coverage.json','app/ordinary-gallery-coverage.json','app/vertical-coverage.json','app/accepted-credit-restart/coverage.json','app/accepted-credit-restart/boundary.log','app/accepted-credit-restart/verify-status.txt'))
 if use:add('current-inputs/api35/'+rel.as_posix(),path)
report='current-verified/native-vertical/result.json';selected[report]=(a.review_root/report).read_bytes()
require(not a.output.exists(),'support archive already exists');rows=[]
with a.output.open('wb') as out:
 with gzip.GzipFile(filename='',fileobj=out,mode='wb',mtime=0) as gz,tarfile.open(fileobj=gz,mode='w') as tar:
  for name,raw in sorted(selected.items()):
   item=tarfile.TarInfo(name);item.size=len(raw);item.mode=0o644;item.uid=item.gid=item.mtime=0;item.uname=item.gname='';tar.addfile(item,io.BytesIO(raw));rows.append(dict(path=name,bytes=len(raw),sha256=sha(raw),kind='ORIGINAL_CURRENT_RAW_INPUT' if name.startswith('current-inputs/') else 'DERIVED_CURRENT_AUDIT_REPORT'))
b=a.output.read_bytes();r=dict(schema=1,head=HEAD,tree=TREE,merge=MERGE,run_id=int(RUN),kind='CURRENT_API35_RAW_INPUTS_PLUS_DERIVED_NATIVE_REPORT',raw_input_count=52,derived_report_count=1,selected_apis=[35],api30_status='NOT_SELECTED; NO_API30_DATA_INCLUDED',archive=dict(path=a.output.name,bytes=len(b),sha256=sha(b)),file_count=len(rows),expanded_bytes=sum(x['bytes'] for x in rows),files=rows,screen_sha256=sha(a.screen.read_bytes()),scope='Compact fresh API35 protocols, XML, summaries, logs, prebuilt/install receipts and native export ZIPs. Original selected input bytes unchanged. One separately labeled derived native report is retained compressed at its original logical evidence path. No prior API30 data, old held packet, APK/source/outer CI ZIP payload, or duplicate decoded PNG/contact sheet.',limits='Not universal secret-absence proof. No current API30 execution. Original outer ZIP and APK/source identity checks are preserved receipts; omitted payloads require original current downloads to replay those checks.')
(a.output.parent/'SUPPORTING-INPUTS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('kind','archive','file_count','expanded_bytes')},indent=2))
