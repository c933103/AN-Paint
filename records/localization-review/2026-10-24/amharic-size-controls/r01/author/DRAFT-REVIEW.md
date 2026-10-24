# Amharic size controls: original draft dossier

Production 66be61df27c5359bffc32d56db21f3949899f873; tree 870c5a584120d92710be516af0dc3b3847b183d9. Fourteen complete source copies are supplied, exact Git blobs checked against freshly retrieved production tree.

No independent acceptance or implementation. Prior47 ready/four held remain separate.

## string/ui_size_px

English: Size (px)

Proposed XML: `<string name="ui_size_px">"መጠን (px)"</string>`

Status: review

Confidence: high lexical; untested UI draft

Exact nonfuzzy Size → መጠን in graphics Position and Size UI. Append source literal (px), rather than localizing the unit. Generic size noun avoids promising that this shared parameter determines every mark dimension.

Separate Pencil size or shared stroke width, both1..100 pixels. Shared width is also shown for some tools where it is not the principal effective parameter (e.g. Spray uses fixed1px dots and its own radius). Do not promise that Size changes every mark dimension for every tool.

['Preserve literal (px).', 'Inspect each tool context: Pencil has independent size; most shared controls edit strokeWidth, while Spray still draws fixed 1px dots.', 'Native/contextual and visual-fit review remain outstanding.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L774-L784, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L247-L258, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L527-L537

## string/ui_radius_px

English: Radius (px)

Proposed XML: `<string name="ui_radius_px">"ራዲየስ (px)"</string>`

Status: review

Confidence: high lexical and matching corner-radius context; untested UI draft

Exact nonfuzzy Radius → ራዲየስ occurs in the LibreOffice rounded-rectangle corner-radius help. This is not diameter or rounding a number. The untranslated Radius → Radius measurement record is excluded.

Rounded-rectangle corner radius. Slider min0, max=max(64,half shorter bitmap dimension,current radius); geometry clamps radius to half shorter dragged rectangle dimension. Pixel units, not diameter.

['Preserve literal (px).', 'Rounded-corner geometry is clamped separately from slider maximum.', 'Loanword choice and native visual fit remain unaccepted.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L779-L782, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L411-L411

## string/ui_spray_radius_px

English: Spray radius (px)

Proposed XML: `<string name="ui_spray_radius_px">"የመርጫ ራዲየስ (px)"</string>`

Status: hold

Confidence: low compositional; terminology HOLD

Original composition meaning spray radius. Only Radius → ራዲየስ has eligible exact primary lexical evidence. The spray component መርጫ is an original draft, not an attested LibreOffice/AOSP term in this corpus. It refers to the random spray disk, not the dot width.

Random spray disk radius1..100 image pixels. Each1px point offset uses sqrt(random)*radius, uniformly distributed in disk. Point count max(8,integer radius) also changes. Not spray-dot width or diameter.

['TERMINOLOGY HOLD: no eligible primary attestation for Spray or Spray radius was established.', 'Do not treat the complete phrase as source-backed or release-ready.', 'Native review must confirm that መርጫ naturally names the spray tool rather than a selection/sprinkler sense.', 'Preserve literal (px), radius not diameter; point density/count also changes with radius.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L784-L784, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L527-L537

## string/ui_strength

English: Strength (%)

Proposed XML: `<string name="ui_strength" formatted="false">"ጥንካሬ (%)"</string>`

Status: review

Confidence: medium-high component evidence; original cross-context draft

AOSP color-correction Intensity → ጥንካሬ is an exact paired short label; signal and vibration strength phrases independently use the same noun. Reusing it for watercolor Strength is an original cross-context adaptation, not an exact painting translation. Consumer source confirms alpha strength in 1..100, so no unsupported opacity assumption is needed.

Watercolor Strength (%)1..100 controls paint alpha=(strength*255/100), not stroke width. Source has formatted=false and literal(%); preserve literal percent sign and formatting attribute. Composition via numeric slider remains outside wording acceptance.

['Preserve literal (%) and formatted="false".', 'Do not replace the visible source Strength with an independently invented opacity label.', 'Check native sense and consistency with neighboring watercolor terminology; no exact Strength (%) painting-source match.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L783-L783, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L247-L258

## string/ui_tolerance

English: Tolerance

Proposed XML: `<string name="ui_tolerance">"ገደብ"</string>`

Status: review

Confidence: high lexical; same color-difference family, different algorithm

Exact nonfuzzy graphics Tolerance → ገደብ is used for accepting a color range. The app uses connected flood fill with an absolute Euclidean ARGB distance, not LibreOffice global color replacement. Transfer only the noun, not the source algorithm or percentage unit.

Bucket fill tolerance0..100 is absolute Euclidean ARGB component-distance threshold from seed color (squared distance<=tolerance squared), not a percentage. Zero requires exact color. Connected scanline flood fill, not global color replacement.

['Do not add (%) or infer percentage from a 0..100 range.', 'LibreOffice color-tolerance percent help retained as exclusion evidence, NOT applicable app semantics.', 'Native clarity of short generic threshold/limit word remains unaccepted.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L767-L767, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L260-L267, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ScanlineFill.kt#L11-L50

## string/ui_original_size34

English: Original size

Proposed XML: `<string name="ui_original_size34" formatted="false">"ዋናው መጠን"</string>`

Status: review

Confidence: high lexical; untested selection-action draft

Nonfuzzy crop-page _Original Size → _ዋናው መጠን; remove the foreign desktop accelerator underscore only. Selection action restores retained source-image dimensions, not position, rotation, or arbitrary prior edits. The alternate help spelling ዋነኛው መጠን is retained rather than silently treated as identical.

Selection action restores floating selection rectangle width/height to retained source-image pixel dimensions, keeps rectangle center and rotation; startMovingSelection may lift pixels/establish history first. Does not restore original location or undo edits. Caller then fits viewport. formatted=false preserved.

['Preserve formatted="false".', 'Do not imply undo, original location, original rotation or viewport zoom reset.', 'Native preference between attested variants and action clarity require review.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L758-L760, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L415-L422

## string/ui_lock_proportions

English: Lock proportions

Proposed XML: `<string name="ui_lock_proportions">"ተመጣጣኝነት መጠበቂያ"</string>`

Status: review

Confidence: medium-high same-function component phrase; original shortened draft

Original concise phrase built from exact nonfuzzy LO proportions-preserving resize prose, including the contiguous phrase ተመጣጣኝነት መጠበቂያ. Chooses preserve proportions rather than a security-lock noun. It keeps the current gesture-start aspect ratio, not necessarily the original image ratio.

Checkbox toggles lockSelectionAspect for selection corner/edge resize gestures. Keeps current rectangle aspect ratio, not necessarily source-image ratio after earlier distortion. It does not lock movement, rotation or dimensions, and does not retroactively restore ratio. Handler saves state.

['Full English Lock proportions short-label equivalent was NOT established in the primary corpus.', 'The LO Keep ratio → መጠን መጠበቂያ alternative could misleadingly suggest keeping fixed size; do not automatically adopt it.', 'Do not imply frozen position, rotation, or dimensions, or retroactive correction of prior distortion.', 'Native grammar, checkbox-state clarity and width/fit review remain unaccepted.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L761-L764, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L617-L642, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/SelectionGeometry.kt#L25-L67

## Shared scope and evidence limits

ClassicPaintActivity.addSlider creates NumericSlider; label is used in visible number template, slider contentDescription, numeric dialog title and composed input hint. NumericSlider formats integer values separately. Related formatter/hint strings are NOT drafted or accepted here. Activity callbacks invalidate and schedule autosave. Selection labels use button/checkbox contexts. Full source copies supplied, no runtime/accessibility claim.

No English defect established in this bounded label scope. Size has tool-specific effectiveness limits and Tolerance is not percent; preserve current English meaning rather than silently rewrite. Any real source correction must be English-first and flag all affected locales.

(px) and (%) preserved literally; formatted=false retained for Strength and Original size. No printf placeholders in selected values; surrounding NumericSlider formatter/accessibility templates remain excluded.

Full lexical reasoning, exact records, source snapshots and retrieval/reuse limitations are in lexical-evidence/. Nonfuzzy is a record flag, not proof of correctness. Component and cross-context evidence does not establish exact full-phrase native acceptance.

Original drafts only, independent checking required.

Prior47 ready and4holds excluded; inherited Palette/Horizontal/Help remain unchanged.

Source-only bounded consumer inspection, not native, rendered, accessibility or lifecycle acceptance.

Production remains12 present/705 missing of717. No production changes, builds, CI, release or Work task.
