# Old English and Old Norse text styling and vertical layout

Base: `57aed76951efc59913f90c48574205a822a14ec4` on `review/nv-bottom-2038-20261103`.

## Change

Add 24 string resources to each catalogue: 23 translated labels/help strings plus the intentionally unchanged multilingual preview sample `Aa Bb 0123 · あいう`. The block covers all nine system font-family choices, strikethrough, text-background fill, horizontal/vertical layout, column order, glyph orientation, vertical alignment, text-placement help and the font-notices button.

The Android XML catalogues are the canonical wording. No font IDs, bundled font names, renderer code or legal texts change.

## Context and review

- All directly referenced resources in `FontCatalog.kt` (9 keys) and `TextStyleDialog.kt` (33 keys) are present in both resulting catalogues. `PaintDocument.kt` consumes the text-placement help.
- Font descriptions distinguish serif terminal strokes, their absence in sans-serif families, equal-width character space, light/thin/medium stroke weights and condensed width. Cursive/casual use descriptive modern adaptations of the existing catalogue's historical-language vocabulary.
- `VerticalText.kt` context was checked: top-to-bottom writing is separate from right-to-left or left-to-right column order; sideways words retain joining-script shaping; upright characters keep combining marks and emoji sequences together; newlines start new columns. Background fill covers the text bounds rather than the whole canvas.
- Independent review accepted the block after a Norse hint clarification explicitly separated keeping emoji sequences together from keeping combining marks with their characters. The correction is applied.
- The font-notices caption opens the existing `legal/FONT_NOTICES.txt` asset. It is not acceptance of a licence or a permission request. The multilingual sample remains exact.

## Verification

- 78 host tests passed after the final correction: translation, localized-help, translation-boundary, current-contract, language-note, string-importance, ordinary-priority and recovery suites.
- Structural validation passed for all 171 offered options with `require_complete=False`.
- XML parses with unique typed resource identities. Android escaping, source attributes, typed/ordered placeholder parity and exact newline-escape runs pass. This block has no format arguments or newline escapes.
- All previous 521 resources per locale, including the existing plural and its items, are preserved. Removing the additive fragment restores the original file bytes.
- All 1,276 materialized base code/resource files were checked against remote blob identities and modes. The 167 unmaterialized research/verification records are preserved by the base tree. Only the two locale files and this evidence record are intended publication changes.
- Per locale: P0 stays 94/94; P1 stays 249/249; P2 rises 171→191/305; P3 rises 7→11/71. The result is 545 typed resources: 544 strings and one plural. Coverage measures direct resource presence, not whole-catalogue linguistic certification.

## Limits

No Android build, device/font rendering, clipping, accessibility traversal, runtime shaping, CI result or historical-language specialist certification is claimed. Technical terms are modern UI adaptations, not claims of historical computing usage. No issue1 action was attempted.
