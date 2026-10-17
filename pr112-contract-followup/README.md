# PR112 complete-value contract and tagged-colour oracle repair

Application head: `4842bfafc49e45d9aaf85471e68ece0972b6fc3f`; tree `d2e0bead9842ba445862f817cfe8a54f6c7e45fa`. Seven test/fixture files change after `75c59756`; production resource bytes are unchanged.

## Findings and repair

The [Codex P1](https://github.com/c933103/AN-Paint/pull/112#discussion_r4301685926) identified incomplete Polish full-text coverage. Every one of the 229 changed full values now has an exact independently reviewed English/Polish pair, plus the two existing composition guards (231 total). The 230th XML node difference is only tail whitespace on an unchanged value. Czech retains all 255 complete changed values; its 256th XML node difference is likewise whitespace-only. All 231 Polish and 255 Czech pairs receive six corruption cases: truncation, alteration, omission, duplication, markup and attributes. Assembly-memory warning clause removal has an explicit negative control: the old subset misses it and both fixed modes reject it.

Both fixtures bind to the original immutable independent review archive and receipt identities. Their complete reviewed-pair digests supplement executable full-text/format/corruption checks; no source-file hash replaces behavior tests. The original fixture values and constraints remain unchanged. The 18 Polish and 21 Czech newly added context-unverified keys remain held. All other original review and Fit layout holds remain.

The previous hosted run’s actual [JUnit failure](previous-hosted-jvm.xml) shows a stale tagged-colour oracle expecting English for Czech, while Android returns the correct independently reviewed Czech value. The family now contains its original 59 expectations plus Czech and Polish, with 110 exact-English fallback expectations. The global 59/112 inventory is unchanged. Negative controls reject missing localization and arbitrary defaults. No resource translation was changed to satisfy the obsolete oracle.

## Evidence

- [Compact receipt](receipt.json): final normal/optimized results, prior failures, source pins, artifact identity and limits.
- [Complete test logs](test-logs.zip): both preserved earlier 840-test timeout failures, their unchanged-method isolated pass, focused checks, and both final exclusive aggregate runs. The only export edit normalizes the validation-workspace prefix; original/export hashes are in the ZIP manifest.
- [Remote source-tree verification](source-tree-verification.json): all 1,169 leaf paths, content hashes and modes matched, with exactly seven test/fixture changes.
- [Independent binding verification](review-binding-verification.json): complete pair counts, original review receipt identities and held keys.
- [Original immutable linguistic review](https://github.com/c933103/AN-Paint/blob/399d7ab1ec6fd197c9824518b470a6d8a0086df9/README.md): retained without replacing or promoting any verdict.

Hosted Android/JVM/device checks and fresh exact-head Codex review are separate pending gates. Local host passes are not Android execution or full-locale acceptance. This evidence ref must not merge into the application branch.
