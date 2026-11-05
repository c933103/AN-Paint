# Zhuang: heart and star drawing tools

Date: 2026-11-05 (UTC). Base: `34f2122ab18aae60dc3dcc1e342420b101b238d0`, tree `7055682ffb9f588a57be459dba10c5379ae67a4b`.

## Change and linguistic review

Added missing P2 `ui_heart` and `ui_star` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 238 previous typed resources remain unchanged. Canonical XML owns current wording.

Independent review accepted both concise tool names. Heart has medium-high confidence: the noun and published stylized-heart usage support the label, although the exact bare software label is not independently attested. Star has high lexical confidence because the dictionary explicitly identifies the star-shaped-mark sense, rather than only an astronomical body. This is source-backed review, not native-user usability certification; native approval is not a publication gate.

Sources checked directly:

- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `sim`, heart (S.htm 32/52); `sing`, star-shaped mark (S.htm 35/52). The astronomical-star entry `ndaundeiq` (N.htm 20/72) is less specific to this consumer. OCR/transcription uncertainty remains, especially for the star entry, which was not checked against a printed dictionary page.
- [Guangxi Minzu Bao, 27 September 2023, page 5](https://www.guangximinzubao.cn/szbzw/page/21/2023-09/27/05/2023092705_pdf.pdf), “Bet Nyied Cibngux Ngonz Ronghndwen”: the mooncake-shape list uses `yiengh aen sim` alongside square and round shapes. The following list separately describes fillings, another sense of `sim`. This supports a stylized-heart shape reading, not an anatomical-only reading or an established interface terminology standard.

## Actual consumers

`PaintTool.HEART` and `PaintTool.STAR` each resolve the corresponding resource through `ui(labelId)`. `ToolButton` uses the complete label as button text, accessibility description and tooltip. `ClassicPaintActivity` also places it in the tool-options heading, help title and main status template. The associated Breeze icons and Insert-category routing are unchanged.

`PaintCanvas.shapePath` routes the tools to `ShapePaths.heart` and `ShapePaths.star`. The former constructs a closed, two-lobed heart with a pointed bottom; the latter uses ten alternating outer/inner vertices for a five-point star. These are drawing tools, not favorites, ratings or astronomy controls. Drag bounds can stretch the shapes; the Star name does not promise a regular, unstretched pentagram.

Both tools retain the existing outline, foreground-fill and background-fill-plus-outline behavior. Preview and committed geometry share the shape path, and committing checkpoints the document before drawing. The separate instructional hints and style-choice labels remain unchanged and can fall back to English. This is not complete tool-help localization.

## Verification

- Fresh remote head and complete tree matched the preceding publication. **1,265 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** remain retained, for 1,534 base leaves.
- Existing nodes, attributes and prefix bytes are preserved; two missing scalars are appended. XML/Android escaping, source attributes, typed/ordered arguments, numerals, newlines and required literals pass. New XML Git blob: `59846a5bc8d280856b6c43ced59199990cf921b0`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 10.177 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Four Java literal-label cases** and **four actual status-template composition cases** passed, covering English/Zhuang labels and retention of dimensions, percent-bearing and non-Latin dynamic text. This is host formatting, not Android execution.
- Targeted token-aware checks passed for both direct enum bindings and the indirect label/display routes, corresponding geometry and icons, shape styles and checkpointed commit. These are source checks, not drawing tests.
- `UnifiedEditorTest.addedShapesDrawFilledGeometryAndUndoInOneStep` was inspected, not executed in this batch.

Zhuang now has **240 typed resources**: P0 **69/94**, P1 **132/249**, P2 **39/305**, P3 **0/71**. Global missing entries across 171 options: P0 162, P1 1,359, P2 30,090, P3 7,481; 46 options have complete presence. Presence is not fluency or runtime acceptance. Scope remains 59 scoped catalogues and 112 outside-scope explicit-English-fallback catalogues.

## Limits

Android build/AAPT, executed tool selection/drawing/undo, device layout, glyph rendering and accessibility were not tested. No Android SDK or Kotlin compiler is configured in this executor. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and wording mirrors are not published.
