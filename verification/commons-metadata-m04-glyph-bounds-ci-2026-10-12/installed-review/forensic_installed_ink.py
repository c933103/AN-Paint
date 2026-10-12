#!/usr/bin/env python3
"""Forensic extraction of failed installed ink; never promotes failure to acceptance."""
import argparse,hashlib,io,json,pathlib,sys,zipfile,subprocess
import numpy as np
from PIL import Image
TREE='8f9f0d5399f88d173a508e0ce5c96682ca173ed4'
HEAD='d5fb31f6cb1562eecba51e5ccff9b118a7e71714'
MERGE='b750c54f6411412ee3f1bc1f51815db205212c35'
RUN=38263619232
DIGESTS={35:'f309d2269839c32bfd5a5c7a6ec2e59464230de969869d5627f5320b647acc25',30:'d4d87b878071ff564f54e7a50f1365431b77829b71a9cd7cc6dbe59406c499aa'}
DECODER_SHA='e6a7d077033d0c84416eaca18807bd1d6b29928e94974685a59086155764df65'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
 if not v:raise ValueError(m)
def bind(archive,root,digest):
 require(sha(archive.read_bytes())==digest,'official artifact digest differs')
 with zipfile.ZipFile(archive) as z:
  names=[n for n in z.namelist() if not n.endswith('/')];require(len(names)==len(set(names)),'duplicate ZIP member')
  for n in names:
   p=pathlib.PurePosixPath(n);require(not p.is_absolute() and '..' not in p.parts and '\\' not in n,'unsafe ZIP member')
   require(z.read(n)==(root/n).read_bytes(),'extraction differs '+n)
  require(set(names)=={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()},'extracted path-set differs')
 return len(names)
def main():
 p=argparse.ArgumentParser()
 for k in ('repo','artifact-root','output-dir'):p.add_argument('--'+k,type=pathlib.Path,required=True)
 a=p.parse_args();a.output_dir.mkdir(exist_ok=True);pins={}
 for api in (30,35):pins[str(api)]={'sha256':DIGESTS[api],'members':bind(a.artifact_root/f'api{api}.zip',a.artifact_root/f'api{api}',DIGESTS[api])}
 decoder=a.repo/'tools/installed_glyph_ink_evidence.py';require(sha(decoder.read_bytes())==DECODER_SHA,'decoder source differs')
 for name in ('run_android_instrumentation.py','app_instrumentation_matrix.py','vertical_locale_matrix.py'):
  require(subprocess.check_output(['git','show',TREE+':tools/'+name],cwd=a.repo)==(a.repo/'tools'/name).read_bytes(),'imported helper differs from tree '+name)
 sys.path.insert(0,str(a.repo/'tools'));import installed_glyph_ink_evidence as m
 rawpath=a.artifact_root/'api35/app/androidTest-results/instrumentation.log';summarypath=rawpath.with_name('summary.json')
 raw=rawpath.read_bytes();summary=m.strict_json(summarypath.read_bytes());digest=m.source_tests_sha256(a.repo/'app/src/androidTest')
 require(digest=='a5dd8b617ce5610378b197e5f5ac5a59748e87e39a592b3198a53e8bb842345f','app source digest changed')
 records=m.extract_records(raw);rows=[]
 try:m.verify_capture(raw,digest,summary,a.repo/'app/src/androidTest')
 except m.EvidenceError as ex:protocol_rejection=str(ex)
 else:raise ValueError('failed producer incorrectly accepted')
 for route in ('copy','insert'):
  d=records[route];images={};arrays={};files=[]
  for kind in ('actual','reference'):
   image,raster=m.decode_image(d[kind+'_png'],kind);images[kind]=raster
   with Image.open(io.BytesIO(image)) as im:
    im.load();require(im.mode=='RGBA' and im.tobytes()==raster.rgba,'Pillow/std decoder mismatch');arrays[kind]=np.array(im)
   target=a.output_dir/(route+'-'+kind+'.png');target.write_bytes(image);files.append({'name':target.name,'sha256':sha(image)})
  box=tuple(map(int,m.RECT.fullmatch(d['reference_box']).groups()));counts=m.recompute(images['actual'],images['reference'],box,d['origin_x'],d['origin_y'],d['content_width'])
  for k,v in counts.items():require(d[k]==v,'producer/recompute mismatch '+k)
  try:m.verify_record(d,route,digest)
  except m.EvidenceError as ex:rejected=str(ex)
  else:raise ValueError('failed record incorrectly accepted')
  # Independent vectorized recomputation, including every alpha>0 and all view ARGB.
  r=arrays['reference'];actual=arrays['actual'];ys,xs=np.nonzero(r[:,:,3]);l,t,rr,b=box;vx=xs+l+d['origin_x'];vy=ys+t+d['origin_y'];ah,aw=actual.shape[:2];inside=(vx>=0)&(vx<aw)&(vy>=0)&(vy<ah)
  overflow=(xs+l<0)|(xs+l>=d['content_width']);missing=~inside;missing[inside]|=actual[vy[inside],vx[inside],3]==0
  expected=np.zeros_like(actual);ax0=max(0,l+d['origin_x']);ay0=max(0,t+d['origin_y']);ax1=min(aw,rr+d['origin_x']);ay1=min(ah,b+d['origin_y'])
  expected[ay0:ay1,ax0:ax1]=r[ay0-d['origin_y']-t:ay1-d['origin_y']-t,ax0-d['origin_x']-l:ax1-d['origin_x']-l]
  independent={'ink_pixels':len(xs),'ink_left':int((xs+l).min()),'ink_right_exclusive':int((xs+l).max())+1,'allocation_edge_pixels':int(np.count_nonzero((xs==0)|(xs==r.shape[1]-1)|(ys==0)|(ys==r.shape[0]-1))),'horizontal_overflow_pixels':int(overflow.sum()),'outside_view_pixels':int((~inside).sum()),'missing_expected_ink_pixels':int(missing.sum()),'different_argb_pixels':int(np.any(actual!=expected,axis=2).sum())}
  require(independent==counts,'independent Pillow/NumPy recomputation differs')
  pixels=[]
  for i in np.flatnonzero(overflow|missing):pixels.append({'layout':[int(xs[i]+l),int(ys[i]+t)],'reference':[int(xs[i]),int(ys[i])],'actual':[int(vx[i]),int(vy[i])],'reference_rgba':r[ys[i],xs[i]].tolist(),'actual_rgba':actual[vy[i],vx[i]].tolist() if inside[i] else None})
  out=a.output_dir/(route+'.json');out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');files.append({'name':out.name,'sha256':sha(out.read_bytes())})
  rows.append({'route':route,'rejection':rejected,'counts':counts,'independent_numpy_exact':True,'problem_pixels':pixels,'geometry':{k:d[k] for k in ('reference_box','glyph_bounds','origin_x','origin_y','content_width','measured_leading_inset_px','root_width','root_height','density','density_dpi','font_scale','default_textview_use_bounds_for_width','view_use_bounds_for_width','layout_use_bounds_for_width','shift_drawing_offset_for_start_overhang','fingerprint')},'files':files})
 result={'status':'FAIL_INSTALLED_INK','head':HEAD,'tree':TREE,'merge':MERGE,'run_id':RUN,'artifact_bindings':pins,'raw_sha256':sha(raw),'summary_sha256':sha(summarypath.read_bytes()),'source_tests_sha256':digest,'decoder_sha256':DECODER_SHA,'strict_acceptance_rejection':protocol_rejection,'routes':rows,'scope':'Forensic extraction of failed installed API35 native software-raster records. Both official ZIPs/extractions verified, but full matrix outcome remains a separate audit. No hardware screenshot/network failure route or native JVM run is claimed.'}
 (a.output_dir/'forensic-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
