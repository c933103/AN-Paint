"""Generate AN Paint launcher assets. Copyright 2026 AN Paint contributors; AGPL-3.0-or-later.
Requires CairoSVG 2.8.2. The checked-in resources are sufficient for Android builds.
"""
from pathlib import Path
import hashlib
import json
import argparse
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('--xml-only', action='store_true', help='Keep existing PNG resources; regenerate XML and verify every output hash.')
args = parser.parse_args()
if not args.xml_only:
    import cairosvg

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artwork/an-paint'
RES=ROOT/'app/src/main/res'
SOURCE=(ART/'launcher.svg').read_text()
svg=ET.fromstring(SOURCE)
paths=[node for node in svg if node.tag.endswith('path')]
outputs=[]
def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(data if isinstance(data,bytes) else data.encode())
    outputs.append({'path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
for density,size in [('ldpi',36),('mdpi',48),('hdpi',72),('xhdpi',96),('xxhdpi',144),('xxxhdpi',192)]:
    for suffix,source in [('',SOURCE),('_round',SOURCE.replace('rx="23"','rx="54"'))]:
        path = RES/f'mipmap-{density}/an_paint_launcher{suffix}.png'
        if args.xml_only:
            outputs.append({'path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        else:
            save(path,cairosvg.svg2png(bytestring=source.encode(),output_width=size,output_height=size))
notice='<!-- Copyright (C) 2026 AN Paint contributors. GNU AGPL-3.0-or-later. -->\n'
foreground=notice+'<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">\n'
# The A outline and its counter have opposite winding. Android's default nonzero
# fill therefore preserves the hole on API 21+, without the API-24 fillType.
foreground+=f'    <path android:fillColor="#FFFFFF" android:pathData="{paths[0].get("d")}"/>\n'
foreground+=f'    <path android:fillColor="#00000000" android:strokeColor="#FFD700" android:strokeWidth="6" android:strokeLineCap="round" android:pathData="{paths[1].get("d")}"/>\n</vector>\n'
save(RES/'drawable/an_paint_launcher_foreground.xml',foreground)
save(RES/'drawable/an_paint_launcher_monochrome.xml',foreground.replace('#FFD700','#FFFFFF'))
save(RES/'values/an_paint_launcher.xml',notice+'<resources><color name="an_paint_launcher_background">#5B67FF</color></resources>\n')
for api in [26,33]:
    xml=notice+'<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n    <background android:drawable="@color/an_paint_launcher_background"/>\n    <foreground android:drawable="@drawable/an_paint_launcher_foreground"/>\n'
    # Android ignores the monochrome child before API 33. Keep it in both icon
    # definitions, as recommended by Android's adaptive-icon documentation.
    xml+='    <monochrome android:drawable="@drawable/an_paint_launcher_monochrome"/>\n'
    xml+='</adaptive-icon>\n'
    for suffix in ['', '_round']: save(RES/f'mipmap-anydpi-v{api}/an_paint_launcher{suffix}.xml',xml)
(ART/'generated.json').write_text(json.dumps({'source':'artwork/an-paint/launcher.svg','licence':'AGPL-3.0-or-later','renderer':'CairoSVG 2.8.2','outputs':outputs},indent=2)+'\n')
print(f'Generated {len(outputs)} launcher resources.')
