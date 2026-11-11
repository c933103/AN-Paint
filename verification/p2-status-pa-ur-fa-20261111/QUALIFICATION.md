# PR #433 qualification

Exact head `ae3cc888807db6928e5d962fa4fe16860699ba79`, tested checkout `06c3a0855fbd498def2d510649713d967c2ccdd1`, tree `9705571dba69bacbb7270363cdcc1f3923de790c`, base `5a39710f8207956671c3248922341d5898326e4e`.

[Original PR workflow 42979869318](https://github.com/c933103/AN-Paint/actions/runs/42979869318), attempt one, passed all seven required jobs. Trusted Codex app/bot review completed at that head without code findings. Security review completed with its merge gate disabled. No review threads or requested changes. Live source, clean/open/ready PR, unchanged held owners, unprotected base and empty ruleset inventory were verified immediately before merge.

Downloaded and independently hash-checked six archives: exact-script, APK/source, test APKs, regression/lint, position and composed API35 results. All 1,280 included tracked source blobs matched the source tree; embedded/standalone source and APK/test-APK identities agree. Existing Gradle/Ant exclusions are `.gitignore`, `.idea/codeStyles/Project.xml`, and `colorpicker/.gitignore`; no included tracked blob differs.

Verified results: 13 resource probes, 865 Python passes plus 2 optional skips, 1392 JVM tests with zero failures/errors/skips, 74 native and 50 app API35 methods. The seven position methods are part of the app union, not extra tests. The existing source-discovered app inventory validator and native raw-protocol parser ran independently against the actual bundled Kotlin tests; raw native cases exactly match the checked report. Composed core/position identities, artifact digests and job linkage were checked; the original core archive was not separately redownloaded in this independent pass.

This qualifies the 31 reviewed resource additions, preserving 1,715 prior complete XML nodes and attributes. Model/source review and source-bound hosted reports are not native-human or exhaustive installed UI/glyph/layout/speech/device acceptance. No release or upgrade signing. Older holds, withdrawals, rechecks and explicit restrictions remain unchanged.

verified-results.zip: 495,910 bytes; SHA-256 `32882f791405ed14219f4a2788a0048ccbefe586059a9de9a283996262e12c48`. Contains exact gates, verifiers, source identities and compact checked raw reports; original larger captures/binaries remain linked CI artifacts. Actual merge and normal post-merge results are recorded separately and are not implied by these PR results.
