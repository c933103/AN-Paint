"""Context-matched Krita vocabulary, used only to fill remaining translation gaps.

AN Paint glue: AGPL-3.0-or-later. Catalogue excerpts keep their original licences
and translator notices; see translations/MAINSTREAM_SOURCE_AUDIT.md.
"""
import json
import pathlib
import re

DATA = pathlib.Path(__file__).resolve().parents[1] / 'translations'


def adapt(value, original, suffix=''):
    value = re.sub(r'[（(]&[A-Za-z0-9][）)]', '', value)
    value = value.replace('&&', '\0').replace('&', '').replace('\0', '&').strip()
    value = value.rstrip(':： .…').strip()
    if original.rstrip().endswith(('…', '...')):
        value += '…'
    return value + suffix


def load(defaults):
    snapshot = json.loads((DATA / 'krita-catalogues.json').read_text())
    mapping = json.loads((DATA / 'krita-terms.json').read_text())
    if not set(mapping) <= set(defaults):
        raise ValueError('Unknown resource in Krita mapping')
    lookups = {}
    for source in snapshot['sources']:
        lookup = {}
        for entry in source['entries']:
            if not entry['msgstr'].strip() or re.search(r'%|\n|<|>', entry['msgstr']) or re.search(r'^#,.*\bfuzzy\b', entry['raw'], re.M):
                raise ValueError('Unreviewed fuzzy, empty or formatted Krita entry')
            if source['locale'] == 'af' and entry.get('msgctxt', '') == '' and entry['msgid'] == 'Rectangle':
                # The pinned catalogue says "Driehoek" (triangle), not rectangle.
                continue
            lookup[entry.get('msgctxt', ''), entry['msgid']] = entry['msgstr']
        lookups[source['locale']] = lookup
    results = {}
    for tag, locale in snapshot['locale_map'].items():
        terms = {}
        for key, selector in mapping.items():
            value = lookups.get(locale, {}).get((selector['msgctxt'], selector['msgid']))
            if value:
                value = adapt(value, defaults[key], selector.get('suffix', ''))
                # English source copies are not evidence of a translated label.
                if value.casefold() == defaults[key].strip().strip('"').casefold():
                    continue
                value = value.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
                terms[key] = '"' + value + '"'
        if terms:
            results[tag] = terms
    return results


def notices():
    snapshot = json.loads((DATA / 'krita-catalogues.json').read_text())
    text = ['Krita translation excerpts — preserved translator notices\n',
            'Source: https://invent.kde.org/graphics/krita\n',
            'Official mirror: ' + snapshot['repository'] + '\n',
            'Revision: ' + snapshot['revision'] + '\n',
            'Krita is distributed under GPL version 3. Catalogue-specific notices follow.\n',
            'The full GPL version 3 text follows the catalogue headers below.\n',
            'AN Paint selects context-matched vocabulary, removes desktop mnemonics,\n',
            'adapts trailing punctuation, and fills gaps without replacing reviewed menus.\n',
            'Exact excerpts, mappings and source blob hashes are in translations/.\n']
    for source in snapshot['sources']:
        text.extend(['\n' + source['path'] + '\n', 'Git blob: ' + source['blob_sha'] + '\n', source['header']])
    text.extend(['\nFULL KRITA LICENCE\n\n', (DATA / 'KRITA-COPYING.txt').read_text()])
    return ''.join(text)
