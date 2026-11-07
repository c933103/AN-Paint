#!/usr/bin/env python3
"""Report direct coverage of editor navigation, independently of P0/P1 tiers.

Read current consumers and canonical XML; presence does not certify translation
quality, Android routing, glyph support, or a complete language catalogue.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import translation_catalogues as catalogues

ROOT = Path(__file__).resolve().parents[1]
CLASSIC = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'


def navigation_keys() -> set[str]:
    activity = (CLASSIC / 'ClassicPaintActivity.kt').read_text()
    menu = activity.split('private fun menuTitle(', 1)[1].split('private fun menuActionEnabled(', 1)[0]
    titles = menu.split('private fun menuActions(', 1)[0]
    keys = set(re.findall(r'R\.string\.(\w+)', titles))
    keys.update(re.findall(r'ui\(R\.string\.(\w+)\)\s+to\s+\{', menu))
    keys.update(re.findall(r'command\(ui\(R\.string\.(\w+)\)', menu))
    # First enum argument is a caption. The second PaintTool argument is help.
    for name in ('ToolCategoryButton.kt', 'PaintDocument.kt'):
        keys.update(re.findall(r'\b[A-Z_]+\(R\.string\.(\w+),', (CLASSIC / name).read_text()))
    actions = (CLASSIC / 'ActionButton.kt').read_text().split('class ActionButton(', 1)[0]
    keys.update(re.findall(r'R\.string\.(\w+)', actions))
    groups = activity.split('private enum class EditGroup', 1)[1].split('private lateinit var toolDrawer', 1)[0]
    keys.update(re.findall(r'R\.string\.(\w+)', groups))
    # Additional visible controls in buildWorkspace/makePalette.
    keys.update(('ui_other_images34', 'ui_swap23', 'ui_reset_bw23', 'ui_advanced', 'ui_add_colour26'))
    source = catalogues.default_resources()[0]
    unknown = keys - source.keys()
    if unknown:
        raise ValueError('Unknown navigation keys: ' + ', '.join(sorted(unknown)))
    return keys


def coverage(tag: str) -> dict:
    keys = navigation_keys()
    path = catalogues.catalogue_paths()[tag]
    local = catalogues.read_strings(path)
    missing = sorted(keys - local.keys())
    return dict(locale=tag, total=len(keys), present=len(keys)-len(missing), missing=missing)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--locale', action='append', help='Offered locale; repeat to select several')
    parser.add_argument('--require-complete', action='store_true', help='Exit nonzero for missing navigation keys')
    args = parser.parse_args()
    tags = args.locale or catalogues.offered_tags()
    unknown = set(tags) - set(catalogues.offered_tags())
    if unknown:
        parser.error('Unknown offered locale(s): ' + ', '.join(sorted(unknown)))
    rows = [coverage(tag) for tag in tags]
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return int(args.require_complete and any(row['missing'] for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
