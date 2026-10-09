# SVG rejection-message readability

Status: source inspection completed; added Android/Robolectric tests have **not
been compiled or executed in this workspace**. No screenshot, line-count,
clipping result, emulator pass or physical-device pass is claimed here.

Inspected baseline: `ea60a00001d766674cbd6b91da791894af5ea624` (PR #29).
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
renderer, would not establish vertical readability. This is a source-confirmed
missing transformation, **not a measured screenshot or a clipping observation**.
No clipping claim has been inferred from string lengths.

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
- System font scales 1.0 and 2.0, applied before creating the activity and asserted
  against its actual resources
- Readability assertions: French, Latin Hakka, Arabic, Nôm, Tibetan and Dzongkha
- Diagnostic captures only: traditional-script Mongolian and Manchu
- Both unusable-original-size and exceeding-bitmap-dimensions failures

The horizontal-readability test asserts complete text, final-line presence, no ellipsis, content width
and height, line bounds, full ancestor-visible bounds, persistence after five
simulated seconds and no Toast. It also asserts RTL layout for Arabic and the
bundled font/supplementary glyph coverage for Nôm. Assertions do not shorten or
substitute translations to get a passing layout. A failed layout remains a
failed test, while subsequent representative cases continue recording evidence.

A separate automatic method,
`verticalGalleryErrorsProduceDiagnosticCapturesWithoutLayoutAcceptance`, captures
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
It captures all five vertical locales at both scales and asserts that the native
status actually uses a vertical renderer before applying full-message geometry.
If the eventual design scrolls, add genuine scroll-to-every-column reachability
checks instead of dropping the renderer or final-content assertions.

## Local checks and limits

- `git diff --check`: passed for these changes.
- Java is available; Gradle, an Android SDK, `adb` and a populated Gradle cache
  are absent from the inspected workspace.
- No dependency bootstrap/build was attempted merely to simulate runtime proof.
- Host compilation/execution, PNG/JSON outputs, manual screenshot review and
  emulator/physical-device verification remain pending. An existing test failure
  elsewhere in PR #29 is not evidence that this new regression has run.
