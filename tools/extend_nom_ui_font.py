#!/usr/bin/env python3
"""Append two normalization glyphs from the already-pinned Nom Na Tong release.

Usage: python tools/extend_nom_ui_font.py NomNaTong-Regular.ttf old-anpaintnomui.ttf output.ttf
Requires fonttools. No downloads, translation changes, or inventory edits.
The old subset and source must match the pinned hashes. Existing glyph order,
compiled outlines, advances, bearings, global metrics and name/licence metadata
are retained; only U+651D and U+671D are appended. The full two-source builder
remains available separately, but is not used for this preservation-only delta.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from fontTools.ttLib import TTFont

PRIMARY_SHA = '37bd8506257d0905d499395e7f0bc2b6a2ae619dbb635a82ea0905b75b2ff5f3'
BASE_SHA = '399798cabc8de4d86e219ab92934bbac4fc9587e547487761ee7cf30167110aa'
ADDITIONS = (0x651D, 0x671D)


def extend(primary_path, base_path, output_path):
    primary_path, base_path, output_path = map(Path, (primary_path, base_path, output_path))
    if hashlib.sha256(primary_path.read_bytes()).hexdigest() != PRIMARY_SHA:
        raise ValueError('Unexpected Nom Na Tong v5.18 source')
    if hashlib.sha256(base_path.read_bytes()).hexdigest() != BASE_SHA:
        raise ValueError('Unexpected pre-extension AN Paint Nom UI subset')
    # Preserve raw outlines and font timestamps. The added glyphs fit the existing
    # global bounds/maxima; verify that explicitly rather than broad recalculation.
    source = TTFont(primary_path, recalcBBoxes=False, recalcTimestamp=False)
    font = TTFont(base_path, recalcBBoxes=False, recalcTimestamp=False)
    if source['head'].unitsPerEm != font['head'].unitsPerEm:
        raise ValueError('Source and subset units per em differ')
    source_map, old_map = source.getBestCmap(), dict(font.getBestCmap())
    old_order = list(font.getGlyphOrder())
    if set(ADDITIONS) & old_map.keys():
        raise ValueError('Additions must be absent from the pre-extension subset')
    for cp in ADDITIONS:
        name = source_map[cp]
        if name in old_order:
            raise ValueError('New glyph name would replace an existing glyph')
        glyph = source['glyf'][name]
        if glyph.isComposite() or not glyph.numberOfContours:
            raise ValueError('Expected a nonempty, self-contained source outline')
        if glyph.numberOfContours > font['maxp'].maxContours or len(glyph.coordinates) > font['maxp'].maxPoints:
            raise ValueError('New outline exceeds the preserved font maxima')
        if len(glyph.program.getBytecode()) > font['maxp'].maxSizeOfInstructions:
            raise ValueError('New outline requires different instruction limits')
        if any(getattr(glyph, key) < getattr(font['head'], key) for key in ('xMin', 'yMin')) or any(
                getattr(glyph, key) > getattr(font['head'], key) for key in ('xMax', 'yMax')):
            raise ValueError('New outline exceeds the preserved global bounds')
        font['glyf'].glyphs[name] = copy.deepcopy(glyph)
        font['hmtx'].metrics[name] = source['hmtx'].metrics[name]
        font.setGlyphOrder(font.getGlyphOrder() + [name])
        for table in font['cmap'].tables:
            if table.isUnicode() and table.format in (4, 12):
                table.cmap[cp] = name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    font.save(output_path)
    check = TTFont(output_path, recalcBBoxes=False, recalcTimestamp=False)
    original = TTFont(base_path, recalcBBoxes=False, recalcTimestamp=False)
    if check.getGlyphOrder()[:len(old_order)] != old_order:
        raise AssertionError('Existing glyph order changed')
    if set(check.getBestCmap()) != set(old_map) | set(ADDITIONS):
        raise AssertionError('Unexpected CMAP delta')
    for cp, name in old_map.items():
        if check.getBestCmap()[cp] != name:
            raise AssertionError('An existing codepoint mapping changed')
    for name in old_order:
        if original['glyf'].glyphs[name].compile(original['glyf']) != check['glyf'].glyphs[name].compile(check['glyf']):
            raise AssertionError('An existing compiled outline changed')
        if original['hmtx'].metrics[name] != check['hmtx'].metrics[name]:
            raise AssertionError('An existing advance/bearing changed')
    for tag in ('OS/2', 'hhea', 'name', 'post'):
        if original.getTableData(tag) != check.getTableData(tag):
            raise AssertionError('Preserved metrics/name/licence table changed: ' + tag)
    result = dict(source_sha256=PRIMARY_SHA, base_sha256=BASE_SHA,
                  added_codepoints=[f'U+{cp:04X}' for cp in ADDITIONS],
                  preserved_codepoints=len(old_map), preserved_glyphs=len(old_order),
                  total_codepoints=len(check.getBestCmap()), total_glyphs=len(check.getGlyphOrder()),
                  bytes=output_path.stat().st_size,
                  sha256=hashlib.sha256(output_path.read_bytes()).hexdigest())
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('primary')
    parser.add_argument('base')
    parser.add_argument('output')
    args = parser.parse_args()
    extend(args.primary, args.base, args.output)
