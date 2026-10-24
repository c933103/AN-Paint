# Amharic brush/shape controls: five reviewable drafts, two held proposals

Production 66be61df27c5359bffc32d56db21f3949899f873; tree 870c5a584120d92710be516af0dc3b3847b183d9. Eleven complete production files and five complete lexical-source snapshots are included with exact hashes and pinned locators.

Original translation drafts only. Calligraphy and Solid fill are explicit author holds; they must not be counted as ready. No source defect established.

## string/ui_round

English: Round

Proposed XML: `<string name="ui_round">"ክብ"</string>`

Status: review; lexical confidence high lexical / draft only.

Exact nonfuzzy LibreOffice line cap Round, cui linetabpage|liststoreCAP_STYLE. Geometric round also fits cursor-marker choice. Not numeric rounding.



Index0 tip choice for Brush/Watercolor/Eraser/Line. PaintDocument uses ROUND stroke cap when brushTip!=1 except Pencil, which is square regardless. Also index0 cursor-shape spinner sets cursorShape and overlay uses circle rather than square. Geometric round shape, not numeric rounding or round-trip.

Native/contextual UI acceptance and visual fit remain untested.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L785-L788, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1526-L1538, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L247-L258, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L292-L292, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintroidCursorOverlay.kt#L95-L112

## string/ui_square

English: Square

Proposed XML: `<string name="ui_square">"ስኴር"</string>`

Status: review; lexical confidence high lexical / draft only.

Exact nonfuzzy LibreOffice line cap Square; svx STR_ObjNameSingulQUAD separately confirms square geometry. Not an area unit.



Index1 brush-tip choice uses SQUARE stroke cap; also index1 cursor-shape spinner selects square marker outline. Shape noun/adjective, not squared number or area unit. Stroke joins remain ROUND, so this is not a promise of square joins at every path corner.

Loanword spelling follows verified UI source. Native preference versus an indigenous geometry expression remains untested; do not substitute a rectangle word.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L785-L788, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1526-L1538, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L247-L258, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintroidCursorOverlay.kt#L95-L112

## string/ui_calligraphy

English: Calligraphy

Proposed XML: `<string name="ui_calligraphy">"ሰያፍ ጭረት"</string>`

Status: hold; lexical confidence low-to-medium compositional / terminology HOLD.

Original descriptive phrase: diagonal/slanted stroke. LibreOffice STR_ObjNameSingulLINE_Diag supports ሰያፍ; Android pointer_stroke_style supports ጭረት as graphical stroke. Targets Brush-only repeated short slanted chisel marks, not font choice. No exact primary Calligraphy brush translation established.



Index2 appears for Brush only, not Watercolor/Eraser/Line. PaintCanvas.stroke creates repeated diagonal short segments with quarter-width strokes to form a slanted/chisel-like brush mark. Not a font picker, text entry or automatic handwriting conversion.

Descriptive paraphrase, NOT an established translation for calligraphy. Native review must check whether singular stroke adequately names repeated short diagonal marks and whether calligraphic/chisel character is preserved. Do not treat this row as release-ready.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L785-L788, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L507-L526

## string/ui_outline

English: Outline

Proposed XML: `<string name="ui_outline">"ድንበር ብቻ"</string>`

Status: review; lexical confidence medium compositional / draft only.

Original border-only phrase. Primary LO Border → ድንበር; only → ብቻ is visible in LO page layout labels. Captures foreground border without fill. Avoids copying text-character Outline → ረቂቅ out of its context.



Index0 shapeStyle; drawShape skips interior fill and draws foreground path border. Offered for Rectangle, Polygon, Ellipse, Rounded rectangle, Heart, Star and Arrow. Polygon open/closed path state remains separate. Not a document outline/sidebar or text outline hierarchy.

Native review and three-style contrast required; no exact full-phrase primary attestation.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L789-L790, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L271-L282

## string/ui_solid_fill

English: Solid fill

Proposed XML: `<string name="ui_solid_fill">"መሙያ ብቻ"</string>`

Status: hold; lexical confidence medium compositional / draft only.

Original fill-only paraphrase emphasizes implemented absence of outline. LO graphics sidebar Fill → መሙያ; only → ብቻ. This does not claim Solid literally means only. Foreground fill is implicit in the control context.

Author adds explicit HOLD beyond lexical suggestion: fill only substitutes an implemented behavior distinction for solid/uniform fill semantics. This must be independently adjudicated, not silently treated as equivalent English or a source correction. Alternative full-fill phrase is also unaccepted; lexical Solid in a transparency context does not establish exact shape-fill terminology.

Index1 shapeStyle fills path interior with foreground color and omits outline. Conventional uniform fill style, not separate flood-fill tool, pattern fill or an implementation guarantee about output alpha beyond inspected canvas behavior.

Confirm intentional behavior-based paraphrase and clarity of foreground-only fill; no exact full-phrase primary attestation.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L789-L790, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L271-L282

## string/ui_fill_line

English: Fill + line

Proposed XML: `<string name="ui_fill_line">"መሙያ + መስመር"</string>`

Status: review; lexical confidence medium-high lexical components / draft only.

LO graphics Fill and Line supply both nouns. Literal ASCII + preserved with spaces. In application context this is background fill plus foreground border, NOT the same foreground-only fill as style1.



Index2 shapeStyle fills interior with background color then draws foreground border. Plus sign joins two simultaneous style components; not a single line drawing tool, arithmetic or a request to fill a line. Preserve + separator.

Short phrase does not encode color roles, just as English does not; native reviewer must inspect swatches/preview and contrast all three styles.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L789-L790, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L271-L282

## string/ui_cursor_shape31

English: Cursor shape

Proposed XML: `<string name="ui_cursor_shape31">"የጠቋሚ ቅርጽ"</string>`

Status: review; lexical confidence medium-high compositional / draft only.

Android uses የጠቋሚ in Pointer speed/color/stroke labels and ጠቋሚ for hovering pointer. LO Shape → ቅርጽ. Original combination names pointer geometry rather than image/bitmap shape.



Visible label and Spinner contentDescription for Round/Square cursor marker. Changing it updates cursorShape, invalidates view and schedules autosave; marker uses cap override to choose circular/square outline independently of brushTip. It does not itself change painted brush-tip shape or document geometry.

Native review and consistency against existing cursor terminology required; no exact full-phrase primary attestation.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1526-L1538, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L292-L292, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L371-L371, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintroidCursorOverlay.kt#L35-L41, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintroidCursorOverlay.kt#L95-L112

## Source and evidence qualifications

Tool options build addChoice arrays, index selection changes brushTip/shapeStyle; addChoice opens a single-choice dialog, invokes action and updates button text. Cursor spinner is a separate consumer of Round/Square and uses cursorShape, not brushTip. Complete relevant classes are included.

No canonical English-source defect established. Shape nouns/adjectives refer to geometry; Fill + line is combined border/interior style. No numeric units or format strings in selected keys.

Round/Square exact line-cap records are nonfuzzy; full cursor compound and three-style phrases are compositions.

Calligraphy descriptive slanted-stroke phrase does not establish calligraphy terminology and remains held.

Solid fill is separately author-held because fill-only behavior paraphrase does not directly preserve solid/uniform wording; no alternative accepted.

Four prior pinned lexical snapshots were reused after hash verification against recorded provenance; only additional cui PO was newly fetched in this lexical task. Inherited fresh_pinned_bytes_match flags refer to prior provenance, not a claim of fresh retrieval of all five here.

Native preference, naturalness, runtime rendering and accessibility remain untested.

Primary records are in lexical-evidence/exact-records.json; full rationale/alternatives in lexical-evidence/README.md.

https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/02.po

https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml?format=TEXT

https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values/strings.xml?format=TEXT

https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po

https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po

Eleven complete source files; exact fresh commit/tree/blob binding, not exhaustive repository consumer search.

No native-speaker, runtime, glyph/layout, screen-reader or lifecycle acceptance.

No source edits, Work task, app builds/tests, CI or release.

Prior42 ready and Crop/Fit-caption holds excluded; Palette uncertainty, optional Horizontal and held Help unchanged.

Production remains12 present/705 missing of717. Previous42 ready and two held proposals remain unchanged; this group adds no independent acceptance or implementation.
