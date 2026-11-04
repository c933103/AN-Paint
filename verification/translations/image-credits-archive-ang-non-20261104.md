# Image credits and saved-credit archive: Old English and Old Norse

Base: `6cf9fc8d3383a04250ccdfc10f1e93987bc4da6f` on `review/nv-bottom-2038-20261103`.

## Change and independent review

Adds 24 missing P2 string resources to each of `values-b+ang` and `values-b+non` (48 total). Canonical Android resources contain the translations. Independent review accepted all entries unchanged after checking the English source, existing catalogue terminology, complete drafts and actual `GalleryCredits`, `LegacyImageCreditsActivity`, `CommonsAttribution` and `ClassicPaintActivity` consumers.

The wording distinguishes credit editing, clipboard copying, archive attachment and text-file export. Archived credits may concern other images; an already-present source keeps its existing text. Current empty-credit wording is translated rather than the obsolete implication of its resource key. Creator, contributor, publisher, source and licence roles remain distinct. Commons file-page checking remains necessary and changes may constitute an adaptation, without claiming certainty or permission. Irasutoya retains creator rights and expressly excludes Creative Commons. Catrobat's original-artwork licence statement is not extended to all hosted content. Technical conversion parameters and placeholders remain unchanged.

## Checks

- 78 host tests passed in 13.872 seconds: translation, localized help, translation boundaries, current localization contracts, language translation note, string importance, ordinary-priority follow-through and open-review recovery suites.
- Validation across all 171 offered language options passed with `require_complete=False`; this is structural validation, not a claim of complete translation.
- XML uniqueness, Android escaping, ordered typed placeholders, newline escape runs and source attributes passed. All previous resource entries and bytes are preserved; only 24 new strings per locale were appended.
- The materialized integration matches the base tree except for the two intended locale files: 1,274 unchanged files verified by Git blob identity and executable mode. The 170 unmaterialized research/verification documents are retained through the verified base tree, not regenerated.
- All direct string references in `GalleryCredits` (20), `LegacyImageCreditsActivity` (13) and `CommonsAttribution` (5) now have locale resources. This is reference coverage, not a runtime claim.

## Resource-presence counts per locale

P0: 94/94; P1: 249/249; P2: 220/305 to 244/305 (61 missing); P3: 12/71 (59 missing). Total typed resources increase from 575 to 599: 598 strings and one plural resource. Counts describe direct resource presence, not whole-catalogue linguistic acceptance.

## Limits

No Android build, device/emulator, rendering, accessibility, runtime, CI or specialist/native certification is claimed by these host and text checks. Modern computing and copyright terms are catalogue-compatible adaptations, not claims of historically attested technical vocabulary. No issue tracker update is part of this change.
