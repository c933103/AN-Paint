#!/usr/bin/env python3
"""Compare all fresh API35 image bytes with the accepted 4a sanitized baseline."""
import argparse,json,pathlib,hashlib
p=argparse.ArgumentParser();p.add_argument('--current',type=pathlib.Path,required=True);p.add_argument('--prior-packet',type=pathlib.Path,required=True);p.add_argument('--prior-decoded',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
 if not v:raise ValueError(m)
require(sha((a.prior_packet/'DELIVERY-FILES.json').read_bytes())=='6b0720bcf45c0619cb810f5974a9a875ae6a732012803d15e850e232d8621bc4','authoritative 4a baseline manifest differs')
manifest=read(a.prior_packet/'DELIVERY-FILES.json');pins={f['path']:f for f in manifest['files']}
used=['ACCEPTANCE.json','api35-visual-inspection.json','visual-review-result.json','reproduced/installed-pixel-result.json']
for name in used:
 b=(a.prior_packet/name).read_bytes();require(sha(b)==pins[name]['sha256'] and len(b)==pins[name]['bytes'],'prior receipt bytes differ '+name)
acc=read(a.prior_packet/'ACCEPTANCE.json');require(acc['run_id']==38303992927 and acc['head']=='4a35933ff6b6d0013dac8743cc5eeac1c1033e05','prior identity differs')
v=read(a.prior_packet/'api35-visual-inspection.json');require(v['status']=='ACTUALLY_INSPECTED_BOUNDED_NATIVE_FRAMES' and v['original_png_count']==96,'prior native inspection scope differs')
prev={f['path']:f['sha256'] for sheet in v['sheets'] for f in sheet['source_images']};require(len(prev)==96,'prior native image inventory differs')
pixel=read(a.prior_packet/'reproduced/installed-pixel-result.json')
# Bind Arabic images to the complete accepted image-specific review, including its explicit reuse.
review=read(a.prior_packet/'visual-review-result.json');arab={x['path']:x['current_sha256'] for x in review['images'] if x['kind']=='arabic'};require(len(arab)==4,'prior Arabic image inventory differs')
rows=[]
for kind,files,sub in [('native',prev,'native-vertical/native-observed-api35'),('arabic',arab,'installed-observed')]:
 current=a.current/sub;prior=a.prior_decoded/sub
 actual={p.relative_to(current).as_posix() for p in current.rglob('*.png')};require(actual==set(files),kind+' current image inventory differs')
 for path,digest in sorted(files.items()):
  old=(prior/path).read_bytes();fresh=(current/path).read_bytes();require(sha(old)==digest,'baseline bytes differ '+path)
  same=fresh==old;rows.append(dict(kind=kind,api=35,path=path,prior_sha256=sha(old),current_sha256=sha(fresh),exact_image_bytes_equal=same,visual_status='EXACT_IMAGE_BYTES_REUSE_PRIOR_REVIEW' if same else 'FRESH_INSPECTION_REQUIRED'))
r={'status':'CHANGED_IMAGES_NEED_VISUAL_REVIEW' if any(not x['exact_image_bytes_equal'] for x in rows) else 'PASS_ALL_EXACT_IMAGE_BYTES_REUSE','head':'eb7451d320ba56e1ece6b1b55797da653966051d','tree':'b6bf7626c1d7c4aef669394970046ffc89a5c877','merge':'e17f49eddd01007a6e776a5d8981e8c1c41ba571','run_id':38308218307,'prior_head':acc['head'],'prior_run_id':acc['run_id'],'prior_selection_sha256':sha((a.prior_packet/'DELIVERY-FILES.json').read_bytes()),'prior_receipts':[{'path':n,'sha256':sha((a.prior_packet/n).read_bytes())} for n in used],'total_images':len(rows),'exact_image_bytes_reuse':sum(x['exact_image_bytes_equal'] for x in rows),'changed_images':sum(not x['exact_image_bytes_equal'] for x in rows),'images':rows,'limits':'Reuse only where exact whole PNG bytes equal an accepted 4a image. Historical API30 is absent. Prior acceptance is not current run credit; current machine checks and changed-frame inspection are separate.'}
a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('status','total_images','exact_image_bytes_reuse','changed_images')},indent=2))
