# Vertical notice resize characterization: current compiled resources

Status: test-only source prepared on 9 October 2026. **Android compilation, all
eight new API30/35 executions, pixel/event outputs, lint, installed tests and
hosted CI are pending.** No production resize policy is selected or implemented.

## Baseline and why this is a successor

The current base was re-read as
[b9a79613b088c9ff54f2c225f6ae53d5b8d8ae61](https://github.com/c933103/AN-Paint/commit/b9a79613b088c9ff54f2c225f6ae53d5b8d8ae61),
tree eea34eac70c8e425648fd6e1370af9643c710bf3. The temporary checkout was
materialized by matching all 1,281 remote leaf Git blob IDs and modes; local
checkout history was not treated as remote ancestry.

[PR26](https://github.com/c933103/AN-Paint/pull/26) already merged the original
evidence-only package at f68807257ec61c71ac119425d26c109124a18792. All 43 files in
that package remain byte-identical. This change does not recreate, alter, or
relabel those measurements, checker inputs, images or logs.

The original evidence used an isolated, manifest-free harness with source XML
fixtures. This successor compiles in the ordinary app-module JVM suite, uses
AppLanguage.wrap and AAPT-linked resources/assets, adds repeated resize/deadline
controls and observes host accessibility-event requests. The distinction matters:
configuration metadata alone does not prove which resource value was selected.

The three production helpers, exact ClassicPaintActivity caller, filename
validator, picker tags and original LocaleNotificationTest are unchanged from
PR26. Five catalogues and the Nôm font have since changed; all 45 measured
catalogue values still match. See current-input-audit.json. The original coherent
input checker is not weakened to accept this new revision, and its historical
success is not claimed as a current native pass.

## What is authored

Four new JUnit methods are configured for API30 and API35 with NATIVE graphics,
the actual compiled module resources, the real bundled fonts, normal 14sp and an
mdpi/1x bounded viewport. This is eight planned executions, not eight passes.

### C01: compiled resource selection and current routes

VerticalNoticeResizeCharacterizationTest.compiledAppResourcesKeepFiveVerticalProfilesOnSystemToasts

- Select all five current vertical profiles through AppLanguage; attach a
  locale-wrapped test Activity using the app theme.
- Check actual selected locale and compare each of three resolved resources with
  an independently source-derived expected value packaged under test resources.
- Validate the six-U+1F600/five-U+200D .png filename with the real ExportNames
  implementation. Preserve exactly one newline in the combined cursor message.
- Call the actual LocaleTypography.showMessage entry point for both messages.
  Require one system toast with full logical text and no foreground notice.
- Cover all three null-configured-face profiles and both column directions.

This is compiled message-entry-point coverage, not a save callback,
DocumentProvider interaction, physical tap or native-language review. The
existing all-140 picker-route regression is reused rather than duplicated.

### C02: unchanged horizontal node, repeated geometry, original deadline

VerticalNoticeResizeCharacterizationTest.unchangedHorizontalDirectHelperKeepsNodeTextAndDeadlineAcrossRepeatedGeometryChanges

- Call LocaleNotification.show directly for all five profiles, explicitly
  bypassing the production route. Keep its existing horizontal TextView.
- Exercise both fitted and edge-to-edge windows through initial, injected IME,
  restored, 180px shrink, 124px shrink, expansion and repeated identical layout.
- Verify actual rootWindowInsets and independently subtract the Notice's window
  coordinates to check padding. The API30 framework mode adjustment is performed
  after attachment and restored, as in PR26.
- Preserve Notice/TextView identities, full original text/accessibility text,
  POLITE live region, touch pass-through and zero toast replay.
- Set the accessibility-recommended lifetime to 8 seconds; require the same
  notice at original deadline minus 1ms and removal by plus 1ms after repeated
  reflows. Layout must not restart the timer.
- Record full horizontal layout height, final line end and actual native ink.
  Render the complete Layout as an unclipped reference, then draw the live
  TextView through its real Notice parent with only its background omitted.
  Compare exact pixels using the TextView content clip plus child/parent clips.
  Require nonempty reference ink and clear guard boundaries.

The app theme omits the historical isolated Activity's action bar. Both shrink
sizes are named new fixtures; the old 101px/92px result is not asserted as a
universal new dimension. At least one bounded complete-layout no-fit scene is
required. Its occurrence is an expected diagnostic, not a production defect in
today's vertical-profile system-toast routing.

### C03: event-observer controls and content/geometry separation

VerticalNoticeResizeCharacterizationTest.accessibilityObserverSeesControlsAndSeparatesInitialContentFromGeometryEvents

- Cover a bundled Mongolian face/LR profile and default-face Literary Chinese/RL.
- Enable the framework accessibility manager and attach a forwarding
  AccessibilityDelegate to the actual host. Snapshot event type, content-change
  mask, source View identity/tag, event text, current logical text, phase and
  monotonic time before Android recycles the event.
- Require an explicit test-only announcement control with exact source and
  marker payload. Also require a genuine TextView text mutation to produce a
  text-change/content-change event from the same node.
- Record quiet, same-layout, shrink, expansion and same-text-assignment cohorts.
  Assert stable identity/text, no toast replay and no TYPE_ANNOUNCEMENT in the
  geometry/same-text cohorts. Ordinary framework content-change events are
  retained, not suppressed, guessed absent or interpreted as speech.
- Preserve the actual delegate forwarding path and restore accessibility state
  and timeout after the test. An empty or disconnected observer cannot pass its
  positive controls.

The recorder observes host event requests, not delivery to an installed
accessibility service. It does not count TalkBack utterances, certify
exactly-once speech, or distinguish every possible framework speech heuristic.
The explicit announcement appears only in the clearly marked positive-control
phase, never in application code.

### C04: actual clipped pixels with current compiled inputs

VerticalNoticeResizeCharacterizationTest.currentRendererNominalFitIsNotAnInkContainmentOracle

- Use the legal unsupported joined-emoji filename, ordinary mixed emoji/glyph
  filename and joined Mongolian-word filename for all five profiles.
- First verify today's actual entry point still requests a system toast.
- Through a separately labelled direct-helper path, replace the horizontal
  child with a test-only drawing child that uses the unchanged shared renderer.
- Preserve the original probe's independent reference/parent-clip comparison:
  nonempty ink, clear reference guard, exact native pixel equality and exact
  escaped-ink count.
- Require nominally fitting counterexamples to lose actual ink and ordinary/
  joined-word controls to remain contained. Do not turn nominal overhang alone
  into clipping proof or alter production measurement to pass the diagnostic.

The historical raw host TSVs contain all 15 exact portrait/1x/mdpi controls on
both APIs. Unsupported-ZWJ clipped ink is 309/309/336/372/336 for
mn-Mong/mnc-Mong/lzh-Hant/en-XV/qaa-Zsye-XV respectively; all ten ordinary and
joined-word controls have zero clipped ink. Each row reports nominal fit. Their
source hashes and exact row selections are in current-input-audit.json.

| Profile | Unsupported-ZWJ clipped ink | Ordinary filename | Joined-word filename |
| --- | ---: | ---: | ---: |
| mn-Mong | 309 | 0 | 0 |
| mnc-Mong | 309 | 0 | 0 |
| lzh-Hant | 336 | 0 | 0 |
| en-XV | 372 | 0 | 0 |
| qaa-Zsye-XV | 336 | 0 | 0 |

These values match independently selected rows on both
[API30](https://github.com/c933103/AN-Paint/blob/cdbd8a1ed0918d004ba0ef85b35a36be72ec8192/verification/vertical-notices-2026-10-09/data/host-api30.tsv.gz)
and [API35](https://github.com/c933103/AN-Paint/blob/cdbd8a1ed0918d004ba0ef85b35a36be72ec8192/verification/vertical-notices-2026-10-09/data/host-api35.tsv.gz).
This supports all-five-profile qualitative assertions; it is not extrapolated only
from the en-XV screenshot. The current app-theme/AAPT-linked cohort must still
reproduce those qualitative outcomes in CI. Exact historical pixel counts are
not hardcoded as new expected counts.

No vertical route is enabled. No logical text is truncated, no text size is
reduced, and no production node or accessibility policy is changed.

## Source and fixture checks

The six new Python tests check the current resource oracle, corpus, API/scope
boundaries, observer/ink controls, and reject eight deliberate control-removal
mutations. They run under ordinary Python and Python -O. These are structural
checks; they do not compile Kotlin or execute Android.

The existing Android workflow is unchanged. Because this increment adds
Paintroid/src/test source, its usual PR regression/build/device jobs apply.
Reports are already included by the workflow's Paintroid/build/reports upload.

Run the focused Android class through the normal build:

    ./gradlew --no-daemon --max-workers=2 --console=plain -PnativeAbis=x86_64 \
      :Paintroid:testDebugUnitTest \
      --tests org.catrobat.paintroid.local.VerticalNoticeResizeCharacterizationTest

The local bootstrap attempt failed before Kotlin compilation:
java.net.SocketException: Network is unreachable while downloading Gradle 8.13.
There is no local Android pass. The attempt and host-check outcomes are recorded
in local-checks.json; subsequent hosted outcomes must identify their exact head,
tested merge SHA, complete JUnit inventory and artifact hashes.

## Output contract

New output is under Paintroid/build/reports/vertical-notice-resize:

- Eight JSON reports: routes/transitions/events/ink for each API
- Reports include completed=false on an interrupted/failed test, the workflow's
  GITHUB_SHA/GITHUB_RUN_ID when present, exact API, source locale and evidence type
- Each API plans 10 route rows, 80 transition rows, variable event rows with two
  positive-control summaries, and 15 pixel-characterization rows
- Fifty planned PNG files per API: 20 horizontal shrink reference/parent images
  and 30 vertical fixture reference/parent images

A report's existence is not a pass. Require successful exact-head JUnit results,
completed=true, full expected inventories, passing observer controls, complete
images and the unweakened pixel assertions. The reports contain source text from
public project catalogues and synthetic filenames, not user documents.

The generated native reports must be archived as a separately named current
cohort after execution. They must not overwrite PR26's historical package, use
lost/held original bytes, or stand in for the absent new run.

## Decisions deliberately still open

1. One shared measured layout/ink-envelope representation must account for
   fallback shaping, wide clusters, punctuation substitution and transforms.
   Do not copy renderer logic into a production notice helper. API35's
   Layout.computeDrawingBoundingBox alone does not cover API30.
2. Initial no-fit behavior and post-exposure behavior have different announcement
   consequences. Existing system-toast fallback before exposure is a baseline;
   replaying a toast after exposure introduces another announcing surface.
3. After exposure, retaining one logical node and original deadline is a useful
   invariant. Whether to reflow, use an independently fitting horizontal option,
   dismiss early or choose another approved behavior remains unselected.
4. Early dismissal shortens availability. This change neither selects that
   tradeoff nor implements it. Horizontal rendering is not assumed always to fit.
5. No exactly-once TalkBack claim follows from a stable node or event log.
   Installed API30/35 real-IME/resize checks and a separately observed TalkBack
   reading check remain necessary before accepting speech behavior.

Only after the contract and policy are reviewed should a bounded implementation
and corresponding policy regressions proceed. Existing lifecycle, dialog,
all-language route and touch controls must remain, with exact-head review and CI.

## Primary references

- [Historical scope, correction and limits](https://github.com/c933103/AN-Paint/blob/b9a79613b088c9ff54f2c225f6ae53d5b8d8ae61/verification/vertical-notices-2026-10-09/README.md#L32-L112)
- [Original remaining design questions](https://github.com/c933103/AN-Paint/blob/b9a79613b088c9ff54f2c225f6ae53d5b8d8ae61/verification/vertical-notices-2026-10-09/README.md#L142-L148)
- [Unchanged production route](https://github.com/c933103/AN-Paint/blob/b9a79613b088c9ff54f2c225f6ae53d5b8d8ae61/Paintroid/src/main/java/org/catrobat/paintroid/classic/LocaleTypography.kt#L38-L49)
- [Unchanged Notice lifecycle/live region](https://github.com/c933103/AN-Paint/blob/b9a79613b088c9ff54f2c225f6ae53d5b8d8ae61/Paintroid/src/main/java/org/catrobat/paintroid/classic/LocaleNotification.kt#L40-L145)
- [PR26 exact parent-pixel oracle](https://github.com/c933103/AN-Paint/blob/b9a79613b088c9ff54f2c225f6ae53d5b8d8ae61/verification/vertical-notices-2026-10-09/probes/VerticalNoticeHostProbe.kt#L119-L151)
- [PR26 horizontal transition diagnostic](https://github.com/c933103/AN-Paint/blob/b9a79613b088c9ff54f2c225f6ae53d5b8d8ae61/verification/vertical-notices-2026-10-09/probes/NoticeTransitionProbe.kt#L42-L68)
- [AOSP API35 TextView drawing and clipping](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/widget/TextView.java)
- [AOSP API30 TextView drawing and clipping](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r1/core/java/android/widget/TextView.java)
- [Pinned Robolectric event source recording](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowAccessibilityRecord.java)
- [Pinned test using the record shadow with AccessibilityEvent](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/robolectric/src/test/java/org/robolectric/shadows/ShadowAccessibilityRecordTest.java)
- [Pinned accessibility-manager shadow controls](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowAccessibilityManager.java)
- [System toast announcement ownership](https://android.googlesource.com/platform/prebuilts/fullsdk/sources/+/refs/heads/main/android-35/android/widget/ToastPresenter.java#249)
- [Layout.computeDrawingBoundingBox API35 boundary](https://developer.android.com/reference/android/text/Layout#computeDrawingBoundingBox())
