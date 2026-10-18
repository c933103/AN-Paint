# French assembly Help: bounded complete-entry correction

Base: `702f0d8afa5bd5c950ec22ae14f29aecf4140482`, including German PR129, Spanish PR130, Italian PR131 and Portuguese PR132.
Corrected English semantic reference: PR122 head `0d56dd970c22398f7fa032d1baee4a1b74c83f2b`; the older develop English Help is not the corrected semantic reference.
Tracker: https://github.com/c933103/AN-Paint/pull/75

## Complete-entry review

The implementation independently compared all eight candidate paragraphs with the current consumers and corrected English reference. The separate full-value linguistic/source review is included as `linguistic-review.md`; neither review claims native-speaker acceptance.

1. Import: preserves the 20-image cap, Android picker, thumbnails/names, dimensions after crop/normalization, provider modification-time condition, sorting choices and no placed-image rearrangement.
2. Crop: preserves selection, individual and batch crop, pixel/percent margins, drag/type input, Reset, non-destructive operation and Undo.
3. Snapping: preserves hold/drag/drop, highlighted edges, translucent exact preview, top/left alignment rules, thumbnail-plus-target route and conditional movement when a parent is cropped. Only the origin and overlap sentences are qualified to target snapping.
4. Exact position: new complete paragraph names the actual “Position exacte” caption, top-left X/Y whole pixels from zero, unchanged other positions, and allowed overlap.
5. Dimensions: preserves common dimension, individual aspect ratio, Pixels/Percentage/Smallest/Largest choices, and Restore removing normalization while retaining crops.
6. Unplace/navigation: preserves the selected-image-only return to tray, other images remaining placed, Remove scope, pan/zoom/Show all behavior and unchanged output dimensions. Gap filling is conditional for attached images; the Undo/Redo sentence is grammatically corrected without changing the commands’ intent.
7. Output: preserves Save PNG, undoable Edit in Paint replacement, both distinct memory-limit branches, unchanged original files, local persistence and reopening.
8. Credits: preserves Catrobat/AGPL and the main-editor About/licences/credits reference.

Exactly one production value changes: `values-fr/strings.xml` / `ui_add_up_to_20_images_with_android_s`. The five untouched paragraphs and every other production byte, including the separate main-editor manual, are verified identical. All existing four-locale fixtures remain identical. The full old/new/corrected-English values and immutable consumer bindings are retained in the packet.

## Behavior coverage

The real Help path is `AssemblyActivity.showHelp` → `EditorDialogBuilder` → `AlertDialog`; no Help DialogFragment exists on this path. The three French JVM methods check complete compiled resources; the actual toolbar showing, dismissing and reopening the exact complete message; and the actual selected-image Exact position/Unplace actions. Selected French UI resources are bound before Activity startup, using the established four-locale test pattern.

The position case keeps the existing 15-second image-loading bound and all established assertions: first absolute placement away from the origin; negative/fractional rejection with unchanged project bytes/layout; Cancel; valid zero; overlap allowed while other rectangles stay fixed; absolute Unplace retaining a gap; snapping origin/collision rules; conditional attached gap filling; and Undo. Synthetic pixels/files avoid user-image/provider access.

Five new host checks enforce the full fixture, every-paragraph deletion rejection, missing/duplicate/truncated/attribute/markup rejection, precise placement-mode semantics, conditional crop and Unplace movement, actual caption references and P3 priority. The existing French memory guard moves from paragraph index 5 to 6 and retains both complete memory assertions. No source hashes or snapshot reconstruction are added as permanent test substitutes.

## Source preservation and limits

One-time evidence checks verify every original blob/mode, no removal, three added test/fixture files, and exactly two modified existing files. The final remote candidate tree is checked against all 1,212 reviewed source leaves before CI. Separate evidence refs are additive and retain the entire application source.

The separate French main-editor manual at line 465 still has unconditional gap-filling guidance and needs a separately bounded correction. PR75’s wider obligations remain open. No whole-language, installed French glyph/layout, enlarged-font, TalkBack or physical-device acceptance is claimed. PR56, locale routing, signing and unrelated project work are unchanged. Local compile checks and hosted execution are reported separately.

## Local results and publication

PR: https://github.com/c933103/AN-Paint/pull/133
Application head: `aeabd97550d82ea7bff9a0e3e9e5e06e906b2c57`
Application tree: `6b04626f3a0353ff6a417387e07db02b62db0651`
Hosted run: https://github.com/c933103/AN-Paint/actions/runs/39099580752

- 942 full host tests pass normally and 942 with Python optimization.
- 22 focused checks pass in both modes.
- Complete resources/exact-script mirrors/link, structural catalogue validation and supplementary changed-test compilation pass.
- Local Gradle/Robolectric is blocked at its distribution download. Hosted exact-source runtime gates are tracked separately.

`checks.json` is the compact receipt. `local-evidence.zip` contains complete old/new/reference values, both full-entry reviews, commands, source bindings, scope/negative-control receipts, raw local logs and the five-file application patch. Synthetic negative-test failures in the raw logs remain preserved. The separate evidence ref retains the complete application source tree. No APK, build output, credential or unrelated private data is included.
