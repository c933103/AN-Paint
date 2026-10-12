#!/usr/bin/env python3
"""Optional local Pillow/FreeType comparison; does not replace Android rendering.

Usage: python tools/verify_nom_m04_renderer.py NomNaTong-Regular.ttf output-directory
The full source must match its existing SHA pin. The old subset is reconstructed
only through the strict M04 reverse delta; all old masks, offsets and advances
are compared at normal and enlarged sizes. Source/subset pixels for the three
added glyphs are reported honestly, while exact outlines/metrics are separately
verified by the extension builder and contracts.
"""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile

from commons_metadata_m04_font_scope import before_m04_font
from extend_nom_ui_font import PRIMARY_SHA
from test_locale_font_coverage import mapped_codepoints


def verify(primary, output):
    from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version
    primary, output = Path(primary), Path(output)
    if hashlib.sha256(primary.read_bytes()).hexdigest() != PRIMARY_SHA:
        raise AssertionError('Expected the existing pinned Nom Na Tong v5.18 source')
    root=Path(__file__).resolve().parents[1]
    current=root/'Paintroid/src/main/assets/fonts/anpaintnomui.ttf'
    sizes=(24,48,96);additions=(0x3002,0x554F,0x8FFD)
    output.mkdir(parents=True,exist_ok=True)
    count=0;comparisons=[]
    image=Image.new('RGB',(1000,790),'white');draw=ImageDraw.Draw(image)
    label=ImageFont.load_default(size=17)
    draw.text((15,10),'M04: local FreeType glyph comparison (not Android / language certification)',font=label,fill='black')
    with tempfile.TemporaryDirectory() as folder:
        old=Path(folder)/'before.ttf';old.write_bytes(before_m04_font(current.read_bytes()))
        old_points=mapped_codepoints(old)
        for row,size in enumerate(sizes):
            baseline=115+row*190
            fonts=[ImageFont.truetype(str(p),size,layout_engine=ImageFont.Layout.BASIC) for p in (old,current,primary)]
            for cp in old_points:
                a,ao=fonts[0].getmask2(chr(cp),mode='L',anchor='ls')
                b,bo=fonts[1].getmask2(chr(cp),mode='L',anchor='ls')
                if a.size!=b.size or bytes(a)!=bytes(b) or ao!=bo or fonts[0].getlength(chr(cp))!=fonts[1].getlength(chr(cp)):
                    raise AssertionError(f'Old glyph U+{cp:04X} changed at {size}px')
                count+=1
            draw.text((15,baseline-size-30),f'{size}px',font=label,fill='black')
            for col,cp in enumerate(additions):
                x=120+col*270
                draw.text((x,baseline-size-45),f'U+{cp:04X} subset | source',font=label,fill='black')
                draw.line((x,baseline,x+230,baseline),fill='#cccccc')
                draw.text((x,baseline),chr(cp),font=fonts[1],anchor='ls',fill='black')
                draw.text((x+125,baseline),chr(cp),font=fonts[2],anchor='ls',fill='black')
                a,ao=fonts[1].getmask2(chr(cp),mode='L',anchor='ls')
                b,bo=fonts[2].getmask2(chr(cp),mode='L',anchor='ls')
                if not any(bytes(a)):raise AssertionError(f'Added glyph U+{cp:04X} is empty at {size}px')
                comparisons.append({'codepoint':f'U+{cp:04X}','size_px':size,'nonempty':True,
                    'baseline_offset_identical':ao==bo,'mask_size_identical':a.size==b.size,
                    'mask_pixels_identical':bytes(a)==bytes(b),'subset_global_metrics':fonts[1].getmetrics(),
                    'source_global_metrics':fonts[2].getmetrics()})
        phrase='追問超與料𧵑 Commons 失敗。'
        draw.text((15,610),'Accepted M04 candidate in the extended subset, 32px / 48px:',font=label,fill='black')
        for size,y in [(32,675),(48,735)]:
            font=ImageFont.truetype(str(current),size,layout_engine=ImageFont.Layout.BASIC)
            draw.text((15,y),phrase,font=font,anchor='ls',fill='black')
    png=output/'nom-renderer-comparison.png';image.save(png)
    result={'renderer':f'Pillow {pillow_version} / FreeType BASIC','scope':'Local font rasterization, not Android or linguistic acceptance',
        'sizes_px':list(sizes),'preserved_codepoints':len(old_points),'old_glyph_render_comparisons':count,
        'old_masks_offsets_and_advances_identical':True,'new_glyph_source_comparisons':comparisons,
        'source_pixel_limit':'Source/subset raster differences at any size are retained below; old subset global metrics stay unchanged. Vector outline/advance/bearing equality is checked separately.',
        'image_sha256':hashlib.sha256(png.read_bytes()).hexdigest()}
    (output/'nom-renderer-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('primary');parser.add_argument('output')
    args=parser.parse_args();verify(args.primary,args.output)
