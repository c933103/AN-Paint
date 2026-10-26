# PR175 actual postmerge terminal evidence

Merge [`05607f0d60131cc9148461ce595155d820748e4e`](https://github.com/c933103/AN-Paint/commit/05607f0d60131cc9148461ce595155d820748e4e), tree `16ff3d877650ad4ad3198ce19007e8606fcd080a`, passed **all six checks** in actual push [run 40295442728](https://github.com/c933103/AN-Paint/actions/runs/40295442728), completed 2026-10-26 09:16:17 UTC. These are newly downloaded and verified merge artifacts, not relabelled PR results. Explicit `develop` remained at this merge at terminal verification. The source snapshot stays pinned if the branch later moves.

Signed merge and ordered parents df9bc04 + reviewed f6b3e71 were verified; merged/reviewed trees are identical. All 1,370 local source blobs were freshly Git-verified. All 1,367 packaged Git-tracked project files match exact bytes, with the same three explicit dotfile exclusions. Embedded/external sourceZIPs match. Extra vendored/generated members are counted, not asserted to be authenticated by the project Git tree.

Actual postmerge results:
- **1,355 JUnit tests** /145 reports: zero failures/errors/skips; all six focused source-method inventories match.
- Hosted Python **1,374 run =1,372 passed +2 skipped**, 169.153 s. Skip identities are not named in nonverbose output and are not guessed. Local ordinary and optimized 1,374/zero-skip results remain separately recorded in r04.
- Lint **zero issues**; all phase exit codes zero.
- API35: **45 app +74 native** exact source-case sets passed; fresh main/test APK and corresponding-source identities revalidated.
- All **13 exact-script** probe hashes/expected exits verify, including the intended reserved-variant rejection.
- Compiled **78 da +78 no +80 prior nn** scoped values match exactly. CI debug signature v1/v2 verifies.

Merge APK SHA256: `08ef7189161fafea5d2cf2e8dd50582afe0d06729593dee3d59baed45b8df504`. SourceZIP SHA256: `3c3f6afbc96701a9666eb767625b3f453d1206be71777f6a8f6bf37d30d5d07b`. The corresponding-source ZIP is identical to the PR's because the trees match; the freshly built/debug-signed APK is separately verified and is not claimed identical. CI debug signing is not private upgrade or release signing.

`merge-source-verification.json` preserves the initial source-identity snapshot with CI in progress. `terminal-gates.json` and actual artifact receipts supply the later terminal outcome without silently rewriting that historical receipt. Verifier scripts are hash-bound to r05 and reproducible against the listed artifact IDs/ZIPs and source pin.

No failure or rerun occurred in this merge run. The completed monitor is closed. No release, native-human, physical-device, whole-language or layout certification. Existing held absences, review qualifications, paired P1/frozen history, #56/#113/#159 and Help/release pauses remain unchanged. Integrated 171-option coverage is recorded separately in r07.
