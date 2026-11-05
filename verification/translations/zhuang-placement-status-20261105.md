# Zhuang: assembly placement status

Date: 2026-11-05 (UTC). Base: `0b42f4340236c830a4281c3905284bced1f1e0f1`, tree `bde43f3210611136ba33b1d628a42a835b147d3a`.

## Change and independent review

Added missing P2 `ui_placed` and `ui_not_placed` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 234 previous typed resources remain unchanged. Canonical XML owns current wording.

Independent review accepted the pair. The positive label denotes completed placement. The negative uses general negation rather than “not yet/not previously”: an image can be placed and subsequently unplaced, while remaining available in the tray. These are current-state labels, not commands. Lexical and consumer support is adequate, but exact two-word UI-pair idiomaticity is not directly attested. The elliptical negative could receive a non-placement-action reading outside context; its status position and the separate instruction constrain that ambiguity. No native-speaker certification is claimed or required as a gate.

Sources checked directly:

- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `baij`, place/arrange (B.htm 13/80); `gaenq`, already/previously (G.htm 10/110); `mbouj`, general negation, versus `mboujcaengz`, not yet/not previously (M.htm 27/56). The OCR's incomplete proofreading remains a source limitation.
- [Guangxi Minzu Bao, Dangq Boux Dangq Hoiz, 28 August 2024](https://www.guangximinzubao.cn/zw/f_282583/390994.html), second prose translation, uses `gaenq baij` in a completed deployment/arrangement description. This supports the aspect-plus-verb construction, not an image-editor status standard. The dictionary's physical placement sense and the actual image-state consumer provide the more specific contextual fit.

## Actual consumer boundaries

`AssemblyImage.isPlaced` means that either an attachment or an absolute position exists. It is not equivalent to having an attachment alone, and does not mean saved or exported. `unplace` clears placement while retaining the image; `remove` separately removes the item. Undo/redo can restore or remove placement, and state changes refresh the tray.

`AssemblyActivity.renderTray` supplies either complete label as the second argument of the thumbnail's accessibility description, between its filename and dimensions. A separate hold-and-drag instruction follows. The surrounding resource is not translated by this batch and currently falls back to English for Zhuang, so the composed description remains mixed-language.

The positive label also appears beside the thumbnail dimensions. The negative label is not displayed in that visible dimension line: unplaced images omit the status suffix there. The two direct resource references and the additional positive reference inside Kotlin string interpolation were checked separately. The change does not alter placement, drag, removal, undo/redo, sorting or output behavior. The separate Unplace command remains unchanged.

## Verification

- Fresh remote head and complete tree matched the preceding publication. All **1,263 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** remain retained, for 1,532 base leaves.
- Existing nodes, attributes and prefix bytes are preserved; two missing scalars are appended. XML/Android escaping, source attributes, ordered typed arguments, numerals, newlines and required literals pass. New XML Git blob: `68af8103a9973469fe88b56c54310efe458eae41`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 9.038 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Four host Java literal-label cases** and **eight actual-template composition cases** passed. Composition covers both states in English and Zhuang, complete status insertion, dimensions, unchanged surrounding instruction, and filenames containing percent-format-looking text and non-Latin characters. This is host formatting, not Android accessibility execution.
- Targeted source checks passed for all three bindings, current attachment-or-position state, unplacement versus removal, and tray refresh after change/undo/redo. These inspect source, not executed Kotlin behavior.
- Existing `AssemblyModelTest` cases for gap-closing unplacement, absolute placement and undo/redo were inspected, not executed in this batch.

Zhuang now has **236 typed resources**: P0 **69/94**, P1 **132/249**, P2 **35/305**, P3 **0/71**. Global missing entries across 171 options: P0 162, P1 1,359, P2 30,094, P3 7,481; 46 options have complete presence. Presence is not fluency or runtime acceptance. Scope remains 59 scoped catalogues and 112 outside-scope explicit-English-fallback catalogues.

## Limits

Android build/AAPT, executed placement/undo/redo, device rendering, narrow thumbnail layout and accessibility were not tested. No Android SDK or Kotlin compiler is configured in this executor. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and wording mirrors are not published.
