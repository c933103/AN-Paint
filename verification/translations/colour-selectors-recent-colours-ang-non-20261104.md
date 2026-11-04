# Old English and Old Norse colour selectors and recent colours

Base: `fcf6593617c105d3c1a7852e41ab5d9b74e92b75` on `review/nv-bottom-2038-20261103`.

## Change

Add 26 resources to each catalogue, covering advanced colour controls, spectrum and wheel descriptions, honeycomb swatches, four preset names, recent-colour gestures and foreground sampling. Ten standard numeric/RGB/HSV/HSL captions per language intentionally remain exact notation, not translated prose. Old English Gold is also naturally identical to the source.

The Android XML catalogues remain canonical. Colour values, model calculations, code, gestures and standard numerical conventions are unchanged.

## Context and review

- All directly referenced resources in `AdvancedColourDialog.kt` (40 keys) and `HoneycombPalette.kt` (2 keys) are present after this batch. The recent-colour and eyedropper consumers in `ClassicPaintActivity.kt` and `PaintDocument.kt` were also checked.
- The spectrum controls HSL hue and saturation with a right-hand lightness bar. The wheel controls HSV hue and saturation with a right-hand value bar. Translations preserve H/S and HSL L versus HSV V, with a functional instruction to drag the visible line marker on the right.
- Honeycomb wording describes the hexagonal colour cells and separate greyscale row. The hexadecimal caption identifies the colour, not the cell index.
- Recent-colour tap selects foreground; holding selects background. Empty slots remain explicitly empty. The eyedropper samples the image colour for foreground use.
- Presets keep the source names and exact values: Pale Violet FF5B67FF, Gold FFFFD700, Silver FFC0C0C0, Copper FFB87333. Colour-name compounds are modern technical adaptations, not historical RGB definitions or metallic-rendering promises.
- Independent review accepted all 52 entries unchanged, including hue/saturation distinctions, pale-violet wording, gestures, numerical labels and structural preservation.

## Verification

- All 78 host tests passed: translation, localized-help, translation-boundary, current-contract, language-note, string-importance, ordinary-priority and recovery suites. Reviewed output exactly matches those tested bytes.
- All 171 offered options passed structural validation with `require_complete=False`.
- XML parses with unique typed keys. Android escaping, source attributes, exact ordered typed placeholders and newline-escape runs pass. Previous 545 resources per locale, including the plural and its items, are unchanged; removing the added fragment restores original bytes.
- R/G/B and HSV/HSL identifiers, 0–255, 0–360°, 0–100%, and all four `formatted=false` percentage attributes remain exact. Six-digit uppercase hexadecimal zero-padding and ordered index/hex arguments were checked with host substitution examples.
- All 1,276 materialized base files match remote blob identities and modes. The 168 unmaterialized research/verification documents remain in the base tree. Only the two locale files and this evidence report are intended publication changes.
- Per locale: P0 stays 94/94; P1 stays 249/249; P2 rises 191→216/305; P3 rises 11→12/71. Each catalogue contains 571 typed resources: 570 strings and one plural. These counts measure direct resource presence, not whole-catalogue linguistic certification.

## Limits

No Android build/device, actual colour rendering, text fit, accessibility traversal, gesture execution, Android runtime formatting, CI or historical-language specialist certification is claimed. No issue1 action was attempted.
