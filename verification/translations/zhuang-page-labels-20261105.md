# Zhuang: page-number input and range validation

Date: 2026-11-05 (UTC). Base: `d590b507e08a133a7da915640bf57647d20b1fc9`, tree `93124b1409f2bc1a334230217c6881af78f9d7d3`.

## Change and independent review

Added missing P2 `formats22_page_number` and `formats22_page_range` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 242 prior typed resources remain unchanged. Canonical XML owns current wording.

Independent review accepted the page-index noun phrase and the final range instruction. The instruction explicitly requests one number, retains the inclusive lower bound 1 and integer upper-bound argument, and follows the existing general numeric-input pattern. This is a page index, not a page count. Exact interface phrases are compositional rather than independently attested stock wording; this narrower idiomaticity confidence is retained. Native-speaker certification is neither claimed nor treated as an approval gate.

Evidence checked independently:

- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): main H.htm 21/45 gives the numbering/designator sense of `hauh`; H.htm 22/45 also records `hauhmax` and `hauhsoq`. The main numbering entry, not the separate appendix's horn/mark senses, supports this usage. S.htm 27/52 gives `sij` (write), D.htm 5/110 `daj` (from), and D.htm 18/110 `daengz` (to/reach).
- [Official Zhuang terminology, 26 August 2024](https://www.guangximinzubao.cn/sy/jxzw/390966.html), item 154, uses `aen hauh baih dwk` for caller number. This supports nominal number/designator usage and its classifier, not the exact page-number compound.
- [Published spelling guidance](https://www.guangximinzubao.cn/sy/jxzw/377556.html) explicitly identifies `mbaw 78` as page 78.
- [Dauqngeix Gij Ndwenngoenz Doihengz Sawcuengh, 27 December 2017](https://www.guangximinzubao.cn/szbzw/html/2017-12/27/content_24073.htm) demonstrates the bounded `daj … daengz` construction with a year range. Applying it to the input's numeric range remains compositional.

The proposed separate page-preview label was deliberately omitted: a view-first action phrase does not clearly name the passive preview image used by its actual ImageView accessibility consumer. Existing generic Preview wording is not proof that this new noun-like image description is suitable. No substitute was invented.

## Actual consumers and preserved boundaries

`ImportSelection.showPages` uses the full number label as the EditText's accessibility description and the full range instruction as visible status after blank, invalid or out-of-range input. Each new resource has one direct production binding in `ImportSelection.kt`.

The initial field value remains 1. Valid input is an integer in `1..count`; imports receive `value - 1`. Invalid input disables opening and both navigation buttons, clears the previous preview, and shows the range message with the actual page count. Valid previous/next actions change the field by one. Preview generation tickets reject stale results; cancel/dispose invalidates pending work and cleans up. No parsing, navigation, import or cancellation logic changes. Other page-description, preview and loading text remains unchanged and can fall back to English.

## Verification

- Fresh remote head/tree matched the preceding publication. **1,267 materialized files** matched base Git hashes and executable modes. **269 unmaterialized leaves** are retained, for **1,536 base leaves**.
- Existing nodes, attributes and prefix bytes are preserved; only the two missing scalar resources are appended. XML/Android escaping, source attributes, typed/ordered arguments, source numerals, newlines and required literals pass. XML Git blob: `28c1e062c1a63e75cba0f0ceca0eb4fde6d9115a`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed in 11.515 seconds**: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **14 host Java cases passed**: for each of English/Zhuang, literal-label preservation, five positive integer upper endpoints (1, 2, 20, 9999 and the maximum Java integer), and rejection of a noninteger format argument. These verify formatting, not executed Android input validation.
- Targeted token-aware source checks passed for both complete-resource consumers, inclusive bounds, one-based/zero-based conversion, invalid-input gating and preview clearing, stale-result rejection, previous/next actions and cancellation cleanup.
- Existing `OrdinaryPriorityFollowthroughTest.actualOneAndTwoPageChooserKeepsRangeNavigationAndCancellation` and `LocaleNumberInputTest.pageFieldRetainsPersianDigitsAndDisablesFractionalNegativeAndOutOfRangeEntries` were inspected, not run in this batch. Their prior or other-locale results are not claimed as current Zhuang runtime evidence.

Zhuang now has **244 typed resources**: P0 **69/94**, P1 **133/249**, P2 **42/305**, P3 **0/71**. Global missing entries across 171 options: P0 162, P1 1,358, P2 30,087, P3 7,481; 46 options have complete presence. Presence is not fluency or runtime acceptance. Scope remains 59 scoped catalogues and 112 outside-scope explicit-English-fallback catalogues.

## Limits

Dictionary OCR/transcription uncertainty remains; no printed dictionary page was independently inspected. Android build/AAPT, executed page selection/decoding, device layout, glyph rendering, keyboard and accessibility were not tested. No Android SDK or Kotlin compiler is configured in this executor. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary checks and wording mirrors are not published.
