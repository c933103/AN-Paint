# Device-language picker row: shared typography propagation

Base: `develop` at `5bf82b67199aaecbd341a8b150a887f8d60b5567`.
Scope: AN-W04, the shared native-control/font-propagation category from the existing seven-category inventory.

## Concrete source-confirmed case

1. The device locale is `mn-Mong` or `mnc-Mong`, while AN Paint explicitly uses `en-001`.
2. Open the app language picker.
3. Row 0 resolves the actual device-language `language20_device_default` resource, for example Mongolian `ᠲᠥᠬᠥᠭᠡᠷᠦᠮᠵᠢ ᠶᠢᠨ ᠬᠡᠯᠡ ᠶᠢ ᠠᠰᠢᠭᠯᠠᠬᠤ`.
4. Before this change, only its `textLocale` was set. The `position > 0` branch skipped its bundled face and vertical `ReplacementSpan`, although the matching explicit language option already used both.

This is a missing application of the existing row mechanism. It is not a claim that an arbitrary system Settings app offers every language, or that each device lacks the same system glyphs. Device locales in regression tests are controlled inputs.

## Bounded correction and applicability

Resolve the device locale once when opening the picker and use that same snapshot for its label and row typography. Resolve each row's own locale, then apply `VerticalUi.languageChoice` uniformly.

- All 140 offered tags go through the existing shared rules; no catalogue copy or translation change is needed.
- `mn-Mong` and `mnc-Mong`: device row gains the bundled Mongolian face and joined-word column treatment.
- `lzh-Hant`, `en-XV`, `qaa-Zsye-XV`: device row gains the existing vertical profile treatment.
- `vi-Hani` and `wuu-Hans`: device row gains its configured horizontal bundled font. No currently missing-glyph claim is made for these particular default labels.
- The remaining 133 offered tags retain normal horizontal rows and platform fonts, including RTL languages. Existing explicit-row treatment, ordering and radio semantics are unchanged.
- Regional/non-picker device tags keep Android resource resolution and the existing script-based font/direction rules. The patch neither rejects nor aliases a device tag nor invents a fallback language.
- The empty tag still means follow the device. Cancel does not select; selecting the already-active choice does not invoke the change callback.

No font/font licence, drawing-font selection, toast, tooltip, vertical-notice experiment, gallery work or PR #19 is changed. This increment does not establish full language fluency, complete glyph coverage, screen-reader acceptance or physical-device readability.

## Regression plan and current status

`DeviceLanguagePickerTest` adds:

- API30/35: an exact reconstructed pre-fix control (native single-choice adapter + `textLocale` only), alongside the repaired production row using the real device resource. The control has no vertical span; the repaired row must have one. This is an in-test before/after mechanism check, not a separate run of the complete old application.
- API30/35: all 140 offered tags as the device locale under a Japanese app override, checking label text, locale, shared font/span application, accessibility text/checkable state and explicit-row recycling isolation.
- API21/25: focused device-resource, font/span and override-switch checks in Robolectric legacy graphics. These do not claim native glyph/layout rendering. No additional shadow is installed.
- API30/35: regional and unknown device-tag resource fallback; repeated opens across Japanese, Arabic and English overrides; mounted rows at 16sp/24sp, a 48dp target, no ellipsis and layout fit. Native row PNGs are emitted under `classic-preview` for inspection.
- API30/35: cancel, follow-device, reselect-current and explicit-selection behavior.

Local `python3 -m unittest discover -s tools -p 'test_*.py'`: **310 tests passed**, 48.777 seconds. `git diff --check`: passed.

The chat-side host has Java 21 but no Android SDK, adb or cached Gradle distribution. Resource-linked Kotlin/JVM/native-rendering tests, Android lint, APK build and installed API35 regressions are therefore **not locally run**. The draft PR's normal CI will provide their actual results; publication is not a pass. No workflow or test threshold is changed.
