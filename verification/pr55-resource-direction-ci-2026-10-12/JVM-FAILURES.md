# Fresh JVM failures: run 38285607590

Source: head da4b40bd47a5d76d45b21d86fdc59368b4b52fd2, synthetic merge daab4b4f2c87bc6475ba6a0d2c0f9b35ea36b7e0, tree ab6f5497e147e81d4c50f4954ea87f364be087aa. The source-bound regression artifact SHA-256 is 459d6ddd95b4ae8f3126477cf8d45d8c01182bf4b342ddb3f1e77e68abae9e7e.

## Observed

All 906 expected JVM identities executed. 902 passed; four assertions failed, with no skipped, missing, extra or duplicate identity. The exact XML stacks remain in the replay inputs and `regression-audit.json`.

- LocalizedDialogLayoutTest.retainedVerticalNoticeKeepsReadingOffsetAcrossRotation[30]: expected reading offset 0, actual 7757.
- Same method on API35 (unsuffixed identity): expected 0, actual 6564.
- UiDirectionContextTest.legacyResourceContextsDoNotNeedProcessDefaultOrApi24LocaleList[21]: unlabeled positive width/height assertion failed.
- Same method on API24 (unsuffixed identity): same assertion failed.

The retained-notice assertion is line323; line67 is only the withActivity wrapper. The legacy assertion is line209, before line210's native-layout/direction assertion. Neither failing legacy widget identity nor its actual dimensions were logged, so this review does not invent those values.

All twelve new API30/35 direction executions passed, including four vertical mismatch profiles, inverse-horizontal mismatch and rotation/recreation. Their geometry/pixel/accessibility assertions remain credited only to this actual native run. API21/24 native rendering was not run.

## Retained-notice fixture inconsistency

The unchanged fixture captures its RL/LR oracle from process Locale.getDefault(). Its resizeDisplay helper then copies Resources.getSystem().configuration into activity.resources at line415, replacing the selected resource locale while retaining the process-based expectation. The changed ResponsiveDialogColumns now correctly consults its rendering Context, so the fixture mixes incompatible direction inputs during the resize.

This is a concrete test-precondition mismatch supported by source and the failed offset assertions. The failed run has no retained-vertical PNG/JSON from that first failed iteration, because capture occurs after the assertions. The actual post-resize locale and exact callback sequence were not logged; no new installed reader-offset defect is established here.

A narrowly supported correction preserves the selected resource locale throughout controlled resize and callbacks, explicitly checks that precondition, and derives the independent expected RL/LR value from the test's fixed tag. Preserve the 0/47 offset, rail identity, repeated layout, focused-control, viewport and dismissed-callback assertions. Do not roll production back to a process-global direction or relax the offset equality.

## Legacy graphics scope

Robolectric4.14.1 selects native graphics only at API26+; its NativePaint also declares minSdk26. The legacy Paint shadow has synthetic text measurement and placeholder metrics. Thus the explicitly LEGACY API21/24 method cannot establish real positive glyph geometry. This explains why its geometry assertion is unsuitable for the intended API-branch guard; it does not establish the unlogged exact dimensions or any real-device rendering outcome.

A principled legacy successor checks resource-locale/API-branch behavior, opposing process-default direction selection and relevant text/scheduling behavior. Retain the twelve API30/35 native geometry, raster and lifecycle cases unchanged. Do not merely force dimensions, add padding or annotate unsupported native rendering to obtain green results.

Primary sources: [GraphicsShadowPicker](https://raw.githubusercontent.com/robolectric/robolectric/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/GraphicsShadowPicker.java), [ShadowPaint](https://raw.githubusercontent.com/robolectric/robolectric/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowPaint.java), [ShadowNativePaint](https://raw.githubusercontent.com/robolectric/robolectric/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowNativePaint.java).

## Status

The exact current JVM gate remains FAIL. These diagnoses do not turn four failures into passes. A separate reviewed test-only successor and fresh exact-source execution are needed to establish corrected fixture results. No production, wording, raster-tolerance or deadline change follows from this evidence.
