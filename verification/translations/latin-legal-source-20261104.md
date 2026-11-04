# Latin About, licence navigation and source export

## Scope and review

- Base: `f718dd662df160bcd5486620c755b4c21e8c5662` on `review/nv-bottom-2038-20261103`.
- Add 21 Latin resources: two P2 and nineteen P3. All 682 previous Latin resources remain unchanged.
- Independent linguistic and UI-context review accepted all 21 unchanged. Canonical wording is in `Paintroid/src/main/res/values-b+la/strings.xml`.
- Inspected the actual About menu, bundled-notice navigation and source export in `ClassicPaintActivity.kt` and `LegalInfo.kt`. Translations change headings and status messages, not the bundled licence bodies.
- Preserve the exact GNU Affero General Public License title; codec, artwork, font and translation-attribution scopes; this-version source export; build scripts and licence notices in the success status; and the separate failure status. Success is emitted after stream copying completes.

## Validation

- 78 host translation/localization tests passed against the fully generated candidate XML.
- Structural validation passed for all 171 offered language options.
- 42 Java resource render checks passed across English and Latin. These strings contain no format arguments; the check verifies that each selected resource renders without a formatting error.
- New entries preserve source attributes, typed-argument absence, literal identifiers and newline structure. XML parses and all previous resources are unchanged.
- Base snapshot verified: 1,252 materialized files and modes match the parent tree; 223 unmaterialized base entries are retained through the unchanged Git base tree.
- Latin now contains 703 typed resources: P0 94/94, P1 249/249, P2 298/305 and P3 62/71. The remaining priority gap is 16 keys.

## Limits

This is bounded translation and structural evidence, not whole-catalogue linguistic acceptance, native-specialist certification, Android/AAPT compilation, device or emulator testing, layout/accessibility runtime verification, or CI acceptance. Modern technical Latin includes adaptations. No issue 1 retry was made.
