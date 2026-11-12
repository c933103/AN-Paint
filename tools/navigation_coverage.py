#!/usr/bin/env python3
"""Report navigation coverage from the same definitions that build the editor.

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


def navigation_keys(validate_source: bool = True) -> set[str]:
    # EditorCommand/EditorTab/EditGroup are actual UI definitions. New entries
    # automatically enter the audit; no locale or command-key list is maintained here.
    definitions = (CLASSIC / 'EditorNavigation.kt').read_text()
    # Only enum constructor labels are actual controls. The title() fallback is
    # not a reachable tab and must not expand the visible-navigation inventory.
    keys = set(re.findall(r'\b[A-Z_][A-Z_0-9]*\((?:"[^"]+",)?R\.string\.(\w+)', definitions))
    for name in ('ToolCategoryButton.kt', 'PaintDocument.kt'):
        keys.update(re.findall(r'\b[A-Z_][A-Z_0-9]*\(R\.string\.(\w+),', (CLASSIC / name).read_text()))
    actions = (CLASSIC / 'ActionButton.kt').read_text().split('class ActionButton(', 1)[0]
    keys.update(re.findall(r'R\.string\.(\w+)', actions))
    source = catalogues.default_resources()[0]
    unknown = keys - source.keys()
    if unknown and validate_source:
        raise ValueError('Unknown navigation keys: ' + ', '.join(sorted(unknown)))
    return keys


def _resolve_local(key: str, values: dict[str, str]) -> str | None:
    seen = set()
    while key in values and key not in seen:
        seen.add(key)
        value = values[key].strip()
        if value.startswith('@string/'):
            key = value.removeprefix('@string/')
        else:
            return value.strip('"').replace(r"\'", "'").replace(r'\n', '\n')
    return None


def _same_prose(value: str, source: str | None) -> bool:
    if source is None or not re.search('[A-Za-z]{3,}', source) or source.isupper():
        return False
    def letters(text):
        return ''.join(c for c in text.casefold() if c.isalpha())
    return letters(value) == letters(source)


def coverage(tag: str) -> dict:
    keys = navigation_keys()
    path = catalogues.catalogue_paths()[tag]
    local = catalogues.read_strings(path)
    defaults = catalogues.default_resources()[0]
    missing = sorted(keys - local.keys())
    fallbacks = sorted(key for key in keys & local.keys() if _resolve_local(key, local) is None)
    # Matching English can also be a valid loanword. Report it for review instead
    # of treating either presence or a different spelling as linguistic approval.
    matches = [] if tag.startswith('en') else sorted(key for key in keys & local.keys()
        if (value := _resolve_local(key, local)) is not None
        and _same_prose(value, _resolve_local(key, defaults)))
    return dict(locale=tag, total=len(keys), present=len(keys)-len(missing), missing=missing,
                fallback_aliases=fallbacks, english_matches_for_review=matches)


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
    return int(args.require_complete and any(row['missing'] or row['fallback_aliases'] for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
