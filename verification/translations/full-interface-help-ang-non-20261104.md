# Old English and Old Norse: complete interface help

Base: `2e1b6b3e272d6b80e584134020a01ea07be9711b`.

## Scope and review

- Add the complete main-editor guide, eight-paragraph assembly guide and canvas-bounds hint to each locale: six authored help entries. Existing resources and application behavior remain unchanged.
- Independent linguistic and UI-context review accepted the batch with one Old English participle correction, applied before final checks. All other text was accepted unchanged.
- Preserve exact existing localized button/menu captions and paths, all eight assembly paragraphs and seven double-newline separators.
- Preserve navigation versus drawing; colour preview/confirm/cancel; save/export/share distinctions; selected image placement/original dimensions; draft plus both undo/redo histories; background-filled canvas expansion.
- Assembly preserves sorting versus placement; reversible crop; snap alignment/rejected overlap versus exact-position allowed overlap; each image's aspect ratio; retained crops; selected-only unplace/remove; view-only zoom; undoable main-editor replacement; smaller output only if offered; memory warning instead of chooser when even tiny output exceeds budget; unchanged source files and local persistence.
- Canonical Android XML owns current wording. No copied permanent prose catalogue or wording-freeze test was added.

## Checks

- 78 host tests passed across translation, localized-help, boundaries, current contracts, language note, importance, ordinary-priority followthrough and open-review recovery suites after correction.
- All 171 offered options passed structural validation. XML, source attributes, Android escaping, typed placeholders, exact newline escape runs and unique typed keys passed; all 692 previous resources per locale are unchanged. Every quoted caption/path component matches an existing localized resource.
- All 1,276 materialized base files matched remote contents and executable modes. The base tree contains 1,454 non-tree entries. The other 178 paths are research/verification records retained from the base.
- Per locale: P0 94/94; P1 249/249; P2 287/305; P3 62→65/71; typed resources 692→695. These are presence counts, not whole-catalogue linguistic acceptance.

## Remaining P2 assessment

All 18 remaining P2 entries are retained canonical resources, not declared unused. Exact-key inspection of 957 materialized text files found no direct production call sites or resource aliases targeting them. Both Paintroid and app modules were considered.

`UiText.kt` dynamically resolves canonical fallback/format contracts for an already supplied compiled ID, and `SourceTextResources.java` generates those resources from canonical values. Neither mechanism proves display of a specific retained key or justifies deleting it.

Concrete test consumers remain: `EditorDeviceTest.kt:455` uses `ui_lossless_jpeg_xl` to locate the lossless checkbox; sizing strings are used by `LocaleTextTest`/`LocaleTextBoundaryTest`; older attribution and colour-profile strings remain in semantic tests. The concrete JPEG XL translation should match the current `ui_lossless_format` template rendered with JPEG XL. Generic sizing signatures must not be replaced by incompatible newer fixed-axis signatures.

Recommended next translation groups: seven generic normalization entries, five format/export entries, four gallery entries and two interface/diagnostic entries. Preserve exact current source semantics and signatures, review independently and retain the entries. Static absence does not exclude dynamic/external consumers or establish dead code.

## Limits

No Android build, device, emulator, rendering, accessibility, runtime, CI, packaging/removal experiment or native-specialist acceptance is claimed. Historical-language computing terms are transparent modern adaptations. No issue 1 action was attempted.
