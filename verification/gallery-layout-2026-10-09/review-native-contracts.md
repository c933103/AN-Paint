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
