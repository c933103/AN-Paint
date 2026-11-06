# Zhuang exact-position control, 6 November 2026

Parent `8a2bdadc13119bcc2efc2f314b80d5a163e93dc0`, tree `1ac2b3da8896f3c5a900b9c9b7b870b76cdb0fde`, was reconciled with no pending write. Adds missing P2 `ui_assembly_exact_position`; all 307 previous typed resources are unchanged, for 308 total. Only canonical XML and this report change.

## Wording and consumer

Independent review recommends the compact noun-plus-adjective translation. Fresh direct [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) checks support `vih` position/seat (V14, L1667; also L2464) and `cinj` accurate (C52, L373). Confidence is **moderate**: these lexical senses support the composition, but the full UI phrase is not independently attested or native-speaker certified. OCR may contain errors. A longer proposed functional phrase was not used because its postverbal “according to” construction was less well supported.

`AssemblyActivity` uses the full resource for the button that opens `AssemblyPositionDialog`; `AssemblyPlacementDialog.kt` uses it as that dialog's title. A selected-image guard precedes opening. Placement happens only after Apply parses the X/Y fields and calls `assembly.position`. This is absolute whole-image-pixel placement of the selected image's top-left corner, not snapping, relative movement, resizing or file saving. Cancel does not apply a position.

The X/Y labels and integer-range error are already localized. The longer explanatory help remains English fallback. The button uses 12sp text, wrap-content width and a fixed 46dp height inside a horizontal scroller. The concise wording does not establish successful font-scale, TalkBack or device-layout behavior; those were not measured. No application logic changes.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, formatting, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 6.834 seconds**.
- Two English/Zhuang Java XML-to-string cases passed for nonempty text and unchanged no-argument formatting. This is not Android resource compilation.
- Temporary token-aware source checks passed for both unique resource bindings, complete button/title text, selected-image guard, X/Y Apply path, Cancel and the horizontal button-row structure.
- All **1,580 base tracked blobs and executable modes** were verified before editing; `git diff --check` passed. Publication checks the full path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Existing `AssemblyActivityTest.exactPositionMovesOnlySelectedImageAllowsOverlapAndSurvivesReopening` and `invalidPositionAndCancelDoNotChangeImagesOrTheSavedProject` were inspected for adjacent dialog/model behavior, not executed. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **158/249**, P2 **79/305**, P3 **2/71**. Global missing counts across 171 options are **162 / 1,333 / 30,050 / 7,479** for P0–P3; 46 options have complete presence. Scope remains 59 scoped catalogues plus 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable. Android compilation, Robolectric, actual dialog/positioning, TalkBack and device/font-scale layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
