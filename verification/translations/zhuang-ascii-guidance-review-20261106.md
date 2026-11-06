# Zhuang ASCII export guidance and width review, 6 November 2026

## Scope and review outcome

Base is `04c1ecfd044c78d8f1732ce0ee90a19bfda95e59` on `review/nv-bottom-2038-20261103`, tree `174dcd157f9750cd5cf93b9756ff42e0ba3dab28`. The preceding share-guidance publication was reconciled with no pending or uncertain write. Develop remained `412aab0c604060fb66fbd2edc6bb05572d10b56d`; no develop integration or separate Navajo work is changed.

This adds missing P0 `formats22_ascii_description`. All 317 existing typed resources are preserved, bringing the catalogue to 318. Only canonical Zhuang XML and this compact report change. The conditional release and complete translated-string review remain governed by [the durable plan](p0-p1-release-plan-20261106.md); this is one bounded cohort, not a completed locale review.

Independent review rejected the initial description's nested character-kind/font construction and cumbersome appearance/image noun stack. The revised functional paraphrase uses short clauses: the output is a `.txt` text file; light/dark characters depict the picture; each displayed character must have equal width; this is a character-drawn rendition; the original picture cannot be restored from this text. The reviewer found no concrete semantic or grammatical error sufficient to reject the revision and recommended it unchanged at **modest compositional confidence**.

The equal-width display requirement replaces an explicit monospaced-font selection instruction. That preserves the practical condition but may be less actionable for a user unfamiliar with font choice. “Restore the original picture from this text” explains the irreversible rendition rather than literally saying “reopen as.” It does not prohibit viewing the text, assert that the original document was deleted, or claim that ordinary text edits are impossible. Verb-led sentences can read as instructions; native software idiomaticity and usability remain unverified. Lack of exact full-sentence attestation or native-human certification is not imposed as a gate.

Three existing complete values were independently reviewed and retained:

- `formats22_ascii_label`: the functional ASCII-character drawing label is semantically appropriate in the format selector, with moderate confidence. Its action-shaped form and length remain style/layout caveats, not demonstrated meaning defects.
- `formats22_ascii_columns`: width measured in characters, moderate-high confidence. These are ASCII cells including spaces, not words, source pixels, or the trailing newline.
- `ui_same_width`: same width, moderate-high confidence. Both its assembly toolbar and normalization dialog consumers are covered. This is an image-normalization command, not a font control; it is not evidence that the rejected font sentence was sound.

## Language evidence

[Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), independently checked, supports character-count `cih` (C39), width (G85), `doxdoengz` sameness (D70), brightness (R27), darkness (L7), `yienzlaiz` original/former (Y17), file/document and obligation vocabulary. “Each” occurs in its old-loan appendices; that evidence is not mislabelled as a main-entry computing standard. These are lexical and construction inputs, not an attested full technical paragraph, and OCR transcription is a limitation.

[Guangxi Minzu Bao, 29 November 2023, page 3](https://www.guangximinzubao.cn/szbzw/page/21/2023-11/29/03/2023112903_pdf.pdf), directly re-read as PDF text during integration, uses `hoizfuk` for restoring a nonhuman state in bilingual ecological-restoration prose (Zhuang lines 107–109 and corresponding Chinese lines 23–24). That supports the recovery verb; applying it to the original picture is an authored technical extension. This check closes the reviewer's lack of a dictionary hit without claiming PDF-raster or native-user validation. Existing Save-as wording supplies catalogue consistency, not independent proof.

## Actual consumers and behavior

`SaveOptionsDialog.update` binds the whole new description only for ASCII art. The same `FlowTextView` is retained in the vertical form. The selected format is `text/plain`, `.txt`, and a derived export. The label is resolved through `ImageFormat.label`; the ASCII-only slider accepts 40–240 columns and feeds its name to the visible value, accessibility descriptions and exact-entry title. Width and inversion flow through `ExportOptions` and `ImageExporter` to `TextImageCodec.encodeAscii`.

The codec scales a working bitmap to a character grid. Production `TextImageData.ascii` maps composited brightness to a fixed ASCII ramp, including spaces, then writes one newline per row. It does not encode per-character colors, embed a font, or embed the original raster for later reconstruction. “Light/dark” is the source's visual-density description. Equal-width font display is guidance to the external text viewer, not an app-enforced font setting. Source-bitmap recycling is avoided when the scaled object is the source. Ordinary derived-export state is unchanged; no save, parser, encoder or layout logic is edited.

Separately, `ui_same_width` opens `NormalizeImagesDialog` with the width axis, also providing its title. Confirmation applies the selected common output width to the assembly images while retaining each cropped image's aspect ratio, with integer rounding and existing size checks. It does not normalize fonts or make all image heights equal.

## Verification and limits

- All 171 offered-option structural catalogue checks and the importance manifest pass. Existing nodes and attributes are unchanged; placeholders, numerals, literal tokens, newline escapes and Android/XML escaping pass. The new `.txt` clarification is justified by the actual format contract.
- Four localization host modules: **61 tests passed in 5.571 seconds**.
- `test_text_image_data.TextImageDataTests.test_ascii_aspect_luminance_inversion_and_size`: **1 test passed in 0.814 seconds**, compiling and executing production Java. It exercises row geometry/size limits, fixed width and newlines, brightness inversion and transparency compositing. An initial invocation omitted `PYTHONPATH=tools` and failed module discovery before executing tests; the corrected invocation passed. This is not Android Bitmap/UI execution.
- **8 English/Zhuang Java XML-template formatting cases** pass for the new description and three retained values. These are not Android resource compilation.
- Temporary token-aware static checks confirm **5 resource bindings**, ASCII visibility/format classification, vertical-view reuse, width display/accessibility/title routing, working-bitmap cleanup and the separate assembly-normalization route. Initial temporary-check assumptions about the vertical detach expression were corrected against the actual shared-control loop; no production fix was needed.
- Inspected but not run: `TextImageCodecTest.asciiUsesChosenWidthAspectAndInversionWithoutChangingSource`, `ExportFormatDialogTest.iconAndAsciiOptionsAreSpecificToTheirFormatAndSurviveReopening`, and `DerivedExportStateTest.asciiExportKeepsOriginalDrawingAndBlocksPendingClose`. These cover different codec, format-switch/cancel/reopen and unsaved-document concerns; inspection is not runtime credit.
- `git diff --check` passes. All **1,591** base file bytes and executable modes matched the complete remote tree. Publication uses a two-file overlay, exact expected parent and non-force lease, followed by complete tree and exact changed-file readback. No permanent per-edit test package or approved-sentence mirror is added.

Presence is P0 **77/94**, P1 **158/249**, P2 **80/305**, P3 **3/71**. Across 171 options, missing counts are **154 / 1,333 / 30,049 / 7,478**, with 46 complete-presence options. Counts distinguish missing resources from reviewed language quality and do not expand excluded fallback-only translation work.

Android SDK/Kotlin compiler are unavailable. Android compilation, Robolectric, Bitmap scaling, external text-viewer typography, actual export/provider and lifecycle flows, TalkBack and device layout were not executed. Exact-head Actions state is checked and reported after publication. No merge, release or CI-pass claim is made.
