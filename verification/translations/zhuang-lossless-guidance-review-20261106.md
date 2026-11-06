# Zhuang quality and lossless guidance review, 6 November 2026

## Scope and outcome

Base: `5487b68a75e7dbf3adc6b853934bb9753fc544ba`, tree `687029269ece1fc61149b65963be32c50d6dec4f`, on `review/nv-bottom-2038-20261103`. The preceding publication was reconciled with no pending or uncertain write. Develop remained `412aab0c604060fb66fbd2edc6bb05572d10b56d`; this does not alter develop or the disjoint Navajo work.

Adds P0 `ui_higher_quality_usually_makes_a_larger_file_lossless` and its directly supporting **P2**, not P1, checkbox label `ui_lossless_format`. The priority manifest corrected the initial checkbox classification before publication. The pair is retained as one coherent P0 explanation/control improvement; no P1 reduction is claimed. All 318 previous resources remain unchanged, for 320 total. Only canonical Zhuang XML and this report change.

Independent review recommends both complete additions unchanged as functional paraphrases, with **moderate linguistic confidence**. The explanation says higher quality generally makes a larger file, then describes the method that does not change colour data and states that all colour data remains unchanged. The checkbox says not to change colour data and retains the selected-format argument. “Generally” preserves the non-guaranteed size relationship. “All colour data” describes underlying data preservation, not merely similar appearance or a colour count. It does not promise identical encoded file bytes or preservation of all metadata. Numerical channel values are not spelled out, so this is not claimed as an independently standardized technical term for lossless encoding.

The repeated unchanged-colour-data phrasing intentionally connects prose to the checkbox. It is longer than the English technical term, with native software idiomaticity and actual layout unverified. The contextual checkbox imperative is not a general prohibition on editing the drawing. No native-human certification or exact full-sentence attestation requirement is imposed.

Existing P2 `ui_quality` was freshly reviewed in full and retained. Its quality noun, percent notation and `formatted="false"` attribute are suitable for the encoder setting, not a percentage-of-retained-fidelity guarantee. This review is a bounded contribution to [the complete translated-string review plan](p0-p1-release-plan-20261106.md), not a full-locale completion claim. The distinct missing P0 description about retaining more detail remains untouched rather than being filled using unsupported detail terminology.

## Evidence

- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), independently retrieved: quality at C37, general/usually at I4, kind/manner at Y19, whole/all at D20, and change vocabulary at G15/B37 support the composition. The quality word is distinct from the similarly spelled plant name. This OCR mirror is lexical evidence, not a modern software terminology standard.
- [Guangxi Minzu Bao, 17 August 2016, page 7](https://www.guangximinzubao.cn/szbzw/page/21/2016-08/17/07/2016081707_pdf.pdf), directly re-read in extracted lines 274–276: the bilingual headline uses the same quality word for film translation. [The 4 March 2015 school report](https://www.guangximinzubao.cn/szbzw/html/2015-03/04/content_12257.htm), line 38, independently combines quality with increasing height/level. Neither establishes a codec-specific quantitative guarantee.
- [Official ninth terminology announcement, 3 September 2025](https://www.guangximinzubao.cn/szbzw/html/2025-09/03/content_54472.htm), item 102, supports `soqgawq` as data. The reviewer's initial page extraction did not expose that item; integration directly re-opened the complete body at line 23 and verified it. The colour-data compound and complete sentences remain authored functional constructions.

## Consumers and technical boundary

`SaveOptionsDialog` binds the complete quality label to a 1–100 NumericSlider, the format argument to the lossless checkbox, and the whole new description to the generic explanation branch. That explanation is visible for JPEG XL, WebP and AVIF, and hidden for PNG. JPEG and HEIC retain their separate description. Other format-specific prose is unchanged. The checkbox is offered only for formats supporting selectable lossless mode; selecting it hides the quality control without discarding its chosen value. Confirmation uses the format's capability when passing the lossless flag. Cancel behavior is unchanged.

`NumericSlider` uses the full label as its accessibility name and exact-entry dialog title, and as an argument in current value/accessibility templates. The percent sign is literal label data, not a recursively interpreted formatting directive. `ImageExporter` passes quality and lossless to JPEG XL/WebP/AVIF, and explicitly passes false for HEIC.

Native source inspection bounds the preserved data to the editor's opaque RGB samples, not original import profiles, source-file bytes or animation. JPEG XL selects frame-lossless mode and zero distance, WebP selects lossless with near-lossless set to 100, and AVIF selects lossless with 4:4:4 and RGB/GBR matrix handling. This is source inspection, not newly executed codec fidelity evidence. No codec, dialog logic or resource consumers are modified.

## Verification and limits

- All 171 offered-option structural catalogue checks and importance-manifest validation pass. Existing entries, attributes, placeholders, numerals, literal tokens and escapes remain intact.
- Four localization host modules: **61 tests passed in 5.942 seconds**.
- **30 English/Zhuang Java cases** pass: static explanation, checkbox formatting with the three actual formats and percent/Unicode/null argument cases, the nonformatted quality attribute, and actual value/accessibility template composition at 1, 27, 95 and 100. These are not Android resource compilation.
- Temporary token-aware source checks verify the **three direct resource bindings**, capability/visibility behavior, range, callbacks, cancellation, quality-label consumers and format-to-codec routing. These are static checks, not Android interaction.
- Inspected, not run: `ExportFormatDialogTest.losslessFormatsToggleQualityAndRetainTheChosenLossyQuality`, its WebP-to-HEIC transition and PNG/JPEG visibility tests, plus the exact opaque-pixel round trips in `NativeCodecTest.losslessJxlRoundTripKeepsEveryOpaquePixelAndDimensions`, `WebpCodecTest.losslessRoundTripPreservesEveryRgbPixelOddDimensionsAndTheSource`, and `HeifCodecTest.avifLosslessPreservesEveryRgbPixelIncludingOddDimensions`. No new codec-success claim is inferred from those tests' existence.
- `git diff --check` passes. All **1,592** base file bytes and executable modes matched the complete remote tree. Publication uses the two-file overlay, exact expected parent and non-force lease, followed by complete remote-tree and exact changed-file readback. No permanent per-edit test package or wording-approval mirror is added.

Zhuang presence becomes P0 **78/94**, P1 **158/249**, P2 **81/305**, P3 **3/71**. Global missing counts are **153 / 1,333 / 30,048 / 7,478** across 171 offered options, with 46 complete-presence options. Presence does not certify linguistic correctness or completed all-string review, and excluded fallback-only catalogues are not newly filled.

Android SDK/Kotlin compiler are unavailable. Android compilation, Robolectric, device/native-codec execution, layout and TalkBack were not run. Exact-head Actions state is checked after publication and reported separately. Conditional release gates remain open; no merge, release or CI-pass claim is made.
