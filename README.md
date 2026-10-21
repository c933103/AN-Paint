# Language review status: 21 October 2026

Source: [develop 4355869e](https://github.com/c933103/AN-Paint/tree/4355869e2e198b5616419291cba225b018444fab), tree `b9b148d5d8ef7c7b088500a9c177f9f59304b800`. The live Git ref and commit-to-tree relation were verified through GitHub. This is an evidence-only update to [intentional draft tracker PR56](https://github.com/c933103/AN-Paint/pull/56), which must not merge.

## Current bounded cohorts

| Language / exact scope | Reviewed or reconciled | Current disposition | Open work / limits |
|---|---:|---|---|
| Japanese P0+P1 | 341/341 | 340 unchanged prior carries + 1 static caller-context rebound | No wording correction; 30 wording-only/no-direct-consumer limits preserved |
| Polish P0+P1 | 341/341 | 310 retained bounded accepts | 31 holds: 30 dormant-context + 1 compact Fit layout; no correction |
| Arabic ar P0+P1 | 341/341 first pass | 1 prior carry + 332 unchanged assessed (302 static-context + 30 wording-only) | 8 independently accepted candidate values, not integrated |
| Spain Spanish es-ES P0+P1 | 341/341 first pass | 336 current values accepted in first pass, including 9 prior carries | 5 independently accepted candidate values, not integrated; 30 source-only limits preserved |
| Vietnamese vi P0+P1 | 341/341 | 336 fresh accepted values + 1 prior exact carry | 4 correction candidates, unapplied and awaiting independent review; 30 wording-only limits; Nôm untouched |
| Czech full 717-identity catalogue | 717/717 existing review rebound | 645 retained bounded accepts; 716 exact entries present | 72 holds: 71 no-direct-consumer, including the absent legacy manual, plus 1 Fit layout |
| Swedish full 717-identity catalogue | 717/717 existing review rebound | 714 retained bounded accepts; 715 exact entries present | 3 holds: present Main label, absent palette and absent legacy manual; source-semantic limits remain |

Every priority batch is **92 P0 + 249 P1 = 341 typed identities**. Japanese and Polish have zero missing priority entries and earn zero new translation or duplicate review credit. Polish still has 319 missing catalogue identities, all outside P0/P1. The old global table's presence and review columns are not interchangeable.

Japanese's `ui_the_draft_is_saving_try_again_shortly` keeps its already-reviewed wording. PR146 now selects it only for autosaving; this resolves the specific static generic-busy caller hold without a new runtime, installed-device or translation claim. The 30 wording-only restrictions remain attached to the original identities.

Spanish has 30 exact old accepted receipts, only 9 overlapping this batch; the other 21 are outside it. Its separate assembly-Help hold is also outside the batch and remains open. The unavailable original full-priority Spanish evidence is not reconstructed. Arabic's first-pass decisions and all proposed replacement values stay distinguished from independently accepted, integrated corrections.

Vietnamese has 21 exact prior receipts, only one overlapping the priority batch. Its deduplicated locale-only current partition is **357 bounded current / 4 needing correction or re-review / 356 unknown / 0 missing = 717**. This is not a recomputed all-language total. The four candidate values have not been independently accepted or integrated.

## Independent candidate review supplement

The separate independent model reviewers accepted all **8 Arabic** and **5 Spanish** candidates, with zero revise/hold decisions. These are candidate-wording decisions only: no corrected value has been integrated, and current-source counts above do not increase. Spanish includes four clarity/idiom improvements and one optional capitalization change; the review establishes zero new save/cancel/output-state defects. Earlier author terminology such as “correction” must not be interpreted as a confirmed state-behavior defect. The independent checks cover only these proposed values, not a second review of all 341 entries. Complete source/target/proposal values, hashes, consumer links and limits are in `independent-candidate-reviews.zip`.

## Existing Czech and Swedish evidence

Czech's complete English/Czech files still match the original review's SHA-256 bindings. Its [published integration summary](https://github.com/c933103/AN-Paint/blob/f25c4514f42fcc5c6aa2bd01d65fd9782c30b0fc/czech-current-integration-20261020/README.md) records 645 bounded accepts and 72 holds; [PR156](https://github.com/c933103/AN-Paint/pull/156) contains the merged catalogue. The original full review archive's publication remains separately pending. This update does not reproduce it or claim it is public.

Swedish's [existing completion evidence](https://github.com/c933103/AN-Paint/blob/cb3b384c69ca999ad3de95aa677a149f84c6360f/swedish-completion-20261020/CURRENT.md) and assembly-Help source rebind match all 717 current source values/attributes and the 714 reviewed current targets. The later [independent Curve-hint receipt](https://github.com/c933103/AN-Paint/blob/180672106a1b0668b6eafa68a8ff2ac8d5ea4c45/swedish-curve-independent-20261020/curve-hint-independent-review.json) accepts the exact corrected current pair; it is not left pending merely because an earlier chronological note predates it. Forty source-semantic-only restrictions remain. [PR151](https://github.com/c933103/AN-Paint/pull/151) contains the merged extended catalogue.

## Global totals are not yet recomputed

The **171-option × 717-identity global table dated 20 October is historical**, not a claim about this source. Its 9,465 bounded / 235 held / 39,225 unknown / 73,682 missing figures have not been globally rebound here. Do not add the rows above to those totals: they overlap earlier reviews, and a review hold can concern an absent entry. The next full union must join exact locale + typed identity + complete source/target values, preserve limitations and deduplicate original receipts.

The [original immutable union](https://github.com/c933103/AN-Paint/tree/2fff195596e7a792185b3b29eb756b7df9081a92/review-reconciliation-20261020) and [merged-review delta](https://github.com/c933103/AN-Paint/tree/854d1402a7a268d9156a159ff3bbe9ca1a6fb95d) remain unchanged. No whole-language acceptance is asserted.

## Files and validation

- `current-cohort-delta.json`: compact source-bound, denominator-explicit cohort status.
- `review-packets.zip`: complete Japanese/Polish rebound ledgers and reports, original Polish final packet, completed Arabic/Spanish first-pass ledgers and summaries. Arabic/Spanish corrections are proposals, not accepted production changes.
- `vi-review-packet.zip`: complete 341-entry Vietnamese review, prior-receipt rebind, four unintegrated candidates and static validation.
- `independent-candidate-reviews.zip`: Arabic eight and Spanish five complete independent candidate receipts, unintegrated.
- `SHA256SUMS.json`: identities of the published packets and their members.

Read-only XML/JSON/hash checks confirmed the source-tree bindings, Japanese/Polish 341-entry counts, unchanged Czech resources, all Swedish source/target bindings, and the independently reviewed Curve pair. **No app build, Gradle, CI dispatch, emulator, version or release action occurred. No production resources changed.** This is not new runtime, installed layout, TalkBack, native-speaker or whole-language certification.
