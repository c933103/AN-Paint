#!/usr/bin/env python3
"""Structural/font checks only. Does not assess fluency or approve translations."""
import hashlib
import json
from pathlib import Path
import re
import sys
from xml.etree import ElementTree as ET
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
INPUT = HERE / 'proposals.json'
FONT = ROOT / 'Paintroid/src/main/assets/fonts/anpaintnomui.ttf'
data = json.loads(INPUT.read_text())
expected = {'ain-Kana','ain-Latn','bo','dz','hak-Hant-TW','hak-Latn-TW','jje','mn-Mong','mnc-Mong','ryu','vi-Hani'}
assert set(data['translations']) == expected
keys = set(data['source_messages'])
svg = 'commons_import_svg_changes'
raster = 'commons_import_raster_changes'
literals = ['AN Paint', 'SVG → PNG', 'antiAlias=false', 'strokeDashArray=none', 'background=#FFFFFF']
per_locale = {}
for locale, values in data['translations'].items():
    assert set(values) == keys
    for key, text in values.items():
        assert text and text.startswith('AN Paint: ') and text.endswith('.')
        assert '\n' not in text and not re.search(r'%\d*\$?[a-zA-Z]', text)
        assert 'original size' not in text and 'alpha compositing' not in text
        assert text.count('AN Paint') == 1 and text.count('background=#FFFFFF') == 1
        node = ET.Element('string', name=key)
        node.text = text
        assert ET.fromstring(ET.tostring(node, encoding='utf-8')).text == text
    for literal in literals:
        assert values[svg].count(literal) == 1
    positions = [values[svg].index(literal) for literal in literals]
    assert positions == sorted(positions)
    assert values[svg].count(';') == 4
    assert values[raster].count('alpha') == 1
    assert values[raster].count('(') == values[raster].count(')') == 1
    per_locale[locale] = {'whole_messages': 2, 'xml_round_trip': True, 'technical_literals': True, 'english_prose_fallback_absent': True}

latin = 'alpha ani noka kor iro newa oka iro a=ukopoye'
kana = 'alpha アニ ノカ コㇿ イロ ネワ オカ イロ アウコポイェ'
alignment = dict(zip(latin.split(), kana.split()))
assert ' '.join(alignment[word] for word in latin.split()) == kana
assert '(' + latin + ')' in data['translations']['ain-Latn'][raster]
assert '(' + kana + ')' in data['translations']['ain-Kana'][raster]

font = TTFont(FONT)
cmap = font.getBestCmap()
text = ''.join(data['translations']['vi-Hani'].values())
chars = sorted(set(text), key=ord)
missing = [c for c in chars if ord(c) not in cmap or font.getGlyphID(cmap[ord(c)]) == 0]
empty = [c for c in chars if not c.isspace() and c not in missing and font['glyf'][cmap[ord(c)]].numberOfContours == 0]
assert not missing, missing
assert not empty, empty
result = {
    'source_commit': data['source_commit'],
    'proposal_sha256': hashlib.sha256(INPUT.read_bytes()).hexdigest(),
    'scope': sorted(expected),
    'full_pairs': len(expected),
    'full_messages': sum(len(v) for v in data['translations'].values()),
    'per_locale': per_locale,
    'ainu_latin_kana_token_pairing': True,
    'font_check': {
        'scope': 'All codepoints in both vi-Hani candidates, including immutable Latin technical literals.',
        'path': str(FONT.relative_to(ROOT)),
        'sha256': hashlib.sha256(FONT.read_bytes()).hexdigest(),
        'unicode_cmap_entries': len(cmap),
        'candidate_unique_codepoints': len(chars),
        'missing_codepoints': [{'character':c,'codepoint':f'U+{ord(c):04X}'} for c in missing],
        'empty_nonspace_glyphs': [{'character':c,'codepoint':f'U+{ord(c):04X}'} for c in empty],
        'font_change_needed_for_codepoint_coverage': False,
        'font_changed_by_this_work': False,
        'shaping_or_visual_rendering_tested': False
    },
    'language_acceptance': False,
    'independent_composition_review_performed_by_this_author': False,
    'android_or_layout_tested': False,
    'production_resources_edited_by_this_worker': False,
    'limit': 'Checks establish exact text structure, literal preservation, XML serialization and glyph presence only. They cannot establish fluency, semantic correctness, visual shaping or runtime integration.'
}
(HERE/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'pairs':result['full_pairs'],'messages':result['full_messages'],'nom_missing':missing,'nom_empty_nonspace':empty,'language_acceptance':False}))
