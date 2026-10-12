#!/usr/bin/env python3
"""Read-only forensic check of the fresh review-required native frame; no universal tolerance."""
import argparse,json,pathlib,hashlib
from collections import deque
import numpy as np
from audit_platform_ink import check_frame,metrics,MUTATIONS,CONTROL_TAGS,tight_reference

def require(v,msg):
 if not v: raise ValueError(msg)
def audit(p):
 stem='api35-ar-640x320-font2.0-negative-controls-reset-mixed-paragraphs'
 d,a,r,rec=check_frame(p,stem)
 from audit_platform_ink import reference_box
 l,t,rr,b=reference_box(d['reference_box']);y,x=np.nonzero(r[:,:,3]);loss=[]
 seen_components=[]
 for yy,xx in zip(y,x):
  vx,vy=int(xx+l+d['origin_x']),int(yy+t+d['origin_y'])
  if not (0<=vx<a.shape[1] and 0<=vy<a.shape[0]):continue
  if a[vy,vx,3]!=0:continue
  loss.append({'layout_xy':[int(xx+l),int(yy+t)],'reference_xy':[int(xx),int(yy)],'actual_xy':[vx,vy],'reference_rgba':r[yy,xx].tolist(),'actual_rgba':a[vy,vx].tolist()})
  if any((int(yy),int(xx)) in c for c in seen_components):continue
  component={(int(yy),int(xx))};q=deque(component)
  while q:
   cy,cx=q.popleft()
   for dy in (-1,0,1):
    for dx in (-1,0,1):
     ny,nx=cy+dy,cx+dx
     if 0<=ny<r.shape[0] and 0<=nx<r.shape[1] and r[ny,nx,3] and (ny,nx) not in component:component.add((ny,nx));q.append((ny,nx))
  seen_components.append(component)
 components=[]
 for c in seen_components:
  total=sum(int(r[cy,cx,3]) for cy,cx in c);removed=[]
  for cy,cx in c:
   vx,vy=cx+l+d['origin_x'],cy+t+d['origin_y']
   if not(0<=vx<a.shape[1] and 0<=vy<a.shape[0]) or a[vy,vx,3]==0:removed.append((cy,cx))
  components.append({'reference_samples':len(c),'missing_samples':len(removed),'reference_alpha_sum':total,'missing_alpha_sum':sum(int(r[cy,cx,3]) for cy,cx in removed),'max_reference_alpha':max(int(r[cy,cx,3]) for cy,cx in c),'max_missing_alpha':max(int(r[cy,cx,3]) for cy,cx in removed),'component_entirely_missing':len(removed)==len(c)})
 checks=[];missing=[]
 for scale in (1.0,2.0):
  for tag in CONTROL_TAGS:
   base=f'api35-{tag}-640x320-font{scale}-negative-controls'
   if not(p/(base+'-intact.json')).exists():
    missing.extend(base+'-'+m for m in MUTATIONS);continue
   ide,ia,ir,irec=check_frame(p,base+'-intact')
   for m in MUTATIONS:
    n=base+'-'+m
    if not(p/(n+'.json')).exists():missing.append(n);continue
    md,ma,mr,mrec=check_frame(p,n)
    require(md['ink_pixels']==ide['ink_pixels'],n+' lost reference glyph ink')
    require((md['origin_x'],md['origin_y'],md['content_width'])==(ide['origin_x'],ide['origin_y'],ide['content_width']),n+' changed geometry')
    if m.startswith('clip-'):
     require(md['reference_box']==ide['reference_box'] and md['glyph_bounds']==ide['glyph_bounds'] and np.array_equal(mr,ir),n+' changed unclipped reference')
     wanted=ia.copy()
     if m=='clip-first-spatial-ink':wanted[:,:ide['origin_x']+ide['ink_left']+1]=0
     else:wanted[:,ide['origin_x']+ide['ink_right_exclusive']-1:]=0
     require(md['missing_expected_ink_pixels']>0 and md['different_argb_pixels']>0,n+' clip removed no ink')
    else:
     delta={'left-overflow':-ide['ink_left']-1,'right-overflow':ide['content_width']-ide['ink_right_exclusive']+1,'wholly-left-of-view':-4*ide['content_width'],'wholly-right-of-view':4*ide['content_width']}[m]
     require(md['ink_left']==ide['ink_left']+delta and md['ink_right_exclusive']==ide['ink_right_exclusive']+delta,n+' wrong shift')
     require(np.array_equal(tight_reference(mr),tight_reference(ir)),n+' changed reference pixels')
     wanted=np.zeros_like(ia);width=ia.shape[1]
     if -width<delta<width:
      if delta>=0:wanted[:,delta:]=ia[:,:width-delta]
      else:wanted[:,:width+delta]=ia[:,-delta:]
     require(md['horizontal_overflow_pixels']>0,n+' no overflow')
    require(np.array_equal(ma,wanted),n+' actual mutation differs')
    checks.append(n)
 return {'classification':'FRESH_REVIEW_REQUIRED_POSITIVE_FRAME_FORENSICS','failed_frame':rec,'metadata':d,'actual_dimensions':[a.shape[1],a.shape[0]],'reference_dimensions':[r.shape[1],r.shape[0]],'lost_pixels':loss,'total_reference_alpha':int(r[:,:,3].sum()),'missing_opaque_equivalent_pixels':sum(x['reference_rgba'][3] for x in loss)/255,'affected_components':components,'independently_verified_present_mutations':checks,'absent_mutations':missing,'limits':['Missing frames/summaries remain unrun, not inferred passes.','Connected components are image structures, not a linguistic glyph or grapheme segmentation.','No universal visual tolerance or readability pass is inferred from alpha counts.']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--frames',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();r=audit(a.frames);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('classification','lost_pixels','affected_components','missing_opaque_equivalent_pixels')},indent=2));print('present mutant relations',len(r['independently_verified_present_mutations']),'absent',len(r['absent_mutations']))
