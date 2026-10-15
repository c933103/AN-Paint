# Count-sensitive UI text uses fixed plural wording

**Status:** Open, low-severity UI-language bug group; documentation-only issue-style tracking PR, not an applied fix. Five independently confirmed occurrences of the same count-agreement cause are tracked separately below. Keep open/draft until each applicable checklist is verified through a separately reviewed implementation.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. **Verification boundary:** independent linguistic/static-source review only. No runtime/device reproduction, incorrect numeric counts, import/export failures or whole-language acceptance is claimed. [Project board](https://github.com/c933103/AN-Paint/pull/39) · [Translation tracker](https://github.com/c933103/AN-Paint/pull/56). Issues remain disabled; settings/visibility are unchanged.

## Expected and actual

Expected: labels for one item and multiple items use grammatical quantity wording without changing the true numeric count or workflow.

Actual: the resources below append fixed plural nouns/adjectives to counts that can equal one. Examples derived from the real formatting paths are “1 pages”, French “1 placées”, “1 images supplémentaires”, “1 / 1 images”, and “1 pixels”. Impact is low-severity incorrect displayed grammar; this does not establish wrong counts or lost data.

The existing document path retains the original page-description name so previous links stay valid. The scope now consolidates the five same-cause count defects rather than opening separate minor trackers.

## Per-key evidence and acceptance checklist

### 1. Page chooser: `formats22_page_description` (English/French)

- [ ] Correct the complete one-/multi-page descriptions while preserving type, filename, true count and selection controls.
- [EN L570](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L570) / [FR L595](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L595) contain unconditional `%3$d pages`.
- [ImportSelection.kt L55–60](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImportSelection.kt#L55-L60) calls `showPages` for every PDF/TIFF. [L98–101](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImportSelection.kt#L98-L101) accepts all positive counts and passes kind, name and count to the string. [PdfCodec.kt L110–112](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/PdfCodec.kt#L110-L112) permits one page.
- TIFF's one-page acceptance is explicit: [TiffCodec.kt L14,L30–31](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/TiffCodec.kt#L30-L31) delegates to native `pageCount`; [tiff_bridge.cpp L111–120](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/cpp/tiff_bridge.cpp#L111-L120) accepts any positive directory count up to the maximum, including 1; [JNI return L428–437](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/cpp/tiff_bridge.cpp#L428-L437) returns that count to Kotlin. This closes the source-link gap noted in [Codex review](https://github.com/c933103/AN-Paint/pull/74#discussion_r4278209260); no TIFF execution is inferred.
- Count-invariant candidates: EN `%1$s · %2$s\nNumber of pages: %3$d. Choose one page to edit as an image.`; FR `%1$s · %2$s\nNombre de pages : %3$d. Choisissez une page à modifier comme image.`
- Test actual one-page and multi-page PDF/TIFF chooser messages, preserving `%1$s`, `%2$s`, `%3$d` and Android newline escaping. Japanese `全%3$dページ` is a valid control, not a defect.
- [Independent French page review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182504034).

### 2. Assembly header: `ui_an_paint_image_assembly_20_images_placed` (French)

- [ ] Correct the French placed-image count for zero, one and multiple placed images without changing image or placement totals.
- [FR L197](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L197) ends `%2$s placées`; [AssemblyActivity.kt L128](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L128) passes `assembly.images.size` and `assembly.layout().size`, which can be one.
- Candidate complete FR value: `AN Paint · Assemblage d’images\nImages : %1$s/20 · Images placées : %2$s`.
- Preserve the two indexed string slots and newline; exercise the actual header after adding, placing, unplacing and removing images.
- [Independent French assembly review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182571039).

### 3. Remaining capacity: `ui_you_can_add_more_images_select_fewer_files` (English/French)

- [ ] Correct the capacity refusal for one remaining slot and larger remaining counts while retaining the selection-limit meaning.
- [EN L471](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L471): “You can add %1$s more images. Select fewer files.” [FR L525](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L525): “Vous pouvez ajouter %1$s images supplémentaires. Sélectionnez moins de fichiers.”
- [AssemblyActivity.kt L216–218](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L216-L218) compares selection size with `20-assembly.images.size` and formats that remainder. Nineteen existing inputs plus two selected files gives one remaining slot.
- Invariant candidates: EN “Number of images you can still add: %1$s. Select fewer files.”; FR “Nombre d’images pouvant encore être ajoutées : %1$s. Sélectionnez moins de fichiers.”
- Preserve `%1$s`, the 20-image cap and refusal behavior. Test the actual over-capacity branch at one remaining slot and other counts, with accepted-within-capacity controls.

### 4. Rendering progress: `ui_rendering_images` (English/French)

- [ ] Correct the one-image and multi-image progress messages without changing progress values or output generation.
- [EN L324](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L324): `Rendering %1$s / %2$s images…`; [FR L410](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L410): `Rendu de %1$s / %2$s images…`.
- [AssemblyRenderer.kt L56–64](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyRenderer.kt#L56-L64) filters placed entries and calls `progress(index+1,entries.size)`. One placed image yields 1/1; [AssemblyActivity.kt L317](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L317) formats the message from that callback.
- Invariant candidates: EN `Images rendered: %1$s / %2$s…`; FR `Images rendues : %1$s / %2$s…`.
- Preserve both indexed string slots; exercise actual one- and multi-image progress callbacks, successful output, and existing failure cleanup.

[Independent French remaining-capacity/render-progress review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182642343) supports cases 3–4.

## Fifth occurrence: dimension summary `ui_d_d_px_d_pixels_2f_mp` (English/French)

- [ ] Correct one-pixel and multi-pixel summaries without changing dimensions, counts, grouping or precision.
- [EN L133](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L133) and [FR L275](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L275) contain `%1$d × %2$d px · %3$,d pixels (%4$.2f MP)`. A valid 1×1 image yields “1 pixels”. [ImageImport.kt L13–16](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageImport.kt#L13-L16) admits positive dimensions and formats their product; [DimensionControls.kt L55–75](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt#L55-L75) accepts dimensions of one and displays `target.describe()`. [ClassicPaintActivity.kt L1005](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1005) installs these controls in New/Resize dialogs.
- Independently agreed complete candidates: EN `%1$d × %2$d px · Pixel count: %3$,d (%4$.2f MP)`; FR `%1$d × %2$d px · Nombre de pixels : %3$,d (%4$.2f MP)`.
- Preserve the four indexed numeric contracts, including the grouped long count `%3$,d` and decimal precision `%4$.2f`. Test real New/Resize controls at 1×1, multiple pixels and a grouped large count, and retain invalid/zero-input behavior. Japanese [L323](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L323) uses count-invariant counter wording and is not a singular defect.
- Both the French reviewer and independent source reviewer confirmed this fifth case after the initial four-case record. The source was re-read; no UI execution is claimed.

## Explicit regional-English overrides

[Expanded-head review](https://github.com/c933103/AN-Paint/pull/74#discussion_r4278250038) identified explicit overrides that a default-only correction would miss. At the pinned baseline, [en-AU](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-en-rAU/strings.xml), [en-CA](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-en-rCA/strings.xml), [en-GB](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-en-rGB/strings.xml), [en-IN](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-en-rIN/strings.xml), [en-SG](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-en-rSG/strings.xml), [en-US](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-en-rUS/strings.xml) all redeclare the same affected values: `formats22_page_description` at L563, `ui_you_can_add_more_images_select_fewer_files` at L468, `ui_rendering_images` at L321, and `ui_d_d_px_d_pixels_2f_mp` at L130. Each file was read and these exact values verified.

- [ ] Correct or deliberately remove each of the 24 broken regional overrides so the six offered locale options cannot retain the old wording; preserve regional distinctions unrelated to these keys.
- [ ] Run the actual one/many page, capacity, render-message and pixel-summary controls under default English and all six regional English locales, plus the French affected cases. Verify actual resource selection/fallback, not just default XML edits.

This named scope supplements the audit of other localized expressions. Later clean review summaries do not erase an earlier unresolved substantive finding; this section explicitly addresses that gap.

## Shared fix rules and next action

Count-invariant labels can preserve current string APIs. Correct plural resources are an alternative if implemented end to end with proper locale quantities. Candidates above are proposed, not applied. Audit affected localized expressions and correct confirmed cases; do not rewrite already valid count-invariant languages for cosmetic uniformity.

Implement all five bounded resource corrections with per-path one/many controls, preserve placeholder types/indexes and line breaks, and complete current-source structural, focused behavioral and code-review gates. Independently review final complete values/context before replacing PR56 receipts. Coordinate with active assembly PR67 at the final integration source; this pinned evidence is not acceptance of later assembly changes. No app/resource/test/workflow change, merge or runtime fix is made by this tracking PR.
