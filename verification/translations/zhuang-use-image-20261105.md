# Zhuang gallery image-use action, 5 November 2026

## Scope

The live review branch was reconciled at parent `e3334f1e5877e2f34b4333e619c41180780f92b1`, tree `335562dea8c7f377e7ff3be66766053a025be4bd`. No prior write was pending. This addition fills the missing P2 `gallery_use_image` scalar (“Use image”) in canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 249 preceding typed resources are preserved; there are now 250. Only that XML and this report change. Other catalogue, application, provider, licence and fallback behavior is untouched.

## Wording and independent review

The [digitized Zhuang–Chinese dictionary](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), main Y section, page 29, supports `yungh` as use/utilize/application. The [Guangxi Minzu Bao bilingual story Hoenz Fwen, 27 December 2017](https://www.guangximinzubao.cn/szbzw/html/2017-12/27/content_24064.htm), bronze-box description at extracted line 30, uses `dozsiengq` for depicted images/figures. This is evidence for the image noun, not a digital-interface phrase. The exact compound was not found in the dictionary OCR and is not attributed to it.

An independent linguistic/context review accepted the straightforward verb-object construction, consistent with the existing image noun and Use colour label, and confirmed that the action selects an image for insertion. It does not imply approval of the image's licence. The translation is compositionally supported; no claim of fixed software-term attestation, native-user testing or complete linguistic acceptance is made. Canonical XML remains the sole current wording source.

## Actual consumer path

- `MediaGalleryActivity.kt:199` passes the complete selected resource to `IllustrationPage.script` when an allowed provider page finishes loading.
- `IllustrationPage.kt` routes Catrobat to `GalleryPage.script`, Commons to its original-download-link adapter, and Irasutoya/Openclipart to their artwork-detail adapters. Labels enter the generated scripts via `JSONObject.quote` and are assigned through `textContent`, not interpreted as HTML.
- Catrobat's existing download action also receives an explicit `aria-label`. Other provider actions receive visible anchor text; this is not a claim that those paths set the same explicit attribute.
- The image action uses the insertion URI scheme, distinct from Copy credit. Native URL routing checks the source and appropriate artwork page before calling `insert`. Its busy/finishing/destroyed and allowed-image/artwork-page guards remain intact before download.
- Repeated DOM adaptation reuses app controls. This source change does not perform an image download, insert artwork into a user's document, accept terms, or alter provider artwork names/prose.

## Executed verification

- XML/source-attribute, ordered format-argument, literal-token, escaping and old-resource preservation checks passed. All 171 offered-option catalogue checks and the importance manifest validated.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts test_gallery_translation_data test_gallery_typography`: **64 tests passed in 9.595 seconds**, with no skips. The three additional existing host tests execute Node-based label-data and DOM-typography checks, including arbitrary display text, repeated adaptation and scoped styling.
- Host Java parsed the English and integrated Zhuang XML and formatted this literal label without arguments: **2 cases passed**. This does not execute Android resource resolution.
- Temporary token-aware checks verified the direct resource binding, provider routing and native guards. A temporary run of the existing minimal-DOM harness with the actual current resource checked **all four providers**: complete action text, unchanged copy-action text, insertion URI identity, Catrobat aria-label and repeated adaptation without duplicate controls. Extracted scripts used JSON-equivalent substitution; Android `JSONObject`, WebView and publisher sites were not executed.
- Base snapshot verification covered **1,272 materialized files**, each with matching Git blob identity and executable mode. **269** unmaterialized non-tree entries remain retained. Publication compares every final path/mode/type/blob against the exact overlay, uses a fresh expected-parent non-force lease, and verifies final remote file bytes.

Existing `GalleryImportTest` cases for image import with credit, cancellation during download, other-provider import and invalid-source rejection were inspected, not run. No permanent per-edit wording mirrors or test packages were added.

## Coverage and remaining limits

Zhuang presence is P0 **69/94**, P1 **133/249**, P2 **48/305**, P3 **0/71**. Global missing typed resources across 171 options are P0 **162**, P1 **1,358**, P2 **30,081**, P3 **7,481**; 46 options have complete resource presence. The bounded scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android compilation, Robolectric, live WebView/site behavior, layout, glyphs, TalkBack and network/import execution were not run. Minimal-DOM Node checks cannot establish those outcomes. Exact-head Actions state is checked after publication and reported separately; this review-branch push does not ordinarily trigger CI. No merge, release, CI-pass or complete-language claim is made.
