# Zhuang dimension constraints

Base: `aa7a8004c876b84659306150e9db2a7d75227f4e` on `review/nv-bottom-2038-20261103`.

Adds three missing P1 strings: positive dimensions no larger than the original, valid dimensions and a positive normalization target. All 175 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Independent review and evidence

Independent linguistic and current-consumer review retained all three compositions at moderate confidence. The no-larger constraint allows equality. Positive numbers remain distinct from integers, which matters for percentage input. The generic validity message describes usable dimensions in context; it does not add a memory-budget guarantee. The target phrase expresses an intended size rather than the current size.

The [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) distinguishes mathematical positive number from integer. Primary prose supports [physical dimensions](https://www.guangximinzubao.cn/zw/s_282578/382779.html), [postnominal original](https://www.guangximinzubao.cn/szbzw/html/2021-09/29/content_41823.htm), and the [larger-than comparative](https://www.guangximinzubao.cn/zw/f_282583/390903.html). The negative comparative is composed from that evidence; the cited article does not attest the exact negative phrase.

[Sybesma's postverbal-potential study](https://www.researchgate.net/publication/300848712_6_Zhuang_A_Tai_language_with_some_Sinitic_characteristics_Postverbal_%27can%27_in_Zhuang_Cantonese_Vietnamese_and_Lao), section 3.3.2, supports an underlying object followed by verb and potential marker for an -able property. [Sio and Sybesma](https://www.academia.edu/214062/The_Nominal_Phrase_in_Northern_Zhuang_A_descriptive_study_2008_) support postnominal modification. [Newspaper prose](https://www.guangximinzubao.cn/szbzw/html/2019-09/25/content_33327.htm) supports the target/objective noun. Its technical combination with dimensions is not independently attested and has narrower confidence than the individual words. The sources support lexical senses and construction, not the complete UI sentences. No native-speaker certification is claimed.

## Consumer and targeted checks

- `ImageResizeDialog.target()` accepts parsed dimensions only when each axis is no greater than its source axis. Equal dimensions remain allowed. The new instruction appears when this result is null; memory admission and resize-button enablement are checked separately.
- `AssemblyActivity.outputSizeDialog()` uses the generic valid-dimensions instruction only when `DimensionControls.dimensions` is null. Renderer memory fit is a separate condition for output-button enablement and submission.
- `DimensionControls` requires finite positive entries, integral values in pixel mode and positive Int-bounded resolved dimensions. Fractional percentage input is permitted. These translations do not impose integer-only entry in all modes.
- `AssemblyImage.placedSize` rejects a nonpositive normalization target before computing the scaled counterpart. The normalization overflow/range diagnostic remains separate. This resource does not represent a complete guarantee that any positive target is usable.
- 62 host tests pass: translations, translation boundaries, priority accounting, current localization contracts and numeric-entry source coverage. All 171 offered catalogues and the priority manifest pass structural checks. Six English/Zhuang Java resource-render checks pass; these strings have no format arguments.
- Missing-only integration preserves attributes, formatting, newlines, escaping, all earlier values and XML prefix bytes. Temporary Kotlin source checks identify every consumer and verify the constraints above. They do not execute Android input, decoding, allocation or assembly operations.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 257 other non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, followed by full tree and changed-file verification.

Zhuang direct presence becomes 178 resources: P0 68/94, P1 110/249, P2 0/305 and P3 0/71. Global P1 gaps fall from 1,384 to 1,381; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed dimension operation, device/layout/accessibility test, merge or release is claimed. No implementation or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
