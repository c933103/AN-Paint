# Independent Amharic tool-caption review

Result: **1 retain, 0 revise, 3 hold**. No implementation. These are new, separate decisions; the prior **90 ready / 14 adjudicated holds** are unchanged.

The input manifest seal is `958dec487b0944490be4af61d4a8e445b2199b50418027ec29afbe1f0420426d`. All 47 covered files match; there are 48 files including the manifest. All 15 complete project-source files match their supplied Git-blob identities at commit `66be61df27c5359bffc32d56db21f3949899f873`. The reviewer did not make a fresh remote develop lookup. Twelve usable PO records and all 18 excluded GIMP records were independently compared with the original snapshots. The four glossary terms were checked visually in their correct Amharic columns.

## Per-key decisions

### ui_rectangle_select — HOLD

English: Rectangle select

Candidate: በቀጤ ጎነ አራት መምረጫ

The components and rectangular image-area meaning are supported. The new method/shape construction is not itself attested. The evidence does not settle whether the geometry phrase plus በ- and selector head is an idiomatic tool caption, rather than selection by or of a geometric object. No demonstrated mistranslation is asserted; do not replace it with another unvalidated composition merely to remove a hold.

Confidence: source semantics: high, component attestation: high, semantic composition: medium, whole phrase idiom: insufficient to pass.

Next step: Validate the whole caption with an Amharic reviewer in the rectangular image-area selection context, or obtain a stronger primary whole-caption precedent. Preserve distinction from drawing a rectangle.

Evidence: [ict_rectangle](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf#page=188), [lo_selection_mode](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/02.po), [lo_select_all](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po). Exact contexts, lines and source hashes are in review.json.

### ui_free_form_select — HOLD

English: Free-form select

Candidate: በስድ ቅርጽ መምረጫ

The glossary component denotes drawn freeform geometry, not freeware or free price. The proposed composition plausibly names selecting by that outline, but source attestation for the complete selection caption and its naturalness are absent. A line-creation caption would change the operation and is not an acceptable substitute.

Confidence: source semantics: high, component attestation: high, semantic composition: medium, whole phrase idiom: insufficient to pass.

Next step: Validate the complete area-selection caption, explicitly distinguishing a freehand closed selection boundary from a freeform line drawing tool.

Evidence: [ict_freeform](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf#page=113), [lo_selection_mode](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/02.po), [lo_select_all](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po), [lo_freeform_behavior](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/02.po). Exact contexts, lines and source hashes are in review.json.

### ui_bucket_fill — HOLD

English: Bucket fill

Candidate: ቀለም መሙያ

The exact phrase is a Fill Color precedent, not a Bucket fill precedent. Colour filling is a real part of the target action, so this is not an unrelated or proven false rendering. However, it generalizes a specific flood-fill tool into a label also supported for an object area-colour control. Omitting the bucket metaphor is not automatically wrong, and a short caption need not spell out contiguity or tolerance. The actual unresolved question is whether the phrase is a natural functional equivalent identifying this tool, including as a standalone accessible name, rather than a fill-colour setting. The supplied evidence does not establish that transfer.

Confidence: source semantics: high, exact Fill Color attestation: high, Bucket fill fidelity: plausible but insufficient, tool setting distinction: unvalidated.

Next step: Obtain a validated idiomatic bucket/flood-fill caption or validate this functional equivalent specifically against colour and shape-fill controls. Do not silently relabel English as Fill Color. If the product intentionally changes the English term, correct English first and flag affected translations across languages.

Evidence: [lo_fill_color](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po), [ict_fill](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf#page=104), [ict_fill_color](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf#page=104). Exact contexts, lines and source hashes are in review.json.

Context corroboration: [LibreOffice Drawing Bar](https://help.libreoffice.org/latest/en-US/text/sdraw/main0210.html). Its Fill Color action sets object area colour, not a raster flood-fill operation.

### ui_eyedropper — RETAIN

English: Eyedropper

Candidate: ጠብታ መለኪያ

Retain for this bounded short-caption review. This is an exact non-fuzzy Pipette caption in a primary software translation source, and the adjacent control help specifically instructs clicking a colour in an image. That is a close match to the relevant sampling action, unlike borrowing the containing Color Replacer dialog label. The English Eyedropper is itself a physical-tool metaphor; the possibility of a literal drop-measurement reading is not by itself evidence of a mistranslation. Moving the sampled value into foreground rather than a replacement-source colour box changes downstream use, not the sampling-tool metaphor. The second Pipette context corroborates spelling only, because its actual operation selects matching-colour bitmap parts. It is not counted as independent evidence for foreground sampling.

Confidence: exact analogous software caption: high, sampling control fidelity: medium-high, modern native preference: not certified, overall bounded review: medium-high.

Next step: No replacement is required by this source/semantic review. Prefer this attested sampling-control term over an unvalidated descriptive composition. Keep native-reader preference, rendering and larger composed strings as separate unperformed checks.

Evidence: [lo_pipette](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po), [lo_pipette_behavior](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po), [lo_pipette_other_context](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po), [lo_pipette_other_context_behavior](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po). Exact contexts, lines and source hashes are in review.json.

## Verified source semantics and one important correction

- Rectangle selection extracts pixels within sorted and clipped drag bounds. Free-form selection closes the traced outline and clips extraction by that path. Neither label means drawing the named geometry. Creating a selection is not itself lifting the pixels, but previous floating work may commit, and subsequent movement/resizing/rotation changes image pixels.
- Bucket fill traverses the seed-connected region using horizontal runs and adjacent rows. Pixel acceptance compares squared RGBA distance to the original seed against squared integer tolerance. It is not a disconnected global colour replacement or an image-area percentage.
- Eyedropper samples one bounds-checked bitmap pixel into foreground, not a general palette/dialog choice or neighbourhood average. The foreground setter forces opaque alpha; this caption review does not promise sampled transparency preservation.
- **Correction to the review context:** choosing any tool calls applyPending; that method always calls finishSelection. Committing a floating selection is not restricted to leaving SELECT/LASSO. It can occur when choosing a selection tool or reselecting the current tool.

Source anchors: [tool choice](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L153-L157), [pending commitment](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L443-L449), [pointer-up operations](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L810-L816), [selection extraction](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L289-L306), [floating selection mutation](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L313-L338), [fill traversal](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ScanlineFill.kt#L12-L54), [foreground setter](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L44-L47), [standalone tool accessibility label](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ToolButton.kt#L10-L11).

## Fidelity and boundaries

No English-caption defect is established. The Bucket fill hold concerns whether the proposed Amharic phrase is a faithful tool-specific equivalent, not whether a translation must mechanically reproduce every English metaphor or describe every algorithmic detail. Do not silently replace the English source with Fill Color. If English is intentionally revised, correct it first and track every affected language separately.

The Eyedropper retain decision is bounded and substantive: direct sampling-control precedent supports the metaphor, while native preference remains untested. It is not an assertion of native certification and does not accept the separate tooltip, status text or other composed strings. Unlike the held selection captions, it does not depend on inventing a new whole phrase.

The XML inventory reconciles to 716 translatable strings plus one plural resource: 717 units, 12 present in Amharic and 705 missing. All four reviewed keys remain absent. No production XML was modified.

This output contains only original assessment, bounded lexical terms, source metadata and links. The complete glossary PDF, page renders and full-page text remain local review material. Complete PO files are not redistributed here. GIMP fuzzy/empty entries were verified only to exclude them. Multiple LibreOffice files are one translation ecosystem, not independent authorities.

No Work task, application build, runtime/UI/accessibility test, production change, CI, release or remote write was performed. No external-action denial or uncertain mutation occurred. Held captions remain linguistic-evidence blockers, not tool-access blockers. Detailed per-key release conditions and confidence limits appear in review.json.
