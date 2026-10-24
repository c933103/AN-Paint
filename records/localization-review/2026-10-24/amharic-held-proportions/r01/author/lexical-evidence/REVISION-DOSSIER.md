# Amharic held dimension/proportion labels: resolution proposal

2026-10-24. Scope: ui_same_width, ui_same_height, ui_lock_proportions only. This is an evidence-backed AI textual assessment for independent adjudication, not native-speaker certification or implementation.

## Proposed outcome

- ui_same_width: revise ተመሳሳይ ስፋት to **እኩል ስፋት** and clear the textual evidence/idiom hold if independently agreed.
- ui_same_height: revise ተመሳሳይ ቁመት to **እኩል ቁመት** and clear the textual evidence/idiom hold if independently agreed.
- ui_lock_proportions: retain **ተመጣጣኝነት መጠበቂያ** and clear the textual evidence/idiom hold if independently agreed.

These are recommendations, not changes to accepted counts. All original candidates, alternatives, hold rationales and release conditions remain preserved in the original record and copied candidate record. No original hold is overwritten. None of the three is implemented by this work.

## What is genuinely new

1. Newly retrieved complete Writer translation source has the complete UI control “Equal width for all columns” paired with “እኩል ስፋት ለሁሉም አምዶች” at lines 13960–13964. Its tooltip and a second column-width control confirm equality of the resulting widths. The complete core UI snapshot independently binds this control to a GtkCheckButton. This supplies an actual equal-dimension noun phrase, rather than deriving it only from the old Equalize action.
2. A new Writer same-height prose record uses the phrase “ተመሳሳይ እርዝመት” in text-column balancing. This is positive evidence that ተመሳሳይ can convey sameness in a dimension context. It prevents the unjustified conclusion that the original drafts are intrinsically wrong.
3. A newly examined record in the old cui snapshot pairs “Similarity Search” with “ተመሳሳይ መፈለጊያ”. Together with the old Same records, this demonstrates actual UI polysemy. The equality wording is a precision improvement for this numerical operation, not a claim that every use of ተመሳሳይ means only approximate similarity.
4. Newly retrieved complete Impress translation source supplies a standalone “Keep aspect ratio” control, “የ መጠን አንጻር መጠበቂያ” (9043–9047). Complete core UI bytes bind asr_check to GtkCheckButton (340–348). This establishes the nominal preservation-label pattern in an actual on/off image-proportion control. It is not an exact attestation of our proposed wording and is not automatically adopted as better terminology.
5. Beermann and Ephrem’s primary grammar paper, §§2.2–2.3 (printed pp. 23–24), supports bare indefinite nominal expressions and the modifier-before-noun pattern. This is general grammar evidence; applying it to these labels is our own analysis. No grammatical source claims to have reviewed this application.

The original AOSP dimension nouns, LO Equalize action variants and proportion-preserving resizing prose are retained as prior support, not relabeled as new discoveries. New Draw equalization help is untranslated in Amharic, so its English semantics are not counted as Amharic evidence.

## Full-phrase assessment: equal width and equal height

Both proposed phrases are concise adjective-plus-dimension noun phrases: እኩል modifies ስፋት or ቁመት. The complete labels describe the property the dialog configures, not a past-tense result or an imperative to apply immediately. No personal, possessive, definite or object suffix is introduced. Their parallel structure suits the shared toolbar-opener and dialog-title uses.

For width, እኩል ስፋት is directly contained as a complete constituent in an attested equal-width control. Removing its table-specific scope phrase does not alter the equality relation; this app’s separate Apply-to-all control and dialog context supply the scope. This is an explicitly described contextual shortening, not an exact whole-label match claim.

For height, using ቁመት keeps the established image-height noun directly paired with Height in AOSP Gallery2. The equality modifier is productive, supported by the parallel equal-width phrase and the prior actual Equalize Height action. The two-word candidate is not independently attested as a complete standalone control in the searched sources. That is a provenance limitation, not a reason to forbid a well-formed translation. The analysis considers the whole phrase and its use, rather than treating two dictionary lookups as sufficient.

The resulting reading is equality of the named scalar dimension across inputs. Neither label says equal shape, equal area, equal file size, equal position, or equality between width and height. Since the key’s noun identifies the axis, the paired wording also avoids confusing common height with vertical alignment.

Source-derived thought experiments, not executed tests:
- For 100×50 and 80×120 cropped images, common width 200 yields 200×100 and 200×300. እኩል ስፋት remains true while the heights differ.
- Common height 150 gives 300×150 and 100×150. እኩል ቁመት remains true while the widths differ.
- Pressing either toolbar opener alone does not perform these transformations. Apply validates and normalizes all assembly inputs, including tray entries; proportional other-axis results remain subject to integer rounding.

The source’s equality meaning needs no English rewrite. Replacing Same with the local equality expression is faithful contextual translation, not a different operation.

### Preserved alternatives

- Original ተመሳሳይ ስፋት and ተመሳሳይ ቁመት remain plausible; no proven mistranslation is alleged. Prefer እኩል here because the operation guarantees an exact common target rather than a general likeness.
- ተመሳሳይ እርዝመት remains the supplied height alternative, now with additional prose corroboration. Do not erase this lexical variation. It is not preferred because ቁመት is the app’s image-height family and the same-versus-similar precision issue would remain.
- The source action constructions ስፋት እኩል ማድረጊያ and እርዝመት እኩል ማድረጊያ remain genuine alternatives in their action context. They are longer and less close to this property-title speech act; no need to import them wholesale.

## Full-phrase assessment: lock proportions

ተመጣጣኝነት supplies the property to preserve; መጠበቂያ names the preserving function. Read as a nominal UI label, the whole phrase is approximately “proportionality preservation”, not “fixed size” or a security lock. The precise phrase already occurs within same-function width/height resizing prose. The new image-aspect checkbox supplies evidence that this preservation-noun construction works as a selectable setting, closing a gap that prose alone did not resolve.

A checkbox need not literally assert “locked” in both states. Its stable label names the option; the checked state enables preservation and the unchecked state disables it. The phrase therefore remains coherent in both states. This is the same functional treatment used by the newly verified Impress checkbox, without claiming identical wording or identical image behavior.

For this app, checked means width and height scale together from the current gesture-start selection ratio. A selection already distorted to 2:1 stays 2:1 during a locked resize; the label does not promise restoration of its imported aspect ratio. Size may change, and movement/rotation are not frozen. Unchecking permits independent deformation. The abstract proportionality noun describes the retained relation rather than the two lengths themselves, which is why the original candidate is preferable to the shorter size-preservation variant.

No new wording is needed to solve the former idiom hold. Retention is based on full-phrase interpretation, preserved same-function evidence and the newly verified selectable-control pattern, not on a claim that a native reader approved it or that exact corpus reuse is mandatory.

### Preserved alternatives and exclusions

- መጠን መጠበቂያ is an attested Keep ratio variant, but its size noun is less explicit about a relation; do not silently adopt it.
- New የ መጠን አንጻር መጠበቂያ is preserved verbatim as a genuine checkbox alternative. Its terminology is longer and no evidence establishes it as clearer than the original proportions noun.
- Empty Keep ratio/Keep Ratio PO entries remain untranslated, not positive attestations.
- A separate Aspect ratio noun is not itself a full Lock proportions translation. No security-lock noun, original-image promise or fixed-dimension wording is proposed.

## Confidence and remaining gaps

- Equal width: high semantic confidence, medium-high full-label contextual confidence.
- Equal height: high scalar/axis confidence, medium-high full-label contextual confidence; exact target phrase is an original productive adaptation.
- Lock proportions: high source-behavior confidence, medium-high full-label/checkbox textual confidence after new pattern evidence.

Remaining gaps are specific: no native-reader study, spoken-accessibility check, actual Amharic rendering, width/line-wrap check, lifecycle exercise, or runtime test. The proportion label is relatively formal and its empirical familiarity remains unmeasured. Multiple LO modules are one translation ecosystem, not multiple independent native judgments. These limits should accompany acceptance and later UI verification; they are not by themselves a universal exact-match or native-signoff prerequisite for every source-only translation.

Independent adjudication should explicitly approve or reject each complete proposed value in both relevant controls/states. A new substantive grammatical or semantic objection should be recorded precisely. Do not carry forward an indefinite hold merely by restating the former request for more review.

## Artifacts and provenance

- sources.json: immutable links, hashes, byte counts, fresh-versus-reused provenance.
- exact-records-local.json: exact PO records and validated line ranges for local review only.
- public-bounded-evidence.json: short excerpts and source links suitable for a bounded public evidence record. Complete upstream snapshots and the full grammar extraction are not included in this public subset.
- original-candidates-and-alternatives.json: unchanged original candidates and all supplied alternatives.
- search-and-retrieval-limits.json: empty/incomplete outcomes and excluded sources.
- source-integrity.json: source and extraction checks; explicitly not app testing.

All six newly retrieved GitHub files have complete local bytes matching returned Git blob SHAs. Five reused complete snapshots match the original SHA-256 provenance. The grammar snapshot is the complete web-tool textual extraction response, not original PDF bytes; tables/graphics are not asserted to be faithfully preserved. This is openly recorded, rather than calling extracted text a downloaded PDF.

No Work task, application-source edit, build, CI run, remote publication, or release was performed.
