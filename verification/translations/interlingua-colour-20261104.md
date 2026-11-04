# Interlingua saved palettes and colour controls

## Scope and review

- Base: `73b85c2b9cc6e13ad5cca4159d39b4e6146499e4` on `review/nv-bottom-2038-20261103`.
- Add 42 Interlingua resources: 41 P2 and one P3. All 387 previous resources remain unchanged, including existing palette-add and Advanced captions.
- Independent linguistic and UI-context review accepted all 42 unchanged. Canonical wording is in `Paintroid/src/main/res/values-b+ia/strings.xml`.
- Cover saved/recent palette actions and slots, honeycomb layout, spectrum/wheel controls, colour presets, numeric ranges and foreground sampling. Actual mode, palette and recent-colour consumers were inspected in `AdvancedColourDialog.kt`, `HoneycombPalette.kt` and `ClassicPaintActivity.kt`.
- Preserve add/edit/replace/remove distinctions, full-palette replacement choice, stored/empty/selected slots, recent-colour tap-foreground/hold-background gestures, honeycomb greyscale row and HSL L versus HSV V meaning. Retained `colour20` strings are translated against source and their dynamic caption stem without claiming current direct consumers where absent.

## Validation

- 78 host translation/localization tests passed.
- Structural validation passed for all 171 offered language options.
- 84 Java resource render checks passed across English and Interlingua: 76 formatted-resource checks and eight literal-resource checks, including static labels.
- All ten standard numeric RGB/HSV/HSL labels remain source-identical, including four `formatted=false` resources. Typed argument order, `%06X` width/case, degree/percent signs, source attributes, numeric ranges and newline structure are preserved.
- XML parses and all previous entries remain unchanged. The shortened replacement instruction matches the dynamic replacement-caption prefix.
- Base snapshot verified: 1,252 materialized files and modes match the parent tree; 227 unmaterialized base entries are retained through the unchanged Git base tree.
- Interlingua now contains 429 typed resources: P0 94/94, P1 249/249, P2 85/305 and P3 1/71. The remaining priority gap is 290 keys.

## Limits

This is bounded translation and structural evidence, not whole-catalogue linguistic acceptance, native-specialist certification, Android/AAPT compilation, device or emulator testing, layout/accessibility runtime verification, or CI acceptance. No issue 1 retry was made.
