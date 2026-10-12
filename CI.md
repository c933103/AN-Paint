# Android build and test workflow

## Working policy

Keep the application tree focused on code, meaningful tests, compact current
product fixtures, licence inputs and current instructions. Historical raw logs,
images, source inventories and one-time preservation audits belong in CI
artifacts or an immutable evidence ref linked from [the archive index](verification/README.md).
Normal CI does not reconstruct old source snapshots or require inverse adapters.
Current source/test discovery and per-run APK/source binding remain required.

Localization status remains scoped: earlier withdrawn review conclusions are
not restored by this migration. The compact 59-locale wording fixtures preserve
current regression expectations and explicitly retain the 108 open fallbacks;
matching them does not certify fluency or complete linguistic review.

## What runs

- Code push to `develop` or a PR targeting any branch: independent host/JVM/lint,
  universal APK/corresponding source, exact-script generation and API35 jobs.
- Workflow dispatch `device_tests`: `current` (API35), `full` (API30+35), or `none`
  (explicitly not run). Release selects full coverage.
- PR label `ci:full-android` selects API30+35 on its next normal source event.
  `ci:release-android` additionally selects release-configured host/APK/tests.
  Label changes alone do not trigger or cancel a run.
- A develop commit subject starting `Release `, or manual `build_type: release`,
  selects the release variant and API30+35. CI release configuration uses the
  temporary CI key, not the private upgrade key, and does not publish a release.
- Markdown/historical-verification-only changes do not automatically rebuild.

Test APKs compile once after delivery artifacts are available. Device jobs use
those prebuilt binaries through `adb shell am instrument -w -r`, without Gradle
or native-codec rebuilds. SDK-aware source discovery determines the expected
identities and explicit exclusions; never freeze a past test count as a source
oracle. API30 omits SDK-ineligible tests and the explicitly API35 restart pair.
API35 includes ordinary, gallery-draft, dialog, two vertical shards and the
external force-stop seed/verify phases. A missing or excluded test is not a pass.

The exact-script job tests clean debug/release resource merges, release-first,
producer-before-consumer order, identical generated XML, an unchanged up-to-date
run, input-change regeneration and stale-output removal in a disposable worktree.
Only `:Paintroid:bundleCorrespondingSource` is excluded there; the normal build
verifies that native-source/bundling graph. Production translations are not edited.

## Local commands

Run relevant focused tests first, then the current host suite:

```sh
python3 -m unittest discover -s tools -p 'test_*.py' -v
python3 -O -m unittest discover -s tools -p 'test_*.py'
```

Use the repository Gradle wrapper with the installed SDK/toolchain for
`:Paintroid:testDebugUnitTest`, lint and APK compilation. The workflow is the
canonical command/variant source. If Android tools are absent locally, report
compile/native/device stages as unrun and use the exact-source hosted results.
Focused checks do not turn an incomplete aggregate into a pass.

## Deadlines and evidence

- Regression job: 22 minutes; Python contracts: 4 minutes; build job: 45 minutes;
  universal assembly: 30 minutes; emulator jobs: 53 minutes, including a 43-minute execution step.
- SDK install: 5 minutes; device discovery: 60 seconds; boot/service readiness:
  shared 120 seconds, each transient probe at most 10 seconds within that budget.
  Main and each test APK installation: 60 seconds; runner discovery: 15 seconds.
- Native and ordinary app phases: 180 seconds each; gallery-draft: 90 seconds;
  API35 dialog phase: 300 seconds; each vertical shard: 180 seconds; seed and
  verify: 60 seconds each. App ceilings total 630 seconds on API30 and 1,050 seconds on API35.
  Including native gives 810 / 1,230 seconds before setup/collection.
- The current 43-minute step includes separately bounded setup, processing and
  cleanup allowances. Inner deadlines and failure behavior must not be relaxed
  to obtain green results. Test/installation failures are not automatically retried.

The runner retains live raw output, JUnit XML and summaries, including partial
failures. Success requires the final protocol plus every selected identity,
without unexpected, missing, ignored, failed or aborted methods. A zero ADB exit
alone is insufficient. Artifact upload runs even on failure, but cancellation
can leave partial evidence. Keep passed, failed, timed out and unrun distinct.
Actions artifacts expire after 14 days; preserve needed final evidence on a
separate durable ref before expiration. Never include keys, credentials or
unrelated private data.

## How to conclude work

Publish the concrete reviewed change and report the exact asynchronous run.
Continue useful work while it runs. Development delivery requires a built APK,
matching source and correct signature, with pending checks clearly stated.
A verified release requires its complete exact-source gates. Inspect a failure
before retrying; use the affected scope, not a repeated full matrix by default.

## Localized dialog evidence and separate phase

Seven installed dialog method/class pairs run in the `app-dialog` report: four
current notice/credit cases plus three normal-font colour cases. Source discovery
still requires every SDK-eligible app identity, without duplication or omission.
The colour cases replace the old zero-height limitation characterization; its
original failed positive and measured negative results remain historical evidence,
not claims about the repaired source. See [PR51's accepted bounded baseline](https://github.com/c933103/AN-Paint/pull/51).

The dialog 300-second cancellation cap and each 45-second interaction limit stay
unchanged. Seven individual maxima exceed that aggregate cap; fresh actual combined
execution must fit, and a timeout remains a failure. Neither historical timings
nor synthetic transport fixtures prove the combined runtime. Font 2x short-landscape
colour remains diagnostic and unaccepted.

## Historical composed cancellation budgets

Older budgets, timings, raw captures and source-preservation checks are in the
[immutable pre-migration CI history](https://github.com/c933103/AN-Paint/blob/04b128889a4ff9159f199d1737bd07d41e22162d/CI.md).
They do not set current caps. Current workflow and phase-budget tests are authoritative.

## Rendering requirements and diagnostics

Hard requirements include full text and UTF-16 line coverage, no ellipsis,
accessible text, reachable controls/scroll endpoints, and correct natural
same-height status updates. Native capture must use a complete independently
bounded reference, with unsupported drawing state and unsafe allocation rejected.
Keep unmasked exact ARGB/alpha comparisons and genuine native overflow/clipping
controls. A completely missing ink component or opaque stroke sample is a hard
failure; components are not glyph segmentation. Other pixel differences require
explicit review, including partial marks/strokes. A reviewed antialias fringe is
not a universal tolerance, and a diagnostic difference is never labelled exact-pixel pass.
The proportional positive-frame policy currently applies to the M04 JVM captures.
The two installed Arabic helper/decoder profiles retain their exact zero-difference
gate; both passed in the archived04 run. A future installed fringe difference
still needs explicit severity review before adding a production workaround.
Installed software-raster evidence is not a hardware screenshot or network-route proof.

## Locale UI font inventory check

The Nôm asset is a subset for catalogue and picker text, so it has the
`ui_only` role and is excluded from the drawing-font selector.
Default Nôm text still uses its glyph coverage, while an explicit drawing font
keeps the user's selected face. Complete Mongolian remains a drawing choice.
Font regressions compare selectable entries with the inventory's drawing roles
instead of freezing catalogue size. The Android test additionally opens, hashes
and loads every declared asset, including UI-only subsets; hiding a subset from
the selector does not remove its font-load coverage.


AN Paint Nom UI is a renamed subset of Nom Na Tong (MIT) and Gothic Nguyen
(SIL OFL 1.1), distributed under SIL OFL 1.1 with the original MIT notice retained.
AN Paint Wu Fallback is a glyph-only subset of Nom Na Tong under MIT.
Keep actual asset/notice/inventory consistency, bundled cmap coverage, current
glyph metrics and upstream input provenance. Historical binary reconstruction
is an archived one-time check, not a normal CI dependency.

API30–33 font-setting synchronization uses bounded shell work and a private
virtual-display acknowledgement. Under normal FIFO ordering this orders relevant
ATMS messages; a synchronization barrier prevents a portable queue-drain guarantee.
Do not describe it as a universal synchronization proof.

## Cache and corresponding-source rules

Cache downloaded dependencies, pinned native source trees and content-checked
ccache objects only. Compiler identity/content, flags, preprocessed inputs and
strict headers remain checked; direct/depend modes are disabled, sloppiness empty.
Do not restore Java/Kotlin classes, APKs, linked libraries or CMake build output.
Build corresponding source from the same checkout and required pinned native
inputs, retaining licences, font attribution and build scripts. Verify the
embedded source ZIP equals the separately delivered ZIP and matches current source.

## Release publication

The separate publisher consumes `verification/releases/request.json`, its
selected version's public signing patch and release notes. Preserve these
operational inputs during evidence cleanup. Private upgrade signing happens
outside GitHub; never publish the key or private backup. Publication requires
successful exact-develop regression/build/API30/API35 jobs, release manifest,
existing certificate, unchanged non-signature payload, four ABIs, 16KB alignment
and matching embedded source. A normal PR update does not authorize a release.

## Android 5.0 and 7.0 compatibility

`.github/workflows/android-legacy.yml` is manual-only (`workflow_dispatch`).
Choose API21, API24 or both and x86, x86_64 or both. It builds one universal debug
APK and reuses strict SDK-aware native/app inventory checks. SDK-ineligible app
phases are explicitly NOT RUN; no fake empty passing report is produced. This
workflow does not expand ordinary API35/full API30+35 or implicit release gates.
Emulator results do not establish physical ARM-device or vendor-picker coverage.
