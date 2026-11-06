# Zhuang whole-number coordinate validation, 6 November 2026

## Scope and language review

Reconciled parent `6862954fe581f1136ca62a632152ef79b9a0c7b0`, tree `98546d165d5f3362cef1e01d7608a211583a0c7b`, with the previous publication complete and no pending write. Adds missing P2 `ui_assembly_position_nonnegative`, preserving all 306 previous typed resources for a total of 307. Only canonical XML and this report change.

Independent review recommends the proposed X-and-Y subject, obligatory modal, integer predicate and inclusive range. It found no blocking grammatical or semantic issue. The error requires each coordinate to be an integer from 0 through 2147483647. It neither excludes zero, instructs rounding, requires digits-only spelling nor implies both coordinates must share one value. The source's written “zero” is represented by numeral 0; the upper bound and X/Y identities are preserved.

Fresh direct [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) retrieval distinguishes `cingjsoq` integer (C54, L377; also old-loan index L2506) from `cingqsoq` positive number (C55, L379). The reviewer independently retrieved supporting entries for `caeuq` and/with, `yaekaeu` must, `dwg` be, `daj` from and `daengz` to/reach. The range matches the project's existing range constructions. Confidence is **high for the lexical distinctions and consumer fit, moderate for complete idiomatic polish**. The evidence is OCR, not a checked printed-page image or independent attestation of the whole sentence. No native-human certification is claimed or treated as a publication gate.

## Consumers and boundaries

The resource has four direct references: twice in `AssemblyPlacementDialog.kt` for rejected X/Y input, and twice in `ImageAssembly.kt` for nonnegative coordinates. The dialog's `placementPixels` accepts only finite numeric values satisfying `0 <= value <= Int.MAX_VALUE` and equality with their floor, before converting to Int. `uiNumber` accepts a complete parsed numeric value, including its locale-aware parsing fallback. Therefore an integer-valued decimal spelling may qualify; a fractional value is rejected rather than rounded.

On a rejected input, the complete exception message appears in the dialog's polite accessibility live region and the dialog remains open. In the model, the Int type already supplies integrality and the numeric upper limit; the repeated checks enforce nonnegativity.

The input range is necessary, not sufficient for a valid final placement: image width/height must also fit within the coordinate extent. A separate existing overflow guard rejects an image whose right/bottom edge exceeds Int.MAX_VALUE. This translation does not claim that every numeric value in range can accommodate every image. Parsing, validation, model, overflow, persistence and undo logic are unchanged. The dialog title and explanatory help still fall back to English.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, formatting, literal tokens, newline escapes and XML escaping are preserved. The zero-to-0 equivalence and exact upper numeric bound were checked explicitly.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 5.782 seconds**.
- Two Java English/Zhuang XML-to-string cases passed for nonempty messages and unchanged no-argument formatting. This is not Android resource compilation or coordinate-parser execution.
- Temporary token-aware source checks passed for all four bindings, both rejected-input paths, numeric integrality/range checks before conversion, complete error display, model nonnegativity checks and the separate full-image extent guard.
- All **1,579 base tracked blobs and executable modes** were verified before editing. `git diff --check` passed. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Existing `AssemblyActivityTest.invalidPositionAndCancelDoNotChangeImagesOrTheSavedProject` covers negative, fractional, blank, oversized and extent-overflow input, plus cancellation and unchanged project bytes. It was inspected, not executed. Its presence does not establish this Zhuang message's layout or accessibility. No permanent per-edit wording mirror or test package is added.

Zhuang presence: P0 **69/94**, P1 **158/249**, P2 **78/305**, P3 **2/71**. Global missing resources across 171 options: P0 **162**, P1 **1,333**, P2 **30,051**, P3 **7,479**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, actual numeric entry, coordinate application, TalkBack and device/font-scale layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
