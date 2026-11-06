# Priority localization release integration

This is a focused integration onto develop `412aab0c604060fb66fbd2edc6bb05572d10b56d`, not a merge of the accumulated evidence-history branch or PR56.

## Current changes

The integration carries 171 canonical locale catalogues, the horizontal NumericSlider wrapping/minimum-height repair and native-layout regressions, 20 inclusive frame-count fragments for P0 warnings, targeted wording fixes and diagnosed CI/test repairs. Tests preserve current-resource consumer behavior rather than freezing previously approved sentences.

The final resource checkpoints `8cceb44f` and `9b46d108` apply 107 reviewed existing-value corrections across 39 catalogues. They add no resource identities or missing P2/P3 translations. Default English, production consumers, tests, workflows, version, permissions and signing data are unchanged by those resource checkpoints. The subsequent report compaction changes only these two Markdown summaries.

## Verification boundaries

- 856 host contract tests passed in 180.621 seconds on the 104-change candidate including the live Ainu decoding clarification.
- The two dormant Ainu follow-throughs passed 40 affected translation/boundary tests, all 38 affected catalogue validators and 318 actual JDK formatting cases on their final candidate.
- The final Azerbaijani unit correction passed the same 40 affected tests, its catalogue validator and three actual JDK caption/slider-wrapper cases.
- Published resource head `9b46d108445d15c3aae3557960da58f9de240e4d` and all 1,278 remote leaves/modes were reconciled with the reviewed checkout, expected parent and non-force branch lease.
- Exact-head CI and Codex status are tracked on [PR297](https://github.com/c933103/AN-Paint/pull/297). Prior runs are not relabelled as execution of a later head; superseded cancellation is not a diagnosed regression.

These checks do not certify universal installed layout, fonts, accessibility or native fluency.

## Evidence and release gates

[Review scope and current authority limits](existing-string-review-20261106.md) links the detailed records retained at immutable evidence commit `9b46d108`, protected from accidental collection by dedicated ref `evidence/localization-review-20261106-9b46d108`.

[Archived chronology, exact predecessors/successors and prior test receipts](https://github.com/c933103/AN-Paint/blob/9b46d108445d15c3aae3557960da58f9de240e4d/verification/translations/priority-release-integration-20261106.md) remain available without bulky inventories in the application patch.

No release is declared ready here. Required gates remain exact-final-head CI/Codex review, a release-configured develop **push** run, upgrade signing with the existing certificate, all four ABIs/16KB alignment, and matching embedded/separate corresponding source. A release-configured PR run does not publish or replace the final develop execution. The existing publisher request for 0.0.40 must not be reused for the new version; no private signing key or backup belongs in GitHub.
