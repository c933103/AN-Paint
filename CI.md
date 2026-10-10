# Android build and test workflow

**Localization status reset — 28 September 2026: all previous progress, completion, repair, verification and no-defect conclusions for PRs #2–#9, #12 and #15 are withdrawn. Every item requires a full recheck; no previous progress is accepted.**

See the [individual recheck register](https://github.com/c933103/AN-Paint/blob/review/localization-integration/verification/localization-recheck-register.md). The rejected delivery is additional material to check, not an accepted audit. Historical source, test outputs and evidence classifications remain available as inputs. They carry no current completion credit. Completing the other 81 locales is outside this task.

Updated 23 September 2026. APK production, regression checks and emulator results
are separate outcomes. An emulator must not prevent obtaining an already-built
APK or completing unrelated work.

## What runs

| Trigger / choice | Regression and lint | Universal APK | Emulator coverage |
|---|---|---|---|
| Code push to `develop`, or pull request targeting any branch | Yes, independently | Yes | API 35, all native and app checks |
| Run workflow → `current` | Yes | Yes | API 35 |
| Run workflow → `full` | Yes | Yes | API 30 and 35 in parallel |
| Run workflow → `none` | Yes | Yes | Explicitly not run |
| Markdown / historical verification changes only | Not automatically rerun | Not automatically rebuilt | Not automatically rerun |

Direct pushes to a working branch do not duplicate a PR/default-branch run.
Pull requests targeting another working branch receive the same checks as those
targeting `develop`. Stacked localization PRs therefore do not need temporary
CI-only PRs or retargeting to obtain build and regression results.
New commits cancel obsolete runs for the same branch/PR. Failed emulator matrix
jobs do not cancel the other platform. A failed test remains a failed check;
there is no `continue-on-error` or replacement of failures with green results.

Host translation checks cover every Android catalogue, including English and
resource locales not listed in the picker. They reject equivalent resource
directories, Android quoting errors, altered syntax/licence identifiers,
incorrect GIF limit numbers and format-placeholder mismatches. The scoped
localization batch also has a completeness gate against the current default
catalogue, so adding an English string requires updating that whole batch.
These structural checks do not certify linguistic accuracy; semantic review
remains necessary, especially for minority languages.

The build job uploads `apk-and-source-<commit>` immediately after assembly and
before compiling instrumented-test APKs. Regression/lint runs in a separate job;
neither those results nor emulator completion is a prerequisite for the upload.
The artifact includes the exact corresponding source ZIP, SHA-256 hashes, commit,
run ID, runtime inventory, notices and signing/alignment tools. It uses a temporary
CI debug key; the existing private signing step supplies an upgradeable delivery.
Artifact availability is not a claim that all tests passed.

Test APKs are compiled once, after the delivery artifact is available. Emulator
jobs download those binaries and run `adb shell am instrument -w -r` directly;
they do not invoke Gradle or rebuild native codecs. Full runs use independent
API 30 and 35 jobs. API 30 excludes Ultra HDR (no gain-map API) and the two explicitly API35-only
accepted-credit restart phase classes. API35 runs all declared methods: its
ordinary app invocation excludes the restart pair, which run separately before
and after an external force-stop. Their exact disjoint union is checked against
the full source inventory; an exclusion is never treated as a passed test.

Dependencies and pinned native source trees are cached. Starting with local.20,
the build job also uses ccache 4.5.1-1 from Ubuntu 22.04's archive, through CMake's
C/C++ compiler-launcher environment variables. Its separate 2 GB cache lives
outside the checkout and hashes the NDK/CMake configuration, pinned-source
fetch scripts and native source files. The root app-version declaration is not
part of that key. Native-source changes can restore the previous compatible
cache, after which ccache checks the compiler binary content, flags and
preprocessed source for each compilation. Direct and depend modes are disabled,
and no sloppiness checks are relaxed. Java/Kotlin classes, APKs, linked libraries
and CMake output directories still rebuild from the current checkout.

Cache statistics are printed after assembly. On 12 September 2026, the initial
[local.20 build](https://github.com/c933103/AN-Paint/actions/runs/34705339120)
took 17m1s for universal assembly. The final
[source-clean build](https://github.com/c933103/AN-Paint/actions/runs/34706970961)
took 3m54s, with 2,666 hits from 3,058 cacheable compiler calls (87.18%). These
are observed run timings, not a controlled benchmark or a guarantee for future
changes. Direct mode stayed disabled; these were preprocessed cache hits.
Regression and emulator jobs do not depend on this cache. References: the official
[CMake 3.22 launcher documentation](https://cmake.org/cmake/help/v3.22/envvar/CMAKE_LANG_COMPILER_LAUNCHER.html),
[ccache 4.5.1 manual](https://ccache.dev/manual/4.5.1.html), and
[Ubuntu Jammy package record](https://launchpad.net/ubuntu/jammy/+package/ccache).

Local.22 adds a fallback restore prefix for the same OS and ccache version when
adding TIFF changes the integration-script namespace. Restoring that cache does
not accept an object without ccache's existing compiler-content, command and
preprocessed-input checks. Strict header checking, disabled direct/depend modes,
empty sloppiness and rebuilding linked libraries/APKs remain unchanged. This
allows unchanged codecs to reuse their valid objects while the new codec builds.

## Deadlines and evidence

- Regression job: 20 minutes; build job: 35 minutes; each emulator job: 25 minutes.
- Emulator SDK installation: 5-minute command deadline; device discovery:
  60 seconds; boot and Android service readiness share 120 seconds; main APK
  installation: 60 seconds. Readiness probes have a maximum 10-second attempt
  inside that shared deadline, with progress and failure logs. They may retry
  transient startup failures; APK installation and app tests are not retried.
- Each test APK installation: 60 seconds; runner discovery: 15 seconds. Each
  ordinary native/app instrumentation invocation: 180 seconds; each of the two
  vertical locale invocations: 180 seconds (360 seconds aggregate vertical
  instrumentation allowance, increased from 180); each accepted-credit
  seed/verify invocation: 60 seconds. The existing whole emulator execution step
  remains capped at 15 minutes. Inner command budgets are ceilings, not a promise
  that every ceiling can be exhausted in one step. The new phase durations need
  exact-head API35 measurement; deadline exhaustion fails rather than relaxing
  a timeout or substituting a weaker restart test.
- Emulator shutdown and log collection are bounded. Failure reports upload with
  `always()` even if a test step fails; forced job cancellation may leave partial
  evidence, which must not be described as a pass.

`tools/run_android_instrumentation.py` streams raw output into the live Actions
log, saves partial output, and writes JUnit XML plus `summary.json`. Success requires
the runner's final result, successful results for every declared method, and no
missing, unexpected, ignored, failed or aborted tests. An `adb` exit code of zero
alone is insufficient. No automatic retry hides a failure or doubles a long run.
Reports are separate artifacts: `regression-and-lint-<commit>` and
`emulator-api-<api>-<commit>`. They are retained for 14 days; archive final release
evidence during private packaging rather than depending on temporary artifacts.

The old private `package18.py` describes the historical local.18 artifact layout
and requires all its recorded results. Future packaging must collect the new
separate artifacts and report the selected matrix, pending checks and failures
explicitly. Do not manufacture missing reports to satisfy the old helper.

## How to conclude work

Continue useful implementation while asynchronous checks run. A task can conclude
with source published and a development build delivered after its build, source
and signature checks, while clearly stating which runtime checks are pending.
Do not wait through every device run simply to end a turn. A fully verified release
still requires the relevant completed checks; a runtime defect remains work to
fix even when the APK has already been made available.

For failure investigation, inspect the failing job and retained logs first.
Run the affected class/method locally or through the direct-ADB runner when an
Android runtime is available. Repeat the complete matrix only for a release or
when a diagnosed risk spans both supported test platforms.

## The local.18 delay and correction

The prior workflow put everything in one 80-minute job: host checks, API 30,
API 35, then a universal rebuild and finally artifact upload. Its concurrency key
included the commit SHA and disabled cancellation, leaving superseded runs active.

The final successful local.18 run lasted 40m44s; its emulator step took about
20m23s. Earlier failed iterations extended the work across multiple runs. These
timings do not excuse using that chain as a blocker for other tasks.

The app tests also incurred eight unnecessary 45-second waits per platform.
After moving the app to `CREATED` to await autosave, AndroidX Test Core 1.6.1's
`close()` restarted its already-visible helper activity and waited for another
resume notification. API 30's app suite increased from 39.849s to 399.623s.
Teardown now preserves the autosave wait, finishes the stopped activity normally,
waits for destruction, and then closes the scenario's observer. Production app
code and functional test assertions are unchanged. The local.19 API 35 run
confirmed the correction: all eight editor tests finished in 37.24 seconds,
compared with the prior 399.623-second API 30 run. These are different platform
runs, so the timing comparison is not a controlled benchmark.

Sources: [the completed local.18 run](https://github.com/c933103/AN-Paint/actions/runs/34692671218),
[AndroidX helper implementation](https://github.com/android/android-test/blob/axt_06_26_2024/core/java/androidx/test/core/app/InstrumentationActivityInvoker.java),
[Android command-line testing](https://developer.android.com/studio/test/command-line),
[GitHub artifact sharing](https://docs.github.com/en/actions/tutorials/store-and-share-data),
[GitHub workflow syntax](https://docs.github.com/actions/reference/workflow-syntax-for-github-actions).

## First independent emulator startup correction

The first split run built the APK and passed regression/lint, but its API 35
emulator stopped before installing the app. The emulator log reports boot in
38.220 seconds. Logcat then reports no focused setup/launcher window and a
launcher input-dispatch ANR; the 10-second synthetic MENU-key command is the
strongly indicated failure point from that timing. The old script did not label
each command, so the exact timed-out command cannot be established from its
Actions log alone.

Startup now dismisses keyguard through WindowManager instead of injecting MENU.
Boot, package-manager availability, animation settings and keyguard dismissal
share one 120-second readiness budget. Short transient command failures retry
within that same budget; all phases and probe results are saved in `startup.log`.
The 15-minute emulator step limit and independent artifact delivery remain
unchanged. Host checks cover transient failure, deadline enforcement, premature
boot-property values, package readiness and emulator death.

The [local.19 API 35 run](https://github.com/c933103/AN-Paint/actions/runs/34702846656)
passed: all 35 native/import tests finished in 64.154 seconds and all eight editor
tests in 37.24 seconds. The emulator script reached successful completion at
166 seconds, including startup and installations; log collection and shutdown
followed. This establishes emulator verification of the startup and teardown
corrections. It does not stand in for physical-device verification. Local.20
uses the new app test component `paint.anpaint.android.test`; the library test
component remains `org.catrobat.paintroid.test`.

## Release builds and GitHub publication (0.0.28)

A `develop` code commit whose subject starts with `Release ` selects the release
variant and the full API 30/35 matrix. Alternatively choose `build_type: release`
when manually running the workflow. Release always overrides `device_tests: none`.
Other code pushes and PRs retain the debug/API 35 defaults. Both release host
regressions/lint and instrumentation compile against the release variant.
The shipped manifest is not debuggable. Code shrinking is disabled in both
modules, so the tested Java/Kotlin code is preserved. Native release compilation
uses its release optimization settings. Kvazaar explicitly requests GNU C11 for
its x86 inline assembly; strict C11 inherited from AOM did not compile it.
Dependency notices use the selected variant's actual runtime dependencies.

GitHub release publication is a separate workflow triggered by a reviewed
`verification/releases/request.json` commit, after private upgrade signing.
The private signing key remains outside GitHub. A small public APK patch contains
ZIP headers, alignment and signatures plus copy ranges for the unchanged CI
payload; it contains no signing key. The publisher requires the declared original
APK hash, final signed APK hash, unchanged non-signature ZIP contents, matching
embedded source, four ABIs, 16 KB alignment, the existing certificate, release
manifest and successful regression/build/API 30/API 35 jobs for that exact commit.
It then uploads APK, corresponding source, checksums and verification evidence to
a draft release, and publishes it. This uses the repository-scoped Actions token
with contents-write and actions-read permissions; routine build jobs remain read-only.
See [GitHub token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
and [release API](https://docs.github.com/en/rest/releases/releases#create-a-release).

The first universal release attempt passed regression/lint but failed to compile
libheif's C++ file streams on 32-bit API 21. AOM's CMake flag helper uses
`CACHE ... FORCE`, adding `_FILE_OFFSET_BITS=64` to shared release flags. Those
stdio aliases need API 24 on 32-bit Android. The libheif target now explicitly
undefines that inherited macro on 32-bit API levels below 24; its bounded in-memory
image import/export API remains unchanged. The targeted compile check covers both
armeabi-v7a and x86. The original native source trees remain unchanged.


## Node 24 action migration and test compilation (0.0.33)

Run [35001403001](https://github.com/c933103/AN-Paint/actions/runs/35001403001)
built the APK and passed the API 35 emulator job. Its regression job stopped at
`compileDebugUnitTestKotlin`: the new test helper traversed an object inferred as
both `ViewParent` and `View`, making their inherited `parent` properties ambiguous.
The helper now traverses explicitly typed nullable `View` references. This keeps
the group-opening and visible-command assertions intact; no test is skipped.
The regression suite did not execute in that run.

Both workflows pin Node 24 action releases by full commit SHA:

| Action | Release | Pinned commit |
|---|---|---|
| checkout | [v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1) | `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| cache | [v6.1.0](https://github.com/actions/cache/releases/tag/v6.1.0) | `55cc8345863c7cc4c66a329aec7e433d2d1c52a9` |
| upload-artifact | [v7.0.1](https://github.com/actions/upload-artifact/releases/tag/v7.0.1) | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` |
| download-artifact | [v8.0.1](https://github.com/actions/download-artifact/releases/tag/v8.0.1) | `3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c` |

Their pinned action manifests declare `node24`. The observed hosted runner is
2.337.0, above the 2.327.1 minimum for Node 24. Uploads explicitly retain ZIP
archives; named downloads still extract into the existing paths. Download v8
rejects digest mismatches by default. Existing permissions, cache paths, source
checks, deadlines and test matrix remain in effect. No insecure Node opt-out or
unsafe fork-checkout option is enabled. See GitHub's
[Node 20 migration notice](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/).

## Locale UI font inventory check (24 September 2026)

The repaired [PR #12 run](https://github.com/c933103/AN-Paint/actions/runs/35934972156)
and [integrated run](https://github.com/c933103/AN-Paint/actions/runs/35935361997)
passed APK/test-APK compilation, regression tests and lint. Both API 35 runs
completed all 71 native checks and all 11 editor checks; their sole failure was
`NativeCodecTest.everyAdvertisedBundledFontLoadsItsActualFontFile`, which expected
20 drawing font choices but found 21 after the Nôm UI subset was added.

The Nôm asset is a subset for catalogue and picker text, so it has the
`ui_only` role and is excluded from the drawing-font selector.
Default Nôm text still uses its glyph coverage, while an explicit drawing font
keeps the user's selected face. Complete Mongolian remains a drawing choice.
Font regressions compare selectable entries with the inventory's drawing roles
instead of freezing catalogue size. The Android test additionally opens, hashes
and loads every declared asset, including UI-only subsets; hiding a subset from
the selector does not remove its font-load coverage.

The subsequent [PR #12 run](https://github.com/c933103/AN-Paint/actions/runs/35937278241)
at `29ef7eab4587071c59a2d013cd7e88112decd674` and
[integrated run](https://github.com/c933103/AN-Paint/actions/runs/35937264365)
at `ee6d2d5e258d9424f8987bb14b11517953019843` passed the full workflow.
The integrated run reports 307 unit tests, lint, production/test APK compilation,
all 71 native tests and all 11 editor device tests passing. This verifies the
font-role and gallery-credit recreation repairs in that snapshot; later changes
still require their own exact-head checks.

## Literal percent checks in translated resources

The final Ainu completion introduced literal percent signs into translated
instructions. Strict AAPT2 compilation caught two errors that the old host
placeholder comparison missed. Static text now explicitly uses
`formatted="false"`; strings with runtime arguments escape literal percent
signs as `%%`. The validator applies these checks to every string, plural and
string-array, including unoffered locales. Disabling AAPT format checking does
not bypass the check for an unescaped percent mixed with runtime arguments.
`%%` consumes no argument, so it is excluded from placeholder-count comparisons;
a translation may use the sign where English spells out “percent”.

## API35 accepted-credit abrupt-process-stop regression

This is one regression split into two one-method app instrumentation classes.
After the ordinary editor suite passes, the host starts the ordinary launcher and
records its live PID. The seed-only `--leave-target-running` wrapper option is
restricted to the seed class and emits both `am instrument --no-restart` and
`-e waitForActivitiesToComplete false`. Normal invocations, protocol parsing,
APK installation, missing/ignored/aborted-test rejection and final-result checks
retain their original behavior.

The seed uses the established synthetic insertion fixture, then removes its
monitor before opening the actual Gallery from the editor. Both synthetic Gallery
insertion monitors echo the exact opaque session token supplied by their launch;
this keeps the existing editor fixtures compatible with result-ownership checks. Real Save accepts
large mixed Unicode credit text while the parent remains stopped with the known
original drawing and ledger already autosaved. Read-only ZIP/JSON assertions
prove the accepted session and retained snapshot are durable and that the original
drawing was not updated. No accepted archive/session API manufactures acceptance.
The method deliberately leaves Gallery and its credit dialog open.

Only a complete successful seed report allows the host boundary to proceed. The
host verifies the original PID still exists and Gallery remains resumed, rechecks
the PID immediately before a bounded external force-stop, then positively checks
absence with a protocol that distinguishes `pidof` absence from ADB failure. The
bootstrap is bounded to 30 seconds; PID, activity-evidence and force-stop commands
to 10 seconds each. There is no test retry, data clear, main-APK reinstall or
orderly Gallery dismissal between acceptance and force-stop.

The ordinary verify runner starts a new process. Before launching the editor it
compares the seed's process identity and exact on-disk digests. It then checks the
original drawing and ledger, reaches the archive through the actual Save dialog,
reconstructs all visible credit pages, and confirms browsing leaves association
unchanged. Production New creates a different blank drawing with no credits.
Only choosing Add for the exact accepted record attaches that source and text;
the new drawing's pixels stay unchanged.

Reports remain under the existing API-specific artifact root:
`app/accepted-credit-restart/seed`, `verify`, `boundary.log`, `verify-status.txt`
and `coverage.json`. Coverage success requires the ordinary, seed and verify
reports to contain mutually disjoint completed identities whose union equals all
app methods declared in source, including future ordinary classes. A failed seed
or host boundary prevents verification and records it as not run. API30 explicitly
omits both phase classes and records that this API35 flow was not run.

Local Python/fake-ADB checks establish command ordering, complete-result gating,
PID/deadline/error propagation and inventory accounting only. They do not establish
Android compilation or runtime success. The exact-head API35 emulator must first
prove complete seed success with the same live PID and undelivered Gallery result;
if that gate fails, diagnose it without claiming Activity recreation or an
already-dead-process force-stop is equivalent. No workflow YAML, dependency,
release matrix or outer deadline is changed.


## SDK-aware instrumentation inventory (0.0.38 release verification)

The source inventory now queries the connected device SDK and applies literal
`@SdkSuppress` minimum/maximum bounds before comparing every eligible method
with AndroidJUnitRunner's completed methods. A method annotation overrides the
class annotation, matching AndroidX. The report records the device SDK and every
SDK-ineligible method separately; those methods are not counted as test passes.
Unknown or malformed SDK annotation syntax fails closed. Existing explicit
class exclusions, skipped-test rejection and restart-phase completeness checks
remain in force.

The first release run 38013637833 passed build, 737 regression tests, lint and
94 API35 tests. API30 completed 90 successful tests but correctly failed the old
inventory check: it expected the API33-only device-language picker method. The
method's `@SdkSuppress(minSdkVersion=33)` was already present, and the method ran
and passed on API35. That run remains failed; a new exact-source full release
run is required after this inventory correction. No test or SDK annotation was
removed or relaxed.

AndroidX precedence and bounds:
https://developer.android.com/reference/androidx/test/filters/SdkSuppress


## Current-base installed four-locale matrix (PR18 continuation)

The historical PR18 test class was intentionally excluded from the later PR19
reconciliation. Its ancestry and old API35 run do not prove coverage in accepted
develop. This continuation adapts those four installed native-input tests to the
current startup, locale picker and autosave behavior; it changes no production UI.

The class covers `mnc-Mong`, `lzh-Hant`, `en-XV` and `qaa-Zsye-XV`, each in portrait
and landscape. Picker viewport positioning is fixture setup; the exact row is
selected through native accessibility input and its real callback is observed.
The tests follow replacement activities, wait for `startupReady`, preserve two
sentinel pixels, select all five tabs, use native overflow swipes and select Line
before Arrow. Arrow input waits for the real scheduled autosave generation to
finish rather than suppressing autosave or retrying a missed tap. Save checks
include initial LR/RL column position, native JPEG popup selection, filename,
quality reachability, no lossless control, Cancel/reopen with PNG and native Back.
No external save/share destination may be launched. Prior orientation and locale
are restored; monitors/listeners are removed at teardown.

The current direct-ADB runner remains the implementation for every invocation.
The ordinary app suite excludes the vertical class and both accepted-credit
restart classes. Two explicit vertical invocations select these original methods:

- `app-vertical-english-manchu`: vertical English and Manchu
- `app-vertical-literary-chinese-emoji`: Literary Chinese and vertical emoji

Each invocation uses repeatable `--include-test CLASS#METHOD` selectors and keeps
its 180-second instrumentation ceiling. This provisions 360 seconds of aggregate
vertical instrumentation allowance, increased from the original 180 seconds.
It also adds a separate test-APK installation and SDK/runner discovery. This is
coverage provisioning, not an optimization or a claim that the old deadline was
met. Both shards execute once even if the first fails; aggregate failure is
retained. The accepted-credit seed and verify retain their separate 60-second
deadlines, live-PID checks, undelivered Gallery state and external force-stop.
The whole emulator execution step remains capped at 15 minutes, independently of
the inner ceilings. The ceilings do not promise that all phases can exhaust their
budgets in that outer window. No test is retried and no failed step is ignored.

`tools/vertical_locale_matrix.py` verifies the exact disjoint SDK-specific union
of ordinary, both vertical shards, seed and verify reports on API35. On API30 it
verifies ordinary plus both vertical shards and records both restart methods as
explicitly excluded, never passed. AndroidX SDK-suppressed methods remain separate
from these explicit class omissions. Every selected method must complete
successfully exactly once. A missing, duplicated, swapped, unexpected or obsolete
monolithic shard report fails. Every report must record the exact selected methods,
unchanged invocation ceiling, and a SHA-256 binding of all Kotlin test-source
relative paths and bytes. The binding identifies the checked-out test inputs; APK
provenance continues to come from the workflow's exact-source build and artifacts.
A source mismatch, timeout, error, skip, missing/non-integer/mismatched device SDK
or incomplete report fails the gate, regardless of a reported success flag. Each
phase must capture the SDK selected for the run before source eligibility is
computed, preserving minimum/maximum SDK bounds. Unknown, duplicate, malformed,
class-conflicting or SDK-ineligible method requests fail before installation or
instrumentation; none can be silently omitted. The full receipt is
`app/coverage.json`; API35 also retains the accepted-credit coverage path. Old
union receipts are removed before verification so failure cannot retain a stale
success receipt.

Fresh matrix screenshots and summaries are cleared once before both invocations.
The shared device screenshot directory is not cleared between the two shards. Bounded
EXIT cleanup pulls screenshots before emulator shutdown, including after failure
or timeout. A successful run requires exactly 32 PNGs: four locales × two
orientations × workspace / initial Save / format popup / JPEG quality. The host
receipt records filename, dimensions, size and SHA-256 after checking PNG headers
and rejecting exact duplicate content across required states. Popup capture waits
for stable native-window geometry, a committed render frame and two subsequent
frame callbacks, and rejects a byte-identical repeat of the closed Save frame.
Missing collection or inventory makes an otherwise successful job fail. This is
an inventory/integrity check, not visual review; inspect all 32 rendered images
before concluding the installed matrix is verified.

Reports are under `app-vertical/english-manchu/androidTest-results` and
`app-vertical/literary-chinese-emoji/androidTest-results`, screenshots under
`app/vertical-locale-evidence`, and the screenshot receipt is
`vertical-locale-screenshots.json`, inside the existing API-specific artifact.
Host/fake-ADB checks establish selection, accounting, cleanup and failure behavior
only. Fresh exact-head compilation, API35 XML/logs, measured phase durations and
visual screenshot review are required. Use the full API30/API35 matrix for release
verification or a diagnosed cross-version risk; no new full-matrix default or
workflow transplant is introduced here.

## Draft control-reachability follow-up to PR18

This additive test proposal starts at exact head
`66c39ca345ef7bc8c5fe1da8ce64cb872c3a0e88`, tree
`a90cdf84be34e6a08ab7a9d25b46cdce2f71b776`. The prior 98 installed passes and
32 capture-state images remain evidence of that source only. They do not prove
these new checks passed. The accepted evidence and the unresolved checklist at
[PR18 comment 6093775811](https://github.com/c933103/AN-Paint/pull/18#issuecomment-6093775811)
remain unchanged.

`VerticalControlReachabilityProbe` adds assertions inside each existing locale /
orientation case. The original phase inventory, all previous assertions, original
32-image collector, 180-second vertical phase deadline and 15-minute enclosing
execution limit remain intact. There is no new phase or workflow change.

The probe first records the currently clipped viewport, then uses native swipes
to reveal the complete quality widget, readout, native SeekBar and thumb. It drags
the actual thumb to quality 1 and 100, requiring each input to change the previous
value and checking both native progress and displayed value. It separately reveals
the complete filename field/preview, JPEG explanation and Cancel action. Geometry
receipts contain raw / ancestor-clipped screen bounds and ancestor scroll offsets.
Reveal gestures match the missing edge plus native touch slop instead of relying
on a fixed long swipe that could overshoot a reachable control. No progress setter,
scroll setter, callback replacement or programmatic click establishes success.

After the original Cancel/reopen/Back and no-external-request assertions, a distinct
native Save flow selects JPEG again and uses Choose location. The existing
ActivityMonitor intercepts exactly one ACTION_CREATE_DOCUMENT request and returns
RESULT_CANCELED before opening a provider. Its MIME, filename and persisted quality
must match. Portrait commits quality 1 and landscape commits 100. No external
storage destination, grant, encoding, real file write or sharing is exercised.
Cancel must not persist the changed draft quality. Draft filename, document
filename, every canvas pixel and selected tool are checked for preservation.

`app/vertical-locale-evidence/reachability/` holds eight case receipts and 64 fresh
PNG captures: before, minimum, maximum, filename, description, cancel-ready,
choose-ready and returned. These cannot replace the original top-level 32 states.
EXIT collection still runs before emulator shutdown and failure stays failed.
The new independent receipt checker rejects missing / extra files, failed or
partial cases, clipped endpoint/thumb/readout bounds, unchanged endpoint input,
wrong values, filename/state loss, missing native scroll movement and byte-identical
minimum/maximum captures. Header, inventory and state receipts do not certify
rendered pixels: reviewers must open every actual image after an installed run.

The candidate is a probe, not a production repair or broad usability acceptance.
A failure needs diagnosis: distinguish a real inaccessible control from a bad
coordinate / native-scroll oracle or a phase-budget failure. Preserve the failing
exact-source evidence. Do not weaken full-bound assertions or extend timeouts to
turn a failure green. Run current-platform API35 only after reviewed publication;
API30/full matrix remains for release verification or diagnosed cross-version risk.

### Reviewed probe-oracle corrections

The first unpublished proposal could finish the landscape Cancel draft at the
same endpoint remembered from portrait. Revision 2 ensures a different value
using another native endpoint gesture when needed, records both remembered and
draft values, asserts the distinction immediately before Cancel, and rejects an
equal-value receipt. Both endpoint screenshots remain required.

Revision 2 also hardens both test-only geometry helpers: a false
`getGlobalVisibleRect` result returns a fresh empty Rect, because Android leaves
its output undefined on false. Each helper has an installed negative fixture that
writes a nonempty rectangle and returns false; a regression of the guard must fail
that fixture. Host checks validate the source/fixture contracts but do not execute
Android/Kotlin. The actual installed negatives remain unexecuted until reviewed CI.

This changes one pre-existing visibility-return line, so "every original line
unchanged" is no longer an exact claim. Existing assertions and their thresholds,
production source, workflow and deadlines are preserved. No prior screenshot is
overwritten or retroactively revalidated by this test-oracle correction.


### Explicit vertical workload provisioning (10 October 2026)

[API35 run 38031416670](https://github.com/c933103/AN-Paint/actions/runs/38031416670)
at PR41 head `f22ff7a206b6e871e54fec4b0e02ae32f7cc4700`, tree
`d21df4db395b12aeac71600d73394323fa040d51`, failed the original single
vertical invocation at 180.636 seconds. English, Manchu and emoji completed;
Literary Chinese began but was terminated during initial portrait navigation.
The original failed run and incomplete evidence remain failed. Splitting future
coverage cannot retroactively pass that run or establish fresh installed timing.

This test-only scheduling change preserves all four original Kotlin methods,
native gestures, stationary anti-fling tails, assertions, screenshot frame waits
and both orientation paths byte-for-byte. The original 32 screenshots plus all
64 reachability images and eight receipts remain mandatory, collected once by
the existing bounded EXIT cleanup. No production/redraw code, evidence pixels,
workflow YAML, ordinary/restart test boundary or outer deadline changes here.
The independent rendered-text defect and its production repair require separate
review; the extra vertical budget cannot repair or certify those pixels.

Host/fake-ADB checks cover strict selection and SDK exclusions, source binding,
exact disjoint report union, timeout/failure propagation, one execution per shard,
one shared cleanup and preservation of existing boundaries. These checks do not
compile Android/Kotlin, measure real two-shard device timing or certify images.
Fresh reviewed exact-source API35 compilation, installed reports, all original
image/receipt inventories and visual review are still required.
