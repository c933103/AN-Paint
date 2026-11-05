# Zhuang crop commands and whole-image warning

Base: `ee40cd8708883d76041ba8c254d1f2f6669e196e` on `review/nv-bottom-2038-20261103`.

Adds two missing P1 crop labels and the P0 warning for margins that would leave no image area. All 150 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Independent review and evidence

Independent language and consumer review replaced the draft's harvesting-oriented cut verb with `daet`, supported by controlled cutting. [Guangxi Minzu Bao's 10 September 2025 translation page](https://www.guangximinzubao.cn/szbzw/html/2025-09/10/content_54492.htm) uses it when cutting a blanket into pieces. [Published prose from 16 October 2024](https://www.guangximinzubao.cn/szbzw/html/2024-10/16/content_51700.htm) uses it in vegetation maintenance and separately supports `henz` for sides and `daengx` for entirety. The [1984 dictionary's OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) corroborates cut, edge and whole, but its OCR is not sole evidence.

The warning preserves a hypothetical adverse result, using the conditional/passive construction found in the [5 June 2024 translation page](https://www.guangximinzubao.cn/szbzw/page/21/2024-06/05/08/2024060508_pdf.pdf). It does not claim removal has already happened, mention deletion of a file, or assert irreversibility. Established catalogue image vocabulary is supported by [published depicted-figure prose](https://www.guangximinzubao.cn/szbzw/html/2017-12/27/content_24064.htm); [MediaWiki's Zhuang resources](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/za.json) corroborate the delete verb.

The accepted wording is a moderate-confidence editorial description of cutting image edges. None of these sources independently attests the complete crop labels or warning as software terminology. Technical idiomaticity remains uncertain; no native-speaker certification is claimed or required for this bounded publication.

## Consumer and targeted checks

- `AssemblyActivity` binds the image-crop button to `crop(false)`, selecting the current image and opening `ImageCropDialog`.
- The single-image dialog title formats the actual `reference.name` into `%1$s`. The batch title is a different resource and remains outside this change.
- `CropMargins.rect()` validates individual margins, computes the remaining rectangle, then rejects nonpositive width or height with this warning before returning a rectangle. The warning is prospective, not a report of a completed crop.
- The dialog validates the reference and selected images during preview. Submission computes every selected rectangle before calling `apply`; exceptions appear in its status view. The crop operation copies rectangle metadata, and `ImageAssembly.change()` validates before writing and recording Undo state. These are source observations, not executed Android or Undo tests.
- 61 host tests pass: translations, translation boundaries, priority accounting and current localization contracts. All 171 offered catalogues and the priority manifest pass structural checks. Six English/Zhuang Java resource-render checks pass, including exact insertion of a filename containing percent, XML-sensitive characters and quotes into `%1$s`.
- Missing-only integration preserves attributes, typed/ordered arguments, newlines, escaping, earlier values and XML prefix bytes. Temporary source checks cover the actual consumer routes above.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 248 other non-tree entries are retained. The publication procedure uses an expected parent and non-force branch lease, with full-tree and changed-file verification.

Zhuang direct presence becomes 153 resources: P0 68/94, P1 85/249, P2 0/305 and P3 0/71. Global gaps become P0 163, P1 1,406, P2 30,129 and P3 7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed crop or pixel operation, device/layout/accessibility test, merge or release is claimed. No implementation or other locales change. Remaining crop instructions and controls still use their existing fallback. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
