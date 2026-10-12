#!/usr/bin/env python3
"""Append only 。 U+3002, 問 U+554F and 追 U+8FFD for reviewed M04 Nôm wording.

Usage: python tools/extend_nom_m04_ui_font.py NomNaTong-Regular.ttf pre-m04.ttf output.ttf
Uses the existing pinned Nom Na Tong v5.18 source, licence and preservation-only
builder. Never overwrite either input; no downloads or inventory edits occur.
"""
import argparse
from extend_nom_ui_font import extend

BASE_SHA = '4ae4cab599622f6c9d66b8a99074f2a291ffc32000a78ba69f241fc12eb64e05'
ADDITIONS = (0x3002, 0x554F, 0x8FFD)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('primary'); parser.add_argument('base'); parser.add_argument('output')
    args = parser.parse_args()
    extend(args.primary, args.base, args.output, base_sha=BASE_SHA, additions=ADDITIONS)
