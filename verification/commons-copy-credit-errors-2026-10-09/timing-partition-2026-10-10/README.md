# PR34: explicitly bounded gallery-draft partition

Candidate for the [current-head P1](https://github.com/c933103/AN-Paint/pull/34#discussion_r4238142198).
This receipt records source/host evidence only. Android compilation and new runtime verification remain pending; publication/CI status is tracked on the existing PR34.

## Exact integration scope

- Existing PR34 head: `5703a61394791f18e9f2597272d908d9840599af`.
- Accepted develop base: `165a6a503529736527c689e3ac1b5432253d19ee`; clean local merge preserves both parents. The only incoming changes are PR42's ImportSelection warning-title fix and its two test files.
- Every app/native Android test source and every app assertion remains byte-identical to PR34. No production file is altered by the partition. PR38's fixture and the Korean resource routing/generator remain intact.
- `run_android_instrumentation.py` and its host tests are exact copies of reviewed PR41 head `107376cbd9a0eafcd3cedbae0365802702b525ff`, reusing its selectors and source provenance fields. No PR41 Android coverage or branch change is imported.
- No change to PR43, PR37, PR18, PR41, workflow labels, release publishing, private signing or repository visibility.

## Before / after and budgets

Before: one ordinary app invocation, API30 18 methods / API35 19 methods, 180 seconds.
After: remaining ordinary invocation, API30 15 / API35 16 methods, unchanged 180 seconds; the same three GalleryDraftDeviceTest methods run separately under an explicit 90-second ceiling. API35's unchanged seed and verify are one method and 60 seconds each. Native is unchanged: API30 73 / API35 74 methods, 180 seconds.

Ordinary coverage's aggregate ceiling changes **180 → 270 seconds**. Total app ceilings change **API30 180 → 270 / API35 300 → 390 seconds**. Total native plus app ceilings change **API30 360 → 450 / API35 480 → 570 seconds**. The existing 15-minute emulator execution step and 25-minute emulator job caps remain unchanged. A separate invocation also repeats the existing bounded test-APK install (60 seconds), SDK query (15 seconds) and runner discovery (15 seconds); these are ceilings, not measured added overhead or a guarantee all ceilings fit concurrently. No retry is added; no existing timeout is extended.

The original [API35 result](https://github.com/c933103/AN-Paint/actions/runs/38024556268) was 178.579 seconds / 180. The [retained investigation](https://github.com/c933103/AN-Paint/pull/34#issuecomment-6094044181) recorded 41.549 seconds across the three gallery methods, but did not demonstrate a removable wait. Subtracting that historical interval is only a planning estimate; a fresh process has different initialization/teardown overhead. Host tests cannot prove new runtime margins.

## Independence and inventory

GalleryDraftDeviceTest's existing `@Before` establishes and positively verifies the rejecting process-local proxy, installs its lifecycle observer/SAF destination monitor, clears its local drawing files/preferences, launches the editor and creates/asserts the local document. Its `@After` waits for real writes/destruction and independently removes monitors/files/proxy. It relies on no prior method's synthetic setup. The real viewport fixture restores locale, font scale, orientation and proxy; editor teardown restores the original language and waits for autosave. The changed invocation order/fresh process still needs the device acceptance below.

The machine-readable inventory records the exact disjoint SDK-specific method union and unchanged Android test hashes. API30's inapplicable API33 language-picker case and two explicitly omitted restart methods are recorded separately. New ordinary methods remain mandatory; new or missing gallery methods fail until the explicit partition is updated. The coverage verifier rejects extra/missing phases, stale summaries, duplicate/unexpected/skipped/failed cases, unsuccessful protocol metadata, wrong selector/deadline/source hash/device SDK, and incomplete union. A failed verification first removes stale successful coverage receipts. The primary output is `app/ordinary-gallery-coverage.json`; the existing API35 `app/accepted-credit-restart/coverage.json` contains the same complete PR34 app union, not only restart tests. Later PR41 integration requires one composed verifier covering ordinary + gallery-draft + both vertical shards + seed/verify, with the combined canonical `app/coverage.json`. Unique output names alone do not make the present independent checkers compatible; neither may replace the other wholesale. That later composition would have 930 seconds of native+app inner ceilings (180 native + 180 ordinary + 90 gallery + 360 vertical + 60 seed + 60 verify), already more than the unchanged 900-second outer step before setup. It therefore needs measured combined runtime and an explicit integration decision; these current PR34 receipts do not establish that all later ceilings are available or that the combined stack is accepted.

## Local checks and independent review

- Full host-suite output: **420/420 passed, no skips** in the final post-rename run (101.565 seconds; `host-tests.txt`). The earlier 420-test run also passed in 86.020 seconds. This is host/fake-ADB evidence only.
- Shell syntax, Python compilation and whitespace checks are required before publication.
- Runner and its tests must match PR41 byte-for-byte; all Android test Kotlin files and workflow YAML must match existing PR34 byte-for-byte.
- No Android SDK/ADB or cached Gradle 8.13 distribution is available here. Android compilation/emulator tests are unrun locally.
- Independent assistant source review found no PR34-only source blocker. Its separate post-rename checks passed 7 matrix/wrapper tests (1.764s), 16 readiness/restart-boundary tests (39.219s), and 28 runner/protocol tests; shell syntax and whitespace checks passed. Final tree binding is required before publication. Runtime margins and later composed PR41 integration remain unverified.

## Exact-source acceptance plan

1. Preserve the current full/release PR labels. Publish only to existing PR34 after independent review and complete remote-tree readback, preserving original head and develop parents. Keep draft; do not merge/release.
2. Verify actual tested merge/tree matches the candidate integrated source and `build-info.json` says release; require generator, complete host/JVM/lint, APK/source and test compilation checks.
3. Require both API30 and API35 jobs, exact native inventories, app counts (15+3 / 16+3+1+1), and source-bound coverage receipts. Inspect the unchanged Korean four-phase exact text/public identity/rotation and French/Mongolian font/viewport logs. Every gallery method must pass in its new independent process.
4. Inspect actual elapsed times. Target remaining ordinary invocation ≤150 seconds (≥30 seconds under180) and gallery invocation ≤70 seconds (≥20 seconds under90), both platforms. These are review acceptance targets, not new test timeouts. Account for install/discovery overhead in the unchanged outer step.
5. Require complete seed, live original PID/resumed Gallery boundary and fresh-process verify. No omission, timeout, skip, blind retry or faster-sample selection counts as acceptance.
6. If any gate fails, diagnose the exact failure and revise only within this authorized repair. Request one fresh exact-head review once evidence is ready. Keep PR43/PR41 integration separate and reconcile both coverage inventories later.
