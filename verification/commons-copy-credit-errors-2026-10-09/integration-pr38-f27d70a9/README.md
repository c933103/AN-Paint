# Explicit PR34 + PR38 integration candidate

This candidate combines PR34 `f02c2e6bfd51eda81b6d16db10322e1f623dcaec` (tree `e27d7c346452912082089f58278e57dcef46a3ab`) with PR38 `f27d70a925aa659983b25cd875a39b485f44909d` (tree `f6b5c93999c945ef0735efe20c84c045e1c2f8a8`). Both descend from develop `80c14372b0504bc44f9f2809ad477247fdc8100b`. Publication, if accepted, uses these two parents in that order on the existing draft PR34 branch. Develop is not changed.

## Source reconciliation

PR38 changes exactly seven paths from the shared base. Only `.github/workflows/android.yml` and `CI.md` overlap PR34. The combined workflow is byte-identical to PR38 after removing PR34's byte-identical independent generator job. The combined CI.md is byte-identical to PR38 after removing PR34's retained generator/installed-Korean documentation blocks. The other five imported paths are byte-identical to PR38:

- `app/src/androidTest/java/paint/anpaint/android/GalleryViewportDeviceTest.kt`
- `tools/ci_run_timed.sh`
- `tools/test_ci_check_phases.py`
- `tools/test_gallery_font_transition.py`
- `tools/test_ci_release_selection.py`

All other 1,336 previously tracked PR34 paths remain byte-identical. In particular, production locale routing, public identity assertions, fixed Korean expected text, real picker/rotation checks, JSONObject instrumentation compilation correction, Gradle resource generation/probe and SDK-aware inventory remain unchanged. No new font workaround is written here. PR38's original bounded private-display fixture and host synchronization-barrier counterexample are imported exactly once. The callback ordering remains conditional on normal FIFO/no intervening synchronization barrier; it is not a portable queue-drain guarantee. Real setting/system/app font agreement, French/Mongolian 2× viewport assertions, rejecting network fixture and original shared 10-second deadline remain required.

## Validation

The combined source passed all 400 discovered Python tests locally, with no skips, failures or errors. The seven selection contracts also passed separately. Workflow YAML parses, all four jobs are present, source/documentation `git diff --check` passes (the verbatim historical Gradle/logcat logs retain their original trailing spaces), and full-file reconciliation checks the exact remote source/mode maps. `reconciliation.json` includes source deltas and installed-method inventories. These host checks do not establish Android compilation or runtime success.

Expected unchanged runtime inventory: 766 JVM cases; API30 73 native + 18 ordinary app methods; API35 74 native + 19 ordinary app methods + one accepted-credit seed + one verify. The existing API33-only language-label method is excluded explicitly from API30 by its SDK annotation, not counted as a pass. CI normally lacks optional Pillow and may report two host skips; distinguish that result from this 400/400 local pass.

PR34 retains `ci:full-android`. After this exact tree is reviewed, apply and read back the additive `ci:release-android` label before the source update so its normal next run selects release/API30+35. Preserve every existing label. The full-only option still selects debug/API30+35 for other work, and existing manual choices and Release-prefixed develop behavior remain. Importing the option does not itself apply a label or publish a release. Inspect the actual new run and build-info.json rather than inferring its variant or matrix from labels alone.

No combined Gradle, JVM, APK or installed-device run has occurred at this candidate stage. Acceptance requires a new exact-source run: all seven generator stages; strict JVM/orientation/public-identity assertions; both API30 and API35 Korean picker and font/viewport methods; full test inventories; successful lint and source/APK verification. Separate green subsets from PR34 and PR38 are not combined acceptance. PR38's release-configured validation and private upgrade signing remain separately tracked.

## Preserved failure evidence

[The preceding f02c2e6b evidence](../acceptance-f02c2e6b/README.md) retains the overall failed result, API30 failed summary, successful strict Korean phases on both devices, generator logs, JVM inventory and source/AAPT verification. The timeline matches the inherited 80c font-transition signature. It is not proof against every possible test-state interaction, which is why the combined head must run both real flows.
