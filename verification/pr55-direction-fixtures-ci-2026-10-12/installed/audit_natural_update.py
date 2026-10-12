#!/usr/bin/env python3
"""Strict natural-traversal log consistency; source/run/PNG authenticity is separate."""
from audit_natural_artifacts import SOURCE_SHA,LIBRARY_SHA
import argparse,hashlib,json,math,pathlib,re
TAG='GalleryStatusNaturalUpdate'
STATUS_CLASS='org.catrobat.paintroid.classic.GlyphBoundsStatusView'
from audit_natural_artifacts import BINDING
MESSAGES=BINDING['arabic_messages']
FIELDS=set('schema route source_tests_sha256 status_class old_message message old_layout_height view_width root_requested_before view_requested_before view_requested_after root_requested_after new_layout_height complete_layout_text root_requested_settled view_requested_settled'.split())
LINE=re.compile(r'^\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}\s+\d+\s+\d+\s+I\s+GalleryStatusNaturalUpdate\s*:\s*(.+)$')
FAILURES=('allocation_edge_pixels','horizontal_overflow_pixels','outside_view_pixels','missing_expected_ink_pixels','different_argb_pixels')
def require(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:require(k not in d,'duplicate JSON field '+k);d[k]=v
 return d
def reject(v):raise ValueError('nonfinite JSON '+v)
def parse(text):return json.loads(text,object_pairs_hook=unique,parse_constant=reject)
def audit(raw,records):
 require(len(raw)<=128*1024*1024,'logcat exceeds bounded audit size')
 lines=raw.decode('utf-8',errors='strict').splitlines();rows={}
 for number,line in enumerate(lines,1):
  if TAG not in line:continue
  m=LINE.fullmatch(line);require(m is not None,'malformed natural-update log line '+str(number))
  payload=m[1];require(len(payload.encode())<=4096,'oversized/truncated log risk')
  d=parse(payload);require(type(d) is dict and set(d)==FIELDS,'natural-update exact fields')
  route=d['route'];require(type(route) is str and route in MESSAGES and route not in rows,'unknown/duplicate natural route')
  exact={'schema':1,'source_tests_sha256':SOURCE_SHA,'status_class':STATUS_CLASS,'message':MESSAGES[route],'old_message':MESSAGES['insert' if route=='copy' else 'copy'],'complete_layout_text':MESSAGES[route],'root_requested_before':False,'view_requested_before':False,'view_requested_after':True,'root_requested_settled':False,'view_requested_settled':False}
  for key,want in exact.items():require(type(d[key]) is type(want) and d[key]==want,'natural state/message differs '+key)
  require(type(d['root_requested_after']) is bool,'root request observation must be boolean')
  for key in ('old_layout_height','new_layout_height','view_width'):require(type(d[key]) is int and 0<d[key]<=16384,'invalid native geometry '+key)
  require(d['old_layout_height']==d['new_layout_height'],'same-height replacement not proved')
  require(d['old_message']!=d['message'],'replacement text did not change')
  require(route in records,'missing corresponding raster record');r=records[route]
  for key,want in {'source_tests_sha256':SOURCE_SHA,'route':route,'locale':'ar','api':35,'target_sdk':35,'font_scale':2,'message':d['message'],'accessibility_text':d['message'],'complete_layout_text':d['message']}.items():require(type(r.get(key)) is type(want) and r[key]==want,'raster/source/profile mismatch '+key)
  require(type(r.get('ink_pixels')) is int and r['ink_pixels']>0,'empty raster record')
  for key in FAILURES:require(type(r.get(key)) is int and r[key]==0,'raster acceptance failed '+key)
  require(r['actual_png']['width']==d['view_width'],'natural/raster width mismatch')
  require(type(r.get('origin_y')) is int and r['origin_y']>=0 and d['new_layout_height']+r['origin_y']<=r['actual_png']['height'],'natural height outside actual view')
  rows[route]={'line_number':number,'record':d,'raster_record_sha256':sha(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()),'scope':'Natural-update receipt agrees with corresponding already-verified full raster record; PNG authenticity/recomputation remains separate.'}
 require(set(rows)==set(MESSAGES),'missing natural-update routes')
 require(rows['copy']['line_number']<rows['insert']['line_number'],'route order differs from reviewed source')
 require(rows['copy']['record']['new_layout_height']==rows['insert']['record']['old_layout_height'],'cross-route height state disagrees')
 require(rows['copy']['record']['view_width']==rows['insert']['record']['view_width'],'cross-route width changed')
 return {'status':'PASS_NATURAL_LOG_CONSISTENCY','source_tests_sha256':SOURCE_SHA,'logcat_sha256':sha(raw),'records':rows,'limits':'Log/schema/source/raster-record consistency only. Requires official source/run/APK binding, exact successful ordinary-app raw protocol, full API30/API35 matrices, strict PNG decoder/recomputation and actual visual inspection. No hardware screenshot/network-route proof.'}
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for k in ('logcat','records','binding','output'):p.add_argument('--'+k,type=pathlib.Path,required=True)
 a=p.parse_args();b=parse(a.binding.read_text());raw=a.logcat.read_bytes()
 for k in ('head','merge','tree'):require(type(b.get(k)) is str and re.fullmatch('[0-9a-f]{40}',b[k]),'actual publication binding missing '+k)
 require(type(b.get('run_id')) is int and b['run_id']>0 and b.get('source_tests_sha256')==SOURCE_SHA,'actual run/source binding missing')
 require(b.get('logcat_sha256')==sha(raw),'actual bound logcat digest differs')
 records={r:parse((a.records/(r+'.json')).read_text()) for r in MESSAGES};result=audit(raw,records);result['binding']=b
 a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':result['status'],'routes':list(result['records']),'run_id':b['run_id']},indent=2))
if __name__=='__main__':main()
