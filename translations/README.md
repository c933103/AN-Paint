# Reused Paintroid vocabulary

AN Paint's View → Languages offers device default and 105 language/region/
script choices, including English. Most choices have partial translations; 28 have starter Brush, Save and Cancel vocabulary, the two Ainu script choices have Brush, Save and Done, and Tai Nüa has five sourced action labels. No choice is now name-only. This is partial vocabulary reuse, not a claim
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
Afrikaans now has a starter catalogue.
The remaining empty catalogues are not offered as translated choices.

Old Android `in` and `iw` resource qualifiers correspond to BCP-47 `id` and `he`.
Upstream `sr-rCS` and `sr-rSP` contain Latin and Cyrillic Serbian respectively;
they are exposed as `sr-Latn` and `sr-Cyrl`, with Android BCP-47 resource qualifiers.
Their original source paths and values remain unchanged in the provenance copy.

Android resources and Crowdin exports use one `strings.xml` per language directory.
`basic-translations.json` contains the explicitly labelled starter vocabulary.

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
with its horizontal language code. Native keyboard fields and format identifiers
remain editable in dialogs; a separate vertical preview displays the filename.

## Language options (0.0.26)

`language-options.json` is the reviewed source for names, legacy aliases,
translation bases and name-only choices. Both inventories pin `en-001` first
(English International); the in-app picker places device language above it.
All remaining entries follow case-insensitive BCP-47 order. Every label includes
its code, and names use consistent initial capitalization. Indonesian is
Bahasa Indonesia and Dutch is Nederlands. The traditional Mongolian autonym
keeps its bundled font and vertical writing; its two words fold into adjacent vertical columns beside the horizontal code.

The English choices include International, United States, United Kingdom,
Australia, Canada, Singapore and India. New English choices explicitly define
spelling and common commands, avoiding Android's fallback to an arbitrary
English region. International, Singapore and India use colour; US uses color.
Spanish offers `es-419` and `es-ES`, Korean offers `ko-KR` and `ko-KP`, and European
Portuguese is labelled `pt-PT`. These regional non-English choices inherit the
existing shared Spanish/Korean/Portuguese vocabulary; this update does not claim
an independent regional translation review. Old `en`, `es`, `ko` and `pt`
preferences migrate to `en-001`, `es-ES`, `ko-KR` and `pt-PT` respectively.

The 30 additional choices are `yue-Hant`, `yue-Latn`, `ryu`, `ain`, `cju`, `af`,
`ku`, `tt`, `lv`, `et`, `is`, `la`, `oc`, `se`, `my`, `shn`, `km`, `lo`, `ceb`,
`jv`, `bo`, `ug`, `za`, `tai`, `mww`, `nan-Hant-TW`, `nan-Latn-TW`, `hak-Hant`,
`hak-Latn` and `wuu-Hans`. Twenty-eight have a small generated translation catalogue; Ainu and the Tai collection use English fallback. For all choices,
missing interface text continues to fall back to English. Native-speaker review is welcome.

BCP-47 places script before region, so the requested `nan-TW-Hant`/`nan-TW-Latn`
are stored as `nan-Hant-TW`/`nan-Latn-TW`. `tai` is the registered Tai language
collection, labelled Tai languages. The Cantonese Latin starter vocabulary uses Jyutping with tone numbers. Other
Latin-script options do not claim a newly standardized romanization system. The metadata records primary naming
sources: the pinned MediaWiki autonym list, the IANA language-subtag registry,
Unicode CLDR and Jeju's official language dictionary.

## PR #1 review (0.0.28)

The consolidation preserves all 4,867 pre-existing string values. Coverage now
accounts for every offered choice, including starter and local catalogues and
regional choices sharing a translation base. A translated Save label is reused
by the unsaved-changes prompt as well as the File panel.

The starter vocabulary remains provisional. The unsupported Japanese substitutes
under Ainu and Thai substitutes under the Tai collection were removed. Their
language options remain available with English fallback and the actual chosen
locale. `tai` is a collection, not the code for Thai; see the
[IANA language subtag registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry).
The Okinawan Cancel label reuses `cancel` from
[MediaWiki ryu.json at ea83228](https://github.com/wikimedia/mediawiki/blob/ea83228d5fe2b1f9559196a2716c8580cdb2407d/languages/i18n/ryu.json),
credited to that catalogue's contributors under MediaWiki's GPL-2.0-or-later.
The Cantonese Latin Save label is corrected to `Cyu5 cyun4` (儲存); compare
[CantoneseClass101's own vocabulary explanation](https://www.cantoneseclass101.com/lesson/lower-intermediate-10-you-really-need-a-chinese-bank-account).
These corrections and automated checks do not certify every starter translation;
shared written forms and remaining vocabulary still need native-speaker review.


## Ainu script catalogues (0.0.29)

`ain-Latn` and `ain-Kana` replace the unscripted `ain` option, which migrates to
`ain-Latn`. Their names are Aynu itak and アイヌ イタㇰ. Three starter labels use
existing community vocabulary from [aynumosir/minecraft-ainu at 7156800](https://github.com/aynumosir/minecraft-ainu/blob/7156800b104515c0ddcc6b36fed7477f63444604/pack/assets/minecraft/lang/ain_latn.json):
Brush (`item.minecraft.brush`) → Hunte / フンテ;
Save (`mco.configure.world.buttons.save`) → Ukaosmare / ウカオㇱマレ;
Done (`gui.done`) → Okere / オケレ.
The source blob is `13dad2e29e9d05d32ea37a5dd8b2260a20d974ba`.
Initial capitalization follows the menu style. Kana output was checked with the
same `ainu-utils` 0.5.0 conversion used by that localization's build script.
Credit: Aynumosir and its Ainu localization contributors. These are selected
lexical labels, not a copy of its software or a complete translation. Cancel
and other unverified entries continue to fall back to English.

## Tai Nüa correction and translation audit (0.0.29, 15 September)

The requested language is Tai Nüa (`tdd`), not the collective `tai` code.
The picker now shows `ᥖᥭᥰ ᥖᥬᥲ ᥑᥨᥒᥰ [tdd]`; existing `tai` preferences migrate
to `tdd` in the app and Android 13's system language setting. The old catalogue
is removed. Historical entries above describe earlier releases only.

Five actions reuse [MediaWiki tdd.json at ea83228](https://github.com/wikimedia/mediawiki/blob/ea83228d5fe2b1f9559196a2716c8580cdb2407d/languages/i18n/tdd.json).
The autonym comes from `includes/Languages/Data/Names.php` at the same revision.
Credit: Aey Tai Nuea, AeyTaiNuea, Albertoleoncio, Dai Meng Mao Long and 咽頭べさ;
GPL-2.0-or-later. Mapping: `cancel` → `ui_cancel`, `edit` → `ui_menu_edit`,
`ok` → `ui_ok`, `savechanges` → `ui_save`, `editundo` → `ui_undo`.
The Save action deliberately uses the source's complete **Save changes** phrase,
also shared by the unsaved-changes prompt; it is not an invented generic Save
word or the source's Save page label. Brush, Discard changes and other unverified
terms remain English. This is starter coverage, not complete localization.

The split/renamed options have the following actual coverage. Counts below are
catalogue labels differing from default English, not a linguistic quality score.

| Choices | Implemented translation | Remaining limitation |
|---|---|---|
| `en-001`, `en-US`, `en-SG`, `en-IN` | Explicit English spelling/command overrides with complete English fallback | No independent regional terminology review |
| `es-419`, `es-ES` | Shared Spanish catalogue, 47 differing labels | No separate Latin American/European vocabulary yet |
| `ko-KP`, `ko-KR` | Shared Korean catalogue, 53 differing labels | No North Korean terminology adaptation yet |
| `pt-PT`, `pt-BR` | Existing distinct Portuguese catalogues, 49 / 52 differing labels | Partial editor coverage |
| `zh-TW`, `zh-HK` | Separate regional catalogues, 88 / 92 differing labels | Partial editor coverage |
| `mn-Cyrl-MN`, `mn-Mong` | Separate script foundations, 100 / 56 labels | Partial coverage; native-speaker review needed |
| `ain-Latn`, `ain-Kana` | Three sourced labels each: Brush, Save, Done | Cancel and the rest remain English |
| `nan-Hant-TW`, `nan-Latn-TW` | Three starter labels each; canonical BCP-47 script/region order | Partial coverage; review needed |
| `id`, `nl` | Existing Indonesian/Dutch catalogues retained when display names were corrected | No new translation was implied by the rename |

Literary Chinese (`lzh-Hant`) has 149 local foundation labels. The other newly
added starter choices each have three labels. Missing text uses English across
all partial catalogues. In particular, offering two regional choices is not a
claim that their regional terminology has been independently translated.


## GIMP editor vocabulary (0.0.31)

Selected standard editor labels now also come from the GIMP translators, pinned
to `e670132a59be1e8fb98d5b935824e4f57937b4ae` on the stable `gimp-3-2` branch.
Original source: <https://github.com/GNOME/gimp/tree/e670132a59be1e8fb98d5b935824e4f57937b4ae>.
`gimp-terms.json` explicitly maps 110 AN Paint labels to a gettext domain,
context and msgid. `gimp-catalogues.json` includes the selected original entries,
full catalogue translator/copyright headers, and SHA-256/Git blob hashes of the
complete upstream files. Sources are `po`, `po-libgimp` and `po-plug-ins`.

The snapshot supplies 5,216 candidate entries across 60 language bases, used by
62 of the offered language choices. Coverage varies from 6 to 110 labels per
base; these are partial editor vocabularies, not complete AN Paint translations.
`coverage.json` distinguishes available GIMP entries from those actually used
after local corrections. Shared source locales for regional choices remain
explicit in `language-options.json`; this does not claim independent regional
review. Rare-script locales receive no unrelated GIMP fallback.

`tools/gimp_translations.py` removes desktop mnemonics, adapts trailing
punctuation/ellipsis and quality units, and escapes Android strings. Fuzzy,
empty, plural and format-bearing translations are excluded. Existing reviewed
clipboard/unsaved-work and regional translations take precedence, as do the
Japanese horizontal/vertical flip corrections. Ambiguous same-English terms
(such as GIMP's WebP preset named Drawing or watercolor palette selector) were
excluded rather than repurposed as drawing tools.

GIMP translations remain **GPL-3.0-or-later**. AN Paint's combined distribution
is under **AGPL-3.0-or-later**, using section 13 of the respective licences.
The original translator headers and complete GPL text are bundled in
`Paintroid/src/main/assets/legal/GIMP_TRANSLATION_NOTICES.txt`, accessible from
File → About, licences & credits → GIMP translation credits & licence. They
also enter the generated third-party notices and exact corresponding source ZIP.
No endorsement by GIMP or its translators is implied. Paint.NET resources were
not imported: its published application licence does not permit this reuse.

Rebuild offline: `python tools/reuse_upstream_translations.py`.
Verify: `python -m unittest discover -s tools -p 'test_*.py'`.
