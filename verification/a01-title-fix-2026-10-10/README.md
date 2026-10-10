# A01 title correction: frozen source and independent review

Date: 10 October 2026. [Draft PR42](https://github.com/c933103/AN-Paint/pull/42) implements the bounded correction tracked in [PR7 comment 6095494460](https://github.com/c933103/AN-Paint/pull/7#issuecomment-6095494460).

## Source identity

- Base commit: `80c14372b0504bc44f9f2809ad477247fdc8100b`.
- Published source commit: `f89fb76e6721e14f3e0b714116795530088812a6`.
- Reviewed and published source tree: `5d7ce333311c452cd7587fd871cdf45d6b6a72ca`.
- Source branch: `fix/a01-animation-warning-title-20261010`.
- One production expression changed; two tests added; 1,289 original files unchanged and no removals. All three remote blobs and full source tree were verified before the PR was opened.
- Evidence is deliberately on a separate branch so the reviewed application tree stays exact.

## Review and test classification

[Independent review](independent-review/review.md) found no actionable source defect in the one-line change. It is a model source/host review, not native-speaker certification or a GitHub Codex clean-review result.

Independently executed: 48 host tests, five rejected title-wiring mutations, and 25 production-Java scanner fixture probes. See the review, [integrity identities](independent-review/integrity.json), [negative controls](independent-review/negative-controls.json), [scanner probes](independent-review/scanner-extra-results.json), and host logs alongside them.

The nine new Robolectric methods and existing ImportSelectionFlowTest were **uncompiled/unrun locally**. [The exact failed attempt](evidence/robolectric-attempt.log) stopped while the Gradle wrapper tried to fetch its uncached 8.13 distribution: Network is unreachable. No Gradle task or Kotlin compiler ran. Local Java 21 supported host scanner compilation; no working Android toolchain was established.

The original [candidate manifest](evidence/candidate-manifest.json), [author validation summary](evidence/validation-summary.json) and independent review are preserved as **prepublication snapshots**; statements there that no remote upload had occurred refer to that earlier review stage. This README records their subsequent publication. Source patch: [recalculated.patch](independent-review/recalculated.patch). The preserved [extra scanner script](independent-review/scan_extra_states.py) expects a sibling directory named `candidate` containing the exact source checkout, as in the review workspace; it never runs Kotlin or Android UI.

[Automatic Android CI run 38041522544](https://github.com/c933103/AN-Paint/actions/runs/38041522544) was observed **in progress** at publication. That is not a completed validation result. Later exact-head results belong in PR42 and subsequent evidence updates.

## Semantic scope retained

For fewer than two proven frames in the existing warning branch, the title uses existing localized Open still wording. Confirmed exact or lower-bound multiple-frame inputs retain the animation title. Bodies, actions, APNG outcomes, scanner/decoder behavior and null-probe fallback are unchanged. This is a shared source correction; it does not identify a pt-BR mistranslation.

The [seven-resource evidence and partially recovered original scope](https://github.com/c933103/AN-Paint/blob/548bc966ea062613a0087d1127698ca11ecd9caf/verification/ptbr-animation-recheck-2026-10-10/README.md) still applies. Other locale contextual/rendered suitability, complete original-thread reconciliation and runtime acceptance remain open. F01 TIFF compression wording is separate and unimplemented.

No A01 runtime closure or parent-row closure is claimed. The authoritative localization register retains 475 rows, 3 structural completed and 472 pending.
