# Amharic: six missing text-style labels, original draft only

Production `66be61df27c5359bffc32d56db21f3949899f873`; nine complete files match fresh GitHub commit/tree.

The13 previously reviewed drawing/editing candidates remain separate and unapplied. These six are new drafts, not accepted coverage.

## string/ui_font

English: Font
Proposed XML: `<string name="ui_font">"ቅርጸ ቁምፊ"</string>`

FontCatalog builds system choices plus bundled non-ui-only faces; the label does not guarantee every selected font supports every glyph.

Heading for the font selector, separate from Size(pixels). Use typography terminology rather than a word for text content or font size.

Confidence: semantic medium-high; UI idiom medium.

Independent check: Check standard typography spelling and consistency with Font family; no size meaning should be introduced.

Sources: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## string/ui_font_family

English: Font family
Proposed XML: `<string name="ui_font_family">"የቅርፀ ቁምፊ ዝርያ"</string>`

Spinner contentDescription identifies the selected typeface/family list. Explicit selection uses FontCatalog.face; default selection can choose a script fallback.

Use the exact glossary family phrase; this is the accessibility name of the same selector, not a separate family-of-people concept or size field.

Confidence: semantic high; UI idiom medium.

Independent check: Confirm concise natural spoken control label and consistency with Font. This is wording review, not screen-reader validation.

Sources: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## string/ui_bold

English: Bold
Proposed XML: `<string name="ui_bold">"ማድመቂያ"</string>`

Checkbox contributes Typeface.BOLD to style(); FontCatalog.faceForText returns the styled face used in preview and final document text.

First-party software formatting noun/action-label suits a checkbox state. It refers to heavier typeface styling, not courage, brightness, selected-text highlighting or changing colour.

Confidence: semantic high; UI idiom medium.

Independent check: Check checkbox idiom and distinction from highlighting. Rendering may depend on selected typeface; no font-weight guarantee is added.

Sources: [lo_bold](https://help.libreoffice.org/latest/am/text/shared/01/05110100.html), [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## string/ui_italic

English: Italic
Proposed XML: `<string name="ui_italic">"ማዝመሚያ"</string>`

Checkbox contributes Typeface.ITALIC, combinable with BOLD; style is passed through faceForText to preview and final commit.

Use first-party formatting label for slanted/italic type, not an instruction to rotate the whole text block or use Italian language. Same function-label register as Bold.

Confidence: semantic high; UI idiom medium.

Independent check: Confirm italic-style idiom, distinct from independent text direction/glyph rotation. No guarantee of a genuine designed italic face versus synthesized style.

Sources: [lo_italic](https://help.libreoffice.org/latest/am/text/shared/01/05110200.html), [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## string/ui_underline

English: Underline
Proposed XML: `<string name="ui_underline">"ከ ስሩ ማስመሪያ"</string>`

Checkbox sets TextSettings.underline and preview.underline. TextPreview and PaintDocument.text set Paint.isUnderlineText; VerticalText creates TextPaint from that Paint for layout/drawing.

Attested first-party formatting label denotes a line under text, not a separate line-drawing tool. Retain the source-attested spacing rather than silently normalizing words.

Confidence: semantic high; UI idiom medium.

Independent check: Check natural checkbox phrasing and spacing; underline follows shaped text, not an absolute bottom-of-screen annotation in all directions.

Sources: [lo_effects](https://help.libreoffice.org/latest/am/text/shared/01/05020200.html), [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## string/ui_strikethrough

English: Strikethrough
Proposed XML: `<string name="ui_strikethrough">"በላዩ ላይ መሰረዣ"</string>`

Checkbox sets TextSettings.strike and preview.strike. TextPreview/PaintDocument.text set Paint.isStrikeThruText; unchanged text goes through VerticalText layout.

Use first-party text-decoration label rather than infer deletion from the everyday erasing sense. The checkbox marks text with a strike; it does not remove characters or erase canvas content.

Confidence: semantic medium-high; UI idiom medium.

Independent check: Explicitly check whether this attested term is clear as line-through rather than overline or deletion in AN Paint; do not accept by dictionary equivalence alone.

Sources: [lo_effects](https://help.libreoffice.org/latest/am/text/shared/01/05020200.html), [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## Scope and limits

No English-source defect established for these six labels. If independent review establishes one, correct English in the proposed workflow and flag affected terms across all locales before translating; no silent code change.

- No production edits, app tests/builds, CI, release, remote publication or Work task.
- Primary lexical/software terminology is evidence, not automatic contextual/native acceptance.
- No rendering/layout/glyph-coverage/screen-reader certification.
- Nine complete source files bind to fresh GitHub commit/tree paths; no reliance on stale local git metadata.
- 12 existing Amharic resources and13 previously reviewed additions unchanged and nonoverlapping.
- Palette uncertainty and optional Horizontal punctuation remain separate.
- Font names, licences, hints, text direction/vertical orientation, size/spacing and complete composed accessibility excluded.
- All held full Help, warnings and other optional/held scopes unchanged.
- Production coverage remains12 present/705 missing of717. No new independent acceptance.

## Orthography and source qualifications

Glossary Font entry1283 (p108) uses ቅርጸ ቁምፊ; Font family entry1287 uses የቅርፀ ቁምፊ ዝርያ. The draft preserves those exact forms and flags ጸ/ፀ consistency for independent adjudication. Do not silently normalize. Four style toggles use the attested LibreOffice function-noun labels, with medium UI confidence. Amharic help includes English fallback; historical GTK style entries are all fuzzy. Neither establishes native acceptance. Glossary text extraction succeeded; screenshots were unavailable.
