# API35 popup capture repair: bounded accepted evidence

This is an **unexecuted, evidence-only documentation continuation** of tested PR18 head `66c39ca345ef7bc8c5fe1da8ce64cb872c3a0e88`. The application/test source was executed at tree `a90cdf84be34e6a08ab7a9d25b46cdce2f71b776`, using synthetic merge `f2162094bec001f13970ae7cf79621aec94c6e3a`, whose complete tree matches that head. This record does not claim that its new documentation tree ran CI. PR18's code head remains unchanged.

`source-equality-proof.json` records that every existing path, blob and mode from the tested source tree is unchanged. All additions are confined to this evidence directory. `evidence-files.json` hashes the retained files; `raw-reports-manifest.json` binds every original member of `raw-reports.zip`.

## Exact run and results

- [Run 38022416053, attempt 1](https://github.com/c933103/AN-Paint/actions/runs/38022416053/attempts/1), all three jobs succeeded.
- Build job `114126059333`: production APK and both instrumentation APKs compiled successfully, including the changed popup-readiness Kotlin.
- Regression/lint job `114126059239`: 737 JVM cases across 77 XML files, zero failures/errors/skips; lint XML contains zero issues.
- CI host suite: 382 tests run, 2 optional Pillow-dependent skips, 71.537 seconds. The skipped checks are `test_adam7_fixture_pixels_match_independent_pillow_decoder` and `test_export_opens_with_independent_pillow_ico_decoder` in `IcoContainerTest`. Local and independent host runs passed all 382 without skips.
- API35 job `114127351184`: all 98 installed cases passed. Native 74 / ordinary app 18 / vertical 4 / seed 1 / verify 1. The SDK35 app union is exactly 24, with disjoint phases and no omissions or skipped cases.
- Instrumentation seconds: native 79.585; ordinary 165.967; vertical 121.531; seed 8.080; verify 9.252. The runner completed at +439 seconds. Existing 180/60-second phase limits and 15-minute outer deadline were unchanged.
- The boundary retains a complete successful seed, the same live PID `5643`, Gallery still resumed with an undelivered result, external force-stop, positively verified PID absence, and fresh-process verification. No activity-recreation substitute or input retry was introduced.
- [API35 artifact 11659005722](https://github.com/c933103/AN-Paint/actions/runs/38022416053/artifacts/11659005722), verified ZIP SHA-256 `cbb0326a2ce6a5e25325bb2fbdc6844d4bb0ac7f99d3eec3ffbbd77a894e0577`.
- [Regression artifact 11659350322](https://github.com/c933103/AN-Paint/actions/runs/38022416053/artifacts/11659350322), verified ZIP SHA-256 `3c8bc4785ded65d9c0720cb8acebeb1c1889652ddedd67af3bd97863ea243c78`.

Original installed XML, phase summaries/raw instrumentation logs, restart boundary, startup/collector receipts, all regression XML/lint XML and complete build/regression/emulator job logs are retained byte-for-byte in `raw-reports.zip`. The archive contains 113 files, including 83 XML files (82 test reports plus lint). All 32 actual screenshots are separately retained under `screenshots/`, with source/run/artifact and per-image hashes in `visual-receipt.json`. No signed download URL is retained.

## Accepted capture-state result

All 32 fresh PNGs matched their filename, byte-size, dimensions and SHA-256 receipt, fully decoded and had distinct byte and decoded pixel contents. Both the implementation worker and an independent reviewer opened every original image individually. All eight expected format images now show the open native popup. In particular, [en-XV landscape popup](screenshots/en-XV-landscape-format-popup.png) is visibly distinct from the [closed Save form](screenshots/en-XV-landscape-save-initial.png).

The independent review accepts this **bounded capture-state evidence** and clears the stale-popup screenshot failure. The original failed pair and all 32 rejected images remain unchanged in `../attempt-2-visual/`; they are never counted as screenshots of this repair.

Canvas/sentinels, initial Save forms, native popups and JPEG quality states are observed in their captured viewports. Visible Manchu joining, upright Literary Chinese glyphs and displayed emoji are bounded rendering observations, not linguistic certification.

## Unresolved follow-up: viewport and full-range control reachability

Capture-state acceptance does not close broader vertical-locale usability.

The [Manchu landscape JPEG image](screenshots/mnc-Mong-landscape-jpeg-quality.png) clips the quality slider thumb at the right viewport edge. Several portrait images also show partial labels or neighboring columns, for example [Literary Chinese JPEG quality](screenshots/lzh-Hant-portrait-jpeg-quality.png) and [vertical emoji JPEG quality](screenshots/qaa-Zsye-XV-portrait-jpeg-quality.png).

These observations require controlled horizontal-scroll and full-range native-interaction verification. They are **not automatically confirmed production defects**: the form is horizontally scrollable, while a single screenshot cannot establish reachability of every part.

- [ ] Follow the real Save flow and record horizontal-scroll positions and visible bounds for the affected controls.
- [ ] Use native gestures to bring each affected label and complete quality control into view; establish whether both ends and the current thumb are reachable without clipping or loss of other required actions.
- [ ] Exercise the quality slider through its full intended range with native input, verify actual resulting values, and capture before/after states.
- [ ] Check relevant locale/orientation cases and interrupted/reopened Save behavior; retain exact-source evidence. Use API30/API35 for release verification or a diagnosed cross-version risk.
- [ ] Classify any reproducible production issue separately, or record evidence that horizontal scrolling provides full access.

Current evidence does not certify full-range slider reachability, complete simultaneous control visibility, broad usability, physical-device behavior or API30. PR18 remains subject to its dependency and review decisions; this record makes no merge or release claim.
