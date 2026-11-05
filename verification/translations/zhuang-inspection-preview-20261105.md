# Zhuang: image inspection and page-preview errors

Date: 2026-11-05 (UTC). Base: `962a5f2d74760ff08836a19a5ae067fd540e010d`, tree `6b6d173407bd8d55ac8e160914b4202723486622`.

## Change and wording review

Added two missing resources to canonical `Paintroid/src/main/res/values-b+za/strings.xml`: P1 `ui_not_enough_memory_to_inspect_this_image` and P2 `formats22_preview_unavailable`. The first retains this-image inspection plus insufficient RAM; the second identifies unavailable previewing and preserves the complete `%1$s` diagnostic. All 201 previous typed resources are unchanged. Canonical XML owns the exact wording.

Independent review retained both proposed compositions, with moderate confidence and no concrete semantic defect found. Exact software collocations and whole sentences are not independently attested; this is not a native-fluency certification. Native-human approval is not a gate.

Sources directly checked:
- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `genjcaz`, check/inspect (G.htm 33/110); `yawj`, view/look/read (Y.htm 11/31); `sien`, first/beforehand (S.htm 29/52). The preview expression is a grounded composition of the latter two, not a dictionary entry claiming standardized software terminology. The OCR warns of incomplete proofreading.
- [Guangxi Minzu Bao, 27 May 2015](https://www.guangximinzubao.cn/szbzw/html/2015-05/27/content_13413.htm), prose paragraphs 2–3: transitive use of checking examination papers supports the inspection verb. The existing preview label supplies product consistency, not independent linguistic evidence.

## Actual consumer boundaries

`ClassicPaintActivity.readImage` uses the P1 notice in its outer worker OOM catch, including staged-file creation/copy/preparation. Later asynchronous `ImportSelection` failures instead return through a callback using `ui_could_not_open_image`. This new resource is **not** the universal inspection or selection failure message. `ioFailed` appends a period and the exception message, or its separate fallback, before displaying the whole result. The translated prefix therefore has no final period.

`ImportSelection.showPages` uses the P2 notice for page-preview `Exception` status, with the whole exception message or an empty string. Preview OOM has a different resource. Status updates require a live activity/current generation; stale decoded results are recycled. A valid page number, not successful previewing, controls opening availability. The translation does not claim opening is impossible or that the file is invalid. An empty diagnostic leaves the source's existing trailing-colon behavior.

## Verification

- Fresh remote tree reconciled with the preceding verified publication. All **1,252 materialized files** matched base Git blob hashes and executable modes; **268 unmaterialized leaves** remain retained, for 1,520 base leaves. This verifies the extracted source reviewed independently against the remote base.
- Existing 201 typed resources, attributes and original prefix bytes preserved. Two missing scalars added. XML, Android escaping, source attributes, ordered typed arguments, numerals, newlines and required literal-token checks pass. New XML Git blob: `f66d057a176fca473d6f748fd8ab9ed58c1b8717`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 10.792 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **14 host Java format/render cases passed** across English and Zhuang: literal inspection prefix, prefix punctuation, and preview diagnostics covering null-to-empty conversion, empty text, ASCII, percent-looking argument text, Unicode/emoji and embedded newline. Diagnostic content is not reinterpreted as a format template.
- Targeted token-aware source checks passed for the staging OOM catch, distinct asynchronous failure callback, preview exception-vs-OOM handling, full diagnostic argument, activity/generation guard, resource bindings and valid-page opening rule.

Zhuang now has **203 typed resources**: P0 **69/94**, P1 **128/249**, P2 **6/305**, P3 **0/71**. Global missing-entry counts across 171 options: P0 162, P1 1,363, P2 30,123, P3 7,481; 46 options have complete presence. These are presence counts, not linguistic acceptance or runtime coverage. Scope remains 59 scoped catalogues plus 112 outside-scope explicit-English-fallback catalogues.

## Limits

No Android build/AAPT, executed input-stream or allocation-failure path, page decoding, chooser/lifecycle, device layout/accessibility or font checks were run. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and sentence mirrors are not published.
