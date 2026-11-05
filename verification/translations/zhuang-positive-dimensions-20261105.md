# Zhuang positive size and image dimensions

Base: `21b67b07e36848c3d7d8a4cfb25b0fe759b010d5` on `review/nv-bottom-2038-20261103`.

Adds three missing P1 strings: positive size, positive dimensions and positive image dimensions. All 162 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Independent review and evidence

Independent linguistic and current-consumer review retained all three compositions. They ask the reader to use positive numbers to enter the size/dimensions, with the image modifier where required. The distinction between positive numbers and integers is intentional: fractional percentage input is valid in the relevant controls. The new wording does not impose a blanket integer-input restriction.

The [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) explicitly distinguishes `cingqsoq` (positive number, marked as a mathematical term) from `cingjsoq` (integer). It also lists an unrelated adverbial homonym; the instrumental construction and numeric-entry context support the mathematical reading here. Both reviews retrieved the explicit entries through targeted search-index text; full-page openings failed, and no printed-page image was checked. Wiktionary was unavailable and contributes no evidence.

Primary newspaper prose supports [physical dimensions](https://www.guangximinzubao.cn/zw/s_282578/382779.html) in the phrase “ciuq cikconq” and the [use-instrument-to-write construction](https://www.guangximinzubao.cn/szbzw/html/2024-06/05/content_50020.htm) in “yungh mauzbit sij.” The latter is narrative prose, not the quoted song lyrics elsewhere on the page. The established image noun and noun-modifier order are retained. These sources support lexical meaning and construction, not the exact new UI sentences. Confidence is stronger for the positive/integer distinction than for complete-sentence idiomaticity; no native-speaker certification is claimed.

## Consumer and targeted checks

- `NormalizeImagesDialog.value()` accepts finite positive input, requires integral pixel-unit input, permits fractional percentages and resolves the target through rounding to `1..Int.MAX_VALUE`. A null result produces the positive-size notice in `refresh()` and disables the apply button. The notice is not a guarantee that every positive value fits pixel bounds.
- `ClassicPaintActivity.dimensionsDialog()` places the positive-dimensions notice on the width input when `DimensionControls.dimensions` is null, before the edit branch. `DimensionControls` validates both dimensions, uses the same positive/pixel-versus-percent distinction and requires resolved pixel values in the positive integer range.
- `ImageDimensions`, `ImageMemoryPolicy.check()` and `PaintDocument.blank()` / `resize()` use the image-dimensions notice for strict width-and-height greater-than-zero guards. Memory-budget and allocation failures remain separate; positivity does not guarantee admission or successful allocation.
- 62 host tests pass: translations, translation boundaries, priority accounting, current localization contracts and numeric-entry source coverage. All 171 offered catalogues and the priority manifest pass structural checks. Six English/Zhuang Java resource-render checks pass; these strings have no format arguments.
- Missing-only integration preserves attributes, formatting, newlines, escaping, all earlier values and XML prefix bytes. Temporary Kotlin source checks identify every consumer of these keys and verify the guards above. They do not execute Android input or dialogs.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 252 other non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, followed by full tree and changed-file verification.

Zhuang direct presence becomes 165 resources: P0 68/94, P1 97/249, P2 0/305 and P3 0/71. Global P1 gaps fall from 1,397 to 1,394; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed dialog operation, device/layout/accessibility test, merge or release is claimed. No implementation or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
