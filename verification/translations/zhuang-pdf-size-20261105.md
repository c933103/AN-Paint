# Zhuang PDF file-size requirement, 5 November 2026

## Scope and review

The live branch was reconciled at parent `05a4b7add5c11babcbc3ec20f88e2192aeff81b4`, tree `f830d1f516959a9c689fc344072a5948fb98a2a7`; no previous operation was pending. This adds missing P2 `formats22_pdf_file_size`. All 260 preceding typed resources remain unchanged; the total is 261. Only canonical XML and this report change.

Independent wording/context review accepted the sentence meaning “The PDF file must contain data and be no larger than 512 MiB.” The file subject and data term make this a reasonable nonzero-file-length paraphrase. It does not require visible text or nonblank pages. Review confidence is high on the required semantics and inclusive upper limit, **moderate on natural Zhuang composition**. The complete UI sentence is not directly attested, and no native-user acceptance is claimed.

Lexical evidence was checked separately: the [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), main Y4, lists `yaekaeu` as must. The [Guangxi language commission's terminology announcement of 3 September 2025](https://www.guangximinzubao.cn/szbzw/html/2025-09/03/content_54472.htm), item 102, uses `soqgawq` as the data component of “data annotation base.” That official terminology supports the data sense, not an exact synonym for an empty/nonempty file. Existing file and comparison vocabulary is retained for consistency. The dictionary is OCR, not an error-free edition. Canonical XML owns the complete wording.

## Actual consumer and boundary

`PdfCodec` uses this full selected resource in two guards:

- `workingBytes` rejects file length at or below zero or above `512L * 1024 * 1024` before calculating document/rendering memory.
- `withRenderer` rejects lengths outside `1..MAX_FILE_BYTES`, before separate PDF-header validation and opening the renderer.

The size interval is therefore **1 through 536,870,912 bytes, inclusive**. It is not a page-count, page-content, pixel or memory-budget requirement. Passing it does not prove the PDF is valid or importable: header, renderer, page, dimensions and memory checks remain separate. Page counting, dimensions and decoding route through these existing checks. No implementation or error-routing changes.

## Executed checks

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, source numerals, literal tokens and escaping remain intact.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 9.852 seconds**.
- Host Java parsed English and integrated Zhuang XML: **two cases passed**, preserving `PDF`, the single exact `512 MiB` token and the complete no-argument string.
- Temporary token-aware source checks verified both actual length guards, the inclusive maximum, sequencing before header validation/renderer opening and separation from memory calculations. These are static checks, not executed PDF boundary tests.
- Base snapshot verification matched Git blob identity and executable mode for **1,279 materialized files**, retaining **269** unmaterialized non-tree entries. Publication checks the complete path/mode/type/blob overlay, fresh expected-parent non-force lease and exact remote bytes.

`JapanesePdfFailureTest.encryptionAndFileSizeErrorsKeepTheirSpecificJapaneseMessages` was inspected, not run. It tests the actual empty-file failure route for Japanese, not Zhuang or the upper-size boundary. No permanent per-edit wording mirror or test package is added.

## Coverage and limits

Zhuang presence is P0 **69/94**, P1 **139/249**, P2 **53/305**, P3 **0/71**. Global missing typed resources across 171 options are P0 **162**, P1 **1,352**, P2 **30,076**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues plus 112 outside-scope catalogues with explicit English fallback. Presence does not establish fluency or runtime acceptance.

Android compilation, Robolectric, actual empty/large-file PDF execution, error display, TalkBack and device layout were not run. Exact-head Actions state is checked after publication and reported separately; this review branch does not normally trigger CI. No merge, release or CI-pass claim is made.
