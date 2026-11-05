# Zhuang: applying edits to image groups

Date: 2026-11-05 (UTC). Base: `4de124e4376b533cbb758e1f87bf9283d0ff7180`, tree `f5e8cfa4b529fe856db4dc73fd30d27df04c9d1c`.

## Change and independent review

Added missing P2 `ui_apply_to_all` and `ui_apply_to_these_images` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`; all 225 earlier typed resources remain unchanged. Canonical XML owns current wording.

Independent review retained both candidates with moderate linguistic confidence. The first is a concise application command whose operation comes from the normalization dialog. The second labels the images to receive the crop, not the preview image or a completed operation. No concrete semantic or grammatical defect was found. Both are compositional UI translations; exact image-editing idiomaticity is not conclusively established. Native-human approval is not a gate or a claimed certification.

Sources checked directly:

- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `yungh` includes use/apply (Y.htm 29/31), `youq` includes at/in (Y.htm 27/31), `sojmiz` means all/everything (S.htm 38/52), and `neix` means this (N.htm 32/72). The appended Sawndip N.htm 8/20 example with `gij` + noun + `neix` demonstrates plural “these.” The source's incomplete OCR proofreading remains a limitation.
- [Guangxi Minzu Bao, Hoenz Fwen / 歌魂, 27 December 2017](https://www.guangximinzubao.cn/szbzw/html/2017-12/27/content_24064.htm) uses `dozsiengq` for depicted images/figures. It supports the image noun outside software, not a complete UI label.
- [Lexmark C925 safety notices](https://publications.lexmark.com/publications/pdfs/2007/c925x/UG/html/sc/laser_ug_notices.html), the Zhuang altitude and climate notices, directly use `yungh youq`. They support a use-in/at construction; applying editing parameters to images is an analogous target use, not a quoted standard software expression.

## Actual consumer boundaries

`NormalizeImagesDialog` displays the full “Apply to all” resource on its positive button. The validated target is committed through `assembly.normalize(axis, target)`, which maps the complete image state, including unplaced images, then reflows the assembly. “All” does not mean only a selected subset or only placed images. The chosen width or height becomes common; the other dimension follows each crop's ratio with integer rounding. This does not promise identical width and height for every image.

`ImageCropDialog` shows the entire “Apply to these images” resource as a heading above checkboxes only when multiple images are supplied. It is not the apply button. The preview reference is separate from the selected-ID set. Initially, items with no attachment are selected, falling back to all if that set is empty; this exact predicate may include absolutely positioned images and is not synonymous with “unplaced.” All/None controls update checkboxes without committing a crop.

The separate Apply crop button rejects an empty selection, computes margins against each selected image's original dimensions, and passes only those IDs to the model. The model preserves nonselected entries. Previewing another image does not itself select it. Names and wording do not control model selection or numeric calculations. Other descriptions, units and errors remain unchanged and may still use English fallback. No implementation changes are included.

## Verification

- Fresh remote head and complete tree matched the preceding publication. All **1,260 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** remain retained, for 1,529 base leaves.
- All existing nodes, attributes and prefix bytes are preserved. Two missing scalars are appended. XML/Android escaping, source attributes, ordered typed arguments, numerals, newlines and required literals pass. New XML Git blob: `7e6962f956020818cd8d88822a2fede5ddf4be25`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 9.654 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Four host Java literal-label cases passed**, covering both entries in English and Zhuang.
- Targeted token-aware source checks passed for both live bindings, full button/heading resources, normalization's complete-state scope, separate crop reference and selected IDs, checkbox controls, empty-selection rejection and selected-only commit. These are source checks, not executed Kotlin/Android flows.
- Existing assembly model/activity cases covering normalization, crop, persistence and undo were inspected, not executed in this batch.

Zhuang now has **227 typed resources**: P0 **69/94**, P1 **132/249**, P2 **26/305**, P3 **0/71**. Global missing entries across 171 options: P0 162, P1 1,359, P2 30,103, P3 7,481; 46 options have complete presence. These are presence counts, not fluency or runtime acceptance. Scope remains 59 scoped catalogues and 112 outside-scope explicit-English-fallback catalogues.

## Limits

Android build/AAPT, executed normalization/crop/selection/lifecycle behavior, device rendering/layout, font and accessibility checks were not run. No Android SDK or Kotlin compiler is configured in this executor. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and wording mirrors are not published.
