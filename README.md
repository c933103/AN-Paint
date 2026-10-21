# Language review status: 21 October 2026

Reviewed source checkpoint: [4355869e](https://github.com/c933103/AN-Paint/tree/4355869e2e198b5616419291cba225b018444fab), tree `b9b148d5d8ef7c7b088500a9c177f9f59304b800`. The live Git ref and commit-to-tree relation were verified through GitHub. This is an evidence-only update to [intentional draft tracker PR56](https://github.com/c933103/AN-Paint/pull/56), which must not merge.

## Later source movement, not a new linguistic review

Develop advanced to [ef46e8aa](https://github.com/c933103/AN-Paint/tree/ef46e8aa4f55825a071f4c1ecd6f3c80b9355f51), tree `c96f97087692d7e0f3ec516ed309d1ceda1c11c3`. A read-only GitHub comparison found exactly six changed paths, **zero resource or priority-manifest edits**, and two production files affecting Fit/status layout. The horizontal Fit caption now uses natural sizing/wrapping rather than the old fixed 44×44 description. Fit, its accessible name and status consumer/layout contexts therefore need bounded current-context reconciliation; prior Polish/Czech layout holds are not automatically closed or represented as proven current defects. The linguistic receipts remain bound to **4355869e / b9b148d5**, not falsely relabeled as complete fresh-head review. Unchanged phrases were not rereviewed merely because the base moved. No builds or runtime checks were run for this reconciliation. `post-review-source-movement.json` preserves the compact exact comparison and scope.

## Bounded cohorts at the reviewed source checkpoint

| Language / exact scope | Reviewed or reconciled | Current disposition | Open work / limits |
|---|---:|---|---|
| Japanese P0+P1 | 341/341 | 340 unchanged prior carries + 1 static caller-context rebound | No wording correction; 30 wording-only/no-direct-consumer limits preserved |
| Polish P0+P1 | 341/341 | 310 retained bounded accepts | 31 holds: 30 dormant-context + 1 compact Fit layout; no correction |
| Arabic ar P0+P1 | 341/341 first pass | 1 prior carry + 332 unchanged assessed (302 static-context + 30 wording-only) | 8 independently accepted candidate values, not integrated |
| Spain Spanish es-ES P0+P1 | 341/341 first pass | 336 current values accepted in first pass, including 9 prior carries | 5 independently accepted candidate values, not integrated; 30 source-only limits preserved |
| Vietnamese vi P0+P1 | 341/341 | 336 fresh accepted values + 1 prior exact carry | 4 accepted final replacement candidates, all unapplied; 30 wording-only limits; Nôm untouched |
| Hungarian hu P0+P1 | 341/341 author review | 323 current bounded values: 292 static + 30 wording-only + 1 prior carry | 18 final priority replacement candidates + 2 adjacent P2 candidates accepted; all unapplied |
| Lithuanian lt P0+P1 | 341/341 author review | 320 current bounded values: 289 static + 30 wording-only + 1 prior carry | 18 priority edits + 4 atomic P2 dependencies accepted; 3 unchanged labels conditional; 4 current-text terminology holds await replacement; all unapplied |
| Czech full 717-identity catalogue | 717/717 existing review rebound | 645 retained bounded accepts; 716 exact entries present | 72 holds: 71 no-direct-consumer, including the absent legacy manual, plus 1 Fit layout |
| Swedish full 717-identity catalogue | 717/717 existing review rebound | 714 retained bounded accepts; 715 exact entries present | 3 holds: present Main label, absent palette and absent legacy manual; source-semantic limits remain |

Every priority batch is **92 P0 + 249 P1 = 341 typed identities**. Japanese and Polish have zero missing priority entries and earn zero new translation or duplicate review credit. Polish still has 319 missing catalogue identities, all outside P0/P1. The old global table's presence and review columns are not interchangeable.

Japanese's `ui_the_draft_is_saving_try_again_shortly` keeps its already-reviewed wording. PR146 now selects it only for autosaving; this resolves the specific static generic-busy caller hold without a new runtime, installed-device or translation claim. The 30 wording-only restrictions remain attached to the original identities.

Spanish has 30 exact old accepted receipts, only 9 overlapping this batch; the other 21 are outside it. Its separate assembly-Help hold is also outside the batch and remains open. The unavailable original full-priority Spanish evidence is not reconstructed. Arabic's first-pass decisions and all proposed replacement values stay distinguished from independently accepted, integrated corrections.

Vietnamese has 21 exact prior receipts, only one overlapping the priority batch. Its deduplicated locale-only current partition is **357 bounded current / 4 needing correction or re-review / 356 unknown / 0 missing = 717**. This is not a recomputed all-language total. The earlier original-proposal result was 2 accept / 2 revise; the two exact substitutes have now passed the separate check, yielding **4 accepted replacement candidates**. All remain unapplied, so the current-source counts do not increase.

## Independent candidate review supplement

The separate independent model reviewers accepted all **8 Arabic** and **5 Spanish** candidates, with zero revise/hold decisions. These are candidate-wording decisions only: no corrected value has been integrated, and current-source counts above do not increase. Spanish includes four clarity/idiom improvements and one optional capitalization change; the review establishes zero new save/cancel/output-state defects. Earlier author terminology such as “correction” must not be interpreted as a confirmed state-behavior defect. The independent checks cover only these proposed values, not a second review of all 341 entries. Complete source/target/proposal values, hashes, consumer links and limits are in `independent-candidate-reviews.zip`.

### Final resolution of the remaining Vietnamese, Hungarian and Lithuanian candidates

The separate second check accepts both Vietnamese substitutes, the four Lithuanian terminology follow-ons and the paired Lithuanian dithering checkbox **Smulkinti spalvas**. It revised the intermediate Hungarian memory substitute once more; that exact final value was then separately accepted in the final Hungarian receipt. No further wording candidate in this bounded set remains awaiting review. **Every replacement is still unapplied**, and current-production counts/holds do not change.

- Vietnamese now has **4 accepted replacement candidates**: two original accepted proposals plus the exact magnifier and whole-operation memory substitutes. The earlier decoder-buffer-only ACCEPT remains withdrawn; it is not revived.
- Hungarian now has **18 priority + 2 adjacent P2 = 20 accepted replacement candidates**. The final memory warning describes inability to load for editing under current memory constraints, not decoder-buffer-only excess. Its exact unquoted UTF-8 SHA-256 is `4e4c9dd53627e79a52ac3bbe1e7986af5c632773488cabf2a30ae9bc111ca86f`. Both earlier memory proposals remain superseded.
- Lithuanian now has **18 priority edits + 4 P2 dependency edits = 22 accepted replacement candidates**. Its three unchanged priority crop labels remain conditional on both crop templates. The four old terminology holds are now paired with accepted replacements, not silently counted as accepted current text. Apply the GIF description together with `save20_dither`; preserve the unit/height/width and both crop-mode template atomic groups. Bounded inspection supported the credit-warning replacements without authorizing a blanket rewrite of all credit labels.

The final second-check receipt is preserved under `remaining-second-check/` with SHA-256 `7fb4b672400e2b37406ad0ddca6ce9896faea2c53b52d9692151ad1f30a05c09`. The final Hungarian acceptance is under `hu/addendum-final-memory-warning/receipt.json`. All original receipts, withdrawn decisions and intermediate substitutes remain in the archive unchanged. The Vietnamese original receipt and one-key addendum retain their original identities; the new second check supplies the final candidate acceptance rather than rewriting them.

Hungarian's current locale-only partition remains **343 bounded / 20 held or needing correction / 354 unknown / 0 missing = 717**. Lithuanian retains **320 current bounded priority pairs**, with 14 current text corrections, 3 dependency-blocked priority contexts and 4 current terminology holds until integration. Vietnamese remains **337 current bounded priority pairs**, with 4 current corrections outstanding. No candidate count is added to current-source or global review totals.

The Lithuanian evidence-only category correction remains: **Įterpti / Elipsė**, **Žymėjimas / Laisvos formos žymėjimas**, and **Piešimas / Akvarelė** are source-valid examples. This is not a translation-patch change. Hungarian raw autosave details retained in `lastAutosaveError` are not asserted to be rendered verbatim.

## Existing Czech and Swedish evidence

Czech's complete English/Czech files still match the original review's SHA-256 bindings. Its [published integration summary](https://github.com/c933103/AN-Paint/blob/f25c4514f42fcc5c6aa2bd01d65fd9782c30b0fc/czech-current-integration-20261020/README.md) records 645 bounded accepts and 72 holds; [PR156](https://github.com/c933103/AN-Paint/pull/156) contains the merged catalogue. The original full review archive's publication remains separately pending. This update does not reproduce it or claim it is public.

Swedish's [existing completion evidence](https://github.com/c933103/AN-Paint/blob/cb3b384c69ca999ad3de95aa677a149f84c6360f/swedish-completion-20261020/CURRENT.md) and assembly-Help source rebind match all 717 current source values/attributes and the 714 reviewed current targets. The later [independent Curve-hint receipt](https://github.com/c933103/AN-Paint/blob/180672106a1b0668b6eafa68a8ff2ac8d5ea4c45/swedish-curve-independent-20261020/curve-hint-independent-review.json) accepts the exact corrected current pair; it is not left pending merely because an earlier chronological note predates it. Forty source-semantic-only restrictions remain. [PR151](https://github.com/c933103/AN-Paint/pull/151) contains the merged extended catalogue.

## Exact accepted-value handoff, not implementation

`accepted-candidate-manifest.json` is the consolidated exact-value handoff: **59 typed resource edits = 53 P0/P1 + 6 P2**, comprising Arabic 8, Spain Spanish 5, Vietnamese 4, Hungarian 20 and Lithuanian 22. A plural with complete quantity forms counts as one typed resource. The three unchanged Lithuanian crop labels are not additional edits. The manifest includes the reviewed English, expected unchanged current target, exact accepted replacement, resource attributes, hashes, receipt lineage and atomic dependency groups. `final-substitutes.json` gives the last eight exact values separately.

This is mechanical assembly of completed reviews, not a new linguistic review or an applied patch. Do not use older whole candidate files blindly: the manifest explicitly supersedes the earlier Vietnamese/Hungarian memory or magnifier proposals and adds the Lithuanian follow-ons. Recheck its expected source/current values against the eventual authorized implementation base; preserve all context, wording-only and presentation limits. Spanish's capitalization remains optional cosmetic.

## Global totals are not yet recomputed

The **171-option × 717-identity global table dated 20 October is historical**, not a claim about this source. Its 9,465 bounded / 235 held / 39,225 unknown / 73,682 missing figures have not been globally rebound here. Do not add the rows above to those totals: they overlap earlier reviews, and a review hold can concern an absent entry. The next full union must join exact locale + typed identity + complete source/target values, preserve limitations and deduplicate original receipts.

The [original immutable union](https://github.com/c933103/AN-Paint/tree/2fff195596e7a792185b3b29eb756b7df9081a92/review-reconciliation-20261020) and [merged-review delta](https://github.com/c933103/AN-Paint/tree/854d1402a7a268d9156a159ff3bbe9ca1a6fb95d) remain unchanged. No whole-language acceptance is asserted.

## Files and validation

- `accepted-candidate-manifest.json`: all 59 exact accepted but unapplied replacements, current/source guards and atomic groups.
- `final-substitutes.json`: the final eight exact substitute values, including the separately accepted Hungarian memory warning.
- `post-review-source-movement.json`: read-only comparison to later ef46e8aa; unchanged text versus changed Fit/status contexts.
- `current-cohort-delta.json`: compact source-bound, denominator-explicit cohort status.
- `review-packets.zip`: complete Japanese/Polish rebound ledgers and reports, original Polish final packet, completed Arabic/Spanish first-pass ledgers and summaries. Arabic/Spanish corrections are proposals, not accepted production changes.
- `hu-review-packet.zip`: complete Hungarian author batch, original prior bindings and separate P2 findings.
- `lt-review-packet.zip`: complete Lithuanian author batch, atomic dependency proposals and terminology holds.
- `vi-review-packet.zip`: complete 341-entry Vietnamese review, prior-receipt rebind, four unintegrated candidates and static validation.
- `independent-candidate-reviews.zip`: Arabic, Spanish, Vietnamese, Hungarian and Lithuanian independent candidate receipts, all unintegrated. The Vietnamese original receipt and one-key superseding addendum are both preserved; the final bounded substitute checks are preserved separately without overwriting earlier stages.
- `SHA256SUMS.json`: identities of the published packets and their members.

Read-only XML/JSON/hash checks confirmed the source-tree bindings, Japanese/Polish 341-entry counts, unchanged Czech resources, all Swedish source/target bindings, and the independently reviewed Curve pair. **No app build, Gradle, CI dispatch, emulator, version or release action occurred. No production resources changed.** This is not new runtime, installed layout, TalkBack, native-speaker or whole-language certification.
