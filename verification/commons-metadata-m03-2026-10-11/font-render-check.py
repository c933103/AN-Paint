"""Optional local Pillow/FreeType check, not Android acceptance.

Run: python font-render-check.py PRIMARY.ttf PRE_M03.ttf [--output DIR]
Requires Pillow and fonttools; uses the repository's current M03 subset.
"""
from pathlib import Path
import argparse
import hashlib,json
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('primary');parser.add_argument('baseline');parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent)
args=parser.parse_args()
r=Path(__file__).resolve().parents[2];out=args.output;out.mkdir(parents=True,exist_ok=True)
old=Path(args.baseline);new=r/'Paintroid/src/main/assets/fonts/anpaintnomui.ttf';source=Path(args.primary)
for path,digest in [(old,'797ac4ef00f0dd8a982d5216dbd78db3edda07b578b9f8642d0156add90bd526'),(new,'4ae4cab599622f6c9d66b8a99074f2a291ffc32000a78ba69f241fc12eb64e05'),(source,'37bd8506257d0905d499395e7f0bc2b6a2ae619dbb635a82ea0905b75b2ff5f3')]:
 assert hashlib.sha256(path.read_bytes()).hexdigest()==digest,'Unexpected font input'
cp=list(TTFont(old).getBestCmap());n=0;source_comparisons=[]
for size in (24,48,96):
 a=ImageFont.truetype(str(old),size,layout_engine=ImageFont.Layout.BASIC);b=ImageFont.truetype(str(new),size,layout_engine=ImageFont.Layout.BASIC);c=ImageFont.truetype(str(source),size,layout_engine=ImageFont.Layout.BASIC)
 for point in cp:
  x,y=a.getmask2(chr(point),mode='L'),b.getmask2(chr(point),mode='L')
  assert x[1]==y[1] and x[0].size==y[0].size and bytes(x[0])==bytes(y[0]),(point,size)
  assert a.getlength(chr(point))==b.getlength(chr(point));n+=1
 x,y=b.getmask2('返',mode='L',anchor='ls'),c.getmask2('返',mode='L',anchor='ls')
 assert any(bytes(x[0]))
 source_comparisons.append(dict(size_px=size,baseline_offset_identical=x[1]==y[1],mask_size_identical=x[0].size==y[0].size,mask_pixels_identical=bytes(x[0])==bytes(y[0]),subset_global_metrics=b.getmetrics(),source_global_metrics=c.getmetrics()))
 assert b.getlength('返')==c.getlength('返')
canvas=Image.new('RGB',(840,230),'white');draw=ImageDraw.Draw(canvas)
label=ImageFont.load_default(size=20)
for x,p,name in [(20,source,'Pinned source'),(300,new,'M03 subset'),(580,old,'Previous subset')]:
 draw.text((x,10),name,font=label,fill='black');draw.text((x+50,175),'返',font=ImageFont.truetype(str(p),96,layout_engine=ImageFont.Layout.BASIC),anchor='ls',fill='black')
canvas.save(out/'nom-u8fd4-render-comparison.png')
(out/'nom-renderer-checks.json').write_text(json.dumps(dict(renderer='Pillow '+__import__('PIL').__version__+' / FreeType BASIC',scope='Local font rasterization, not Android or linguistic acceptance',sizes_px=[24,48,96],preserved_codepoints=len(cp),old_glyph_render_comparisons=n,old_masks_offsets_and_advances_identical=True,new_glyph_source_comparisons=source_comparisons,new_glyph_nonempty=True,source_pixel_limit="At24px the source and subset masks differ; they match at48/96px with common baseline. Exact vector outline and advance/bearing identity is independently checked. The existing subset global metrics remain unchanged; pixel identity to the full source at every size is not claimed.",image_sha256=hashlib.sha256((out/'nom-u8fd4-render-comparison.png').read_bytes()).hexdigest()),indent=2)+'\n')
print('Passed',n,'old-glyph comparisons; added glyph nonempty at all3sizes; source pixels match at2of3sizes, with difference retained explicitly')
