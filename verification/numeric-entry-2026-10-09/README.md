# Selected-locale numeric entry propagation

Base: `develop` at `f68807257ec61c71ac119425d26c109124a18792`, 9 October 2026.

## Reproduced inconsistency

The existing numeric slider and advanced colour editor installed explicit localized digit filters, but dimensions, crop margins, normalization, text styling and import page selection only selected a numeric input type. On Android API21–25 that selects the framework's ASCII-only numeric filter. Before `uiNumber` or the integer parser can validate the value, French `12,5` becomes `125`, while Arabic `١٢٫٥` and Persian `۱۲٫۵` become empty. Parsing support alone does not repair an input filter.

`FrameworkFilterProbe.java` executes unchanged `DigitsKeyListener`, `NumberKeyListener` and `SpannedString` classes from the pinned API21 and API25 Android framework artifacts directly on this host. Single-character insertions avoid Android VM-only array operations; no shim is installed. The committed TSV files and summaries preserve the complete 140-picker-tag matrix. With this host JDK's locale symbols, 11 integer examples and 73 decimal examples lose input under each original framework filter; all 140 examples retain the candidate syntax and parse correctly with the explicit character set. The two matrices agree. These counts describe this host-symbol cohort, not all Android locale databases or languages' linguistic conventions.

The probe's candidate character construction mirrors the helper, but it does **not** instantiate the app's `EditText` or execute Kotlin production code. Real app bindings, input modes, editable insertion and validation are covered by the separately committed Robolectric tests; their results must be checked in current-head CI. This is not emulator, physical-device, keyboard/IME or accessibility-service validation.

## Bounded shared correction

`LocaleNumberInput.configure` uses the field's configured app locale, ASCII digits, locale decimal digits, ASCII decimal dot, the locale decimal separator and ASCII/locale sign characters. It installs a single shared filter in all seven current numeric-entry routes in the classic application. The existing hexadecimal colour editor remains a text field.

Both integer and decimal fields retain pasted fractions and signs until their existing validators can reject them, rather than deleting punctuation and turning the entry into a different valid integer. The numeric key listener itself distinguishes integer from decimal IME entry; it does not request a signed keyboard. `TextView.setKeyListener` therefore sees the final mode before restarting an active input connection. No parser, valid range, rounding rule, translation, label or resource changes.

| Route | Keyboard mode | Existing validation preserved |
| --- | --- | --- |
| Numeric slider | Integer | Integer parser and caller minimum/maximum |
| Colour numeric components | Decimal | `uiNumber` and component range; hexadecimal remains text |
| Dimensions | Integer pixels / decimal percent | Positive whole pixels, percent rounding, maximum dimension and aspect lock |
| Crop margins | Decimal | Whole nonnegative pixel margins / fractional percentages, crop bounds |
| Normalize size | Integer pixels / decimal percent | Positive whole pixels / fractional percent, output dimension bounds |
| Text size / spacing | Decimal | Size 1–1024, spacing 50–300 |
| Import page | Integer | Integer parser and 1–page-count bounds |

The same path applies to all 140 offered tags, including horizontal, RTL, bundled-font and five vertical profiles. ASCII-symbol profiles retain their entry characters. Locale-specific digit/decimal profiles gain the missing filter propagation. This is numeric-entry applicability, not catalogue completeness or translation acceptance. Unrelated technical serialization, drawing text and filenames are untouched.

## Regression and verification record

- Local full Python host suite: **309 passed**, no failures/errors/skips, 49.169 seconds. This includes two new source guards requiring the seven caller routes and distinct IME modes. Source guards do not prove runtime behavior. This is the rerun after the focused-IME review repair.
- Local whitespace check: passed.
- Controlled direct framework probes: API21 and API25 each completed all 140 tags; original-loss and candidate-preservation results are in the adjacent TSV/summary files.
- New `LocaleNumberInputTest` exercises actual editable insertion, not `setText` alone: all 140 offered tags with integer/decimal IME modes on API21/25/30/35; original/fixed framework comparison on API21/25; actual dimensions, crop, normalization, text-style, slider, colour and page controls on API21/25/35. It covers fractions, signs, ranges, repeated unit switching, cancel/reopen, control descriptions and existing input-filter preservation. A custom InputMethodManager shadow records the input type at each real TextView restart call and EditorInfo reports the final mode; this is not a real-IME test.
- The page test opens the actual private page form without staging/decoding a document. It validates input and button enablement, not the import decoder or preview route.
- Android compilation, all unit tests, lint, APK builds and the existing API35 installed suite are **pending current-head CI at publication**. The local host has Java21 but no configured Android SDK/NDK, so no local Android build is claimed.
- No production vertical-notice change and no duplicate of draft PR19. Broader AN-W04 remains open.

## Reproduction dependencies

These are public Maven Central Android framework bytecode artifacts; binaries are not vendored here.

- API21: `org.robolectric:android-all:5.0.2_r3-robolectric-r0`, SHA-256 `5e63d4c7f2c691afed648bf0675e0b0a76d19f0e23d93705f4faf9ed3b2734de`.
- API25: `org.robolectric:android-all:7.1.0_r7-robolectric-r1`, SHA-256 `6eb4a8049ff343cace89469441215ee14a1ee90295059729ece51821c078248d`.
- Host: OpenJDK 21.0.12.1, Debian x86_64. Java locale data is host-supplied.

From the repository root, substitute the verified local jar path:

```sh
java -cp /path/to/android-all.jar verification/numeric-entry-2026-10-09/FrameworkFilterProbe.java Paintroid/src/main/res/values/app_language_tags.xml
```

The command writes the TSV to stdout and its bounded summary to stderr. Failure in any candidate retention/parse check exits unsuccessfully. It uses the unchanged real framework filter for both the old numeric constructor and the explicit-character NumberKeyListener; it does not test live input-method delivery.

## First-head Codex finding: focused IME restart ordering

[Review of a9b7577](https://github.com/c933103/AN-Paint/pull/27#discussion_r4227029924) found that assigning the string-based listener restarts an active IME before a subsequent `setRawInputType` call. The later property value alone is insufficient. API21 bytecode inspection confirms `TextView.setKeyListener` obtains the listener's input type, then calls `InputMethodManager.restartInput`; the explicit-string DigitsKeyListener on API21 advertises integer mode, not decimal mode. The initial report's blanket “text keyboard” description was too broad; the relevant defect is a restart with the wrong mode.

The correction uses a NumberKeyListener that advertises the final numeric mode immediately. The new restart-boundary regression reproduces the first-head misordering before checking repeated corrected transitions and EditorInfo. Framework-filter output is unchanged by this listener-type correction. Fresh review and current-head Android CI are required; no actual keyboard result is inferred from the shadow.
