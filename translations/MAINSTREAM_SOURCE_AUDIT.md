# Mainstream translation-source audit — 16 September 2026

The supplementary search is limited to major applications, with priority given
to languages absent from AN Paint's pinned GIMP import. Repository or translation
hosting (GitHub, GitLab, Crowdin, Weblate) does not itself grant permission to
reuse text; the application/catalogue licence and original notices govern reuse.

Existing imports were not limited to GIMP: they also include Paintroid's
Crowdin-origin Android resources, AOSP action labels, selected MediaWiki actions,
and the previously documented Ainu community vocabulary. Their sources and
credits remain unchanged.

| Application | Source checked | Result in 0.0.35 |
| --- | --- | --- |
| Krita | Official KDE GitLab project and its GitHub mirror, revision `428d44705de20770434ea2915021241dc073879c` | 14 non-English catalogues absent from the GIMP locale map inspected; 256 actual resource gap fills across 12 language bases, including 8 additional partial choices. |
| Inkscape | [Official translation repository](https://gitlab.com/inkscape/translations) and [translation service](https://translate.inkscape.org/projects/inkscape/master/inkscape/kn/) | GPL-2.0-or-later catalogue licence confirmed. No Inkscape terms imported in this change; a pinned, context-level extraction has not been completed. |
| LibreOffice | [Translation repository](https://github.com/LibreOffice/translations/tree/84fc1f3ce6a7d0ff415ac93495ba172b8ce2bac6/source) and [official translation service](https://translations.documentfoundation.org/projects/libo_ui-26-2/) | Broad language inventory checked, including languages outside GIMP. Official translation components use MPL-2.0. No LibreOffice terms imported in this change; component-specific mapping and notice review remain to be done. |

## Krita import

Krita's [licence statement](https://krita.org/en/about/license/) identifies GPL
version 3 for the application, with file-specific notices retained. The exact
upstream `COPYING` text is in `KRITA-COPYING.txt`. Original catalogue headers,
including translator names and older component notices, remain in
`krita-catalogues.json` and the APK's `KRITA_TRANSLATION_NOTICES.txt`.
The combined application uses the GPL/AGPL version 3 section 13 provisions;
this does not replace the original catalogue notices.

The import maps 76 AN Paint resource keys by exact gettext context and msgid.
Clipboard labels use action contexts, image mirroring uses image actions, and
colour inversion uses the colour filter rather than selection inversion.
Fuzzy, plural, empty, multiline and format-bearing entries are excluded.
Desktop keyboard mnemonics and trailing punctuation are adapted for Android;
existing translated strings and all reviewed menu overrides retain precedence.
English source copies are not counted as translated coverage.

The 14 full source catalogues were checked against their pinned Git blob SHA-1
before excerpting. `audited_sources` records every inspected file, including
Tajik and Cyrillic Uzbek, which yielded no usable non-fuzzy matches. Those two
do not get empty language-menu entries. The 12 retained sources contain 261
matching original entries; repeated resources, existing translations, English
copies and explicit semantic rejection explain the distinct effective count.

One clear upstream error is rejected: Afrikaans `Rectangle` is translated as
`Driehoek` (triangle). Its original entry remains available for audit but is not
imported. Matching context and a suitable licence are not claims of independent
native-speaker review of every translation.

| Language choice | Imported resource gap fills |
| --- | ---: |
| Afrikaans (`af`, existing) | 2 |
| Albanian (`sq`, existing) | 4 |
| Northern Sámi (`se`, existing) | 24 |
| Uyghur (`ug`, existing) | 62 |
| Welsh (`cy`, new) | 13 |
| Western Frisian (`fy`, new) | 18 |
| Chhattisgarhi (`hne`, new) | 16 |
| Interlingua (`ia`, new) | 60 |
| Maithili (`mai`, new) | 18 |
| Toki Pona (`tok`, new) | 3 |
| Uzbek Latin (`uz-Latn`, new) | 12 |
| Walloon (`wa`, new) | 24 |

These are partial vocabulary choices, not completed interfaces. In particular,
the three Toki Pona labels do not imply broad coverage. The existing 30 reviewed
main-menu catalogues are preserved. `coverage.json` records the exact used keys
and counts, separately from candidate availability and menu completion.

Regenerate with `python tools/reuse_upstream_translations.py`; validate with
`python -m unittest discover -s tools -p 'test_translations.py'`.
