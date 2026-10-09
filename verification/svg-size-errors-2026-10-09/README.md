# Two SVG original-size errors: incomplete AN-W05 draft

Analysis base: `develop` at `5bf82b67199aaecbd341a8b150a887f8d60b5567`, tree
`05f9f6aa330f2f1432264938d5d0e41dfe8d86ee`.
Publication base: merged #28 at `4b615ce2d9e27814df84812b90858b5f676ce51a`, tree
`84107dd03e8ac96ed953afd95bf6cbe5b72f84c4`. Its device-language-row changes are
preserved without modification; they do not overlap this patch.
This follows [AN-W05-C01's source inventory](https://github.com/c933103/AN-Paint/pull/20#issuecomment-6077456325).

**Not ready to merge.** This draft has two default-English resources and 96 proposed
values in 48 of the existing 59 scoped catalogues. The remaining 22 values in 11
scoped catalogues are deliberately absent pending adequate language/script evidence.
Their existing English fallback is preserved, not copied into localized overrides.
The other 81 offered incomplete catalogues remain separate unfinished work.
Therefore these two messages currently have 48 exact offered overrides and 92
offered-tag gaps. The full 59-catalogue acceptance gate remains unchanged and fails.

## Production change

`SvgOriginalSize` keeps the same finite/positive and ceil-to-Int checks. A typed
`IllegalArgumentException` subclass identifies the two reasons without depending
on Android resources. The gallery's existing error presentation maps only that
exception to canonical resources; all other exception messages pass through as
before. No memory limit, bitmap limit, input dimension, resizing, canvas fallback,
network, metadata, file cleanup, credit-association or successful-import behavior
is changed. The two English messages retain their original words.

The unchanged meaning is important:
- A usable original size was not declared; no canvas-based size was substituted.
- The original size exceeds Android's bitmap dimension limit; no resizing was applied.
- The bitmap dimension limit is not the memory budget or the 32 MiB SVG download limit.
- “No resizing” must not become merely “no automatic shrinking.”

## Coverage and evidence

`translations.json` lists all 48 proposed pairs, the exact 11 blockers and the other
81 offered tags. `initial-proposals.json` preserves the original source-assisted
proposal/evidence snapshot. Its description refers to the proposal stage; the
non-null values were subsequently copied into this incomplete draft's resources.
`translation-review.md` records each scoped locale's terminology, source catalogue
link and limitations. These are source-assisted proposals, not independent
native-speaker acceptance.

The missing scoped tags are `ain-Kana`, `ain-Latn`, `bo`, `dz`, `hak-Hant-TW`,
`hak-Latn-TW`, `jje`, `mn-Mong`, `mnc-Mong`, `ryu`, and `vi-Hani`.
The additional bounded evidence pass found reusable size/no-resize language and two
partial Hakka size-limit candidates, but no complete additional pair. Its exact
remaining declaration/substitution/grammar questions are in
`additional-pass-review.md` and `.json`, with inspected source clauses in
`additional-clause-evidence.json`. PDF-invalid-size and destination-replacement
failure messages are not asserted to mean undeclared SVG size or an intentionally
absent canvas substitute. No neighboring-language or mechanical-script conversion
has been inserted to satisfy the gate.

## Tests and actual results

- Canonical XML/format structure passes; five new focused host checks pass.
- The full host suite executes **315 methods and reports 16 failing completeness
  records**, all caused by the 22 withheld values in those same 11 scoped locales.
  There are no errors or skips. This is a failed result, not a pass with exceptions.
- Global strict completeness now reports **92 incomplete offered catalogues** and
  173 report entries: the previous 81 plus these 11 newly incomplete scoped catalogues.
- `host-tests.log` and `checks.json` retain the complete local result and its hash.
  `host-tests-rebased.log` repeats the full run on the publication base with the
  same 315-method / 16-completeness-failure result; no unrelated failure appeared.
  JSON diagnostic failures later in that log are intentional existing negative
  instrumentation-runner fixtures, not an Android test run performed here.
- All previous test bodies/assertions, completeness groups, workflows and deadlines
  are unchanged. `SvgOriginalSizeTest` only gains additive cases. The focused
  manifest check does not replace the full gate.
- Added pure Kotlin regressions classify both width/height failure modes and retain
  boundary/fractional behavior. Added API30/35 Robolectric tests use real gallery
  actions, downloaded SVG fixture bytes, the real SVG parser and displayed status.
  They cover six representative resource contexts, repeated attempts, the failed
  import's `RESULT_CANCELED`, no substitute-size dialog, temporary-file cleanup, no credit association,
  and unchanged unrelated diagnostics. Nôm/Manchu are explicitly tested as current
  English-reason fallback, not claimed translated.
- Those Kotlin/Robolectric tests are **authored, not executed locally**. This executor
  has Java 21 but no Android SDK, cached Gradle or Kotlin compiler. Normal CI will
  report build/device outcomes separately; its existing early host gate prevents
  JVM/lint execution while this known completeness failure remains.

No physical-device, screen-reader, native shaping/layout, fluent-language, or
complete-batch acceptance is claimed. The draft needs the missing source-supported
wording, updated resource/fallback expectations, fresh passing full checks and
acceptable exact-head review before integration. Merged #28 is preserved unchanged.
