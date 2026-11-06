# Zhuang assembly view-fit status, 6 November 2026

Parent `2e47808e791c19143d8335a9370cee469f36d5da`, tree `e82c39438d6c71862666e55e6916d8902034b339`, was reconciled with no pending write. Adds missing P3 `ui_shows_the_whole_assembly_image_and_output_sizes`, preserving all 309 previous typed resources for 310 total. Only canonical XML and this report change.

## Concurrency and scope

Develop was checked at `412aab0c604060fb66fbd2edc6bb05572d10b56d`, which merges [PR #295](https://github.com/c933103/AN-Paint/pull/295). The compare has two develop-only commits and 312 review-only commits from merge base `1f763dbd25e93ad13285041e3d2bcb5051a40241`; the develop-side change is the nine-locale batch. Its three Zhuang diagnostic additions already match this branch exactly. Develop has 93 Zhuang entries, with two pre-existing height values differing from this branch (`Gau` versus `Sang`); those are untouched. This batch neither merges/rebases develop nor updates another branch, PR, catalogue or engineering work. Both live heads were checked again before publication.

## Language and consumer review

Independent review recommends explicitly repeating the dimensions phrase for both image and output dimensions. This prevents a less precise reading that the output image itself, rather than its size, is unchanged. The first sentence uses the established view-whole construction and assembly term. The output image term follows the current output-size dialog; the full sentence is a composed translation, not an independently attested software sentence.

- Directly retrieved [Guangxi Minzu Bao, 6 July 2016](https://www.guangximinzubao.cn/szbzw/html/2016-07/06/content_18142.htm), line 27, has `Yawj daengx mbanj dacaengz`, supporting view + whole + noun. The source is literary rather than a UI terminology standard.
- Directly retrieved [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), line 177, gives `bienq` the change/transform sense. OCR quality and homonymous senses do not certify the whole sentence.

Confidence is high on code meaning and the explicit-size correction, moderate on complete Zhuang fluency. No native software-usability certification is claimed or required as a publication gate. Canonical Android XML owns the wording.

`AssemblyActivity` has the only direct resource binding: after the Show all button calls `board.fit()`, it assigns the complete selected resource to the status TextView. `AssemblyCanvas.fit` reads placed-image layout plus possible attachment targets, computes zoom and pan, and redraws. It does not change image dimensions, crop, normalization, placement or model/output dimensions. An unmeasured/zero-size viewport returns early. The message is therefore a view-fit explanation, not a promise that files were saved or image pixels resized.

The existing status allows one line in compact mode or two otherwise, with end ellipsis. The clearer translation is longer than the first draft; clipping at narrow widths or large font scales remains possible and was not measured. This batch does not change layout or fit behavior.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, formatting, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 7.300 seconds**.
- Two English/Zhuang Java XML-to-string cases passed for nonempty text and unchanged no-argument formatting. This is not Android compilation.
- Temporary token-aware source checks passed for the unique status binding after fit, layout/target bounds, view-only zoom/pan changes, model-derived output size and the actual one/two-line ellipsis policy. These are static checks, not execution of the fit operation or status rendering.
- All **1,582 base tracked blobs and executable modes** were verified before editing; `git diff --check` passed. Publication checks the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

The existing `AssemblyActivityTest.sameWidthAndHeightOfferPercentPreserveRatiosAndUndoWithoutChangingSources` was inspected, not run. Its final Show all assertion checks unchanged assembly dimensions. No permanent per-edit wording test or mirror is added.

Zhuang presence: P0 **69/94**, P1 **158/249**, P2 **80/305**, P3 **3/71**. Global missing counts over 171 options: **162 / 1,333 / 30,049 / 7,478** for P0–P3; 46 options have complete presence. Scope stays 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence does not certify fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, actual fit execution, TalkBack and device/font-scale layout were not run. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
