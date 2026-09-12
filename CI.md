# Android build and test workflow

Updated 12 September 2026. APK production, regression checks and emulator results
are separate outcomes. An emulator must not prevent obtaining an already-built
APK or completing unrelated work.

## What runs

| Trigger / choice | Regression and lint | Universal APK | Emulator coverage |
|---|---|---|---|
| Code push to `develop`, or pull request targeting it | Yes, independently | Yes | API 35, all native and app checks |
| Run workflow → `current` | Yes | Yes | API 35 |
| Run workflow → `full` | Yes | Yes | API 30 and 35 in parallel |
| Run workflow → `none` | Yes | Yes | Explicitly not run |
| Markdown / historical verification changes only | Not automatically rerun | Not automatically rebuilt | Not automatically rerun |

Direct pushes to a working branch do not duplicate a PR/default-branch run.
New commits cancel obsolete runs for the same branch/PR. Failed emulator matrix
jobs do not cancel the other platform. A failed test remains a failed check;
there is no `continue-on-error` or replacement of failures with green results.

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
API 30 and 35 jobs. Only the Ultra HDR class is excluded on API 30, where Android
has no gain-map API. No test is removed from the current-platform suite.

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

Cache statistics are printed after assembly. The first run populates the cache;
no speedup is claimed until reuse has been measured on a later build. Regression
and emulator jobs do not depend on this cache. References: the official
[CMake 3.22 launcher documentation](https://cmake.org/cmake/help/v3.22/envvar/CMAKE_LANG_COMPILER_LAUNCHER.html),
[ccache 4.5.1 manual](https://ccache.dev/manual/4.5.1.html), and
[Ubuntu Jammy package record](https://launchpad.net/ubuntu/jammy/+package/ccache).

## Deadlines and evidence

- Regression job: 20 minutes; build job: 35 minutes; each emulator job: 25 minutes.
- Emulator SDK installation: 5-minute command deadline; device discovery:
  60 seconds; boot and Android service readiness share 120 seconds; main APK
  installation: 60 seconds. Readiness probes have a maximum 10-second attempt
  inside that shared deadline, with progress and failure logs. They may retry
  transient startup failures; APK installation and app tests are not retried.
- Each test APK installation: 60 seconds; runner discovery: 15 seconds. Each
  native/app instrumentation invocation: 180 seconds. These inner budgets fit
  within the whole emulator execution step's 15-minute limit, leaving time to
  collect failure reports and shut down.
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
