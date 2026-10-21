# API30 Manchu process-default locale failure

Read-only diagnosis of run 39540842251, core API30 job 119030652466, frozen merge 1c9b71afb5f5cbde39bc5fff70630bca1a7a3419 (tree 5fa767ed5bb57364a1ca4bd3cab95cae36187847). No source changes, tests, CI reruns, signing or publication performed.

## Verified finding

The failure is **process-wide `java.util.Locale.getDefault()`**, not the Activity resource locale. In `VerticalLocaleDeviceTest.assertCanvas`, the Activity resource assertion at line 384 and saved preference assertion at line 385 pass, then line 386 fails: expected `mnc-Mong`, actual `en-US`. The failing outer stage is the first landscape View-tab check in `checkLocale` line 167. No landscape Draw-tab tap follows.

Raw log sequence:

- 04:05:56.887 onward: Manchu portrait navigation and canvas assertions pass.
- 04:06:16.870: last explicit Save touch snapshot has `default=mnc-Mong activity=mnc-Mong target=mnc-Mong rootLocale=mnc-Mong application=en-US selected=mnc-Mong`.
- Portrait Cancel, Back and monitored Choose location complete; the final portrait assert at line 256 must have passed to enter the landscape iteration.
- 04:06:22.140: monitored external result pauses/resumes the same `ClassicPaintActivity@8e56c81`.
- 04:06:22.375: system landscape configuration is published with device `en_US`.
- 04:06:22.432: first landscape View tap.
- By 04:06:22.640: failure screenshot is captured and case ends.

There is no Activity recreation between selection and failure. Test lifecycle state uses the same live Activity; stale-reference evidence is absent. Screenshot retains Manchu vertical labels, consistent with the passed Activity-resource assertion, but does not certify all rendering.

The complete portrait export plus landscape failure capture is expected partial evidence after this assertion. It is not a transport-only failure.

## Comparison with successful 0.0.40

Prior core run 39452992495 at d664b3e72ea3261dba662119a429b0bb3914c04a passes both English and Manchu in the same order. Its Manchu landscape begins 2026-10-20 16:14:04.838. Its 16:14:13.496 Save snapshot also has `application=en-US` while default/Activity/preference are `mnc-Mong`.

Both use image fingerprint `google/sdk_gphone_x86_64/generic_x86_64_arm64:11/RSR1.240422.006/12134477:userdebug/dev-keys` and test-source SHA256 `38c02f3b7c9545742af8d26e68c1ad2ec2a29aa40a3a68ff0fac3b8580e9b617`. AppLanguage.kt, UiText.kt, ClassicPaintActivity.kt and VerticalLocaleDeviceTest.kt are unchanged between the inspected sources. The changed numeric filter adds U+2212 to accepted characters; it adds no locale mutation. This supports a pre-existing state/order susceptibility, not attribution to Czech text or minus handling. A previous pass does not invalidate this failure.

## Source-supported mechanism, not an observed caller trace

`PaintApplication.attachBaseContext` wraps once at startup. Later its configuration callback replaces only static `currentResources`. `AppLanguage.refresh` updates Activity resources and the Java default, not Application resources. Consequently Application resources can keep startup en-US while the editor has Manchu.

Android 11 ActivityThread recomputes the process LocaleList from Application-context resources. In configuration handling this occurs before the stale-sequence early return; equivalent changes can skip Application/Activity callbacks. A ViewRoot configuration callback also resets the locale before queuing configuration delivery. A late/redundant system update can therefore restore en-US without another production refresh. This is a plausible explanation matching the observed split, not proof of which framework callback fired in this run. No setter stack trace was captured.

Observed classification: an application-state invariant violation. No test-only Locale setter runs inside this vertical case; unrelated locale-restoring tests are outside this selected instrumentation shard. The exact timing trigger and persistence duration after failure remain unknown. Potential default-locale consumers include uiNumber, AdvancedColourDialog formatting, FontCatalog, and default overloads of LocaleTypography/VerticalText/GalleryTypography. Specific user-visible damage beyond the failed invariant is unproven.

## Minimal regression and repair scope

1. Add a deterministic SDK30 host regression starting with an en-US Application, then selecting Manchu in the already-running editor via production select/refresh. Check saved/public identity, Activity resource identity, Application-context resource identity, and default identity before invoking any helper that calls wrap/refresh.
2. After a real production Activity configuration callback, model the source-backed Android reset using the actual Application resource locale and the system LocaleList. Do not directly force en-US, call refresh as the oracle, or add sleeps. Assert the chosen public default still holds. This is a deterministic mechanism regression, explicitly not proof of Android event ordering. An actual ActivityThread configuration replay in a supported host framework harness would be stronger, if available.
3. Bound production repair to AppLanguage/PaintApplication locale ownership: keep the Application source consulted by Android synchronized with the current selection and preserve the public default after platform configuration processing. Updating only static currentResources is insufficient. Do not fix by weakening/removing the default assertion, mutating Locale in the test, or repeatedly retrying until green.
4. Cover Manchu, an ordinary decimal-comma locale such as French, switching back to empty device-default selection, and unsupported device-locale English fallback. Do not validate the empty preference as an app-catalogue tag or replace its true system identity with en-US. Existing device-default test checks only the picker label, not this lifecycle path.
5. Preserve the deliberate resource/public split: ko-Kore-KR uses ko-Kore-KR-anpaint resources; qaa-Zsye-XV uses en-Zsye-XV-anpaint resources but must retain qaa-Zsye-XV as public/default identity. A naive application-resources update can make Android copy the private qualifier into Locale.default, so both mappings need explicit regressions. Preserve live orientation, window dimensions/font scale, documents/selections/undo and API33+ LocaleManager authority.
6. Expand read-only failure snapshots to include Activity identity, Application identity/class, preference, public/default Locale and LocaleList, all relevant resource locales, configuration sequence/orientation, and callback entry/exit. That distinguishes a late callback reset from a transient assertion-observation window.

Existing AppLanguageTest:529–567 directly invokes Activity.onConfigurationChanged, and line 557 calls AppLanguage.wrap(activity), which itself resets the process default. It checks neither Application resources nor post-callback framework reset. Its successful direct callback test does not cover this defect. Existing vertical identity tests are at 389–405; device-default picker-label test is at 430–446.

Once repair/diagnostic execution is authorized, the smallest installed reproduction is the unchanged English+Manchu shard on API30 with the same prebuilt/source identity and normal 180-second cap, not an entire release rebuild. A deliberately added same-process switch/rotation regression can then exercise repeated transitions within its existing bounded test budget; any failure remains failure. A passing retry alone would not diagnose or erase attempt 1. No rerun was started here.

## Exact sources

- Failure oracle: https://github.com/c933103/AN-Paint/blob/1c9b71afb5f5cbde39bc5fff70630bca1a7a3419/app/src/androidTest/java/paint/anpaint/android/VerticalLocaleDeviceTest.kt#L383-L388
- Failing stage: same file lines 155–168; rotation readiness lines 270–278; setup/teardown lines 91–147.
- Application lifecycle: https://github.com/c933103/AN-Paint/blob/1c9b71afb5f5cbde39bc5fff70630bca1a7a3419/Paintroid/src/main/java/org/catrobat/paintroid/classic/UiText.kt#L13-L21
- Locale mutations: https://github.com/c933103/AN-Paint/blob/1c9b71afb5f5cbde39bc5fff70630bca1a7a3419/Paintroid/src/main/java/org/catrobat/paintroid/classic/AppLanguage.kt#L80-L114
- Existing host rotation coverage: https://github.com/c933103/AN-Paint/blob/1c9b71afb5f5cbde39bc5fff70630bca1a7a3419/Paintroid/src/test/java/org/catrobat/paintroid/local/AppLanguageTest.kt#L529-L567
- AOSP Android11 ActivityThread, exact retrieved blob 4cc486a0b9b4452d282cbfaabfa17782f567bdca, reset before stale-return and callback gating: https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r48/core/java/android/app/ActivityThread.java#L5785-L5830
- AOSP default-selection algorithm: same file lines 6362–6375.
- AOSP ViewRoot callback reset/queued delivery: same file lines 7387–7413.
- AOSP equal Activity configuration skips callback: same file lines 5646–5658.
- Canonical AOSP file: https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-11.0.0_r48/core/java/android/app/ActivityThread.java

AOSP line numbers and blob identity were verified with GitHub file-content reads, not inferred from browser-rendered line numbers. The source establishes Android11 behavior but is not a byte-level comparison of the emulator's framework binary.
