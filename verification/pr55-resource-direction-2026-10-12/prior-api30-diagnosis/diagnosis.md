# API30 Literary Chinese Save failure: read-only diagnosis

## Finding

Fresh run 38279470164 fails after a real landscape writing-direction drift already visible **before** Save. The most strongly supported candidate is UI layout consulting the mutable process-default locale instead of the selected app/resource locale. A missed Save tap or autosave-at-UP is not established. No source, test, resource, workflow, timeout or remote state was changed during this diagnosis.

Source under review: published `43ab6622cdf6aac957a8d31cf2c5c20009e71d6e`, tree `592a60877524c5c118695cb45a4d0d5cd257b25a`, tested merge `e191c4660ef8709450df213cb75bd4bcf0810cb2`. The seven relevant files inspected match the delivered corresponding-source ZIP byte-for-byte; see `source-comparison.json`. The checkout's Git HEAD is its historical baseline, so it is not used as the published source identity.

## Observed evidence

- API30 XML: 95 selected methods, 94 passes, one failure. The two-method literary/emoji shard ran 100.196 seconds; the individual assertion is the unchanged 15-second `native vertical Save layout` wait, not a phase deadline.
- Fresh Literary Chinese portrait screenshot has vertical labels. Its last landscape workspace frame instead has horizontal tab/tool text and a horizontally laid-out status string clipped inside the retained vertical status rail. Actual pixels were inspected. The archived04 API30 landscape frame has vertical labels/status. `pixel-source-manifest.json` binds these frames; no image was edited.
- Fresh logcat lines 38494 and 38510 show the same status `FlowTextView` changing from 47×200 during rotation to 123×44 by the first View-tab selection. Subsequent warnings retain 123×44.
- At 16:57:58.930, Arrow ACTION_UP was observed with busy=false and draft=saved=37. File tap followed at 16:57:59.001. Save tap was requested once at 16:58:02.548 at Rect(148,164–199,194), 51×30. The 04 passing run used Rect(82,122–126,241), 44×119. The smaller height is consistent with ordinary horizontal Button measurement.
- No Save DOWN/UP/CANCEL observer, locale snapshot or Save-root presence snapshot was retained. `lastIoError` was null. Those omissions prohibit claims about exact delivered input, busy state at Save UP, or whether a horizontal dialog actually opened.
- The failed test catches the error and attempts a `-failure.png`, but `VerticalEvidenceExportRule.paths()` omits that filename. Only expected positive screenshots and reachability files are exported. Therefore no retained failure screenshot does **not** establish that no dialog opened.

## Source mechanism

1. `VerticalLocaleDeviceTest.assertCanvas()` accepts `activity.resources.configuration.locales[0] == lzh-Hant` and a shown `vertical_status_rail`. It does not check the direction currently used by child measurement/drawing.
2. `VerticalText.kt:19–27` defaults `uiDirection()` to `Locale.getDefault()`. `uiVertical()` derives from it. `RibbonWidgets.kt` re-evaluates these globals during FlowButton/FlowTextView measurement and drawing, as well as column scroll positioning.
3. `SaveOptionsDialog.kt:148` selects the existence of `vertical_save_form` from that process-default predicate. `EditorDialogBuilder` in `VerticalUi.kt` separately checks it again in a posted attach callback before creating `vertical_dialog_columns`. A valid horizontal Save dialog would therefore leave the existing vertical-layout wait false.
4. `AppLanguage.refresh()` updates activity resources, `PaintApplication.currentResources`, and the process default. `PaintApplication.onConfigurationChanged()` creates a newly wrapped resources object for `currentResources`; it does not replace the Application's existing base context.

Android 11 framework code provides a plausible later-reset route: `ActivityThread.handleConfigurationChanged()` and its `ViewRootImpl.ConfigChangedCallback` both update default locale from the Application context. The former does so before checking for an obsolete configuration sequence. `updateLocaleListFromAppContext()` calls `LocaleList.setDefault()`. See the [Android 11 ActivityThread source](https://android.googlesource.com/platform/frameworks/base/+/refs/heads/android11-release/core/java/android/app/ActivityThread.java), inspected blob `812ca4aefb9b01fb9c55a80a410ea8a04a5335d4`. [LocaleList.setDefault documentation](https://developer.android.com/reference/android/os/LocaleList#setDefault(android.os.LocaleList)) confirms it also changes the Java process default. **The actual callback that changed this run's default and its exact value were not logged.** This is a supported mechanism, not a claimed observed callback trace.

## Smallest justified candidate and verification

Use the rendering Context's resource locale for UI writing-direction decisions. Add explicit context-based `uiDirection(context)` / `uiVertical(context)` entry points while retaining the explicit-Locale mapping semantics. Handle API21–23 using the configuration locale rather than unguarded LocaleList access. Avoid changing AppLanguage selection, preference aliases, exact Korean resource routing, or default-locale mutation policy as part of this fix.

The minimum **complete failing-path** change must include more than SaveOptionsDialog: workspace/status construction in ClassicPaintActivity, dynamic FlowButton/FlowTextView measurement/drawing and ColumnScrollView in RibbonWidgets, SaveOptionsDialog content selection, and VerticalUi/EditorDialogBuilder's deferred mount/caption/spinner paths. Pass the same context-derived direction to wrapLabel/bounds/draw; otherwise its optional process-default argument can reintroduce drift. NumericSlider is present in the Save path and also needs its direction uses reviewed. There are additional UI clients elsewhere; migrate context-bearing direction calls consistently or explicitly state any remaining scope rather than silently changing the no-context helper's contract. Do not mechanically replace the pure Locale overload or explicitly localized language-picker rows.

Do not change bundled font selection or drawing-font semantics merely to fix direction. `uiTypeface(context)` currently also defaults to the process locale: it is an adjacent risk for Manchu/Nôm/Wu and should be explicitly tested/reviewed if changed, rather than smuggled into the narrow direction patch. Existing tests which set only Locale.setDefault must be converted to use an explicitly localized rendering Context only where the widget contract changes; retain their redraw/coverage assertions.

Required behavior regression, before/after candidate:
- Select a real app locale; keep the activity/resource locale fixed while deliberately setting a different process default. Assert vertical controls and both Save form/shell survive a fresh measure/draw and the deferred dialog mount.
- Cover all four vertical profiles, including LR and RL first-column expectations, plus a horizontal resource locale with a vertical process default as the inverse control. Expected direction should be fixed by the test case, not obtained from the production resolver being tested.
- Exercise rotation and recreation while preserving the selected locale and document. Introduce the mismatch **after** each configuration callback so AppLanguage.refresh cannot hide the regression by repairing the default first. Restore process defaults in finally.
- Keep the original native tap/swipe scenario and all full-text, accessibility, reachability, cancel/Back/positive-action checks. No longer deadline, blind retry or removed test.

Bounded installed telemetry should retain one pre-Save snapshot, read-only Save DOWN/UP/CANCEL events returning false, and a failure snapshot: process default, activity/root/application resource locale, selected preference, busy/draft/saved, target raw/visible bounds, saveRoot presence and separate form/column dimensions. Export optional failure screenshots without making them mandatory success evidence. This distinguishes horizontal dialog, rejected input and busy gating on the next exact-source run.

## Limits

This is a source/log/pixel diagnosis, not a reproduction or tested fix. No Android SDK is configured in this diagnosis environment. Fresh 43 remains failed; archived04's pass does not restore it. A successor must have a controlled old-fails/new-passes regression and exact-source installed validation before claiming repair.
