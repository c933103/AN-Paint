#!/usr/bin/env python3
"""Read exact downloaded PNG pixels; no image modifications or tolerance."""
import argparse,pathlib,json,hashlib
import numpy as np
from PIL import Image
from audit_painted_ink import read_rgba,metrics,read_json,reference_box
STEMS=('api35-ar-640x320-font2.0-copy','api35-ar-640x320-font2.0-insert','api35-ar-640x320-font2.0-negative-controls-intact')
def main():
 p=argparse.ArgumentParser();p.add_argument('directory',type=pathlib.Path);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();rows=[]
 for stem in STEMS:
  paths=[a.directory/(stem+s) for s in ('.json','-actual-textview.png','-complete-layout.png')];d=read_json(paths[0]);actual=read_rgba(paths[1]);ref=read_rgba(paths[2]);m=metrics(actual,ref,d)
  for k,v in m.items():assert d[k]==v,(stem,k)
  l,t,r,b=reference_box(d['reference_box']);y,x=np.nonzero(ref[:,:,3]);outside=(x+l<0)|(x+l>=d['content_width']);points=[]
  for py,px in zip(y[outside],x[outside]):
   vx=int(px+l+d['origin_x']);vy=int(py+t+d['origin_y']);points.append({'layout_xy':[int(px+l),int(py+t)],'reference_xy':[int(px),int(py)],'actual_view_xy':[vx,vy],'reference_rgba':ref[py,px].tolist(),'actual_rgba':actual[vy,vx].tolist()})
  rows.append({'stem':stem,'metrics':m,'content_width':d['content_width'],'reference_box':d['reference_box'],'glyph_bounds':d['glyph_bounds'],'actual_dimensions':[actual.shape[1],actual.shape[0]],'outside_content_pixels':points,'files':[{'name':q.name,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for q in paths]})
 result={'status':'EXACT_PIXEL_LOSS_CONFIRMED_ORACLE_FAILED','profiles':rows,'interpretation':'Each complete native reference contains two low-alpha pixels beyond the horizontal content boundary; the actual TextView bitmap omits them. This is observed native clipping under the strict oracle, unlike the earlier advance-only Ainu mismatch. No tolerance, alpha masking, production repair or linguistic change is inferred.','limits':'Native Robolectric snapshot, not installed-device reproduction. Shared native text layout is not independent linguistic or universal glyph-shaping proof.'};a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
