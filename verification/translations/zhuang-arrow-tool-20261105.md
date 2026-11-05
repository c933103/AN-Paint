# Zhuang: Arrow drawing tool

Date: 2026-11-05 (UTC). Base: `c335d598bf8873ec5f847a81a2b58cc8e947db5f`, tree `2ccc442096e4a4ecc1f63fdd42e8dff69513c400`.

## Change and independent review

Added missing P2 `ui_arrow` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 245 previous typed resources remain unchanged. Canonical XML owns current wording.

Independent review accepted the concise arrow noun for this drawing tool. Lexical confidence is high; confidence that it is an established graphical/software idiom is narrower. The actual tool draws a complete arrow silhouette, making the object-name extension appropriate in context. This is not an arrowhead-only shape or navigation command. No unsupported compound was introduced.

Sources independently checked:

- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), N.htm 3/72, explicitly gives `naq` as arrow, with `cienq` and `bwn` as dialect alternatives. The appendix separately distinguishes bow and arrow. The earlier unresolved bow/crossbow concern is therefore resolved by the actual entry, not carried forward as a blocker.
- [Published Zhuang translations, 10 July 2024](https://www.guangximinzubao.cn/szbzw/html/2024-07/10/content_50627.htm), use `naq` for arrows that are shot, embedded in straw and counted. This independently supports the physical-arrow sense.

Bounded searches did not establish direct graphical-arrow/interface attestation. The chosen label is a source-supported noun adapted to the actual drawing shape, not a claimed standardized Zhuang software term. Dictionary OCR/transcription uncertainty remains; no printed page or native-speaker certification is claimed.

## Actual consumers

`PaintTool.ARROW` resolves the complete label through `ui(labelId)`. It reaches the tool button's text, accessibility description and tooltip, the activity's options heading and help title, and the status template. The distinct arrow icon and tool routing remain unchanged.

`ShapePaths.arrow` creates a closed seven-vertex polygon with a shaft and triangular head, rotated from the drag's start/tail towards its end/tip. Near-zero lengths are guarded. Existing outline, foreground-fill and background-fill-plus-outline modes remain intact; releasing the drag commits through the checkpointed shape path. No shape geometry, drawing, undo or gesture logic changes. The separate drawing hint and style choices remain unchanged and may fall back to English.

## Verification

- Fresh remote matched the preceding publication. **1,269 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** are retained, for **1,538 base leaves**.
- Existing nodes, attributes and prefix bytes are preserved; one missing scalar is appended. XML/Android escaping, source attributes, typed/ordered arguments, numerals, newlines and required literals pass. XML Git blob: `979e423006bfe9b5b796054fa2d986fefd465a56`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed in 8.073 seconds**: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Two Java literal-label cases and two actual status-template composition cases passed**, covering English/Zhuang labels, retained dimensions, percent-bearing and non-Latin dynamic text. These are host formatting checks, not Android execution.
- Targeted token-aware source checks passed for the direct enum binding and complete display routes, arrow icon, seven-vertex shape, tail/tip orientation, near-zero guard, fill modes and checkpointed commit.
- Existing `UnifiedEditorTest.addedShapesDrawFilledGeometryAndUndoInOneStep` was inspected, not run. It includes the real Arrow tool alongside Heart and Star; its existence is not a current Zhuang runtime pass.

Zhuang now has **246 typed resources**: P0 **69/94**, P1 **133/249**, P2 **44/305**, P3 **0/71**. Global missing entries across 171 options: P0 162, P1 1,358, P2 30,085, P3 7,481; 46 options have complete presence. Presence is not fluency or runtime acceptance. Scope remains 59 scoped catalogues and 112 outside-scope explicit-English-fallback catalogues.

Android build/AAPT, executed selection/drawing/undo, device layout, glyph rendering and accessibility were not tested. No Android SDK or Kotlin compiler is configured in this executor. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary checks and wording mirrors are not published.
