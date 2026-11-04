# Remaining Latin image labels and complete help

## Scope and review

- Base: `f803ee30f256ee9d63bc2225119e73750ba00b96` on `review/nv-bottom-2038-20261103`.
- Add eight Latin resources: three P2 and five P3. All 711 previous Latin resources remain unchanged.
- Translate the complete eight-paragraph assembly guide, active editor help, ten-paragraph retained editor manual, shared-image/default-filename labels, missing-picker instruction, selection-copy hint and duplicate pencil description. Retained keys are not removed or declared unused.
- Independent linguistic and UI-context review accepted the batch with one narrow assembly sentence clarification: the assembled image is placed in the current image's place, and that change can be undone. The corrected wording is in `Paintroid/src/main/res/values-b+la/strings.xml`.
- Inspected actual `AssemblyActivity.kt` and `ClassicPaintActivity.kt` help, picker, sharing and assembly-edit consumers; selection masking, transform, drawing and bounds behavior; and prior reviewed UI captions.
- Preserve snapping-only overlap rejection versus allowed exact-position overlap; conditional smaller-output choice and memory warning; unchanged original files and local persistence; view-only zoom; opaque-canvas versus floating-selection transparency; original-save-target and saved-state distinctions; complete controls and source-specific import behavior. PNG is separate from adjustable-quality JPEG/HEIC. The retained long manual is distinct from active `ui_help23`.

## Validation

- 78 host translation/localization tests passed after the final correction.
- Structural validation passed for all 171 offered language options after the final correction.
- 16 Java resource render checks passed across English and Latin: 14 formatted-resource checks and two literal-resource checks. These strings contain no format arguments.
- 168 quoted caption/path components match current Latin captions or the source-preserved Android app names. Android outer quoting on existing labels is handled as resource syntax, not displayed text.
- Eight assembly paragraphs and ten manual paragraphs, all newline separators, four exact hex values, three literal 100% occurrences, source numerals, .png suffix, source attributes and duplicate-pencil equivalence pass checks. All previous entries remain unchanged and XML parses.
- Base snapshot verified: 1,252 materialized files and modes match the parent tree; 225 unmaterialized base entries are retained through the unchanged Git base tree.
- Latin now contains 719 typed resources: P0 94/94, P1 249/249, P2 305/305 and P3 71/71. No direct priority key is missing.

## Limits

Complete priority-key presence is not whole-catalogue linguistic acceptance. This is bounded translation and structural evidence, not native-specialist certification, Android/AAPT compilation, device or emulator testing, layout/accessibility runtime verification, current provider-term verification, or CI acceptance. Modern technical Latin includes adaptations. No issue 1 retry was made.
