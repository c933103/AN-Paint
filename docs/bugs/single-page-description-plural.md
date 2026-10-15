# Count-sensitive UI text uses fixed plural wording

**Status:** Open, low-severity UI-language bug group; documentation-only issue-style tracking PR, not an applied fix. Four independently confirmed occurrences of the same count-agreement cause are tracked separately below. Keep open/draft until each applicable checklist is verified through a separately reviewed implementation.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. **Verification boundary:** independent linguistic/static-source review only. No runtime/device reproduction, incorrect numeric counts, import/export failures or whole-language acceptance is claimed. [Project board](https://github.com/c933103/AN-Paint/pull/39) · [Translation tracker](https://github.com/c933103/AN-Paint/pull/56). Issues remain disabled; settings/visibility are unchanged.

## Expected and actual

Expected: labels for one item and multiple items use grammatical quantity wording without changing the true numeric count or workflow.

Actual: the resources below append fixed plural nouns/adjectives to counts that can equal one. Examples derived from the real formatting paths are “1 pages”, French “1 placées”, “1 images supplémentaires”, and “1 / 1 images”. Impact is low-severity incorrect displayed grammar; this does not establish wrong counts or lost data.

The existing document path retains the original page-description name so previous links stay valid. The scope now consolidates the four same-cause count defects rather than opening separate minor trackers.

## Per-key evidence and acceptance checklist

### 1. Page chooser: `formats22_page_description` (English/French)

- [ ] Correct the complete one-/multi-page descriptions while preserving type, filename, true count and selection controls.
- [EN L570](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L570) / [FR L595](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L595) contain unconditional `%3$d pages`.
- [ImportSelection.kt L55–60](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImportSelection.kt#L55-L60) calls `showPages` for every PDF/TIFF. [L98–101](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImportSelection.kt#L98-L101) accepts all positive counts and passes kind, name and count to the string. [PdfCodec.kt L110–112](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/PdfCodec.kt#L110-L112) permits one page.
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

## Shared fix rules and next action

Count-invariant labels can preserve current string APIs. Correct plural resources are an alternative if implemented end to end with proper locale quantities. Candidates above are proposed, not applied. Audit affected localized expressions and correct confirmed cases; do not rewrite already valid count-invariant languages for cosmetic uniformity.

Implement all four bounded resource corrections with per-path one/many controls, preserve placeholder types/indexes and line breaks, and complete current-source structural, focused behavioral and code-review gates. Independently review final complete values/context before replacing PR56 receipts. Coordinate with active assembly PR67 at the final integration source; this pinned evidence is not acceptance of later assembly changes. No app/resource/test/workflow change, merge or runtime fix is made by this tracking PR.
