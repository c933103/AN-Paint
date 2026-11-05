# Zhuang Base64 text label, 5 November 2026

## Scope and language review

The live branch was reconciled at parent `8038faa2b8c11bb90e4f79295a319f7085612d9c`, tree `b2ab738d12c66bfb8d2ddaf6af7edd74cff53d9d`. The preceding publication was confirmed and no write was pending or uncertain. This adds missing P2 `formats22_base64_label`, preserving all 292 previous typed resources for a total of 293. Only canonical XML and this report change.

Independent review recommends `Saw Base64` with **moderate confidence for this UI context**. The [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), S18, gives `saw` a written-language/text sense as well as character/book senses, so it is not book-only. The existing catalogue already uses this vocabulary in its Base64 image-data notices. That consistency is not independent linguistic validation.

[Guangxi Minzu Bao, 6 November 2013](https://www.guangximinzubao.cn/szbzw/html/2013-11/06/content_5501.htm), found by the reviewer and directly retrieved during integration, uses `Saw` in its Zhuang title about bilingual education. It supports the broader written-language context, not Base64 terminology. The dictionary is an OCR reproduction with possible errors. No independent published Zhuang Base64 label was found during proportionate checking; no standardized computing term or native-human certification is claimed.

The exact Base64 identifier is preserved. The label refers to textual image data, not human text annotations or encryption. No encryption terminology is added. Existing `Vwnz` labels are not changed: the review did not establish that they are wrong, only that `Saw Base64` has suitable support here.

## Actual consumer

`ImageFormat.BASE64` uses this resource through its selected-locale label getter. `SaveOptionsDialog` displays those labels in its format selector. BASE64 is `text/plain` with `.txt` extension and is classified as a derived export. The existing selector filters formats according to save/export/share mode; that behavior is unchanged.

`ImageExporter` routes BASE64 to `TextImageCodec.encodeBase64`. It writes a PNG data-URI prefix, compresses the bitmap as PNG into the Base64 encoder, finalizes it and appends a newline. The representation is encoded PNG data, not a text description of the drawing. In the ordinary export flow, `ClassicPaintActivity.writeImage` does not mark the current document saved or replace its saved target; it retains the separate warning if a pending action expected a save. This label makes no claim that exporting satisfies Save.

No format filtering, encoding, file extension, MIME type, provider write or editor-state logic changes.

## Verification

Work and tests used the available temporary filesystem. No unrelated files were removed from the full main workspace.

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved, including the Base64 identifier.
- The four localization host suites plus `test_text_image_data`: **65 tests passed in 84.948 seconds**. The latter compiles and executes the production Java primitives: Base64 comparisons with the independent JDK implementation, malformed-input and size rejection, image-signature detection, and ASCII reference cases. These are host executions, not Android PNG compression or full app round trips.
- Two Java XML-to-string cases checked the English/Zhuang label for nonempty text and unchanged no-argument formatting. These are not Android resource compilation.
- Temporary token-aware Kotlin checks verified the sole label binding, selector route, derived-export classification, MIME/extension, PNG-to-Base64 data-URI route and unchanged save/export state separation.
- Base snapshot verification matched Git blobs and executable modes for **1,283 materialized files**, retaining **288** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `TextImageCodecTest.base64PngRestoresExactPixelsAndSupportsInPlaceNormalization` exercises PNG Bitmap encoding and restoration. `DerivedExportStateTest.base64ExportKeepsOriginalDrawingAndWritesRecoverableImage` exercises the derived-export application flow. These inspections are not runtime evidence. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **158/249**, P2 **64/305**, P3 **2/71**. Across 171 options, missing resources are P0 **162**, P1 **1,333**, P2 **30,065**, P3 **7,479**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, Bitmap/PNG compression, provider writes, complete app restoration, TalkBack and device layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
