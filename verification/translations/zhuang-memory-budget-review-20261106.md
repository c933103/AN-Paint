# Zhuang export memory budget and neighboring warning review

Date: 2026-11-06 UTC. Base `de5d1559f46b31f48561020c029662583d07e965`, tree `95fd0480bc9092729735d30a11a926c8bac79680`.

## Change and review outcome

Added missing P0 `save20_encoding_budget` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. It describes the image plus the data used to create the output needing more RAM than AN Paint permits. It does not confuse an application working allowance with total installed RAM, disk space, output file size or image corruption. All 313 preceding resource nodes, attributes and original prefix bytes remain unchanged.

Independent review accepted this functional paraphrase with high consumer-semantic confidence and moderate full-sentence linguistic confidence. “Encoding buffers” is explained through the encoding work rather than presented as an established Zhuang technical compound. `yaek yungh` describes prospective memory use, not a claim that an oversized allocation already happened. Native-speaker or software-usability certification is neither claimed nor imposed as an approval gate.

A bounded complete-value review also retained two existing resources:
- `ui_not_enough_memory_to_save_in_this_format`: the actual `OutOfMemoryError` save notice remains distinct from a budget rejection. Its PNG instruction is slightly stronger than English “Try PNG,” but does not promise success.
- `ui_there_is_not_enough_memory_for_this_operation`: retains insufficient memory at original dimensions and no automatic resizing. Original dimensions is a defensible rendering of resolution in this pixel-dimension context. Its generic edit-error consumer is separate from `ImageSizeException` admission failures. This review does not certify every edit operation's failure atomicity.

These three values are the entire language-review cohort. Other translated warnings and English fallbacks are not cleared by association. The all-string release review remains incomplete.

## Evidence

- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): supports file/document, storage, permission, dimensions, original, enough and selection vocabulary. `hawj` permission is at H.htm 22/45; `yaek` prospective action at Y.htm 4/31; `yungh` use at Y.htm 29/31. The OCR warns of incomplete proofreading. Components do not establish whole-sentence idiomaticity.
- [Guangxi language commission's ninth terminology announcement, item 102](https://www.guangximinzubao.cn/szbzw/html/2025-09/03/content_54472.htm) supports `soqgawq` for data within a standardized compound. Directly retrieved during both reviews.
- [Guangxi Minzu Bao digital-document article, 6 November 2024](https://www.guangximinzubao.cn/szbzw/html/2024-11/06/content_51822.htm) uses `yungh daeuj` in a technical software context. Directly retrieved during both reviews.
- The independent review additionally checked [numerical `lai gvaq` usage](https://www.guangximinzubao.cn/szbzw/html/2022-08/10/content_44648.htm). No source is claimed to attest this exact warning or a standardized encoding-buffer term.

## Production consumers

`ClassicPaintActivity.writeImage` passes `ImageMemoryPolicy.forDevice(...).workingBytes` through `ImageExporter`. The policy deliberately reserves memory and limits process/system shares; it is not total device RAM.

Four resource bindings cover six formats:
- `LegacyImageEncoder.check` accounts for source pixels plus scratch work for BMP, GIF and DIB. `BitmapFileCodec` and `DibCodec` map its budget failure to this string, while retaining separate format-size errors.
- `IcoCodec.encode` compares bitmap allocation plus icon work and reserve before creating its temporary output.
- `TextImageCodec.requireBudget` is called by Base64 and ASCII export with bitmap allocation plus row/scaled-image work and reserve, before output replacement.

Other codecs retain their own errors. The new warning is not a universal encoder catch-all. The existing format-memory notice is selected by `writeImage` on actual `OutOfMemoryError`; `editFailed` uses the original-dimensions notice on an editing `OutOfMemoryError`, after separately handling `ImageSizeException`.

## Verification

- Fresh remote review head reconciled with the previous publication. Develop remained `412aab0c604060fb66fbd2edc6bb05572d10b56d`; no develop or separate Navajo-branch changes. All 1,587 base file contents and executable modes matched the reviewed checkout.
- One unique missing scalar added; source attributes, placeholders, literal tokens, numeric and newline boundaries, XML/Android escaping and previous values preserved. All 171 offered catalogues and priority manifest pass structural validation. XML blob `dacc8fc02182ec8faa3dffae3db3eae2966d9b5c`, 30,950 UTF-8 bytes.
- 61 relevant host tests passed in 6.255 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- The existing production Java encoder bounds test passed in 0.833 seconds: `test_legacy_image_encoder.LegacyEncoderTest.test_gif_dimensions_and_both_memory_budgets_before_reading`. It exercises actual GIF/BMP budget rejection before source-row reads, plus invalid GIF dimensions. This is not Kotlin or Android execution.
- Six host Java format checks passed: English and Zhuang for the three reviewed static resources. Static source checks verified all six resource bindings, budget routing, failure distinctions and text/icon rejection before output creation. `git diff --check` passed.
- Existing `TextImageCodecTest.rejectedExportsPreserveExistingFile`, `IcoCodecTest.rejectedBudgetsAndSizesPreserveDestinationAndSourceWithoutLeakingTemporaryFiles` and the bounded encoder assertions in `SerbianP0WordingTest` were inspected, not executed.

Zhuang has 314 typed resources: P0 73/94, P1 158/249, P2 80/305, P3 3/71. Global missing counts over 171 offered options are 158/1,333/30,049/7,478 for P0–P3; 46 options have complete presence. These are presence counts, not fluency, full-review or release completion.

No Android SDK or Kotlin compiler is configured here. Android build/AAPT, localized runtime errors, device layout, accessibility, glyph rendering and device memory behavior were not run. No merge or release is claimed. Only canonical XML and this compact report change; temporary checks and wording mirrors are not published. The existing conditional P0/P1 completion and all-translated-string review release plan remains in force.
