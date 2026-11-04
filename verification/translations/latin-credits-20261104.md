# Latin image credits and saved-credit archive

## Scope and review

Twenty-four missing Latin strings cover image-attribution records, editing and clipboard copy, saved-credit selection and text export, provider-specific notices and technical import changes. Canonical wording is in `Paintroid/src/main/res/values-b+la/strings.xml`. Independent review accepted all entries unchanged.

Reviewed against English resources, `GalleryCredits`, `LegacyImageCreditsActivity`, `ClassicPaintActivity` and `CommonsAttribution`. Copy, add-to-image and text-file save remain distinct. Archived records may belong to other images; an existing source record retains its text. The notices preserve named creators/copyright, required attribution, possible adaptation, Catrobat original-work licensing and Irasutoya copyright/non-Creative-Commons conditions. Machine-readable SVG/raster parameters and provider names remain exact. These are translations of existing UI notices, not new legal advice.

## Verification

- 591 prior typed resources and attributes preserved; 24 strings added, yielding 615 typed Latin resources.
- XML, Android escaping, ordered typed arguments, newline escapes and source numerals checked.
- 78 host tests passed; structural validation passed for all 171 offered language options.
- 48 Java resource-render checks passed across English and Latin: 44 formatted-template checks and four literal checks for resources marked formatted=false.
- Base-tree verification checked content hashes and executable modes for all 1,252 materialized files; 218 other entries retained through the base tree.
- Priority coverage: P0 94/94, P1 249/249, P2 257/305 and P3 15/71. There are 104 priority keys still missing in Latin.

## Limits

This is a bounded translation and host-structure review, not Android compilation, AAPT, device, layout, accessibility-runtime, CI or specialist linguistic certification. No issue 1 action was retried.
