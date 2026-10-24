# Independent Amharic brush/shape review

Input seal: `3a6311a0e0131c7cf173fe27c755d8e465d26de9d3db3b6727609302697317e4`
Production: `66be61df27c5359bffc32d56db21f3949899f873`

**Result: retain 5, revise 0, hold 2. No production changes.**

“Retain” is exact-wording acceptance for this independent static translation review, not native-speaker, runtime or release acceptance. Prior 42 ready proposals and two earlier holds remain separate and unchanged.

## Exact decisions

### string/ui_round: RETAIN
- English: Round
- Reviewed candidate: "ክብ"
- Accepted wording: ክብ
- Fidelity: The same geometric word fits a round brush/line cap and a circular cursor marker. It adds no stroke-join promise and carries no numeric-rounding meaning in either menu.
- Idiom: A compact shape label, independently attested in the identical line-cap context. Retain the unmodified value rather than making it brush-specific, because the resource is shared with the cursor control.
- Confidence: {"source_fidelity": "high", "lexical_match": "high", "idiom": "medium-high; not native-validated"}
- Evidence:
  - LO cui messages.po lines 13187–13191: nonfuzzy linetabpage|liststoreCAP_STYLE, Round → ክብ.
  - LibreOffice Insert Shape help lists ክብ among geometry labels; supplementary live corroboration only.
- Consumer sources: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L785-L788, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1526-L1538, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L247-L258, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L292-L292, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintroidCursorOverlay.kt#L95-L112

### string/ui_square: RETAIN
- English: Square
- Reviewed candidate: "ስኴር"
- Accepted wording: ስኴር
- Fidelity: Names the SQUARE line cap and a square cursor-marker outline. Both consumers require geometry, not a square unit or exponent. The code keeps ROUND joins; this label need not and must not be expanded into a guarantee of square corners throughout the ink path.
- Idiom: The supplied spelling is attested as both the line-cap option and a square graphic object. This supports retaining it, not claiming it is the uniquely preferred everyday/native term. I found no evidence here that warrants replacing it with an unverified geometry alternative.
- Confidence: {"source_fidelity": "high", "lexical_match": "high attestation, not independent native preference", "idiom": "medium"}
- Evidence:
  - LO cui messages.po lines 13193–13197: nonfuzzy linetabpage|liststoreCAP_STYLE, Square → ስኴር.
  - LO svx messages.po lines 103–107: nonfuzzy STR_ObjNameSingulQUAD, Square → ስኴር.
  - LibreOffice Insert Shape help lists ስኴር in the common-shape sentence.
- Consumer sources: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L785-L788, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1526-L1538, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L247-L258, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintroidCursorOverlay.kt#L95-L112

### string/ui_calligraphy: HOLD
- English: Calligraphy
- Reviewed candidate: "ሰያፍ ጭረት"
- Accepted wording: None; held.
- Fidelity: ሰያፍ ጭረት describes orientation and a graphical mark, not the named calligraphic character/style. The Brush implementation stamps diagonal segments, but an implementation description cannot silently replace the English Calligraphy. Changing singular to plural would not restore the missing concept.
- Idiom: Components are interpretable, but neither their compositional grammar nor their implementation fit establishes the Amharic term for a calligraphic brush. No exact replacement is accepted by this review.
- Confidence: {"decision": "high", "source_semantics": "high", "submitted_value_as_translation": "low"}
- Evidence:
  - LO svx messages.po lines 79–83 supports Diagonal line; Android pointer_stroke_style supports graphical stroke vocabulary, not Calligraphy.
  - ClassicPaintActivity.kt lines 785–788 restricts this third choice to Brush; PaintCanvas.kt lines 507–526 implements repeated diagonal strokes.
- Next step: Find or independently validate an Amharic term conveying the calligraphic style in a brush context. Retain the English source unless a genuine source defect is separately established; then follow English-first, all-affected-locales review.
- Consumer sources: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L785-L788, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L507-L526

### string/ui_outline: RETAIN
- English: Outline
- Reviewed candidate: "ድንበር ብቻ"
- Accepted wording: ድንበር ብቻ
- Fidelity: In this three-choice shape-style control, Outline denotes the shape boundary without an interior fill. Border only is a faithful contextual rendering: only makes the exclusion already inherent in this Outline-versus-fill contrast explicit. Unlike fill only for Solid fill, it does not discard an independent modifier of the source.
- Idiom: ድንበር is attested for a graphical control border rather than solely a national boundary, and ብቻ follows the noun naturally as a restrictive particle. The full phrase is an original composition, not an exact phrase certified by LibreOffice. Do not import ረቂቅ merely because another context has the English Outline.
- Confidence: {"source_fidelity": "high in this consumer contrast", "lexical_match": "medium-high component support", "idiom": "medium"}
- Evidence:
  - LO help02.po lines 4312–4319: Border → ድንበር; following record describes a visible control frame.
  - LO cui messages.po lines 18591–18601 attests ብቻ in Only right/Only left.
  - PaintDocument.kt lines 271–282: style 0 skips the fill pass and draws the foreground stroke.
- Consumer sources: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L789-L790, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L271-L282

### string/ui_solid_fill: HOLD
- English: Solid fill
- Reviewed candidate: "መሙያ ብቻ"
- Accepted wording: None; held.
- Fidelity: መሙያ ብቻ replaces solid/uniform fill with absence of an outline. The implemented option indeed lacks an outline, but that fact does not translate the source adjective solid. The paraphrase could describe non-solid patterned fill just as well and therefore loses source meaning.
- Idiom: The submitted words are intelligible, but intelligibility and behavior contrast do not repair this fidelity gap. ሙሉ መሙያ is also not accepted: full/complete is not automatically the appropriate graphics sense of solid, and the supplied Solid record belongs to transparency rather than this shape-fill option.
- Confidence: {"decision": "high", "source_semantics": "high", "submitted_value_as_translation": "low"}
- Evidence:
  - LO svx messages.po lines 19823–19827 supports Fill → መሙያ.
  - LO svx messages.po lines 19955–20013 establishes that Solid → ሙሉ occurs inside a Transparency Type control.
  - PaintDocument.kt lines 271–282 fills style 1 with foreground and suppresses the outline; it does not make solid synonymous with only.
- Next step: Validate a wording that preserves solid/uniform fill as a graphics concept. Do not replace the English source with Fill only to rescue this translation. Any independently justified source change must precede an affected-languages review.
- Consumer sources: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L789-L790, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L271-L282

### string/ui_fill_line: RETAIN
- English: Fill + line
- Reviewed candidate: "መሙያ + መስመር"
- Accepted wording: መሙያ + መስመር
- Fidelity: Both component nouns and the additive relationship are preserved. Here line is the shape border, not an instruction to fill a line. The English does not spell out foreground/background roles, so leaving those implicit is faithful rather than an omission introduced by translation.
- Idiom: A concise noun-plus-noun UI label. The noun መሙያ matches a graphics-fill setting, and መስመር names a line; ASCII + and its surrounding spaces are preserved.
- Confidence: {"source_fidelity": "high", "lexical_match": "high components, composed phrase", "idiom": "medium-high"}
- Evidence:
  - LO svx messages.po lines 19823–19827 supports Fill → መሙያ.
  - LO svx messages.po lines 61–65 supports graphic-object Line → መስመር.
  - PaintDocument.kt lines 271–282: style 2 uses background interior plus foreground stroke.
- Consumer sources: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L789-L790, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L271-L282

### string/ui_cursor_shape31: RETAIN
- English: Cursor shape
- Reviewed candidate: "የጠቋሚ ቅርጽ"
- Accepted wording: የጠቋሚ ቅርጽ
- Fidelity: Names the geometry of the drawing-position marker. The code changes cursorShape and overrides the overlay cap independently of brushTip; the label must not be rewritten as Brush shape or Image shape.
- Idiom: The genitive compound follows the Android የጠቋሚ pattern and uses the attested shape noun ቅርጽ. A graphical pointer term is appropriate here, unlike a text-caret-only term. No competing Amharic cursor vocabulary appears among the 12 supplied production entries; wider pending proposals were outside this review.
- Confidence: {"source_fidelity": "high", "lexical_match": "medium-high components", "idiom": "medium-high; composed phrase"}
- Evidence:
  - Android values-am/strings.xml lines 2020, 2077 and 5413 support pointer/stylus-pointer vocabulary paired with supplied English records.
  - LO svx messages.po lines 517–521 supports Shape → ቅርጽ.
  - ClassicPaintActivity.kt lines 1526–1538 uses this value as visible label and Spinner contentDescription. PaintCanvas.kt lines 292 and 371 passes independent cursorShape caps to the overlay.
- Consumer sources: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1526-L1538, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L292-L292, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L371-L371, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintroidCursorOverlay.kt#L35-L41, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintroidCursorOverlay.kt#L95-L112

## Important consumer qualification

The shape-style contrast is conditional on a fill-capable shape. Open Polygon dispatches as PaintTool.LINE for preview (PaintCanvas.kt:276) and commit (445); PaintDocument.drawShape excludes LINE/CURVE from interior fill and always strokes them. Do not claim that choosing Solid fill fills an open polygon. This qualification is not an English-source defect finding.

## Verification and limits

- Verified input manifest seal, all 27 file SHA-256 values, all 11 Git blob IDs, all seven exact English values/source hashes/proposal hashes/missing-key states, and all 36 lexical records. Selected PO records are nonfuzzy.
- Source windows are preserved in inspected-consumer-excerpts.json; exact input bindings remain sealed in input-manifest.json and verification.json.
- Primary localization records demonstrate usage, not correctness or native acceptance. Nonfuzzy means the record is not marked fuzzy; it is not a quality certification. Round and Square have exact same-domain evidence; the other retained phrases are component-based compositions. Full source files were inspected at the pinned snapshot, not an exhaustive repository-wide consumer search.
- No source change is proposed or silently incorporated. The two holds are translation-fidelity failures, not proof the English source is defective. If a source defect is later established, correct English, flag affected languages, then review them one by one.
- No Work task, builds, CI, release, external publication, or source-language edit.
- No native, rendering, accessibility or lifecycle acceptance is claimed.

Supplementary [LibreOffice shape vocabulary](https://help.libreoffice.org/latest/am/text/shared/menu/insert_shape.html) corroborates the round/square geometry usage; the pinned records remain the decisive lexical evidence.
