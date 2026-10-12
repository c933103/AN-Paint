from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json
R=Path('/workspace/shared/anpaint-pr52-recovery-20261012/replayed-vertical-evidence/reachability');O=Path(__file__).parent/'vertical-contact-sheets';O.mkdir(exist_ok=True)
phases=['before','minimum','maximum','filename','description','cancel-ready','choose-ready','returned'];rows=[]
for tag in ['en-XV','lzh-Hant','mnc-Mong','qaa-Zsye-XV']:
 for orientation in ['portrait','landscape']:
  w,h=(320,640) if orientation=='portrait' else (640,320);cols=4 if orientation=='portrait' else 2
  sheet=Image.new('RGB',(cols*w,((len(phases)+cols-1)//cols)*(h+28)+32),'#dedede');d=ImageDraw.Draw(sheet);d.text((8,8),tag+' / '+orientation+' / original pixels',fill='black')
  for i,phase in enumerate(phases):
   name=f'{tag}-{orientation}-{phase}.png';p=R/name;image=Image.open(p);image.load();assert image.size==(w,h)
   x=(i%cols)*w;y=32+(i//cols)*(h+28);d.text((x+6,y+5),phase,fill='black');sheet.paste(image,(x,y+28));rows.append(dict(path=name,size=image.size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
  sheet.save(O/f'{tag}-{orientation}.png')
(Path(__file__).parent/'vertical-images-reviewed-manifest.json').write_text(json.dumps(rows,indent=2)+'\n');print('64 original images included at original pixel resolution in 8 contact sheets.')
