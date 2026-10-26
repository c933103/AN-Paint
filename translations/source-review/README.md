# Memory-warning source correction and sequential review

This is an active **two-term** review queue, not a new whole-language review or
acceptance report. The canonical English is corrected first. No localized
catalogue, English variant or historical linguistic receipt is changed here.

## Corrected source

Source baseline: [`ef46e8aa`](https://github.com/c933103/AN-Paint/commit/ef46e8aa4f55825a071f4c1ecd6f3c80b9355f51).
The [source finding](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6314782623)
records the distinct predicates and counterexamples. Existing resource IDs remain
unchanged for compatibility; their historical names are not diagnostic claims.

- `ui_no_resize_fits_decoder_memory` (P1):
  “Even at the smallest output size, this image cannot be loaded for editing
  within the current memory limits. Cancel and use a smaller source image.”
- `ui_assembly_source_memory_floor` (P0):
  “This assembly is estimated to exceed the current working-memory budget, even
  at the smallest output size. Reducing the assembly dimensions alone is not
  enough under the current limits. Close other documents or prepare a smaller
  source image before trying again. Your assembly is unchanged.”

The assembly wording explicitly identifies an estimate. Neither warning claims
that decoder buffers or one source's decoding memory alone exceed the total
budget. Both retain their complete remedies and current-limit qualification.

### Do not merge the consumer predicates

The import dialog selects its warning for valid entered dimensions when the
current plan fails and `hasNativeWork && !accepts(minimumPlan, residentPixels)`.
`ImportMemoryRequirements.accepts` combines ordinary target/decoded/editing and
resident estimates, native-or-decoded-plus-metadata work, further target-sized
buffers, and allocation/bitmap guards. The minimum plan is 1×1. The inspected
formulas do not establish a separately reachable allocation-only rejection at
that size. Keep the adjacent codec source/tile explanation unchanged.

The assembly dialog instead displays its warning when `suggested` returns null
on `!fits(1×1)`, then returns without creating output. `fits` compares the output
pixel count and **combined estimated peak** with the working budget. At 1×1 the
pixel guard passes. The estimate is the maximum of `28 × output pixels + 4 ×
resident pixels` and each placed source's combined import estimate, including
resident output. It is not a sum of all source decoders, does not call the full
import-admission predicate, and has no `hasNativeWork` condition.

Relevant unchanged consumers:
`ImageResizeDialog.kt` (40–50), `ImageImport.kt` (27–44, 63–108),
`ImageMemoryPolicy.kt` (38–40), `AssemblyActivity.kt` (297–301), and
`AssemblyRenderer.kt` (23–48), under
`Paintroid/src/main/java/org/catrobat/paintroid/classic/` at the baseline above.

## All 171 options are flagged

[`memory-warnings-20261021.json`](memory-warnings-20261021.json) is the durable
active queue. It contains all **171 offered options × 2 terms = 342 review
items**, in picker order, with exact catalogue paths and values, explicit missing
values and canonical-English fallbacks, English-variant identity, review status,
editing disposition and an initially empty successor-receipt field.

For **each** term there are:

- 1 corrected canonical-English option (`en-001`);
- 54 present non-English values;
- 6 present regional-English overrides and the present private-use English
  option (`en-XV`), all still using the old English and needing editing after
  review;
- 109 absent exact values with canonical-English fallback.

These are exact-term presence counts, not the older 59/112 whole-catalogue scope
classification or counts of reviewed languages. **All 342 items need review;
zero are approved against the corrected English.** Missing entries are not
translations, and inheriting corrected fallback is not linguistic acceptance.
The source correction itself does not close its `en-001` review item.

## Review one by one after accepting the corrected English

1. Take the next option in recorded picker order, then its two complete terms.
2. Compare its exact current wording or fallback with the corrected English,
   relevant composition and the appropriate predicate above. Do not diagnose a
   translation defect merely because it was flagged.
3. Decide separately whether to retain, edit, translate, or explicitly retain
   fallback. Bind any decision to exact wording and new evidence before updating
   its status and successor receipt.
4. Preserve unrelated entries and original receipts. Earlier paraphrases,
   including Hungarian/Vietnamese and the proposed Simplified Chinese addendum,
   are historical/provisional inputs for these terms, not already-approved
   translations of this new source. No whole-language reset or new completion
   credit follows from this queue.

## Verification limits

The source regression checks full English values, scalar/format structure and
negative controls. Queue checks cover all offered identities, values, absences,
fallbacks and pending dispositions. Six existing paired-language suites use an
explicit default-English successor expectation for these two keys only. Their
original fixtures, hashes, language values and receipt bindings remain unchanged;
passing their preservation tests does **not** renew semantic acceptance.

No application build, Gradle, APK, workflow dispatch or runtime/device check is
needed or claimed for this wording review. No version, release input, signing or
application-publication change is included. The release pause remains in force.

## 25 October 2026: bounded Ainu warning successors

The historical queue above and `memory-warning-successors-20261023.json` are preserved unchanged. The current compact behavioral fixture is now [memory-warning-successors-20261025.json](memory-warning-successors-20261025.json): it retains the earlier 114 exact pairs and adds only the two reviewed warnings in each of `ain-Kana` and `ain-Latn`.

The [exact source/value review](https://github.com/c933103/AN-Paint/blob/ed90d5ce76b9971ee934a4175fb585215cd22b37/records/localization-review/2026-10-25/ainu-partial-help-warnings/r01/warnings.json) supports these four successor values. Review remains bounded, with medium idiom confidence and no native-reader or runtime certification. The loading warning's existing cancel/smaller-source sentence is retained, not independently perfected.

The active two-key contract covers 118 reviewed successor pairs across 59 options; four present pairs remain outside that successor set (`jje` and `vi-Hani`), alongside 218 missing pairs and two canonical-English pairs. These are warning-key inventory counts, not whole-language acceptance or Help-key approval. The separate Ainu estimate-label correction is not part of this two-key registry.

The registry continues to require exact source, historical target, locale/key inventory and expected current wording. Existing corruption checks remain, now also exercising the four Ainu successors; held-case controls use the still-held `jje`/ `vi-Hani` identities. No old receipt or queue value is rewritten to make the new text pass.


## 25 October 2026: bounded Amharic priority successors

The current compact behavioral fixture is now
[memory-warning-successors-amharic-20261025.json](memory-warning-successors-amharic-20261025.json).
It retains all 118 earlier exact pairs and adds the two independently reviewed
Amharic priority strings. The historical queue and both earlier successor
fixtures remain unchanged. Amharic's historical values are explicitly required
to be absent; this is not permission to accept missing history for other locales.
The current registry covers 120 pairs across 60 options, leaving four held pairs,
216 historically missing pairs without successors, and two canonical-English pairs.
These counts do not certify whole-language, native-reader or runtime completion.
