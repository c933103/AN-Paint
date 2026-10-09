# Hint drawing and the host WebView measurement boundary

The second complete run passed the original attachment and rotation assertions,
then exposed two later fixture mistakes. Its [exact-head results](second-ci-47208ff/README.md)
remain failures; they are not reclassified as full layout acceptance.

## Measure the layout Android actually draws for a hint

`TextView.getTotalPaddingTop/Bottom()` deliberately use the normal edit buffer's
gravity offset. An empty one-line edit buffer and a wrapped multi-line hint can
have different heights. Comparing hint height against that normal-text remainder
incorrectly rejects a correctly measured hint.

The corrected hint-only branch follows the actual framework draw origin:
`extendedPaddingTop + getVerticalOffset(false) - scrollY`. It requires the entire
hint layout inside the padded view, final characters present, no ellipses and all
horizontal line bounds fitting. The actual text branch keeps its original stricter
`totalPadding` assertions unchanged. JSON records both layouts, padding, scroll
and draw-origin values. Neither control text size nor native layout is changed.

Exact platform references:
- [API30 TextView.onDraw](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r1/core/java/android/widget/TextView.java#L7411-L7456)
- [API35 TextView.onDraw](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/widget/TextView.java#L8653-L8698)
- [API35 normal-padding methods](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/widget/TextView.java#L2881-L2896)
- [API35 hint/normal gravity selection](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/widget/TextView.java#L7978-L8029)

## Keep a host model distinct from the installed browser

[Robolectric 4.14.1 ShadowWebView](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowWebView.java#L94-L150)
creates a provider whose ViewDelegate methods, including `onMeasure`, return a
no-op/default value. Thus the host cannot certify Chromium's real measured area.

A test-scoped shadow now applies Android View's default measurement contract to
that missing delegate. Final browser width/height MeasureSpecs must both be EXACT,
and the unchanged full-visible-bounds/reserved-area assertions still apply. No
positive minimum, control size, visibility or window bounds are fabricated: a
zero allocation from the production parent stays zero and fails. Native controls
continue to use their real Android measurement/rendering.

`GalleryViewportDeviceTest` independently tests the real installed WebView with
French/Mongolian, actual system font scale 2× and portrait/landscape same-Activity
rotation. It verifies the browser's full visible rectangle, no controls overlap,
reserved area, and retained search/browser objects and query. Locale and font
scale are asserted in the real Activity. The system font configuration is changed
and restored through emulator settings, never a test-only Resource font override.
A real configuration transition refreshes selected-language resources on API30.

The test reuses the accepted process-local rejecting proxy helper, verifies an
HTTPS CONNECT preflight, then uses local HTML only. It tracks galleries from
PRE_ON_CREATE, closes them before restoring the proxy, and fails closed if any
window survives. It restores the previous font scale and app language on failure.
The installed window measurements are logged as JSON in the emulator logcat.
It adds one ordinary-app case (18 ordinary, 94 total on API35) and leaves every
existing PR #19 path, test and 180-second deadline unchanged. The latest old-suite
154.401-second result is a timing reference, not proof the expanded suite fits.

Fresh CI must validate both halves and the runtime budget. Host screenshots alone
still do not show a real Chromium page; no physical-device/TalkBack/fluent-language
acceptance is claimed.

Local combined validation: 326 Python tests passed in 49.981 seconds, zero
failures/errors/skips (`logs/host-python-native-contract.log`). Android compilation
and the expanded installed case still require the next exact-head CI run.

## Installed-test preference isolation

Source review identified that the initial cleanup always wrote
`platform-initialized=true` and left a `language-tag` key. The former controls
AppLanguage's migration, so absence/false is meaningful. Cleanup now captures and
restores both keys' exact presence/value, independently from the original platform
locale list. It first settles real locale/font callbacks, which can otherwise
initialize those preferences, then restores and asserts the snapshot. Font/locale
restoration uses nested finally blocks so either failure still attempts the other.
The complete Python suite after this isolation follow-up passed all 326 tests in
51.618 seconds, zero failures/errors/skips (`logs/host-python-viewport-isolation.log`).

## Complete the host frame contract

The [third complete run](third-ci-9043849/README.md) passed all 1,680 native control
cases and the independent installed real-browser check. Its eight host reachability
failures still recorded zero browser width/height. The missing step was the frame:
`WebView.setFrame` delegates entirely to the same no-op provider. Measurement alone
does not update View's laid-out rectangle.

The test shadow now forwards the actual parent's `left/top/right/bottom` through
`WebView.PrivateAccess.super_setFrame`, Android's own provider-to-superclass bridge.
It supplies no alternate geometry. JSON records incoming frame, MeasureSpecs and
measured/actual dimensions, and all full-visible/reserve assertions remain intact.

Exact framework sources:
- [API30 setFrame delegate](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r1/core/java/android/webkit/WebView.java#L2937-L2943)
- [API30 superclass bridge](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r1/core/java/android/webkit/WebView.java#L2428-L2430)
- [API35 setFrame delegate](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/webkit/WebView.java#L2992-L2998)
- [API35 superclass bridge](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/webkit/WebView.java#L2450-L2452)

The real-provider evidence is the passing installed test, with its actual four
window/browser records retained in `third-ci-9043849/installed-viewport.json`.
The full corrected head still requires completed CI, including lint under the
unchanged deadline and remaining representative reachability/gesture checks.
