# Zhuang unsupported-image notices, 5 November 2026

## Scope and review

The live branch was reconciled at parent `f586cb934ed588ffe989e830bd1b5058d7f81c3a`, tree `2615e8513d3dd7cb16c55648191e07a458aa1bee`; no operation was pending. This fills P1 `ui_this_file_is_not_a_supported_image_use` and P2 `formats22_text_not_image`. All 261 preceding typed resources remain unchanged; the total is 263. Only canonical XML and this report change.

Independent linguistic/context review accepted both operational paraphrases: an image that AN Paint can open. The Base64 notice says the text contains no such image; the general notice identifies the file as not such an image and preserves the full source format guidance. Neither attributes the failure to malformed Base64 syntax, corruption, permissions, user fault or replacement failure. All format names and their order are unchanged, including JPEG XL and Base64.

The [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) supports writing/text senses for `saw`, related word/character senses for `cih`, and general support for `cihciz`. The general support gloss does not independently establish software compatibility usage, so the concrete opening-capability paraphrase is retained. Direct dictionary fetching timed out during this batch; indexed dictionary evidence and existing lexical/context checks were used rather than claiming a successful new full-page fetch.

[NCCU-hosted Zhuang teaching material, Lesson 3, page 2](https://newdoc.nccu.edu.tw/teasyllabus/113721209100/Lesson%203.pdf) explains head-plus-modifier order and postposed demonstratives. It supports the general construction, not these exact software sentences or a full relative-clause analysis. Existing file/image/opening vocabulary and descriptive clauses provide consistency only. The final Base64 image-text noun phrase remains compositional, with **moderate confidence in idiomatic polish**, not direct phrase attestation or native-user approval. Canonical XML owns the complete wording.

## Actual consumers

`TextImageCodec.decodeToFile` decodes into a temporary file, then reads a small header and throws the complete selected Base64 notice if no bytes are read or `TextImageData.imageSignature` does not recognize an image. The empty check is defensive: the normal data decoder already rejects zero decoded bytes as malformed. Syntax and byte-limit failures remain separate errors. Successful signature recognition is not a promise that full decoding will succeed.

`replace` calls the writer before renaming the temporary file over the destination and deletes temporary output in `finally`. Consequently, a signature error occurs before replacement. `ImportFiles.normalize` uses this path for recognized text-image input. No decode, replacement or cleanup implementation changes.

`ImportedImage` in `ImageImport.kt` supplies the general notice after the appropriate format/dimension inspection if decoded bounds are nonpositive. The full list is guidance inherited from the source, not a new guarantee that every file or every Base64/format combination is accepted.

## Executed verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing-node identity, source attributes, escaping and literal/format identifiers remain intact.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts test_text_image_data`: **65 tests passed in 19.353 seconds**.
- Four of those tests compile and execute the actual Android-independent `TextImageData.java`. They cover independent Base64 round trips, malformed padding/alphabet/URI and byte limits, signature detection including encoded prose/MP4 rejection and AVIF recognition, plus ASCII rendering primitives. These are executed host Java checks, not Android codec tests.
- Four additional XML-to-string Java cases preserve the complete English/Zhuang notices and ordered format identifiers under no-argument formatting.
- Temporary token-aware checks inspect both real Kotlin bindings, decode-before-signature sequencing, write-before-rename and cleanup, nonpositive bounds and normalization routing.
- Base snapshot verification matched Git blobs and executable modes for **1,280 materialized files**, retaining **269** unmaterialized entries. Publication checks the complete path/mode/type/blob overlay, fresh expected-parent non-force lease and exact remote bytes.

`TextImageCodecTest.invalidPayloadAndSizeLimitKeepOriginalDestinationAndCleanTemporaryFiles` was inspected, not run. It exercises nonimage decoded text, invalid Base64 and byte-limit failures while preserving the existing destination. No permanent per-edit wording mirror or duplicate test package is added.

## Coverage and limits

Zhuang presence is P0 **69/94**, P1 **140/249**, P2 **54/305**, P3 **0/71**. Global missing resources across 171 options are P0 **162**, P1 **1,351**, P2 **30,075**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence does not establish fluency or runtime acceptance.

Android compilation, Robolectric, full image-decoder/error display and file-replacement lifecycle, TalkBack and layout were not executed. Exact-head Actions state is checked after publication and reported separately; this review branch does not normally trigger CI. No merge, release or CI-pass claim is made.
