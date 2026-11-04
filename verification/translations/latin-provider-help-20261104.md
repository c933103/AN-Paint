# Latin illustration-provider help and attribution notices

## Scope and review

- Base: `83fc652c690f88a11f829cc7c267ca7d83055ffb` on `review/nv-bottom-2038-20261103`.
- Add eight Latin resources: four P2 and four P3. All 703 previous Latin resources remain unchanged.
- Independent linguistic and UI-context review accepted all eight unchanged. Canonical wording is in `Paintroid/src/main/res/values-b+la/strings.xml`.
- Inspected active provider labels/descriptions in `IllustrationSource.kt` and `MediaGalleryActivity.kt`. Four related retained Catrobat/insert resources were translated without treating absent direct Kotlin references as evidence they are unused.
- Preserve exact localized captions and menu paths; immediate insertion and credit-copy fields; separately named creators and source notices; adaptation descriptions and compatible-licence alternative; source-specific exceptions; Irasutoya's stated 21-or-more commercial-use payment condition and possible collaboration conditions; Japanese site text; and Openclipart CC0/Large PNG instructions.
- This review checks fidelity to the supplied repository source, not the providers' current external legal terms. Licence bodies, provider URLs and access settings are unchanged.

## Validation

- 78 host translation/localization tests passed.
- Structural validation passed for all 171 offered language options.
- 16 Java resource render checks passed across English and Latin: 12 formatted-resource checks and four literal-resource checks. These strings contain no format arguments.
- New entries preserve source attributes, numeric literals, identifiers, menu path separators and the retained notice's trailing double-newline escape. XML parses and all previous resources are unchanged.
- Base snapshot verified: 1,252 materialized files and modes match the parent tree; 224 unmaterialized base entries are retained through the unchanged Git base tree.
- Latin now contains 711 typed resources: P0 94/94, P1 249/249, P2 302/305 and P3 66/71. The remaining priority gap is eight keys.

## Limits

This is bounded translation and structural evidence, not whole-catalogue linguistic acceptance, native-specialist certification, Android/AAPT compilation, device or emulator testing, layout/accessibility runtime verification, or CI acceptance. Modern technical Latin includes adaptations. No issue 1 retry was made.
