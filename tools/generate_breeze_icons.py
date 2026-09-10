"""AN Paint icon resource conversion, 2026-09-09; AGPL-3.0-or-later.

The artwork remains LGPL-3.0-or-later. See artwork/breeze/COPYING-ICONS.
Requires Python 3 and CairoSVG 2.8.2 (python3 -m pip install CairoSVG==2.8.2).
Normal Android builds use the checked-in PNGs and need no SVG runtime library.
Original SVG bytes, including dashed strokes, are rendered without redrawing.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artwork/breeze'
inventory = json.loads((ART / 'inventory.json').read_text())
outputs = []
parser = argparse.ArgumentParser()
parser.add_argument('--vectors-only', action='store_true', help='Regenerate the four vector icons without CairoSVG')
args = parser.parse_args()
if args.vectors_only:
    outputs = [row for row in json.loads((ART/'generated.json').read_text())['outputs'] if not row['path'].endswith('.xml')]
else:
    import cairosvg

def vector(svg):
    root = ET.fromstring(svg)
    lines = ['<?xml version="1.0" encoding="utf-8"?>',
        '<!-- KDE Breeze; LGPL-3.0-or-later. Original SVG and notice in artwork/breeze. -->',
        '<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="44dp" android:height="44dp" android:viewportWidth="22" android:viewportHeight="22">']
    for path in root.findall('{*}path'):
        translate = path.get('transform')
        if translate:
            match = re.fullmatch(r'translate\(([-.\d]+)[ ,]+([-.\d]+)\)', translate)
            assert match, translate
            lines.append(f'<group android:translateX="{match[1]}" android:translateY="{match[2]}">')
        lines.append('<path android:fillColor="#FF232629" android:fillAlpha='+quoteattr(path.get('fill-opacity','1'))+' android:pathData='+quoteattr(path.get('d'))+'/>')
        if translate: lines.append('</group>')
    return '\n'.join(lines+['</vector>',''])

for icon in inventory['icons']:
    svg = (ART / icon['upstream_path']).read_bytes()
    assert hashlib.sha256(svg).hexdigest() == icon['sha256'], icon['resource']
    if icon.get('android_conversion', '').startswith('SVG path'):
        target = ROOT/f"Paintroid/src/main/res/drawable/{icon['resource']}.xml"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(vector(svg))
        outputs.append({'path':str(target.relative_to(ROOT)), 'source_resource':icon['resource'],
                        'format':'VectorDrawable', 'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
        continue
    if args.vectors_only: continue
    for density, size in [('mdpi',44),('hdpi',66),('xhdpi',88),('xxhdpi',132),('xxxhdpi',176)]:
        target = ROOT / f"Paintroid/src/main/res/drawable-{density}/{icon['resource']}.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        cairosvg.svg2png(bytestring=svg, output_width=size, output_height=size, write_to=str(target))
        outputs.append({'path':str(target.relative_to(ROOT)), 'source_resource':icon['resource'],
                        'width':size,'height':size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
(ROOT / 'artwork/breeze/generated.json').write_text(json.dumps({'renderer':'CairoSVG 2.8.2; SVG path data to VectorDrawable for four additions','outputs':outputs},indent=2)+'\n')
print(f'Rendered {len(inventory["icons"])} Breeze icons into {len(outputs)} Android density resources.')
