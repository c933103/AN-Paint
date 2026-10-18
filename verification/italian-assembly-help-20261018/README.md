# Italian complete assembly Help: bounded placement-mode correction

Base: `7ee75e4a1400587a775db420c1e1bebdbe88fa1d` (`develop`, includes German PR129 and Spanish PR130).
Corrected English reference: PR122 exact head `0d56dd970c22398f7fa032d1baee4a1b74c83f2b`; develop still has the older English entry.
Tracker: https://github.com/c933103/AN-Paint/pull/75

## Production scope

Only `Paintroid/src/main/res/values-it/strings.xml` → `ui_add_up_to_20_images_with_android_s` changes in production. The four edits are:

- “Quando si usa l’aggancio, la prima immagine parte dall’origine.”
- “Le sovrapposizioni non sono consentite quando si usa l’aggancio.”
- New paragraph: “Seleziona un’immagine e usa «Posizione esatta» per impostare le coordinate X/Y del suo angolo superiore sinistro, espresse in numeri interi di pixel a partire da zero. Le altre immagini mantengono le proprie posizioni e le sovrapposizioni sono consentite.”
- “Le altre immagini restano posizionate; le immagini collegate possono spostarsi per colmare lo spazio.”

Every other production byte, XML attribute/entity and executable mode remains unchanged. The full Italian Help fixture changes; every crop quantity and other locale fixture remains identical. The five-file patch has no additions or removals. No routing, PR56 or held-scope changes are made.

## Complete-entry review

The whole Italian entry was compared with the complete corrected English reference and actual controls/consumers. The preceding independent review selected exactly these four changes; this implementation also checked the complete entry and immutable source binding.

1. Import cap (20), Android file picker, thumbnails/names, dimensions after crop and optional normalization, provider-dependent modification times, and sorting without rearranging placed images are retained exactly.
2. Thumbnail selection, single/batch crop, pixel/percentage margins, handles or typed values, reset, non-destructive crops and Undo are retained exactly. Existing Italian control labels remain unchanged.
3. Long-press/drag snapping, semitransparent preview, top/left alignment and thumbnail-plus-target route remain. Only origin and overlap rejection are restricted to snapping. “Le immagini collegate possono spostarsi quando viene ritagliata l’immagine a cui sono collegate.” remains byte-for-byte intact.
4. New Exact position guidance uses the actual toolbar label “Posizione esatta”. Top-left X/Y coordinates, whole pixels from zero, unchanged other positions and allowed overlap agree with the existing Italian position-dialog Help and production model.
5. “Stessa larghezza”/“Stessa altezza”, each image’s proportions, “Pixel”/“percento”/“Più piccola”/“Più grande”, and restoring dimensions while retaining crops remain exactly as before.
6. Unplace returns only the selected image to the tray. Other images remain placed and linked images may move; gap filling is conditional. Remove, Undo/Redo, dragging, pan, pinch zoom and view-only “Mostra tutto” remain unchanged.
7. Direct PNG save, undoable transfer to Paint, conditional smaller output, memory warning when even tiny output exceeds the limit, unchanged originals, and local persistence remain unchanged. Both complete Italian memory-limit sentences now have a dedicated host paragraph guard.
8. Catrobat/AGPL and asset credits retain the existing “File > Informazioni, licenze e ringraziamenti” route and XML `&gt;` encoding.

## Source binding and regressions

`source-bindings.json` verifies identical blobs for AssemblyActivity, AssemblyPlacementDialog and ImageAssembly at the base and corrected English reference. AssemblyActivity’s actual Help button consumes this resource; its selected-image toolbar action opens AssemblyPositionDialog. The dialog accepts finite, nonnegative whole X/Y values and calls ImageAssembly.position. Position preserves every other rectangle by converting directly attached children to their former absolute positions. It permits overlap. Snapping starts at zero and rejects collision. Unplacing an absolute anchor preserves other coordinates; detaching a snapped image can promote a child and reflow, so the gap claim is conditional.

The full-value compiled-resource and real Help-dialog methods require the entire Italian entry, now eight paragraphs. Existing full crop-plural and batch-crop consumer checks stay intact. A new Italian test uses the existing German/Spanish production-control helper, with Italian label and invalid-value text. It checks first absolute placement away from origin, negative/fractional rejection with unchanged saved project, Cancel, valid zero, deliberate overlap without moving other rectangles, absolute Unplace retaining a gap, snapping origin/collision rejection, snapped gap filling and Undo. The German locale-initialization repair is preserved. Synthetic image fixtures do not read user images or external providers.

The full-value oracle rejects the actual old Italian entry. One-time scope checks verify the four exact edits, five untouched paragraphs, unchanged fixture remainder, all 1,209 file blobs/modes, and the complete candidate remote tree. Generated evidence belongs only on a separate source-preserving ref.

## Verification boundaries

Resource and supplementary compiler checks are not Android runtime execution. Local Gradle results and exact-head hosted gates are recorded separately. No whole-language, native-speaker, installed Italian glyph/layout, enlarged-font, TalkBack or physical-device acceptance is claimed. This bounded correction does not close PR75’s broader obligations.

## Local results and publication

PR: https://github.com/c933103/AN-Paint/pull/131
Application head: `13cdaf6f8cbf8a764c36aba6bd227f455cbaef8d`
Application tree: `38f4130f0452db1fab1477d0362cee0304d2fced`
Hosted run: https://github.com/c933103/AN-Paint/actions/runs/39093113728

- 935 full host tests pass normally and 935 with Python optimization.
- 15 focused checks pass in both modes.
- Complete resources/exact-script mirrors/link, structural catalogue validation and supplementary changed-test compilation pass.
- Local Gradle/Robolectric is blocked at its distribution download. Hosted exact-source runtime gates are tracked separately.

`checks.json` is the compact receipt. `local-evidence.zip` contains complete old/new/reference values, immutable source bindings, scope/negative-control receipts, commands, raw local logs and the five-file application patch. This separate evidence ref preserves the complete application source tree. No APK, build output, credential or unrelated private data is included.
