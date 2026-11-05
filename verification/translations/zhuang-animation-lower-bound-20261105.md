# Zhuang: confirmed animation frame-count lower bound

Date: 2026-11-05 (UTC). Base: `f0e3852c8b7cfc9b6486186608398dae0a3130cd`, tree `88e23db91e46f33c9416eae67b4b758d6723eb94`.

## Published change

Added the missing P2 `formats22_at_least_frames` resource in canonical `Paintroid/src/main/res/values-b+za/strings.xml`. It expresses a lower bound, not an exact count, and composes with the existing translated animation message. The fragment supplies neither a frame noun nor a classifier: the containing message already supplies those. Exact wording remains in canonical XML; all previous 200 typed resources are unchanged.

Independent review accepted the meaning with high confidence and the composition with moderately high confidence. [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), C.htm 32/78, directly supports `ceiqnoix` as at least/minimum. The full quantified-object composition was reviewed separately. The OCR warns of incomplete proofreading; this is not native-fluency certification.

## Important boundary and deferred P0

`ImportSelection.showAnimation` computes an exact count or a lower-bound fragment, then selects the displayed body:
- A proven count of at least two uses the existing animation message. If the scan is incomplete, this new fragment becomes its whole second format argument.
- Zero or one proven frame uses the separate unknown-status warning and neutral open-still title. It must not claim the source is definitely animated or definitely static. The computed count fragment is not inserted into that warning.

The P0 `formats22_animation_unknown` remains absent in Zhuang and therefore retains English fallback. A bounded review and revision did not resolve one specific linguistic issue: the final yes/no marker's scope after a negated ascertainment predicate could cover the whole inability statement rather than the subordinate question of whether there are at least two frames. The revised draft was plausible, not shown to be wrong, but was not published as accepted wording. The required meaning is inability to confirm multi-frame status because of complexity, **not merely an unknown exact count**. No native-human approval gate is imposed. Next work on this string should resolve or avoid that construction, while retaining still-image opening and loss of animation on saved output.

The production `AnimationMetadata` scanner returns an incomplete lower bound at its bounded work limit. Its result fields pass unchanged through `AnimationInfo`. Continue selects the initial image; cancel disposes of the staged import. These are source boundaries, not end-to-end device results.

## Checks

- Fresh remote tree reconciled with the preceding verified publication; all **1,252 materialized files** matched base Git hashes and executable modes. **267 unmaterialized leaves** are retained, for 1,519 base leaves.
- Previous 200 typed resources, attributes and original prefix bytes preserved. One missing scalar added, keeping its ordered `%1$d` argument. XML, escaping, literal tokens, numerals and newline checks pass. New XML blob: `ee31f8af71d48af0dbeb3bca8033acede7b10a96`, 18,470 bytes.
- All **171 offered catalogues** and priority manifest pass structural checks.
- **61 host tests passed** in 9.454 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **11 production Java scanner host tests passed** in 11.055 seconds via `test_animation_metadata`: GIF/APNG/WebP counts; separate APNG poster; decoy markers; malformed/truncated containers; work limits before any frame, after one frame, and after a proven lower bound; large sparse chunks. These execute the production scanner, not Android image decoding.
- **90 host Java formatting/composition cases passed** across English and Zhuang: lower bounds and exact-count message paths for GIF/APNG/PNG/WebP, with counts 2, 3, 21, 101 and the signed-int maximum. The rendered count text occurs once in each composed message. The largest values are formatting robustness cases, not claims about scanner output sizes.
- Targeted static checks passed for the zero/one-frame branch, incomplete-count fragment, complete second-argument insertion, neutral title, continue/cancel actions, result-field forwarding and the sole actual resource binding. The unapproved P0 addition is absent.

Zhuang now has **201 typed resources**: P0 **69/94**, P1 **127/249**, P2 **5/305**, P3 **0/71**. Global missing-entry counts over 171 options: P0 162, P1 1,364, P2 30,124, P3 7,481; 46 options have complete presence. Presence is not linguistic acceptance or runtime coverage. The bounded scope remains 59 scoped catalogues plus 112 outside-scope explicit-English-fallback catalogues.

## Limits

No Android build/AAPT, resource execution on device, chooser, image decoding, saved-output animation behavior, lifecycle, layout/accessibility or font checks were run. No merge, release or deployment is claimed. Only canonical XML and this report are intended to change; temporary harnesses and sentence approval mirrors are not published.
