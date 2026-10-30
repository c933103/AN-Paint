# M2 bounded adoption receipt — separate delta

The final project acceptance decision adopted the two exact M2 values at moderate confidence after inspecting the independent source-backed rationale. PR56 receipt: https://github.com/c933103/AN-Paint/pull/56#issuecomment-6535005927

Direct comment-ID retrieval verified that its body exactly equals `pr56-comment-request.md`.

- Adds 2 P1 lexical values, no notation; historical cumulative total 457 adopted / 225 held.
- ANG: 223 adopted / 118 held; NON: 234 adopted / 107 held.
- Adopted tiers: 100 P0 + 357 P1; 14 notation-only included unchanged, 443 lexical.
- M1 + M2 together add 8 lexical values: 4 P0 + 4 P1.
- All unrelated holds remain. Frozen 449 packet, frozen recommendation ledger and M1 receipt hashes were rechecked unchanged.

`adopted-M2-two-values.tsv` is an additive decision overlay. Its copied `bounded_wording_status` column preserves the earlier recommendation-stage state rather than pretending that review began adopted; the explicit `M2_adoption_status` and `M2_adoption_authority` columns record the later controlling decision. The independent review files remain historical recommendation records.

`data-only-final-validation.json` records exact two-row agreement with the review, exact supplied-baseline English, exact authorized one-word-form changes, cumulative disjoint row counts, absence of placeholders/numeric limits in these two rows, and immutable hash checks. These are review-data checks, not project tests.

The limited M1 metadata convention covers structured descriptive/control records, textual or binary, embedded or archive-associated, without requiring prose, external/appended position, optionality or disposability. Historical component/grammar evidence does not claim historical software attestation. Old `onfo` and `endar` variants are not declared impossible.

Documentation only. No application/Work/source change, integration, runtime/UI, project-test, native-human, CI, release or merge certification. PR56 remains the never-merge tracking draft.
