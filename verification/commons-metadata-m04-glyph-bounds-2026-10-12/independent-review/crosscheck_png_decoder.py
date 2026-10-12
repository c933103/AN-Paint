#!/usr/bin/env python3
"""Cross-check the new decoder against Pillow and immutable actual failed-run rasters."""
import argparse, hashlib, io, json, pathlib, re, sys
from PIL import Image, __version__ as PIL_VERSION
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True)
p.add_argument('--prior-evidence',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True)
a=p.parse_args();sys.path.insert(0,str(a.repo/'tools'));import installed_glyph_ink_evidence as ink
def check(v,m):
 if not v:raise ValueError(m)
rows=[]
for stem in ['api35-ar-640x320-font2.0-copy','api35-ar-640x320-font2.0-insert','api35-ar-640x320-font2.0-negative-controls-intact']:
 metadata_raw=(a.prior_evidence/(stem+'.json')).read_bytes();metadata=json.loads(metadata_raw);images={};pins={}
 for kind,suffix in [('actual','-actual-textview.png'),('reference','-complete-layout.png')]:
  raw=(a.prior_evidence/(stem+suffix)).read_bytes();raster=ink.decode_png(raw)
  with Image.open(io.BytesIO(raw)) as image:
   check(image.mode=='RGBA','Unexpected Pillow mode');check(image.size==(raster.width,raster.height),'Dimensions differ')
   check(image.tobytes()==raster.rgba,'Raw pixels differ from independent Pillow decoder')
  images[kind]=raster;pins[kind]=hashlib.sha256(raw).hexdigest()
 match=ink.RECT.fullmatch(metadata['reference_box']);check(match,'bad old reference rectangle')
 counts=ink.recompute(images['actual'],images['reference'],tuple(map(int,match.groups())),metadata['origin_x'],metadata['origin_y'],metadata['content_width'])
 for field,value in counts.items():check(metadata[field]==value,'old reported/recomputed mismatch '+field)
 for field in ['horizontal_overflow_pixels','missing_expected_ink_pixels','different_argb_pixels']:check(counts[field]==2,'historical two-pixel failure changed '+field)
 check(counts['allocation_edge_pixels']==0,'historical allocation edge changed')
 rows.append({'stem':stem,'png_sha256':pins,'metadata_sha256':hashlib.sha256(metadata_raw).hexdigest(),'recomputed':counts,'pillow_raw_rgba_identical':True})
result={'status':'PASS','scope':'New decoder arithmetic/PNG interoperability on the immutable failed run, not repaired/native successor evidence','historical_run':38250189049,'historical_tree':'8752ed99c9350235da46fac1b4a188ca89296889','pillow_version':PIL_VERSION,'decoder_sha256':hashlib.sha256((a.repo/'tools/installed_glyph_ink_evidence.py').read_bytes()).hexdigest(),'frames':rows}
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','frames':len(rows),'all_pngs_match_pillow':True,'all_three_historical_failures_preserved':True}))
