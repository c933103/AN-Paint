# M03 exact-head hosted runtime evidence

This evidence branch records validation of PR #54 code head
`d4ee9762580bbaf983fc58edb84755840c31626c`; it does not change that reviewed source.
GitHub's pull-request test merge `d43c6b33fdb79b93d1be137d8f332f9be579ca91` has the
same full tree `c1d65b3f0f89a8af12a9dbe69eb1824ef19e28c1`. Its two parents are
`79b1f990a98eaf44c28351cd02c20157c70d8dff` and the reviewed code head.

- [Normal API 35 workflow](https://github.com/c933103/AN-Paint/actions/runs/38191148104)
- [Clean exact-head Codex result](https://github.com/c933103/AN-Paint/pull/54#issuecomment-6116050419)
- [Language and independent technical reviews](https://github.com/c933103/AN-Paint/tree/d4ee9762580bbaf983fc58edb84755840c31626c/verification/commons-metadata-m03-languages-2026-10-12)

The `initial-*` XML and JSON preserve the first, deliberately incomplete draft:
all 12 M03 flow tests passed, while the four API 30/35 translation-test cases
correctly failed the 59-value and 81-fallback requirements (actual 56/84). They
are not successor results. Its run was superseded by the language commit.

## Rendering interpretation

The status captures are Robolectric API 35 NATIVE-graphics renders, not installed-
device screenshots. They cover both Copy credit and insertion at normal and
2× font scale on a 320×640 dp layout. Test assertions verify complete text layout,
no ellipsis and visible/reachable status text; vertical rails are checked at both
ends. A still can show the last tested scroll position because resetting the rail
requests a later layout. A still therefore does not by itself prove that every
column is simultaneously visible. The per-capture metadata and test assertions
must be read together.

The selected Ainu, Manchu and Vietnamese Hán/Nôm captures address the new wording
and added 返 glyph. The ordinary API 35 installed test separately checks every
bundled font asset's digest and actual Typeface load. It does not directly
exercise this M03 status message on an installed device. That is a disclosed
coverage limit, not evidence of a rendering defect.

The earlier Pillow comparison to the full primary Nôm font differed at 24 px,
while the subset's old-glyph renders were unchanged and the new outline/metrics
matched the source. Pixel equivalence to a different full font at every size is
not an M03 requirement. A missing, corrupt, clipped or unreadable glyph in the
actual app font would be a defect; no such conclusion follows from that isolated
source/subset pixel difference. No broad font replacement is proposed.

The independent three-language recommendations remain moderate-confidence,
source-assisted contextual paraphrases. This report does not claim native
certification, every dialect's preferred wording, or universal device behavior.
Readiness and merge are separate owner decisions.

## Verified hosted result and collection failure

Hosted Python: **568 pass**. Hosted JVM: **820 pass**, no failures/errors/skips,
including all 12 M03 flow cases and four API 30/35 resource-routing/completeness
cases. Lint, APK/source build and exact-script resource generation passed.
`runtime-summary.json` binds the reports and all 48 screenshot hashes.
[Independent visual review](visual-review/REVIEW.md) found no actionable M03
rendered-status defect in the 16 selected captures.

The first API 35 attempt passed **74 native tests and all 25 app tests**, including
the every-font asset hash/Typeface load check. Its overall job still FAILED:
cleanup could not finish pulling the vertical-locale screenshot exports. The
73-byte pull log contains only the first progress update (2% overall, 8% of the
qaa ZIP); no detailed error or child exit status was recorded. The failure was
within about a second, not the 15-second deadline. The collector/exporter is
unchanged from the green baseline run 38129685199; no deterministic M03 or
collector defect is evidenced by this failed transfer.

`api35-attempt1/` preserves the failed pull log, startup timeline, complete native
summary, app-union receipt and bounded diagnosis. A single failed-job-only retry
was accepted on the same source head. Green jobs retain their original execution
timestamps; only the API 35 job executes again. At this evidence checkpoint the
second attempt is in progress. The failed collection gate is not suppressed,
and passing instrumentation alone is not claimed as full CI success.
