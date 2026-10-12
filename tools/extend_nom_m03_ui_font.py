#!/usr/bin/env python3
"""Append only 返 U+8FD4 for the M03 Nôm metadata-response proposal.

Usage: python tools/extend_nom_m03_ui_font.py NomNaTong-Regular.ttf pre-m03.ttf output.ttf
Uses the existing pinned Nom Na Tong v5.18 source, licence and preservation-only
builder. Never overwrite either input; no downloads or inventory edits occur.
"""
import argparse
from extend_nom_ui_font import extend

BASE_SHA = '797ac4ef00f0dd8a982d5216dbd78db3edda07b578b9f8642d0156add90bd526'
ADDITIONS = (0x8FD4,)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('primary'); parser.add_argument('base'); parser.add_argument('output')
    args = parser.parse_args()
    extend(args.primary, args.base, args.output, base_sha=BASE_SHA, additions=ADDITIONS)
