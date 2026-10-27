# Marathi, Tamil and Telugu: complete priority review and implementation

Implementation: [b05569f5f960d152abaa5f2dba0bfcb01c421833](https://github.com/c933103/AN-Paint/commit/b05569f5f960d152abaa5f2dba0bfcb01c421833), tree `b66b22c30f6404e37fe55f3fd185299eb241a2fa`, based on merged `1126b650216478c422997dcd1236ca6cc780e4e3`. All 1,412 remote blobs/modes match the reviewed source tree; exactly 17 paths change and none are removed. Earlier merged localization units and PR188's six-path change remain intact. This unit does not include any unpublished parallel implementation.

## Complete scope and separate accounting

Each language accounts for all **92 P0 + 249 P1 = 341** identities. Independent review accepts **87 P0 and 247 P1** complete values per language, with seven exact absent holds. No mapped historical acceptance is credited as new. The 23 accepted identities per locale without a direct caller remain **wording-only**, including corrected dormant labels; this is not runtime-context acceptance.

| Language | Source catalogue before → after | Added typed entries | Existing corrections | Total edits | Original entries unchanged |
|---|---:|---:|---:|---:|---:|
| Marathi (`mr`) | 99 → 356 | 257 | 18 | 275 | 81 |
| Tamil (`ta`) | 96 → 360 | 264 | 13 | 277 | 83 |
| Telugu (`te`) | 97 → 360 | 263 | 22 | 285 | 75 |

The **837 typed edits** comprise **752 missing priority additions, 46 retained-priority corrections and 39 atomic P2 edits**. P0 has 236 additions and eight corrections; P1 has 516 additions and 38 corrections. Fifteen adjacent typed identities were assessed per locale: 45 assessments, 39 edits and six unchanged values. The companions cover animation lower bounds, crop sides/units, quality/lossless/dither, interpolated tool labels and complete crop-preview plurals. Plural children are not inflated into separate resource identities.

Seven absent holds in each catalogue remain: `formats22_derived_exported`, `ui_save_as`, `ui_save_as_jpeg`, `ui_save_as_jpeg_xl`, `ui_save_as_png`, `ui_foreground_background_colour_palette` and `ui_pinch_and_pan_mode`. Specific Help/callback/archive restrictions, PR159, PR113 retarget restrictions, PR56 never-merge and the 0.0.41 release pause remain unchanged.

## Previously reviewed Swahili and Vietnamese follow-through

A separate **four typed edits** apply the [already durable complete retained reviews](https://github.com/c933103/AN-Paint/blob/569659e1a5fbadb71f2c3b33650efac825ee36d4/verification/sw-vi-complete-review-20261027/README.md): Swahili's return-to-drawing command and conditional crop plural, Vietnamese's previously accepted but unapplied magnifier sentence and conditional crop plural. Vietnamese magnifier wording receives no fresh candidate credit. These are not two additional newly authored full-priority cohorts. Each catalogue's other 715 typed entries is unchanged. Original Swahili/Vietnamese acceptance, narrower historical receipts, holds and dormant-context limits remain separately recorded.

The coherent source unit therefore contains **841 typed edits**, not 841 new translations or newly reviewed priority values.

## Verification and limits

- Exact independent complete-value/source/attribute/caller review and integrated XML readback passed.
- The compact fixture preserves full target strings/plural children, one shared complete English source map, exact edited/retained partitions, finite predecessor values, the Marathi Save alias, exact disposition and 23-key dormant-context partitions. No older fixture is rewritten or broadened.
- Independent fixture review rejected **1,095 metadata mutations**. Both new focused suites pass **15 tests** in ordinary and optimized Python, including each plural child and cross-locale value substitution.
- Final full local host suites: **1,506 passed in ordinary mode (200.618 seconds)** and **1,506 passed in optimized mode (203.745 seconds)**. Earlier diagnostic output is retained separately from the final ordinary log.
- Fifteen new JVM methods cover actual dimension/crop/category/animation/memory/save consumers, left/right text alignment, format controls, return-to-drawing, magnifier controls and conditional attachment geometry. Static independent API review passed. **Hosted compilation/JVM/lint/device execution is pending at this evidence checkpoint.** There is no local Android SDK, native-speaker certification, installed-device acceptance, release or merge claim.

`all171-source-presence.json` in the archive reports all 171 offered catalogues before and after this unit. It reports source presence, not linguistic acceptance or completion.

## Evidence

[complete-review.tar.xz](complete-review.tar.xz) contains 50 regular members including its per-member SHA256 manifest: complete author packets, original candidate versions, independent ledgers and feedback/adoption history, original-catalogue Git bindings, exact integration/readback receipts, source delta and local test evidence. [archive-binding.json](archive-binding.json) binds the archive bytes and source baseline. Source implementation and evidence use normal reachable commits; no history is rewritten.
