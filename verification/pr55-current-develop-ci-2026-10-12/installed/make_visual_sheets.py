#!/usr/bin/env python3
"""Place unchanged native frame pixels in labelled inspection sheets; no resampling."""
import argparse,json,pathlib,hashlib
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('--frames',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
entries=[]
for casefile in sorted((a.frames/'reachability').glob('*.json')):
 case=casefile.stem;paths=[a.frames/f'{case}-{s}.png' for s in ('workspace','save-initial','format-popup','jpeg-quality')]+[a.frames/'reachability'/f'{case}-{s}.png' for s in ('before','minimum','maximum','filename','description','cancel-ready','choose-ready','returned')]
 images=[Image.open(p).convert('RGB') for p in paths];w,h=images[0].size;cols=2 if w>h else 4;rows=(len(paths)+cols-1)//cols
 sheet=Image.new('RGB',(w*cols,(h+28)*rows),(244,244,244));d=ImageDraw.Draw(sheet)
 for i,(path,image) in enumerate(zip(paths,images)):
  if image.size!=(w,h):raise ValueError('inconsistent image dimensions')
  x=(i%cols)*w;y=(i//cols)*(h+28);d.text((x+4,y+8),path.name,fill=(0,0,0));sheet.paste(image,(x,y+28))
 dest=a.output/(case+'.png');sheet.save(dest);entries.append({'sheet':dest.name,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source_images':[{'path':p.relative_to(a.frames).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],'resampled':False})
(a.output/'sheets.json').write_text(json.dumps(entries,indent=2)+'\n')
