# AN-W04: native gallery prose lacks vertical rendering

## Confirmed defect and baseline

Observed at PR #29 commit `afbb8015130dd82546a4c22a9d3337782f7b995f`.
`MediaGalleryActivity` built `gallery_status` and `gallery_description` as ordinary
TextViews and installed only locale fonts. API30/35 native-host PNGs show Mongolian
and Manchu prose in horizontal rows, including both SVG failure reasons at 1×/2×.
All 16 vertical baseline captures are diagnostic evidence, not accepted layout.

Reproduce: choose `mn-Mong` or `mnc-Mong`, open Wikimedia Commons, invoke the real
import link for an SVG with only percentage dimensions or a dimension above the
supported integer range, and inspect the persistent gallery error. Baseline
artifacts are the `svg-error-readability` report from PR #29 exact-head CI.

## Bounded repair

Apply the existing `VerticalUi.caption` renderer and `ColumnScrollView` to native
gallery description and persistent status. Direction comes from the shared script
policy, covering all Mong-script locales, Literary Chinese and both test-only
vertical pseudo-locales. Horizontal languages retain ordinary TextView rendering.
New messages reset to the first reading column, including right-to-left columns.
The underlying text remains accessible, and persistent status is a polite live
region. There are no new user-facing strings, translation values or font changes.

The surrounding fixed-height controls are a distinct finding and source commit.

## Regression and evidence limits

`GalleryVerticalStatusTest` exercises API30/35, five vertical profiles, both real
SVG failure paths and method-level system font scale 1×/2×. It checks the actual
full-text ReplacementSpan, source text exposed to accessibility, shared direction,
measured complete columns, both horizontal scroll endpoints and repeated-message
reset. Its PNG/JSON evidence uses `build/reports/gallery-vertical-status` so it
cannot overwrite the separate SVG diagnostic captures. Existing SVG text/no-
substitution/persistence checks remain intact.

Native-host rendering must be run in CI and visually inspected after publication.
Compilation, physical-device gestures, TalkBack and fluent-language acceptance are
not established by source review or the local Python checks.

## Candidate visual-review correction

The first full candidate captures exposed repeated painting of the provider
caption because its inserted newline crossed one atomic vertical span. The
[gallery-only separator correction and native paragraph regression](review-description-paragraph.md)
remain part of this finding. Passing status tests alone did not establish the
separate description's visual acceptance.
