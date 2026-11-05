# Zhuang: round and square tip and cursor shapes

Date: 2026-11-05 (UTC). Base: `4cadf47ccd45e392e30829ac300ee535ad185b4b`, tree `2805091a5e025870813b87066f556d581db53c53`.

## Change and independent review

Added missing P2 `ui_round` and `ui_square` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 236 previous typed resources remain unchanged. Canonical XML owns current wording.

Independent review retained both concise shape labels. Semantic fit and spelling evidence are strong; the square term specifically denotes a square rather than a generic four-sided shape. Neither label names the separate Rectangle or Rounded Rectangle tools. These are shared tip/marker-shape choices, so no brush-only qualifier was added. This is source-backed linguistic review, not native-speaker usability testing or certification; native-speaker approval is not a publication gate.

Sources checked directly:

- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `luenz`, circular/round shape (L.htm 38/49), with `nduen` and `mwnz` listed as dialect alternatives; `seiqcingq`, square, versus broader `seiqfueng`, four-sided/four directions (S.htm 23/52). The OCR's incomplete proofreading remains a source limitation, particularly for the square term, which was not independently checked against a printed dictionary page.
- [Guangxi Minzu Bao, 13 July 2022, page 5](https://www.guangximinzubao.cn/szbzw/page/21/2022-07/13/05/2022071305_pdf.pdf), “Doxbeij Gij Singdiuh Vahcuengh Lungzging Caeuq Vahcuengh Biucinj / 金秀龙庆壮语方言与壮语标准音声调比较研究”: the conclusion explicitly gives `luenz` with the meaning “round” while comparing dialect and standard pronunciation. This independently supports spelling and meaning, not a published software-interface standard.

## Actual consumer boundaries

`ClassicPaintActivity.showToolOptions` presents Round then Square for Brush, Watercolor, Eraser and Line. Brush additionally offers the unchanged Calligraphy option. `addChoice` displays the complete selected label on its button and passes the complete label list to its single-choice dialog; selecting an item updates the brush-tip index and button text.

`PaintDocument.paint` maps brush-tip index 1 to square stroke caps and the ordinary round option to round caps. The pencil's separate forced-square behavior and calligraphy drawing path are unchanged. A square tip does not imply that every resulting stroke is a square-shaped drawing.

`populateCursorOptions` also uses the labels in a Round/Square spinner. Its selection updates `cursorShape`, independently of `document.brushTip`. Both cursor rendering routes pass that shape as an outline override. `PaintroidCursorOverlay` copies the incoming paint before applying the override and draws a circle or an equal-width/equal-height square; it does not change the ink's paint cap. Cursor-shape persistence and restored index bounds remain unchanged.

Each resource has three live references in `ClassicPaintActivity`, for six total. The separate cursor-shape heading, tool-option title and Calligraphy label remain unchanged and can use English fallback. This does not complete either settings surface's localization.

## Verification

- Fresh remote head and complete tree matched the preceding publication. All **1,264 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** remain retained, for 1,533 base leaves.
- Existing nodes, attributes and prefix bytes are preserved; two missing scalars are appended. XML/Android escaping, source attributes, ordered typed arguments, numerals, newlines and required literals pass. New XML Git blob: `ed012313f7bb4a64bc7e8bcf35ff14501ba4b0e4`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 8.524 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Four host Java literal-label cases passed**, covering both entries in English and Zhuang.
- Targeted token-aware source checks passed for all six bindings, full selected/list labels, Round/Square index order, brush-tip versus cursor-marker state, paint-copy isolation, square geometry, both cursor-render paths and shape persistence. These inspect source, not executed Kotlin/Android behavior.
- Existing `CursorDrawingTest` coverage for round/square outlines, marker/ink independence, persistence and magnifier rendering was inspected, not executed in this batch.

Zhuang now has **238 typed resources**: P0 **69/94**, P1 **132/249**, P2 **37/305**, P3 **0/71**. Global missing entries across 171 options: P0 162, P1 1,359, P2 30,092, P3 7,481; 46 options have complete presence. Presence is not fluency or runtime acceptance. Scope remains 59 scoped catalogues and 112 outside-scope explicit-English-fallback catalogues.

## Limits

Android build/AAPT, executed tool selection, ink/marker rendering and persistence, device layout and accessibility were not tested. No Android SDK or Kotlin compiler is configured in this executor. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and wording mirrors are not published.
