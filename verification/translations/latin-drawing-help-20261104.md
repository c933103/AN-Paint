# Latin drawing controls and cursor help

## Scope and review

- Base: `9f23060038ea4b670d3722086abd46bc5a24fd52` on `review/nv-bottom-2038-20261103`.
- Add 12 Latin resources: four P2 controls and eight P3 help entries. All 651 prior Latin resources remain unchanged.
- Independent linguistic and UI-context review accepted all 12 unchanged. Canonical wording is in `Paintroid/src/main/res/values-b+la/strings.xml`.
- Inspected actual tool-option, selection, full-screen, grid, pencil, cursor and assembly-help consumers. Retained arrow/scroll descriptions were translated from source without inferring that absence of a direct static reference makes them unused.
- Preserve selection resize versus rotation, crisp pencil edges at any selected width, cursor position/start-pan-stop sequence, separate marker and painted brush sizes, exact localized menu path, help alias, and the literal 800%-or-higher condition.

## Validation

- 78 host translation/localization tests passed.
- Structural validation passed for all 171 offered language options.
- 24 Java resource render checks passed across English and Latin: 22 formatted-resource checks and two literal-resource checks. These include static strings and the source-preserved alias, not Android runtime alias resolution.
- New entries preserve source attributes, resource alias, typed arguments, numeric literals, percent handling and newline structure. XML parses and all previous resources are unchanged.
- Base snapshot verified: 1,252 materialized files and modes match the parent tree; 221 unmaterialized base entries are retained through the unchanged Git base tree.
- Latin now contains 663 typed resources: P0 94/94, P1 249/249, P2 296/305 and P3 24/71. The remaining priority gap is 56 keys.

## Limits

This is bounded translation and structural evidence, not whole-catalogue linguistic acceptance, native-specialist certification, Android/AAPT compilation, device or emulator testing, layout/accessibility runtime verification, or CI acceptance. Modern technical Latin includes adaptations. No issue 1 retry was made.
