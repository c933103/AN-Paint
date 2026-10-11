# PR18 installed locale matrix: current-base candidate

This is a test-only adaptation, not an installed-runtime completion claim.

## Base and historical provenance

- Accepted develop at preparation: `eab28203893ffba45f14a7f96df6d19cf4d19d3b`.
- Required SDK-inventory prerequisite: PR36 head
  `034cd5d92a66ba244afbd2040201ee31f1ccf726`, tree
  `d9858229f98068bef9c6194c90d77610c5ecceec`. The temporary baseline's full Git
  tree matches that remote tree exactly. PR36 acceptance is separate.
- PR18 head `040d64f43a6cf938a0a0b3985942774fb6380fd4` and later autosave
  readiness repair `b6c560d32` are historical source inputs. The PR19
  reconciliation `a1f9d6d8cf4062c4f764c3436a73ecec21a59d9a` explicitly excluded
  this matrix; ancestry alone cannot close PR18.
- The current production sources, existing editor/Gallery/restart methods,
  SDK-aware runner and workflow YAML are unchanged by this candidate.

## Retained acceptance scope

Four installed methods each exercise portrait and landscape for `mnc-Mong`,
`lzh-Hant`, `en-XV` and `qaa-Zsye-XV`:

1. Open the actual picker, position its viewport, select the exact real row
   with native input, observe the actual callback and follow replacement
   activities until current startup and locale readiness are established.
2. Physically select View, Draw, File, Edit and Color, asserting only the
   requested panel is selected. Preserve the 100×100 document and both sentinel
   pixels throughout; retain a usable canvas and vertical status rail.
3. Open Brush then Insert, select Line before Arrow, wait for the actual
   scheduled autosave generation, reveal overflow with native swipes and assert
   Arrow selection. Passive input logging does not consume touch events.
4. Check initial File and Save column position in the locale's reading order.
   Open Save as, physically choose JPEG in the native popup, assert `.jpg`,
   reachable quality control and hidden lossless control; cancel, reopen with
   PNG unchanged, then dismiss using native Back.
5. Reject any external picker/save/share destination throughout. Restore prior
   orientation and language and remove monitors/listeners in teardown.
6. Retain 32 expected installed screenshots: four locales × two orientations ×
   workspace / initial Save / open format popup / JPEG quality. Failures retain
   any additional failure screenshot for diagnosis.

Ribbon/tool/dialog actions never use `performClick`, `requestRectangleOnScreen`
or programmatic scrolling. Picker viewport positioning is the documented setup
exception. No clipboard, remote-gallery fixture or encoding destination is added.

## Current runner integration

The ordinary app invocation excludes the vertical class and both restart classes.
The separate vertical invocation derives all other class exclusions from source,
so future ordinary classes cannot accidentally enter the bounded matrix. Native,
ordinary and vertical invocations each retain a 180-second deadline; seed/verify
retain 60 seconds each, with the original 15-minute outer step unchanged.

The new coverage checker requires exact, disjoint, successful reports with one
captured integer device SDK matching the selected platform in every phase. The
captured SDK is validated before applying source `@SdkSuppress` bounds, retaining
PR36's accepted-credit fix for future SDK-ineligible ordinary methods. Missing,
string, boolean, fractional or mismatched SDK values fail closed. On API35 the candidate inventory is 18 ordinary + 4 vertical
+ 1 seed + 1 verify = 24 app methods. On API30 it is 17 ordinary + 4 vertical =
21 executed app methods, one AndroidX-SDK-suppressed editor method and two
explicitly omitted API35 restart methods. Omissions are never counted as passed.

The external live-process seed/force-stop/verify sequence is retained. Only its
final aggregate checker moves to the main driver so the vertical report can be
included. Existing accepted-credit coverage output remains available alongside
the new full app receipt. Missing/failed vertical coverage cannot turn green
because the ordinary or restart suites pass.

Fresh summaries/screenshots are cleared before the matrix. Bounded EXIT cleanup
pulls images before shutdown even on failure/timeout. A missing pull or incomplete
32-image inventory changes a successful exit to failure and preserves an existing
nonzero exit. PNG receipts check headers and record dimensions/size/SHA-256 only;
they do not substitute for opening and visually reviewing the screenshots.

## Verification performed

- Full Python contracts: **375 tests passed**, no skips, in 55.193 seconds.
  `host-contracts.log` retains the actual output. Some tests intentionally print
  rejected protocol fixtures; the overall unittest result is the authoritative
  host result.
- Added matrix host tests cover both SDK selections, future classes, every phase
  missing/duplicate/unexpected/skipped/wrong-SDK result, screenshot failure,
  one-shot native runner selection, stale-summary removal, screenshot collection
  before shutdown and preservation of a prior failure exit.
- CLI fixtures cover future methods with both minimum and maximum SDK bounds
  on API30 and API35, including the inclusive boundary. SDK-ineligible methods
  never receive pass credit. Existing three-phase runner checks remain unchanged.
- Existing accepted-credit fake-ADB tests retain PR36's SDK-bound future-method
  regression, now requiring a seven-method union including all four vertical
  methods when that future method is ineligible. They continue to cover real ten-second
  command deadlines, a benign 16-second setup delay, PID disappearance/change,
  incomplete seed, failed/ineffective force-stop and bounded harness cleanup.
- Bash syntax and `git diff --check` passed.
- Local `:app:compileDebugAndroidTestKotlin` did **not** run: the pinned Gradle
  distribution was uncached and its network download was unavailable in the
  original candidate attempt. That historical wrapper failure is retained in
  `local-compile-unavailable.log`; it is not a compilation attempt or result for
  this reconciliation. The current environment still has no configured Android
  SDK, `adb` or `kotlinc`. Host tests do not establish Kotlin compilation or runtime.

## Exact-head completion gates still required

After source review and publication, verify the remote source tree and run the
normal current-platform CI for that exact candidate:

- Production/test APK compilation, full host/JVM regressions and lint.
- Successful native/import, ordinary app, vertical app and accepted-credit
  seed/verify XML and raw logs, with no unexpected/missing/ignored results.
- Measured phase durations within existing budgets; do not increase deadlines or
  retry missed native input to hide a failure.
- All 32 installed PNGs downloaded, hash/filename checked and visually inspected
  for all locales and orientations. Check joining, upright glyphs, intact emoji,
  reachable controls and displayed states as bounded UI observations, not broad
  linguistic certification.
- API30 remains a full-release/cross-version-risk gate under current CI policy.
  No physical-device, broad language certification or release claim follows from
  this test-only candidate.

PR18 should remain unresolved until a reviewed current-base continuation passes
these gates and its original discussion is reconciled with the new evidence.
