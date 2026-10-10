from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
import sys,json,hashlib
root=Path(__file__).resolve().parent;sdk=sys.argv[1]
src=root/('device'+sdk)/'app/vertical-locale-evidence';out=root/'contact-sheets'/sdk;out.mkdir(parents=True,exist_ok=True)
rows=[]
for tag in ['en-XV','mnc-Mong','lzh-Hant','qaa-Zsye-XV']:
 for orient in ['portrait','landscape']:
  files=sorted(src.rglob(f'{tag}-{orient}-*.png'));assert len(files)==12,(tag,orient,len(files))
  sheet=Image.new('RGB',(1280,1524),'#dddddd');draw=ImageDraw.Draw(sheet)
  for i,p in enumerate(files):
   x=(i%4)*320;y=(i//4)*508;im=Image.open(p).convert('RGB');im.thumbnail((320,480));sheet.paste(im,(x+(320-im.width)//2,y+28+(480-im.height)//2));draw.text((x+4,y+4),p.stem.removeprefix(tag+'-'+orient+'-'),fill='black')
   rows.append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
  sheet.save(out/f'{tag}-{orient}.jpg',quality=94)
(root/f'contacts-{sdk}-manifest.json').write_text(json.dumps(rows,indent=2))
