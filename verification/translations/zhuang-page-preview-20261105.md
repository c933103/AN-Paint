# Zhuang selected-page preview label, 5 November 2026

## Scope and language review

The review branch was freshly reconciled at parent `3561bee0d7c229ea14801c7c915cea3bd939a84b`, tree `813d1128fbd8241d66b7031dc905b0b8d6768fe6`. The preceding publication was confirmed and no write was pending or uncertain. This adds missing P2 `formats22_page_preview`, preserving all 290 previous typed resources for a total of 291. Only canonical XML and this report change.

The label identifies the preview of the selected page. Independent review accepted the proposed phrase as concise and project-consistent, with **moderate confidence** in the selected-page expression and **low confidence** in the independently unverified technical preview idiom. No demonstrated semantic defect was found, but this is not authoritative terminology or full linguistic certification.

Evidence and limits:

- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), independently retrieved by the reviewer, supports the component meanings: `mbaw` sheet classifier (M21), `senj` select (S24), `sien` first/before (S29), and `yawj` look (Y11). This does not establish the whole phrase or a preferred digital-page term.
- A [People's Daily Zhuang constitutional translation](https://sawcuengh.people.com.cn/158004/15719369.html) has selected-representative constructions ending in `senj ok haenx`, supporting a following modifier/demonstrative pattern. This was search-index evidence only; direct opening timed out during review.
- The existing catalogue uses `Yawj sien` for preview and `mbaw` in the page-navigation controls. These are project conventions, not independent validation. [IBM Zhuang safety information](https://www.ibm.com/docs/en/systems-hardware/linuxone/9176-ML2?topic=notices-safety-information) uses the ordinary sequence `Sien yawj` for first read/look. That does not prove the project's technical compound wrong or establish a replacement, so existing preview wording is preserved.

A separate settings-label candidate was investigated and left unchanged: the tentative settings word lacked sufficient lexical or primary-use support. This report makes no settings-translation progress claim. No native-human certification is claimed or treated as a prerequisite.

## Actual consumer

`ImportSelection.showPages` assigns the selected-locale resource to the content description of its preview ImageView. The page chooser is reached for **PDF and TIFF**, not ICO. This label identifies a preview region; it is neither a command nor an announcement that a preview has loaded.

Each update clears and releases the old bitmap before validating input or starting a preview. The page field is one-based and the imported page index is zero-based. Generation/lifecycle guards prevent stale results from replacing the current preview. Loading, successful dimensions, invalid input and unavailable-preview errors use separate existing status resources. The static content description persists in those states, including when no preview bitmap is present. The translation adds no page number, successful-load claim or promise to import.

No rendering, validation, selection, loading, cleanup or accessibility logic changes. The remaining chooser text is outside this one-label batch and is not claimed as fully localized.

## Verification

Work and tests used the available temporary filesystem. No unrelated files were removed from the full main workspace.

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 10.972 seconds**.
- Two host Java XML-to-string cases checked the English/Zhuang label for nonempty text and unchanged no-argument formatting. These are not Android resource compilation.
- Temporary token-aware Kotlin checks verified the sole binding, PDF/TIFF route, old-preview clearing, validation/loading order, generation/lifecycle rejection and separate success/error status resources. These are static checks, not asynchronous preview execution.
- Base snapshot verification matched Git blobs and executable modes for **1,281 materialized files**, retaining **288** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `LocaleNumberInputTest.pageFieldRetainsPersianDigitsAndDisablesFractionalNegativeAndOutOfRangeEntries` opens the real TIFF page form, checks invalid/valid page entry and cancellation without staging or decoding a document. It does not assert the translated preview content description or preview loading. Inspection is not runtime evidence. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **158/249**, P2 **62/305**, P3 **2/71**. Across 171 options, missing resources are P0 **162**, P1 **1,333**, P2 **30,067**, P3 **7,479**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, preview decoding, rapid navigation, lifecycle interruption, TalkBack and device layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
