# Zhuang lossy-quality guidance and numeric composition review

2026-11-06. Base: `e97889e3b79bdc7b92c937a4c2009157f0fb8562`, branch `review/nv-bottom-2038-20261103`. Canonical wording: `Paintroid/src/main/res/values-b+za/strings.xml`.

## Scope and finding

Add the missing P0 `save20_lossy_quality_description`, used by JPEG and HEIC export options. Independently review the two existing numeric composition resources in full and retain them. This is a bounded addition and review, not whole-catalogue acceptance or a release qualification.

New wording: “Cizlieng sang di, gij bouhfaenh saeq ndaw dozsiengq haenx baujlouz ndaej ndei di. Itbuen vwnzgen couh hung di.” Functional reading: higher quality preserves the fine parts within the image better; generally the file is larger.

The review changed the draft's “preserve more small parts” to “preserve fine parts better.” This avoids implying more image regions, increased image dimensions, or retention of an additional area. The source's detail-preservation idea is expressed as fidelity of fine image parts, not a claimed specialist term. The separate second sentence keeps “generally” attached to file size. There is no promise of identical pixels, preservation of all information, or a guaranteed increase in bytes. Meaning and composed wording confidence are moderate; the detail paraphrase is less precise than an established specialist expression. No native-human software usability assessment is claimed.

Retained full resources:
- `ui_numeric_slider_value`: `%1$s: %2$d`
- `ui_tap_to_type_a_number`: `%1$s: %2$s. Diemj daeuj sij aen soq ndeu.`

`NumericSlider` supplies the name and an integer to both. The accessibility template's `%s` accepts that integer. With the unchanged `ui_quality` label these read “Cizlieng (%): 95” and “Cizlieng (%): 95. Diemj daeuj sij aen soq ndeu.” The action opens exact numeric entry; it does not immediately change the value. Formatting/action correspondence is high confidence, linguistic retention moderate. The earlier [quality-label/lossless review](zhuang-lossless-guidance-review-20261106.md) remains applicable to its unchanged label, source and consumer; this batch does not claim a new complete review of that earlier cohort.

## Language evidence

Both integrator and independent reviewer checked relevant components, complete sentences and consumers.
- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `cizlieng` quality (C37/L342), distinct from the plant `cizliengz`; `baujlouz` retain (B25/L153); `saeq` fine/small (S4/L1531); `itbuen` generally (I4/L1053); `ndei` good (N21/L1332). The reviewer also checked `sij` write. Older dictionary entries for `diemj` alone do not certify the modern touchscreen sense.
- [2015 primary prose](https://www.guangximinzubao.cn/szbzw/html/2015-03/04/content_12257.htm), L38, supports quality plus high comparative usage.
- [2020 bilingual teaching article](https://www.guangximinzubao.cn/szbzw/html/2020-04/22/content_35282.htm), L27, explicitly pairs `bouhfaenh` with part of a whole. It supports the component, not an attested translation of technical image detail. The original draft's ambiguity was addressed rather than treating this article as proof of the complete UI phrase.

No exact-sentence attestation or native certification is implied. Bounded dictionary searches did not supply a better established detail noun; no invented transliteration was used.

## Consumer and behavior boundaries

`SaveOptionsDialog.kt:82–105` supplies the full resource to the export description `FlowTextView` for JPEG and HEIC. These formats show quality from 1 to 100 and hide the lossless control. JPEG XL, WebP and AVIF use separate guidance. PNG hides the description. Format changes refresh the text. Confirmation masks the lossless flag by format support; cancellation invokes the existing cancel path.

`ImageExporter.kt:15,23–25` passes quality to HEIC with lossless false, and to Android JPEG compression with a 1–100 clamp. No dimension change is part of these calls. `NumericSlider.kt:57–80` uses the complete value and accessibility templates, passes the unchanged quality label as data rather than as a formatting template, opens numeric input on a tap, and validates the inclusive range. No fixed line limit is applied to the description at its binding; this is not a rendered-layout guarantee.

## Checks and limits

- All 1,594 base non-tree entries matched the fetched remote tree and local bytes/executable modes before editing. Only canonical Zhuang XML plus this report are intended for publication. Develop remained `412aab0c604060fb66fbd2edc6bb05572d10b56d`; separate Navajo work is untouched.
- Generic resource validation: no duplicate identity, XML, placeholder, Android escaping, literal-token, or manifest errors. All 321 earlier Zhuang resource elements and source attributes are preserved.
- 61 existing host tests passed in 5.660 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- JDK execution passed 20 English/Zhuang cases: both prose strings, the literal-percent label's `formatted="false"`, and both real numeric templates at 1, 27, 95 and 100. Four static source bindings and JPEG/HEIC control/export paths passed. `git diff --check` passed. Temporary checks are not permanent sentence approval fixtures.
- Inspected, not run: `ExportFormatDialogTest.changingFromLosslessWebpToHeicShowsNumericQualityAndNeverClaimsLosslessHeic` (reject 101, accept 38); `pngHidesQualityAndJpegKeepsItWithoutOfferingLossless` (PNG/JPEG switching retains 74); complete JPEG-description bindings in `CroatianBosnianP0WordingTest` for its locales. Those are not evidence of Zhuang runtime execution.
- Inspected, not run: `HeifCodecTest.heicAndAvifQualityControlsProduceDecodableOpaqueImages`. It compares low/high encoded bytes and checks decoding; it does not prove every image's file size increases monotonically.
- No Android SDK/Kotlin compiler is available here. Android compilation, Robolectric, native codec execution, device/TalkBack and rendered layout were not run. Remote exact-head Actions status must be reported separately. No CI, merge or release pass is claimed.

Presence after this addition: 322 typed Zhuang resources; P0 80/94, P1 158/249, P2 81/305, P3 3/71. Across 171 offered options, missing counts are P0 151, P1 1,333, P2 30,048 and P3 7,478; 46 options have complete direct presence. Counts do not certify wording, scope expansion, fallback translation or full review. Continue the [P0/P1 and all-translated-string release plan](p0-p1-release-plan-20261106.md); release gates remain open.
