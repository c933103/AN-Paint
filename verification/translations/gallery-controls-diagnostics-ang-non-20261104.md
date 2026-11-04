# Online gallery controls and load diagnostics: Old English and Old Norse

Base: `6c64e2c7825814c58bce975b4b25699fef168487` on `review/nv-bottom-2038-20261103`.

## Change and review

Adds 18 missing string resources per locale (36 total): 17 P2 gallery controls/diagnostics and the related P3 Credits & terms action. Canonical Android XML owns the wording. Independent review accepted all entries unchanged after examining the English source, complete drafts, existing catalogue terms, integrated XML and actual consumers.

The block preserves the selected-provider gate, artwork-page-first instruction, English-or-Japanese search hint, in-progress image fetching, unavailable image, file-size limit, unsupported image URL, redirect limit, download failure, missing component and memory failure. The missing-component notice explicitly says the image was not imported. It does not promise success or direct the user to bypass URL restrictions. Android's inability to find an app for an external link is separate from the online gallery connection-check/retry notice.

The Use image caption embedded in the artwork instruction exactly matches the label injected into provider pages. Credits & terms opens the provider's terms; its wording does not imply agreement. Current source wording is followed rather than obsolete implications in the search-English and supported-hosts key names.

## Consumer and structural checks

- All 44 direct string references in `MediaGalleryActivity` now have resources in both locales. The gallery result-validation notice in `ClassicPaintActivity` is also covered. Provider-specific descriptions and labels remain separate work; this is not whole-gallery completion or runtime verification.
- All 18 added keys per locale have actual Kotlin consumers.
- XML uniqueness, Android escaping, source attributes, ordered typed placeholders and newline escapes pass. The single `%1$s` error-detail argument and all five `formatted="false"` attributes are unchanged. The previous 616 typed resources and their bytes are preserved, with exactly 18 appended strings.
- 78 host tests passed in 15.218 seconds across translation, localized help, boundaries, current localization contracts, language note, string importance, ordinary-priority follow-through and open-review recovery.
- All 171 offered language options passed structural validation with `require_complete=False`.
- The base integration was checked against the full Git tree: 1,276 materialized files matched content and executable mode. The 172 unmaterialized research/verification records remain preserved through the base tree. Only the two locale files change in the application tree.

## Resource presence per locale

P0: 94/94; P1: 249/249; P2: 261/305 to 278/305 (27 missing); P3: 12/71 to 13/71 (58 missing). Total typed resources increase from 616 to 634: 633 strings and one plural resource. Presence counts are not whole-catalogue linguistic acceptance.

## Limits

Modern network/software terms are functional catalogue adaptations, not claims of historically attested computing vocabulary. No Android build, device/emulator, rendering, accessibility, runtime, CI or specialist/native certification is claimed. No issue tracker update is included.
