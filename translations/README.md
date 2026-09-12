# Reused Paintroid vocabulary

AN Paint's Settings → App language offers device default and 64 language/region/
script variants, including English. This is partial vocabulary reuse, not a claim
that the entire new editor has been translated. New or absent entries fall back
to English; the language picker explains that limitation.

The 42 mapped entries reuse the actual Paintroid translations for common brush,
shape, editing and save-dialog terms. The gallery's Use image button uses the
original translated Import image action; its Copy credit button uses the original
translated Copy action. The surrounding gallery instructions identify what will
be copied. Save-dialog File name and File format reuse Image name and Image format.
The original Quality label's terminal colon is removed because AN Paint's numeric
slider supplies its own punctuation. Other mapped translation values are preserved.

Source: [Catrobat/Paintroid at 853ce3c346910ea73aa4de5514f2a76ace1396fb](https://github.com/Catrobat/Paintroid/tree/853ce3c346910ea73aa4de5514f2a76ace1396fb/Paintroid/src/main/res).
Copyright belongs to the Catrobat Team and translation contributors, under
GNU AGPL-3.0-or-later. Original copyright and licence headers remain in all 73
source XML files under `upstream/`. AN Paint's AGPL notice and corresponding-source
export cover these changes. [Catrobat credits](https://developer.catrobat.org/credits).

`upstream-index.json` records every original path and Git blob hash;
`common-terms.json` maps AN Paint keys to their original resource keys;
`coverage.json` records source SHA-256, output path, language tag, reused-entry
count and the number differing from the original English value. A differing value
does not certify human translation quality. No machine translations were invented
to fill missing upstream entries.

Nine upstream locale files have no translated vocabulary among the mapped terms:
Afrikaans, Cherokee, Finnish, Hausa, Igbo, Georgian, Twi, Uzbek and Yoruba/Nigeria.
They are retained as provenance but are not misleadingly offered as translated
choices. Selecting device default with one of these languages uses English.

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
