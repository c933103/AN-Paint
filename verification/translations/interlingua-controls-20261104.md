# Interlingua shape, stroke and cursor controls

Base: `c828304aa1ed7a6c38e4fe98612ef6684e437a36` on `review/nv-bottom-2038-20261103`.

Added 31 missing P2 strings to the canonical Interlingua catalogue. Independent review accepted all 31 unchanged. All 429 previous resources and their attributes remain unchanged; the catalogue now has 460 typed resources.

## Scope

Shape completion is distinct from polygon closure. Fill-plus-line denotes fill plus outline. Freehand smoothing and pixel-edge anti-aliasing remain separate controls. Cursor-mode enablement differs from starting or stopping ink. Marker size denotes the visible cursor indicator, not brush width. Pan/start/stop guidance, the two integer coordinates, magnified preview and the 800%+ grid threshold retain source meaning and formatting. Existing round/square-related catalogue entries are preserved.

Checked actual consumers in `ClassicPaintActivity`, `PaintCanvas` and `PaintDocument`. Six retained control keys lack direct production Kotlin references in the bounded scan; they remain translated in their control family, not declared unused or removed. Canonical Android resources own the wording; no prose mirror or per-language approval fixture is introduced.

## Verification

- 78 host tests pass: translations, localized help, translation boundaries, current localization contracts, language translation note, string importance, ordinary priority follow-through and open-review recovery.
- Structural validation passes for all 171 offered options and the priority manifest.
- 62 English/Interlingua resource-render checks pass: 54 formatted and eight literal. Source attributes, argument order/types, XML/Android escaping, newline structure and numerals are preserved. Four literal-percent entries retain `formatted="false"`; the x/y numeric template is unchanged.
- All 1,252 materialized base files match Git blob hashes and executable modes; 228 unmaterialized non-tree entries are retained through the base tree.
- Direct Interlingua priority presence: P0 94/94, P1 249/249, P2 116/305, P3 1/71. Remaining: 259 keys (189 P2, 70 P3). Presence is not whole-catalogue linguistic acceptance.

No Android build, AAPT, installed layout, device, accessibility/runtime, CI or native/specialist certification is claimed. No issue1 action or retry. Publication requires the expected parent and a non-force lease, followed by full remote tree and changed-file readback verification.
