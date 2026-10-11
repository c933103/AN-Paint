#!/usr/bin/env python3
"""Enumerate every canonical catalogue, including non-picker locales.

This is a source applicability inventory, not a text-width, linguistic, installed
runtime or physical-device acceptance claim. Android remains the font/shaping oracle.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import translation_catalogues as catalogues

KEYS = ('ui_about_credits23', 'ui_icons_fonts_artwork_credits',
        'ui_open_source_credits_and_notices', 'ui_gimp_translations31',
        'ui_copy_all', 'ui_other_terms', 'ui_done', 'ui_cancel',
        'ui_image_credits', 'gallery_copy_credit', 'ui_save')
RUNTIME = ('en-US', 'hu', 'de', 'fr', 'pt-BR', 'ar', 'he', 'hi', 'th',
           'ja', 'ko-Kore-KR', 'zh-TW', 'mn-Cyrl-MN', 'vi-Hani', 'wuu-Hans')
VERTICAL = ('mn-Mong', 'mnc-Mong', 'lzh-Hant', 'en-XV', 'qaa-Zsye-XV')

def inventory():
    defaults = catalogues.default_resources()[0]
    offered = set(catalogues.offered_tags())
    rows = []
    paths = {'default': catalogues.RES / 'values/strings.xml', **catalogues.catalogue_paths()}
    for tag, path in sorted(paths.items()):
        own = defaults if tag == 'default' else catalogues.read_strings(path)
        rows.append(dict(tag=tag, offered=tag in offered,
            layout='vertical-columns' if tag in VERTICAL else 'horizontal-responsive-regions',
            runtime_representative=tag in RUNTIME or tag in VERTICAL,
            source_path=str(path.relative_to(catalogues.ROOT)),
            source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            exact_override_keys=[key for key in KEYS if key in own],
            missing_effective_keys=[key for key in KEYS if not own.get(key, defaults[key])]))
    return dict(scope='All canonical catalogues plus default; source applicability only',
        source_claim='Every catalogue reaches the same shared notice/dialog layout; no translation values change.',
        fallback_limit='exact_override documents direct source presence, not the full Android locale fallback algorithm.',
        coverage_limit='Selected API30/API35 Robolectric NATIVE profiles only; no full-language, accessibility-service or physical-device acceptance.',
        keys=KEYS, catalogues=len(rows), offered_languages=len(offered), rows=rows)

if __name__ == '__main__':
    print(json.dumps(inventory(), ensure_ascii=False, indent=2))
