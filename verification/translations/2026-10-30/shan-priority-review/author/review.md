# Shan residual priority wording — batch A

## Source binding and status

- Declared merged baseline: AN Paint develop `96681f687671a1fdffe134a325843919c1543401`, tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`.
- Read-only source: `Paintroid/src/main/res/values/strings.xml`, `values-b+shn/strings.xml`, `translations/string-importance.json`, and `tools/fixtures/current_localization/reviewed_priority_batches.json`.
- The selected files are source-bound by the recorded unchanged-file assurance. This materialized checkout has no resolvable local Git HEAD; no independent claim of local commit attestation is made.
- Prior work inspected: `earlier Shan candidate record (shn.tsv)`, `deliverable/review.md`, and `deliverable/shn-priority-key-values.json`. Prior candidates are not accepted merely because they already existed.
- This batch contains **37 missing-value candidates: 9 P0 + 28 P1**, and separate assessments of the **two existing_unreviewed P1 values**. Candidates require independent linguistic review; this is same-author semantic review only. PR237's accepted additions, the six unchanged acceptances, and all canonical resources remain untouched.
- Current official residual stays **53 P0 + 130 P1** until independent acceptance/integration. Candidate count is not completion credit. No source integration, renderer/device verification or native-human certification is asserted.

## Translation approach

New wording was composed against each actual English proposition. The candidate table includes the complete source, exact candidate, source attributes, prior relationship, backtranslation, and item-specific review limit. No generic Northern Thai, Burmese, or Tai Nüa substitution was used. Repeated accepted vocabulary is used as terminology context, not counted as new acceptance of old keys.

The two required existing rows were assessed first. Undo now has positive evidence of the intended reverse-edit software meaning; the brush compound remains an explicit lexical hold. A search yielding a dictionary's toothbrush sense was rejected, not imported.

## References and what they establish

1. [MediaWiki's primary Shan software catalogue](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/shn.json), inspected 2026-10-30: `editundo` is `ၶိုၼ်ၶိုၼ်း`; adjacent undo messages use the term for edit reversion. `show-big-image-size` uses `ၽိၵ်ႉသႄႇလ်` for pixels; preview-related messages corroborate viewing in advance. This supports those specific terms, not a blanket approval of the catalogue or this batch.
2. [MediaWiki Help:Diff/shn](https://www.mediawiki.org/wiki/Help:Diff/shn), inspected 2026-10-30: the Undo-labelled action links to reversion documentation. This corroborates reversal, not repetition.
3. [TAIDictionary](https://taidictionary.com/), inspected 2026-10-30: its English brush entry gives a tooth-cleaning implement, not a paint brush. This is a rejected sense match, not evidence against the current Shan compound.
4. [KD English–Shan dictionary](https://www.kddictionary.com/dictionary/eng-shan) and [Shan Dictionary](https://www.shandictionary.com/) were inspected but did not provide an inspectable relevant paintbrush/draft entry in this pass. No lexical conclusion is drawn from that retrieval limitation.

## Safety and context checks

- Derived export wording retains successful export plus the full drawing's continued unsaved changes, and requires a full-image copy before replacement. It does not equate export with Save.
- Destination failure states replacement failure, not selection failure; no successful save is implied.
- Autosave failures are separately about the full image or selected content; missing pixels and unreadable pixels remain distinct.
- Recovered image is a completed recovery label, not a guarantee that undo history or other metadata was recovered.
- Resize and zoom use distinct wording; the resize-copy action retains the copy object.
- Rotation retains the angle and clockwise direction; swapping explicitly expresses exchange.
- Paste hint uses the already accepted menu-label wording and preserves the OR alternative and arrow sequence.
- The 1–1024 boundary is unchanged; positive target dimension remains strictly greater than zero.
- All visible placeholders, degree marks, arrows, ellipses and formatted=false declarations in this authored batch were manually compared to the supplied source. This is not a parser/test result.

## Next review scope

Independently accept/reject each row rather than the language as a whole. Pay particular attention to the encoder/calque family, the destination-replacement predicate, derived-export pronoun scope, preview header naturalness, short geometric verbs, and the explicit clock-hand expression. The pixels spelling is now supported by primary software use but still needs the same context review as any other candidate.

The other residual keys are not silently waived. They were not drafted in this bounded batch. The brush hold is a specific lexical limit, not a permission blocker.

## Batch B: recovery-copy and canvas/crop semantics

`batch-b.tsv` adds **21 candidates: 5 P0 + 16 P1**. They are separate from batch A and from existing accepted wording. The same source baseline and independent-review requirements apply. Combined actual drafts are **58 missing keys: 14 P0 + 44 P1**, plus the two existing-value reviews.

The canvas term `ပိုၼ်ႉတီႈတႅမ်ႈႁၢင်ႈ` is an explicitly proposed descriptive compound, 'drawing area'. It is not claimed to be an established software term. Source context distinguishes bounded bitmap canvas from viewport and image resizing: PaintDocument.kt `cropCanvas`/`cropSelection`, ClassicPaintActivity.kt canvas-bounds action, and ImageCropDialog.kt crop-region validation. Crop-to-selection explicitly leaves the selected area, rather than deleting it. Smaller-canvas guidance keeps top-left anchoring, right/bottom pixel discard, and Undo restoration. Recovery-copy instructions retain separate preservation, ZIP, exact `canvas.png`, menu path, extraction/load sequence, and conditional normal resize.

`draft-term-holds.tsv` records **14 item-specific holds (12 P0 + 2 P1)** after actual semantic review. The previous draft noun is not casually reused: a model/example noun, an unfinished-drawing paraphrase, and a temporary-image paraphrase each risk misidentifying persistent autosave state. These holds do not say all Shan is blocked and do not replace the 58 actual drafts. In particular the long paused-autosave warning distinguishes the protected OLD draft from CURRENT work, while history-unavailable distinguishes recovered canvas from unreadable undo history. Neither warning is offered as a fluent full translation until its object terminology is secure.

Direct `shn.wiktionary.org` entry requests for brush, paintbrush, draft, and canvas were not accessible through the web tool in this pass. That is a retrieval limitation, not a user rejection or evidence that a word does not exist. No translation service or machine-translated commercial site was used to substantiate these terms.
