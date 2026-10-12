# Direction-fix JVM fixture correction

## Scope and observed failures

The two-test-file patch applies to the exact published da4b40bd47a5d76d45b21d86fdc59368b4b52fd2 tree ab6f5497e147e81d4c50f4954ea87f364be087aa, in the separate successor checkout. Frozen source and CI artifacts remain unchanged. No production, installed-test, font, resource, workflow, deadline or threshold changes.

The original JVM run has 906 executions: 902 pass and four failures. Preserve these actual failures:

- LocalizedDialogLayoutTest.retainedVerticalNoticeKeepsReadingOffsetAcrossRotation: API30 expected reader offset 0, observed 7757; API35 expected 0, observed 6564, both at old line 323. These numbers are the assertion's reading offsets, not recorded raw scrollX.
- UiDirectionContextTest.legacyResourceContextsDoNotNeedProcessDefaultOrApi24LocaleList: API21 and API24 fail the combined positive width/height assertion at old line 209. Exact dimensions and the individual failing widget were not recorded. Do not invent either.

Raw XML remains in /workspace/shared/anpaint-pr55-resource-direction-ci-20261012/regression/Paintroid/build/test-results/testDebugUnitTest/, with the two corresponding TEST-org.catrobat.paintroid.local.* XML files. The complete regression-job.log remains alongside the original artifact directory. The published da4 result is still a failed run; this patch has no fresh hosted result yet.

## Retained notice: fixture resource overwrite

The fixture mounts a plain Activity and localizes it once. Its old resizeDisplay later writes Resources.getSystem().configuration into that Activity, removing the selected resource locale. The new production direction contract reads that context correctly; the retained-notice oracle still cached a process-global direction. The real ClassicPaintActivity refreshes AppLanguage during its callback, unlike this plain fixture host.

Robolectric 4.14.1 ordering is explicit: [RuntimeEnvironment.setQualifiers](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/RuntimeEnvironment.java#L191-L237) first changes the display and then updates resources; [ShadowDisplayManager.changeDisplay](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowDisplayManager.java#L246-L250) drains the main looper. Thus the first notification still has the prior selected resources, but the old helper's second notification can traverse with the overwritten locale.

Correction: snapshot the full selected LocaleList; after setQualifiers, synchronously combine it with the new system geometry before the next display callback. Assert the complete list after restore, after the ViewRoot resize callback, and after final configuration dispatch. The retained-notice test additionally checks selected tag and full resource lists for Activity, dialog, root and both rails before/after callbacks. Expected RTL/LTR is fixed from the two test tags. Both reader offsets (0 and 47), both orientations, rail identity, window width, overflow, repeated-layout, body text and capture assertions remain exact. There is no manual scroll repair or forced child layout.

## Legacy Paint: supported behavior instead of an unsupported raster premise

Primary-source support, rather than an inference from the assertion alone:

- [GraphicsShadowPicker 4.14.1](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/GraphicsShadowPicker.java) chooses native graphics only from API26 onward.
- [ShadowPaint 4.14.1](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowPaint.java) uses synthetic length-based text measurement and placeholder integer font metrics, with no implementation of the floating-point font-metrics calls used by fontSpacing.
- [Android 5.0 Paint](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-5.0.0_r1/graphics/java/android/graphics/Paint.java#L1380-L1437) and [Android 7.0 Paint](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-7.0.0_r1/graphics/java/android/graphics/Paint.java#L1622-L1689) obtain fontSpacing from a native float metric method.
- [ClassInstrumentor 4.14.1](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/sandbox/src/main/java/org/robolectric/internal/bytecode/ClassInstrumentor.java#L574-L598) emits default-return bodies for instrumented native methods; [RobolectricGeneratorAdapter](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/sandbox/src/main/java/org/robolectric/internal/bytecode/RobolectricGeneratorAdapter.java#L50-L68) supplies 0f for float. This is source support for the unsuitable LEGACY font-metric premise, not a claim that the failed run logged numeric font metrics.

The replacement retains both SDK executions and actual widget construction/vertical measurement, but no longer certifies positive real-font geometry in LEGACY. It directly exercises API21 Configuration.locale and API24 Configuration.locales with fixed directions for lzh-Hant, mnc-Mong, en-XV, qaa-Zsye-XV and inverse horizontal en-US under an opposite process default. It checks complete text/content descriptions; each vertical widget must finish its preceding layout, clear observed scheduling/invalidation, then request layout and invalidate after a same-length text mutation. No fake font metrics or platform shadows are added.

All 12 API30/35 NATIVE mismatch/lifecycle executions and their shared helpers remain byte-identical. Their geometry, exact pixels, full attached accessibility, Save, rotation and recreation assertions stay in force. Because the revised legacy method now directly calls the new context overload, whole-class compilation against old production is no longer claimed; any old-production/new-test compatibility claim is limited to the unchanged native cases. No historical projection or counterfactual run was added.

## Local validation and remaining gates

Nine focused host tests pass normally and under python -O; git diff --check passes. All unchanged native methods/helpers were compared byte-for-byte against the baseline. Local Android compilation/JVM/native/device execution is unrun because this environment has no Android SDK. Fresh exact-successor CI is required; prior da4 installed passes do not give this successor a current-head pass.
