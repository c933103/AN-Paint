# Amharic colour-selector action/caption drafts

Five original missing-label drafts, separate from prior 81 ready and 12 held proposals. No implementation or accepted additions; production remains 12 present / 705 missing of 717 translatable containers.

## string/ui_basic_colours

English: Basic colours

Proposed XML: `<string name="ui_basic_colours">"መሰረታዊ ቀለሞች"</string>`

Section caption above built-in 48-swatch grid:16 predefined RGB colours plus32 HSV-derived colours. A swatch click updates current ColourValue and syncs the preview; it does not by itself save a custom slot.

Qualification: Basic denotes supplied standard choice set, not a scientific primary-colour-only set or elementary colour theory. Caption, not action; plural retained.

Evidence and confidence: {"key": "ui_basic_colours", "english": "Basic colours", "value": "መሰረታዊ ቀለሞች", "confidence": "medium compositional; draft only", "evidence_ids": ["lo_basic", "lo_basic_shapes", "lo_colours", "aosp_basic_info", "aosp_colours"], "rationale": "Compose the exact LibreOffice Basic adjective with its exact Colours plural. Non-programming effects and geometric-shapes labels supply the ordinary basic sense. Here it labels the built-in swatch group, not a scientific set of primary colours.", "composition_limits": ["The full phrase is unattested in these records; generic basic may carry a primary-colour reading for some readers, so assess that ambiguity explicitly. The AOSP spelling መሠረታዊ and plural ቀለማት are source-backed alternatives, not corrections silently imposed on LibreOffice.", "Original author-composed phrase, not an exact full-phrase source translation or native-reader approval.", "Primary records establish component usage in their source products, not AN-Paint suitability. Independent contextual and native-language review, rendering and accessibility validation remain required.", "No production resources, builds, CI, remote records or held translations changed."], "status": "source-backed candidate for independent review; not accepted", "consumer_context_supplied_by_coordinator": "Labels the 48 built-in swatches, not scientific primary colours."}

## string/ui_selected_colour23

English: Selected color

Proposed XML: `<string name="ui_selected_colour23">"የተመረጠው ቀለም"</string>`

Caption beside current sample preview. The sample draws value.colour; sync invalidates it after current selection/field changes. The selected value may be provisional before final acceptance.

Qualification: Selected is a current-state description, not Select colour imperative, not original colour or saved palette colour. Invalid field input may retain last valid preview. No rendering outcome certified.

Evidence and confidence: {"key": "ui_selected_colour23", "english": "Selected color", "value": "የተመረጠው ቀለም", "confidence": "medium compositional; draft only", "evidence_ids": ["lo_selected_object", "lo_selected_preview", "lo_colour", "aosp_selected"], "rationale": "Compose a singular attributive selected-colour noun phrase for the current preview label. LibreOffice attests the selected-object relative form; replace the object with exact Color. Remove its accusative suffix ን because the label is not the object of a verb.", "composition_limits": ["This involves grammatical composition, including the nominative relative form and noun substitution. AOSP Selected → ተመርጧል is a standalone state sentence and is not copied as a modifier. Does not imply a saved custom slot or final application.", "Original author-composed phrase, not an exact full-phrase source translation or native-reader approval.", "Primary records establish component usage in their source products, not AN-Paint suitability. Independent contextual and native-language review, rendering and accessibility validation remain required.", "No production resources, builds, CI, remote records or held translations changed."], "status": "source-backed candidate for independent review; not accepted", "consumer_context_supplied_by_coordinator": "Labels the current valid preview, which may be provisional until Use colour."}

## string/ui_add_colour26

English: Add colour

Proposed XML: `<string name="ui_add_colour26">"ቀለም አክል"</string>`

Colour-tab Add colour opens custom-slot workflow. First empty slot is selected; if full, user chooses a slot to replace. In a new-slot dialog the same label serves title and positive action. After valid fields, positive callback stores current opaque colour, refreshes palette and makes it foreground.

Qualification: Not paint/add pixels immediately, not adding a new layer. Outer action opens dialog; inner action commits. Full-palette route may replace existing slot; no promise of increasing slot count. Separate Add to palette key is outside scope.

Evidence and confidence: {"key": "ui_add_colour26", "english": "Add colour", "value": "ቀለም አክል", "confidence": "medium compositional; draft only", "evidence_ids": ["aosp_add", "aosp_add_account", "aosp_colour", "lo_add"], "rationale": "Compose AOSP Color plus its exact imperative Add. The object-before-verb pattern is independently present in Add account. Targets adding a custom colour slot, not adding a palette, document or colour effect.", "composition_limits": ["No exact Add colour pair is claimed. LibreOffice nominal-action መጨመሪያ is a source-backed alternative but the AOSP imperative matches the Android action-button approach.", "Original author-composed phrase, not an exact full-phrase source translation or native-reader approval.", "Primary records establish component usage in their source products, not AN-Paint suitability. Independent contextual and native-language review, rendering and accessibility validation remain required.", "No production resources, builds, CI, remote records or held translations changed."], "status": "source-backed candidate for independent review; not accepted", "consumer_context_supplied_by_coordinator": "Outer action opens the custom-colour slot editor. A full palette asks which slot to replace; this label must not promise immediate allocation or saving."}

## string/ui_edit_colour26

English: Edit colour

Proposed XML: `<string name="ui_edit_colour26">"ቀለም አርትዕ"</string>`

Menu action for an existing saved custom-colour cell, and title for replacement dialog. Choosing it calls addColour(index), initializes existing colour and passes replacingPaletteColour=true; positive button in that mode is separately labeled Save.

Qualification: Edits chosen saved swatch, not every pixel of that colour, whole-image colour adjustment or text formatting. Title/action share resource; retain functional editing semantics.

Evidence and confidence: {"key": "ui_edit_colour26", "english": "Edit colour", "value": "ቀለም አርትዕ", "confidence": "medium compositional; draft only", "evidence_ids": ["aosp_edit", "aosp_edit_word", "aosp_colour", "lo_edit"], "rationale": "Compose AOSP Color with the exact Edit action. Edit word corroborates object-before-verb order. It edits the custom colour value/slot; it does not mean choose a palette or alter all image colours.", "composition_limits": ["The specific-colour definite/accusative alternative ቀለሙን አርትዕ may be more natural in context; the proposed bare object matches the short English label but needs native review. LibreOffice ማረሚያ is a different nominal-action convention.", "Original author-composed phrase, not an exact full-phrase source translation or native-reader approval.", "Primary records establish component usage in their source products, not AN-Paint suitability. Independent contextual and native-language review, rendering and accessibility validation remain required.", "No production resources, builds, CI, remote records or held translations changed."], "status": "source-backed candidate for independent review; not accepted", "consumer_context_supplied_by_coordinator": "Opens the existing custom-colour slot editor. Its separate confirmation says Save; Edit is not itself that save action."}

## string/ui_use_colour

English: Use colour

Proposed XML: `<string name="ui_use_colour">"ቀለም ተጠቀም"</string>`

Positive dialog action when not adding/replacing a custom slot. After validation it accepts current colour and invokes caller commit for foreground or background, then dismisses. Preview changes may already have updated document colour property; cancel restores original preview.

Qualification: Use means apply the selected drawing/background colour, not save image or necessarily store a custom slot. Does not itself paint a stroke or recolour existing pixels. Separate custom-palette changes may persist independently; no blanket rollback promise.

Evidence and confidence: {"key": "ui_use_colour", "english": "Use colour", "value": "ቀለም ተጠቀም", "confidence": "medium compositional; draft only", "evidence_ids": ["aosp_use_colour_inversion", "aosp_use_details", "aosp_colour", "lo_use_colour"], "rationale": "Compose Color with AOSP singular imperative Use, attested in Use color inversion and Use details. The button commits the chosen foreground/background colour, so preserve use rather than substituting add, save or select.", "composition_limits": ["The specific-colour definite/accusative alternative ቀለሙን ተጠቀም should be considered by a native reviewer. LibreOffice ይጠቀሙ is a polite/plural imperative variant; mixing registers across the three action buttons is not automatically justified.", "Original author-composed phrase, not an exact full-phrase source translation or native-reader approval.", "Primary records establish component usage in their source products, not AN-Paint suitability. Independent contextual and native-language review, rendering and accessibility validation remain required.", "No production resources, builds, CI, remote records or held translations changed."], "status": "source-backed candidate for independent review; not accepted", "consumer_context_supplied_by_coordinator": "Accepts the current foreground/background colour value. It does not save the image or recolour existing pixels."}

## Review scope and limitations

All five are composed phrases requiring independent contextual judgment. Exact component records do not become exact full-label attestations. Basic means the supplied built-in swatch set, not exclusively scientific primary colours. Selected describes current valid preview state, which may still be provisional, rather than an imperative or saved-state guarantee. Add and Edit act on custom saved slots; Add may lead to replacement when the palette is full. Use accepts foreground/background choice, not saving an image or painting pixels. Shared labels can serve both action and dialog-title contexts; avoid mechanically forcing one register without considering those consumers.

No English defect established. Five plain labels contain no units, placeholders or ellipses. Neighbouring full hints, individual colour names, numerical colour-model labels, inherited Palette uncertainty and held Solid fill/Calligraphy are excluded. No translation of existing accepted values or new whole-language certification.

12 complete current project source files are included with exact Git blob and SHA-256 bindings. Fresh develop ref/commit/tree: 66be61df27c5359bffc32d56db21f3949899f873 / 870c5a584120d92710be516af0dc3b3847b183d9. Bounded scan reproduces eight key occurrences across two direct caller files. Historical discovery was rebound to complete current files, not an exhaustive fresh repository search. ColourValue and ColourSurface are nested in the complete AdvancedColourDialog source, rather than omitted separate files.

Lexical dossier preserves complete primary snapshots, original records, source URLs, reuse provenance, alternatives and confidence. Reused bytes are not fresh upstream retrieval. These original drafts are not human native-reader sign-off, runtime/rendering/colour-science verification or accessibility approval. No Work task, production resource/code edits, app builds, CI or release. Prior 81 ready candidates, 12 holds, optional recommendations and 12/705 production coverage remain unchanged.
