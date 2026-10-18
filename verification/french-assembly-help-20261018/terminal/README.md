# French assembly Help: final-head CI and review status

PR: https://github.com/c933103/AN-Paint/pull/133
Final application head: `f6ce5b732ceb957d8c4da5f7336c8126375d344f`
Final tree: `9fca189d2e7e404155bb01fe99e6b4e8a39f4b47`
Run: https://github.com/c933103/AN-Paint/actions/runs/39100882873

All six final-head CI jobs passed on attempt 1. Codex Code review is clean on the final head. Security remains unverified on that head: the [review summary](https://github.com/c933103/AN-Paint/pull/133#issuecomment-6245963924) still identifies initial head `aeabd97550d82ea7bff9a0e3e9e5e06e906b2c57`, despite the [single explicit final-head Security request](https://github.com/c933103/AN-Paint/pull/133#issuecomment-6246166543). The old Security result is not carried forward as a final-head pass. No duplicate request or draft-cycle change was made.

## Verified actual artifacts

- 1,130 JVM tests across 121 suites, with zero failures, errors or skips. All three new French methods match source identities and pass: complete compiled Help, real Help toolbar dismissal/reopening with exact full text, and real Exact position/Unplace behavior.
- All 20 source-declared AssemblyActivityTest methods and all seven CropCounterpartGuidanceTest methods pass. This includes the existing full French Help/drag-status method repaired after the initial stale-oracle failure. Annotated methods retain their exact identities; no method is omitted.
- 942 hosted Python checks pass. Before the workspace reset, final-source local host checks also passed 942 normally and 942 with optimization; the 22 focused checks, full resources/mirrors/link, catalogue structure and supplementary changed Kotlin compilation passed. Local Gradle/Robolectric remained network-blocked at distribution download.
- The complete source-bound API35 union passes: 74 native and 45 app methods, without missing, unexpected, failed, skipped or timed-out methods. Core/position identities match the same checkout, run, variant, APK and source hashes.
- The actual APK embeds exactly the companion source ZIP. All 1,209 packaged tracked source files match final reviewed blob contents and executable modes. The three omitted files are repository/editor metadata: `.gitignore`, `.idea/codeStyles/Project.xml` and `colorpicker/.gitignore`. The build uses the CI debug key; upgrade signing is separate.
- All nine exact-script clean/incremental probes pass, with correct final source tree and matching raw log hashes.

The PR checkout `b91e98bd1cfe7a980e476fa4fe88a0d57e2c4c8d` has the same tree as the final application head. Artifact digests were checked against GitHub before content verification. No production repair, assertion weakening, cap/deadline change or manual job rerun was used.

## Initial review, failure and bounded repair

[Initial complete-entry review and local evidence](https://github.com/c933103/AN-Paint/blob/aafa034f631522a587191b1fc4d133519d50ff8e/verification/french-assembly-help-20261018/README.md) retains the complete old/new/corrected-English values, both full-entry model/source reviews, source bindings and raw local checks. Only one production value changes; five paragraphs and every other production byte remain intact.

[Original failure evidence](https://github.com/c933103/AN-Paint/blob/a7db3e5d1b9b3e805d5248bed110bbeeca5a6abf/verification/french-assembly-help-20261018/initial-failure/README.md) retains the first run’s one failed comparison among 1,130 JVM tests, all original JVM XML and phase logs. Its three new French methods already passed. The sixth changed file updates only the existing complete inline French Help oracle to the same reviewed eight-paragraph text. Full equality, the real toolbar, subsequent drag-status assertion and every other test-file byte are preserved. The failed original record is not replaced by the final pass.

## Evidence integrity and limits

The shared workspace reset during final archival, after verification. GitHub source and previously archived evidence remained intact. The final artifacts were downloaded again, digest-checked and independently reverified using the included script. Initial local raw logs remain in the earlier evidence ref; final local raw logs were lost in the reset. The final hosted Python/JVM phase logs and every JVM XML remain available and are included here. The final optimized local count is an observed pre-reset result, not a newly recovered raw log.

`checks.json` records exact run/job/review/source/artifact identities. `verification-packet.zip` includes all final JVM XML, CI phase logs/timings, device XML/JSON, exact-script logs, verification code and per-file hashes. Related test XML is separate. This evidence commit preserves all final application blobs/modes and every prior evidence file; older source versions remain reachable in history.

This is bounded full French assembly Help verification. It does not certify the full language, native-speaker acceptance, installed French glyph/layout, enlarged-font, TalkBack or physical-device behavior. Ordinary API35 coverage does not establish French-specific installed appearance. The separate main-editor manual’s guaranteed gap filling at line 465 remains open. PR75’s wider obligations, PR56 and locale routing are unchanged.
