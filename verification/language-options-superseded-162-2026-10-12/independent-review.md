# Independent sixteen-option review

Source baseline: merged PR #57 at `1011233a89a3cac98f56fc2d46a902a9476a1e08`, independently fetched through GitHub. Its tree `bbf2766504e1b743cc9a580a429f0a2179a10b2d` is byte-identical to reviewed PR source `be60964a5b62c73f6517ec2fa8f58b101ab05c99`.

Result: no blocking source finding in the 37-path successor change reviewed on 12 October 2026. The source snapshot is bound by `reviewed-source-sha256.json`, SHA-256 `81cafb8f052cd82efd61b2dc24c5b8f16ac447102e4bb8614db862596908dae5`.

## Evidence

- 162 unique live options; all prior 146 identities and their relative order retained. Exactly 16 new requested options, no duplicate existing identity or exact resource catalogue.
- Picker tags, names, Android `app_locales.xml` and the new metadata rows agree. No app production Kotlin was modified.
- All 16 exact `values-b+TAG/strings.xml` catalogues are empty and truthfully marked translation/review not started. Default source has 695 translatable strings and one plural resource; registration supplies no translated content.
- The original six-option fixture and historical 140-option/81-fallback evidence remain unchanged. Current regression checks compose 22 additions and 103 out-of-scope fallback/partial catalogues without rewriting historical evidence.
- 64 focused Python tests passed in 11.111 seconds. Command: `PYTHONPATH=tools python3 -m unittest -v test_language_option_additions test_language_option_additions_second test_translations test_help_commons_provider test_commons_import_change_translations test_commons_copy_credit_errors test_commons_metadata_m03`.
- Seven independent negative controls were correctly rejected: duplicate tag, wrong autonym, an English-filled catalogue labelled untranslated, Nahuatl misclassified as an individual language, omitted second extension, changed prior identity at the same inventory size, and altered first-extension fixture.
- `git diff --check` passed.

## Language identity sources and limits

The [IANA registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry), File-Date 2026-09-17, supplies current registered nondeprecated tags. `nah` has collection scope; `qu` and `sa` have macrolanguage scope. The other thirteen are individual languages. The source explicitly keeps concrete Nahuatl, Quechua and Sanskrit translation-variety decisions open. It does not promise automatic matching from individual Nahuatl tags.

Autonyms agree with [pinned MediaWiki names](https://github.com/wikimedia/mediawiki/blob/eb2c0acaeeb2135c7a6e2952b536f0deb3343ba2/includes/Languages/Data/Names.php), with disclosed menu capitalization for Yucatec Maya and Tajik. MediaWiki's incidental variety comments were not used to override IANA taxonomy. [RFC 5646 §4.1](https://www.rfc-editor.org/rfc/rfc5646.html#section-4.1) supports retaining a broad identity when more precise language information is unavailable; translation scope still needs deliberate selection.

The `values-b+` form follows Android BCP-47 resource conventions, with two- and three-letter language parsing present in [AOSP locale implementation](https://android.googlesource.com/platform/frameworks/base/+/android-9.0.0_r1/tools/aapt2/Locale.cpp).

This is source/host verification. It does not establish Android compilation, emulator execution, glyph coverage, installed picker UI, completed translation, linguistic acceptance, or whole-UI acceptance. API 30/35 identity/fallback regression methods were inspected, not run by this independent review. Hosted results must be reported separately for the exact published commit.

## Merge-parent provenance refresh

Only the second fixture changed after initial source review: its parent commit now records the verified PR #57 merge, retaining the reviewed source commit and identical tree. Reversing those three provenance fields reconstructs the initially reviewed fixture SHA-256 exactly. All seven focused option tests and all seven independent mutation controls passed again after this refresh. No language or test logic changed.

## Tracker-generation checks

The pending sixteen-option tracker generator passed isolated tests with dummy PR/commit identifiers for both first-PR merge states. Both generated exactly 162 unique rows, retained all original 140 rows verbatim, kept the new sixteen rows at zero coverage/review not started, and matched all sixteen canonical Git blob hashes. The merged branch removed the first six pending-option markers and merge actions. These dummy outputs were not published; the final output must use verified real source identifiers.
