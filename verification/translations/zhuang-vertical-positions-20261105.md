# Zhuang: top crop edge and vertical text alignment

Date: 2026-11-05 (UTC). Base: `4eb3a61759926f29abb6e57bbb1c2f422d6983d9`, tree `05f132d475c66b82e2efa5f504fc57874118f56b`.

## Change and independent review

Added P2 `ui_top`, `ui_top23` and `ui_bottom23` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 219 previous typed resources are unchanged. Canonical XML owns the wording.

Independent review accepted upper-side/lower-side positional terms for the actual controls. The top crop label names an edge; the top/bottom alignment entries are concise choices inside an alignment spinner, parallel to the existing left/centre/right choices. They do not instruct moving text to the canvas edges. Lexical confidence is strong; exact typography-register and word-spacing confidence is narrower. Native-human approval is not a gate or a claimed certification.

The directly checked [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), B.htm 15/80, lists `baihgwnz` for upper side/above and `baihlaj` for lower side/below, alongside the separate `baih` side term. Their additional hierarchical senses do not displace the spatial readings in these controls. The source warns of incomplete OCR proofreading. The new labels follow the catalogue's separated spelling, consistent with retained left/right/bottom labels and horizontal alignment options. This spacing is a project editorial choice, not the dictionary's fused spelling or a claim of established typography terminology.

## Actual consumer boundaries

`ImageCropDialog` maps the top resource to the second field in left/top/right/bottom order. It supplies the entire visible edge label and is inserted into the separate pixel/percent trim accessibility templates. The numeric value remains the amount removed from the original top edge, not retained height or the position of the whole image. `CropMargins.rect` converts the top amount against image height; field ordering and calculations do not depend on translated text.

`TextStyleDialog` changes its alignment choices from left/centre/right in horizontal mode to top/centre/bottom in either vertical direction, preserving the selected index. Preview and committed settings map indices to `Paint.Align.LEFT/CENTER/RIGHT`. The shared renderer uses top/centre/bottom offsets within the text bounds, while `PaintDocument.text` shifts the block relative to the insertion point. These are not alignments to the whole canvas. The shared centre option remains axis-neutral.

The separate alignment heading and trim-unit accessibility templates remain unchanged and may still use English fallback. This batch does not claim complete text/crop-dialog localization. No model, layout or rendering code changes are included.

## Verification

- Fresh remote head/tree reconciled with the preceding verified publication. All **1,258 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** remain retained, for 1,527 base leaves.
- All 219 original nodes, attributes and prefix bytes are preserved; three missing scalars are appended. XML/Android escaping, source attributes, ordered typed arguments, numerals, newlines and required literal tokens pass. New XML Git blob: `4a75a0f4e9435a78df010b98097e5e74e3b5082f`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 10.826 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Six host Java literal-label cases passed**, covering the three entries in English and Zhuang.
- Targeted token-aware source checks passed for all three added-key bindings, full crop edge labels and accessibility arguments, numeric margin order and height conversion, vertical alignment option order, retained selection on direction change, preview/commit mapping, shared renderer and insertion-anchor behavior. These checks inspect source rather than execute Kotlin or Android flows.

Zhuang now has **222 typed resources**: P0 **69/94**, P1 **132/249**, P2 **21/305**, P3 **0/71**. Global missing-entry counts across 171 options: P0 162, P1 1,359, P2 30,108, P3 7,481; 46 options have complete presence. These are presence counts, not linguistic acceptance or runtime coverage. Scope remains 59 scoped catalogues plus 112 outside-scope explicit-English-fallback catalogues.

## Limits

No Android build/AAPT, executed crop/alignment/direction-change flow, device rendering/layout, accessibility or font checks were run. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and sentence mirrors are not published.
