# Zhuang: page selection and navigation actions

Date: 2026-11-05 (UTC). Base: `b59d6c05bbdccea24c9273195feab77eae3e3e52`, tree `75ff12886a1dc44f55b3ad1332f9af6664eddbdb`.

## Change and independent review

Added missing P2 `formats22_select_page`, `formats22_previous_page`, `formats22_next_page` and `formats22_open_page` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 227 previous typed resources remain unchanged. Canonical XML owns current wording.

Independent review retained all four. The title requests selection of one page; the positive button opens it. Previous/next describe earlier/following pages in the current sequence, fitting both document import and the legacy credit viewer. Linguistic confidence is moderate: component meanings and page terminology are supported, but exact UI-phrase idiomaticity is not directly attested. The immediately adjacent sense of the relational terms depends on these clear navigation controls. No native-speaker certification is claimed or required as a gate.

Sources checked directly:

- [Guangxi Minzu Bao, 基础知识系列（七）：壮文的拼写规则](https://www.guangximinzubao.cn/sy/jxzw/377556.html), abbreviation section, explicitly gives `mbaw 78` for page 78, abbreviated `mb.78`. This supports page-denoting usage beyond the leaf/sheet classifier gloss. It does not attest the complete new labels.
- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `senj` choose (S.htm 24/52), `hai` open (H.htm 15/45), `gonq` prior/before/front (G.htm 67/110), `laeng` after/behind (L.htm 6/49), and `mbaw` leaf/sheet (M.htm 21/56). The page classifier `bienj` and its `yieb` variant are also present (B.htm 36/80; Y.htm 15/31), but the published page usage provides no reason to prefer those alternatives here. The OCR's incomplete proofreading remains a source limitation.

A bounded search did not establish direct previous/next-page phrase attestation. The reviewed terms preserve sequence direction; “behind” is not interpreted as reversing the next action. No PDF-only, physical-sheet or animation-frame qualifier was introduced, because the resources have broader consumers.

## Actual consumer boundaries

`ImportSelection.showPages` serves PDF and TIFF imports. It displays the complete selected-page title and Open page caption. Previous/next supply the full accessibility descriptions of the existing arrow buttons; their visible arrow glyphs remain unchanged. The numeric input accepts pages 1 through the document count. Previous decrements and next increments by one, with endpoint/invalid-input disabling. Preview and final opening both convert that value to the zero-based page index. Opening selects one page as an image; it does not open all pages or preserve editable document objects.

Preview generation checks and cancellation/disposal guards are unchanged. The separate page-number field description, preview label, loading/range messages and rasterization notice remain unchanged and may use English fallback. This is not complete importer localization.

`LegacyImageCreditsActivity` also uses previous/next as full visible button captions. These navigate bounded presentation pages of stored credit text, not original PDF/TIFF pages. It decrements/increments the page index, clamps the current page, disables endpoints, hides navigation for a single page, resets scroll on navigation and starts at the first page after changing the selected credit. `ImageCreditTextPages` preserves the complete text across pages without splitting a supplementary character. No attribution, storage or export text is changed by this batch.

## Verification

- Fresh remote head and complete tree matched the preceding publication. All **1,261 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** remain retained, for 1,530 base leaves.
- Existing nodes, attributes and prefix bytes are preserved; four missing scalars are appended. XML/Android escaping, source attributes, ordered typed arguments, numerals, newlines and required literals pass. New XML Git blob: `cbe43da2ecb8e282fda70dba1c3f72d90d18e42c`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 8.368 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Eight host Java literal-label cases passed**, covering all four entries in English and Zhuang.
- Targeted token-aware source checks passed for all six live resource bindings, full title/button/accessibility text, navigation direction and endpoint gates, one-based input/zero-based selection, preview/cancel guards, and the legacy viewer's separate text-page route. These inspect source, not Kotlin/Android execution.
- Existing legacy-viewer navigation and text-page boundary tests were inspected, not executed in this batch.

Zhuang now has **231 typed resources**: P0 **69/94**, P1 **132/249**, P2 **30/305**, P3 **0/71**. Global missing entries across 171 options: P0 162, P1 1,359, P2 30,099, P3 7,481; 46 options have complete presence. Presence is not fluency or runtime acceptance. Scope remains 59 scoped catalogues and 112 outside-scope explicit-English-fallback catalogues.

## Limits

Android build/AAPT, executed import/pagination/lifecycle behavior, device rendering/layout, fonts and accessibility were not tested. No Android SDK or Kotlin compiler is configured in this executor. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and wording mirrors are not published.
