# Independent review: two JVM fixture corrections

No blocking source-review finding remains in the two-file candidate. The corrections align the fixtures with their actual locale and graphics contracts; they do not establish a fresh Android pass.

- Baseline public head: `da4b40bd47a5d76d45b21d86fdc59368b4b52fd2`
- Baseline tree: `ab6f5497e147e81d4c50f4954ea87f364be087aa`
- Reviewed candidate tree: `d2379b932cc976bb5347515887ecdfc4729ee70d`
- Writer patch SHA256: `ecf5acb692828fc75b545e4de40073b944ed52d8474c1b81a9cc0d25c342ebe9`

Only LocalizedDialogLayoutTest.kt and UiDirectionContextTest.kt change. One-time scope comparison confirms all production, resources, fonts, installed tests, workflow and deadlines unchanged. The twelve native direction executions and their shared helper bodies are unchanged; only the legacy method and an import change in that file. Exact source bindings are in `source-scope.json`. No permanent source-snapshot test is added.

## Retained notice

The original exact run failed reading-offset equality on API30/35 after the fixture copied system configuration into a plain Activity's selected-locale resources. The corrected helper saves the full LocaleList, retains the new system geometry, restores the selected list before the next display callback, and verifies activity/root locale lists after each stage. The test additionally checks activity, dialog, root and both rail contexts, using fixed tag-derived expected direction.

I checked the ordering against Robolectric4.14.1 primary source: setQualifiers invokes changeDisplay before updating resources, and changeDisplay idles the main looper. Therefore the new restoration is synchronous between the resource replacement and the explicit second display traversal. It does not fake child measurements or scroll the reader back into the expected position.

The original 0/47 reading-offset equalities, both orientations, rail identity, range, repeated-layout, window width, body text, focus behavior and dismissal guards remain. New assertions make incorrect locale preconditions fail explicitly. Runtime proof is still required because local Python checks do not execute these callbacks.

Sources: [RuntimeEnvironment](https://raw.githubusercontent.com/robolectric/robolectric/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/RuntimeEnvironment.java), [ShadowDisplayManager](https://raw.githubusercontent.com/robolectric/robolectric/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowDisplayManager.java).

## API21/24 legacy coverage

The failed legacy assertion demanded positive real-font geometry despite using LEGACY graphics below Robolectric's API26 native-graphics minimum. The replacement preserves both SDK executions and widget construction/vertical measurement, but tests the supported requirement: explicit Configuration.locale versus Configuration.locales access, four fixed vertical directions and inverse horizontal direction under opposite process defaults, full text/content descriptions and genuine same-length text-change layout/invalidation scheduling.

The test first completes the previous layout and explicitly verifies cleared scheduling observations, then changes text and requires real new requests. It adds no fake metrics, dimensions, paint shadow or forced positive raster. Official ShadowView4.14.1 exposes clearWasInvalidated and setDidRequestLayout without SDK restrictions; the requestLayout/invalidate shadows record the observations and forward the real methods. These are supported instrumentation hooks, not a substitute rendering result. [ShadowView source](https://raw.githubusercontent.com/robolectric/robolectric/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowView.java).

The twelve API30/35 native geometry/pixel/accessibility/Save/lifecycle cases remain intact. The entire updated class cannot be claimed to compile against old production because the revised legacy body directly calls the new Context overload. Any old-production compatibility claim is limited to the unchanged native cases. Actual legacy-device glyph rendering remains unrun and unclaimed.

## Checks and limits

PASS: exact two-file source/mode scope, whitespace, and independent 58 selected host tests normally plus the same 58 under Python -O, exits 0, 1.056s/0.845s. Modules: test_localized_dialog_layout, test_localized_dialog_composition, test_vertical_text_redraw, test_vertical_notice_characterization, test_dialog_evidence_transport, test_vertical_control_reachability. Commands use PYTHONDONTWRITEBYTECODE=1 and PYTHONPATH=tools.

PASS: both terminal writer aggregates independently reconcile all 643 current source-discovered identities, with no missing, extra, duplicate, failed or skipped method. Ordinary: 144.120 seconds (144.677 wrapper); optimized: 155.518 seconds (156.260 wrapper). Both exit 0 under the unchanged 240-second cap and bind tree d2379b93. Exact log and receipt digests are in `writer-aggregate-audit.json`. Local Android compilation and execution are unrun because the SDK is absent. Prior da4 remains an actual failed checkpoint: 906 executed, 902 passed, four failed. Its separate immutable artifact review retains both failed XML pairs, all rasters, the explicit fringe disposition and installed successes. Those successes do not turn this fixture successor into an executed pass.

Fresh exact-source JVM evidence must retain all 906 current identities and show the four corrected executions passing without skipping them or weakening the native 12/reading-offset guards. Reconcile the rest of the source-derived runtime inventory and artifact bindings at the actual run; select installed scope under current project policy rather than inventing a new blanket matrix requirement for this test-only change. No production, wording, pixel tolerance or timeout alteration follows from this review.

## Reproduction and frozen inputs

Run `audit_fixture_scope.py --repo REVIEWED_CHECKOUT --output RESULT_JSON` for the one-time source scope. Run `audit_host_aggregates.py --repo REVIEWED_CHECKOUT --writer-dir WRITER_RECEIPT_DIRECTORY --output RESULT_JSON` for complete terminal host reconciliation. The raw writer logs/receipts are separately delivered in the same evidence archive to avoid duplicate logs. The reported actual-da4 archive is separate; this review never edits its evidence or changes its failed gate.
