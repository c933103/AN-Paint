# Zhuang Android decoding-failure notice, 5 November 2026

## Scope and review

The live branch was reconciled at parent `92be9ac1181897bd400fb447260028f5fe69f072`, tree `ef1a42996cf82022ccbb2d233332511cb59f4769`; no operation was pending. This fills missing P1 `ui_android_could_not_decode_this_image`. All 263 preceding typed resources remain unchanged; the total is 264. Only canonical XML and this report change.

Independent wording/context review accepted the plain-language paraphrase “Android cannot produce an image from this data.” It preserves decoding direction, data to image, without asserting corruption, permission failure, unsupported format or an encoding/save operation. Review moved the source phrase before the verb rather than retaining English-influenced post-object placement. The alternative read/open paraphrase was rejected as less precise about decoding.

Supporting sources:

- [Guangxi Minzu Bao's paper-making article, 17 September 2020](https://www.guangximinzubao.cn/zw/y/383151.html), uses `daj faexcuk bienqbaenz ceij`, bamboo becoming paper, supporting a source phrase before transformation.
- [Aen Cungmeng Daxboh, 17 January 2024](https://www.guangximinzubao.cn/szbzw/html/2024-01/17/content_49035.htm), attests `guh mbouj ndaej hongnaek`, inability to do heavy work, supporting the potential-negative construction.
- [The language commission's terminology announcement, 3 September 2025](https://www.guangximinzubao.cn/szbzw/html/2025-09/03/content_54472.htm), item 102, supports the data sense of `soqgawq`.

These sources support components and construction, not the complete software sentence. Confidence is high on contextual meaning and **moderate on idiomatic Zhuang composition**. No established decoding term, native-user approval or complete-language acceptance is claimed. Canonical XML owns the full wording.

## Actual consumer

`ImportedImage.decode` in `ImageImport.kt` has the sole direct binding. After memory admission and separate JXL/HEIF/TIFF/PDF/ICO dispatch, the platform path calls `BitmapFactory.decodeFile` through the existing file/colour wrappers. A null result throws the complete selected notice before colour conversion, bitmap transformation or returning output. Other exceptions and memory errors retain their existing handling.

The decoder is used by editor image loading, import previews and assembly thumbnails. The message identifies the platform's failure to obtain a decoded bitmap; it does not prove an underlying cause. No decoder, cleanup, memory policy or caller implementation changes.

## Executed checks

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, literal tokens and escaping remain intact.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 9.589 seconds**.
- Two host Java XML-to-string cases preserve the exact Android name and the complete no-argument English/Zhuang notice.
- Temporary token-aware Kotlin checks verify the null-result binding, preceding memory/special-codec handling, sequencing before colour conversion/transform, callers and existing bitmap cleanup. They do not inject a null Android decoder result.
- Base snapshot verification matched Git blobs and executable modes for **1,281 materialized files**, retaining **269** unmaterialized entries. Publication checks the complete path/mode/type/blob overlay, fresh expected-parent non-force lease and exact remote bytes.

`ImportMemoryIntegrationTest.pngKeepsSampledEstimatesAndDecodesWithoutLoadingANativeCodec` was inspected, not run. It covers a successful sampled PNG path, not this failure branch. No permanent per-edit wording mirror or test package is added.

## Coverage and limits

Zhuang presence is P0 **69/94**, P1 **141/249**, P2 **54/305**, P3 **0/71**. Global missing resources across 171 options are P0 **162**, P1 **1,350**, P2 **30,075**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence does not establish fluency or runtime acceptance.

Android compilation, Robolectric, decoder failure injection, error display, TalkBack and layout were not executed. Exact-head Actions state is checked after publication and reported separately; this review branch does not normally trigger CI. No merge, release or CI-pass claim is made.
