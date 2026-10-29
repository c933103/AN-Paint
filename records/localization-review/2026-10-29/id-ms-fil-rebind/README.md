# Indonesian / Malay / Filipino priority reconciliation

Reviewed current source `0070c5816ad31911d227fab50ea193e2a39b13ab`, tree `ef689a16f5460f901b3b3db49c89dc171140a8e2`. This is a bounded reconciliation, not 1,023 fresh linguistic reviews or whole-language/native-human certification. Production resources are unchanged.

## Useful correction: Filipino account is 335 bounded / 6 held

The 28 October index ingested `fil-complete-review.json` v1 (334 bounded / seven held), omitting the subsequent exact `fil-discard-source-only-addendum.json` and `fil-complete-review-v2.json`. Both are preserved in the [original complete archive](https://github.com/c933103/AN-Paint/blob/d53543b81e1cdd81a3163c392c2dc64f64a66ae5/records/localization-review/2026-10-27/kn-ml-fil-priority/complete-review.tar.xz). Current `Itapon` matches the accepted correction exactly. It has **wording-only** acceptance, no runtime object/flow claim. This is recovered prior credit, not a new acceptance. All 341 complete English/target priority pairs match v2, including its six unchanged holds, and all 41 noncatalogue source blobs bound by that receipt remain exact. The older seven core candidates and subsequent five edits are already integrated; no reapplication is warranted.

## Indonesian: retain prior review, do not retranslate

The [original full341 author review](https://github.com/c933103/AN-Paint/blob/ea373d1948880e4e22f0b3f8111674f7237fec23/evidence/indonesian-priority-review-20261017/README.md) already accounted for 303 static acceptances,32 wording-only, two independently accepted corrections and four holds. Current339 complete target values match that final packet; only the two memory-warning successors differ. They match the existing `translations/source-review/memory-warning-successors-amharic-20261025.json` guard and must not be counted as fresh translations.

The old generic-busy credit-attachment problem is already fixed: `ClassicPaintActivity.attachLegacyImageCredit` selects draft-saving wording only when `autosaving`, otherwise generic-operation wording. The independent `ensureNotAutosaving` guard likewise tests autosaving. Current full Indonesian sentence correctly describes saving in progress. This closes the identified static source-context mismatch, not an installed-device or broad runtime claim. The compact `Depan`/`Latar` clarity/fit and absent palette composition holds remain; no unsupported wording replacement is invented. Historical author review does not become whole341 independent acceptance merely through this reconciliation.

## Malay: current source unchanged, evidence limitation retained

The recovered current index cites a complete341 independent receipt at `id-ms-sw-p0-p1-20261027/independent-review/ms-complete-review.json`, source `651ab24b2c4dfd26d432daf0d8771fdb179ff013`, with340 bounded / one held. All production Java, Malay catalogue and priority manifest bytes are unchanged from that source to0070. The original full receipt itself was not recovered in this pass; its indexed340/1 is retained as indexed historical evidence, not falsely presented as a new full review. No new source defect or unapplied core candidate established.

## Tags and checks

Actual public tags are `id`, `ms`, `fil`; resource directories are respectively `values-in`, `values-ms`, `values-b+fil`. Indonesian uses Android's legacy resource spelling, not a new `in` picker option; historical Tagalog `tl` is not a duplicate public option.

Focused existing tests passed: Indonesian6, KN/ML/FIL9, Malay Help8 (23 total). These test exact values, placeholders/Android syntax, compositions, alias/hold preservation and corruption rejection; they are not linguistic proof. The full host aggregate, Gradle, lint, APK and device tests were not rerun for this evidence-only record. No release, signing, access or PR113 changes.

Next concrete unresolved ordinary trio proposed to the coordinator: Hindi `hi`, Gujarati `gu`, Thai `th`; this does not claim the wider programme complete. Do not add these results to global totals without preserving all original per-entry qualifications.
