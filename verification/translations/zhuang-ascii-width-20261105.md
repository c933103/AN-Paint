# Zhuang ASCII export width, 5 November 2026

## Scope and language review

The live branch was reconciled at parent `0546b1403b02a160b7bae63a8be69b7ebf616c47`, tree `5d871e229b3df015b1e3b6e178a35d7b1160e51b`. The preceding publication was confirmed and no write was pending or uncertain. This adds missing P2 `formats22_ascii_columns`, preserving all 291 previous typed resources for a total of 292. Only canonical XML and this report change.

Independent review recommends the concise width label with characters as its unit. Confidence is **moderate-high for contextual meaning**. The [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), independently retrieved by the reviewer, supports `gvangq` as wide/broad (G85) and `cih` as a unit of written characters (C39). Although a separate sense of `cih` is word, it is not restricted to lexical words. Existing project width/text labels use the same vocabulary.

The implementation establishes the relevant unit as ASCII character cells per output row, not words or source-image pixels. The dictionary is an OCR mirror rather than a modern computing terminology standard; the complete label is a contextual construction, not a separately attested technical standard. No native-human certification is claimed.

An earlier Unplace candidate was investigated and left unchanged because the proposed phrase could conflate clearing an existing placement with canceling an unfinished action. It is not counted as progress in this batch.

## Actual consumer

`SaveOptionsDialog` binds the resource to the ASCII-only NumericSlider. It clamps the initial value and accepts 40–240 columns. `NumericSlider` presents this name with the current value, uses it in accessibility descriptions, and uses it as the exact-entry dialog title. The selected count is carried through `ExportOptions` and `ImageExporter` into `TextImageCodec.encodeAscii`.

The codec computes rows for the output aspect ratio, scales a working bitmap to the chosen columns, then calls the production Java `TextImageData.ascii` primitive. That primitive writes exactly the requested count of ASCII characters, including any spaces, followed by one newline per row. The width does not include the newline and is not a word count. No validation, encoder, source-image, export-state or UI logic changes.

## Verification

Work and tests used the available temporary filesystem. No unrelated files were removed from the full main workspace.

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- The four localization host suites plus `test_text_image_data.TextImageDataTests.test_ascii_aspect_luminance_inversion_and_size`: **62 tests passed in 16.499 seconds**. The latter compiles and executes the production Java primitive, checking fixed row width/newlines, aspect ratio, out-of-range geometry, minimum row, luminance inversion and transparency compositing. This is actual host execution, not Android Bitmap or UI execution.
- Two Java XML-to-string cases checked the English/Zhuang label for nonempty text and unchanged no-argument formatting. These are not Android resource compilation.
- Temporary token-aware Kotlin checks verified the sole binding, ASCII-only visibility, 40–240 limits, value-to-encoder route, and visible/accessibility/exact-entry label consumers.
- Base snapshot verification matched Git blobs and executable modes for **1,282 materialized files**, retaining **288** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `TextImageCodecTest.asciiUsesChosenWidthAspectAndInversionWithoutChangingSource` tests Bitmap-to-text output and source preservation. `ExportFormatDialogTest.iconAndAsciiOptionsAreSpecificToTheirFormatAndSurviveReopening` tests format visibility and option persistence. These inspections are not runtime evidence. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **158/249**, P2 **63/305**, P3 **2/71**. Across 171 options, missing resources are P0 **162**, P1 **1,333**, P2 **30,066**, P3 **7,479**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, Bitmap scaling, output-provider execution, option restoration, TalkBack and device layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
