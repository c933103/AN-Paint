# SVG rejection-message readability

Status: CI at `c73ad1a` compiled and ran the tests; all four readability executions
failed at the 2.0-scale fixture precondition (the activity still reported 1.0).
Eight normal-scale PNG/JSON pairs were produced before those failures. The revised
scale setup below is source-checked and awaits fresh CI. No complete readability,
emulator or physical-device pass is claimed.

Initial inspected baseline: `ea60a00001d766674cbd6b91da791894af5ea624` (PR #29).
Only the additive test and this evidence directory are owned by this check.
Production UI and workflows were not changed.

## Display path and Android Toast limits

`MediaGalleryActivity.download` catches `SvgOriginalSize.SizeException`, resolves
its resource reason and wraps it with `ui_could_not_load_gallery_image`.
Its local `failure` function calls `showStatus` on the UI thread.
`showStatus` replaces the text in the activity's `gallery_status` TextView and
sets it visible. This status has no expiry callback or explicit two-line limit.
These two SVG rejections do **not** use `Toast` or `LocaleTypography.showMessage`.

Android's documented two-line text-Toast limit applies to apps targeting
Android 12/API 31 or later. It is relevant when evaluating Toasts elsewhere in
the app, but it is not the display constraint for these rejection messages:
[Android Developers: Toasts](https://developer.android.com/guide/topics/ui/notifiers/toasts).

## Concrete vertical-layout gap: separate AN-W04 scope

Source establishes all of the following:

- `VerticalText.uiDirection` requires vertical columns for `mn-Mong`, `mnc-Mong`,
  `lzh-Hant`, `en-XV` and `qaa-Zsye-XV`.
- `MediaGalleryActivity` constructs `gallery_status` as an ordinary `TextView`.
  It never calls `VerticalUi.caption` on it or replaces it with `FlowTextView`.
- The activity calls `LocaleTypography.install(root)`, which changes fonts but
  does not change text orientation, add column layout, install replacement spans
  or make this status scrollable.
- `GalleryTypography.script` applies writing-mode CSS to app-added controls
  inside the WebView. That CSS cannot affect the native status above the WebView.

Thus the status lacks the app's required vertical rendering path. A correct
vertical-reading assertion will fail that source condition. Retaining every
Unicode character in a horizontal TextView, or matching a standalone vertical
renderer, would not establish vertical readability. CI at `c73ad1a` now also
confirms this in native-rendered host output: Mongolian status has four/five
horizontal lines, an ordinary `TextView`, no replacement spans and no vertical
renderer. The API35 unusable-size PNG was visually inspected and shows that
horizontal rendering. This is not an emulator/physical-device screenshot. No
clipping claim has been inferred from string lengths.

The follow-on AN-W04 work should verify the real status in both column directions,
including the newly localized Manchu/Mongolian resource pairs, bundled Mongolian shaping,
full column reachability, large text and narrow/landscape windows. Any fix must
keep the gallery actions available and the error persistent. The candidate test
below is a starting regression, not complete acceptance of a future scroll design.

## Additive PR #29 host regression and diagnostic captures

`Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsSvgErrorReadabilityTest.kt`
uses the real activity, native Android resources/graphics, real SVG parser and
actual `IllustrationPage.USE_SCHEME` click handler. Only the download connection
is replaced with deterministic SVG bytes. The test never injects the displayed
message, replaces the status view, enlarges its height or sets its text size.

Matrix:

- API 30 and API 35 through Robolectric 4.14.1 `GraphicsMode.NATIVE`
- 320 × 640 dp portrait viewport
- System font scales 1.0 and 2.0 in separate method-level `@Config(fontScale=...)`
  environments, applied before application/resources/activity creation; system,
  application, language-wrapper and actual activity scale are all asserted
- Readability assertions: French, Latin Hakka, Arabic, Nôm, Tibetan and Dzongkha
- Diagnostic captures only: traditional-script Mongolian and Manchu
- Both unusable-original-size and exceeding-bitmap-dimensions failures

The horizontal-readability test asserts complete text, final-line presence, no ellipsis, content width
and height, line bounds, full ancestor-visible bounds, persistence after five
simulated seconds and no Toast. It also asserts RTL layout for Arabic and the
bundled font/supplementary glyph coverage for Nôm. Assertions do not shorten or
substitute translations to get a passing layout. A failed layout remains a
failed test, while subsequent representative cases continue recording evidence.

Two separate automatic normal/large-text diagnostic methods capture
`mn-Mong` and `mnc-Mong` using their newly integrated translations at both scales
on both APIs. It checks the real failure path, exact displayed resources, actual
font-scale enlargement, persistent status and absence of a Toast, then records
pixels and metrics. It deliberately makes **no vertical-rendering, clipping or
readability acceptance assertion**. A successful diagnostic capture is **not a
vertical-layout pass**, and it must never be reported as such. The proper failing
renderer candidate remains isolated outside test source sets. No English fallback
is assumed for these two resource pairs.

Each completed failure path saves the actual full activity rendering and line
measurements **before** acceptance assertions:

- `Paintroid/build/reports/svg-error-readability/*.png`
- `Paintroid/build/reports/svg-error-readability/*.json`

The JSON labels the render as native-rendered **host** evidence, not a device
capture. It records visible-area, final-character and content-height measurements
for diagnostic cases as well, and explicitly marks vertical acceptance pending. Passing geometry and glyph availability would still need screenshot
review for visual shaping/readability; they cannot certify translation quality.
The empty WebView area is expected in a network-independent Robolectric run.

Existing CI route (verified in source; no workflow modification):
`.github/workflows/android.yml` runs `:Paintroid:test${BUILD_VARIANT^}UnitTest`
and uploads `Paintroid/build/reports/` and test results even on failure.
This test is selected by that **host regression** task. It is not in
`src/androidTest` and is not selected by the emulator instrumentation route.

Focused execution on an Android-equipped build machine:

```sh
./gradlew --no-daemon --max-workers=2 --console=plain -PnativeAbis=x86_64 \
  :Paintroid:testDebugUnitTest \
  --tests org.catrobat.paintroid.local.CommonsSvgErrorReadabilityTest
```

## Isolated vertical regression candidate

`GalleryVerticalStatusRegressionCandidate.kt` is deliberately stored here,
outside all Gradle test source sets. It has **not** run and contributes no passing
or ignored-test credit to PR #29. A separately authorized AN-W04 fix can copy it
to `Paintroid/src/test/java/org/catrobat/paintroid/local/` alongside the fixture.
It defines separate `@Config(fontScale=1f)` and `@Config(fontScale=2f)` entry
points for all five vertical locales and asserts that the native status actually
uses a vertical renderer before applying full-message geometry. It follows the
corrected automatic setup; do not restore runtime scale changes inside a loop.
If the eventual design scrolls, add genuine scroll-to-every-column reachability
checks instead of dropping the renderer or final-content assertions.

## Observed c73ad1a run and fixture diagnosis

The recorded regression artifact SHA-256 is
`ea2a7e467da777967534c7b267507b8d346830543fec0c02e488ca5083d1a06e`.
The downloaded original artifacts were inspected without modification.
`TEST-org.catrobat.paintroid.local.CommonsSvgErrorReadabilityTest.xml` records
four executions/four failures, each `expected:<2.0> but was:<1.0>` at the actual
Activity scale assertion. Separate SVG translation-path tests record six passing
executions. This is a failed readability suite, not a partial overall pass.

The eight completed samples contain only French and traditional-script Mongolian
at 1.0 scale on API30/35 (two errors each). Both APIs record 28 px status text.
French uses four lines, 145 px status height. Mongolian uses five lines/261 px for
unusable size and four lines/212 px for excessive size. All eight JSON records
report their entire status visible and their layout fitting its content height.
These observations do not cover other locales, 2.0 scale or vertical acceptance.

### Source-supported cause

`PaintApplication.attachBaseContext` and `MediaGalleryActivity.attachBaseContext`
both delegate to `AppLanguage.wrap`. That method explicitly uses `fontScale=0f`
in its locale-only override. Android API30 and API35 only apply a delta font scale
when positive; zero does not request a return to 1.0. Thus the inspected production
wrapper does not contain the hypothesized default-scale reset:
[API30 Configuration](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r1/core/java/android/content/res/Configuration.java),
[API35 Configuration](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/content/res/Configuration.java).

Robolectric 4.14.1's runtime `setFontScale` updates system/application resources
and the manager configuration, but does not propagate configuration to every
cached locale-derived resource instance. Its update helper even documents the
missing resource-manager propagation. Reusing already-created wrapped resources
while switching from 1.0 to 2.0 is therefore an unsupported assumption in this
fixture, consistent with all four observed failures:
[RuntimeEnvironment 4.14.1](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/RuntimeEnvironment.java).
This diagnosis does not claim that large text has already passed on a device.

### Corrected setup, awaiting fresh execution

Each scale is now selected by method-level `@Config(fontScale=...)`, which
Robolectric applies before constructing the application and its resources:
[Config API](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/annotations/src/main/java/org/robolectric/annotation/Config.java),
[AndroidTestEnvironment](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/robolectric/src/main/java/org/robolectric/android/internal/AndroidTestEnvironment.java).
Four methods produce eight API-specific executions. No runtime call updates the
measured Activity's resources, no theme/locale wrapper is bypassed, and no text
size is injected into the status. A reset in the production wrapping path still
fails the retained scale precondition, now with checks at all four resource levels.

The glyph-enlargement requirement also remains: a normal-scale `TextView` is
constructed solely as an independent size reference, with the same manifest theme
and locale. The actual gallery status must be larger at 2.0 scale. Creating that
reference must leave the measured Activity's scale unchanged. Readability remains
measured on the real attached status and its ancestors, not on the reference view.
JSON output now separately records requested, system, application and activity
font scales for diagnosis. All message, width, height, clipping, glyph and
persistence acceptance assertions remain in place.

## Local checks and limits

- `git diff --check`: passed for the revised setup.
- Source/API checks confirm method-level fontScale support in pinned Robolectric
  4.14.1, distinct normal/large cases and preservation of the acceptance assertions.
- Java is available; Gradle, an Android SDK, `adb` and a populated Gradle cache
  are absent from this workspace. The revised tests have not been compiled or run
  locally; fresh CI is required. The previous CI compilation does not verify edits.
- Original c73ad1a PNG/JSON and JUnit artifacts remain unchanged.
- Full matrix rendering/review and emulator/physical-device verification remain
  pending. The separate vertical-renderer candidate remains unexecuted.
