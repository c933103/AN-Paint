#!/usr/bin/env python3
"""Append two normalization glyphs from the already-pinned Nom Na Tong release.

Usage: python tools/extend_nom_ui_font.py NomNaTong-Regular.ttf old-anpaintnomui.ttf output.ttf
Requires fonttools. No downloads, translation changes, or inventory edits.
The old subset and source must match the pinned hashes. Existing glyph order,
compiled outlines, advances, bearings, global metrics and name/licence metadata
are retained; by default only U+651D and U+671D are appended. Pinned follow-on
extensions can call extend with an explicit base hash and additions. The full
two-source builder is not used for these preservation-only deltas.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

PRIMARY_SHA = '37bd8506257d0905d499395e7f0bc2b6a2ae619dbb635a82ea0905b75b2ff5f3'
BASE_SHA = '399798cabc8de4d86e219ab92934bbac4fc9587e547487761ee7cf30167110aa'
ADDITIONS = (0x651D, 0x671D)


def extend(primary_path, base_path, output_path, *, base_sha=BASE_SHA, additions=ADDITIONS):
    primary_path, base_path, output_path = map(Path, (primary_path, base_path, output_path))
    inputs = (primary_path, base_path)
    if (output_path.resolve() in tuple(path.resolve() for path in inputs)
            or output_path.exists() and any(output_path.samefile(path) for path in inputs)):
        raise ValueError('Output must not overwrite either pinned input')
    additions = tuple(additions)
    if not additions or len(set(additions)) != len(additions) or any(cp < 0 or cp > 0xffff for cp in additions):
        raise ValueError('Expected distinct BMP codepoints for the existing cmap formats')
    if hashlib.sha256(primary_path.read_bytes()).hexdigest() != PRIMARY_SHA:
        raise ValueError('Unexpected Nom Na Tong v5.18 source')
    if hashlib.sha256(base_path.read_bytes()).hexdigest() != base_sha:
        raise ValueError('Unexpected pre-extension AN Paint Nom UI subset')
    from fontTools.ttLib import TTFont
    # Preserve raw outlines and font timestamps. The added glyphs fit the existing
    # global bounds/maxima; verify that explicitly rather than broad recalculation.
    source = TTFont(primary_path, recalcBBoxes=False, recalcTimestamp=False)
    font = TTFont(base_path, recalcBBoxes=False, recalcTimestamp=False)
    if source['head'].unitsPerEm != font['head'].unitsPerEm:
        raise ValueError('Source and subset units per em differ')
    source_map, old_map = source.getBestCmap(), dict(font.getBestCmap())
    old_order = list(font.getGlyphOrder())
    if set(additions) & old_map.keys():
        raise ValueError('Additions must be absent from the pre-extension subset')
    for cp in additions:
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
    if check.getGlyphOrder() != old_order + [source_map[cp] for cp in additions]:
        raise AssertionError('Existing glyph order changed')
    if set(check.getBestCmap()) != set(old_map) | set(additions):
        raise AssertionError('Unexpected CMAP delta')
    for cp, name in old_map.items():
        if check.getBestCmap()[cp] != name:
            raise AssertionError('An existing codepoint mapping changed')
    if len(original['cmap'].tables) != len(check['cmap'].tables):
        raise AssertionError('An existing cmap subtable was added or removed')
    for before, after in zip(original['cmap'].tables, check['cmap'].tables):
        if (before.platformID, before.platEncID, before.format, before.language) != (
                after.platformID, after.platEncID, after.format, after.language):
            raise AssertionError('An existing cmap subtable identity changed')
        expected = dict(before.cmap)
        if before.isUnicode() and before.format in (4, 12):
            expected.update({cp: source_map[cp] for cp in additions})
        if after.cmap != expected:
            raise AssertionError('Unexpected cmap subtable mapping delta')
    for name in old_order:
        if original['glyf'].glyphs[name].compile(original['glyf']) != check['glyf'].glyphs[name].compile(check['glyf']):
            raise AssertionError('An existing compiled outline changed')
        if original['hmtx'].metrics[name] != check['hmtx'].metrics[name]:
            raise AssertionError('An existing advance/bearing changed')
    for tag in ('OS/2', 'hhea', 'name', 'post'):
        if original.getTableData(tag) != check.getTableData(tag):
            raise AssertionError('Preserved metrics/name/licence table changed: ' + tag)
    # head changes only its whole-font checksum; maxp changes only numGlyphs.
    for tag, start, end in (('head', 8, 12), ('maxp', 4, 6)):
        before, after = original.getTableData(tag), check.getTableData(tag)
        if before[:start] + before[end:] != after[:start] + after[end:]:
            raise AssertionError('Preserved global metrics changed: ' + tag)
    result = dict(source_sha256=PRIMARY_SHA, base_sha256=base_sha,
                  added_codepoints=[f'U+{cp:04X}' for cp in additions],
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
