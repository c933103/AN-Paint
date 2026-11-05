# Interlingua remaining controls and short help

Base: `6e473e6f37c03106c86159e5734f19b722dfe096` on `review/nv-bottom-2038-20261103`.

Adds 55 missing priority resources: the remaining seven P2 entries and 48 short P3 entries. All 661 previous typed resources and attributes remain unchanged; the catalogue now contains 716 typed resources. The additions include one preserved alias (`ui_cursor_help29` → `ui_cursor_help31`) and the unchanged formal licence name `GNU Affero General Public License`.

## Scope and review

The batch covers drawing and selection hints, cursor operation, shape/curve/polygon gestures, canvas-bounds help, the pixel grid, toolbox accessibility captions, file-picker recovery, source export and licence/credit headings. It preserves the pencil's 1–100 pixel range, the pixel grid's 800% threshold, the half-shorter-side radius limit and the distinction between resizing, rotating and moving selections. Help routes name the actual localized drawing and insert categories. Fill terminology is aligned with the existing `Reimplimento` controls.

Independent linguistic and semantic review checked the full batch against canonical English, the existing Interlingua controls and available production consumers. Review corrected `circumscribe`, named the pencil's actual `Dimension (px)` control and clarified that `Termina curva` applies the curve without completing all gesture steps. No implementation, English resource, other locale, font or licence body changed. No permanent per-batch fixture or copied prose approval mirror is introduced.

Fifty-one additions have exact direct production references, including the alias consumed by cursor-mode help. Four retained manifest resources have no exact direct production reference: the old right-arrow caption, paste guidance, duplicate pencil hint and toolbox-scroll description. Those four received resource-level review only; no runtime-display claim is made for them.

## Verification

- 87 affected host tests pass: localization structure/contracts/boundaries, current help routes, priority follow-through, tooltip wiring, save/export help, numeric-input wiring and count wording. This is an affected subset, not the entire repository suite.
- All 171 offered options and the priority manifest pass structural validation.
- All 110 English/Interlingua Java resource-template checks pass for the 55 additions. Source attributes, literal-percent handling, numerical limits and the cursor-help alias are preserved. These are source/template checks, not Android runtime rendering.
- All 1,252 materialized base files match the freshly verified remote tree's Git blob hashes and executable modes. Its 234 unmaterialized non-tree entries are retained unchanged.
- Direct priority presence: P0 94/94, P1 249/249, P2 305/305, P3 68/71. Remaining: three long P3 help resources, down from 58. Presence is not whole-catalogue linguistic acceptance.

No Android build, AAPT, installed-layout, device, accessibility/runtime, CI or native-speaker certification is claimed. Publication uses the exact expected parent and a non-force lease, followed by final remote tree and changed-file readback verification. Remaining resources are the assembly manual (`ui_add_up_to_20_images_with_android_s`), short overall help (`ui_help23`) and full editor manual (`ui_the_arrow_on_the_left_directly_below_the`).
