# Gallery Back follows the effective app locale

## Confirmed scope

Initial base: accepted develop `0b3d737e19448c47d36deee8cebfffd5d40c1ea3`, tree
`9a456494701a1e9fe46c401f389d16891f674311`. The corrected fixture also integrates
actual PR32 merge `43148951ac6bd23687e66685855909ac538ba004`, tree
`ab5ff7fe6d04d5e22348b979c9e0054eef9b1c0f`, preserving every disjoint accepted Help path.

The [production gallery button](https://github.com/c933103/AN-Paint/blob/0b3d737e19448c47d36deee8cebfffd5d40c1ea3/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L121-L124)
used a literal left arrow. The existing [Arabic host capture](https://github.com/c933103/AN-Paint/blob/29e04086e42c464585057bad119e0c50837fef34/verification/gallery-layout-captures-2026-10-09/fourth-ci-b37782d/reviewed-captures/api30-ar-font2.0-640x320-search.png)
was visually inspected: the navigation group is mirrored to the right, but its Back
button still points left. That is a historical Robolectric NATIVE capture, not an
installed device or a capture of this patch.

Android's [RTL guidance](https://developer.android.com/training/basics/supporting-devices/languages#Mirroring)
shows the Back arrow pointing right in the RTL counterpart and explains direction-aware
resources and drawables. The same page's [property-change guidance](https://developer.android.com/training/basics/supporting-devices/languages#UpdateLogic)
describes adapting custom UI to layout direction.

`AppLanguage.wrap` sets both locale and layout direction on the Activity's context.
The gallery's manifest handles rotation/window changes, but does not handle locale
or layout-direction changes in place. Those changes recreate its views. The arrow
therefore uses `resources.configuration.layoutDirection` when the gallery is built.
It has no language allowlist and applies to supported and device-default RTL locales.

The custom vertical row can use right-to-left **column ordering** even when the app
locale's horizontal layout direction is left-to-right. That is why this patch reads
the Activity configuration instead of `GalleryActions.layoutDirection`. It leaves
all vertical column layout, the horizontal arrow (`verticalCaption=false`), translated
accessible name, WebView history Back, and provider-home fallback unchanged.

No translations, provider behavior, fonts, system-font transition barrier, installed
fixture, CI workflow or archived evidence is changed. PR #32's 68 changed Help paths
at `80914c9e86111ead4f24bf8463dbdeddd0e43646` were inspected and are disjoint from this
patch. Its status was open and non-draft at inspection; its original draft label is
not treated as current status.

## Independent RTL oracle

The expected set is the intersection of the actual 140 picker tags with Unicode
[CLDR 45 likely subtags](https://github.com/unicode-org/cldr/blob/release-45/common/supplemental/likelySubtags.xml):
`ar`, `ckb`, `fa`, `fa-IR`, `ps`, `sd`, `ug`, and `ur` resolve to Arab; `he` and
`yi` resolve to Hebr. The Persian default is already `fa_Arab_IR`. Nearby controls
`ku`, `az`, and `uz-Latn` use Latin in these exact picker forms; regional or explicit
Arabic-script variants are different tags. Thus this is a script/tag assertion,
not an assumption that every variety of a named language has one direction.
Android documents Arabic/Hebrew RTL support in the primary guidance above, and its
[API35 TextUtils implementation](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/text/TextUtils.java#L2012-L2028)
defers locale direction to ICU. The test oracle is independent of the production
conditional and will not be changed merely to accommodate a failing runtime result.

## Verification contract

`GalleryBackDirectionTest` runs the production `MediaGalleryActivity` and actual
Android Button/accessibility/layout code under Robolectric NATIVE API30/35 configurations.
Its three methods produce six configured JUnit executions:

1. Every one of the 140 offered app tags at font scale 2.0, with an independent
   expected RTL set (`ar`, `ckb`, `fa`, `fa-IR`, `he`, `ps`, `sd`, `ug`, `ur`, `yi`).
   Checks direction, full horizontal arrow, >=48dp target, existing localized
   accessibility description, native button semantics, and vertical-row ordering.
   It exercises both history Back and provider-home fallback for every tag,
   rotating through all four providers, and retains the search query.
2. Arabic device-language configuration with explicit English, device default,
   Hebrew, then English app selection. This distinguishes device language from
   the effective app locale.
3. Explicit save/destroy/create Activity lifecycle for English→Arabic→English→Hebrew→English,
   restoring browser history and checking the new arrow and working Back each time with
   a fresh wrapped locale context. This does not independently establish delivery of a
   real framework-triggered locale recreation or a real OS setting change.


[ShadowWebView](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowWebView.java)
records load URLs and uses test-populated history. It sends no provider requests.
The tests exercise the production click listener against that offline model; they
are not Chromium history certification, installed-device execution, TalkBack
acceptance, language-fluency review, or all-language localization completion.

The fixture writes per-locale completed-case JSON and seven representative host
captures per API into `Paintroid/build/reports/gallery-back-direction/`, already
covered by the existing CI report upload. A JSON count or image alone is not a
passing JUnit result. Exact-head CI results and captures must be reviewed separately.
The fixture restores original preference presence/values, platform app locales,
application text resources and process locale.

`tools/test_gallery_back_direction.py` adds four source-only contracts for the
conditional, preserved listener/accessible description, recreation manifest and
test coverage. They are not runtime tests.

## Initial local status before publication

- Four focused source contracts pass: `local/source-contracts.log`.
- All 346 Python tests pass in 50.566 seconds: `local/python-tests.log`.
  Negative-test fixtures intentionally print unsuccessful instrumentation summaries;
  the encompassing unittest result is `OK`.
- The focused Gradle invocation could not start compilation. Downloading the pinned
  Gradle 8.13 distribution failed with `java.net.SocketException: Network is unreachable`.
  See `local/gradle-attempt.log`. No local JVM pass, lint pass, APK build or installed
  test result is claimed.
- `git diff --check` passes.

Reproduction: `python3 -m unittest discover -s tools -p 'test_*.py'`, then
`./gradlew --no-daemon --max-workers=2 --console=plain -PnativeAbis=x86_64 :Paintroid:testDebugUnitTest --tests org.catrobat.paintroid.local.GalleryBackDirectionTest`.
The normal exact-head PR workflow supplies the broader existing JVM/lint/build/API35
regression checks without modifying the completed font-barrier fixture.

## First hosted result and fixture correction

See [the preserved first-run record](first-ci-072bb73/README.md). The run compiled
all app/test APKs and passed lint and all 94 installed API35 checks, but failed two
of 722 JVM tests at the locale-recreation arrow assertion. The revised host lifecycle passed in the second run. Its auxiliary identity control
failed and is removed with its counterevidence preserved below; both runs remain failed.

## Corrected combined-head local checks

All 352 Python tests pass in 51.216 seconds against the accepted Help composition
plus corrected fixture (`local/python-tests-corrected-combined.log`).
Focused source contracts and `git diff --check` pass for this patch. Local Gradle remains unavailable
for the verified wrapper-network reason above; exact-head hosted tests are required.

## Verified second result and narrow diagnostic removal

The [second-run record](second-ci-f226b4d/README.md) preserves the actual JUnit
comparisons, complete suite inventory, all 140-locale results per API, and inspected
RTL/LTR/vertical host captures. Artifact retrieval is resolved via the supported
Sediment reference route, and both complete source ZIP hashes verify. The raw-log
Git blob upload remains separately paused.

All six production-view configurations pass. The only two second-run failures are
an auxiliary Resources-object-identity assertion, which disproves that particular
mechanism assumption. That diagnostic is removed; no production assertion is
weakened. The original synthetic helper mismatch is observed, but its precise
mechanism is not claimed as proven. Fresh exact-head CI/review remain required.

Final local check after removing only the invalid diagnostic: all 352 Python tests
pass in 50.770 seconds (`local/python-tests-final.log`).
