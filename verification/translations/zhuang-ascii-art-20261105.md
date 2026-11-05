# Zhuang ASCII-character image label, 5 November 2026

## Scope and language review

The live branch was reconciled at parent `f9e4c6291182aaaa8433caf9df363747e23a14d6`, tree `171f8adb674c19403478f8a9a51bf2fc5106e7b4`. Its preceding publication was confirmed with no pending or uncertain write. This adds missing P2 `formats22_ascii_label`, preserving all 293 previous typed resources for a total of 294. Only canonical XML and this report change.

Independent review recommends a functional phrase meaning “Use ASCII characters to draw an image,” with **moderate confidence**. The characters are the drawing medium; the phrase does not describe arbitrary text annotations or promise a raster output. The exact ASCII identifier is preserved. The shorter initial stacked-noun candidate was not adopted because its relationship between image and characters was less explicit.

Sources, both found by the reviewer and directly retrieved during integration:

- [Guangxi Minzu Bao, 24 December 2014](https://www.guangximinzubao.cn/szbzw/html/2014-12/24/content_11479.htm), a discussion of Zhuang vocabulary, explicitly lists `cih` as character and a unit for counting characters. The article's full body contains this evidence even though the initial web find operation returned no match.
- [Guangxi Minzu Bao, 20 February 2013](https://www.guangximinzubao.cn/szbzw/html/2013-02/20/content_1178.htm) quotes `yungh saek heu daeuj nyumx`, supporting the productive “use [medium] to [action]” construction. This is a teaching article, not software documentation.
- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), independently checked by the reviewer, supports `yungh` use and `veh` draw. The OCR mirror may contain transcription errors.

The exact full wording is a newly composed functional paraphrase, not an independently attested Zhuang term for ASCII art. Its action-shaped form occupies a format selector and is longer than the English label. No standard technical-term or native-human certification claim is made.

## Actual consumer

`ImageFormat.ASCII_ART` resolves the resource through its selected-locale label getter. `SaveOptionsDialog` displays it in the format spinner and separately shows the ASCII controls and description. The format remains `text/plain`, `.txt`, and a derived export.

`ImageExporter` passes the selected column count and inversion option to `TextImageCodec.encodeAscii`. A working bitmap is scaled to the requested text grid, then the production Java `TextImageData.ascii` primitive maps brightness to ASCII ramp characters, including spaces, and writes one newline per row. The output is a text rendition of the image rather than a raster file. Cleanup does not recycle the source bitmap when the scaled object is the source. In the ordinary export flow, the document is not marked saved and its saved target is not replaced.

The spinner uses the standard dropdown-item layout with the full resource string. Actual fit, truncation and accessibility presentation of the longer label have not been measured on a device. The surrounding description and inversion control are not changed or claimed as localized by this batch. No encoder, filtering, state or layout logic changes.

## Verification

Work and tests used the available temporary filesystem; no unrelated files were removed from the full main workspace.

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved, including ASCII.
- The four localization host suites plus `test_text_image_data.TextImageDataTests.test_ascii_aspect_luminance_inversion_and_size`: **62 tests passed in 17.975 seconds**. The latter compiles and executes the production Java primitive, checking fixed row width/newlines, aspect ratio, invalid geometry, minimum row, luminance inversion and transparency compositing. These are host executions, not Android Bitmap or UI execution.
- Two Java XML-to-string cases checked the English/Zhuang label for nonempty text and unchanged no-argument formatting. These are not Android resource compilation.
- Temporary token-aware Kotlin checks verified the sole resource binding, format-selector route, MIME/extension and derived-export classification, selected column/inversion route, working-copy cleanup and save/export state separation.
- Base snapshot verification matched Git blobs and executable modes for **1,284 materialized files**, retaining **288** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `TextImageCodecTest.asciiUsesChosenWidthAspectAndInversionWithoutChangingSource` and `DerivedExportStateTest.asciiExportKeepsOriginalDrawingAndBlocksPendingClose`. These inspections are not runtime evidence. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **158/249**, P2 **65/305**, P3 **2/71**. Across 171 options, missing resources are P0 **162**, P1 **1,333**, P2 **30,064**, P3 **7,479**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, Bitmap scaling, provider writes, actual export/lifecycle flows, TalkBack and device layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
