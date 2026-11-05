# Zhuang unavailable image timestamp, 5 November 2026

## Scope and language review

The live review branch was reconciled at parent `79ebbad3f40b42613bd5ecf79f0a54e242d4fe6c`, tree `af9eb1d8703fe90391a5e8c7a0164b258c34409b`. No write was pending or uncertain. This fills missing P2 `ui_time_unavailable`. All 282 preceding typed resources remain unchanged; the total is 283. Only canonical XML and this report change.

Independent review recommended a short heading-plus-value rendering, “Time: unknown”. The colon distinguishes a time field with an unknown value from a statement that time itself does not know something. It avoids saying the user has no time, that the image is unavailable, or that importing failed. The source is a generic time notice, so a longer modification-time heading was unnecessary.

Evidence:

- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), directly retrieved by the reviewer: S22 supports `seizgan` for time; R18 supports `rox` for know/understand; M27 supports `mbouj` for negation.
- [Guangxi Minzu Bao, “Gou Mbouj Nyienh Dang Daih’it”, 11 October 2017](https://www.guangximinzubao.cn/szbzw/html/2017-10/11/content_23277.htm), directly retrieved by both checks, uses `Mbouj rox seiz lawz` to express not knowing when. It also uses `seizgan` in ordinary prose. This supports temporal uncertainty, not the exact UI string.

Confidence is **moderate**. The components and negative knowing expression are supported; the exact abbreviated heading/value combination is a composed recommendation, not an attested software translation or native-speaker certification. Canonical Android XML owns current wording.

## Actual consumer

The sole application binding is the image assembly thumbnail card in `AssemblyActivity.renderTray`. A known timestamp is rendered with short date and short time formatting. A null timestamp selects this complete resource and passes it to a 10sp TextView. The view has one line and end ellipsis inside a 138dp-wide card: assigning the full string does not establish that every character will be visible under all font/display settings. The card has a separate existing accessibility description, which this patch does not change.

The metadata reader initializes time as unknown, reads the provider's last-modified column, or uses `date_modified` when that column is absent/null. Values must be positive; the seconds fallback has an overflow bound before conversion to milliseconds. Missing metadata and metadata-query exceptions do not create an import timestamp or establish that the image is invalid. Import continues using the nullable time alongside the name, image dimensions and page index. No metadata, image-import, date-formatting or layout logic changes.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 9.751 seconds**.
- Two host Java XML-to-string cases check nonempty English/Zhuang labels and unchanged no-argument formatting. These are not Android resource compilation.
- Temporary token-aware Kotlin checks verify the sole resource binding, known-date versus null-notice routing, complete text assignment, one-line ellipsis, optional provider metadata and absence of a non-null timestamp requirement for import. These are static checks, not provider or Android execution.
- Base snapshot verification matched Git blobs and executable modes for **1,294 materialized files**, retaining **269** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `AssemblyModelTest.sortByNameOrRealModificationTimeDoesNotChangePlacementAndUnknownTimesStayLast` includes an image with unknown time and checks ordering/placement, not this notice. `AssemblyActivityTest`'s load fixture supplies null times after its first three records; its capacity test imports such fixtures, but does not assert the notice. Neither inspection establishes runtime rendering, invalid-value handling or layout for this patch. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **154/249**, P2 **60/305**, P3 **0/71**. Across 171 options, missing resources are P0 **162**, P1 **1,337**, P2 **30,069**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, actual missing/invalid provider metadata, date rendering, TalkBack and tray layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
