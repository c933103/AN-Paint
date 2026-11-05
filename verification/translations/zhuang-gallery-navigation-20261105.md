# Zhuang: gallery Search and Back

Date: 2026-11-05 (UTC). Base: `6551df32da1ea72343f8fcce950be377ba2a201d`, tree `2b68872061f7d8e084dda4ba0ce23b650e7fce1a`.

## Change and independent review

Added missing P2 `ui_search34` and `ui_gallery_back34` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`, retaining both `formatted="false"` attributes. All 246 previous typed resources remain unchanged. Canonical XML owns current wording.

Independent review accepted both short action verbs. The search verb's broad seek/find sense covers provider search and in-page finding; it does not require remote navigation. The return verb fits browser history and the provider-home fallback, without asserting an exit to the painting canvas. No evidence required an invented longer phrase. Lexical meaning and action fit are supported; conventional software idiom and native usability remain unverified.

Evidence:

- Both reviews checked [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `ra`, seek/find (R.htm 1/33), with `cimh` cross-reference (C.htm 51/78); `dauq`, return, referring to `ma` (D.htm 40/110), with reciprocal alternatives in the M opening entries. The appended `itciengz` example also uses bare `dauq` for going back after finishing work. The broader search-through/rummage entry was considered but is not demonstrably preferable to the neutral seek/find verb here.
- A separate [official terminology publication, 8 July 2026](https://www.guangximinzubao.cn/sy/gg/637735.html), item 177, uses `dauq` in return-to-the-wild terminology. This corroborates return meaning, not a browser-label convention.

The dictionary is an OCR/transcription of the 1984 work; no printed page was independently inspected. No inaccessible scholarly paper is used as inspected evidence, and native-speaker certification is not claimed or treated as an approval gate.

## Actual consumers and limits of scope

`ui_search34` has two direct bindings in `MediaGalleryActivity`: the generic search-field label and the common Search button. `gallerySearchField` assigns the complete label as a native hint, not an explicit content description. In vertical mode the complete visible caption instead uses `labelFor=search.id` and clears that hint. The Search button receives the full text through `galleryButton`.

The Irasutoya field uses the separate, unchanged English/Japanese-language hint; the common action button still uses Search. Searching retains its trimmed, 512-character query and empty-input guard. Openclipart/Commons navigate to provider searches, Irasutoya uses its existing script/pending-search flow, and Catrobat performs `web.findAllAsync`. Both button and keyboard Search actions invoke the same function. No provider/network action was executed for this wording change.

`ui_gallery_back34` is the explicit accessibility description of the Back arrow. It invokes `web.goBack()` when possible, otherwise loads `provider.home`. The visible arrow still follows the effective locale's horizontal navigation direction, not vertical text-column order. It does not close the activity. No navigation, query, provider, input or layout code changes.

## Verification

- Fresh remote matched the preceding publication. **1,270 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** are retained, for **1,539 base leaves**.
- Existing nodes, attributes and prefix bytes are preserved; two missing scalars are appended. XML/Android escaping, source attributes, typed/ordered arguments, numerals, newlines and required literals pass. XML Git blob: `18d3083bd86ab77d8f37afbfe1af357d66ec26a5`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed in 8.675 seconds**: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Four Java literal-label cases passed**, covering both labels in English/Zhuang.
- Targeted token-aware source checks passed for all three direct bindings, full hint/caption/button/accessibility routes, history/home behavior, effective-locale arrow, provider-specific search routes, empty-input guard and keyboard action. An escaping error in the temporary Commons-query assertion was corrected before these checks passed; no production code changed.
- Existing `GalleryBackDirectionTest`, `GalleryControlReachabilityTest` and `GalleryControlsLayoutTest` cases were inspected, not run. Their history branches, accessibility, query action and layout coverage are not claimed as current Zhuang runtime results.

Zhuang now has **248 typed resources**: P0 **69/94**, P1 **133/249**, P2 **46/305**, P3 **0/71**. Global missing entries across 171 options: P0 162, P1 1,358, P2 30,083, P3 7,481; 46 options have complete presence. Presence is not fluency or runtime acceptance. Scope remains 59 scoped catalogues and 112 outside-scope explicit-English-fallback catalogues.

Android build/AAPT, executed navigation/search/input, provider behavior, device layout, glyph rendering and accessibility were not tested. No Android SDK or Kotlin compiler is configured in this executor. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary checks and wording mirrors are not published.
