# Shan batch E — metadata, memory warnings and remaining controls

`batch-e.tsv` contains **17 additional missing-key candidates: 5 P0 + 12 P1**. Fourteen are new; three revise earlier unaccepted proposals (translation note and two original-resolution messages). No previously accepted key is repeated for credit.

Source binding is unchanged: source-bound merged develop `96681f687671a1fdffe134a325843919c1543401`, tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`, materialized source under `baseline resource snapshot`. Exact source values, attributes and placeholders accompany every candidate. The local materialization cannot itself resolve HEAD; this is not an independent Git attestation.

## Evidence and semantic choices

- MediaWiki's primary [Shan locale](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/shn.json), `metadata` and adjacent image-metadata help, directly attests **မႄႇတႃႇတေႇတႃႇ**. It supports the technical noun in four new messages, not automatic acceptance of the authored full sentences.
- `AutosaveStore.kt` distinguishes `draft.json` metadata from `canvas.png`/`floating.png`; the missing/invalid metadata messages do not say the whole drawing was deleted.
- `PlatformImageColour.kt` distinguishes malformed/unsupported metadata, data truncation, and failure to start the colour converter. The last case must retain that the image was not imported.
- Existing accepted memory, decode and working-buffer vocabulary is reused. **No held encoding phrase is reused**. Original resolution is rendered descriptively as original pixel dimensions in the image-memory/assembly-output contexts, not byte size or display dpi.
- The long P0 budget warning retains the whole-image memory requirement, reserved transform/selection space, dependence on available memory, stopping **before** oversized allocation, and **no** automatic resize. Its authored transform and temporal wording are explicit review points.
- ASCII export uses descriptive unformatted-text and equal-character-width-font wording. The inability to reopen it as the original image is preserved, not softened to inconvenience.
- SVG errors preserve both the dimension condition and refusal to silently substitute/resize.
- `ScanlineFill.kt` establishes that Tolerance is a pixel-colour-difference threshold. Navigate is pan-only viewing, not changing stored pixels. The three-placeholder palette alias lacks a current caller, so its third argument remains a narrow contextual hold risk even though all three tokens are retained.

All are authored candidates awaiting independent review, not native-human certification or official credit. No implementation or test result is asserted.
