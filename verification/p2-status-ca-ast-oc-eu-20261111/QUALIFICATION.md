# PR #432 qualification

Exact head `126e151a8e5f650c22c1072a43c5f6da81e78591`, tested checkout `f1aee229fcba5833ccc030d8ff73dc1f30be534d`, tree `ecf163df40e7a7d58cdc42e1c77875cdbd9b0b5a`, base `7d41d341956a6fcd4246cb2ff8d05d7ad20e45f9`.

[Original PR workflow 42974214906](https://github.com/c933103/AN-Paint/actions/runs/42974214906), attempt one, passed all seven required jobs. Trusted Codex app/bot review completed at that head without code findings. Security review completed with its merge gate disabled. No review threads or requested changes. Live source, clean/open/ready PR, unchanged held owners, unprotected base and empty ruleset inventory were verified immediately before merge.

Downloaded and independently hash-checked six archives: exact-script, APK/source, test APKs, regression/lint, position and composed API35 results. All 1,280 included tracked source blobs matched the source tree; embedded/standalone source and APK/test-APK identities agree. Existing Gradle/Ant exclusions are `.gitignore`, `.idea/codeStyles/Project.xml`, and `colorpicker/.gitignore`; no included tracked blob differs.

Verified results: 13 resource probes, 865 Python passes plus 2 optional skips, 1392 JVM tests with zero failures/errors/skips, 74 native and 50 app API35 methods. The seven position methods are part of the app union, not extra tests. The existing source-discovered inventory validator ran against the actual bundled Kotlin tests. Composed core/position identities, artifact digests and job linkage were checked; the original core archive was not separately redownloaded in this independent pass.

This qualifies the 32 reviewed resource additions, preserving 1,628 prior complete XML nodes and attributes. Model/source review and source-bound hosted reports are not native-human or exhaustive installed UI/glyph/layout/speech/device acceptance. No release or upgrade signing. Older holds, withdrawals, rechecks and explicit restrictions remain unchanged.

verified-results.zip: 490,228 bytes; SHA-256 `95652ad1be0152f15fab5f36752c3b68d5751a43f0c7170f10c6e39a4a8838e8`. Contains exact gates, verifiers, source identities and compact checked raw reports; original larger captures/binaries remain linked CI artifacts. Actual merge and normal post-merge results are recorded separately and are not implied by these PR results.
