# PR117 selected-resource numeric formatting repair

Codex finding: https://github.com/c933103/AN-Paint/pull/117#discussion_r4303256624

The original pt-BR consumer test incorrectly accepted English/ROOT numeric punctuation. This follow-up fixes the production consumers and corrects that expectation; it does not remove or weaken full-message checks.

- Original head: `76807df744b990159fa62c2a68cfe7f4558b967b`.
- Repaired head: `30413454eaa1c1599c15a0a42a4110d8d1976514`.
- Repaired tree: `3ac7a0abe119504abbde70537bd6d4a2fcc46d3d`.
- All 1,184 application blobs and modes match the prior complete tree plus the six-file repair delta.
- Prior 341-entry linguistic evidence remains immutable at https://github.com/c933103/AN-Paint/tree/fb0c77cb5964df034989c692d39f952d76a73e01 . The eight wording changes, their resource blob, all three holds and PR56 are unchanged.

## Repair

`ImageDimensions.describe()` and `memoryLabel()` in ImageImport.kt now pass typed arguments to `ui(id, args)`, which calls `currentResources.getString(id, args)`. The selected resource configuration determines number formatting, including when process defaults differ or a missing translation falls back to English. No parser, numerical range/admission calculation, memory estimate or editable-field serialization changes.

The pt-BR test now expects `2.000.000 (2,00 MP)`. The existing complete English/French sizing-dialog test uses locale grouping symbols without normalizing whitespace. Six new JVM methods cover pt-BR/German/English/Arabic, French grouping, Romanian fallback, differing process defaults, resource refresh, memory unit boundaries and zero clamp, percent parsing, unit round-trips, invalid dimensions and exact maximum-Int-squared Long counts.

## Verification and limits

The test summary distinguishes full host tests, supplementary direct Kotlin/API35 compilation, and isolated JVM execution. The isolated runner compiles exact production helper bodies and source XML templates with a documented resource-formatting stand-in; it is not Android/Robolectric execution. Both ROOT-formatting mutations and a process-default-locale mutation must fail. The added/updated Android tests require the new exact-head hosted run. Run 39045262426 covers the original head only.

The earlier evidence remains historical. Its description of ROOT formatting as expected is superseded by this repair; no wider linguistic receipt is withdrawn or expanded.

## Remaining display-only follow-up

`remaining-root-display-consumers.json` pins six untouched source locations and demonstrates their ROOT versus selected-locale results using exact source templates and Java Formatter. They include resize and new-image MP budgets, oversize warnings, selection rotation, recent-colour index digits and low-zoom percentages. This PR does not claim all numeric UI is localized.

Editable numeric serialization, colour hex syntax, sort/identifier normalization and codec syntax are intentionally distinguished from display defects. Follow-up changes need their own consumer tests.

Platform basis: Android Resources formatting and Formatter's locale digit/decimal/grouping rules:
- https://android.googlesource.com/platform/frameworks/base/+/android-7.0.0_r33/core/java/android/content/res/Resources.java
- https://developer.android.com/reference/java/util/Formatter
- https://cldr.unicode.org/downloads/cldr-34
