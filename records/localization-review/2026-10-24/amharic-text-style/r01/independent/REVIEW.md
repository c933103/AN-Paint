# Independent review: six Amharic text-style labels

Date: 2026-10-24. Result: **4 retain, 2 revise, 0 hold; 0 implemented**.

This is an independent, evidence-based AI translation review, not native-speaker certification or application acceptance. Four original drafts have a retain recommendation. The two revised values below are exact review recommendations to reconcile with the author, not unchanged-draft acceptances. The thirteen earlier drawing/editing additions are separate and have not been re-reviewed or duplicated.

## Exact decisions

| Key | Decision | Reviewed target value | Semantic confidence | UI/orthographic confidence |
|---|---|---|---|---|
| string/ui_font | Retain | ቅርጸ ቁምፊ | High | Medium-high |
| string/ui_font_family | Revise | የቅርጸ ቁምፊ ዝርያ | High | Medium |
| string/ui_bold | Retain | ማድመቂያ | High | Medium-high |
| string/ui_italic | Retain | ማዝመሚያ | High | Medium-high |
| string/ui_underline | Revise | ከስሩ ማስመሪያ | High | Medium |
| string/ui_strikethrough | Retain | በላዩ ላይ መሰረዣ | Medium-high | Medium |

Recommended XML values, preserving the artifact's Android-resource quoting convention:

```xml
<string name="ui_font">"ቅርጸ ቁምፊ"</string>
<string name="ui_font_family">"የቅርጸ ቁምፊ ዝርያ"</string>
<string name="ui_bold">"ማድመቂያ"</string>
<string name="ui_italic">"ማዝመሚያ"</string>
<string name="ui_underline">"ከስሩ ማስመሪያ"</string>
<string name="ui_strikethrough">"በላዩ ላይ መሰረዣ"</string>
```

### string/ui_font: retain

This is the visible heading for the typeface selector, not font size or entered text. The [ICT Development Office / Ethiopian Languages Research Center glossary, p108, entry 1283](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf#page=108) directly supports the core phrase. The short nominal label fits its heading role. Do not add wording promising glyph support or a particular appearance. Consumer: [TextStyleDialog.kt, lines 37-39](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L37-L39).

### string/ui_font_family: revise one character

Original: የቅርፀ ቁምፊ ዝርያ. Recommended: የቅርጸ ቁምፊ ዝርያ.

The glossary's entry 1287 supports the family phrase, but its font-related entries alternate the root's spelling. I recommend using the same ቅርጸ root as the adjacent Font heading. This is an explicit local consistency decision, not a claim that the attested ፀ form is meaningless, belongs to another language, or is universally incorrect. The selected value retains the family distinction and remains a nominal accessibility label for the same selector. [Glossary p108](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf#page=108); [spinner consumer, line 38](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L38).

The change is U+1340 (ፀ, ETHIOPIC SYLLABLE TZA) to U+1338 (ጸ, ETHIOPIC SYLLABLE TSA). They are distinct characters, not uppercase/lowercase forms. Do not apply a catalogue-wide character replacement or present this editorial choice as Unicode normalization. Natural spoken control wording has not been tested with Amharic screen-reader users.

### string/ui_bold: retain

[LibreOffice's Amharic Bold help](https://help.libreoffice.org/latest/am/text/shared/01/05110100.html) uses this exact function label and describes switching bold formatting on and off. In this dialog it belongs to a group of text-formatting checkboxes and contributes Typeface.BOLD, not highlighting, brightness, bravery, or a color operation. A function noun is acceptable here; an adjective-only translation is not required. No evidence justifies replacing the attested form with an invented synonym. [Consumer, lines 49-75](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L49-L75).

### string/ui_italic: retain

[LibreOffice's Amharic Italic help](https://help.libreoffice.org/latest/am/text/shared/01/05110200.html?DbPAR=WRITER&System=UNIX) independently confirms the exact label in text-formatting context. It pairs naturally in register with Bold. The checkbox contributes Typeface.ITALIC and can combine with Bold; it does not rotate the whole text object or select Italian. Actual italic-face availability or synthesis is a rendering matter, not something this label guarantees. [Consumer, lines 49-75](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L49-L75).

### string/ui_underline: revise spacing only

Original: ከ ስሩ ማስመሪያ. Recommended: ከስሩ ማስመሪያ.

Retain the lexical choice supported by [LibreOffice Font Effects](https://help.libreoffice.org/latest/am/text/shared/01/05020200.html), but join the bound ከ- prefix to its host. [Baker and Kramer, 2014, section 3, p145, example 13 and following discussion](https://sites.rutgers.edu/mark-baker/wp-content/uploads/sites/199/2019/07/amharic-preps-as-case-offprint.pdf#page=6) analyzes this prefix as host-dependent and explicitly illustrates its combination with the under/beneath expression. Joining is my orthographic recommendation from that linguistic evidence, not a claim that the paper prescribes this exact UI string or that LibreOffice already uses the joined form.

The label still denotes text underlining, not the line-drawing tool. Its control sets a text-decoration flag. It must not promise a line at the absolute screen bottom in vertical text. [Consumer, lines 50-75](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L50-L75). The explicit spacing revision replaces, rather than silently copies, the draft's source-spacing preference.

### string/ui_strikethrough: retain

[LibreOffice Font Effects](https://help.libreoffice.org/latest/am/text/shared/01/05020200.html) gives this exact label in its strikethrough section and separately names overlining. That separation is important evidence against reading this as an overline label. In the app's parallel text-style group it selects a decoration flag; it does not delete input characters, erase pixels as an eraser tool, or discard a document. The familiar formatting context is sufficient to retain the term, but its everyday erasing sense makes idiom confidence lower than Bold/Italic. A native usability review could still favor a different phrase. [Consumer, lines 50-75](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L50-L75).

## Checkbox register

All four style values are parallel function nouns rather than a mixture of commands and state sentences. Microsoft's [Amharic Style Guide, p42](https://download.microsoft.com/download/6/2/a/62a993f1-d3b2-4f28-b3e7-22965eb91426/amh-eth-styleguide.pdf#page=42) permits nouns or conjugated verbs for checkbox labels. That supports the grammatical register, not automatic approval of every LibreOffice translation. The guide is Microsoft-specific and historical (2011). Its Amharic text extraction is unreliable, so I used the rendered page to verify the relevant English guideline rather than copying corrupted extracted examples. Checkbox grouping and checked-state semantics here are independently established by the app source.

## Provenance and source semantics

- Input MANIFEST SHA-256 is exactly ac4e39f97d763adf13f19623917b2125904fdd8f0e765d3aba22d7bc79b09d88; all four listed input-file digests match.
- Target is commit 66be61df27c5359bffc32d56db21f3949899f873. All nine complete local source files independently reproduce their SHA-256 and Git blob SHA-1 bindings. All nine were also independently retrieved by exact path and commit using GitHub, returning those same blob identities. This verifies the pinned snapshot, not that the branch can never advance. See source-verification.json and fresh-github-retrieval.json.
- Exact English labels match the draft. All six exact keys are absent from the twelve-entry Amharic catalogue. None has placeholders or plurals. Existing resources and coverage are unchanged.
- [FontCatalog.kt, lines 19-41](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/FontCatalog.kt#L19-L41) builds system and bundled choices, applies requested typeface styling and reserves script fallback handling for the default selection. It does not make every chosen font support all scripts.
- [TextStyleDialog.kt](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt) supplies the same chosen typeface and decoration settings to preview and commit. [ClassicPaintActivity.kt, lines 1064-1071](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1064-L1071) passes them onward.
- [PaintDocument.kt, lines 482-497](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L482-L497) sets isUnderlineText/isStrikeThruText and draws rather than deleting the supplied text. [VerticalText.kt, lines 96-125](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/VerticalText.kt#L96-L125) copies Paint into TextPaint and uses shaped layout in horizontal/vertical paths. This is source-path verification, not proof of every rendered appearance.
- UiText.kt and LocaleText.kt were inspected as resolution plumbing. No surrounding hints or complete composed accessibility experience are accepted here.

## Evidence qualifications and stopping boundary

The glossary is a primary-authored ICT/ELRC document hosted on a third-party mirror; its publication date was not established. Page 108 was downloaded, rendered and visually inspected, confirming that the variant spellings really appear in the Amharic column rather than arising solely from extraction. LibreOffice pages were independently reopened; they contain some English fallback and are terminology precedent, not a native acceptance record. The Italic URL with query parameters worked after the bare URL produced a cache-miss error. The failed web PDF screenshot was recovered by direct PDF download and local rendering. No access denial occurred.

No English-source defect was established for these six. If a later review establishes one, the correct workflow remains to correct English, flag affected terms across languages, and review them in turn. These two target-language editorial recommendations do not trigger that source-defect workflow.

No application source or production resources were edited. No app build, app test, CI, release, remote publication, Work task, native-speaker test, glyph-coverage/layout test or screen-reader certification was performed. Font names/licences, direction/orientation, size/spacing, prior thirteen drawing/editing additions, Palette uncertainty, optional Horizontal punctuation, full Help and other held work remain separate. Reference PDFs and rendered inspection images are not bundled for republication. The review is complete; reconciliation of the two revised candidates is the next bounded translation step.
