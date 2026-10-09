# Separate AN-W04 gallery language-layout fixes

Two independently tracked findings, with separate source commits:

1. [Native vertical description/status](AN-W04-gallery-vertical-status.md).
2. [Truncated action/search labels](AN-W04-gallery-control-clipping.md).

Baseline is PR #29 `afbb8015130dd82546a4c22a9d3337782f7b995f`, whose scoped SVG
translation work is not changed or claimed as gallery-layout acceptance.
All-language applicability concerns non-translation rendering/controls. Existing
incomplete translation catalogues keep their genuine fallback, without adding
English-filled overrides or weakening completeness gates.

The existing shared `VerticalUi` / `ColumnScrollView` mechanisms are reused. No
older unaccepted PR #18/#19 production prototype is imported. New tests and
source snapshots require exact-head CI/native-rendered capture review before
acceptance; local Python checks alone cannot establish Android UI behavior.

## Local checks and test budget

All 321 existing Python host tests passed in 49.959 seconds after the complete
candidate source changes; zero skips/failures/errors. The first vertical-only
run had one formatting-sensitive source assertion failure. Its equivalent
ColumnScrollView expression was restored to the expected form, its 21-test class
passed, then the complete 321-test suite passed. The final raw log is retained in
`logs/host-python.log`; some passing runner-fixture tests deliberately print mock
failure JSON, so the unittest summary determines this host result.

The new Android matrix adds 16 JUnit executions across API30/35, not 1,680 Activity
launches. `GalleryControlsLayoutTest` checks 140 current offered catalogues × two
font scales × three widths × two APIs = 1,680 lightweight layout cases. Controls
are reused across widths; it creates 3,360 buttons and 1,120 search fields overall,
with 6,720 empty-hint/entered-query measurements. It records actual duration and
completed/expected cases in `build/reports/gallery-controls-matrix` rather than
claiming an unmeasured runtime.

The real-Activity additions comprise 20 launches for vertical SVG failures and
72 launches for control reachability, with up to 184 PNG/JSON pairs across the
new representative checks. Existing tests and workflow deadlines are unchanged.
Android compile/native runtime and CI budget fit remain unverified until CI runs;
if profiling identifies a runtime problem, optimize fixture reuse before reducing
coverage or increasing deadlines.

## Refreshed combined base

The candidate was rebased onto exact PR #29 integration commit
`d601dba3821fafa254b02172eee350428b28a0f4`, tree
`293708639d4bc3382c4f3de8cf35cc0164257b91`. All 21 accepted PR #19 paths were
verified against GitHub blob IDs and remain unchanged by either fix. The complete
combined Python suite passed: 326 tests in 50.932 seconds, zero failures/errors/
skips. This includes the five newly integrated gallery task-routing source tests.
The corresponding log is `logs/host-python-combined.log`. Android validation still
requires exact-head CI; neither the prior base's CI nor this host result substitutes
for compilation, native-rendered layout evidence or installed checks of the fixes.

The final rotation pass replaced the obsolete orientation callback for the removed
fixed-height description scroller with a request to remeasure the live controls.
The same-Activity regression also rotates French and Mongolian in both directions,
preserving the browser, native editable field and typed query. No extra Activity
launch or screenshot is added. The final complete combined Python run passed all
326 tests in 53.372 seconds; its raw log is `logs/host-python-rotation.log`.

## First complete CI and fixture correction

The [first complete candidate run](first-ci-0a2d19d/README.md) passed compilation
and all 93 installed API35 checks, but failed 12 of 706 JVM checks in the new
fixture setup; lint was not reached. Its complete case inventory/failure details
and hash-verified artifact manifest are preserved separately from later results.
The bounded correction attaches catalogue controls to one reusable Activity per
API/scale, and synchronizes the simulated Display/ViewRoot during same-Activity
rotation. All previous label, live-query, reachability and state-retention
assertions remain; additional actual-node/window diagnostics and fixture sanity
assertions are added. This adds four lightweight Activity hosts overall, not one
per catalogue. No production behavior, strings or workflow deadline changes.
The complete combined Python suite passed again: 326 tests in 50.557 seconds,
zero failures/errors/skips (`logs/host-python-fixture.log`). Android verification
of the corrected fixtures remains pending the next CI run.
