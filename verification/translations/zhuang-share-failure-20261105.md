# Zhuang: saved-image sharing failure

Date: 2026-11-05 (UTC). Review-branch base: `b6b7a1749784f7d9ce3c435b5d143ac9d2bbcfa6`, tree `98d85dc4976e68fba1fb334fd42aee871d75192e`.

## Change and meaning

Added two missing strings in the canonical `Paintroid/src/main/res/values-b+za/strings.xml`: the P0 notice that the image was saved but Android could not open sharing, and the P2 AN Paint image payload label. The existing 196 typed resources are unchanged. The notice retains the successful save, contrasting failure to open the sharing flow, and the complete `%1$s` diagnostic. The label identifies an AN Paint image. Canonical XML, rather than this report, owns the exact wording.

Independent wording and context review found no concrete semantic error and retained both compositions. Confidence is moderate: `rom` has a storage sense, but its digital-save use is not independently attested here; `hai … gij faenyiengj` combines opening with a nominal sharing expression, but this software collocation is not independently attested. This is not a claim of certified idiomaticity or standardized Android terminology. Native-human approval is not treated as a gate.

## Sources checked

- [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `rom` includes accumulation/storage (R.htm 26/33), `hai` opening/starting (H.htm 15/45), `hoeng` contrast (H.htm 35/45), `faenyiengj` sharing (F.htm 5/29), and nominal/classifier `gij` (G.htm 37/110). The source warns of incomplete proofreading; component meanings do not certify a complete UI phrase.
- [Guangxi Minzu Bao, 17 July 2024](https://www.guangximinzubao.cn/szbzw/html/2024-07/17/content_50661.htm): the article's analysis, sections III.1 and III.2, discusses the sharing sense and head-before-modifier structure. The body was directly checked after an initially incomplete extraction. No lyrics are reproduced.
- [Guangxi Minzu Bao, 27 December 2017](https://www.guangximinzubao.cn/szbzw/html/2017-12/27/content_24064.htm): parallel prose supports `dozsiengq` for depicted images/figures, not a software-specific collocation.

## Actual consumer boundary

`ClassicPaintActivity.writeImage` completes the destination output-stream write before its UI success callback attempts sharing. Normal save state changes (`savedTarget`, filename, `markSaved`, autosave scheduling) are conditional on not exporting; the saved toast precedes sharing. Its outer save-failure path uses a different resource.

`shareSavedImage` obtains a FileProvider URI, prepares ACTION_SEND/EXTRA_STREAM, assigns `ui_an_paint_image` as the **ClipData description**, grants URI-read intent permission, and launches a chooser. The label is not the chooser title. Its broad exception handler includes URI/intent/ClipData preparation and launch, not just a missing receiving app. It formats the P0 notice with `error.message` and passes the whole result to the dialog. Both resource keys have one actual `R.string` binding here. The notice does not assert delivery to another app or undo the completed save.

## Verification

- Fresh base tree reconciled before editing. All 1,252 materialized files matched base Git blob hashes and executable modes; 265 unmaterialized entries remain retained, for 1,517 base non-tree entries.
- All 196 previous typed resources/attributes and their original prefix bytes preserved; two missing entries added. XML parses, Android escapes, source attributes, ordered typed placeholders, newlines, numerals and required literal tokens pass. New XML Git blob: `ac8c92edec8085e338f799b9795e7d131df5d52f` (18,060 bytes).
- All 171 offered catalogues and the priority manifest pass their structural checks.
- **61 host tests passed** in 7.696 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **14 host Java format/render cases passed** across English and Zhuang: the single diagnostic slot, null, empty, ASCII, percent-bearing text resembling a format argument, Unicode/emoji, embedded newline, and the literal payload label. Diagnostic text is not reinterpreted as a format string.
- Targeted static consumer checks passed for write-before-share ordering, export-vs-normal-save state, saved toast, payload-label role, broad preparation/launch catch, complete diagnostic argument, and whole-message delivery. Source tracing also checked `UiText`/`LocaleText` resolution; Android resource execution was not performed.

Zhuang now has **198 typed resources**: P0 **69/94**, P1 **125/249**, P2 **4/305**, P3 **0/71**. Across all 171 offered options, missing-entry counts are P0 162, P1 1,366, P2 30,125 and P3 7,481; 46 options have complete entry presence. These counts are not linguistic acceptance or runtime coverage. The current scope remains 59 scoped catalogues plus 112 outside-scope explicit-English-fallback catalogues.

## Limits

No Android build/AAPT, executed device saving, provider-close/durability, URI-permission, chooser, receiving-app delivery, lifecycle, layout/accessibility or font tests were run. The host checks do not establish those properties. No merge, release or deployment is claimed. Only the canonical locale XML and this concise evidence report are intended to change; temporary test harnesses and sentence mirrors are not added to the repository.
