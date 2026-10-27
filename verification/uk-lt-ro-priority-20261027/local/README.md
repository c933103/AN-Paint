# Ukrainian, Lithuanian and Romanian — complete P0/P1 unit

Reviewed source: `0c4f732e7c959bb0829bc537b8e1d34e474e4258` / `72ff2d3db4bb3319a0914990331165f901f8309f`.
Implementation: `0023c724e4e33bc43d0645673bfba9b6277f8768` / `b7258b58b6ff95f78dcb2a2a5509818fa5af2e44`. This is an unmerged candidate, not a release.

Each language has an explicit **92 P0 + 249 P1 = 341-identity** complete review/rebind ledger. Polish appears only as a historical completion rebind (310 carried accepts, 30 dormant limits, one Fit-layout hold); it is not an active new translation workstream.

| Catalogue | New entries | Corrected existing | Unchanged existing | Result entries | P0 presence | P1 presence |
|---|---:|---:|---:|---:|---:|---:|
| Ukrainian | 226 | 17 | 120 | 363 | 87/92 | 248/249 |
| Lithuanian | 0 | 22 | 695 | 717 | 92/92 | 249/249 |
| Romanian | 158 | 16 | 189 | 363 | 87/92 | 248/249 |

The **439 exact edits** comprise UK 243 (222 missing priority + 16 existing priority + 5 P2 dependencies), LT 22 (18 priority + 4 P2 dependencies), RO 174 (154 missing priority + 16 existing priority + 4 P2 dependencies). P2 dependencies include actual unit/crop templates, lower-bound frame counts and dithering terminology, not a general P2 expansion. All ten PR185 Ukrainian Save/export/share values remain exact. Romanian retains 75 prior accepted P0 values, with three explicit successors for file-format command composition, Load-image command composition and count-invariant animation wording; those prior receipts remain historical, not duplicated new acceptance.

Both UK and RO retain exactly six absent holds: P0 `formats22_derived_exported`, `ui_save_as`, `ui_save_as_jpeg`, `ui_save_as_jpeg_xl`, `ui_save_as_png`; P1 `ui_foreground_background_colour_palette` lacks a current composed palette-name consumer. Fourteen newly supplied dormant P1 labels per language have wording-only review, not active-context/runtime acceptance. Lithuanian's three unchanged edge-label dependency conditions are satisfied by both exact integrated crop templates; this is not three extra edits. Its 30 historical wording-only limits remain.

## Structural presence, independently separate from review

All 171 exact catalogue rows were recomputed. P0: **7,308 → 7,376 present; 8,424 → 8,356 missing**. P1: **20,022 → 20,330 present; 22,557 → 22,249 missing**. Other 168 rows are unchanged. These source-presence counts are not whole-language approval or current merged totals.

## Verification state

- Independent integrated readback matches all 1,443 UK/RO/LT resource identities, attributes and complete values; no unintended resource changes.
- Original bounded wording fixtures and the historical memory-warning queue/120-pair oracle are preserved. Explicit finite forward bindings require exact prior values/source/attributes; new SVG, colour-profile and memory-warning expectations are scoped additions, not weakened fallback assertions.
- New host tests enforce all 439 exact changed identities, complete text and format tokens, literal percent/newline handling, omitted/extra/wrong-locale negatives, atomic compositions and exact holds. Focused checks pass.
- Initial full aggregate: 1,467 tests, 11 failures/3 errors from missing cross-family expectation updates. Second aggregate: 1,469 tests, one stale Romanian P1 absence assertion. These are failures, not relabelled passes; their exact scoped expectation repairs preserve prior history and data-safety assertions. Final ordinary and optimized aggregates each pass all 1,469 tests (192.591 s / 194.883 s, exit 0). Sanitized complete logs are retained in `host-validation-logs.zip`.
- Eight new JVM methods cover compiled resources/arguments, actual dimension/crop controls, tool accessibility, animation count/cancel flows, memory rejection and byte-preserving draft recovery. They are authored, **not yet a runtime pass**. Local Android SDK/Gradle distribution is unavailable; exact-head hosted CI is pending.

`complete-review-ledgers.zip` contains all full source-bound decisions, final values, prior-receipt lineage, source consumer bindings, confidence and limitations, independent map validation, integrated readback and dependency overlay. `integration-proof.json` records exact added/corrected/preserved keys. `all171-priority-presence-delta.json` retains every before/after row.

Model-based bounded review is not native-speaker, whole-language, installed-screen, complete-layout, physical-device or TalkBack certification. Dither/codec terminology retains moderate confidence. Unrelated P2/P3 work and established release/Help/other-PR holds remain unchanged. No release, visibility change, credential, private user data or authorization transcript is included.
