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

A PR with the `ci:full-android` label uses the existing API 30/35 matrix on its
next normal opened/synchronized/reopened run. Apply the label before publishing
the code update that needs cross-version coverage, then verify the run's actual
matrix. Applying/removing the label alone does not trigger or cancel a workflow.
This opt-in is for a diagnosed cross-version risk, not the default for routine
edits. It adds no new test runner and does not waive ordinary test inventory,
timeouts, artifact provenance or release requirements.

For premerge release-variant verification, the `ci:release-android` PR label
selects release host checks, APKs, instrumentation and the API 30/35 matrix on
the next normal opened/synchronized/reopened run. This label includes full
coverage; `ci:full-android` alone retains the debug variant. Verify the label
before publishing the reviewed source update, then inspect both actual emulator
jobs and `build-info.json`'s `build_variant` for that exact source. A label change
alone does not start a run, and rerunning an earlier debug run is not release
verification. The existing `-PciReleaseSigning` path uses the temporary CI debug
key for these release-configured APKs; it does not access the private upgrade key
or publish a release. No credentials, security settings or release-publication
triggers are changed by this opt-in.

The independent **Exact-script resource generation** job runs the pinned Gradle
8.13/AGP 8.13 toolchain in a disposable exact-HEAD worktree. It verifies clean
debug/release resource merges (including release-first after another clean),
generation before each direct resource consumer, byte-identical XML output,
an unchanged up-to-date run, an input-change rerun, and stale-output removal.
Its only excluded task is `:Paintroid:bundleCorrespondingSource`, whose native
source download/bundling graph is tested by the ordinary build. No resource
producer/consumer is excluded. The harmless temporary XML comment and stale
output fixture never change the checkout or the published translations.
Logs, task outcomes, input/output hashes and a strict success summary are in
`exact-script-generation-<commit>`. A missing or failed report is not a pass.

`EditorDeviceTest.mixedScriptKoreanUsesItsCatalogueAcrossRealPickerSwitchesAndRotation`
uses the installed app's visible picker for mixed-script Korean → ordinary
Korean → mixed-script Korean. It checks fixed Save/Copy-credit text, public
preference/platform/Java locale identity and the private configured resource
tag before and after a real orientation/dimension change. Per-phase JSON is
logged under `ExactScriptResourceTest` in the retained emulator logcat. This is
complementary to API30/API35 native-resource JVM tests, not linguistic acceptance.

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
ordinary app invocation excludes the three gallery-draft methods, four vertical
methods and the restart pair. The unchanged gallery-draft class runs separately
with a 90-second ceiling; the vertical methods run in two 180-second shards. The
restart pair runs separately before and after an external force-stop. The
exact disjoint union is checked against the full SDK-aware source inventory on
both APIs; an exclusion is never treated as a passed test.

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
Cache misses do not bypass compilation; emulator jobs do not use this cache. References: the official
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

- Regression job: 22 minutes; Python contracts: 4 minutes; build job: 35 minutes;
  each emulator job: 46 minutes, including a 36-minute execution step.
  These are hard cancellation ceilings, not target runtimes.
- Emulator SDK installation: 5-minute command deadline; device discovery:
  60 seconds; boot and Android service readiness share 120 seconds; main APK
  installation: 60 seconds. Readiness probes have a maximum 10-second attempt
  inside that shared deadline, with progress and failure logs. They may retry
  transient startup failures; APK installation and app tests are not retried.
- Each test APK installation: 60 seconds; runner discovery: 15 seconds. Each
  native and ordinary-app instrumentation: 180 seconds each; gallery-draft:
  90 seconds; each of two vertical shards: 180 seconds; accepted-credit seed
  and verify: 60 seconds each. App-only ceilings sum to 630 seconds on API30
  and 750 seconds on API35. Including native instrumentation gives 810 / 930
  seconds, before installation, discovery, startup, boundary and collection.
  The original composed head retained a 900-second outer step, which was
  structurally insufficient. The corrected 36-minute step admits the existing
  controlled subprocess paths plus explicit processing/cleanup allowances; the
  detailed source-bound model is below. Exact-head combined API30/API35 runtime
  remains required. Deadline exhaustion fails without relaxing an inner timeout
  or substituting a weaker restart test.
- Emulator shutdown and log-collection ADB commands have individual deadlines.
  Local parsing/file I/O have only the outer step/job cancellation authority; no
  universal subprocess or filesystem liveness guarantee is claimed. Failure reports upload with
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
Other code pushes and unlabeled PRs retain the debug/API 35 defaults; `ci:full-android`
PRs use debug/API 30+35, and `ci:release-android` PRs use release/API 30+35 as
described above. Both release host regressions/lint and instrumentation compile
against the release variant.
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
and `coverage.json`. Coverage success requires the ordinary, gallery-draft, both vertical shards, seed and verify
reports to contain mutually disjoint completed identities whose union equals all
SDK-eligible app methods declared in source, including future ordinary classes.
The full union is written to `app/ordinary-gallery-coverage.json` and the existing
API35 restart coverage location only after every required phase passes. Both
receipts describe the complete composed app union, not only the restart pair. A failed seed
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

## API30 font write-back synchronization and bounded lint preparation

Release verification run [38018126008](https://github.com/c933103/AN-Paint/actions/runs/38018126008)
at `80c14372b0504bc44f9f2809ad477247fdc8100b` passed APK/test-APK building and
API35. API30 reached the correct SDK-aware test inventory, but the gallery
viewport fixture failed its second 1.0-to-2.0 system font transition. Its log
shows setting, system resources and target resources briefly agreeing on 1.0;
the following request for 2.0 finished its original 10-second deadline with all
three still at 1.0. This is consistent with the pending ATMS configuration
snapshot overwriting the subsequent setting write. It does not establish a
production gallery layout defect.

On API30-33, the fixture now follows three-way agreement with a unique
DisplayManager display-added/removal acknowledgment. In the inspected AOSP API30 source,
ATMS's persistence message and DisplayManager's display-event messages use
DisplayThread. The fixture registers a listener, creates a temporary private
1-by-1 own-content-only virtual display without a Surface, waits for that exact
ID's added callback, releases it, then requires its removed callback. Under normal
FIFO delivery with no intervening synchronization barrier, the second acknowledgment
also covers a snapshot posted while the earlier configuration message was still
running. DMS messages are asynchronous; ATMS messages are ordinary. A MessageQueue
synchronization barrier can therefore let both DMS acknowledgments bypass an older
ATMS persistence message. This is not a portable queue-drain guarantee. The host
model includes that counterexample, and a callback alone never replaces the real
font/layout assertions or exact-device verification. Display/listener cleanup
remains in `finally`. No content is captured, mirrored, presented or drawn on the
temporary display. The API34+ shell flush remains.
All waits share the original 10-second transition deadline, including the legacy
shell output read. Both real 1.0-to-2.0 transitions, the actual setting/system/app
checks, and every installed gallery/font/viewport oracle remain required.
The queue model is host-only ordering evidence; exact-head Android compilation
and API30 runtime verification are still required before calling this repaired.

Source references for the API30 ordering (Android 11.0.0_r27):
- [AMS supplies DisplayThread to ATMS](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r27/services/core/java/com/android/server/am/ActivityManagerService.java#L2651-L2653)
- [ATMS queues configuration persistence](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r27/services/core/java/com/android/server/wm/ActivityTaskManagerService.java#L5153-L5294)
- [DisplayManager uses DisplayThread](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r27/services/core/java/com/android/server/display/DisplayManagerService.java#L334)
- [Display creation queues the added event](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r27/services/core/java/com/android/server/display/DisplayManagerService.java#L804-L825)
- [Display event queue and delivery](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r27/services/core/java/com/android/server/display/DisplayManagerService.java#L1632-L1669)
- [Public virtual display API and flags](https://developer.android.com/reference/android/hardware/display/DisplayManager)

The same run's regression job completed Python and JVM checks; JVM elapsed time
was 518.454 seconds. Its six-minute combined native/lint step built the native
libraries, entered lint analysis, then stopped without a completed lint result.
Native preparation and lint now have separate required six-minute steps and
separate logs/profiles. Lint still runs the complete original task with no task
exclusions. The checks job reuses the build job's pinned ccache and identical
content-checking configuration to avoid redundant native compilation. Cached
classes, linked libraries, APKs and CMake directories remain forbidden; cache
misses compile normally. The outer 20-minute regression-job limit, all test and
release gates, and independent APK delivery remain unchanged. The new timing
must be measured on the next exact-source run; no performance claim is inferred
from the host contracts.


## PR34 ordinary-app timing partition (10 October 2026)

The exact release-configured run at `5703a613` completed its 19-method API35
ordinary invocation in 178.579 seconds against the unchanged 180-second deadline.
The retained timing investigation found no demonstrated redundant wait. No test
body, assertion, fixture synchronization or production behavior is changed here.

`GalleryDraftDeviceTest` now runs its same three complete methods in a separate
ordinary instrumentation process with a 90-second ceiling. Its historical method
intervals totaled 41.549 seconds; that is a planning observation from the old
single invocation, not a measured new-partition duration or guaranteed savings.
The remaining ordinary invocation keeps its original 180-second ceiling and
includes the mixed-script Korean picker/rotation check and real font/viewport
check. API30 selects 15 ordinary + 3 gallery methods; API35 selects 16 ordinary +
3 gallery + 1 seed + 1 verify. API30 separately records its one SDK-ineligible
method and the two explicit API35 restart exclusions, none as passes.

The gallery fixture establishes and verifies its own process-local rejecting
proxy before launching any gallery, prepares each local document/preferences,
and tears down its own activities, WebViews, monitors, files and proxy. It has no
dependency on an earlier test method creating those fixtures. New cold-process
behavior and cross-phase configuration restoration still require exact-source
emulator validation. A failed ordinary or gallery phase prevents the restart
boundary; the other independent phase is still attempted for diagnostic evidence.

The repeated exact `--include-test CLASS#METHOD` selector and source-digest/report
fields are reused byte-for-byte from reviewed PR41 head `107376cb`. No PR41 test
or branch is imported or modified. `tools/app_instrumentation_matrix.py` requires
one report per phase, captured matching integer SDKs, exact test-source hashes,
unchanged declared budgets, complete successful protocol evidence, exact selectors,
and a disjoint union. New gallery methods, missing/extra/duplicate/skipped cases,
stale extra report paths, source/SDK mismatches and timeout/failure evidence fail
closed. Future ordinary methods remain required automatically. Test source hashes
identify checked-out input bytes; the workflow's exact-source APK provenance must
still be checked separately. Later PR41 integration must compose both partition
inventories rather than replace either union check. It needs one authoritative
composed verifier for ordinary + gallery-draft + both vertical shards + seed/verify,
writing the combined canonical `app/coverage.json`. Distinct receipt filenames
alone do not make the current independent PR34/PR41 checkers compatible.

The additional 90-second invocation and its bounded install/discovery overhead are
explicit extra aggregate work; the 15-minute emulator step and 25-minute job caps,
180-second native/ordinary and 60-second seed/verify ceilings are unchanged. No
retry is added. Before accepting the timing fix, measure both API30/API35 release
jobs on the integrated exact source, require every method and existing oracle,
and inspect ordinary/gallery elapsed times with a target of at least 30/20 seconds
of margin respectively. These are acceptance targets, not increased timeouts or
claims from host tests. If margin is inadequate, diagnose that run rather than
rerun unchanged source to select a faster sample.

## Composed PR34 / PR41 phase contract (10 October 2026)

The preceding PR34 and PR41 sections retain their historical standalone scope,
including the failed 180-second vertical run. Their standalone successes do not
establish that this composition fits its enclosing deadline.

The driver now selects ordinary + gallery-draft + English/Manchu vertical +
Literary Chinese/emoji vertical + API35 seed/external-stop/verify. The direct-ADB
runner, all original Kotlin methods and their assertions remain unchanged from
the accepted source union. API30 requires 15 + 3 + 2 + 2 = 22 app methods, with
one SDK-suppressed method and two explicit restart exclusions. API35 requires
16 + 3 + 2 + 2 + 1 + 1 = 25 app methods. A failed ordinary/gallery phase blocks
the restart boundary; independent vertical shards still collect diagnostic
coverage, and every failure remains failed.

`tools/app_instrumentation_matrix.py` is the single authoritative source-bound
verifier for all phases. The former vertical verification command delegates to
it. Exact report-path inventory spans all three app report roots; stale, extra,
missing, duplicate, failed, skipped, timed-out or wrong-source/SDK reports fail.
`app/coverage.json`, `app/ordinary-gallery-coverage.json`,
`app/vertical-coverage.json` and API35 `app/accepted-credit-restart/coverage.json`
are separately retained byte-identical receipts of the complete composed union.
All are removed before validation; no subset checker can overwrite a full pass.
The original 32 locale captures plus 64 reachability captures, eight receipts,
native input checks and rendered-image review remain separate required evidence.

The first composed head retained the historical 900-second outer limit despite
930 seconds of API35 instrumentation ceilings before overhead. Codex identified
this structural inconsistency. The correction below changes only enclosing CI
cancellation budgets; every inner deadline, assertion and method is retained.
Final current-base release-configured API30/API35 CI must
measure actual complete execution, preserving the ordinary/gallery 30/20-second
margin targets and every existing artifact/provenance/review gate. Missing SDK
locally means host/fake-ADB checks only; standalone CI is not combined acceptance.


## Corrected composed cancellation budgets (10 October 2026)

The historical sections above describe their original 15-minute / 25-minute
limits. Those values are superseded for the current combined driver by **36
minutes for emulator execution and 46 minutes for each emulator job**. Neither
is a target runtime. The unchanged inner instrumentation ceilings total 930
seconds on API35 and 810 on API30. The direct-ADB runner and all source tests
are unchanged by this budget correction.

The source-bound model is checked by `tools/test_ci_timeout_budget.py`. References
in the following model name functions so that comment-only line shifts do not
invalidate the explanation:

| API35 controlled component | Seconds | Source |
|---|---:|---|
| AVD create, ADB discovery, one shared readiness budget, main APK install | 270 | `ci_emulator.sh:main`: 30 + 60 + 120 + 60 |
| Seven instrumentation phases | 930 | `main`, gallery, two vertical shards, restart seed and verify |
| Seven SDK-query / test-APK-install / runner-discovery preparations | 630 | `run_android_instrumentation.py:main`: 7 × (15 + 60 + 15) |
| Seed-only runner live-PID query | 10 | runner `--leave-target-running` path, distinct from shell PID checks |
| External restart boundary | 90 | `run_credit_restart_regression`: launcher 30 + four PID checks 10 each + dumpsys 10 + force-stop 10 |
| Vertical evidence-directory reset | 10 | `run_vertical_locale_matrix`, once before both shards |
| Seven capture tails | 35 | `capture_live`: 7 × 5; its normal process wait uses the remaining instrumentation deadline |
| One collection/shutdown path | 54 | `cleanup`: logcat 10+3, pull 15+3, emulator kill 10+3, ten one-second polls |
| Four possible timeout recoveries while still attempting all seven phases | 40 | native, both vertical shards and verify: runner target force-stop 10 each |
| Controlled-path envelope | **2,069** | Sum of the preceding rows |
| Processing/scheduling allowance | **60** | Inventory, protocol/report and visual-evidence processing plus normal local I/O |

Rounding 2,129 seconds upward gives 36 minutes (2,160 seconds). The job retains
its existing 6-minute image-install step and 4-minute checkout/download/upload
allowance: 36 + 6 + 4 = 46. The SDK image command remains 5 minutes plus its
15-second kill grace and is outside the script; it is not counted twice.

The all-success controlled path is 2,029 seconds. The maximum continuing failed
path is 2,069, and must remain failed. Ordinary/gallery failure skips the entire
410-second restart portion; allowing five recoveries gives 1,669. Seed failure
skips the final 50 seconds of external boundary and the 155-second verify
invocation, giving at most 1,864 with four recoveries. A failure at the last
external PID check adds its 1-second kill grace but skips verify, giving at most
1,905. Earlier failures are shorter. API30 has no restart portion and its five
possible recoveries produce the same 1,669-second envelope.

Startup timeout kill graces terminate a prefix and skip all later tests. The
readiness probes share one 120-second budget; their retries are not separate
120-second allowances. Vertical-reset timeout grace skips both shards. Capture
failure has mutually exclusive suffixes: either 5-second tail + 10-second
recovery, or exceptional 5-second tail + 5-second final wait. In the latter case
`capture_live` never returns its tuple, so main's `timed_out` remains false and
the extra recovery does not run. Cleanup is counted once; pull failure skips
both visual verifiers, and screenshot failure skips reachability.

This is a configured-path model, not a universal liveness proof. Python inventory,
union and image-verification processes, file/log I/O, process creation and OS
termination can stall outside the inner monotonic checks. They have the Actions
outer cancellation authority, not separate proven deadlines. The 60-second
processing reserve is an operational allowance. Forced cancellation may leave
partial evidence, which never becomes a pass.

Historical observations inform these allowances without proving composition:
PR41 run `38069153905` reached main completion at +547 seconds and completed the
step in 549; its job overhead excluding the step and image install was 11 seconds.
PR34 run `38064577479` steps took 274 / 174 seconds on API35 / API30, with residual
job overhead of 29 / 19 seconds. Their phase results and earlier timeouts remain
separate historical receipts. Actual corrected combined CI is still required.

The first composed run `38073935029` reported exactly: “The action 'Run Python
contracts' has timed out after 2 minutes.” Its retained process artifact later
reported 462 tests in 176.348 seconds, with two inherited optional-Pillow ICO
checks skipped and wrapper exit 0 at 176.752 seconds. That late artifact does not
override the failed Actions step. The final local composed suite required 167.102 seconds, versus 144.499 in an
earlier full run. A 3-minute cap would leave only 12.898 seconds above the higher
sample, less than the observed 22.603-second spread; 4 minutes is the first whole
minute covering both. No test is removed and unexpected failures remain failures.
The checks job moves from 20 to 22 minutes only to preserve its previous aggregate
allowance after the Python increase. Its step maxima now total 38 minutes before
untimed overhead, so **22 does not structurally admit every maximum**. That is a
separate inherited aggregate policy risk, not a solved timeout theorem.

Merge still requires fresh exact-source review and release-configured API30/35
CI, all original methods and receipts, ordinary/gallery 30/20-second margin
targets, and the existing source/APK/visual-evidence gates. A larger outer cap
cannot make an inner timeout or missing method acceptable.

## App-owned vertical evidence export (10 October 2026)

The first combined release run `38073935029` passed API30's 73 native and 22 app
method union, then failed `adb pull` of its app-specific Android/data screenshot
directory with `Permission denied`. API35 could collect that exact release
source's evidence. The API30 union pass and collection failure remain separate;
no screenshots are accepted from that missing archive. Debug/API30 behavior was
not measured by that run.

`VerticalEvidenceExportRule` is instrumentation-only. It wraps the four unchanged
vertical test methods, removes only their exact old synthetic source files and
owned MediaStore rows, then exports the already-captured bytes after the original
test and cleanup. The original method bodies, capture-state/native-input
assertions, release/debug flags, production manifest and strict direct-ADB runner
are unchanged. Original test failures and export/cleanup errors are retained
together using suppressed exceptions.

The app uses its own `MediaStore.Downloads` entries under
`Download/anpaint-ci-vertical-evidence/`; Android 10+ supports access to an app's
own Downloads entries without new storage permissions. See the
[Android shared-storage documentation](https://developer.android.com/training/data-storage/shared/media).
No root, broad storage permission, shell permission adoption or production
provider is introduced. Clearing files on the host does not clear MediaStore
rows, so the rule separately queries/deletes only its own exact locale ZIP row,
including pending rows, with a 16-row duplicate sanity limit. Owner, relative
path, literal filename and `IS_PENDING` are verified around publication. A pending
ZIP is read back and byte-hashed before it is made visible; provider SIZE metadata
is not treated as proof of flushed bytes. Failed pending rows are removed.

Four locale ZIPs each contain 26 unchanged data files plus a bounded manifest:
eight original screenshots, sixteen reachability screenshots and two JSON
receipts. The manifests bind the SDK, method identity, exact paths, byte lengths
and SHA256 values. Partial exports remain diagnostics and cannot satisfy the
complete marker. Files are limited to 2 MiB, each locale to 8 MiB uncompressed and
8 MiB ZIP, the combined data to 32 MiB, and each manifest to 64 KiB. The preceding
API35 release sample had 104 data files totaling 7,127,121 bytes; its largest was
a 605,630-byte JSON receipt. Size checks precede large content allocation and
copying uses bounded chunks.

The host resets only this public synthetic export directory inside the existing
10-second reset deadline, and pulls it inside the existing 15-second collection
deadline. `vertical_evidence_transport.py` validates every archive and its exact
allowlisted members before staging into a fresh destination, then atomically
publishes the original host layout. Missing/extra/duplicate/renamed or swapped
ZIPs, traversal, symlinks, encrypted entries, wrong SDK/method/owner, unknown
manifest fields/duplicate JSON keys, partial markers, size/hash mismatches and
truncation fail closed. Existing screenshot and native reachability validators
still run afterward and every prior failure status is retained.

Export work stays inside each unchanged 180-second vertical invocation. The
36/46-minute outer hard ceilings and all other phase/reset/pull limits remain
unchanged. Host parsing/export checks are covered by the stated outer processing
allowance, not by a new universal liveness claim. Host corruption fixtures and
source contracts cannot prove MediaStore behavior on a device: fresh exact-source
release API30/API35 CI, all 96 actual images, eight receipts, 28 native drags,
source/APK provenance and rendered-image review remain required. Debug is covered
by the same source path and host selection checks; installed debug compatibility
must be reported explicitly rather than inferred from release results.
