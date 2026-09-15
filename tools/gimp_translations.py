"""Adapt selected, context-matched GIMP vocabulary from the bundled PO excerpts.

AN Paint contributors, 2026, AGPL-3.0-or-later. The original catalogue entries
and translator notices remain GPL-3.0-or-later; see translations/README.md.
"""
import json
import pathlib
import re

DATA = pathlib.Path(__file__).resolve().parents[1] / 'translations'


def adapt(value, original, suffix=''):
    # GIMP uses both inline Latin mnemonics and suffixes for CJK languages.
    value = re.sub(r'[（(]_[A-Za-z0-9][）)]', '', value).replace('_', '').strip()
    value = value.rstrip(':： .…').strip()
    if original.rstrip().endswith(('…', '...')):
        value += '…'
    return value + suffix


def load(defaults):
    snapshot = json.loads((DATA / 'gimp-catalogues.json').read_text())
    mapping = json.loads((DATA / 'gimp-terms.json').read_text())
    if not set(mapping) <= set(defaults):
        raise ValueError('Unknown resource in GIMP mapping')
    lookups = {}
    for source in snapshot['sources']:
        lookup = {}
        for entry in source['entries']:
            if not entry['msgstr'].strip() or re.search(r'%|\n', entry['msgstr']) or re.search(r'^#,.*\bfuzzy\b', entry['raw'], re.M):
                raise ValueError('Unreviewed fuzzy, empty or formatted GIMP entry')
            lookup[entry.get('msgctxt', ''), entry['msgid']] = entry['msgstr']
        lookups[source['locale'], source['domain']] = lookup
    results = {}
    for tag, locale in snapshot['locale_map'].items():
        terms = {}
        for key, selector in mapping.items():
            value = lookups.get((locale, selector['domain']), {}).get((selector['msgctxt'], selector['msgid']))
            if value:
                # Fully quote Android strings after escaping literal backslashes,
                # quotes and apostrophes; leading @/? must not become references.
                value = adapt(value, defaults[key], selector.get('suffix', ''))
                value = value.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
                terms[key] = '"' + value + '"'
        if terms:
            results[tag] = terms
    return results
