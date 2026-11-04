# Equal image dimensions: Old English and Old Norse

Base commit: c1b1428c4930cbb4670f03d7c493a6677754c688.

Adds 14 previously absent P2 strings to each offered `ang` (Ænglisc) and `non` (Norrœna) catalogue. Independent semantic review accepted all 28 after normalizing the spelling of the Old Norse movement verb in both live summaries to the catalogue's fœra family.

The batch covers equal-width/equal-height actions, complete introductions, live dimension/range summaries, percentage-input descriptions, apply-to-all, smallest/largest presets, original-size reset, range validation and width-unit accessibility. NormalizeImagesDialog, ImageAssembly.ImageNormalization and DimensionControls were inspected for the actual argument and control context.

Both introductions retain each image's own aspect ratio and state that original files and crop settings remain unchanged. The percentage denominator is the largest current dimension on the selected axis, not each image's original size. The summaries distinguish target size, the other-axis minimum/maximum range and that denominator; only already placed images are described as moving to make room. Range errors refer to calculated dimensions outside Android's limits, without asserting that rejected dimensions have been applied. Width-unit accessibility reuses each catalogue's existing Width (%1$s) form so the supplied unit label remains independent of case inflection.

Validation passed:
- Exact English and target base Git identities; offered picker entries; XML parsing and duplicate-name checks; exactly 14 additions per locale; all 410 previous entries, attributes and surrounding bytes unchanged.
- Android escaping/formatting, source attributes and exact typed placeholder sequences. Each live summary retains the source's two escaped-newline runs, including exact backslash counts. Pixel units, range dash and Android identifier are unchanged.
- 78 host tests: test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery.
- Structural catalogue validation passed for all 171 offered options. All 1,276 materialized tracked base files matched their Git blob identities and executable modes. The 160 unmaterialized research/verification documents are retained unchanged in the publication tree and were not needed by these checks.

Each locale changes from P2 67/305 to 81/305, leaving 224 P2 keys absent. P0 remains 94/94, P1 249/249 and P3 0/71. These are direct-key-presence counts, not whole-catalogue quality ratings. The priority manifest is unchanged.

Vocabulary follows existing width, height, image, aspect-ratio, original-file, crop, percentage and size terms. Technical explanations are adapted for the current application; they are not claimed historical computing vocabulary or full-sentence attestations.

Limits: no historical-language specialist certification, whole-catalogue linguistic acceptance, Android build, device/rendering check or CI result is claimed. Canonical Android resources own current wording; this evidence is not a wording freeze.
