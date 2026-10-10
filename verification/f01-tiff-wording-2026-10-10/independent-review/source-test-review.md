# F01 independent source and test review

10 October 2026. **Accepted within the bounded source/test-design review scope after the checkbox-test repair. No remaining source/test-design blocker found.** Android execution and release acceptance remain pending.

## Verified source identities

| Snapshot | Independently recomputed Git tree |
|---|---|
| Develop base, commit `80c14372b0504bc44f9f2809ad477247fdc8100b` | `d9858229f98068bef9c6194c90d77610c5ecceec` |
| Revised eleven-entry candidate | `89e43725c5b7c2f01827cfa06510c21f5268314c` |
| Isolated 26-entry expansion | `b81391fb46dd9ee1bdb86c3faf693462e1316232` |
| Final combined candidate | `bde13ca4bbd9a45198ab4da9cadd85d900aaa594` |

The final tree contains exactly **37 one-resource substitutions and four added test files**, with **1,253 base files unchanged**, 1,294 files total, no removals and no mode changes. Actual file hashes, executable bits and the exact union were independently checked, then rechecked when this report was materialized. The original and expansion resource bytes match their respective reviewed stages.

English “may reduce” and pt-BR “pode reduzir” appropriately qualify the size outcome while retaining pixel preservation and unchecked/uncompressed guidance. All 26 additional resource replacements and both expansion test-oracle maps match the individual linguistic proposal map. The encoder, other application code, existing tests, other resources, routing, fallback policy and canonical-source policy remain unchanged. Script, regional and emoji distinctions are preserved. This narrow model review is not native-speaker or full-language acceptance.

## Finding resolved before acceptance

Both new Kotlin classes initially asserted that the TIFF checkbox’s performClick() returned true. The checkbox has no click listener: its checked state can toggle while the returned listener-handled value is false. The author removed only those two return-value assertions. Actual clicks and explicit checked-state, description and callback assertions remain. No production or resource byte changed.

This is a **source/API-contract finding, not an executed Android failure**. Evidence:

- [Android return-value contract](https://developer.android.com/reference/android/widget/CompoundButton#performClick())
- [Android 13 framework implementation](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-13.0.0_r1/core/java/android/widget/CompoundButton.java#L142-L154), blob `63f8ee7528f2f939a4001fe3bf8b6391f0bc231c`
- [Robolectric 4.14.1 CompoundButton shadow](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowCompoundButton.java), blob `18b606a357d25a14f5cd35c59b56af80e5f11d2f`, does not override the click method
- [Robolectric 4.14.1 View delegation](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowView.java#L269-L275), blob `1887043237a57dd3bff431f4cc82631de44b7c2e`, returns the underlying result

Superseded trees are retained as history: eleven-entry `f0c9e32a6d8e3b69d0d55b2c1972433cd05533d9`; combined `40a4df55453208f46cf9c3188e717c07e75882a4`. They are not the accepted final snapshots.

## Independent checks on the revised combined tree

- Structural validator: passed
- Complete host suite: **374 tests passed, no skips, 52.074 seconds**, exit 0
- **41 negative controls rejected by assertions**, with zero test errors
- Positive eight-test focused runs passed before and after the temporary-copy mutations
- Candidate source identities remained unchanged after testing

The mutations individually reverted all 37 corrected clauses and separately removed the emoji, corrupted pixel preservation, reversed unchecked guidance, and inserted an invented Welsh translation. The [host log](../combined-evidence/independent-final-host.log) has SHA-256 `5ecb90e7446a8e48cf653172d42517f71a69dad43cbdbf320fbf27c1069dcbe5`; [negative-control evidence](../combined-evidence/independent-final-negative-controls.json) has SHA-256 `eb114e4d39cee62f04b9280dd9b5bba1e7310c8a2faa334fd27d8c07ae74d6fe`. Deliberately rejected mocked instrumentation summaries in the host log are not Android test results.

## Coverage and remaining limits

Nine new API33 Robolectric methods across two classes inspect actual production SaveOptionsDialog/resources with fixed reviewed expected strings. They cover both starting checkbox states, positive callback flags and filename, toggles, DIB/TIFF switches, both cancellation paths across the suite, English variants, pt-BR, vertical/emoji fixtures, Welsh fallback and the 26 additional locales. They do not invoke an encoder.

**All nine methods remain uncompiled and unrun locally.** The pre-repair combined Gradle attempt at `40a4df55453208f46cf9c3188e717c07e75882a4` failed fetching uncached Gradle 8.13 with “Network is unreachable,” before any task or Kotlin compiler. No revised-source execution is inferred. No APK, lint, emulator/physical-device, screenshot, rendering/accessibility or whole-TIFF size-measurement pass is established. Candidate-specific Android validation and applicable rendered checks remain required.

The inventory matches all 60 explicit definitions: 37 corrected and 23 unchanged. Twelve probable and four uncertain language cases remain unresolved; the seven already-qualified entries receive no broader acceptance. All 81 missing-key offered locales remain unchanged, with source-predicted fallback rather than per-locale runtime proof. F01 remains open. Parent counts remain **475 total / 3 structural complete / 472 pending**; no parent or full-language obligation is closed.

The [structured report](source-test-review.json) contains all nine method names and detailed verification scope. Separate [expansion-map](expansion-map-review.json) and [combined-inventory](combined-inventory-review.json) reviews cover map/script preservation and inventory bookkeeping. This reviewer performed no source edits, remote writes or CI dispatch.
