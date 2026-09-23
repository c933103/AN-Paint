#!/usr/bin/env python3
"""Rebuild the bundled Nôm UI subset from two pinned, locally supplied fonts.

Usage: python tools/build_nom_ui_font.py NomNaTong-Regular.ttf GothicNguyen.ttf
Requires fonttools. This tool never generates or changes translations.
"""
from pathlib import Path
import hashlib
import json
import sys
import tempfile
import xml.etree.ElementTree as ET
from fontTools import subset
from fontTools.merge import Merger
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'Paintroid/src/main/assets'
PRIMARY_SHA = '37bd8506257d0905d499395e7f0bc2b6a2ae619dbb635a82ea0905b75b2ff5f3'
SECONDARY_GIT_BLOB = '7edfe73d9b730e3ae3422fd5d8c7bd73b8b9ac18'


def build(primary, secondary):
    first = Path(primary).read_bytes()
    second = Path(secondary).read_bytes()
    assert hashlib.sha256(first).hexdigest() == PRIMARY_SHA, 'Unexpected Nom Na Tong release'
    assert hashlib.sha1(b'blob ' + str(len(second)).encode() + b'\0' + second).hexdigest() == SECONDARY_GIT_BLOB, 'Unexpected Gothic Nguyen source'
    catalogue = ROOT / 'Paintroid/src/main/res/values-b+vi+Hani/strings.xml'
    text = ''.join(ET.parse(catalogue).getroot().itertext()) + '㗂越（𡨸喃）'
    # Include punctuation, ASCII and the original problem glyphs as stable regressions.
    required = {ord(c) for c in text} | set(range(0x20, 0x7f)) | {0x367b,0x5838,0x6c7b,0x7e7f,0x25ec2,0x26ef3,0x2e7b6}
    fonts = [TTFont(primary), TTFont(secondary)]
    cmaps = [font.getBestCmap() for font in fonts]
    ideographs = {cp for cp in required if 0x3400 <= cp <= 0x9fff or 0x20000 <= cp <= 0x3ffff}
    assert not (ideographs - cmaps[0].keys() - cmaps[1].keys()), 'Uncovered Nôm ideograph'
    allocations = [required & cmaps[0].keys(), (required - cmaps[0].keys()) & cmaps[1].keys()]
    with tempfile.TemporaryDirectory() as directory:
        paths = []
        for index, (font, codepoints) in enumerate(zip(fonts, allocations)):
            options = subset.Options()
            options.name_IDs = ['*']
            options.name_legacy = True
            options.name_languages = ['*']
            options.drop_tables += ['GSUB','GPOS','GDEF','BASE','JSTF','DSIG']
            processor = subset.Subsetter(options=options)
            processor.populate(unicodes=codepoints)
            processor.subset(font)
            path = Path(directory) / f'{index}.ttf'
            font.save(path)
            paths.append(str(path))
        merged = Merger().merge(paths)
    names = {1:'AN Paint Nom UI', 2:'Regular', 3:'AN Paint Nom UI 1.0',
             4:'AN Paint Nom UI', 6:'ANPaintNomUI-Regular', 16:'AN Paint Nom UI',17:'Regular',
             13:'SIL Open Font License 1.1. Nom Na Tong source is also subject to its retained MIT notice. See bundled notices.',
             14:'https://openfontlicense.org/'}
    for name_id, value in names.items():
        merged['name'].removeNames(nameID=name_id)
        merged['name'].setName(value,name_id,3,1,0x409)
    merged['head'].created = 3862464000
    merged['head'].modified = 3862464000
    merged.recalcTimestamp = False
    output = ASSETS / 'fonts/anpaintnomui.ttf'
    merged.save(output)
    actual = TTFont(output).getBestCmap()
    assert ideographs <= actual.keys()
    inventory_path = ASSETS / 'fonts/inventory.json'
    inventory = json.loads(inventory_path.read_text())
    for entry in inventory:
        if entry['id'] == 'anpaintnomui':
            entry['sha256'] = hashlib.sha256(output.read_bytes()).hexdigest()
    inventory_path.write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
    print(f'Covered {len(ideographs)} ideographs, including {sum(cp>0xffff for cp in ideographs)} supplementary characters; {output.stat().st_size} bytes')
    print('SHA256:',hashlib.sha256(output.read_bytes()).hexdigest())


if __name__ == '__main__':
    build(*sys.argv[1:])
