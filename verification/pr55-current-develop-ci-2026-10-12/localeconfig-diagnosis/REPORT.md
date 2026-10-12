# AN Paint localeConfig: version-bound, read-only diagnosis

## Finding

The exact default AGP 8.13.0 merger intentionally does **not inherit `android:localeConfig` from a library manifest**. It accepts the attribute from the application main manifest or a build overlay. AN Paint declares it only in the `Paintroid` library. This rule directly explains the observed absence in the delivered application manifest, subject to the CI execution limit below.

**Confirmed artifact fact:** the reviewed APK contains the correct 167-entry locale XML and picker arrays, but its application element has 12 attributes and no localeConfig binding. The previous and current APK manifests are byte-identical: 5,320 bytes, SHA-256 `652f94b8e56061f9b4342d258d6d5724717ce059726cf2426a0d56e08f677bdb`. This gap predates the latest integration.

## Exact version proof

1. The delivered matching-source archive pins `com.android.application` and `com.android.library` to **8.13.0** in root `build.gradle:34–35`. `Paintroid/build.gradle:22` applies the library plugin; `app/build.gradle:23,132` applies the application plugin and depends on `:Paintroid`.
2. Google's [AGP 8.13.0 POM](https://dl.google.com/dl/android/maven2/com/android/tools/build/gradle/8.13.0/gradle-8.13.0.pom) depends on builder 8.13.0. The [builder 8.13.0 POM](https://dl.google.com/dl/android/maven2/com/android/tools/build/builder/8.13.0/builder-8.13.0.pom) depends on **manifest-merger 31.13.0**. Both published `.module` metadata files independently agree for API and runtime variants.
3. Google's [manifest-merger 31.13.0 source archive](https://dl.google.com/dl/android/maven2/com/android/tools/build/manifest-merger/31.13.0/manifest-merger-31.13.0-sources.jar), SHA-256 `9ace7fab8c679ea3d9480f7e3be07c5a90e9770db9299afdb152203e6e3c738c`, contains:
   - `ManifestModel.java:345–346`: localeConfig uses `STRICT_MAIN_OR_OVERLAY_MERGING_POLICY`.
   - `AttributeModel.java:266–286`: that policy accepts only `XmlDocument.Type.MAIN` or `.OVERLAY`.
   - `ManifestMerger2.java:1276–1312`: dependency manifests are loaded as `.LIBRARY`.
   - `XmlAttribute.java:198–207,343–352,489–497`: a library-only value is recorded as `REJECTED`, yields null, and is not added to the higher-priority application element.
4. The library declares `@xml/app_locales` at `Paintroid/src/main/AndroidManifest.xml:5`; the application manifest lacks the attribute. The source archive scan found no `generateLocaleConfig` or runtime LocaleConfig override. `AppLanguage.kt` does set `applicationLocales`, which is a separate API.

The source JAR's SHA-1 also matches Google's published `.sha1` (`368768c53d2633d03c8b0c2adcaf39193282043e`). Its relevant duplicate ZIP entries have identical decoded bytes. Nothing downloaded was executed.

## Platform meaning and limits

Android's [per-app language guide](https://developer.android.com/guide/topics/resources/app-languages#use-localeconfig) says the manifest binding enables the supported-language list in system Settings. Setting `applicationLocales` changes the selected language; it does not replace that declaration.

In [Android 13 framework source](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-13.0.0_r1/core/java/android/app/LocaleConfig.java), LocaleConfig obtains the resource through ApplicationInfo and reports `STATUS_NOT_SPECIFIED` when the resource cannot be found (lines 92–108). [Android 13 Settings](https://android.googlesource.com/platform/packages/apps/Settings/+/refs/tags/android-13.0.0_r1/src/com/android/settings/applications/AppLocaleUtil.java) requires a nonempty successful LocaleConfig by default (101–112,143–153), alongside other app-eligibility checks. Its opt-in [feature flag defaults to true](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-13.0.0_r1/core/java/android/util/FeatureFlagUtils.java#109); disabling that flag permits a fallback to asset locales. [Android 14 LocaleConfig](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-14.0.0_r1/core/java/android/app/LocaleConfig.java#120) also honors a runtime override before manifest resources.

Therefore the static defect is confirmed and the default AOSP Settings consequence is source-backed. **No installed-device LocaleConfig result or Settings behavior was observed.** Do not state that the in-app picker is broken, that all devices hide the app, or that a production fix has passed.

The archived CI build log records the Paintroid and application manifest tasks running. The artifact set has no merger/blame report or resolved build-plugin classpath. Thus this is an exact-version source diagnosis consistent with the delivered result, **not a captured replay of that CI merger decision**.

## Smallest proposed fix and verification

For a separately authorized production change, put `android:localeConfig="@xml/app_locales"` on the **application module's** `<application>` element. Keep the curated XML unchanged. Enabling automatic generation would be a broader change and could change the advertised locale set.

Before claiming the gap fixed:
- Archive the application merger/blame report and the fresh APK/source pair.
- Assert the compiled application attribute resolves to the actual packaged `xml/app_locales`, with the intended 167-locale set still present.
- On a supported installed Android image, check `LocaleConfig` status and supported locale set, and inspect Settings. Check language selection and return-to-system behavior separately.

## Evidence packet

`official/` holds exact official metadata and Apache-licensed source; `EXCERPTS.txt` has numbered proof excerpts; `source-bindings.json` binds relevant project files directly to delivered source ZIP SHA-256 `96689be0a84822c75d51751b4889f6cd974ee68d009533a913fdc558a0163f4e`. The ZIP is linked by the existing artifact receipt to run `38296205283`, public head `b0697fd58a2a37fb94e351f4c4ec68757b0f6b5e`, tree `b5d8cbeac9bf6d613ed7c3be787aa984826daafd`. The supplied working directory's Git HEAD is older, so this diagnosis does not use its HEAD as the publication identity.

`checks.json` records read-only checks, including preservation of the frozen delivery packet. No project source or GitHub state was changed, no build or install was run, and no runtime observation is claimed.
