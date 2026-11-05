# Zhuang: Finish curve command

Date: 2026-11-05 (UTC). Base: `d5c4268cfc80d05a0d5602863acf705ff5d9f5b0`, tree `8f9074db622a0a827bd0c6b41ba17c8ae9cda0e9`.

## Change and wording review

Added missing P2 `ui_finish_curve` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 244 previous typed resources, including the existing Curve tool label, remain unchanged. Canonical XML owns current wording.

Independent review accepted the command as “finish drawing the curve,” with moderate confidence. Drawing-specific `veh` is preferable here to generic doing/making. The completion construction fits committing the current drawing operation; it does not promise another gesture, closing a shape, cancellation, or completion of all work. The exact phrase and drawing collocation were not independently attested, so this remains evidence-backed composition rather than a verified conventional UI term. Native-speaker certification is not claimed or required as a gate.

Sources checked independently:

- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `veh` means drawing (V.htm 12/19), with a line-drawing example at C.htm 36/78. `liux` has completion/after senses and a verb-plus-completion example at L.htm 28/49. The existing curved-line components are supported by `goz` (G.htm 58/110) and geometric `sienqdiuz`/`sienqsoh` (S.htm 29/52).
- [Published translation, 10 July 2024](https://www.guangximinzubao.cn/szbzw/html/2024-07/10/content_50627.htm), uses `guh liux` for completing assigned work. This corroborates the productive completion construction, not the exact new command.

Dictionary OCR/transcription and interface idiomaticity remain limitations; no printed dictionary page or authentic exact drawing collocation was independently established.

## Actual consumer and behavior boundaries

The sole direct binding is the Curve-specific branch of the activity's `apply` button. The complete resource reaches button text and its accessibility description. Busy/autosave gating is unchanged.

`PaintCanvas.applyPending()` commits the current path only when `curveStage > 0`, then resets the stage. The first drag initializes collinear cubic control points, so Finish can commit a straight result before either bend, or a curve after one bend. The second control gesture normally completes automatically. Repeating Finish without a new pending curve does not commit that curve again. The existing checkpointed commit, cancellation reset and status refresh are unchanged. The resource names the action; it does not assert that a committed curve necessarily has nonzero curvature. Separate tool hints remain unchanged and may fall back to English.

## Verification

- Fresh remote matched the preceding publication. **1,268 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** are retained, for **1,537 base leaves**.
- Existing nodes, attributes and prefix bytes are preserved; one missing scalar is appended. XML/Android escaping, source attributes, typed/ordered arguments, numerals, newlines and required literals pass. XML Git blob: `9f0d24017d064e206ede5b8270091b1e34a229a8`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed in 8.510 seconds**: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Two host Java literal-label cases** passed, one per English/Zhuang catalogue.
- Targeted token-aware source checks passed for the complete label/display binding, Curve action routing, busy/autosave gating, positive-stage commit/reset, initial control points, automatic completion, checkpointing and distinct cancellation.
- `ClassicWorkspaceTest.lineAndTwoBendCurveCommitAsSeparateUndoSteps` and `finishCurveCommitsBeforeBothBendsWithoutDuplicatingTheUndoStep` were inspected, not executed. The latter covers the real button after zero/one bends, repeated Finish, undo and redo; its existence is not a current runtime pass.

Zhuang now has **245 typed resources**: P0 **69/94**, P1 **133/249**, P2 **43/305**, P3 **0/71**. Global missing entries across 171 options: P0 162, P1 1,358, P2 30,086, P3 7,481; 46 options have complete presence. Presence is not fluency or runtime acceptance. Scope remains 59 scoped catalogues and 112 outside-scope explicit-English-fallback catalogues.

Android build/AAPT, executed gestures/early finish/repeated clicks/undo, device layout, glyph rendering and accessibility were not tested. No Android SDK or Kotlin compiler is configured in this executor. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary checks and wording mirrors are not published.
