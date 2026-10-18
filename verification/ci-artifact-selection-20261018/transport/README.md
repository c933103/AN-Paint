# Exact-ID transport correction, integrated source

PR [136](https://github.com/c933103/AN-Paint/pull/136), head `817ec4633b697a3ac0b33d584292fba2b8292cbd`, tree `9c7d9123a134ab75e8bc5f2d090e283f4ac0f218`. The synthetic PR checkout `287a2387163d38c54c904462172c2bdfae5f8ff6` has that identical tree. Current develop `4380b734438a25c74289f85e79e794039165d78c` is a parent: all source/tests from #135, #133 and #123 are preserved. Only seven CI code/test/documentation files differ from that develop baseline, with no removals. Every one of the 1,224 remote tracked blobs/modes was checked against the proposed local tree before publishing the head.

## Why a second transport correction was necessary

The [initial preserved diagnosis](https://github.com/c933103/AN-Paint/blob/4d027e2ed0525888c120cac018cc7936aaab1ea0/verification/ci-artifact-selection-20261018/initial/README.md) records original run 39126110768, both same-name position artifacts, their jobs/attempts/timestamps/digests, the original failed composer and successful local correct-ID composition. That original hosted run remains failed. No evidence or old artifact was deleted.

Inspection of the [pinned download action](https://github.com/actions/download-artifact/blob/3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c/src/download-artifact.ts) found that its ID-download path still calls `listArtifacts({latest: true})`. The SDK's name deduplication sorts numeric IDs descending. Merely giving that action a correct lower artifact ID can therefore lose it before download. The earlier patch head `2477633f0a1eab2dc4ea4fd090d4ced697ab3467` is superseded and its review/results do not certify this head.

The current head keeps interval/source selection but directly GETs each exact REST artifact ID using the runner's existing `gh api`. It verifies the selected SHA-256 before bounded ZIP extraction and refuses unsafe paths, symlinks, duplicate members and overwriting existing evidence, including the selector receipt. Existing ephemeral credentials are consumed by the GitHub CLI, never printed or passed as command-line token values. Read-only Actions metadata access remains job-scoped. The complete inventory/APK/source-hash composer is unchanged.

Existing eight-minute composition-job, device, interaction, phase and setup caps are unchanged. The selector has a one-minute step and a shared 45-second metadata budget; each download has a 90-second deadline within a four-minute transport step. Report archives are checked against 128 MiB compressed, 512 MiB expanded and 10,000-member bounds. These are cancellation/input bounds, not measured universal runtime guarantees.

## Checks completed as of 2026-10-18 13:15 UTC

- All 976 integrated host tests passed normally (169.451s) and with optimization (168.221s).
- 11 selector and eight direct-transport regressions pass. The original eight composition tests remain, with only download-wiring assertions adjusted.
- A local transport fixture supplies the original downloaded core artifact `12136657509` and successful position artifact `12136049338`, preserving their selected-ID REST requests. SHA-256 validation, safe extraction and the unchanged complete 45-method composer pass with core attempt 1 plus position attempt 2. This fixture does not claim a new network transfer or hosted composition.
- The first supplementary local invocation used the wrong environment variable name and stopped with `KeyError: BUILD_VARIANT` before composition. The corrected invocation and its complete result are retained; this diagnostic error is not a production/CI failure or a suppressed test.
- [Code review](https://github.com/c933103/AN-Paint/pull/136#issuecomment-6250140174) completed clean at current head `817ec463`. Security remains advisory; its latest completed result at this snapshot covers the prior head only, with a current-head request pending.
- [Hosted run 39129926489](https://github.com/c933103/AN-Paint/actions/runs/39129926489): build and all nine exact-script probes passed. JVM/lint, core/position API35 and final composition are still pending/running. No complete hosted-pass claim is made by this snapshot.
- The debug APK's embedded source equals the companion source ZIP. All 1,221 packaged tracked blobs/modes match this exact current tree. Only `.gitignore`, `.idea/codeStyles/Project.xml` and `colorpicker/.gitignore` are omitted metadata. `build-binding.json` records the original artifact digest and APK/source identities.

`local-transport-packet.zip` is 6,548 bytes, SHA-256 `2020682822bdf01ff08210f91c344683898b32adab7b2883ddf6bc2002b325e7`. It retains normal/optimized host logs, the local transport/composition receipt, reproducible fixture script, initial invocation-error note and publication identity. Its per-member manifest was verified after creation. This ref adds these records to the entire exact patch source tree; the earlier evidence ref remains immutable and reachable separately.

This is CI recovery and integrated development-build evidence. It does not establish a release, physical-device, Chinese installed-appearance/TalkBack or whole-language acceptance. CN full Help and eight Sinitic catalogue follow-ups remain unreviewed as recorded in tracker75.
