# PR122: preserve distinct English and default Help oracles

Application head: `0d56dd970c22398f7fa032d1baee4a1b74c83f2b`  
Application tree: `b8655bf9b69f89afd3499b9efce1414746de326c`  
First parent: prior PR122 head `fcdb417dddd5cba516eea661e917f0183ed61d46`  
Second parent / integrated develop: `5dba779c904a25bde2ec6d6f8f48eb3cad901a1e`  
PR: https://github.com/c933103/AN-Paint/pull/122  
Scope tracker: https://github.com/c933103/AN-Paint/pull/75

## Exact hosted failure

[Run 39057824063](https://github.com/c933103/AN-Paint/actions/runs/39057824063), job `117469343203`, artifact `12110274600`, executed the prior head. The downloaded artifact has 114 JVM reports: 1,104 tests, one failure, no errors or skipped tests. The failing method was `AssemblyActivityTest.englishHelpModesReachActualHelpAndExactPositionToolbarWithCurrentLabels`, line 460. Exact JUnit comparison:

`expected:<...«File > About, licen[c]es & credits» panel.> but was:<...«File > About, licen[s]es & credits» panel.>`

The test incorrectly assumed a language-only `en` configuration selected unqualified default resources. In this hosted API33 configuration it resolved to the en-US value, whose full Help ends in `licenses`, while the unqualified default ends in `licences`. This is a test oracle/routing error, not an assembly placement/model failure.

The failing pre-loop assertion prevented the subsequent actual Help/toolbar locale loop from running. No pass is attributed to that loop on the failed head. The separate `exactFirstPlacementAndUnplaceMatchHelpWhileSnapRemovalCanFillTheGap` method passed (0.424s); `AssemblyActivityTest` overall had 22 tests and one failure. Lint subsequently passed on the failed head. The exact XML, job excerpt, aggregate report counts and downloaded artifact hash are preserved here.

## Repair and coverage

The only new PR122 repair changes `AssemblyActivityTest.kt`:

- Compare the complete language-only `en` result to the complete en-US fixture.
- Separately request unmatched `zxx` and compare its complete result to the unqualified default fixture.
- Assert the two complete fixtures differ, and assert each requested resource configuration is retained.
- Leave the nine app-language actual Help/toolbar consumers and the placement/model controls intact.

No text normalization, spelling substitution, containment-only replacement, or assertion removal is used. Both original complete fixtures remain byte-identical. Android's [default-resource matching guidance](https://developer.android.com/guide/topics/resources/providing-resources.html) supports using a locale without a matching catalogue; `zxx` is absent from the application catalogues. Its actual runtime route and the full repaired method remain pending the new hosted run. Compilation alone does not execute this route.

The current develop merge integrates PR121's five disjoint files. Every one of the 1,196 application leaf paths, blob hashes and modes was verified against the composed source before publication. Relative to current develop, the application diff is the same 17 scoped PR122 paths. All initial Help text, fixtures, source-boundary host tests and production placement/model code are unchanged by this repair. The separate Japanese follow-on is not included. P3 priority and held PR56 remain unchanged.

## Verification of the composed repair

- Full host suite: **902 passed**, normal (208.956s) and optimized (208.548s).
- Focused assembly Help/source-binding plus integrated memory-modality controls: **69 passed** in each mode.
- Canonical catalogue validation and `git diff --check`: passed.
- AAPT2 compile of all canonical resources plus the existing two exact-script mirror layouts, and resource link: passed.
- Supplementary Kotlin 1.9.24/API35 compilation of changed test source and its support classes against existing compiled dependencies with fresh resource symbols: passed. This is not a clean Gradle build or Robolectric runtime execution.
- The previously recorded local Gradle attempt was blocked while downloading Gradle8.13 (`Network is unreachable`); the original immutable evidence retains that failure. No local JVM/device pass is claimed.
- New exact-head [hosted run 39059990522](https://github.com/c933103/AN-Paint/actions/runs/39059990522) was queued when this receipt was prepared. No full hosted JVM pass is claimed by this receipt.

## Other-language source bindings

The separate [initial full-source change receipt](https://github.com/c933103/AN-Paint/blob/878c912c017e7b145d51d366e064727b34602e38/README.md) and its [binding inventory](https://github.com/c933103/AN-Paint/blob/878c912c017e7b145d51d366e064727b34602e38/other-language-source-bindings.json) remain applicable: 50 other-language full Help overrides need complete-entry/source-binding re-review and 112 English-fallback locale routes need recheck. Historical full-value acceptance is not carried forward across the changed English source. This repair makes no whole-language claim and grants no acceptance to those bindings.

`evidence.zip` contains raw failed-run evidence, exact repair patch, source/remote-tree manifests, both full host logs, focused logs, catalogue/diff results, supplementary compilation recipe/logs, and snapshots of the repaired test and unchanged complete fixtures. `receipt.json` binds the archive and application head. Review and merge remain with the parent reviewer.
