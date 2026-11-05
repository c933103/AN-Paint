# Zhuang: start and stop cursor drawing

Date: 2026-11-05 (UTC). Base: `9626432b6bb18de24ea177b0bfd95bd68fb0e7cb`, tree `3a41546cdd71fc768ce7fc6184c348d157fd9b3b`.

## Change and independent review

Added P2 `ui_cursor_start31` and `ui_cursor_stop31` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 217 previous typed resources remain unchanged. Canonical XML owns the wording.

Independent review accepted both as action labels: begin drawing and cease drawing. Evidence is stronger for the start construction. The stop phrase is a compositional grammatical judgment using the attested stop/cease verb before the drawing activity; bounded searches did not establish an independent corpus example of that exact verb-complement construction. This leaves narrower idiomatic confidence, not a demonstrated semantic defect. Neither label claims completion, cancellation, undo or deletion. Exact sentence attestation and native-human approval are not gates or claimed certifications.

Evidence:
- Directly checked [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `haidaeuz` (H.htm 15/45) refers to beginning/start, with its `codaeuz` entry at C.htm 59/78; `dingzcij` means stop/cease (D.htm 58/110); `veh` means draw (V.htm 12/19). The source warns of incomplete OCR proofreading.
- [People's Daily Zhuang, report on the 2019 plan and 2020 draft plan](https://sawcuengh.people.com.cn/158003/15813459.html) supplies the modern activity construction `haidaeuz guh buek hanghmoeg`, supporting begin before an activity verb. This was checked through search extraction; direct opening returned HTTP 502. It is not an exact drawing-UI quotation.

## Actual consumer boundaries

`ClassicPaintActivity` initially builds the cursor toggle with the start label and binds it to `PaintCanvas.toggleCursorDrawing()`. `updateStatus()` then selects stop when `cursorDrawing` is true and start otherwise. The same complete selected text is assigned to `contentDescription` and the tooltip. The button is disabled while busy and visible only when cursor drawing is available.

Availability requires cursor mode and a supported brush, pencil, watercolor or eraser tool. Generic drawing terminology retains the English source's umbrella meaning, including erasing. Starting enables drawing for subsequent cursor interaction; it does not itself promise an immediate mark. Stopping does not disable cursor mode. The setter finishes the current gesture through `pauseGesture()`, updates the drawing flag and refreshes status. It does not call undo, cancel-gesture or new-image operations. A tap on the cursor can invoke the same toggle. Draft restoration retains cursor mode but resets active drawing to false.

Separate movement/drawing instruction toasts remain separate resources and may still use English fallback. These two labels do not claim complete cursor-interface localization. No control flow or rendering code changes are included.

## Verification

- Fresh remote head/tree reconciled with the preceding verified publication. All **1,257 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** remain retained, for 1,526 base leaves.
- All 217 original nodes, attributes and prefix bytes are preserved; two missing scalars are appended. XML/Android escaping, source attributes, ordered typed arguments, numerals, newlines and required literal tokens pass. New XML Git blob: `d71b60b83705521ecd400df71262c6b69ff11df3`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 9.535 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Four host Java literal-label cases passed**, covering both entries in English and Zhuang.
- Targeted token-aware source checks passed for all three resource bindings, state-selected labels and identical accessibility/tooltip text, availability/busy gates, shared toggle behavior, gesture finishing, cursor-mode preservation and safe inactive drawing after draft restoration. These are static checks, not executed Kotlin or Android behavior.
- Existing `CursorDrawingTest` covers starting/stopping while retaining pixels, and `LocaleTooltipControlsTest` checks start/stop/start resource binding for another locale. These cases were inspected, not run or counted as passes here.

Zhuang now has **219 typed resources**: P0 **69/94**, P1 **132/249**, P2 **18/305**, P3 **0/71**. Global missing-entry counts across 171 options: P0 162, P1 1,359, P2 30,111, P3 7,481; 46 options have complete presence. These are presence counts, not linguistic acceptance or runtime coverage. Scope remains 59 scoped catalogues plus 112 outside-scope explicit-English-fallback catalogues.

## Limits

No Android build/AAPT, executed cursor gesture or restoration flow, device layout, screen-reader, tooltip display or font checks were run. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and sentence mirrors are not published.
