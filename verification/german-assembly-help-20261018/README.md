# German assembly Help: bounded correction and full-entry review

Base: `d47ae81a7dca1ab562ab0e8b276b13c24a374cee` (`develop`).
Application head: `4e3816f82cabd73295a06acaac75a304504f871b`.
Application tree: `72dd7be2cdd28486a0f8347e73f16ae13b25c4f2`.
Source request: https://github.com/c933103/AN-Paint/pull/75#issuecomment-6243771594
Corrected English reference: PR122 exact head `0d56dd970c22398f7fa032d1baee4a1b74c83f2b`.

## Production scope

Exactly one value changes: `Paintroid/src/main/res/values-de/strings.xml` → `ui_add_up_to_20_images_with_android_s` (P3). All other production bytes, values, XML attributes/entities and modes remain unchanged. The full expected German fixture changes with it; no crop plural or other-language fixture changes. Application code is unchanged. PR56 and all existing holds remain untouched.

The new wording is exactly the prepared comment:

- “Beim Einrasten beginnt das erste Bild am Ursprung.”
- “Beim Einrasten werden Überlappungen abgelehnt.”
- New complete paragraph: “Wählen Sie ein Bild aus und legen Sie mit «Exakte Position» die X- und Y-Koordinaten seiner oberen linken Ecke in ganzen Pixeln fest. Die Koordinaten beginnen bei null. Die anderen Bilder behalten ihre Positionen, und Überlappungen sind erlaubt.”
- “Die anderen Bilder bleiben platziert; verbundene Bilder können sich verschieben, um die Lücke zu schließen.”

The earlier sentence “Verbundene Bilder können sich verschieben, wenn ihr übergeordnetes Bild zugeschnitten wird.” is retained verbatim. The paragraph structure increases from seven to eight solely by inserting the Exact position paragraph after snapping.

## Complete-entry comparison

All eight resulting paragraphs were compared with the complete corrected English reference, rather than checking isolated substrings:

1. Import limit, Android picker, thumbnail/name/dimensions/mtime tray details, provider-dependent times and sorting without changing placement: unchanged and retained.
2. Selection; single and batch crop; pixel/percent margins; handles and typed values; reset; nondestructive undo: unchanged and retained.
3. Long-press/drag edge snapping, translucent result, right/top and bottom/left alignment, thumbnail-plus-target route: unchanged. Origin and rejection now explicitly apply to snapping. Conditional attached-image crop movement is retained exactly.
4. Exact position: selection, actual German control name “Exakte Position”, top-left X/Y, whole pixels starting at zero, unchanged other positions and allowed overlap match the separate existing German position guidance and actual dialog/model. No claim that arbitrary negative or fractional coordinates work.
5. Same width/height preserve each image's aspect ratio; pixels/percent/min/max choices; restoring sizes retains crops: unchanged and retained.
6. Unplace returns only the selected image; other images remain placed; attached images may move to close the gap. This avoids promising movement or gap filling for independent absolute placements. Remove, undo/redo, dragging, panning, pinch zoom and view-only Show all remain unchanged.
7. Direct PNG output and undoable Paint transfer; a smaller copy only if offered; memory warning when even a tiny output cannot fit; unchanged originals; local assembly restoration: unchanged and retained.
8. Catrobat/AGPL and resource credits at the existing German About/licences/credits route: unchanged, including XML `&gt;` encoding.

## Consumer/source semantics

`AssemblyActivity.kt` selects the current image for `AssemblyPositionDialog` and shows this full resource from its real Help button. `AssemblyPlacementDialog.kt` uses `ui_assembly_exact_position`, parses X and Y as finite whole nonnegative values, and calls `ImageAssembly.position`. The source consumer files are byte-identical at the base and corrected-English reference, recorded in `source-bindings.json`.

`ImageAssembly.position` writes only the selected image's requested rectangle; direct attached children become absolute at their old rectangles, preserving descendants. Exact placements may overlap. `targets` offers the origin for an empty snapped assembly; `validateSnapPlacement` rejects collisions. `detached` preserves other rectangles for an absolute anchor, while a snapped image may promote a child and reflow, so gap closing is conditional.

## Regression scope

The existing real Help test still asserts the entire compiled Help value and closes the actual dialog, now with eight paragraphs for German and seven for the other three untouched locales. The full compiled-resource and real crop-warning consumers remain active.

A new German actual-toolbar method checks the existing control label, first exact placement away from the origin, rejected negative and German fractional X/Y values, unchanged project bytes on rejection and Cancel, valid zero, overlap with unchanged other rectangles, absolute Unplace retaining the gap, snapping origin and overlap rejection, snapped Unplace moving its successor, and Undo. The test uses synthetic images only. These are authored regression assertions; a supplementary compile is not runtime execution.

Twelve focused host tests validate complete strings/structure and new mode-specific wording. The unchanged full-value corruption controls remain. The actual old German value fails the current whole-value oracle. The complete base and candidate trees are verified by path, Git blob and executable mode (1,209 retained leaves; five edited files).

## Limits

No native-speaker, installed-device layout, raster/glyph, TalkBack, complete German catalogue, or other-language acceptance is claimed. This repairs the bounded Help entry; broader tracker obligations remain open. Local full Gradle/Robolectric execution is blocked by a network-unreachable Gradle distribution download. Hosted exact-head build/JVM/lint/API35 results must be checked independently.

## First aggregate check and repair

The first full host runs found two failures in the existing German memory guidance guard: it hardcoded paragraph index 5, which now points to Unplace after the new paragraph is inserted. Both required memory phrases are unchanged in index 6. The bounded repair updates only the German index; all other locales and both exact memory assertions remain unchanged. Initial logs are retained, and final full-suite reruns supersede them.

## Exact-head Codex review

Codex completed its code review of `4e3816f82cabd73295a06acaac75a304504f871b` at 2026-10-18 00:54:52 UTC with no findings: https://github.com/c933103/AN-Paint/pull/129#issuecomment-6243946687. This review does not substitute for the pending hosted JVM/build/device gates.

## Final local results

- 932 full host tests pass normally and 932 with Python optimization.
- All 12 focused checks pass in both modes.
- Complete resource compile/mirror/link, catalogue validation and supplementary changed-test compilation pass.
- Local Gradle/Robolectric remains blocked at the distribution download; this evidence does not turn a compiler pass into runtime execution.
- [Exact-head hosted run](https://github.com/c933103/AN-Paint/actions/runs/39084426999) and [Codex review request](https://github.com/c933103/AN-Paint/pull/129#issuecomment-6243934992) are tracked separately.

`checks.json` is the compact machine-readable result. `local-evidence.zip` contains full old/new/reference values, precise source bindings, scope/negative-control receipts, raw passing and failed local logs, commands, and the five-file patch. It contains no APKs, generated binaries or unrelated private data. This receipt lives only on a separate evidence ref, retaining the complete application tree unchanged.
