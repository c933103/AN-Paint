# Zhuang: size presets and restoration

Date: 2026-11-05 (UTC). Base: `1affa02db979482ffb7b9096cac3ca5b5806aff1`, tree `3984c0975f61ff6551bd773f6ab1d4a10dacff4e`.

## Change and independent review

Added three missing P2 resources to canonical `Paintroid/src/main/res/values-b+za/strings.xml`: `ui_smallest`, `ui_largest`, `ui_restore_original_sizes`. All 207 previous typed resources are unchanged. Canonical XML owns the exact wording.

Independent review accepted the superlative presets with high confidence in spelling and word order. The restoration label is a grounded composition meaning “Use original sizes again”, with moderate confidence in full UI idiomaticity. Like its English source, “original” remains context-dependent: the operation restores unscaled **cropped** dimensions, not full-file dimensions. No unsupported crop-removal promise was added. Native-human approval is not a gate or a claimed certification.

Sources directly checked:
- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `ceiq`, superlative before an adjective (C.htm 32/78); `iq`, small (I.htm 1/5); `hung`, large (H.htm 42/45); `caiq`, again (C.htm 17/78); `cikconq`, dimensions (C.htm 50/78); `yienzlaiz`, original/former (Y.htm 17/31); `yungh`, use (Y.htm 29/31). The OCR warns of incomplete proofreading.
- [Guangxi Minzu Bao, 10 September 2025, Riep Baengzndaij](https://www.guangximinzubao.cn/szbzw/html/2025-09/10/content_54490.htm), paragraphs beginning `Caj daengz donq daihngeih` and `Mizseiz nanz`: `ceiq iq` describes the youngest siblings. This attests the construction, not dimensional usage specifically.
- [Guangxi Minzu Bao, 6 July 2016, Mbanjsingzgeq](https://www.guangximinzubao.cn/szbzw/html/2016-07/06/content_18147.htm), paragraph beginning `Mbanjsingzgeq dwg`: `ceiq hung` describes a largest village, with area and population immediately following. Existing product wording supplies consistency only, not independent linguistic proof.

## Actual consumer boundaries

`NormalizeImagesDialog` takes min/max of all assembly images' current placed width or height, according to the selected axis. The presets are not based on area, source-file size or the original uncropped dimensions. Each button retains its identity independently of its translated label. Clicking a preset changes the input and refreshes validation; applying is a separate action. In percent mode, the preset is displayed relative to the largest current chosen dimension, rounded to four decimal places by the existing formatter.

The restoration button instead calls `assembly.resetSizes()` immediately and dismisses on success. `ImageAssembly.resetSizes` clears normalization for all entries, keeps their crops, and reflows their placement. With normalization absent, `placedSize` returns `croppedSize`. The ordinary validated change/persistence/undo path remains in use; exceptions are shown in the dialog. This is not a crop reset or a guarantee that placements stay unchanged.

## Verification

- Fresh remote head/tree reconciled with the preceding verified publication. All **1,253 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** remain retained, for 1,522 base leaves.
- The original 207 resource nodes, attributes and prefix bytes are preserved; three missing scalars are appended. XML/Android escaping, source attributes, ordered typed arguments, numerals, newlines and literal-token checks pass. New XML Git blob: `cdd5eacf3383a43752d512b7a21105da959be726`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 9.821 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Six host Java literal-label cases passed**, covering all three keys in English and Zhuang.
- Targeted token-aware source checks passed for all resource bindings, current-axis min/max inputs, label-independent button identity, preset versus apply behavior, percent conversion, immediate reset, retained crops and the ordinary validated change path. Existing JVM tests for preset identity/cancel/apply and cropped-size reset were inspected, but were **not executed** in this batch.

Zhuang now has **210 typed resources**: P0 **69/94**, P1 **129/249**, P2 **12/305**, P3 **0/71**. Global missing-entry counts across 171 options: P0 162, P1 1,362, P2 30,117, P3 7,481; 46 options have complete presence. These are presence counts, not linguistic acceptance or runtime coverage. Scope remains 59 scoped catalogues plus 112 outside-scope explicit-English-fallback catalogues.

## Limits

No Android build/AAPT, executed button/normalization/persistence path, device layout, accessibility or font checks were run. Consumer findings are static source checks. The complete reset phrase is not independently attested as established software terminology. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and sentence mirrors are not published.
