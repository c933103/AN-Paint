# PR #431 qualification

Exact head `4fc57f167505dc99ea4088466ff1564ae0c17616`, tested checkout `a1c5d7d2b7994b0bc5c1f9206ca60555081e13bb`, tree `b1dda28cc02cdecdfb81a7c28037bee99f58a01e`, base `755f25524b5e676b9d0f2a33ef65ba46aa815065`.

[Original PR workflow 42969090241](https://github.com/c933103/AN-Paint/actions/runs/42969090241), attempt one, passed all seven required jobs. Trusted Codex app/bot review completed at that head without code findings. Security review completed with its merge gate disabled. No review threads or requested changes. Live source, clean/open/ready PR, unchanged held owners, unprotected base and empty ruleset inventory were verified immediately before merge.

Downloaded and independently hash-checked six archives: exact-script, APK/source, test APKs, regression/lint, position and composed API35 results. All 1,280 included tracked source blobs matched the source tree; embedded/standalone source and APK/test-APK identities agree. Existing Gradle/Ant exclusions are `.gitignore`, `.idea/codeStyles/Project.xml`, and `colorpicker/.gitignore`; no included tracked blob differs.

Verified results: 13 resource probes, 865 Python passes plus 2 optional skips, 1392 JVM tests with zero failures/errors/skips, 74 native and 50 app API35 methods. The seven position methods are part of the app union, not extra tests. The existing source-discovered inventory validator ran against the actual bundled Kotlin tests. Composed core/position identities, artifact digests and job linkage were checked; the original core archive was not separately redownloaded in this independent pass.

This qualifies the 32 reviewed resource additions, preserving 1,631 prior complete XML nodes and attributes. Model/source review and source-bound hosted reports are not native-human or exhaustive installed UI/glyph/layout/speech/device acceptance. No release or upgrade signing. Older holds, withdrawals, rechecks and explicit restrictions remain unchanged.

verified-results.zip: 465,187 bytes; SHA-256 `10632f235fdf18c174a1f7664f496c622431ed046b5d98e6ce83bec3b5c3d386`. Contains exact gates, verifiers, source identities and compact checked raw reports; original larger captures/binaries remain linked CI artifacts. Actual merge and normal post-merge results are recorded separately and are not implied by these PR results.
