# Zhuang export-quality control, 5 November 2026

## Scope and wording

The live review branch was reconciled at parent `c9ee2e337dae8a0d1f9765daff2735d67cce8a5d`, tree `81e678ab10ca65ac022485f87e315840b58e8dbd`; no earlier write was pending. The missing P2 `ui_quality` label (“Quality (%)”) is added to canonical `Paintroid/src/main/res/values-b+za/strings.xml`, retaining `formatted="false"` and the literal percent notation. All 255 preceding typed resources are unchanged; the total is 256. Only the canonical XML and this report are published.

The [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), main C section, page 37, gives `cizlieng` for quality, distinct from the nearby `cizliengz` plant name. [Guangxi Minzu Bao, 17 August 2016, page 7](https://www.guangximinzubao.cn/szbzw/page/21/2016-08/17/07/2016081707_pdf.pdf), bilingual headline at extracted lines 274–276, independently uses the same spelling for improving film-translation quality. This corroborates quality rather than physical mass; it is not evidence of a particular encoder scale.

Independent linguistic/context review accepted the noun plus unchanged unit notation, with high lexical confidence and moderate-high confidence for this UI use. It denotes the encoder-quality setting, not a promise of retained fidelity or a percentage of file size. No native-user or complete-language acceptance is claimed. Canonical XML owns the wording.

## Actual consumers

`SaveOptionsDialog.kt:50,84–89,196` clamps the starting quality to 1–100, supplies the complete label to NumericSlider, and passes the chosen integer to ExportOptions in the confirmed SaveRequest. Quality is offered for JPEG, JPEG XL, WebP, HEIC and AVIF; the control is hidden in applicable lossless mode and for formats without quality support. Changing this label does not change codecs, quality values, visibility or cancellation.

`NumericSlider.kt` uses the full name as the SeekBar content description and exact-number dialog title. The value button and its accessibility description compose that label through the existing `%1$s` argument of separate resources. Consequently the label's percent sign remains literal data. Slider callbacks and exact-entry validation retain the 1–100 integer range. This does not promise any codec-specific relationship between the chosen number and visual fidelity.

## Executed verification

- All 171 offered-option catalogue checks and importance-manifest validation passed, together with existing-resource identity, source attributes, literal tokens and escaping.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 9.563 seconds**.
- Host Java checks: **18 cases passed**. Two XML contracts verify a nonformatted label with one literal percent; 16 compositions exercise the actual current value/accessibility templates in English and Zhuang at 1, 27, 95 and 100. The label is not incorrectly treated as a standalone format string. This is host XML/Java behavior, not Android resource compilation.
- Temporary token-aware consumer checks passed for the complete label bindings, integer bounds, callbacks to SaveRequest, supported-format/lossless visibility and cancel callback.
- Base snapshot verification checked Git blob identities and executable modes for **1,275 materialized files**. **269** unmaterialized non-tree entries remain retained. Publication verifies the complete final path/mode/type/blob overlay, a fresh expected-parent non-force lease and exact remote file readback.

Existing `SinhalaBurmeseZhuangPriorityWordingTest.qualityLosslessAndDitherRemainCoherentAcrossRealFormatChangesAndCancel` and `ExportFormatDialogTest` quality/lossless cases were inspected, not run. No permanent per-edit wording mirror or test package was added.

## Coverage and limits

Zhuang presence is P0 **69/94**, P1 **137/249**, P2 **50/305**, P3 **0/71**. Global missing typed resources across 171 options are P0 **162**, P1 **1,354**, P2 **30,079**, P3 **7,481**; 46 options have complete resource presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence does not establish fluency or runtime acceptance.

Android compilation, Robolectric, device glyph/layout, TalkBack, interactive format changes and actual encoding were not executed. Exact-head Actions state is checked after publication and reported separately; review-branch pushes do not ordinarily trigger CI. No merge, release, complete-language or CI-pass claim is made.
