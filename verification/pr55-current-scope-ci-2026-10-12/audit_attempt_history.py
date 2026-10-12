#!/usr/bin/env python3
"""Keep actual executed jobs distinct from successful job aliases on a targeted rerun."""
import argparse,hashlib,json,pathlib
p=argparse.ArgumentParser();p.add_argument('--attempt1',type=pathlib.Path,required=True);p.add_argument('--attempt2',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);p.add_argument('--final-publication',type=pathlib.Path);a=p.parse_args()
def read(path):
 d=json.loads(path.read_text());jobs=d['jobs'];names=[j['name'] for j in jobs]
 if len(names)!=len(set(names)):raise ValueError('duplicate jobs')
 return {j['name']:j for j in jobs}
one,two=read(a.attempt1),read(a.attempt2)
if one.keys()!=two.keys():raise ValueError('changed job matrix')
rerun='Emulator API 30';rows=[]
if one[rerun]['id']!=114996862363 or one[rerun]['conclusion']!='failure':raise ValueError('attempt1 failure binding')
if two[rerun]['id']!=115001925607:raise ValueError('unexpected retry job')
for name,j in one.items():
 n=two[name]
 if name==rerun:
  if not(n['started_at']>j['completed_at']):raise ValueError('retry chronology')
  rows.append({'name':name,'original_job_id':j['id'],'new_job_id':n['id'],'classification':'ACTUAL_TARGETED_RERUN','attempt1_conclusion':j['conclusion'],'attempt2_status':n['status'],'attempt2_conclusion':n['conclusion'],'original_started_at':j['started_at'],'original_completed_at':j['completed_at'],'retry_started_at':n['started_at'],'retry_completed_at':n.get('completed_at')})
 else:
  for key in ('started_at','completed_at','conclusion','status'):
   if j[key]!=n[key]:raise ValueError('supposed copied job differs '+name+' '+key)
  if j['status']!='completed' or j['conclusion']!='success':raise ValueError('copied incomplete/nonpassing job')
  rows.append({'name':name,'original_executed_job_id':j['id'],'attempt2_alias_job_id':n['id'],'classification':'COPIED_SUCCESS_RECORD_NOT_NEW_EXECUTION','started_at':j['started_at'],'completed_at':j['completed_at']})
r={'status':'PASS_ATTEMPT_SEPARATION','run_id':38303992927,'actual_targeted_job_reruns':1,'successful_job_aliases_not_new_executions':len(rows)-1,'rows':rows,'inputs':[{'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (a.attempt1,a.attempt2)],'limit':'Metadata timestamps support copied-success classification; independent original logs and artifact digests retain actual execution provenance. Attempt1 API30 remains setup failure with all95 selected tests unrun.'}
if a.final_publication:
 f=json.loads(a.final_publication.read_text());current={j['id']:j for j in f['jobs']}
 if set(current)!={j['id'] for j in two.values()} or not all(j['status']=='completed' and j['conclusion']=='success' for j in current.values()):raise ValueError('final selected job outcomes')
 if f['run_id']!=r['run_id'] or f['head']!='4a35933ff6b6d0013dac8743cc5eeac1c1033e05' or f['tree']!='b6bf7626c1d7c4aef669394970046ffc89a5c877':raise ValueError('final source binding')
 r['status']='PASS_FINAL_ATTEMPT_SEPARATION';r['final_publication_receipt_sha256']=hashlib.sha256(a.final_publication.read_bytes()).hexdigest();r['final_displayed_jobs_all_completed_success']=True
 for row in r['rows']:
  if row['classification']=='ACTUAL_TARGETED_RERUN':
   row['attempt2_status']='completed';row['attempt2_conclusion']='success';row['retry_completed_at']=None;row['final_status_source']='final-source-publication.json; raw final job timestamp metadata not supplied here'
a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
