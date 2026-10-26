#!/usr/bin/env python3
"""Append six glyphs needed by the reviewed Nôm exact-position controls.

Usage: python tools/extend_nom_position_ui_font.py NomNaTong-Regular.ttf base.ttf output.ttf
Uses pinned Nom Na Tong v5.18 and preserves every existing outline, mapping,
metric and name/licence table. No downloads, translations or inventory edits.
"""
import argparse
from extend_nom_ui_font import extend

BASE_SHA = '6b70d3c5c146c9d11503e5dff7ade5e7ccb3ae5a70c511f71902d4a75f7a3006'
ADDITIONS = (0x4EFD, 0x6089, 0x6578, 0x91CD, 0x2A700, 0x2CA20)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('primary'); parser.add_argument('base'); parser.add_argument('output')
    args = parser.parse_args()
    extend(args.primary, args.base, args.output, base_sha=BASE_SHA, additions=ADDITIONS)
