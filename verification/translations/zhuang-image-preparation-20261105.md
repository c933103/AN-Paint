# Zhuang: image preparation and opening-completion errors

Date: 2026-11-05 (UTC). Base: `1d373cb96cd00dfb6a6a53d347c9fc5b3b9f63a4`, tree `59a5fb879eb05343688d37cf2375d885416ca15c`.

## Change and review

Added two missing P1 resources in `Paintroid/src/main/res/values-b+za/strings.xml`: `ui_could_not_prepare_the_image` and `ui_not_enough_memory_to_finish_opening_this_image`. The first describes unsuccessful image preparation. The second preserves insufficient working memory and inability to **finish opening this image**, rather than claiming decoding failure or offering only a bare memory warning. The canonical XML owns the exact wording; the previous 198 typed resources are unchanged.

Independent linguistic and source-context review retained the preparation composition and recommended the negative-completion construction with `liux`. A provisional `sat` construction was not used because its negative form was less well supported. Confidence is moderate in the component meanings and negative-completion structure, lower in the idiomatic software combination of opening an image with that structure. These are grounded compositions, not independently attested complete software phrases or native-fluency certification. Native-human approval is not a gate.

Sources directly checked:
- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `cinjbi`, prepare, C.htm 52/78. The negative completion evidence for `liux` is in the **Sawndip appendix**, L.htm 8/13, with a telling/finishing example; it is not a claim about an independently verified modern software entry. The OCR warns of incomplete proofreading.
- [Guangxi Minzu Bao, 15 September 2017](https://www.guangximinzubao.cn/szb/html/2017-09/15/content_23126.htm): reported speech independently attests `cinjbi` in a preparation context.
- [Guangxi Minzu Bao, 18 August 2026](https://www.guangximinzubao.cn/zw/f_282583/645681.html): Cungh Swmingz's verse translation provides modern topic–verb–negative-completion usage. This is poetry, not technical prose; no verse is reproduced here. Applying the construction to opening one specific image remains an explicitly identified analogy.

## Actual consumers

- `PaintDocument.copyToCanvasFormat` throws the preparation message as an `OutOfMemoryError` when an already canonical image's mutable ARGB_8888 `Bitmap.copy` returns null. The helper is called by `replace` and `paste`. It also has a separate noncanonical bitmap-conversion path, but that path does not explicitly emit this message. The message does not describe file access or decoding.
- `ClassicPaintActivity.decodeImage` decodes on a worker before entering the UI callback. Inside that callback, image paste/replacement and subsequent UI work are protected by the catch that emits the finish-opening message. Worker-phase `ImageSizeException` and OOM instead offer resizing. The notice therefore preserves the later-stage completion distinction; it does not diagnose which UI-phase allocation failed or promise that no document state changed.
- Each key has exactly one actual `R.string` binding in its respective file. `ioFailed` appends a period and the exception message (or its fallback), then sends the whole composed text to the dialog. The finish-opening resource intentionally has no final period, matching its English prefix role and avoiding a duplicated separator. Its internal sentence boundary remains intact.

## Verification

- Fresh base reconciliation: all **1,252 materialized files** match base Git blob hashes and executable modes. **266 unmaterialized leaves** remain retained, for 1,518 base non-tree entries.
- All 198 previous typed resources, attributes and original prefix bytes preserved; two missing scalar strings added. XML, Android escaping, source attributes, ordered typed placeholders, newlines, numerals and required literal-token checks pass. New XML blob: `f2574737442b0f21964b0117f980c48d9f8164c0`, 18,344 bytes.
- All **171 offered catalogues** and the priority manifest pass structural validation.
- **61 host tests passed** in 10.902 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Four host Java resource-format/render cases passed**, one per new resource in English and Zhuang; both are zero-argument strings. The prefix punctuation check also passed.
- Targeted token-aware static checks passed for bitmap-copy failure, replace/paste call sites, successful decode preceding UI-phase error handling, distinct worker resize recovery, exact resource bindings, and complete prefix/detail delivery. An initial temporary harness selector was ambiguous because the method has multiple UI callbacks; scoping it to the callback immediately after source-file cleanup fixed the harness. No application-code failure was inferred from that harness error.

Zhuang now contains **200 typed resources**: P0 **69/94**, P1 **127/249**, P2 **4/305**, P3 **0/71**. Across 171 offered options, missing-entry counts are P0 162, P1 1,364, P2 30,125 and P3 7,481; 46 options have complete entry presence. These are presence counts, not linguistic acceptance or runtime coverage. Current scope remains 59 scoped catalogues and 112 outside-scope explicit-English-fallback catalogues.

## Limits

No Android build/AAPT, runtime bitmap-allocation failure, decoding/import, lifecycle, device layout/accessibility or font rendering tests were run. Source checks do not execute those paths. No merge, release or deployment is claimed. Only the canonical locale XML and this evidence report are intended to change; temporary harnesses and sentence mirrors are not published.
