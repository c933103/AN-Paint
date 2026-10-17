# Commons/import application failures

This implementation externalizes M01 and M05–M12 from the
[remaining-message inventory](https://github.com/c933103/AN-Paint/blob/c6fbbc7d23483a48bbef066313849129197398ce/verification/commons-metadata-message-inventory-2026-10-09/README.md).
M02–M04 retain their existing typed implementations and translations.

## Runtime contract

`CommonsImportFailure` identifies application-owned failures without carrying
English text or resolving resources on a worker. Invalid file pages and
original-download mismatches remain `IllegalArgumentException`; metadata,
cache and PNG-encoding failures remain `IOException`. The existing alive UI
callbacks resolve a complete resource value, then insert it into the existing
Copy credit or image-insertion wrapper exactly once. Untyped provider/framework
messages, including whitespace and percent sequences, retain their existing
handling.

The metadata request, response and field limits, attribution field identities,
HTML/link policy, licence/source URLs, cache schema, original-file identity
checks, SVG dimensions, clipboard/edited-credit policy and lifecycle guards are
unchanged. M01 is normally guarded at entry; insertion can still reach it after
its existing page truncation. That behavior is covered, not broadened or fixed
as part of this localization slice.

## Locale applicability and review

All 171 offered tags are functionally applicable to these shared paths. The
current catalogue contract retains 59 scoped tags and 112 explicitly open
fallback tags. The nine keys therefore require 531 scoped entries, in addition
to nine defaults; the other 1,008 tag/key pairs remain outside the bounded batch.
English regional entries and the private-use English/layout conventions are
reviewed as such, not counted as foreign-language translations.

`tools/fixtures/current_localization/commons_import_failures_current_wording.json`
records exact implemented complete values. A tag absent from a key's fixture
uses the English default and remains untranslated for that key. Missing scoped
values still fail the unchanged catalogue-completeness gates. Do not copy
English into an unresolved foreign-language catalogue or substitute a neighboring
language/script to obtain a passing key count. Add independently reviewed
complete values and their exact fixture entries together; preserve per-language
review limitations.

The keys and translation constraints are:

- `commons_metadata_not_file_page`: invalid Commons file-page precondition.
- `commons_metadata_ambiguous_file`: zero **or** multiple returned file pages.
- `commons_metadata_unavailable`: missing file, absent namespace or non-file namespace.
- `commons_metadata_original_mismatch`: attribution describes a different original image.
- `commons_metadata_invalid_page`: invalid provider file-description page URL.
- `commons_metadata_field_too_large`: raw HTML field exceeds 64 Ki UTF-16 units, before decoding.
- `commons_metadata_cache_failed`: metadata snapshot could not be retained, not a drawing/clipboard failure.
- `commons_download_original_mismatch`: an allowed redirect changes the original image; insertion only.
- `commons_svg_png_encode_failed`: PNG encoding returned false; SVG insertion only.

None of the nine values has a placeholder. Commons and PNG retain their service
and format identities. Provider attribution and licence text is not translated.

## Regression checks and remaining acceptance

`CommonsImportFailureFlowTest` exercises the production producers and WebView
actions with fake local connections, including empty/multiple responses,
namespace variants, exact UTF-16 boundaries, cache commit false, page truncation,
redirect identity and PNG compression false. A context wrapper and a Bitmap
shadow provide the last two deterministic failures only in test code. Assertions
cover unchanged document/clipboard state, connection/stream/bitmap/file cleanup,
retry, duplicate suppression, rotation, queued callback language resolution and
destruction. The PNG shadow retains native Bitmap behavior for other calls.

`CommonsImportFailureTranslationTest` resolves all offered tags through
`AppLanguage` on API30 and API35 and keeps the exact `ko-Kore-KR` private-resource
identity diagnostic separate from ordinary `ko-KR`. The flow test supplies
portrait 1× and short-landscape 2× text/accessibility/layout/scroll checks and
native Robolectric captures for representative scripts. These require execution
and visual inspection; test source is not evidence of a passing render, installed
device behavior, TalkBack speech or native-language acceptance. The existing
M02–M04, untyped-error, clipboard and SVG-size tests remain complementary.

Run focused Python contracts first, then the normal and optimized full host
suites in `CI.md`; use the repository wrapper for Android unit tests, lint and
builds. Keep incomplete translation, failed, timed-out and unrun stages explicit.
Use exact-head hosted results when the local SDK/toolchain is unavailable.
