"""Selected LibreOffice / MediaWiki gaps; glue is AGPL-3.0-or-later.

Original excerpts and their adaptations retain MPL-2.0 / GPL-2.0-or-later.
MPL excerpts are additionally offered under AGPL-3.0-or-later under MPL 3.3.
See translations/MAINSTREAM_SOURCE_AUDIT.md for context and licence evidence.
"""
import json
import pathlib
import re

DATA = pathlib.Path(__file__).resolve().parents[1] / 'translations'
PROJECTS = ('libreoffice', 'mediawiki')


def adapt(value, original, project):
    if project == 'libreoffice':
        value = re.sub(r'[（(]~[A-Za-z0-9][）)]', '', value).replace('~', '')
    value = value.strip().rstrip(':： .…').strip()
    if original.rstrip().endswith(('…', '...')):
        value += '…'
    return value


def load(project, defaults):
    snapshot = json.loads((DATA / f'{project}-catalogues.json').read_text())
    mapping = json.loads((DATA / f'{project}-terms.json').read_text())
    if not set(mapping) <= set(defaults):
        raise ValueError(f'Unknown resource in {project} mapping')
    lookups = {}
    for source in snapshot['sources']:
        if project == 'libreoffice':
            lookup = {}
            for entry in source['entries']:
                if re.search(r'^#,.*\bfuzzy\b', entry['raw'], re.M):
                    raise ValueError('Fuzzy LibreOffice entry')
                lookup[entry['msgctxt'], entry['msgid']] = entry['msgstr']
        else:
            lookup = source['messages']
        lookups[source['locale']] = lookup
    result = {}
    for tag, locale in snapshot['locale_map'].items():
        terms = {}
        for key, selector in mapping.items():
            source_key = (selector['msgctxt'], selector['msgid']) if project == 'libreoffice' else selector['key']
            value = lookups[locale].get(source_key)
            if not value:
                continue
            if re.search(r'[$%<>\[\]{}\n]', value) or re.search(r'%\d*\$?[sd]', defaults[key]):
                raise ValueError(f'Formatted text is outside the reviewed import: {project}/{tag}/{key}')
            value = adapt(value, defaults[key], project)
            source_english = selector.get('msgid', selector.get('english', ''))
            if value.casefold() in (adapt(source_english, defaults[key], project).casefold(), defaults[key].casefold()):
                continue
            if tag == 'uz-Latn' and re.search(r'[\u0400-\u04ff]', value):
                raise ValueError('Cyrillic text cannot enter the Uzbek Latin catalogue')
            value = value.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
            terms[key] = '"' + value + '"'
        if terms:
            result[tag] = terms
    return result


def notices(project):
    snapshot = json.loads((DATA / f'{project}-catalogues.json').read_text())
    text = [f'{project.title()} translation excerpts\n',
            'Repository: ' + snapshot['repository'] + '\n',
            'Revision: ' + snapshot['revision'] + '\n',
            'Original licence: ' + snapshot['license'] + '\n',
            'Original excerpts, message contexts, translator notices, source hashes and\n',
            'Android adaptations are distributed in translations/ with the corresponding source.\n',
            'Only remaining gaps are filled; reviewed translations retain precedence.\n']
    if project == 'libreoffice':
        text.extend(['Licence evidence: https://www.libreoffice.org/licenses/\n',
                     'Component: https://translations.documentfoundation.org/projects/libo_ui-26-2/officecfgregistrydataorgopenofficeofficeui/fy/\n',
                     'These excerpts and adaptations remain available under MPL-2.0 and are\n',
                     'additionally distributed under AGPL-3.0-or-later as part of AN Paint,\n',
                     'under MPL section 3.3. Desktop mnemonics and trailing punctuation are adapted.\n'])
    for source in snapshot['sources']:
        text.extend(['\n' + source['path'] + '\n', 'Git blob: ' + source['blob_sha'] + '\n'])
        text.append(source['header'] if project == 'libreoffice' else json.dumps(source['metadata'], ensure_ascii=False, indent=2) + '\n')
    filename = 'LIBREOFFICE-COPYING.MPL' if project == 'libreoffice' else 'MEDIAWIKI-COPYING.txt'
    text.extend(['\nFULL ORIGINAL LICENCE\n\n', (DATA / filename).read_text()])
    return ''.join(text)
