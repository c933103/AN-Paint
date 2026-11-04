# Interlingua typography and text controls

Base: `cd199013272a66fdee01a51c696d328d61466904` on `review/nv-bottom-2038-20261103`.

Added 23 missing resources to the canonical Interlingua catalogue: 19 P2 and four P3. Independent review accepted all 23 unchanged. All 460 previous typed resources and their attributes remain unchanged; the catalogue now contains 483. The multilingual preview sample is deliberately unchanged and is not newly translated prose.

## Scope

The nine system font captions distinguish stroke weight from condensed width and fixed character spacing. Vertical text controls distinguish top-to-bottom direction and column order from character orientation. The hint preserves joined sideways script, including Mongolian, combining marks with their characters and complete emoji sequences. Background fill applies to the text bounds. Top/bottom alignment, canvas placement, font and size selection, and the font-notices caption retain their source functions.

All 23 additions have direct production references. Context was checked in `FontCatalog`, `TextStyleDialog`, `TextPreview` and `VerticalText`. No font files, licence bodies, shaping code or runtime implementation changed. Canonical Android resources own the wording; no full-prose mirror or per-language approval fixture is introduced. `Serifas` is an international typographic adaptation, not a claim of dictionary attestation or specialist certification.

## Verification

- 78 host tests pass: translations, localized help, translation boundaries, current localization contracts, language translation note, string importance, ordinary priority follow-through and open-review recovery.
- Structural validation passes for all 171 offered options and the priority manifest.
- 46 English/Interlingua resource-render checks pass. XML/Android escaping, attributes, argument structure and the exact mixed-script sample are preserved.
- All 1,253 materialized base files match Git blob hashes and executable modes. The verified base tree retains 228 unmaterialized non-tree entries.
- Direct priority presence: P0 94/94, P1 249/249, P2 135/305, P3 5/71. Remaining: 236 keys (170 P2, 66 P3). Presence is not whole-catalogue linguistic acceptance.

No Android build, AAPT, installed layout, device, accessibility/runtime, CI or native/specialist certification is claimed. No issue1 action or retry. Publication requires the expected parent and a non-force lease, followed by full remote tree and changed-file readback verification.
