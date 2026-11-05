# Zhuang PDF page-count limit, 5 November 2026

## Scope and wording

The live review branch was reconciled at parent `805ef6b8cc55679083eb9de6d5979051086cab60`, tree `c184eb45df41bcb421a2c60aabef8a264d839d17`. No write was pending or uncertain. This fills missing P2 `formats22_pdf_page_count`. All 276 preceding typed resources remain unchanged; the total is 277. Only canonical XML and this report change.

Independent review recommended the draft unchanged, backtranslated as “The PDF must have from 1 to %1$d pages.” The range describes the total number of pages, not the number of a selected page. `PDF`, the lower bound `1` and typed integer argument `%1$d` are preserved.

Sources and limits:

- [Guangxi Minzu Bao spelling guidance, 15 May 2019](https://www.guangximinzubao.cn/sy/jxzw/377556.html), abbreviation section, explicitly identifies `mbaw 78` as page 78. This supports the page sense, not the complete count sentence.
- [“Dauqngeix Gij Ndwenngoenz Doihengz Sawcuengh”, 27 December 2017](https://www.guangximinzubao.cn/szbzw/html/2017-12/27/content_24073.htm), uses `Daj 1980 nienz daengz 1989 nienz`, supporting the from-to construction. Applying that construction to a page-count range remains compositional.
- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): review directly retrieved the `ajaeu` cross-reference to `yaekaeu` for “must” and a numeral-before-`mbaw` introduction example. Earlier direct readings support `yaekaeu` (Y4), `daj` from (D5), `daengz` to/reach (D18), and `mbaw` sheet (M21). Attempts to re-retrieve these entries during this batch timed out; fresh independent verification of every lexical gloss is not claimed. The section-page references are the OCR's internal pagination, and its transcription is not fully proofread.

Confidence is **moderate for the complete phrasing and high for its match to the intended constraint**. No attested complete PDF warning, official technical terminology or native-human certification is claimed. Canonical XML owns the wording.

## Actual consumer

`PdfCodec.checkedPageCount` is the sole direct binding. It reads `PdfRenderer.pageCount` and throws the localized `PdfImportException` when the result is outside the inclusive interval `1..MAX_PAGES`. `MAX_PAGES` is currently 4096 and is passed as the integer formatting argument. Both endpoints are allowed by this guard; zero and counts above 4096 are rejected.

Both public `pageCount` and `withPage` use that guard. `withPage` separately validates the zero-based selected-page index before `openPage`. Renderer/page cleanup and preservation of specific `PdfImportException` messages remain unchanged. The warning is an application admission limit, not a claim that every admitted PDF is otherwise valid or renderable. No PDF implementation, memory or limit changes.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 11.095 seconds**.
- Eight host Java formatting cases cover English/Zhuang integer arguments 1, 4096 and 2147483647, fixed lower-bound/PDF literals, and rejection of a string supplied for the integer argument. Large synthetic arguments test formatting only, not admissible PDF limits or Android compilation.
- Temporary token-aware Kotlin checks verify the inclusive count predicate, actual maximum argument, both count-check routes, the separate selected-page-index guard, specific exception retention and cleanup statements. These are static checks, not execution of Android's PDF parser.
- Base snapshot verification matched Git blobs and executable modes for **1,290 materialized files**, retaining **269** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

The inspected device test `PdfCodecTest.generatedMultipageDocumentUsesSelectedPageAnd144DpiDimensions` checks a generated two-page PDF's count, dimensions and rendering. It was not run and is not a 0/4096/4097 boundary test. No page-count boundary execution is claimed. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **153/249**, P2 **55/305**, P3 **0/71**. Across 171 options, missing resources are P0 **162**, P1 **1,338**, P2 **30,074**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, device/Robolectric tests, PDF parsing, exception routing, descriptor cleanup, TalkBack and warning layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
