# Amharic foreground/background colour-role drafts

Three live missing-label proposals, excluding prior 86 ready and 12 held proposals. Swap colors is a tentative author-side HOLD for idiomatic review, not a ready candidate or an already adjudicated additional hold. No accepted additions or implementation; production remains 12 present / 705 missing of 717 translatable containers.

## string/ui_foreground_colour

English: Foreground colour

Proposed XML: `<string name="ui_foreground_colour">"የፊት ለፊት ቀለም"</string>`

Title of the normal foreground colour editor and one part of combined foreground/background status contentDescription. Foreground is the current opaque drawing colour used by ordinary strokes, flood fill, shape outlines/most fills and text, rather than a distinct image layer.

Qualification: Does not select/reorder a front layer, describe photographic foreground depth, change all existing pixels or promise immediate painting. Current value may preview before confirmation. Short FG caption and hex-specific Edit colour accessibility templates are separate untranslated resources.

Evidence and confidence: {"key": "ui_foreground_colour", "english": "Foreground colour", "value": "የፊት ለፊት ቀለም", "confidence": "medium; source-backed normalized draft, not accepted", "evidence_ids": ["lo_pattern_foreground", "gimp_foreground_rgb"], "rationale": "LibreOffice pattern-colour control directly attests the full colour-role phrase. Remove its terminal colon and normalize spaces after the genitive prefix and within ለፊት, with GIMP non-fuzzy RGB foreground status supporting ፊት ለፊት as a colour role. Not based on layer stacking. The normalization and AN-Paint idiomatic fit require independent review.", "status": "draft for review, not production acceptance"}

## string/ui_background_colour

English: Background colour

Proposed XML: `<string name="ui_background_colour">"የመደብ ቀለም"</string>`

Title of normal background-colour editor, combined status description, and existing custom-slot context-menu action assigning that swatch to document.background. Background is current opaque secondary/erase/fill colour, not a layer.

Qualification: Changing property alone does not repaint the whole existing image. It is used by subsequent erasing/clearing/new canvas/fill operations and some geometry previews; not OS wallpaper or app theme. Existing ui_edit_background inherited wording is reference history, not new acceptance.

Evidence and confidence: {"key": "ui_background_colour", "english": "Background colour", "value": "የመደብ ቀለም", "confidence": "medium-high lexical; normalized draft, not accepted", "evidence_ids": ["lo_pattern_background", "lo_background_colour", "gimp_background_rgb"], "rationale": "Exact non-fuzzy LibreOffice colour-role noun phrase with genitive-prefix space removed; pattern-control evidence is not layer stacking. GIMP RGB status corroborates መደብ. Existing ui_edit_background is inherited context, not new acceptance and is unchanged.", "status": "draft for review, not production acceptance"}

## string/ui_swap23

English: Swap colors

Proposed XML: `<string name="ui_swap23">"ቀለሞችን ያለዋውጡ"</string>`

Colour dock button exchanges the two current document colour properties via a temporary variable, then refreshes status, invalidates canvas and schedules autosave.

Qualification: Swaps current foreground/background colours only, not arbitrary palette slots, image layers, pixel colour inversion, black/white reset or selected pixels. Existing pixels are not rewritten by the callback; invalidation can affect previews. No forced colour reversal terminology from fuzzy exchange evidence.

Evidence and confidence: {"key": "ui_swap23", "english": "Swap colors", "value": "ቀለሞችን ያለዋውጡ", "confidence": "low-to-medium compositional; HOLD pending idiomatic review", "evidence_ids": ["aosp_swap_buttons", "lo_colours", "aosp_colours"], "rationale": "Compose LibreOffice plural colours with the accusative ending ን and preserve the exact AOSP swap verb from swapping the two mouse-button roles. This role-exchange context is closer than character replacement. AOSP verb spelling/register is not independently validated here, and the complete phrase is unattested; do not force acceptance. The action exchanges foreground/background properties, not pixels, layers or RGB inversion.", "status": "HOLD; candidate only; native/independent review needed"}

## Source and scope qualifications

Foreground/background refer to current opaque drawing/secondary colours, not layer order, photographic depth, application theme or OS wallpaper. Setting either property does not itself recolour all existing pixels. Foreground serves ordinary drawing, fill and text; background serves erase, clear/new-canvas and selected background-fill operations. The same Background colour noun label also assigns a custom swatch via its context menu. Swap colors exchanges these properties, refreshes status/canvas previews and schedules autosave, not pixel inversion or black/white reset.

Both colour-role labels also occur in a combined status contentDescription joined by an external slash. Their independent review does not certify the full spoken combination, FG/BG abbreviations or hex-specific edit templates. Existing Amharic Edit background is retained as historical production text, not new linguistic acceptance. Palette uncertainty and all previous held proposals remain untouched.

Initial candidate discovery excluded ui_swap_foreground_background and ui_edit_foreground after finding no direct live references in the bounded source. Actual live swap is ui_swap23. Exclusion does not certify global dead code or review those resources. No English defect established, no hidden source rewrite.

12 complete current source files with exact Git blob/SHA-256 bindings are supplied. Fresh develop ref/commit/tree verify 66be61df27c5359bffc32d56db21f3949899f873 / 870c5a584120d92710be516af0dc3b3847b183d9. Six exact references across three direct caller files. Historical discovery rebound to complete current files; not a fresh exhaustive repository search. Lexical sources preserve exact original pairs, adaptation/composition notes, fuzzy exclusions and immutable provenance; reused snapshots are not new retrieval.

No placeholders, units or ellipses in the three target labels. No human native-reader approval, runtime/rendering, spoken-accessibility or whole-language acceptance. No Work task, production edits, app builds, CI or release. Prior 86 ready/12 held and zero implementation remain unchanged.
