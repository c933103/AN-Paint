# Amharic text geometry: original draft dossier

Production 66be61df27c5359bffc32d56db21f3949899f873; tree 870c5a584120d92710be516af0dc3b3847b183d9. Eleven complete source copies are supplied, exact Git blobs checked against freshly retrieved production tree.

No independent acceptance or implementation. Prior52 ready/six held remain separate.

## string/ui_size_pixels

English: Size (pixels)

Proposed XML: `<string name="ui_size_pixels">"መጠን (ፒክሰሎች)"</string>`

Status: review

Confidence: medium-high lexical components; medium contextual/orthographic choice; unaccepted

Original composition from exact LibreOffice Size → መጠን and the directly attested AOSP Gallery2 plural token ፒክሰሎች inside 13M pixels/4M pixels. Retains parentheses but translates the spelled-out English pixels; unlike Size (px), there is no literal px to preserve. The selected spelling family matches the prior Pixel grid candidate የፒክሰል ፍርግርግ. This is not an exact whole-label quotation.

Label for text size numeric field, Paint.textSize1..1024 image pixels. Not font point size, screen dp/sp or guaranteed glyph bounding-box height. Preview can scale whole block down to fit, independently of eventual canvas text size.

['Full Size (pixels) phrase was not established as an exact primary-source translation.', 'LibreOffice variants ፒክስሎች and ፒክስልስ are retained; reviewer must adjudicate spelling consistency rather than claim one attestation invalid.', 'Refers to Paint.textSize in image pixels (1..1024), not points, dp/sp, text length, preview scale, or a guaranteed visible glyph height.', 'Original AI-authored review draft, not independently accepted or native-speaker validated.', 'No app implementation, build, rendering, UI-fit, accessibility or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L40-L46, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L73-L76, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L100-L107, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L482-L497

## string/ui_line_spacing

English: Line spacing (%)

Proposed XML: `<string name="ui_line_spacing" formatted="false">"የ መስመር ክፍተት (%)"</string>`

Status: review

Confidence: high lexical; medium-high semantic transfer; unaccepted

Exact nonfuzzy LibreOffice paragraph/formatting Line Spacing → የ መስመር ክፍተት plus the source literal (%). Keep source-attested spacing in the author draft rather than silently normalize it. Proportional-spacing help corroborates the percentage concept, but AN-Paint consumer code alone defines its behavior.

Label for numeric percentage field50..300. Value divided by100 multiplies paint.fontSpacing. Controls horizontal row steps or vertical column steps, not character spacing or extra pixel gap. Preserve literal(%) and formatted=false. Current source line concept spans both writing directions; no established source defect.

['Preserve literal (%) and formatted="false".', 'This 50..300% value multiplies paint.fontSpacing for horizontal row steps and vertical column steps; not character spacing, paragraph margins, or an extra pixel gap.', 'The draft should remain axis-neutral. A reviewer may prefer normalized የመስመር spacing; that would be an editorial change, not exact source bytes.', 'Original AI-authored review draft, not independently accepted or native-speaker validated.', 'No app implementation, build, rendering, UI-fit, accessibility or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L41-L46, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L78-L79, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L100-L107, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/VerticalText.kt#L100-L130

## string/ui_text_alignment

English: Text alignment

Proposed XML: `<string name="ui_text_alignment">"ጽሑፍ ማሰለፊያ"</string>`

Status: review

Confidence: high lexical alignment support; medium-high project-normalized composition; unaccepted

Adapt exact nonfuzzy LibreOffice Text Alignment → ጽሁፍ ማሰለፊያ, explicitly normalizing the text noun from ጽሁፍ to current project ui_text spelling ጽሑፍ. Alignment is ማሰለፊያ, distinct from the separately attested text-direction term አቅጣጫ. This normalized full phrase is an original editorial draft, not an exact quotation.

Alignment Spinner contentDescription, identifies text alignment, not text direction or image placement. Options switch axis with writing direction. Accessibility label wording only, no screen-reader acceptance. Horizontal shorter lines are aligned within the maximum-width text block; vertical shorter columns are aligned within maximum-height block. When committing, block placement is also anchored at chosen canvas point using alignment. Neither translation nor source checks certify actual rendered glyphs.

['Orthographic change ሁ→ሑ is disclosed and needs independent review; it does not invalidate the attested alternate or authorize changes to other labels.', 'Accessibility name of an alignment spinner; not a writing-direction control, canvas/image movement command, or assurance of screen-reader performance.', 'Alignment also determines text-block anchoring at the chosen canvas point, as well as shorter row/column placement within the block. Do not reduce it to only internal alignment.', 'Original AI-authored review draft, not independently accepted or native-speaker validated.', 'No app implementation, build, rendering, UI-fit, accessibility or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L54-L54, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L79-L86, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/VerticalText.kt#L106-L130, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L489-L496

## string/ui_left_aligned

English: Left aligned

Proposed XML: `<string name="ui_left_aligned">"በ ግራ ማሰለፊያ"</string>`

Status: review

Confidence: high text-alignment lexical support; medium option-state idiom; unaccepted

Use the exact nonfuzzy LibreOffice paragraph left-alignment function label, also attested in Fontwork text alignment. Adapting Align Left to the AN-Paint option Left aligned is an original grammatical/function-label transfer, not an exact English-label match. Keep attested spacing for review.

Horizontal-text option index0/LEFT; shorter lines flush left and block starts at canvas x coordinate. Not logical bidi-start or selecting left-to-right script direction. Horizontal shorter lines are aligned within the maximum-width text block; vertical shorter columns are aligned within maximum-height block. When committing, block placement is also anchored at chosen canvas point using alignment. Neither translation nor source checks certify actual rendered glyphs.

['Review function-label ማሰለፊያ versus a passive aligned-state construction in this spinner; neither is forced accepted.', 'Refers to the physical left edge for horizontal text alignment/anchoring, not writing start/end, reading order, or moving an existing image.', 'The app substitutes Top/Centred/Bottom options for vertical text, so do not make this label axis-neutral.', 'Original AI-authored review draft, not independently accepted or native-speaker validated.', 'No app implementation, build, rendering, UI-fit, accessibility or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L54-L54, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L81-L86, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/VerticalText.kt#L110-L113, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L489-L496

## string/ui_centred

English: Centred

Proposed XML: `<string name="ui_centred">"መሀከል"</string>`

Status: review

Confidence: high lexical and dual-axis evidence; medium option-group idiom; unaccepted

Reuse exact nonfuzzy Centered → መሀከል from paragraph last-line alignment; Center is also መሀከል in both horizontal and vertical text-adjustment values. British Centred and American Centered are the same English sense. Short neutral form serves both axes without adding a horizontal qualifier.

Shared index1/CENTER option. Horizontal: line centering across width and block centered on x anchor. Vertical: column content centered along height and block centered on y anchor. Not canvas center or justified/distributed alignment. Horizontal shorter lines are aligned within the maximum-width text block; vertical shorter columns are aligned within maximum-height block. When committing, block placement is also anchored at chosen canvas point using alignment. Neither translation nor source checks certify actual rendered glyphs.

['Must serve both horizontal rows and vertical columns and corresponding block anchoring; do not translate as horizontal center only.', 'Center of the text alignment block/anchor, not necessarily the whole canvas or screen.', 'Attested short noun is intentionally shorter than neighboring function-label forms; independent review should decide whether uniform ማሰለፊያ suffixes improve the group. Source spelling መሀከል is preserved without claiming native orthographic preference.', 'Original AI-authored review draft, not independently accepted or native-speaker validated.', 'No app implementation, build, rendering, UI-fit, accessibility or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L54-L54, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L81-L86, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/VerticalText.kt#L110-L121, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L489-L496

## string/ui_right_aligned

English: Right aligned

Proposed XML: `<string name="ui_right_aligned">"በ ቀኝ ማሰለፊያ"</string>`

Status: review

Confidence: high text-alignment lexical support; medium option-state idiom; unaccepted

Use the exact nonfuzzy LibreOffice paragraph right-alignment function label, also attested in Fontwork text alignment. Adapting Align Right to the AN-Paint option Right aligned is an original grammatical/function-label transfer, not an exact English-label match. Keep attested spacing for review.

Horizontal-text option index2/RIGHT; shorter lines right-aligned in block and block ends at x anchor. Not choosing right-to-left writing direction or mirroring. Horizontal shorter lines are aligned within the maximum-width text block; vertical shorter columns are aligned within maximum-height block. When committing, block placement is also anchored at chosen canvas point using alignment. Neither translation nor source checks certify actual rendered glyphs.

['Review function-label ማሰለፊያ versus a passive aligned-state construction in this spinner; neither is forced accepted.', 'Refers to the physical right edge for horizontal text alignment/anchoring, not writing start/end, reading order, or moving an existing image.', 'The app substitutes Top/Centred/Bottom options for vertical text, so do not make this label axis-neutral.', 'Original AI-authored review draft, not independently accepted or native-speaker validated.', 'No app implementation, build, rendering, UI-fit, accessibility or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L54-L54, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L81-L86, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/VerticalText.kt#L110-L113, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L489-L496

## string/ui_top23

English: Top aligned

Proposed XML: `<string name="ui_top23">"ከ ላይ ማሰለፊያ"</string>`

Status: review

Confidence: high lexical components and content-edge sense; medium vertical-text option transfer; unaccepted

Use exact nonfuzzy LibreOffice cell-content Align Top → ከ ላይ ማሰለፊያ, corroborated by text vertical-adjustment Top value and content-edge help. The original transfer adapts a function label to the source Top aligned state option; it does not transplant a spreadsheet/cell concept.

Vertical-text option index0/LEFT internally means top-aligned along column height; block starts at y anchor. Not start column on right or top of whole canvas. Horizontal shorter lines are aligned within the maximum-width text block; vertical shorter columns are aligned within maximum-height block. When committing, block placement is also anchored at chosen canvas point using alignment. Neither translation nor source checks certify actual rendered glyphs.

['Not an exact primary-source English Top aligned label match; independent review should assess state-versus-function idiom.', 'Controls top alignment/anchoring of vertical text columns, not moving the canvas/image, vertical writing direction, glyph rotation, or UI position.', 'Use physical top meaning even when vertical columns progress right-to-left or left-to-right. No separate direction word should be inserted.', 'Original AI-authored review draft, not independently accepted or native-speaker validated.', 'No app implementation, build, rendering, UI-fit, accessibility or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L81-L86, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/VerticalText.kt#L116-L130, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L489-L496

## string/ui_bottom23

English: Bottom aligned

Proposed XML: `<string name="ui_bottom23">"ከ ታች ማሰለፊያ"</string>`

Status: review

Confidence: high lexical components and content-edge sense; medium vertical-text option transfer; unaccepted

Use exact nonfuzzy LibreOffice cell-content Align Bottom → ከ ታች ማሰለፊያ, corroborated by text vertical-adjustment Bottom value and content-edge help. The original transfer adapts a function label to the source Bottom aligned state option; it does not transplant a spreadsheet/cell concept.

Vertical-text option index2/RIGHT internally means bottom-aligned along column height; block ends at y anchor. Not bottom of whole canvas or last column. Horizontal shorter lines are aligned within the maximum-width text block; vertical shorter columns are aligned within maximum-height block. When committing, block placement is also anchored at chosen canvas point using alignment. Neither translation nor source checks certify actual rendered glyphs.

['Not an exact primary-source English Bottom aligned label match; independent review should assess state-versus-function idiom.', 'Controls bottom alignment/anchoring of vertical text columns, not moving the canvas/image, vertical writing direction, glyph rotation, or UI position.', 'Use physical bottom meaning even when vertical columns progress right-to-left or left-to-right. No separate direction word should be inserted.', 'Original AI-authored review draft, not independently accepted or native-speaker validated.', 'No app implementation, build, rendering, UI-fit, accessibility or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L81-L86, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/VerticalText.kt#L116-L130, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L489-L496

## Shared scope and evidence limits

TextStyleDialog fields and alignment choices update TextPreview; confirmation validates numeric ranges and passes TextSettings through ClassicPaintActivity.showTextDialog to PaintDocument.text, then VerticalText.bounds/draw. Preview has independent fit scale. All selected labels missing; prior52ready/sixholds excluded. Font fallback selection, shaping quality and general numeric-parser validation outside this bounded wording review.

No English defect established. Preserve physical alignment versus writing-direction distinctions and line-spacing row/column behavior. If real source defect established later, correct English first and flag all affected locales; no silent Amharic-only compensation.

Literal (%) and formatted=false retained for Line spacing. The word pixels remains an explicit unit in Size. No printf arguments occur in selected values. Numeric validation and other dialog messages remain excluded.

Full lexical reasoning, exact records, source snapshots and retrieval/reuse limitations are in lexical-evidence/. Nonfuzzy is a record flag, not proof of correctness. Component and cross-context evidence does not establish exact full-phrase native acceptance.

Original drafts only; independent review required.

Source-only bounded consumer inspection, not native, rendered, accessibility or lifecycle acceptance.

Previous inherited-label uncertainties, optional suggestions, six held proposals and full Help holds unchanged.

Production remains12 present/705 missing of717. No production changes, builds, CI, release or Work task.
