# Independent review: Amharic colour-selector captions and actions

## Outcome

Retain three drafts; revise two; no additional hold forced by the evidence. These are review recommendations, not implementation or native-reader certification. The prior 81 ready / 12 held totals and inherited Palette uncertainty are unchanged by this review.

### string/ui_basic_colours: RETAIN

English: Basic colours

Recommended: **መሰረታዊ ቀለሞች**

A plural caption for the built-in baseline swatch group. Basic Shapes/Basic and Colors supply the broad ordinary sense and construction. No evidence establishes that this adjective exclusively denotes scientific primaries. Preserve author spelling and plural; do not silently replace Basic with Default, Standard or Built-in.

Confidence: medium.

- Possible basic/primary colour association is contextual ambiguity, not certified eliminated.
- The exact full English/Amharic label pair is not attested; this is an original two-word composition.

### string/ui_selected_colour23: RETAIN

English: Selected color

Recommended: **የተመረጠው ቀለም**

A definite singular selected-state noun phrase fits the current valid preview. The relative modifier carries definiteness; the label is not a direct object and needs no accusative suffix. AOSP singular selected-language wording and Gasser relative-clause contrasts independently support the structure.

Confidence: medium-high for grammatical structure; medium overall.

- Does not denote final acceptance or saving.
- Not equivalent to Select color imperative or a complete state sentence.

### string/ui_add_colour26: RETAIN

English: Add colour

Recommended: **ቀለም አክል**

Bare-object introduction of a colour is defensible for the new-item operation, matching Add a language/Add account constructions. Works as a short action and shared dialog title. Do not force definiteness merely for visual symmetry with Edit and Use.

Confidence: medium.

- The outer action opens the editor; it does not immediately save.
- Full slots can trigger replacement; the wording makes no guaranteed count-increase promise.

### string/ui_edit_colour26: REVISE

English: Edit colour

Recommended: **ቀለሙን አርትዕ**

Replace draft: ቀለም አርትዕ

This operation edits the already-identified custom swatch. Prefer definite ቀለሙ plus accusative ን. Crucially the closest cited AOSP dialog title Edit word is ቃሉን አርትዕ, not a bare-object model. The English articleless UI label does not require articleless Amharic.

Confidence: medium-high for preference; medium overall naturalness.

- Bare-object labels exist in AOSP, e.g. Edit access point; original is not declared universally ungrammatical.
- A grammatical contextual improvement, not an English source rewrite and not a Save action.

### string/ui_use_colour: REVISE

English: Use colour

Recommended: **ቀለሙን ተጠቀም**

Replace draft: ቀለም ተጠቀም

Acceptance concerns the specific current colour, not colour as a generic mode. Definite accusative ቀለሙን preserves this reference while keeping the singular imperative register. Genuine AOSP Use color inversion/correction and Use System Selection support object-before-verb with case marking.

Confidence: medium-high for preference; medium overall naturalness.

- Exclude Use details from imperative corroboration because its source context is a battery-usage subtitle.
- Some AOSP Use labels have unmarked objects; recommendation is contextual, not a universal grammatical prohibition.
- No need to substitute Save, Select, Apply or add an instrumental prefix merely to avoid the object marking.

## Definite/accusative adjudication

The revised Edit and Use objects identify a colour already supplied by the UI context: ቀለም → ቀለሙ → ቀለሙን (colour → the colour → the colour as object). This grammatical specificity does not add an unauthorized feature to the English label. English UI articles and Amharic nominal marking need not correspond word-for-word.

The strongest Edit analogue already in the dossier is AOSP Edit word → ቃሉን አርትዕ. Treating that record as support only for word order misses its definite-accusative ending. Independent inspection also found unmarked AOSP Edit access point and Use 24-hour format, so this report does not claim all bare-object labels are ill-formed. The concrete identified-colour contexts favor the marked alternatives.

Sisay Fissaha Adafre's [Formal Analysis of Some Aspects of Amharic Noun Phrases](https://aclanthology.org/2004.eamt-1.6.pdf), printed pp. 44–46, distinguishes definiteness and accusative suffixes, explains their order, and discusses marking on modifiers. Michael Gasser's [A Dependency Grammar for Amharic](https://www.ps.uni-saarland.de/~rade/papers/related/Gasser10.pdf), sections 3.2–3.3, contrasts a definite noun with its accusative form and definite relative modifiers with and without accusative marking. These independent grammatical descriptions support the analysis; neither attests these complete colour labels. Ruth Kramer's [Object Markers in Amharic](https://faculty.georgetown.edu/rtk8/Kramer%20ACAL%2041%20Object%20Markers%20in%20Amharic%20handout.pdf), pp. 6–8, also cautions against conflating noun case marking with the separate verbal object-marker system. No new verbal object suffix is mechanically required here.

## Register and evidence correction

Keep the short singular-imperative family አክል / አርትዕ / ተጠቀም. Polite/plural AOSP ይጠቀሙ and LibreOffice nominal-action labels are genuine alternatives, but mixing them selectively is not an improvement. AOSP contains mixed register, so it is supporting evidence rather than a universal style authority. Supplied production ui_edit_background already ends with a singular imperative. Add/Edit are also titles, but an action title is valid; there is no need to replace only those strings with a nominal form.

Important correction: aosp_use_details is a valid source record but poor imperative evidence. English lines 6050–6066 place details_subtitle under application/subsystem battery usage. Its Use is a usage noun in context, not an instruction to use details. The Amharic record therefore cannot safely validate a faithful imperative translation. Exclude it from the original rationale. Independently inspected Use color correction, Use color inversion, Use System Selection and Use location are actual action analogues and remain adequate component support.

Selected color is a state caption for a provisional current preview, not an instruction and not a saved-state guarantee. The additional AOSP singular selected-language branch supports የተመረጠው without accusative. Basic colours is a supplied baseline set, not a scientific primaries-only claim. Preserve the broad Basic translation rather than silently changing it to Built-in, Standard or Default. No English defect was established; if a source defect is later established, correct English and flag affected language terms rather than hiding the change inside Amharic.

## Integrity and evidence limits

- Input manifest seal verified: 3b9ae3162debcf9759d8f8c439233efef73cfaca8856ba5747deaa2cf32874be.
- All 30 sealed input files match. All 12 complete project copies match their SHA-256, Git blob hashes, tree entries and lengths.
- Source snapshot is develop commit 66be61df27c5359bffc32d56db21f3949899f873 / tree 870c5a584120d92710be516af0dc3b3847b183d9. This reviewer checked those supplied bindings, not a newly retrieved current ref.
- Bounded rescan reproduces eight direct occurrences across the two caller files. Reviewed consumer contexts agree with the supplied description: 48 built-in swatches, provisional preview, custom-slot add/edit, acceptance of foreground/background choice.
- All 19 supplied lexical records verify against the four pinned snapshots. Eleven independently selected AOSP record pairs are preserved, including corroboration, counterevidence and the rejected-use-context record. They reuse sealed snapshot bytes, not a fresh AOSP retrieval.
- Three primary scholarly PDFs were freshly downloaded, hashed and text-extracted. They independently support the grammar analysis, not exact phrase attestation or product suitability.
- Search results did not establish an exact complete phrase pair in an independent authoritative source. Incidental web snippets were not promoted to attestations; an indexed government art textbook failed to open with HTTP 404 and was not used as verified evidence.
- All recommended labels remain original compositions. Naturalness confidence is bounded: no human native-reader approval, running-device layout, font rendering, accessibility or colour-science validation was performed.
- No Work task, production edit, build, CI, release or remote-state action occurred. No prior holds or optional recommendations were changed.

The JSON report provides exact keys and recommendations. Evidence records include immutable source URLs and line locations. The coordinator should preserve both the rejected original variants and this rationale when adopting revisions, without counting revised drafts as already adopted.
