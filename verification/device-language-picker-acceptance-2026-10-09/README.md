# Device-language picker: final-head acceptance evidence

Source PR: [AN Paint #28](https://github.com/c933103/AN-Paint/pull/28).
This evidence-only branch preserves the tested source head; it does not change the PR code or its test identity.

## Exact identity and gates

- Source head: `7685980e57ad074655fba479b6874d9e5d94f9e2`.
- Complete source tree: `84107dd03e8ac96ed953afd95bf6cbe5b72f84c4`.
- CI merge: `d3744544864ca713b9111cc0830b24c3d39c6146`. Its fetched tree equals the source tree above.
- [Full CI run 37904655049](https://github.com/c933103/AN-Paint/actions/runs/37904655049): regression/lint, APK/source build and installed API35 jobs all succeeded.
- **675 JVM cases passed**, with no failures, errors or skips. This includes all 14 `DeviceLanguagePickerTest` cases.
- **90 installed API35 emulator cases passed**: 74 library, 14 ordinary app, one restart seed and one restart verification.
- Android lint: **0 issues**. APK/source and both instrumentation APK builds succeeded.
- Local host checks: 310 Python cases and `git diff --check` passed. The chat-side host has no SDK, adb or cached Gradle distribution; Android resource-linked, rendering and installed checks ran in the linked CI, not locally.

`final-results.json` preserves suite counts, every installed test result, the relevant picker callback/geometry observations, native image hashes, and exact artifact identities. The original downloaded artifacts remain available from the linked CI run.

## Scope actually checked

The only production change snapshots the device locale and applies the existing shared `VerticalUi.languageChoice` formatter to the first, follow-device row, as it already does for explicit choices. The before/after mechanism control reconstructs the exact old row sequence; it is not a separate full old-app run.

- All 140 offered device locale tags use their existing shared rules. Regional and unsupported tags retain Android's resource fallback. Explicit selection, follow-device, current-choice reselect and cancel keep their semantics.
- API21/25 have focused legacy-graphics resource, typography, attachment/accessibility and override-switch checks. They do not establish native glyph rendering on those APIs. No new framework shadow was added.
- API30/35 native checks cover nine representative horizontal, RTL and vertical device locales under Japanese, Arabic and English app overrides. Each pair opens twice. Mounted row assertions cover an independent literal catalogue label, locale, span/font profile, accessibility label/checkability, at least a 48dp touch target, complete text without ellipsis, and layout fitting the row. Japanese/English overrides use 16sp; Arabic uses 24sp.
- The 18 raw PNGs here are the second opening under the **Arabic app override at 24sp**, for nine device locales on API30 and API35. They are row snapshots, not whole-screen or physical-device captures. All were visually inspected before readiness: the samples show the expected label and existing horizontal/vertical treatment without visible truncation. In particular the en-US row reads the independent literal `Use device language`, while the Arabic row shows its Arabic catalogue label.
- A separate real `ClassicPaintActivity` test checks actual in-place app overrides. The installed API35 emulator test uses real UI taps to choose Japanese, Arabic and English, checking the independent English device label after each. The device is en-US. These are emulator UI-input tests, not physical-device verification.
- The installed selector retains one real tap. It verifies the exact requested accessible label/current bounds, records and delegates the unchanged production item callback, then waits for the actual preference transition. The final en-XV case received position 32; native and accessibility bounds were both `(16,193)-(304,291)`. The override-switch case received positions 59, 6 and 1 for Japanese, Arabic and English respectively.

## Earlier evidence retained

[The source branch investigation record](https://github.com/c933103/AN-Paint/tree/7685980e57ad074655fba479b6874d9e5d94f9e2/verification/device-language-picker-2026-10-09) keeps the initial diagnosed fixture failures, the old installed tap failure and the second run's contradictory native image. The old tap failure's cause remains undetermined because its logs lack the new callback/bounds observations. A later passing run does not establish that old cause.

The generic bare-Activity image mismatch prompted independent literal oracles and real-app tests. Rendering fixtures now use fresh app-wrapped contexts; actual in-place switching is tested separately. The final run passes both routes. No production label-resolution change was inferred from the earlier fixture result.

This closes only the bounded first-row typography increment. It does not establish fluent-language, complete glyph, screen-reader/native-speaker or physical-device acceptance. The vertical-notice joined-emoji experiment remains outside this patch; broader AN-W04 remains open.
