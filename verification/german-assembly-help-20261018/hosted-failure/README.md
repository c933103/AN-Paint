# Hosted German toolbar regression: failed fixture and bounded repair

Failed head: `4e3816f82cabd73295a06acaac75a304504f871b`.
Checkout: `3b33db77edb1dd7ce13b11a5448779fb2adafe55` (PR merge checkout).
[Failed run](https://github.com/c933103/AN-Paint/actions/runs/39084426999), regression job `117547916672`.
Repaired head: [`2686f35c1c43910f659fdfe48944a61516bd473e`](https://github.com/c933103/AN-Paint/commit/2686f35c1c43910f659fdfe48944a61516bd473e).
[Fresh run](https://github.com/c933103/AN-Paint/actions/runs/39086030171) is pending at receipt creation.

## Exact failure

The downloaded regression artifact's SHA-256 is `4600f826129e6838629b1f4a9cb2493395a22fbd7bb09a728ec2ea78cf126546`, matching the upload log. Its 120 JUnit suites contain 1,124 tests, one failure, zero errors and zero skips. The exact affected XML is retained alongside this receipt.

`germanExactPositionToolbarMatchesHelpAndUnplaceOnlySometimesClosesAGap` failed at its first assertion (line 121; reported through callback line 63): expected `Exakte Position`, actual `Exact position`. Its later placement assertions did not run. The other three class methods passed, including complete compiled-resource values, the actual full Help dialog and actual crop toolbar flow.

The test selected German using `AppLanguage.select`, then created the Activity, and only afterward called `AppLanguage.refresh`. The global `ui()` resources used during toolbar creation were still English. Unlike Android's application lifecycle, setting the Robolectric LocaleManager fixture does not dispatch the application's locale-change callback. Dialogs created after the helper's refresh used German and passed.

## Repair and retained coverage

Before constructing the Activity, the helper now binds `PaintApplication.currentResources = AppLanguage.wrap(context).resources`, matching existing localized test fixtures and the production application's locale-change binding. Its existing cleanup restores the original resources, platform locale, preference and process locale.

The exact German initial toolbar assertion remains. No assertion is removed or relaxed: full Help, negative/fractional/zero coordinates, persisted state on invalid/Cancel, overlap, unchanged other images, snapping rejection, both Unplace outcomes and Undo remain. All production files and resource values are unchanged by the repair. `repair.patch` is the entire three-line test-only increment.

Focused 12-test checks pass normally and optimized. Full AAPT2/mirrors/link and supplementary changed-test compilation pass. Full host reruns are pending at this receipt's creation. Local full Gradle/Robolectric remains unavailable because its distribution download is network-blocked. Only the new hosted result can establish whether the complete repaired consumer method passes; compilation alone cannot.

The failed run's APK/source, exact-script resource, core API35, position API35 and combined emulator jobs all passed; the regression job failed despite its lint step passing. These old-head passes are not silently transferred to the repaired head. Code and Security reviews were requested anew on the exact repaired head.

This receipt is additive on the separate evidence ref. The earlier local review/check packet and failed application source remain reachable; no PR56, other-language or explicit-hold status is changed.
