"""AN Paint icon resource conversion, 2026-09-09; AGPL-3.0-or-later.

The artwork remains LGPL-3.0-or-later. See artwork/breeze/COPYING-ICONS.
Requires Python 3 and CairoSVG 2.8.2 (python3 -m pip install CairoSVG==2.8.2).
Normal Android builds use the checked-in PNGs and need no SVG runtime library.
Original SVG bytes, including dashed strokes, are rendered without redrawing.
"""
from pathlib import Path
import hashlib
import json
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artwork/breeze'
inventory = json.loads((ART / 'inventory.json').read_text())
outputs = []
for icon in inventory['icons']:
    svg = (ART / icon['upstream_path']).read_bytes()
    assert hashlib.sha256(svg).hexdigest() == icon['sha256'], icon['resource']
    for density, size in [('mdpi',44),('hdpi',66),('xhdpi',88),('xxhdpi',132),('xxxhdpi',176)]:
        target = ROOT / f"Paintroid/src/main/res/drawable-{density}/{icon['resource']}.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        cairosvg.svg2png(bytestring=svg, output_width=size, output_height=size, write_to=str(target))
        outputs.append({'path':str(target.relative_to(ROOT)), 'source_resource':icon['resource'],
                        'width':size,'height':size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
(ROOT / 'artwork/breeze/generated.json').write_text(json.dumps({'renderer':'CairoSVG 2.8.2','outputs':outputs},indent=2)+'\n')
print(f'Rendered {len(inventory["icons"])} Breeze icons into {len(outputs)} Android density resources.')
