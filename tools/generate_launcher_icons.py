"""Generate AN Paint launcher assets from the editable vector artwork.

Copyright 2026 AN Paint contributors; SPDX-License-Identifier: AGPL-3.0-or-later.
Requires CairoSVG 2.8.2. Checked-in resources are sufficient for Android builds.
"""
from pathlib import Path
import argparse
import hashlib
import json
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('--xml-only', action='store_true',
                    help='Keep existing PNG resources; regenerate XML and hash every output.')
parser.add_argument('--preview-directory', type=Path,
                    help='Also render square, round and themed previews at 48, 96 and 512 px.')
args = parser.parse_args()
if not args.xml_only or args.preview_directory:
    import cairosvg

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artwork/an-paint'
RES = ROOT / 'app/src/main/res'
SOURCE = (ART / 'launcher.svg').read_bytes()
svg = ET.fromstring(SOURCE)
NS = {'svg': 'http://www.w3.org/2000/svg'}
foreground = svg.find("svg:g[@id='foreground']", NS)
monochrome = svg.find("svg:defs/svg:g[@id='monochrome']", NS)
background = svg.find("svg:rect[@id='background']", NS)
assert foreground is not None and monochrome is not None and background is not None
outputs = []


def record(path):
    outputs.append({'path': path.relative_to(ROOT).as_posix(),
                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode())
    record(path)


def render_source(round_mask=False, themed=False, adaptive=False):
    """Return SVG for legacy output or a launcher-style adaptive mask preview."""
    root = ET.fromstring(SOURCE)
    bg = root.find("svg:rect[@id='background']", NS)
    if round_mask:
        bg.set('rx', '54')
    if adaptive:
        # Android crops the outer 18 dp of the 108 dp layer before applying
        # a launcher mask. Preview the visible central 72 dp for visual review.
        root.set('viewBox', '18 18 72 72')
        bg.set('x', '18')
        bg.set('y', '18')
        bg.set('width', '72')
        bg.set('height', '72')
        bg.set('rx', '36' if round_mask else '16')
    if themed:
        root.remove(root.find("svg:g[@id='foreground']", NS))
        copy = ET.fromstring(ET.tostring(monochrome))
        for path in copy:
            path.set('fill', '#21005D')
        root.append(copy)
    return ET.tostring(root)


for density, size in [('ldpi', 36), ('mdpi', 48), ('hdpi', 72),
                      ('xhdpi', 96), ('xxhdpi', 144), ('xxxhdpi', 192)]:
    for suffix, is_round in [('', False), ('_round', True)]:
        path = RES / f'mipmap-{density}/an_paint_launcher{suffix}.png'
        if args.xml_only:
            record(path)
        else:
            # Legacy launchers do not crop the adaptive layer's parallax margin.
            # Bake the visible 72 dp area so the symbol keeps the same size.
            save(path, cairosvg.svg2png(bytestring=render_source(is_round, adaptive=True),
                                       output_width=size, output_height=size))

notice = '<!-- Copyright (C) 2026 AN Paint contributors. GNU AGPL-3.0-or-later. -->\n'


def vector(group):
    # Filled paths only: no font, filters, raster layers, API-24 fillType or
    # transformations whose Android rendering differs from the SVG source.
    result = notice + ('<vector xmlns:android="http://schemas.android.com/apk/res/android" '
                       'android:width="108dp" android:height="108dp" '
                       'android:viewportWidth="108" android:viewportHeight="108">\n')
    for node in group:
        assert node.tag == '{http://www.w3.org/2000/svg}path'
        assert set(node.attrib) == {'fill', 'd'}, 'Use simple filled paths for Android parity.'
        result += f'    <path android:fillColor="{node.get("fill")}" android:pathData="{node.get("d")}"/>\n'
    return result + '</vector>\n'


save(RES / 'drawable/an_paint_launcher_foreground.xml', vector(foreground))
save(RES / 'drawable/an_paint_launcher_monochrome.xml', vector(monochrome))
save(RES / 'values/an_paint_launcher.xml', notice +
     f'<resources><color name="an_paint_launcher_background">{background.get("fill")}</color></resources>\n')
for api in [26, 33]:
    xml = notice + ('<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
                    '    <background android:drawable="@color/an_paint_launcher_background"/>\n'
                    '    <foreground android:drawable="@drawable/an_paint_launcher_foreground"/>\n'
                    '    <monochrome android:drawable="@drawable/an_paint_launcher_monochrome"/>\n'
                    '</adaptive-icon>\n')
    for suffix in ['', '_round']:
        save(RES / f'mipmap-anydpi-v{api}/an_paint_launcher{suffix}.xml', xml)

(ART / 'generated.json').write_text(json.dumps({
    'source': 'artwork/an-paint/launcher.svg',
    'source_sha256': hashlib.sha256(SOURCE).hexdigest(),
    'licence': 'AGPL-3.0-or-later',
    'renderer': 'CairoSVG 2.8.2',
    'outputs': outputs
}, indent=2) + '\n')
if args.preview_directory:
    args.preview_directory.mkdir(parents=True, exist_ok=True)
    for name, is_round, is_themed, is_adaptive in [
        ('square', False, False, True), ('round', True, False, True),
        ('adaptive-square', False, False, True), ('adaptive-round', True, False, True),
        ('themed-square', False, True, True), ('themed-round', True, True, True)
    ]:
        for size in [48, 96, 512]:
            data = render_source(is_round, is_themed, is_adaptive)
            cairosvg.svg2png(bytestring=data, output_width=size, output_height=size,
                             write_to=str(args.preview_directory / f'{name}-{size}.png'))
    # Full adaptive layer, transparent foreground and the 66 dp safe-zone overlay
    # make edge padding inspectable without introducing these guides into assets.
    for name, guide in [('foreground', False), ('safe-zone', True)]:
        root = ET.fromstring(SOURCE)
        root.remove(root.find("svg:rect[@id='background']", NS))
        if guide:
            ET.SubElement(root, '{http://www.w3.org/2000/svg}circle', {
                'cx': '54', 'cy': '54', 'r': '33', 'fill': 'none',
                'stroke': '#1D1B20', 'stroke-width': '0.3', 'stroke-dasharray': '1 1'})
        cairosvg.svg2png(bytestring=ET.tostring(root), output_width=512, output_height=512,
                         write_to=str(args.preview_directory / f'{name}-512.png'))
print(f'Generated {len(outputs)} launcher resources.')
