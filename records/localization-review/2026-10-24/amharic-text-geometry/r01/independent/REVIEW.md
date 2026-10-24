# Independent Amharic text-geometry review

Result: **2 retain, 6 revise, 0 hold; 0 implemented**.

Input manifest SHA-256: `f3200cc397637aaad77ef060b251a13e6bbc673b8b6201c49b06f0935421fb31`.
Production: `66be61df27c5359bffc32d56db21f3949899f873`; tree: `870c5a584120d92710be516af0dc3b3847b183d9`.

Retain means a bounded independent AI wording/source judgment, not native-speaker or release acceptance. Revised values are exact editorial recommendations for author reconciliation. Prior 52 ready/six holds are separate and unchanged.

## Exact recommendations

- string/ui_size_pixels: **RETAIN** → መጠን (ፒክሰሎች)
- string/ui_line_spacing: **REVISE** → የመስመር ክፍተት (%)
- string/ui_text_alignment: **RETAIN** → ጽሑፍ ማሰለፊያ
- string/ui_left_aligned: **REVISE** → በግራ ማሰለፊያ
- string/ui_centred: **REVISE** → መሀከል ማሰለፊያ
- string/ui_right_aligned: **REVISE** → በቀኝ ማሰለፊያ
- string/ui_top23: **REVISE** → ከላይ ማሰለፊያ
- string/ui_bottom23: **REVISE** → ከታች ማሰለፊያ

## Shared language decisions

The five alignment options may use nominal alignment-mode labels in this spinner. A passive state sentence is not required merely because English says “aligned”: selecting the mode conveys the setting. This is the reviewer’s contextual judgment, not a claim of a direct whole-label source match.

Centred is revised to the already-attested `መሀከል ማሰለፊያ` for group parallelism. The shorter draft is not semantically wrong. It remains suitable for both horizontal and vertical alignment and never means centre the whole canvas. [Microsoft’s historical Amharic Style Guide, p43](https://download.microsoft.com/download/6/2/a/62a993f1-d3b2-4f28-b3e7-22965eb91426/amh-eth-styleguide.pdf#page=43) supports parallel form in list items, but does not certify these particular labels.

The five prefix-spacing changes are explicit editorial joins. [Baker and Kramer, 2014, pp144–145](https://sites.rutgers.edu/mark-baker/wp-content/uploads/sites/199/2019/07/amharic-preps-as-case-offprint.pdf#page=5) analyze the relevant elements as host-dependent prefixes, including genitive yä- in footnote 6. Applying that analysis to these UI spellings is the reviewer’s recommendation; the paper does not prescribe these exact labels. The spaced LibreOffice evidence is not altered.

For Text alignment, retain the disclosed ሁ→ሑ choice: ጽሑፍ matches current ui_text. These are U+1201 and U+1211, not Unicode normalization forms. Do not globally rewrite other words or pretend the source contained the revised spelling. Preserve the attested centre spelling መሀከል without claiming native orthographic preference.

## Source and integrity checks

All 36 manifest entries, all 11 source Git blob/SHA-256 bindings, all 11 lexical snapshot hashes, all 34 exact lexical records (37 source fragments), and all eight English/target values and attributes verified independently. All eight keys are absent from the supplied twelve-entry Amharic catalogue. No production file was changed.

The reviewer did not refetch production or the 11 lexical snapshots. The production-tree retrieval date is supplied packet provenance; the lexical files remain complete reused snapshots with their no-fresh-HTTP qualification. Supplementary linguistic references were independently opened. The Microsoft PDF could not be fetched by the web tool, so the complete existing PDF was rehashed and printed p43 rendered and visually checked. Its unreliable extracted Amharic examples were not used.

## Per-key decisions

### string/ui_size_pixels: RETAIN

English: Size (pixels)
Original: "መጠን (ፒክሰሎች)"
Recommended XML: `<string name="ui_size_pixels">"መጠን (ፒክሰሎች)"</string>`

Retain the ordinary Size noun and the independently attested pixels plural. This original composition explicitly preserves the text-size unit without importing camera megapixel quantity, points, dp/sp, character count, or exact visible glyph height. The ፒክሰል stem is coherent with the separate Pixel grid spelling family, but that earlier item is not re-reviewed here.

Consumer check: TextStyleDialog.kt:41-46,73,101-106 validates 1..1024 image-pixel textSize. PaintDocument.kt:486-487 consumes size directly as Paint.textSize. Preview fit scaling at TextStyleDialog.kt:121-127 is independent. No integer-only promise is made.

Confidence: High for size and unit sense; medium-high for the composed label and spelling choice.

Primary lexical evidence:
- size_label: [libreoffice-am-cui.po:19993–19997](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po)
- pixels_aosp_13mp: [android-gallery2-en.xml:689](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values/strings.xml?format=TEXT)
- pixels_aosp_13mp: [android-gallery2-am.xml:255](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT)
- pixels_aosp_4mp: [android-gallery2-en.xml:695](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values/strings.xml?format=TEXT)
- pixels_aosp_4mp: [android-gallery2-am.xml:258](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT)
- pixels_aosp_8mp: [android-gallery2-en.xml:691](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values/strings.xml?format=TEXT)
- pixels_aosp_8mp: [android-gallery2-am.xml:256](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT)
- pixels_lo_plural: [libreoffice-am-help01.po:32968–32975](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/01.po)
- pixels_lo_ui_variant: [libreoffice-am-cui.po:22253–22257](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po)

Pinned consumer: [Text dialog](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L40-L46).

Original XML-text SHA-256: `ac0258a5566273f7067738d5d1b3447afb56a0cff80ea7ac2fc871408169a85d`.
Recommended XML-text SHA-256: `ac0258a5566273f7067738d5d1b3447afb56a0cff80ea7ac2fc871408169a85d`.
Per-key decision seal: `3e50228abc5fe4eb1abcf41606cccad9f13cd1e78a63106380febdaa7fae697e`.

### string/ui_line_spacing: REVISE

English: Line spacing (%)
Original: "የ መስመር ክፍተት (%)"
Recommended XML: `<string name="ui_line_spacing" formatted="false">"የመስመር ክፍተት (%)"</string>`

Join the bound የ- prefix to መስመር. Retain the attested spacing noun, literal (%) and formatted=false. This is an explicitly editorial spacing change, not an exact quotation of the LibreOffice bytes. The axis-neutral line concept is appropriate for horizontal lines and vertical columns.

Consumer check: TextStyleDialog.kt:42,78,101-106 divides the 50..300 percentage by 100. VerticalText.kt:100-124 uses paint.fontSpacing * spacing as the step between horizontal rows or vertical columns. It is not an extra pixel gap, character spacing or paragraph margin.

Confidence: High for semantic/unit fidelity; medium-high for the editorial spelling choice.

Primary lexical evidence:
- line_spacing_label: [libreoffice-am-ui.po:19680–19688](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po)
- line_spacing_paragraph: [libreoffice-am-cui.po:19284–19288](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po)
- line_spacing_factor: [libreoffice-am-ui.po:19720–19728](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po)
- line_spacing_percent: [libreoffice-am-help01.po:21817–21824](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/01.po)

Pinned consumer: [Text dialog](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L41-L46).

Original XML-text SHA-256: `1dddc8e8bef5f8cb4aece0e15186eb18b43a9dc52a05aa99c21298f35442a643`.
Recommended XML-text SHA-256: `963c84a1e3ee18501b1efe650dc9043da5e64fc1590f39d2c23d3a4141843203`.
Per-key decision seal: `6304c368b59439f55b023212cc8f88d672d6430f727f77a19cd23037f8bdc11c`.

### string/ui_text_alignment: RETAIN

English: Text alignment
Original: "ጽሑፍ ማሰለፊያ"
Recommended XML: `<string name="ui_text_alignment">"ጽሑፍ ማሰለፊያ"</string>`

Retain the disclosed project-consistent spelling ጽሑፍ and the attested alignment noun. This names the spinner function rather than writing direction. The ሁ to ሑ replacement is a local orthographic choice, not Unicode normalization, a correction of all source attestations, or permission to rewrite unrelated labels.

Consumer check: TextStyleDialog.kt:54 is the spinner contentDescription; 79-84 selects LEFT/CENTER/RIGHT and switches the visible options by writing direction. VerticalText.kt:110-124 aligns shorter layout rows/columns inside the maximum-width/height block. PaintDocument.kt:489-496 also anchors the block to the chosen canvas coordinate.

Confidence: High for alignment sense; medium-high for locally consistent orthography and label idiom.

Primary lexical evidence:
- text_alignment_label: [libreoffice-am-cui.po:7955–7959](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po)
- text_alignment_vertical: [libreoffice-am-svx.po:11136–11140](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po)
- text_direction_distinction: [libreoffice-am-cui.po:18977–18981](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po)
- current_project_text_spelling: [project-am-strings.xml:9](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/res/values-b+am/strings.xml)

Pinned consumer: [Text dialog](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L54-L54).

Original XML-text SHA-256: `a4e4e9f480cf8b7c488db33518199fa5074a0e6bfbf2fd219b5b0fa8f4bb45a2`.
Recommended XML-text SHA-256: `a4e4e9f480cf8b7c488db33518199fa5074a0e6bfbf2fd219b5b0fa8f4bb45a2`.
Per-key decision seal: `15731bcbbc2f83183a436e0625147224152d7498cb3dc3525ea48ea81a603f8b`.

### string/ui_left_aligned: REVISE

English: Left aligned
Original: "በ ግራ ማሰለፊያ"
Recommended XML: `<string name="ui_left_aligned">"በግራ ማሰለፊያ"</string>`

Join the bound በ- prefix to ግራ; retain the attested nominal alignment-mode wording. In this spinner an alignment-mode name conveys the selected setting without requiring a passive state sentence. Do not convert physical left to logical start or writing direction.

Consumer check: Horizontal option index 0 maps to Paint.Align.LEFT. Internal row offset is 0; block left is canvas x. The claim concerns layout bounds, not a pixel-perfect glyph-ink edge. TextStyleDialog.kt:79-84; VerticalText.kt:110-113; PaintDocument.kt:489-496.

Confidence: High for physical-side and alignment sense; medium-high for nominal option idiom and joined spelling.

Primary lexical evidence:
- align_left_paragraph: [libreoffice-am-ui.po:19570–19578](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po)
- align_left_fontwork: [libreoffice-am-svx.po:16366–16370](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po)
- align_left_fontwork_context: [libreoffice-am-svx.po:16372–16376](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po)

Pinned consumer: [Text dialog](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L54-L54).

Original XML-text SHA-256: `d811c5e6a8ac4e2dc2f83735495612cd5714907dc9ff6a61ff90961073873870`.
Recommended XML-text SHA-256: `4660992642cc65bcc26d426d00835f54185724175aa25220a6ee33caf5db5c07`.
Per-key decision seal: `be8ce923f17db1947d36fb0bd97bee50ae0b96a5b6c7aeba0993c2c874622143`.

### string/ui_centred: REVISE

English: Centred
Original: "መሀከል"
Recommended XML: `<string name="ui_centred">"መሀከል ማሰለፊያ"</string>`

Use the supplied exact Align Center counterpart for parallel nominal mode labels across both option sets. The shorter መሀከል is semantically supported and is not declared erroneous; the added alignment noun is a consistency recommendation. Preserve the attested መሀከል spelling rather than silently choosing a different native orthographic variant. Add no horizontal, screen or whole-canvas qualifier.

Consumer check: Shared option index 1 maps to CENTER. Horizontal row offset is (block width - row width)/2, and the block shifts by half its width around canvas x. Vertical content offset is (block height - column length)/2, and the block shifts by half its height around canvas y. It does not place text at the centre of the canvas. Same three consumers as the other alignment modes.

Confidence: High for dual-axis centering sense; medium-high for option-group parallelism; no claim of native orthographic preference.

Primary lexical evidence:
- align_center_paragraph: [libreoffice-am-ui.po:19610–19618](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po)
- centred_paragraph: [libreoffice-am-cui.po:18881–18885](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po)
- center_horizontal_text: [libreoffice-am-svx.po:1568–1572](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po)
- center_vertical_text: [libreoffice-am-svx.po:1538–1542](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po)

Pinned consumer: [Text dialog](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L54-L54).

Original XML-text SHA-256: `a4e79f32aaedd30af077f65e886c15c4cb4136e722c4c3c6213b37ad4d13c3bf`.
Recommended XML-text SHA-256: `d692a33941348eb4e33f2de7cf9c52518a107f24f1b8c95bc29331e485967d95`.
Per-key decision seal: `a55aa6ffd3bbec4e742e7d914ec321b06ea75fb25b6d8db69f5a2f73c3019ea0`.

### string/ui_right_aligned: REVISE

English: Right aligned
Original: "በ ቀኝ ማሰለፊያ"
Recommended XML: `<string name="ui_right_aligned">"በቀኝ ማሰለፊያ"</string>`

Join the bound በ- prefix to ቀኝ; retain the nominal alignment-mode wording. It is parallel to left and the revised centre option. Preserve physical right rather than logical end, right-to-left writing, or image motion.

Consumer check: Horizontal option index 2 maps to Paint.Align.RIGHT. Internal row offset is block width minus row width; block left is canvas x minus block width. TextStyleDialog.kt:79-84; VerticalText.kt:110-113; PaintDocument.kt:489-496.

Confidence: High for physical-side and alignment sense; medium-high for nominal option idiom and joined spelling.

Primary lexical evidence:
- align_right_paragraph: [libreoffice-am-ui.po:19590–19598](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po)
- align_right_fontwork: [libreoffice-am-svx.po:16390–16394](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po)
- align_right_fontwork_context: [libreoffice-am-svx.po:16396–16400](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po)

Pinned consumer: [Text dialog](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L54-L54).

Original XML-text SHA-256: `46a9221e80bff982b1df85115c37dfd3ed62d7a2cbf7b9700ebfa5f64f37ec06`.
Recommended XML-text SHA-256: `cb2af18bc6338647938698632ea9d93a503cb0c052c39b7b1dd75600cd095f30`.
Per-key decision seal: `595dd661a650744e66bb279373474d010d0a4175721af7e1e553198bd03817c0`.

### string/ui_top23: REVISE

English: Top aligned
Original: "ከ ላይ ማሰለፊያ"
Recommended XML: `<string name="ui_top23">"ከላይ ማሰለፊያ"</string>`

Join the bound ከ- prefix to ላይ; retain the nominal alignment-mode wording. The text-adjustment Top record and cell-content Align Top record establish the content-edge sense without importing a cell, page or whole-canvas destination.

Consumer check: Vertical option index 0 still maps to LEFT internally, but y offset is 0 and block top is canvas y. Column progression left-to-right or right-to-left is a separate direction setting. The English key ui_top23 must not be replaced by another Top label. TextStyleDialog.kt:79-84; VerticalText.kt:116-124; PaintDocument.kt:489-496.

Confidence: High for top/content-edge meaning; medium-high for transfer to the vertical-text mode option and joined spelling.

Primary lexical evidence:
- align_top_cell: [libreoffice-am-ui.po:27236–27244](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po)
- align_top_cell_context: [libreoffice-am-help01.po:25975–25982](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/01.po)
- align_top_text_value: [libreoffice-am-svx.po:1532–1536](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po)

Pinned consumer: [Text dialog](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L81-L86).

Original XML-text SHA-256: `95fd55488103f97b08625a570a9be189fa9b9cd7ee282e4630e626ef77d2c58c`.
Recommended XML-text SHA-256: `ffff20f53c24619b06921f1faab7ad004184bfe0f6b73e83e8d68929958e8d04`.
Per-key decision seal: `7520c66f3ab5cb7fc55a5bf9a3b2ad0fd9b54c1044f68afc99a250353a60629e`.

### string/ui_bottom23: REVISE

English: Bottom aligned
Original: "ከ ታች ማሰለፊያ"
Recommended XML: `<string name="ui_bottom23">"ከታች ማሰለፊያ"</string>`

Join the bound ከ- prefix to ታች; retain the nominal alignment-mode wording. The text-adjustment Bottom record and cell-content Align Bottom record establish the content-edge sense. The excluded object-bottom help does not support this decision.

Consumer check: Vertical option index 2 still maps to RIGHT internally, but y offset is block height minus column length and block top is canvas y minus block height. This is bottom content alignment/anchoring, not last-column order or canvas-bottom placement. Preserve ui_bottom23. TextStyleDialog.kt:79-84; VerticalText.kt:116-124; PaintDocument.kt:489-496.

Confidence: High for bottom/content-edge meaning; medium-high for transfer to the vertical-text mode option and joined spelling.

Primary lexical evidence:
- align_bottom_cell: [libreoffice-am-ui.po:27276–27284](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po)
- align_bottom_cell_context: [libreoffice-am-help01.po:26047–26054](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/01.po)
- align_bottom_text_value: [libreoffice-am-svx.po:1544–1548](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po)

Pinned consumer: [Text dialog](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L81-L86).

Original XML-text SHA-256: `d8e0122c605fa75cbc9dcd3eef70cb4b1ca9cc8ff62c12504aae410dc7cca62a`.
Recommended XML-text SHA-256: `6aad5b7653ea0ad3e6b2a36074973cb7a4ffca727b00c2ee4ad3ee8fa2b8caed`.
Per-key decision seal: `d859b84d5c245ed09838cf9ed33613184a30a93da9f149210520e4cc71b00786`.

## Boundary and next action

The consumer chain is text dialog → ClassicPaintActivity.showTextDialog → PaintDocument.text → VerticalText bounds/draw. Horizontal alignment changes row offset and x anchoring; vertical alignment changes column-content y offset and y anchoring. Column progression and glyph orientation remain separate. The claims concern layout bounds, not exact glyph ink or verified screen-reader output.

No English defect is established. If one is established later, correct English first, flag the affected term across languages, then review each language rather than compensating only in Amharic.

Reconcile the six revised exact values with the author. Do not count them as unchanged-draft acceptances or silently add them to the prior ready set. No Work task, production edit, app build, CI, release, external publication, native review, UI-fit or runtime validation was performed. The input evidence and prior holds are unchanged.

The JSON report includes exact keys, attributes, hashes, limitations and all decisions. MANIFEST.json is a byte-integrity seal, not a cryptographic signature. Reference PDFs and rendered pages are not republished in this report.
