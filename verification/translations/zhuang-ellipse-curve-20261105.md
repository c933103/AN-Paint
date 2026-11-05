# Zhuang: ellipse and curve drawing tools

Date: 2026-11-05 (UTC). Base: `5c5c1909e47bbe7c6ad3cb2e83dbae2847bc0f35`, tree `567f498b2184a61d6bf0e18896188e9c7034e1b1`.

## Change and linguistic review

Added missing P1 `ui_ellipse` and P2 `ui_curve` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 240 previous typed resources remain unchanged. Canonical XML owns current wording.

Independent review accepted both for this bounded tool-name scope. The ellipse label has an explicit oval-shape dictionary sense, separate from the adjacent homonymous body/face descriptions. It is not merely an inferred egg metaphor; however, this does not establish a formal conic-section terminology standard. The Curve label is a compositional “curved line” phrase. Its components and meaning are supported, while exact phrase idiomaticity and interface usage remain less certain. No concrete semantic error or better directly supported short alternative was identified. Native-speaker certification is not claimed or required as a gate.

Source independently checked by both reviews: [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html).

- `bomj`, oval shape (B.htm 52/80), lists `mwnzgaeq` and `luenx` as dialect alternatives. The `luenx` entry refers back to it (L.htm 38/49).
- `goz`, curved (adjective), G.htm 58/110; `gaeuz` is a dialect alternative/cross-reference (G.htm 13/110).
- The geometric line root is supported by `sienqdiuz` (line) and `sienqsoh` (straight line), S.htm 29/52. The isolated `sienq` entry also has a metal-wire sense, so that gloss alone was not treated as sufficient evidence.

Bounded searches did not establish independent published use of these exact interface labels. OCR/transcription uncertainty remains; no printed dictionary page was independently inspected. Component review is not direct phrase attestation.

## Actual consumers and boundaries

`PaintTool.ELLIPSE` and `PaintTool.CURVE` each resolve their label with `ui(labelId)`. Complete labels flow to `ToolButton` text, accessibility description and tooltip, and to the activity's tool-options heading, help title and status template. Their distinct icons and Insert-category routing are unchanged.

Ellipse uses `Path.addOval` within normalized drag bounds. Equal extents can produce a circle; the label does not impose unequal axes. Ellipse supports the existing outline, foreground-fill and background-fill-plus-outline modes.

Curve starts with a line and then uses two control-point gestures to construct a cubic Bézier path. The second control gesture completes it automatically. The existing Finish curve action can commit earlier; cancellation clears the pending stage. Curve remains stroked regardless of the shape-fill setting. The label describes the curved-line drawing tool, not a colour-adjustment graph or closed filled shape. No gesture, state or rendering logic changes.

Separate hints, the Finish curve caption and style choices remain unchanged and can fall back to English. This is not complete tool-help localization.

## Verification

- Fresh remote head and complete tree matched the preceding publication. **1,266 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** remain retained, for 1,535 base leaves.
- Existing nodes, attributes and prefix bytes are preserved; two missing scalars are appended. XML/Android escaping, source attributes, typed/ordered arguments, numerals, newlines and required literals pass. New XML Git blob: `e6a01f1c3254662975884ed3d52752cf2f39b9a5`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 9.831 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Four Java literal-label cases** and **four actual status-template composition cases** passed, covering English/Zhuang labels and retained dimensions, percent-bearing and non-Latin dynamic text. This is host formatting, not Android execution.
- Targeted token-aware checks passed for both direct enum bindings and indirect label/display routes, oval bounds, cubic-path construction, finish/cancel state, corresponding icons, distinct fill behavior and checkpointed commit. These inspect source, not executed drawing behavior.
- Existing `ClassicWorkspaceTest` curve completion/early-finish/undo and shape-geometry cases, plus `WorkspaceRefinementTest` pending-curve preservation during two-finger navigation, were inspected, not executed in this batch.

Zhuang now has **242 typed resources**: P0 **69/94**, P1 **133/249**, P2 **40/305**, P3 **0/71**. Global missing entries across 171 options: P0 162, P1 1,358, P2 30,089, P3 7,481; 46 options have complete presence. Presence is not fluency or runtime acceptance. Scope remains 59 scoped catalogues and 112 outside-scope explicit-English-fallback catalogues.

## Limits

Android build/AAPT, executed tool selection/drawing/undo/cancellation, device layout, glyph rendering and accessibility were not tested. No Android SDK or Kotlin compiler is configured in this executor. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and wording mirrors are not published.
