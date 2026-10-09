#!/usr/bin/env python3
"""Append only 豫 U+8C6B for the Nôm SVG error translation.

Usage: python tools/extend_nom_svg_ui_font.py NomNaTong-Regular.ttf pre-svg.ttf output.ttf
Requires fonttools and the two exact pinned inputs. No downloads, translations,
inventory edits, or changes to other fonts. See tools/extend_nom_ui_font.py for
preservation checks. Keep output distinct from both input paths.
"""
import argparse

from extend_nom_ui_font import extend

BASE_SHA = '1c809021f3c74ce27bb7cbe73e63339f46fa66f5b85252db504f4f62405701b9'
ADDITIONS = (0x8C6B,)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('primary')
    parser.add_argument('base')
    parser.add_argument('output')
    args = parser.parse_args()
    extend(args.primary, args.base, args.output, base_sha=BASE_SHA, additions=ADDITIONS)
