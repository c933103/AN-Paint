# Reused Paintroid vocabulary

AN Paint's View → Languages offers device default and 104 language/region/
script choices, including English. Thirty explicitly requested entries currently
provide a name only and use the English interface. This is partial vocabulary reuse, not a claim
that the entire new editor has been translated. New or absent entries fall back
to English; the language picker explains that limitation.

The 42 mapped entries reuse the actual Paintroid translations for common brush,
shape, editing and save-dialog terms. The gallery's Use image button uses the
original translated Import image action; its Copy credit button uses the original
translated Copy action. The surrounding gallery instructions identify what will
be copied. Save-dialog File name and File format reuse Image name and Image format.
The original Quality label's terminal colon is removed because AN Paint's numeric
slider supplies its own punctuation. Japanese horizontal and vertical flip labels
are corrected to 左右反転 and 上下反転 respectively: the pinned upstream translation
had them reversed. `LOCAL_CORRECTIONS` in the generator records the original and
corrected values, and requires review if the upstream value changes. Coverage
records these separately from unchanged reused entries. Other mapped translation
values are preserved; the original source XML and its hashes remain unchanged.

Source: [Catrobat/Paintroid at 853ce3c346910ea73aa4de5514f2a76ace1396fb](https://github.com/Catrobat/Paintroid/tree/853ce3c346910ea73aa4de5514f2a76ace1396fb/Paintroid/src/main/res).
Copyright belongs to the Catrobat Team and translation contributors, under
GNU AGPL-3.0-or-later. Original copyright and licence headers remain in all 73
source XML files under `upstream/`. AN Paint's AGPL notice and corresponding-source
export cover these changes. [Catrobat credits](https://developer.catrobat.org/credits).

`upstream-index.json` records every original path and Git blob hash;
`common-terms.json` maps AN Paint keys to their original resource keys;
`coverage.json` records source SHA-256, output path, language tag, reused-entry
count and the number differing from the original English value. A differing value
does not certify human translation quality. The pinned upstream XML remains unchanged. Additional local catalogues are partial
editor translations and must not be presented as independently certified translations.

Nine upstream locale files originally had no translated vocabulary among the mapped terms:
Afrikaans, Cherokee, Finnish, Hausa, Igbo, Georgian, Twi, Uzbek and Yoruba/Nigeria.
They are retained as provenance. Later reviewed terms supply Finnish vocabulary;
Afrikaans is now explicitly offered as a name-only choice, with English UI.
The remaining empty catalogues are not offered as translated choices.

Old Android `in` and `iw` resource qualifiers correspond to BCP-47 `id` and `he`.
Upstream `sr-rCS` and `sr-rSP` contain Latin and Cyrillic Serbian respectively;
they are exposed as `sr-Latn` and `sr-Cyrl`, with Android BCP-47 resource qualifiers.
Their original source paths and values remain unchanged in the provenance copy.

Rebuild or check without network access:

```sh
python3 tools/reuse_upstream_translations.py
python3 tools/reuse_upstream_translations.py --check
python3 -m unittest discover -s tools -p 'test_translations.py'
```

The generator verifies each original file's Git blob hash before generating
translated resources and both language inventories (picker and Android 13's
system App languages page). Tests check matching bytes, valid resource names and
agreement between the language inventories. Missing translations deliberately
fall back to English; `MissingTranslation` lint is scoped to the default catalogue
for that documented policy. Other translation/resource errors remain checked.

Language changes rebuild the current editor controls without recreating its
document, so undo and unfinished selections remain available. Android 13 and newer
share the setting with the system App languages page. Older Android versions use
the saved app preference. Number entry and formatting follow the selected app
locale, while image file formats and source-language legal texts stay unchanged.


## Regional and script catalogues (0.0.24)

The same case-insensitive BCP-47 order was generated for every language in both
inventories; additions are integrated into that order, with device default first
only in the in-app picker. Traditional Chinese is offered as `zh-TW` (Taiwan) and
`zh-HK` (Hong Kong), with regional editor vocabulary such as 橡皮擦 / 擦膠 and
色盤 / 調色板. The removed `zh-Hant` preference migrates to `zh-TW` on both
legacy Android preferences and Android 13's LocaleManager.

`mn-Cyrl-MN` adds a horizontal Mongolian Cyrillic foundation alongside the vertical
`mn-Mong` foundation. Clipboard, undo/redo and confirmation terms for the new
catalogues are selected from AOSP `android-15.0.0_r1`; exact URLs, original Git
blob hashes and reused entries are recorded in `android-actions.json`. Other new
Mongolian terms are local editor translations and still need native-speaker review.
Missing terms continue to use English. Literary Chinese remains `lzh-Hant`.

Vertical UI captions use natural glyph sizes, joined Mongolian words and explicit
column wrapping. The language picker alone mixes a vertical Mongolian autonym
with a horizontal identifying label. Native keyboard fields and format identifiers
remain editable in dialogs; a separate vertical preview displays the filename.

## Language options (0.0.26)

`language-options.json` is the reviewed source for names, legacy aliases,
translation bases and name-only choices. Both inventories pin `en-001` first
(English International); the in-app picker places device language above it.
All remaining entries follow case-insensitive BCP-47 order. Every label includes
its code, and names use consistent initial capitalization. Indonesian is
Bahasa Indonesia and Dutch is Nederlands. The traditional Mongolian autonym
keeps its bundled font and vertical writing; its code occupies a separate line.

The English choices include International, United States, United Kingdom,
Australia, Canada, Singapore and India. New English choices explicitly define
spelling and common commands, avoiding Android's fallback to an arbitrary
English region. International, Singapore and India use colour; US uses color.
Spanish offers `es-419` and `es-ES`, Korean offers `ko-KR` and `ko-KP`, and European
Portuguese is labelled `pt-PT`. These regional non-English choices inherit the
existing shared Spanish/Korean/Portuguese vocabulary; this update does not claim
an independent regional translation review. Old `en`, `es`, `ko` and `pt`
preferences migrate to `en-001`, `es-ES`, `ko-KR` and `pt-PT` respectively.

The 30 name-only choices are `yue-Hant`, `yue-Latn`, `ryu`, `ain`, `cju`, `af`,
`ku`, `tt`, `lv`, `et`, `is`, `la`, `oc`, `se`, `my`, `shn`, `km`, `lo`, `ceb`,
`jv`, `bo`, `ug`, `za`, `tai`, `mww`, `nan-Hant-TW`, `nan-Latn-TW`, `hak-Hant`,
`hak-Latn` and `wuu-Hans`. They have no new translation resource catalogues.
Selection is retained while English resources are used explicitly, so related
language fallbacks cannot imply a translation that does not exist.

BCP-47 places script before region, so the requested `nan-TW-Hant`/`nan-TW-Latn`
are stored as `nan-Hant-TW`/`nan-Latn-TW`. `tai` is the registered Tai language
collection, labelled Tai languages. Labels that only request Latin script do
not claim a specific romanization system. The metadata records primary naming
sources: the pinned MediaWiki autonym list, the IANA language-subtag registry,
Unicode CLDR and Jeju's official language dictionary.
