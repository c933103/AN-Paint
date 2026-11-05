# Zhuang clockwise quarter-turn command, 5 November 2026

## Scope and wording

The live branch was reconciled at parent `5f5516a539144fedb582504312be8a5bfc60cbdc`, tree `ed5df4d65f46f64fe6eee63f1360817bb8a96755`; no operation was pending. This fills missing P1 `ui_rotate_90_clockwise`. All 272 preceding typed resources remain unchanged; the total is 273. Only canonical XML and this report change.

Independent wording/context review recommended the plain-language rendering “Rotate 90° to the right.” For this two-dimensional image command, a right quarter-turn expresses the clockwise operation. The rotation verb and explicit angle distinguish it from translating the image right or horizontally reflecting it. The existing half-turn label remains unchanged.

[The Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) independently supports `baenq` turn/rotate (B9), directional `coh` toward, after a verb/before a noun (C60), and `baihgvaz` right side (B15). These component senses support the paraphrase. The OCR source does not attest the complete UI command or determine where an angular measure belongs relative to the directional phrase. Bounded source checks found no reliable full-phrase attestation; moving the angle after the direction would not be an evidence-backed correction.

Confidence is **high on intended command meaning and moderate on idiomatic wording/order**. The right-turn interpretation is contextual UI phrasing, not a claimed official Zhuang term for clockwise. No native-human certification or complete-language acceptance is claimed. Canonical XML owns the wording.

## Actual consumer

`ClassicPaintActivity` has the sole direct binding in its Edit panel. The command applies pending work, calls `document.transform` with `Matrix.setRotate(90f)`, then fits the resulting image in the view. In the image's screen coordinates, where y increases downward, positive 90° turns the top toward the right: visually clockwise. The separate horizontal flip uses a negative x scale, not this rotation.

`PaintDocument.transform` checks memory, finishes the selection, transforms the entire bitmap, replaces it as an undoable edit and performs the existing temporary-bitmap cleanup. A floating selection is committed before the whole-image operation. No transformation, selection, memory, viewport or history implementation changes.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 10.075 seconds**.
- Two host Java XML-to-string cases check one exact `90°` literal and unchanged no-argument formatting. This is not Android resource compilation.
- Temporary token-aware Kotlin checks verify the positive-90-degree binding, following viewport fit, distinct half-turn/flip commands, pending-work/selection sequencing, whole-bitmap transformation, undo checkpoint and cleanup. They do not execute Android rotation rendering.
- Base snapshot verification matched Git blobs and executable modes for **1,287 materialized files**, retaining **269** unmaterialized entries. Publication checks the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

The inspected `ClassicWorkspaceTest.paletteForegroundBackgroundAndImageTransformMenusWork` covers a horizontal-flip pixel relocation and undo through the shared transformation path, not this quarter-turn. It was not run. No quarter-turn pixel test is claimed, and no permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **150/249**, P2 **54/305**, P3 **0/71**. Across 171 options, missing resources are P0 **162**, P1 **1,341**, P2 **30,075**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, rotated pixel placement, undo, TalkBack and label layout were not executed. Exact-head Actions state is checked after publication and reported separately; this review branch does not normally trigger CI. No merge, release or CI-pass claim is made.
