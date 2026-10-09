# AN-W05-C03: active Help names the Commons provider

Base: `55a6158a9b651871d0d204e52fb34c0f8a20d2a0`, the merged PR31 tree.

## Bounded change

Only the provider-list passage inside `ui_help23` changes in the default resource
and the existing 59-tag scoped catalogues. The exact existing
`commons_blank_maps` menu caption is quoted in each complete Help message.
Nothing is dynamically concatenated at runtime. No production Kotlin, Activity,
layout, provider implementation, attribution value, persisted credit, font,
workflow, or language-picker inventory changes.

The actual Other images picker has device files plus `CATROBAT`, `IRASUTOYA`,
`OPENCLIPART`, and `COMMONS` in that order. File > How to use opens the active
`ui_help23` message through `ui`; the dormant historical manual is not edited.
Source references at the base:

- [Picker and enum routing](https://github.com/c933103/AN-Paint/blob/55a6158a9b651871d0d204e52fb34c0f8a20d2a0/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L886-L899)
- [Provider inventory and caption](https://github.com/c933103/AN-Paint/blob/55a6158a9b651871d0d204e52fb34c0f8a20d2a0/Paintroid/src/main/java/org/catrobat/paintroid/classic/IllustrationSource.kt#L8-L14)
- [Active Help route](https://github.com/c933103/AN-Paint/blob/55a6158a9b651871d0d204e52fb34c0f8a20d2a0/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1576-L1577)

`translations.json` is a separate one-key C03 manifest, not an extension of PR29's
SVG error or PR31's import-note manifest. It records every exact before/after
segment and surrounding context, plus decoded Help SHA-256 hashes. Replacing the
new segment with the old one reconstructs the complete prior Help text exactly.
`source-scope.json` records whole-file hashes and checks that even XML bytes outside
that single element body are unchanged.

The other 81 offered tags still omit this key and use genuine default fallback.
No English-filled override is added. This is not acceptance of those languages,
the complete Help text, or any historical localization claim.

## Review and typography

The implementing pass and two independent editorial passes read all 60 provider-list
segments. The existing list conjunctions and localized Commons captions are
preserved; grammatical cases around quoted labels are carried by words such as
Estonian `valikut`, Finnish `-valinnan`, Hungarian `menüpontot`, and Turkish
`seçeneğini`. Quoting the menu caption keeps its displayed spelling unchanged.
This is bounded consistency/editorial review, not native-speaker fluency validation.
The additional independent editorial review completed before publication. Its
one concrete finding, Nôm spacing before a quoted
label, is corrected and protected by both host and JVM wording checks.
`independent-review.json` records its bounded findings and remaining uncertainty;
reusing a caption does not prove the new sentence natural in every language.

Primary references used for two concrete corrections:

- [EKI quotation guidance](https://teatmik.eki.ee/teatmik/jutumargid/): Estonian
  opening `„` and closing `“` follow the strong current convention documented by EKI.
- [Kotus multiword compounds](https://kielitoimistonohjepankki.fi/ohje/yhdysmerkki-sanaliiton-sisaltavissa-yhdyssanoissa-avaimet-kateen-sopimus/):
  the Finnish quoted multiword label needs a space before `-valinnan`.
- [Kotus quotation marks](https://kielitoimistonohjepankki.fi/ohje/lainausmerkit/):
  Finnish uses `”` at both ends. Ryukyuan retains the catalogue's existing `「」` convention.

All newly used characters already occur in the same respective catalogue.
The existing four bundled-font inventory/coverage checks pass, including all Nôm
catalogue codepoints and required Mongolian/Manchu letters. No font extension is
needed or made. Android glyph assertions are also included for the affected
Commons captions with complete bundled UI fonts; a full visual/layout audit is
not claimed.

## Validation boundary

- Five new Python contracts cover exact scope, genuine absence in the other 81
  catalogues, reverse-hash preservation of the complete surrounding Help text,
  provider inventory, route wiring, caption identity, formatting and the two
  punctuation corrections.
- New Robolectric tests resolve all 59 scoped Help/caption pairs and all 81 real
  fallbacks on API30 and API35. Independent representative full-passage oracles
  cover English, French, Japanese, Nôm, Estonian and Finnish.
- A real-Activity test under the API35 Robolectric configuration opens File > How to use twice with normal
  dismissal, then opens/cancels the actual Other images picker for French,
  Japanese, Mongolian script, Nôm, and an Amharic fallback. It compares the whole
  displayed Help body and the real adapter inventory. Locale preference presence,
  platform app locales, global resources and default locale are restored exactly.
- These add seven JVM/Robolectric executions, not device execution. No installed instrumentation method is added;
  the existing installed suite and 180-second ordinary-suite budget stay intact.
  Exact-head hosted results and timing/margins remain pending until linked in the PR.
  Installed results are regression coverage, not new Help-specific device coverage.
- Local Android execution was attempted with Java21 and stopped before Gradle
  started: its wrapper could not download `gradle-8.13-bin.zip` because the local
  network returned `Network is unreachable`. This is not a compilation or runtime pass.

All 341 Python tests passed in 52.368 seconds after the review correction. The full raw result and local Gradle
limitation are recorded under `local/`.
Android compilation, lint, packaged resources, JVM execution and installed checks
must be evaluated from the exact published-head CI run before acceptance.
