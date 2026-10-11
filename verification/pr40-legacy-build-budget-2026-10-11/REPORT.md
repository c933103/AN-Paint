# PR #40: carry forward the reviewed cold-build allowance

[The fresh Code review of fea1f628](https://github.com/c933103/AN-Paint/pull/40#discussion_r4241010753) identified one P2: the original manual legacy workflow retained a 26-minute combined assembly step and 40-minute job, despite current develop's 30-minute universal-assembly and 45-minute job allowance. Cold native compilation can consume the old limit before legacy emulator coverage starts.

This bounded correction changes only the manual workflow, its documentation, and its host contract:

- Match current `android.yml`: 45-minute build job and 30-minute universal app assembly.
- Compile both instrumentation APKs in a separate three-minute step, so test compilation does not consume the universal assembly allowance.
- Continue to distribute the exact same prebuilt APK outputs.
- Preserve manual-only dispatch, every API/ABI choice, SDK omissions, strict protocol/source inventory, inner instrumentation deadlines, and the existing device step/job limits.

This is an operational build allowance, not a performance guarantee. It does not prove a cold legacy build or an actual API21/API24 run succeeded.

## Verification

- Seven focused legacy contracts passed.
- The new build-budget contract passed under `PYTHONOPTIMIZE=1`.
- Two injected regressions (job restored to 40 minutes; universal assembly restored to 26 minutes) each failed the actual new test, with no harness errors.
- Both workflow YAML files parsed and all their shell run blocks passed `bash -n`; `git diff --check` passed.
- The final exact-source whole host suite passed: 553 tests, zero failures, in 161.400 seconds. See `host-tests.log`.
- `source-manifest.json` binds the three modified source/document files. It supersedes those three entries from the original repair's manifest; the original repair evidence remains unchanged at immutable parent `fea1f62818adb9fc82532bc61750385b0af2a922`.

Fresh exact-head Code review and Android CI are required after publication. The prior Code review found this P2 and is not presented as a clean review. The API21/API24 app phases remain explicitly NOT RUN, with zero claimed app passes. No actual legacy emulator execution, physical-device coverage, default-branch merge, or release readiness is claimed.
