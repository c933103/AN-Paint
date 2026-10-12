# Independent review: resource-context UI direction

## Decision and scope

No blocking source-review finding remains in the corrected candidate. The patch is a coherent, bounded response to the observed API30 direction inconsistency. This is an authoring review; Android compilation, native execution and installed repair proof remain unrun for this candidate.

- Baseline: public head `43ab6622cdf6aac957a8d31cf2c5c20009e71d6e`, tree `592a60877524c5c118695cb45a4d0d5cd257b25a`.
- Reviewed candidate staged tree: `ab6f5497e147e81d4c50f4954ea87f364be087aa`.
- Writer patch SHA-256: `d3b0e52cbe8589cbfc0cb93b634cbfa3abe1a6bd8a2c04047d2163bb9cd5752a`.
- Exact scope: 23 paths, including 15 production Kotlin files, two JVM files, two installed-test/evidence files and four host-test files. `source-scope.json` binds their contents and modes. This is a one-time review receipt, not a permanent application CI snapshot contract.

## Source assessment

The new `VerticalText.uiDirection(Context)` reads the locale from that Context's resources, with API24-guarded LocaleList access and the legacy Configuration.locale branch below API24. The explicit-Locale mapping remains the same. Each changed UI call site supplies its activity, widget, panel or dialog-builder Context. Activity receivers are explicitly qualified where nested Kotlin receivers could otherwise change their meaning.

The important chain is consistent: workspace scaffold, FlowButton/FlowTextView construction and measurement/drawing, wrapping, reading-column origin, Save form construction, deferred dialog mounting and NumericSlider geometry all consult resource-context direction. The small adjacent consumer sweep applies that same rule to colour controls, gallery shells, legal-dialog shells and empty-canvas UI captions. It does not alter drawing-text model defaults, explicit picker-row locale choices or font selection.

Resources, fonts, assets, workflow and timeout limits are unchanged. The full M04 query-failure raster/control source and installed gallery comparator are unchanged. LocaleTypography and LocaleTooltip retain their existing font-adjacent defaults; the candidate does not establish a general font/process-default consistency repair.

## Behavioral tests and review corrections

The new UiDirectionContextTest has seven methods and 14 expected JVM executions: the six class-level methods run on API30/35, and the legacy method on API21/24. These are current-source expectations, not historic method-count gates. Existing 892 executions plus these 14 imply 906 for this candidate; fresh source-derived inventory must confirm the actual run.

The controlled mismatch cases cover all four vertical profiles (Literary Chinese, Manchu, vertical English and vertical emoji) plus English horizontal resources under a vertical process default. They compare the same attached widgets' geometry and exact raster arrays before/after the default reset, assert full accessibility text, and check native versus vertical rendering mode. Save construction and the separate deferred-mount race are exercised, including slider orientation, real actions and LR/RL initial columns.

The rotation/recreation matrix now covers the inverse horizontal case as well as the four vertical cases. It checks fixed expected scaffold and renderer modes after the default is reset following callbacks, uses display-backed root geometry, and preserves a real document pixel through normal persistence/recreation. Existing VerticalTextRedrawTest uses localized resource Contexts while retaining its prior growth, empty-text, redraw and same-height assertions.

Corrections reviewed before the freeze:

1. Attach the widget fixtures before reading their native accessibility nodes.
2. Include the inverse-horizontal case in lifecycle coverage, rather than relying only on vertical cases.
3. Wait for actual laid-out Save content, including mounted columns.
4. Record workspace-root and dialog-root resource locales separately in installed failure telemetry.
5. Restore locale/resources even if teardown I/O fails.

The test class uses APIs available to baseline43, so a targeted old-production/new-test run can demonstrate old-fails/new-passes without reconstructing a permanent snapshot gate. That Android control has not run locally.

## Installed diagnostics and evidence transport

The Save test retains the existing command resolver, native click, busy/readiness behavior and 15-second wait. Its observer logs before input, DOWN/UP/CANCEL and failure, returns false, and is removed afterward. The snapshots distinguish process, activity, target, workspace-root, dialog-root and application locales; they also retain selection, busy/save generation, attachment, bounds and form/column presence.

The exporter clears three exact optional failure-frame names and includes them only after failure. Successful exports retain the original required inventory. Failure frames cannot make an incomplete export pass: the new host corruption test covers both honest incomplete and dishonest complete claims. Raw failed-frame export remains diagnostic; the strict success decoder still rejects it as successful evidence.

## Relationship to the actual failure

The separate immutable run43 review records API30 94/95 with the Literary Chinese native Save-layout timeout, and API35 104/104. Actual landscape pixels and geometry establish inconsistent horizontal rendering under the selected vertical resource locale. Source analysis makes a process-default reset a plausible mechanism; the exact framework callback/default value was not logged in that run. This patch must not retroactively mark that failure passed or claim that the hypothesized callback was observed.

## Verification

PASS: independent source-scope/mode/manifest audit and whitespace check. PASS: 101 selected Python host methods in ordinary mode (90 + 11) and the same 101 in optimized mode, all exit 0. Exact commands, durations and log hashes are in `independent-local-checks.json`.

PASS: both frozen writer aggregates independently reconciled against all 643 current source-discovered host identities, with no missing, duplicate, failed or skipped identity. Ordinary: 156.249 seconds (156.706 wrapper); optimized: 164.943 seconds (166.517 wrapper). Both exit 0 under the unchanged 240-second cap and bind the same candidate tree. `writer-aggregate-audit.json` retains exact receipt/log hashes. A Python host pass is not Kotlin compilation or Android runtime proof.

UNRUN locally: Kotlin compilation, API21/24 legacy tests, API30/35 native tests, old-fails control, installed Save flow, candidate screenshots and current-device shaping. The local environment lacks the Android SDK and Kotlin compiler.

## Fresh CI acceptance plan

1. Bind the actual head, base, ordered synthetic-merge parents, tree, run/jobs and artifact digests. Require successful main/test-APK and JVM compilation; match APK embedded/delivered source and compiled resource/font/licence inputs to that actual tree.
2. Derive complete JVM identities from the current Kotlin declarations. Expect this candidate's 906 executions with no missing, duplicate, unexpected, failed or skipped identity. Inspect all 14 new executions individually. A targeted old-production/new-test failure is additional causal evidence, not permission to relax current tests.
3. Reconcile installed source-derived schedules and terminal protocol receipts on API30/35. Preserve API30's two explicit restart omissions and require the remaining scheduled tests. Inspect the previously failed Literary Chinese case's portrait/landscape native Save flow, exported frames, JPEG/input receipts and locale/touch telemetry. Keep existing phase and case deadlines unchanged.
4. Recompute the unchanged M04 112 success pairs, 28 pre-assertion diagnostics, 189 full-reference raster triplets, 78 real mutation controls and four control summaries. Preserve all pixels and current semantic/accessibility/lifecycle/component/opaque-loss guards. Review every nonzero positive difference afresh; do not silently reuse the run43 mixed-Arabic fringe disposition or invent a universal pixel tolerance.
5. Recompute installed Arabic COPY/INSERT complete-reference rasters and source/route/message-bound natural-update receipts. Their installed comparator remains strict. Source publication or a development APK may be labelled accurately while asynchronous runtime gates are pending; no fully verified repair claim until the required actual results support it.

## Primary API review

Robolectric 4.14.1's ActivityController implements the explicit Configuration/DisplayMetrics/diff overload used here. Its recreate operation restores the original stopped lifecycle state, consistent with the fixture's subsequent restart/resume sequence. This source compatibility inspection is not execution evidence. Sources: [ActivityController](https://raw.githubusercontent.com/robolectric/robolectric/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/android/controller/ActivityController.java), [ShadowDisplayManager](https://raw.githubusercontent.com/robolectric/robolectric/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowDisplayManager.java).

## Replay

Run `audit_source_scope.py --repo CHECKOUT --manifest WRITER_CHANGED_FILES_JSON --output RESULT_JSON` against the reviewed staged checkout. The script checks only this one-time source binding; it is not intended to enter application CI. Run the seven modules in `independent-local-checks.json` with `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tools python3 [-O] -m unittest -v ...` for the selected host checks. Do not run heavy checks concurrently with bounded full-suite timings.

The actual run43 artifact checkpoint is separately durable at `50d632805721ea0099bdf4b16400d24b94104abf`; it preserves the failed API30 outcome and replay inputs. The writer reports reconstruction/hash verification of the original large replay ZIP from ordered transport parts. This authoring review does not replace that actual-run receipt.
