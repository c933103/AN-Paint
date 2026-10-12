#!/usr/bin/env python3
"""Recheck source-bound retained-notice capture metadata; pixels need visual review."""
import argparse,hashlib,json,pathlib
from PIL import Image
EVIDENCE='Retained Robolectric NATIVE notice rotation and programmatic reader-offset preservation; oversized test captions; not installed input acceptance'
def require(value,message):
 if not value:raise ValueError(message)
def check_rails(data,tag,offset):
 require(set(data)=={'evidence_kind','rails'} and data['evidence_kind']==EVIDENCE,'notice evidence schema')
 require(isinstance(data['rails'],list) and len(data['rails'])==2,'two native rails')
 for row in data['rails']:
  require(set(row)=={'range','scroll_x','reading_offset','viewport_width'},'rail schema')
  require(all(type(v) is int for v in row.values()),'integer geometry')
  require(row['range']>47 and row['viewport_width']>0,'overflowing positive geometry')
  require(0<=row['scroll_x']<=row['range'],'valid scroll interval')
  observed=row['range']-row['scroll_x'] if tag=='lzh-Hant' else row['scroll_x']
  require(row['reading_offset']==observed==offset,'exact reading-start-relative offset')
def audit(directory):
 wanted={f'api{sdk}-retained-vertical-{tag}-offset{offset}-{rotation}':(sdk,tag,offset,rotation) for sdk in (30,35) for tag in ('lzh-Hant','mn-Mong') for offset in (0,47) for rotation in (0,1)}
 present={p.name:p for p in directory.glob('*retained-vertical*') if p.is_file()}
 needed={s+x for s in wanted for x in ('.json','.png')};missing=sorted(needed-present.keys());extra=sorted(present.keys()-needed);errors=[];rows=[]
 for stem,(sdk,tag,offset,rotation) in sorted(wanted.items()):
  if any(stem+s not in present for s in ('.json','.png')):continue
  try:
   j=present[stem+'.json'];p=present[stem+'.png'];data=json.loads(j.read_bytes());check_rails(data,tag,offset)
   with Image.open(p) as im:
    im.load();require(im.format=='PNG' and min(im.size)>0,'nonempty PNG');require(any(a!=b for a,b in im.convert('RGB').getextrema()),'nonuniform actual capture');size=list(im.size)
   rows.append({'profile':stem,'sdk':sdk,'tag':tag,'reading_offset':offset,'rotation_index':rotation,'dimensions':size,'rails':data['rails'],'json_sha256':hashlib.sha256(j.read_bytes()).hexdigest(),'png_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
  except Exception as ex:errors.append({'profile':stem,'error':str(ex)})
 return {'status':'PASS' if not(missing or extra or errors) else 'FAIL','expected_pairs':len(wanted),'checked_pairs':len(rows),'missing':missing,'extra':extra,'errors':errors,'pairs':rows,'scope':'Actual metadata and PNG integrity; programmatic oversized-caption rail retention. JUnit must independently confirm unchanged source assertions, and these frames do not replace installed input or language review.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--directory',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();r=audit(a.directory);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('status','expected_pairs','checked_pairs','missing','extra','errors')},indent=2));raise SystemExit(0 if r['status']=='PASS' else 1)
