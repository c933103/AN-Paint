# PR #434 qualification

Exact head `17c24d0e6f10a3a9cf61d9d1c5bb988a9a408e68`, tested checkout `ee2dc5b8b552864d6aee0b87fef03c36e01fe26f`, tree `b0630eb17f88334f31c0c5f5fdc476db2a601c1b`, base `ecdf4d97c431bc49eb4356f6a6abf8cd2600d466`.

[Original PR workflow 42984652996](https://github.com/c933103/AN-Paint/actions/runs/42984652996), attempt one, passed all seven required jobs. Trusted Codex app/bot review completed at that head without code findings. Security review completed with its merge gate disabled. No review threads or requested changes. Live source, clean/open/ready PR, unchanged held owners, unprotected base and empty ruleset inventory were verified immediately before merge.

Downloaded and independently hash-checked six archives: exact-script, APK/source, test APKs, regression/lint, position and composed API35 results. All 1,280 included tracked source blobs matched the source tree; embedded/standalone source and APK/test-APK identities agree. Existing Gradle/Ant exclusions are `.gitignore`, `.idea/codeStyles/Project.xml`, and `colorpicker/.gitignore`; no included tracked blob differs.

Verified results: 13 resource probes, 865 Python passes plus 2 optional skips, 1392 JVM tests with zero failures/errors/skips, 74 native and 50 app API35 methods. The seven position methods are part of the app union, not extra tests. The existing source-discovered app inventory validator and native raw-protocol parser ran independently against the actual bundled Kotlin tests; raw native cases exactly match the checked report. Composed core/position identities, artifact digests and job linkage were checked; the original core archive was not separately redownloaded in this independent pass.

This qualifies the 32 reviewed resource additions, preserving 1,611 prior complete XML nodes and attributes. Model/source review and source-bound hosted reports are not native-human or exhaustive installed UI/glyph/layout/speech/device acceptance. No release or upgrade signing. Older holds, withdrawals, rechecks and explicit restrictions remain unchanged.

verified-results.zip: 494,397 bytes; SHA-256 `0e93ef1b8977ac46e9a2b9af483cae9e6cd21474e3b249ab4d14730fd9509567`. Contains exact gates, verifiers, source identities and compact checked raw reports; original larger captures/binaries remain linked CI artifacts. Actual merge and normal post-merge results are recorded separately and are not implied by these PR results.
