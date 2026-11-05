# Zhuang: RGB component explanations

Date: 2026-11-05 (UTC). Base: `cc25c09c7dc5a2e219bc332fc0d7b3c1bfcab000`, tree `365cb940c64115d9a59cd12e50a773ce076b07ca`.

## Change and independent review

Added missing P2 `ui_colour_red_range`, `ui_colour_green_range` and `ui_colour_blue_range` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. Each retains the familiar RGB initial and original 0–255 range, adding a Zhuang colour explanation. All 231 previous typed resources remain unchanged, including the already translated shared colour/hex description. Canonical XML owns current wording.

Independent review retained all three. Red and blue have strong lexical support; green has slightly narrower confidence because its term can also cover traditional “qing”/blue senses. The retained G initial and adjacent B channel distinguish the controls. The new complete RGB captions are composed UI wording, not a claimed published terminology standard. No native-speaker certification is claimed or required as a gate.

Sources checked directly:

- [Guangxi Minzu Bao, 15 May 2019, page 7](https://www.guangximinzubao.cn/szbzw/page/21/2019-05/15/07/2019051507_pdf.pdf), Li Pin, “Loqgangj Fanhoiz Cuengh Gun Sawloih Saek / 试说颜色词的汉壮翻译——以‘绿’的翻译为例”: the colour-word list gives red `nding/hoengz`, green `heu/loeg` and blue `lamz` together. The following discussion explains the broader historical range of `heu`, including “qing”/blue usage. This supports the chosen colour meanings but not the complete new captions.
- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `nding` red (N.htm 24/72), `heu` qing (H.htm 26/45), `lamz` blue (L.htm 10/49). The OCR's incomplete proofreading remains a source limitation; the published colour-word list supplies independent corroboration.

## Actual consumer boundaries

Each new resource has one live binding in `AdvancedColourDialog`. The RGB group preserves the R/G/B channel order and each maximum of 255. The field helper uses the entire caption both for its visible label and for the numeric field's accessibility description. No surrounding sentence or dynamic value is assembled from these resources.

The internal channel keys remain `r`, `g` and `b`. The input path checks the 0–255 range and converts the values to integer components before `Color.rgb`. Decimal input is accepted and then truncated with `toInt`; this is not integer-only validation. Synchronization uses `Color.red`, `Color.green` and `Color.blue`, displayed with zero decimal places. These operations, alpha handling and all HSV/HSL fields are unchanged.

The existing shared colour/hex description remains unchanged. It describes basic swatches and occupied saved swatches using a leading hash and six uppercase hexadecimal digits; it is not newly translated by this batch. These three field captions do not complete the colour dialog's localization.

## Verification

- Fresh remote head and complete tree matched the preceding publication. All **1,262 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** remain retained, for 1,531 base leaves.
- Existing nodes, attributes and prefix bytes are preserved; three missing scalars are appended. XML/Android escaping, source attributes, ordered typed arguments, numerals, newlines and required literals pass. New XML Git blob: `71d812d5ba75dfce9dcae440d88ec21caeff8652`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 9.080 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Six host Java literal-label cases passed**, covering the three entries in English and Zhuang.
- Targeted token-aware source checks passed for all three live bindings, complete visible/accessibility captions, RGB order and range, unchanged channel conversion, and the retained shared colour-description consumers. These inspect source, not executed Kotlin/Android behavior.

Zhuang now has **234 typed resources**: P0 **69/94**, P1 **132/249**, P2 **33/305**, P3 **0/71**. Global missing entries across 171 options: P0 162, P1 1,359, P2 30,096, P3 7,481; 46 options have complete presence. Presence is not fluency or runtime acceptance. Scope remains 59 scoped catalogues and 112 outside-scope explicit-English-fallback catalogues.

## Limits

Android build/AAPT, executed colour conversion and field interactions, device rendering, layout and accessibility were not tested. The longer captions particularly need actual narrow-screen and accessibility verification. No Android SDK or Kotlin compiler is configured in this executor. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and wording mirrors are not published.
