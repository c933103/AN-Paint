# A01 title correction: frozen source and independent review

Date: 10 October 2026. [PR42](https://github.com/c933103/AN-Paint/pull/42) implements the bounded correction tracked in [PR7 comment 6095494460](https://github.com/c933103/AN-Paint/pull/7#issuecomment-6095494460).

## Current status: merged and post-merge verified

[PR42](https://github.com/c933103/AN-Paint/pull/42) merged at 15:24:12 UTC as `165a6a503529736527c689e3ac1b5432253d19ee` after the [clean exact-head Codex review](https://github.com/c933103/AN-Paint/pull/42#issuecomment-6099030308). The actual merge has the same reviewed and tested tree `5d7ce333311c452cd7587fd871cdf45d6b6a72ca`.

[Post-merge push CI 38063463830](https://github.com/c933103/AN-Paint/actions/runs/38063463830) passed all three jobs on attempt 1. Independent artifact readback confirms 746 JVM methods, all 9 title and 5 import-flow methods, zero lint issues, Python 369 passed plus 2 optional skips, and 94 installed API35 methods. All four archive hashes match GitHub metadata. APK/source identity, every bundled tracked source file and all raw instrumentation method identities were verified.

[Full post-merge evidence](post-merge/README.md) preserves identities, qualifications and selected raw results. Title rendering is still only tested in API33 Robolectric; installed-device title layout/accessibility and broader localization remain open. No release was published. The historical quota block below was superseded by the renewed successful review; A01 wider acceptance and parent counts are unchanged.

## Historical pre-merge update, 10 October 2026

The following section preserves the result as recorded before the renewed review and merge. Current status is above.

**[CI run 38041522544](https://github.com/c933103/AN-Paint/actions/runs/38041522544) completed successfully on attempt 1.** [Independent exact-source artifact review](independent-review/pr42-runtime-review.md) confirms the same reviewed tree, 9/9 new title tests, 5/5 existing flow tests, 746 JVM tests with no failures/errors/skips, zero lint issues, and all 94 declared API35 methods (74 native/import + 18 editor + two restart phases). Python recorded 369 passes and two optional Pillow skips; skips are not passes.

The earlier local bootstrap limitation remains an accurate local result, but it no longer blocks Kotlin/Robolectric verification: those stages successfully executed in CI. The title assertions ran in API33 Robolectric simulation. Installed API35 animation tests verify decoding, not the warning dialog's visual/layout/accessibility rendering; no screenshot evidence was produced.

A single [final-head Codex request](https://github.com/c933103/AN-Paint/pull/42#issuecomment-6096260829) was made after stable-head CI verification. [The bot response](https://github.com/c933103/AN-Paint/pull/42#issuecomment-6096261882) explicitly reports the code-review usage limit. **No Codex review was performed and no clean Codex review is claimed.** No repeat request, account/credit change, merge or readiness promotion was performed.

[Current status](status.json), [terminal job/artifact identities](independent-review/pr42-terminal-ci.json), [test counts and qualifications](independent-review/pr42-test-verification.json), [build/source verification](independent-review/pr42-build-verification.json), focused XML and raw phase logs preserve the result. CI artifact download retention ends on 24 October; the selected text reports and identities here remain durable. The CI debug-key APK is not an upgrade-signed release.

PR42 remains draft and unmerged. A01's installed-title visual and broader language requirements, original-thread reconciliation, F01 and parent rows are not closed.

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

[Automatic Android CI run 38041522544](https://github.com/c933103/AN-Paint/actions/runs/38041522544) was observed **in progress** at the initial evidence publication (before the terminal update above). That is not a completed validation result. Later exact-head results belong in PR42 and subsequent evidence updates.

## Semantic scope retained

For fewer than two proven frames in the existing warning branch, the title uses existing localized Open still wording. Confirmed exact or lower-bound multiple-frame inputs retain the animation title. Bodies, actions, APNG outcomes, scanner/decoder behavior and null-probe fallback are unchanged. This is a shared source correction; it does not identify a pt-BR mistranslation.

The [seven-resource evidence and partially recovered original scope](https://github.com/c933103/AN-Paint/blob/548bc966ea062613a0087d1127698ca11ecd9caf/verification/ptbr-animation-recheck-2026-10-10/README.md) still applies. Other locale contextual/rendered suitability, complete original-thread reconciliation and runtime acceptance remain open. F01 TIFF compression wording is separate and unimplemented.

No A01 runtime closure or parent-row closure is claimed. The authoritative localization register retains 475 rows, 3 structural completed and 472 pending.
