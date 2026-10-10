# Cross-language engineering propagation: first bounded pass

Base inspected: [`develop` at 9f15a0bc9140462214ddef4c020421a7848444e3](https://github.com/c933103/AN-Paint/commit/9f15a0bc9140462214ddef4c020421a7848444e3), 8 October 2026.

This is an initial engineering inventory and one notification-routing repair. It is not completion of the cross-language task, a re-acceptance of withdrawn localization audits, translation approval, or visual acceptance of every language. No catalogue wording, XML conventions, fonts, font licences, drawing-font choices or existing test thresholds change.

## Inventory and applicability

The picker currently declares **140 tags** in [`app_language_tags.xml`](../Paintroid/src/main/res/values/app_language_tags.xml). There are **143 default/localized `strings.xml` catalogues**. Picker membership is not the same as catalogue completeness or language acceptance.

| Shared engineering improvement | Applicability and present implementation | Further verification or propagation needed |
| --- | --- | --- |
| Locale identity, aliases and configuration | [`AppLanguage`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/AppLanguage.kt) handles tag aliases, saved preferences, Android 13 application locales, device-default labels and in-place resource refresh. These are shared paths for all picker tags, including horizontal, RTL and vertical profiles. | Existing selected migration/configuration tests are not an all-locale, all-OS runtime matrix. |
| Bundled glyph coverage | [`LocaleTypography.asset`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/LocaleTypography.kt) maps `vi-Hani`, `wuu-Hans` and Mong-script locales. [`test_locale_font_coverage.py`](../tools/test_locale_font_coverage.py) checks the actual cmap and inventory hashes. | Wu's fallback contains only U+20C8E; the Nôm font is catalogue-oriented. Neither promises arbitrary filename/user-text coverage. |
| Native control and popup font propagation | `LocaleTypography.install` handles text views, later descendants and spinner popup adapters; `EditorDialogBuilder` handles dialog roots; language-picker rows use each option's own font/script. Explicit drawing previews remain excluded. | Native `tooltipText` surfaces on tool/category/panel buttons are separate framework windows and have no explicit shared typeface/vertical-shaping installation. This is a source-level integration gap; actual hover/device effects are unverified. |
| Vertical shaping and column layouts | [`VerticalText`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/VerticalText.kt), [`VerticalUi`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/VerticalUi.kt) and ribbon widgets share clustering, shaping, orientation and column layout. Current vertical picker profiles are `mn-Mong`, `mnc-Mong`, `lzh-Hant`, `en-XV` and `qaa-Zsye-XV`. `mn-Cyrl-MN` remains horizontal. | [`AssemblyCanvas`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyCanvas.kt)'s empty-state instruction and [`PaintCanvas`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt)'s rotation caption bind the UI face but still use horizontal `Canvas.drawText`. Their direction-aware layout remains open. Unicode helper presence is not complete grapheme-conformance evidence. |
| Foreground feedback, lifecycle and accessibility | [`LocaleNotification`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/LocaleNotification.kt) supplies a font-capable in-app notice with dialog anchoring, non-intercepting touch behavior, timeout, live region, insets and deferred cleanup. The base selected only Nôm on API 30+. | This change includes the other configured **horizontal** UI font, Wu. All five vertical profiles remain excluded because this notice is a horizontal TextView. Vertical feedback needs a separate layout design and runtime checks. Background/application/detached contexts retain standard system toasts without a bundled-font guarantee. |
| Drawing-font isolation | [`FontCatalog`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/FontCatalog.kt) excludes `ui_only` fonts from drawing choices and preserves explicitly chosen drawing fonts. | Its default drawing-content fallback policy intentionally names particular scripts/fonts. Adding another UI font must not silently change the user's drawing-font selection. |
| Numbers, plurals and resource safety | Shared numeric parsing, quantity resources, normalization messages and [`test_translations.py`](../tools/test_translations.py) cover structural concerns such as placeholders, percentage literals, duplicate keys and picker/resource mappings. | Structural success is not linguistic accuracy, complete plural semantics or rendered-layout acceptance. Some technical/entry values intentionally use invariant formats; those need contextual review rather than indiscriminate localization. |

The automatic common code paths above do not need copies in each resource directory. The next pass should cover the concrete vertical canvas and tooltip gaps, then additional recent engineering changes and their language-specific runtime evidence. Open gallery/Commons PRs #19/#20 are not duplicated here. Translating newly introduced UI and completing incomplete languages remain separate work.

## Concrete repair: propagate modern foreground font binding to Wu

At the base, `LocaleTypography.showMessage` tested the literal Nôm font path. Wu already had a bundled UI fallback, but API 30+ feedback skipped that configured face and used a system-rendered toast.

The fixed Wu message catalogue has its U+20C8E (`𠲎`) occurrence in `ui_save_your_changes`, a confirmation dialog already covered by the existing font installer. **No current canned Wu toast is claimed to be missing that glyph.** The real variable-data route is Save feedback: `ClassicPaintActivity` formats `ui_saved` with the saved filename. A filename such as `𠲎.png` therefore needs the configured fallback in that foreground message too.

The predicate now requires API 30+, a horizontal UI direction, and a non-null configured typeface. With current mappings:

- `vi-Hani`: retains the existing Nôm foreground notice.
- `wuu-Hans`: gains the same foreground notice with the Wu fallback.
- The other 138 picker tags: retain existing feedback routing, including all five vertical profiles.
- The existing legacy API <30 installer, dialog anchors, background fallback, notification lifetime and drawing-font boundaries remain intact.

This guarantees carrying the existing configured face into the eligible notice, not coverage for every possible character. Android may already have some glyphs through device fallback; no uniform system-font absence is assumed.

## Regression coverage and limits

`LocaleNotificationTest` retains all existing cases and adds, for API 30 and 35:

1. The actual Wu `ui_saved` resource formatted with `𠲎.png`, preserving the complete message, bundled typeface and U+20C8E glyph.
2. Every declared picker tag, asserting the two eligible font routes and unchanged toast routing elsewhere, including all vertical profiles.
3. Wu dialog anchoring, dismissed/detached-anchor fallback and application-context fallback.

The source guard now requires the shared horizontal predicate, a configured font and the same visibility-aware notification call. Its legacy binding, lifecycle, inset, accessibility, dialog-anchor and Nôm cmap assertions remain. No test is deleted or skipped.

Local check results and exact-head CI status are recorded in the pull request. The added Android tests need the repository's normal resource-linked build/runtime execution; a host source check is not a substitute. No physical-device visual check or actual end-to-end save operation is claimed by these new notification tests.
