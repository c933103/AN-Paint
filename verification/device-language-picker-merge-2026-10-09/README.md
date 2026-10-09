# PR #28 accepted merge receipt

[PR #28](https://github.com/c933103/AN-Paint/pull/28) merged on 9 October 2026 at 08:52:46 UTC.

## Accepted identity

- Accepted merge: `4b615ce2d9e27814df84812b90858b5f676ce51a`.
- Reviewed source head: `7685980e57ad074655fba479b6874d9e5d94f9e2`.
- Both complete trees are exactly `84107dd03e8ac96ed953afd95bf6cbe5b72f84c4`. This was independently verified by fetching both Git commits and comparing their tree objects. The develop ref matched the accepted merge at the check.
- [Separate Codex Code and Security reviews](https://github.com/c933103/AN-Paint/pull/28#issuecomment-6076362660) completed on the exact reviewed source head without reported findings or inline review threads. Their summary is preserved in `receipt.json`.

## Automatic post-merge verification

[Run 37907698008](https://github.com/c933103/AN-Paint/actions/runs/37907698008), triggered automatically by the develop push, completed successfully at **09:05:07 UTC** on its first attempt. No manual rerun or workflow change was made.

- **675 JVM tests passed**, with zero failures, errors or skips.
- Android lint: **0 issues**.
- **90 installed API35 emulator cases passed**: 74 library, 14 ordinary app, one restart seed and one restart verification.
- APK/corresponding-source and instrumentation APK builds passed.
- All **18 native API30/35 device-row PNGs are byte-identical** to the final pre-merge images already inspected and [preserved here](https://github.com/c933103/AN-Paint/tree/0d073462d0d62fa37a9d9dda5c6c93c95cba47ee/verification/device-language-picker-acceptance-2026-10-09). No duplicate image files are added in this receipt.

`receipt.json` retains exact run, job, review and artifact identities. `regression-results.json` preserves suite counts, lint results and image hashes. `installed-api35-results.json` preserves every installed test result. Downloaded ZIP hashes were compared with GitHub artifact metadata.

## Boundaries and retained history

This accepts the bounded application of existing shared typography to the follow-device picker row. The tests include all offered locale rules, regional/unknown tag fallback, old API21/25 focused legacy-graphics checks, mounted native rows on API30/35, repeated opens and real installed API35 emulator language-selection taps. These establish neither physical-device nor broad fluent-language/native-speaker/screen-reader acceptance. The API21/25 checks do not establish native glyph rendering.

The [earlier failed and withheld evidence](https://github.com/c933103/AN-Paint/tree/7685980e57ad074655fba479b6874d9e5d94f9e2/verification/device-language-picker-2026-10-09) remains unchanged, including the original failed tap and contradictory generic-fixture image. The old tap failure's cause is still undetermined. Broader AN-W04 remains open, and the experimental vertical-notice joined-emoji clipping has not been accepted or changed here.
