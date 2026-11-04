# Commons diagnostics: Old English and Old Norse

Base: `fe708eb5df4a4e6b6128caf2938e87a42d587479` on `review/nv-bottom-2038-20261103`.

## Change and review

Adds 17 missing P2 string resources per locale (34 total): 16 translated prose labels/diagnostics and one unchanged technical caption, `SVG > 32 MiB`, in each of `values-b+ang` and `values-b+non`. Canonical Android XML owns the wording. Independent review accepted all 34 unchanged after checking the English source, catalogue terminology, complete drafts, integrated resources and actual consumers.

The block covers metadata-only credit copying, HTTP status, response and individual-field limits, query failure, non-file pages, unresolved file identity, unavailable metadata, attribution/original-file mismatch, invalid attribution pages, retention failure, download redirects to a different original, and PNG encoding failure. These remain distinct diagnoses; none claims successful import, verified permission or deletion of existing credits. The blank-map label retains the existing catalogue map terminology. Technical vocabulary remains a modern adaptation rather than a claim of historically attested computing terms.

`MediaGalleryActivity.copyCommonsCredit` fetches metadata without image bytes or a registered insertion. `commonsMetadataReason` maps typed failures at the UI boundary; its already-localized reason is substituted once. `CommonsAttribution` checks the original source path, file page, response/field limits and cache commit. `BlankMapSvg` separately reports PNG encoding failure. All Commons-prefixed direct resource references in the Kotlin sources now have resources in both locales; this does not assert whole-gallery coverage or runtime verification.

## Checks

- 78 host tests passed in 49.876 seconds across the translation, localized-help, translation-boundary, current-localization-contract, language-note, string-importance, ordinary-priority and open-review-recovery suites.
- All 171 offered language options passed structural validation with `require_complete=False`.
- XML uniqueness, Android escaping, source attributes, ordered typed arguments and newline escapes passed. Each locale preserves all 599 prior typed resources and their bytes, appending exactly 17 strings.
- Two `%1$s` occurrences per locale remain: HTTP status and failure reason. The SVG limit, units and comparison symbol are unchanged. No formatting flags or newline escapes were added.
- The integration base was checked against the Git tree: 1,276 materialized files matched content and executable mode. The 171 unmaterialized research/verification documents are retained through the verified base tree. The only changed application files are the two locale XML files.

## Resource presence per locale

P0: 94/94; P1: 249/249; P2: 244/305 to 261/305 (44 missing); P3: 12/71 (59 missing). Total typed resources rise from 599 to 616: 615 strings and one plural resource. Counts describe direct presence, not whole-catalogue linguistic acceptance.

## Limits

No Android build, device/emulator, rendering, accessibility, runtime, CI or specialist/native certification is claimed. No issue tracker update is included.
