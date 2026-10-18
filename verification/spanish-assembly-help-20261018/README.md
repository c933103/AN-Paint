# es-ES assembly Help: bounded placement-mode correction

Base: `ec4d74eb222c58d51e4a339e43ca83cc7aa16ec3` (`develop`, includes German PR129).
Application head: `94869be423441fc943ff0b2eeb8dfe76036c83bb`.
Application tree: `e3ba7b23a38230f7820d148d5e99eaf364f7c20c`.
Corrected English reference: PR122 exact head `0d56dd970c22398f7fa032d1baee4a1b74c83f2b`.
Tracker: https://github.com/c933103/AN-Paint/pull/75

## Production scope

Only `Paintroid/src/main/res/values-b+es+ES/strings.xml` → `ui_add_up_to_20_images_with_android_s` changes in production. Four bounded edits distinguish snapping from exact placement and avoid promising gap filling:

- “Al encajar, la primera imagen empieza en el origen.”
- “No se permiten solapamientos al encajar.”
- New paragraph: “Selecciona una imagen y usa Posición exacta para establecer las coordenadas X/Y de su esquina superior izquierda en números enteros de píxeles, a partir de cero. Las demás imágenes mantienen sus posiciones y se permiten solapamientos.”
- “Las demás imágenes siguen colocadas; las imágenes unidas pueden desplazarse para ocupar el hueco.”

Every other production byte, XML attribute/entity and executable mode remains unchanged. The complete es-ES Help fixture is updated; its crop quantities and every other locale fixture remain identical. There are five changed application-tree files in total, with no additions or removals. Generic Spanish and es-419 routing are unchanged. PR56 and existing holds are untouched.

## Complete-entry review

The full entry was compared with the complete corrected English reference and its actual consumers. The independent pre-implementation linguistic/source review identified only the four corrections above; this record also preserves the implementer's full-entry comparison and source binding.

1. Import cap (20), Android file picker, thumbnails/names, dimensions after crop and normalization, provider-dependent modification times, and sorting without rearranging placement are retained exactly.
2. Thumbnail selection, single and batch crop, pixel/percent margins, handles or typed values, reset, non-destructive crops and Undo are retained exactly.
3. Long-press/drag snapping, translucent preview, top/left edge alignment and thumbnail-plus-target route are retained. Only origin and overlap rejection are scoped to snapping. The qualified crop sentence “Las imágenes unidas pueden desplazarse cuando se recorta su imagen principal.” is retained exactly.
4. The inserted exact-position paragraph uses the actual Spanish control label “Posición exacta”, top-left X/Y coordinates in nonnegative whole pixels, unchanged positions for other images and permitted overlap. It agrees with the existing separate Spanish position Help and the actual model/dialog.
5. Common width/height, each image's own aspect ratio, pixel/percent/minimum/maximum choices and restoring sizes while retaining crops are retained exactly.
6. Unplace returns only the selected image to the tray; other images remain placed and attached images may move. It no longer guarantees a filled gap. Remove, Undo/Redo, dragging, panning, pinch zoom and view-only Show all remain unchanged.
7. Direct PNG save, undoable transfer to Paint, conditional smaller output, memory warning if even a tiny output cannot fit, unchanged originals and local persistence are retained exactly.
8. Catrobat/AGPL and asset credits at the existing Archivo → Acerca de route are retained exactly, including XML `&gt;` encoding.

## Source and consumer binding

`source-bindings.json` records identical Git blobs at the base and English reference for AssemblyActivity, AssemblyPlacementDialog and ImageAssembly. The implementation changes no app code.

AssemblyActivity binds its real Help button to this complete resource, and its exact-position toolbar action opens AssemblyPositionDialog for the selected image. The dialog uses `ui_assembly_exact_position`, accepts finite nonnegative whole X/Y values and calls ImageAssembly.position. Position writes only the selected rectangle and converts directly attached children to their old absolute coordinates so other rectangles stay put; overlap is permitted. The snapping target for an empty assembly starts at zero and validateSnapPlacement rejects collisions. Unplacing an absolute anchor preserves the other positions; removing a snapped image may promote a child and reflow. Thus gap filling is conditional.

## Regression coverage and limits

The existing compiled-resource and actual Help-dialog methods require the entire es-ES string, now eight paragraphs. The complete crop plural/resource consumer checks remain unchanged. The new real Spanish toolbar/position test runs the same existing production-control regression as German, preserving its exact Spanish label and invalid-value message. It checks first absolute placement away from the origin, rejected negative/fractional X/Y, unchanged saved project on rejection and Cancel, valid zero, overlap with unchanged other rectangles, absolute Unplace retaining a gap, snapping origin/collision behavior, conditional snapped gap filling and Undo. Synthetic image fixtures are used; no user images or external providers are read.

The existing pre-Activity app-wide locale-resource refresh from PR129 remains intact, so toolbar construction uses the selected locale. No translated assertion was relaxed. The memory guard moves only es-ES from output paragraph index 5 to 6, preserving both exact conditional-memory assertions and all other locale indices.

The host whole-value oracle rejects the actual old Spanish value. One-time scope verification checks the four exact edits, five untouched paragraphs, unchanged fixture remainder, and all 1,209 files/modes against the complete base and candidate remote tree. This generated evidence stays on a separate ref, not in the application tree.

Resource/compiler checks are not runtime execution. Local Gradle/Robolectric is blocked while downloading Gradle 8.13 (`Network is unreachable`); hosted exact-head runtime results must be inspected separately. No whole-language, native-speaker, installed Spanish layout/glyph, enlarged-font or TalkBack acceptance is claimed. This bounded correction does not close PR75's broader obligations.

## Local results

- 933 full host tests pass normally and 933 with Python optimization.
- 13 focused checks pass in both modes.
- Complete resources/exact-script mirrors/link, structural catalogue validation and supplementary changed-test compilation pass.
- Local Gradle/Robolectric is blocked at the distribution download. Hosted exact-source runtime gates are tracked separately.

`checks.json` is the compact receipt. `local-evidence.zip` contains complete old/new/reference values, exact source bindings, scope/negative-control receipts, commands, raw local logs and the five-file application patch. This separate evidence ref preserves the complete application source tree. No APK, build output, credential or unrelated private data is included.
