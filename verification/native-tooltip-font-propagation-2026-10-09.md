# Native tooltip configured-font propagation

Base: [`develop` at 441c8c8d03fcfa507097d3a61d9776579e6dd103](https://github.com/c933103/AN-Paint/commit/441c8c8d03fcfa507097d3a61d9776579e6dd103), 9 October 2026.

This is a bounded continuation of the [cross-language engineering inventory](cross-language-engineering-propagation-2026-10-08.md). It addresses a source-level font-propagation gap, not a reproduced current tooltip missing-glyph failure. No translation, resource XML, font asset, licence, drawing-font rule, workflow or existing test threshold changes.

## Scope and applicability

The framework creates tooltip windows outside the Activity view tree, so the ordinary `LocaleTypography.install` traversal cannot reach their message TextView. `LocaleTooltip` now supplies the existing configured horizontal UI face as a `MetricAffectingSpan`, with identical measurement and drawing updates. This carries the face through the native `CharSequence` path without replacing Android's tooltip window.

- The current applicable picker tags are `vi-Hani` and `wuu-Hans`.
- All other 138 picker tags retain their original tooltip text and routing.
- All five vertical profiles remain unchanged. A direction-aware tooltip needs a separate overflow design for the native popup's limited width, three-line maximum and ellipsis; this change does not flatten them into a new horizontal surface.
- Wu's current tooltip resources do not contain its fallback's U+20C8E. The test's `𠲎` is a font-binding fixture, not evidence of a missing current Wu tooltip glyph. The one-character fallback does not guarantee arbitrary user text.

All six assignments use the same setter:

1. Tool button labels.
2. Category descriptions, including selected tool and expand/collapse refresh.
3. Action icon labels, including Assembly Undo/Redo.
4. Editor panel button labels.
5. Pixel-grid help override.
6. Cursor Start/Stop refresh.

The setter guards the API26 tooltip call. Its custom span avoids the API28-only `TypefaceSpan(Typeface)` constructor. It preserves the incoming paint's style and other paint properties, original logical text and unrelated source spans. Reformatting replaces only its own spans and removes them if the next locale is inapplicable; caller-owned text is never mutated. Native null/empty clearing remains intact.

The patch adds no listener, overlay, timer, global-layout decorator, accessibility delegate or new user-visible wording. Existing editor help listeners still consume long press. Hover, unconsumed long press, native placement, timeout, detach and accessible show/hide remain framework-owned. `contentDescription` remains the original text.

## Regression coverage

- `LocaleTooltipTest`: API26, 27, 30 and 35 font/style binding for both measurement and drawing; native layout width/pixel comparison against the explicit configured face; unrelated spans, repeat formatting and locale transitions; all 140 declared picker tags through the setter, ToolButton, ActionButton and refreshed ToolCategoryButton; null/empty clearing.
- `LocaleTypographyApi21Test`: the guarded setter does not link API26 methods or change the existing content description/long-click listener.
- `LocaleTooltipWindowTest`: actual framework TooltipPopup on API30/35, delayed stylus hover, exit, timeout, pending detach, native long press, accessible show/hide, logical accessibility text, consumed-long-press suppression, null/empty clearing and popup detachment. Robolectric 4.14.1 does not model the separate mouse-cursor coordinates used in API35 hit testing, so this fixture supplies stylus pointer coordinates. Tests enter the real hidden ViewGroup hover dispatcher by reflection; they do not invoke popup-show directly or use a replacement popup/timer shadow.
- `LocaleTooltipControlsTest`: actual editor help paths, category selection, panel/pixel-grid text, cursor Start/Stop, header notification, locale/orientation rebuild and Assembly action popup detachment on API35.
- `test_locale_tooltips.py`: source wiring guard for the six assignments and single API guard; explicitly not runtime acceptance.

Local and exact-head CI results are recorded separately in the PR. Isolated native probes attach an archive containing the unchanged verified font assets, use the real formatter/span and native framework, and do not link the application's resources. These do not substitute for resource-linked control tests, API26/27 execution, lint, APK build, emulator checks or physical-device/screen-reader acceptance. A test corpus containing all picker tags is not full visual/semantic acceptance of every language.

## Platform references

- [Android View tooltip contract](https://developer.android.com/reference/android/view/View#setTooltipText(java.lang.CharSequence)): native long click unless consumed, delayed hover and null clearing.
- [AOSP Android 15 View implementation](https://raw.githubusercontent.com/aosp-mirror/platform_frameworks_base/android-15.0.0_r1/core/java/android/view/View.java): native tooltip scheduling, dispatch, accessibility and lifetime.
- [MetricAffectingSpan](https://developer.android.com/reference/android/text/style/MetricAffectingSpan): text measurement and drawing contract.
- [TypefaceSpan](https://developer.android.com/reference/android/text/style/TypefaceSpan): typeface constructor API boundary.
