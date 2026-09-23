# Translating AN Paint

AN Paint uses ordinary Android resource catalogues. The English source catalogue is
`Paintroid/src/main/res/values/strings.xml`, together with the other translatable
XML files in `Paintroid/src/main/res/values/`.

Each localized `strings.xml` under `Paintroid/src/main/res/values*/` is a
**canonical source file**. It is not generated from JSON and must not be overwritten
from Paintroid, GIMP, Krita, LibreOffice, MediaWiki, Android or any other application.

Those older catalogues remain under `translations/` as reference and provenance.
They can be useful terminology evidence, but they are not assumed to be correct.
When their wording conflicts with the meaning of AN Paint, the AN Paint translation
should be corrected directly in the locale's `strings.xml`.

The intended end state is a complete catalogue for every language offered by
View → Languages and Android's App languages page. English fallback is only a
temporary migration condition while the full-catalogue pass is being completed.

## Editing a translation

Edit the locale directly, for example:

- `Paintroid/src/main/res/values-ja/strings.xml`
- `Paintroid/src/main/res/values-fr/strings.xml`
- `Paintroid/src/main/res/values-zh-rHK/strings.xml`
- `Paintroid/src/main/res/values-b+yue+Hant/strings.xml`
- `Paintroid/src/main/res/values-b+sr+Latn/strings.xml`

Keep one `strings.xml` catalogue for each exact offered language/script/region.
Use explicit BCP-47 Android qualifiers for variants where a plain language qualifier
would be ambiguous.

Do not edit `translations/local-translations.json`,
`translations/basic-translations.json`, `translations/main-menu-translations.json`
or the imported catalogue snapshots as a way of changing the live UI. They document
earlier/imported work and can be consulted when reviewing terminology.

`crowdin.yml` points directly from the English Android catalogue to localized
Android `strings.xml` files, so no conversion step is needed for Crowdin or similar
Android-resource translation systems.

## Correctness rules

- Translate according to the actual AN Paint operation and surrounding UI. Existing
  wording from another application is evidence, not authority.
- Preserve positional placeholders such as `%1$s`, `%2$d` and `%3$.2f`.
  Their position may change but their number and type must not.
- Translate all plural forms required by the target language and preserve their
  placeholders.
- Preserve escaped newlines, literal percent signs, resource references and XML
  escaping.
- Entries marked `translatable="false"` are identifiers such as fixed export
  filenames and are not translated.
- Product, codec and licence names should remain recognizable where they are proper
  names.
- Legal licence bodies and copyright notices remain available verbatim; translate
  only their UI/navigation labels unless the licence itself supplies an official
  localized text.
- Distinguish regional and script variants where their terminology actually differs.
  Do not substitute a neighbouring language merely because it is easier to source.
- Script-specific catalogues must use the requested script. Romanized variants are
  not allowed to fall back to Cyrillic/Han/etc. text unless the item is itself a
  proper name conventionally written that way.
- Canvas directions, coordinates, image rotation and physical attachment directions
  describe image geometry. They must not be semantically mirrored merely because
  the surrounding interface is right-to-left.

## Sinitic variety conventions

Several language tags cover varieties for which a script tag alone does not identify
one universal written standard. AN Paint currently uses these explicit conventions:

- `lzh-Hant`: technical Literary Chinese in Traditional characters. Modern product,
  codec and computing terms may remain modern where forcing an archaic paraphrase
  would obscure the operation.
- `hak-Hant`: Sixian Hakka in Han characters.
- `hak-Latn`: the same Sixian Hakka wording in Pha̍k-fa-sṳ (PFS), not a
  romanization of Mandarin text.
- `nan-Hant-TW`: Taiwan Southern Min / Taiwanese Hokkien in Han characters.
- `nan-Latn-TW`: the same Taiwanese wording in Pe̍h-ōe-jī (POJ), not Mandarin
  transliteration.
- `wuu-Hans`: Simplified-script written Wu using Shanghainese as the concrete
  vernacular basis. `wuu` is a macrolanguage tag and this catalogue must not be
  described as a standardized pan-Wu written norm.

Han- and Latin-script pairs must stay semantically aligned, but the Latin catalogue
is a real orthographic rendering of the target variety rather than a character-by-
character transliteration of Standard Chinese.

## Validation

`tools/translation_catalogues.py` reads the canonical XML directly. Run:

```sh
python3 tools/translation_catalogues.py
python3 tools/translation_catalogues.py --complete
python3 -m unittest discover -s tools -p 'test_translations.py'
```

The first command checks catalogue/resource structure and format placeholders.
`--complete` additionally requires every translatable source key and plural
resource in every offered non-English locale. During the current completion pass,
the structural check is suitable for intermediate commits; the complete check is
the acceptance criterion for finishing the pass.

Then run the normal Android unit/lint checks and inspect both orientations, short
screens, large font sizes, dialogs, accessibility labels and RTL layouts as
applicable.

`TranslationReadinessTest` covers layout/resource behavior under RTL conditions.
`AppLanguageTest` covers persisted app-language choice, localized numeric entry,
Android 13 integration, and preserving the current canvas/undo/selection state
through a language change.

## Provenance material

Files under `translations/upstream/` and the GIMP/Krita/LibreOffice/MediaWiki/
Android snapshot files are retained so previous wording and licences remain
auditable. They do not regenerate or override canonical Android locale files.

Known imported errors should remain documented where useful. For example, the
historical Paintroid Japanese horizontal/vertical flip strings were reversed;
AN Paint's canonical Japanese catalogue uses `左右反転` for horizontal flip and
`上下反転` for vertical flip.

## Locale conventions used by AN Paint

Some BCP-47 language tags cover more than one spoken variety or more than one
writing convention. AN Paint labels the concrete convention used by each catalogue
instead of implying that one file is a neutral standard for the entire macrolanguage.

- `lzh-Hant`: technical Literary Chinese in Traditional script. Classical grammar
  and concise imperatives are preferred, while modern technical proper names and
  unavoidable computing terminology remain recognizable.
- `hak-Hant`: Sixian Hakka in Han characters.
- `hak-Latn`: the same Sixian Hakka wording in Pha̍k-fa-sṳ (PFS). It is a companion
  catalogue, not a romanization of Mandarin wording.
- `nan-Hant-TW`: Taiwan Hokkien/Taiwanese in Han characters.
- `nan-Latn-TW`: the same Taiwan Hokkien wording in Pe̍h-ōe-jī (POJ).
- `wuu-Hans`: Shanghai-based written Wu in Simplified script. The `wuu` tag covers
  multiple Wu varieties; this catalogue does not claim to be a standardized pan-Wu
  written language.

For script-paired catalogues, first settle the vernacular wording and semantics in
that language, then keep the companion script/romanization semantically aligned.
Do not create a Latin catalogue by mechanically romanizing Mandarin or another
neighbouring Sinitic language.
