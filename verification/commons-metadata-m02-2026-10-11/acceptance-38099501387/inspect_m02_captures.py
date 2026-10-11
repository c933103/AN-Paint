#!/usr/bin/env python3
"""Check the precise M02 capture inventory and build review contacts; not linguistic acceptance."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib,json

root=Path('regression/Paintroid/build/reports/commons-metadata-m02')
out=Path('contacts');out.mkdir(exist_ok=True)
tags=['en-GB','fr','ar','ja','vi-Hani','mn-Mong','mnc-Mong','lzh-Hant','en-XV','qaa-Zsye-XV']
expected={f'api35-{tag}-font{scale:.1f}-{action}' for tag in tags for scale in (1,2) for action in ('copy','insert')}
assert {p.stem for p in root.glob('*.json')}==expected
assert {p.stem for p in root.glob('*.png')}==expected
rows=[];pixels={}
for name in sorted(expected):
 report=json.loads((root/(name+'.json')).read_text())
 assert report['evidence_kind']=='Robolectric NATIVE rendering, not installed-device capture'
 assert report['all_characters_laid_out'] is True
 assert report['locale'] in tags and report['font_scale'] in [1,2] and report['action'] in ['copy','insert']
 assert name==f"api35-{report['locale']}-font{report['font_scale']:.1f}-{report['action']}"
 assert 'HTTP 503' in report['message'] and '%1$s' not in report['message']
 with Image.open(root/(name+'.png')) as im:
  im.load();assert im.size==(640,1280)
  rgba=im.convert('RGBA');assert len(rgba.getcolors(rgba.width*rgba.height))>10
  pixel_hash=hashlib.sha256(rgba.tobytes()).hexdigest();pixels[name]=pixel_hash
  rows.append(dict(name=name,report=report,png_sha256=hashlib.sha256((root/(name+'.png')).read_bytes()).hexdigest(),pixel_sha256=pixel_hash,width=im.width,height=im.height))
assert len(set(pixels.values()))==40,'Unexpected duplicate pixel captures'
for tag in tags:
 sheet=Image.new('RGB',(2560,1020),'#d0d0d0');draw=ImageDraw.Draw(sheet)
 for i,(scale,action) in enumerate([(1,'copy'),(1,'insert'),(2,'copy'),(2,'insert')]):
  name=f'api35-{tag}-font{scale:.1f}-{action}'
  with Image.open(root/(name+'.png')) as im:sheet.paste(im.convert('RGB').crop((0,0,640,960)),(i*640,60))
  draw.text((i*640+12,12),f'{tag} | {action} | actual font scale {scale}x',fill='black',font_size=24)
 sheet.save(out/(tag+'.png'))
Path('capture-receipt.json').write_text(json.dumps(dict(expected_pairs=40,verified_pairs=len(rows),all_pixels_distinct=True,scope='Original 640x1280 pixels decoded. Contacts crop the lower 320 pixels to aid review; original PNGs remain authoritative. Human visual and competent language acceptance are separate.',captures=rows),ensure_ascii=False,indent=2)+'\n')
print('Verified40 exact PNG/JSON pairs; contacts prepared for pixel inspection.')
