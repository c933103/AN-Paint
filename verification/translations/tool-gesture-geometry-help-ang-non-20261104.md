# Drawing-tool gesture and geometry help: Old English and Old Norse

Base: `acb4669f24580ea308c12d17c0f1918787368176` on `review/nv-bottom-2038-20261103`.

## Change and independent review

Adds 18 missing P3 tool-hint strings per locale (36 translated entries). Canonical Android XML owns the wording. Independent review accepted the batch after two Old English pronoun corrections from `innan hans` to `innan his`, in the rectangular-selection and free-form-selection hints. The corrected integration was revalidated. Other wording was accepted unchanged.

The hints preserve curve drawing plus two bends and early completion, selection movement/resizing/rotation, aspect locking and committing, ellipse bounds, opposite-corner shape gestures, five-pointed stars, arrow tail-to-head direction, background-colour erasing, two-finger navigation while drawing tools are selected, pencil widths from 1 to 100 pixels, selected brush tip/size, watercolor strength and blending, hold-or-drag spray, and closed/open polygon behavior. Rounded-rectangle radius is capped per shape at half its shorter side, not globally fixed by the slider. The current pencil source is translated rather than the obsolete one-pixel implication of its key.

Exact embedded action/setting captions match the existing locale resources for Finish curve, Lock proportions, Commit selection, Radius (px), Tolerance, Finish polygon and Close polygon. Strength uses the caption stem without the percentage suffix, as the source hint does. Technical compounds remain catalogue adaptations, not claims of historically attested computing vocabulary.

## Consumers and checks

- `PaintDocument.PaintTool` maps all 20 tools to their real labels and hints. `ClassicPaintActivity.populateToolOptions` displays the hints and associated controls. Every new key is one of these production hints. All 20 hints and all 20 labels now have resources in both locales; this is reference coverage, not complete runtime validation.
- `PaintCanvas` geometry, pending-curve/polygon commits and per-rectangle radius clamping were inspected; `PaintDocument` watercolor alpha is controlled by strength.
- XML uniqueness, Android escaping, exact source attributes, typed placeholders and newline escapes pass. All 644 previous typed resources and bytes per locale remain unchanged, with exactly 18 appended strings. Numeric bounds 1 and 100, px in the radius caption and all embedded captions are preserved. No extra placeholders or formatting flags are introduced.
- 78 host tests passed after both pronoun corrections in 11.351 seconds across translation, localized help, boundaries, current localization contracts, language note, string importance, ordinary-priority follow-through and open-review recovery.
- All 171 offered language options passed structural validation with `require_complete=False` after correction.
- The base integration was checked against the Git tree: 1,276 materialized files matched content and executable mode. The 174 unmaterialized research/verification records are retained through the verified base tree. The two locale XML files are the only changed application files.

## Resource presence per locale

P0: 94/94; P1: 249/249; P2: 281/305 (24 missing); P3: 20/71 to 38/71 (33 missing). Total typed resources increase from 644 to 662: 661 strings and one plural resource. Counts are direct resource presence, not whole-catalogue linguistic acceptance.

## Limits

No Android build, device/emulator, rendering, accessibility, runtime, CI or specialist/native certification is claimed. No issue tracker update is included.
