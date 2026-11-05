# Zhuang: height, width and equal-dimension labels

Date: 2026-11-05 (UTC). Base: `09de8b6a6f453ac0be43f3485f14f263fd1f14da`, tree `e54952bada54f78838951b06a01686e8246b56db`.

## Change and wording review

Corrected existing `ui_height` and `ui_heights` from the unsupported height term `Gau` to `Sang`. Added four missing resources: P1 `ui_height_in`, and P2 `ui_width_in`, `ui_same_height`, `ui_same_width`. The existing width term `Gvangq` is retained. Canonical `Paintroid/src/main/res/values-b+za/strings.xml` owns the exact wording; no permanent sentence mirror or per-edit test package is added.

Independent linguistic/context review supports all six changes. Height and width have strong direct evidence in measured rectangular dimensions; equal-height wording is directly attested, while equal-width is a supported parallel composition. Confidence is narrower for compact software-label idiomaticity. The correction is supported by positive height evidence and the checked dictionary's different meanings for `gau`, not merely by failure to find a word. This does not assert that no dialect anywhere could use it. Native-human approval is not a gate or a claimed certification.

Sources directly checked:
- [Guangxi Minzu Bao, 11 June 2025](https://www.guangximinzubao.cn/szbzw/html/2025-06/11/content_53748.htm), page 7 article about an old Sawndip book, first body paragraph: “Ceksaw sang 20.5 lizmij, gvangq 15.5 lizmij” directly describes the book's measured height and width.
- [Guangxi Minzu Bao, bilingual prose about village Zhuang](https://www.guangximinzubao.cn/sy/mzwx/379365.html), the `Detnet` section: “caeuq gou sang doxdoengz” directly supports equal-height wording. Equal-width wording is a transparent parallel, not a quoted attestation.
- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `sang`, high (S.htm 14/52); `gvangq`, broad/wide (G.htm 85/110); `doxdoengz`, same/matching (D.htm 70/110). The checked `gau` entry (G.htm 26/110) gives cake, glue/rubber and a dialect knocking sense, not height. The OCR warns of incomplete proofreading.

## Actual consumer boundaries

`DimensionControls.display` keeps height and width on their correct axes. Visible labels receive `px` or `%`; the two input content descriptions receive expanded unit-name resources. Those expanded unit names still use English fallback in Zhuang, so this is not a claim that the entire accessibility phrase is localized.

`AssemblyActivity` binds the equal-width and equal-height commands to their matching `NormalizeAxis` values. `NormalizeImagesDialog` uses the same labels as titles, and `ImageAssembly.normalize` applies the chosen dimension to all assembly entries, not merely a selected/placed image. The other dimension scales from the crop with integer rounding. Percent mode uses the largest current dimension on the chosen axis as its reference. These commands normalize size; they do not mean alignment or equal spacing. Pixel-mode normalization input descriptions also use the corrected height label.

No actual Kotlin resource binding for `ui_heights` was found. That correction is catalogue consistency, not an additional claimed runtime fix.

## Verification

- Fresh remote tree reconciled with the preceding verified publication. All **1,252 materialized files** matched base Git blob hashes and executable modes; **269 unmaterialized leaves** are retained, for 1,521 base leaves.
- Of 203 previous typed resources, **201 remain unchanged**, two receive only the reviewed height-text correction, and four missing scalars are added. Source attributes, ordered typed arguments, XML/Android escaping, numerals, newlines and required literal tokens pass. Original bytes outside the two substitutions and appended entries are preserved. New XML Git blob: `1885a9a7d4c0d58bd653f5b286338d68bbb7b64b`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 11.531 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **42 host Java formatting/literal cases passed** across English and Zhuang. Unit arguments cover `px`, `%`, expanded English units, Unicode/emoji and percent-looking text. Each formatted unit remains intact and is not interpreted again as a format template.
- Targeted token-aware source checks passed for all six resource bindings, axis identity, expanded input-unit arguments, normalization command/title dispatch, all-entry application and integer-rounded crop scaling. The unused plural-height key is kept distinct from live bindings.

Zhuang now has **207 typed resources**: P0 **69/94**, P1 **129/249**, P2 **9/305**, P3 **0/71**. Global missing-entry counts across 171 options: P0 162, P1 1,362, P2 30,120, P3 7,481; 46 options have complete presence. These are presence counts, not linguistic acceptance or runtime coverage. Scope remains 59 scoped catalogues plus 112 outside-scope explicit-English-fallback catalogues.

## Limits

No Android build/AAPT, executed dimension-control or normalization path, device layout, accessibility speech or font checks were run. Consumer findings are static source checks, not runtime execution. No merge, release or deployment is claimed. Only canonical locale XML and this concise report are intended to change; temporary harnesses are not published.
