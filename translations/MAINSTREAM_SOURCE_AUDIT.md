# Mainstream translation-source audit — 16 September 2026

The supplementary search is limited to major applications, with priority given
to languages absent from AN Paint's pinned GIMP import. Repository or translation
hosting (GitHub, GitLab, Crowdin, Weblate) does not itself grant permission to
reuse text; the application/catalogue licence and original notices govern reuse.

Existing imports were not limited to GIMP: they also include Paintroid's
Crowdin-origin Android resources, AOSP action labels, selected MediaWiki actions,
and the previously documented Ainu community vocabulary. Their sources and
credits remain unchanged.

| Application | Source checked | Current result (0.0.36) |
| --- | --- | --- |
| Krita | Official KDE GitLab project and its GitHub mirror, revision `428d44705de20770434ea2915021241dc073879c` | 14 non-English catalogues absent from the GIMP locale map inspected; 256 actual resource gap fills across 12 language bases, including 8 additional partial choices. |
| Inkscape | [Official translation repository](https://gitlab.com/inkscape/translations) and [translation service](https://translate.inkscape.org/projects/inkscape/master/inkscape/kn/) | GPL-2.0-or-later catalogue licence confirmed. No Inkscape terms imported in this change; a pinned, context-level extraction has not been completed. |
| LibreOffice | [Pinned command catalogues](https://github.com/LibreOffice/translations/tree/84fc1f3ce6a7d0ff415ac93495ba172b8ce2bac6/source) and [official translation service](https://translations.documentfoundation.org/projects/libo_ui-26-2/) | 206 actual resource gap fills across 14 existing language choices, using exact GenericCommands contexts. |
| MediaWiki | [Pinned core catalogues](https://github.com/wikimedia/mediawiki/tree/ea83228d5fe2b1f9559196a2716c8580cdb2407d/languages/i18n) and `qqq.json` message documentation | 26 further resource gap fills across eight existing choices. This extends the earlier narrow Ryukyuan/Tai Nüa use. |
| Paint.NET | [Official translation documentation](https://paint.net/doc/latest/Translations.html) and [application licence](https://paint.net/license.html) | Official RESX translations use Crowdin, but these pages do not establish a separate licence allowing catalogue reuse. No import. Independently published language packs require their own explicit permission; none has been imported. |

## LibreOffice and MediaWiki import (0.0.36)

The 0.0.35 work checked LibreOffice's inventory/licensing but did not extract
individual terms. MediaWiki had only supplied a few starter actions and language
names. Paint.NET's application licence had been mentioned in the older translation
notes; there was no catalogue-level audit or import. The current review checks
the official sources directly and records the narrower actual scope above.

LibreOffice uses the `officecfg/registry/data/org/openoffice/Office/UI.po`
component. Its [translation service](https://translations.documentfoundation.org/projects/libo_ui-26-2/officecfgregistrydataorgopenofficeofficeui/fy/)
identifies MPL-2.0; [LibreOffice's licence statement](https://www.libreoffice.org/licenses/)
and the full retained `LIBREOFFICE-COPYING.MPL` supply the terms. Excerpts and
adaptations remain available under MPL-2.0 and are additionally distributed
under AGPL-3.0-or-later under MPL section 3.3, when combined into AN Paint.
Original headers remain intact. See also the
[MPL compatibility guidance](https://www.mozilla.org/en-US/MPL/2.0/FAQ/#q14-may-i-combine-mpl-licensed-code-and-lgpl-licensed-code-in-the-same-executable-program).

The mapping selects 27 Android resource keys by exact msgctxt and English msgid:
menu labels come from popup-menu contexts, clipboard actions from command
contexts, and geometric tools from their shape commands. It deliberately avoids
using reset-formatting `Clear` for clearing a canvas, and avoids replacing the
formatted `Save as %1$s` resource with an unformatted label. Fuzzy, empty and
English-copy entries are excluded. Desktop `~` mnemonics and trailing dialog
punctuation are adapted. Uzbek is explicitly mapped to `uz-Latn`, with a check
against Cyrillic leakage. Interlingua and Northern Sámi have no such component
at this revision and produce no import.

MediaWiki uses seven documented keys: Cancel, Help, OK, Edit, Undo, Done and
Save. It does not reuse the File namespace tab as a File menu or wiki-specific
page commands as canvas commands. Markup, variables and language fallbacks are
excluded; only messages present in the exact language JSON are eligible.
Core message documentation was checked in `qqq.json`. Jeju has no core catalogue
at the pinned revision, so nothing is invented for it. The full upstream
`COPYING` (GPL-2.0-or-later) and every selected catalogue's `@metadata` authors
are retained. Wikipedia article text and website documentation licences are
not used as the source of these software strings.

All 22 full source files matched their reported Git blob hashes before
excerpting. `libreoffice-catalogues.json` and `mediawiki-catalogues.json` retain
file identities, original selected entries and contributor metadata; the term
maps retain exact semantic selectors. Both original licences and notices enter
the APK and matching corresponding source. No new language choices are added:
there remain 135 offered choices, with varying partial coverage. Context review
does not imply independent native-speaker review of every label.

| Existing choice | LibreOffice gap fills | MediaWiki gap fills |
| --- | ---: | ---: |
| Afrikaans (`af`) | 26 | 0 |
| Tibetan (`bo`) | 21 | 0 |
| Cebuano (`ceb`) | 0 | 3 |
| Welsh (`cy`) | 24 | 0 |
| Western Frisian (`fy`) | 22 | 0 |
| Javanese (`jv`) | 1 | 0 |
| Latin (`la`) | 0 | 4 |
| Lao (`lo`) | 26 | 1 |
| Maithili (`mai`) | 19 | 0 |
| Ryukyuan (`ryu`) | 0 | 4 |
| Sindhi (`sd`) | 18 | 0 |
| Shan (`shn`) | 0 | 5 |
| Albanian (`sq`) | 14 | 0 |
| Swahili (`sw`) | 5 | 0 |
| Tai Nüa (`tdd`) | 0 | 1 |
| Tagalog (`tl`) | 6 | 0 |
| Toki Pona (`tok`) | 0 | 5 |
| Uyghur (`ug`) | 3 | 0 |
| Urdu (`ur`) | 1 | 0 |
| Uzbek Latin (`uz-Latn`) | 20 | 0 |
| Zhuang (`za`) | 0 | 3 |
| **Total resources** | **206** | **26** |

Existing translations and all 30 reviewed main-menu catalogues retain
precedence. Coverage counts compare the final generated resources, after menu
overrides; candidate entries are reported separately. Offline regeneration and
host checks verify notices, contexts, scripts, exact gap counts and preservation
of every previously translated label.

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
