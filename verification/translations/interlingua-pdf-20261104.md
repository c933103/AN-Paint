# Interlingua PDF and document-page selection

## Scope and review

- Base: `5d529b23ff996526cda17a8fd24e2731aee893cd` on `review/nv-bottom-2038-20261103`.
- Add 20 genuinely missing P2 entries to the offered Interlingua (`ia`) catalogue. All 367 prior resources remain unchanged; no other catalogue changes.
- Independent linguistic and UI-context review accepted all 20 unchanged. Canonical wording is in `Paintroid/src/main/res/values-b+ia/strings.xml`.
- Inspected `ImportSelection.kt` page chooser and preview consumers and `PdfCodec.kt` page, crop, file-size and memory guards. Generic document-page controls remain distinct from PDF-only diagnostics.
- Preserve possible damage/unsupported features; password OR unsupported encryption; saved unprotected copy before import; nonempty file with inclusive 512 MiB maximum; 1..maximum page bounds; stale selection chosen again from this document; nonempty crop within the selected page; memory limit; and smaller-size choices only when possible.
- Existing Interlingua preview, crop, file, loading and recovery terminology is reused. Selection was based on missing P2 entries, not an inference that raw P0 gaps represent English fallbacks.

## Validation

- 78 host translation/localization tests passed.
- Structural validation passed for all 171 offered language options.
- 40 Java resource render checks passed across English and Interlingua, including static labels and ordered typed formatting arguments.
- XML, source attributes, argument signatures/order, newline escapes and numeric literals pass checks. All previous resources are unchanged.
- Base snapshot verified: 1,252 materialized files and modes match the parent tree; 226 unmaterialized base entries are retained through the unchanged Git base tree.
- Interlingua now contains 387 typed resources: P0 94/94, P1 249/249, P2 44/305 and P3 0/71. The remaining priority gap is 332 keys.

## Limits

This is bounded translation and structural evidence, not whole-catalogue linguistic acceptance, native-specialist certification, Android/AAPT compilation, device or emulator testing, layout/accessibility runtime verification, or CI acceptance. No issue 1 retry was made.
