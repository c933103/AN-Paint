# AN-W05-METADATA-M03 — incomplete technical draft

## Scope and status

Baseline: `79b1f990a98eaf44c28351cd02c20157c70d8dff` (`develop`, verified 11 October 2026).
This separate increment addresses only the Commons metadata streaming-response
limit message identified as M03 in the [12-message inventory](https://github.com/c933103/AN-Paint/blob/c6fbbc7d23483a48bbef066313849129197398ce/verification/commons-metadata-message-inventory-2026-10-09/inventory.json).
It does not import the held M02 branch, change M09's individual-field limit,
change the direct-parser precondition, or close any broader localization obligation.

**Incomplete; not ready for merge or release.** The required catalogue gate stays
red for Ainu Kana (`ain-Kana`), Ainu Latin (`ain-Latn`) and Manchu (`mnc-Mong`).
No English entries have been inserted into those catalogues to force a pass.
The default plus 56 scoped catalogue proposals are present; the required target
is default plus all 59. All 140 offered tags have individual dispositions:
56 proposals, three unresolved required entries, and 81 separately enumerated
out-of-scope missing-key English fallbacks. Thus this draft currently resolves
84 offered tags through default fallback, while the strict target remains 81.

Every non-English value is a model proposal with its own rationale, confidence
and review limit. None is competent-language acceptance. Three source-assisted
low-confidence drafts (Hakka Latin, traditional Mongolian and Vietnamese Hán/Nôm)
record primary constituent terminology sources and their limits. The remaining
Ainu and Manchu research supports individual words but not a responsible complete
technical sentence. Existing catalogue wording is candidate context, not inherited
acceptance. The two pseudo catalogues are explicitly synthetic layout fixtures.
See [all-language-dispositions.json](all-language-dispositions.json).

## Technical contract

- Keep the exact byte ceiling, `2 * 1024 * 1024`, and accept exactly that many bytes.
- Raise `CommonsAttribution.ResponseLimitException : IOException` only when the
  streaming accumulator plus the next read exceeds that ceiling. It carries no
  worker-localized prose. The resource default remains exactly
  `Commons metadata exceeds the response limit`.
- Resolve this typed failure at the alive-activity UI callback for both actual
  WebView routes: Copy credit and image insertion. Do not identify errors by text.
- Preserve the unrelated HTTP reason, provider/framework messages, direct-parser
  precondition, 64 KiB attribution-field limit, stream closure, disconnect and
  active-connection clearing, temporary-file cleanup, clipboard semantics, credit
  drafts/accepted edits and retries. Existing SVG reasons remain separate.
- Exact pinned fixtures reverse only this two-file production delta and the
  individual resource additions. Historical Copy-credit, F01 and C023 hashes and
  fixtures are unchanged. Removal, duplication, content corruption, unrelated
  edits and fixture corruption are negative controls, not allowed successor scope.

## Verification and limits

`CommonsMetadataResponseLimitFlowTest` uses local fake connections and the real
WebView action callbacks, never Wikimedia requests. It covers valid UTF-8 JSON
padded to exactly 2 MiB, +1-byte rejection, stream closure/active clearing,
unrelated read/cancellation failures, both localized actions and exact-boundary
retry, unchanged unaccepted draft/clipboard/result state, UI-time resource
resolution, duplicate input, late typed failures after destruction, already-queued
success after destruction, and representative ordinary/RTL/vertical layouts at
font scales 1 and 2. Screenshots produced by these tests are Robolectric-native
renders, not installed-device captures.

`CommonsMetadataResponseLimitTranslationTest` checks the actual resource route on
API 30 and 35 for all 140 offered tags, including mixed-script Korean's internal
resource tag. Its 59-proposal/81-fallback assertions deliberately remain strict
and fail while the three required proposals are unresolved.

Local exploratory aggregate: 560 Python methods ran in 224.362 seconds, with
11 failure records, all caused by the six then-unresolved required catalogues.
The three later source-assisted proposals are not covered by that initial log.
The initial focused M03 run passed five technical/source methods and failed two
strict catalogue-completeness methods. Final-source validation is recorded
separately; no aggregate success is claimed from these exploratory logs.

The first local JVM invocation could not use the default Gradle directory. A
writable scoped directory exposed Java transport failure. Official Gradle 8.13
was then downloaded through the supported transport and verified against the
repository's SHA-256 pin:
`20f1b1176237254a6fc204d8434196fa11a4cfb387567519c61556e8710aed78`.
The existing configured proxy allowed plugin resolution. Correcting temporary
Android user-directory configuration reached the actual remaining blocker:
**SDK location not found**. No Android SDK, platform `android.jar`, `sdkmanager`,
`ANDROID_HOME` or `ANDROID_SDK_ROOT` was found in the inspected local tooling.
Local JVM compilation and runtime tests have therefore not run. An intermediate
tool-wait cancellation is retained separately and is not attributed to a user
rejection. No security/network setting was changed or access denial bypassed.

Hosted CI must establish compilation, JVM results, lint, resource generation and
applicable installed-emulator checks for the exact published source. Catalogue
failures remain real failures. A technical draft review is not full acceptance;
physical-device, competent-language and existing security/device/archive holds
remain open. No archive-producer retry, release, merge or ready-for-review action
is part of this increment.

## Exact additive font follow-through

The first synchronized 56-proposal aggregate correctly found missing bundled glyph
U+8FD4 (返) in the Vietnamese Hán/Nôm candidate. Its 560 methods finished in
213.781 seconds with six failures: this glyph failure and five failure records
for the three unresolved catalogue entries. The original failure is retained in
`all-host-final.log`; the name records that checkpoint, not current acceptance.
A subsequent independent 561-method checkpoint included the extra all-140
structural method and reproduced the same six failures.

The existing preservation-only font procedure supports the exact glyph from the
already-used, SHA-pinned Nom Na Tong v5.18 source. `extend_nom_m03_ui_font.py`
appends only U+8FD4. The new subset is 275,788 bytes, SHA-256
`4ae4cab599622f6c9d66b8a99074f2a291ffc32000a78ba69f241fc12eb64e05`.
All 734 existing codepoints, 736 existing glyphs, old outlines/metrics, cmap
identities/mappings and global/name/licence metadata remain unchanged. The old
font is restored byte-for-byte by a pinned 22-span binary reverse delta before
running the unmodified historical SVG-font oracle. The existing licence notice
and source terms are unchanged; no new source or legal agreement is introduced.
The font inventory changes only this subset digest.

Nine focused font methods pass, including current catalogue coverage and the
historical preservation check. The optional local Pillow/FreeType script checks
all 734 old glyph masks, offsets and advances at 24, 48 and 96 px (2,202 equal
comparisons). The added glyph is nonempty at all three sizes; its vector outline
and advance/bearing equal the source. With a common baseline, source/subset pixel
masks match at 48/96 px but differ at 24 px. That observed limit is retained in
`nom-render-initial-diagnostic.json` and `nom-renderer-checks.json`; universal
pixel identity to the full source font is not claimed. The subset's existing
global metrics are deliberately preserved. The comparison PNG is a local font
render, not an Android screenshot or linguistic/physical-device acceptance.

The revised source manifest contains 76 production/resource/font/test/guard paths.
Hosted validation and independent review must name this revised snapshot.

## Independent corrected-snapshot review and draft publication

The independent review approved incomplete technical-draft publication only for
source tree `4f44f466eb9ed1f90790219b51d900a4a0603e95` and source patch SHA-256
`96be917f8da57d3178637b92141de3448241ab9fc5ceb140aa2edfc6aab1ae27`, based on
`79b1f990a98eaf44c28351cd02c20157c70d8dff`. The final independent aggregate
executed 566 methods in 182.775 seconds and FAILED with five failure records,
all retained required-language completeness gates. No unexpected failures
remained. The final focused run executed 64 methods: 62 passed and two strict
completeness methods failed. See [the full review](independent-review/review.md)
and [its machine-readable summary](independent-review/review-summary.json).

Publication on 12 October 2026 preserves this reviewed source unchanged alongside
these evidence files. The published commit's full tree therefore includes more
than the source-only tree above; `source-manifest.json` binds every reviewed
production/resource/font/test/guard path. Earlier failed checkpoints are retained
as history, not current acceptance. No missing translation is waived: `ain-Kana`,
`ain-Latn` and `mnc-Mong` are still unresolved, with 56 scoped proposals and 84
actual default fallbacks (required target: 59 proposals and 81 fallbacks).

The ordinary complete API 35 pull-request workflow is the applicable hosted
validation route under `CI.md`. API 30/35 JVM resource-routing assertions remain
in the source. Local Android compilation/runtime was not established because
the SDK was unavailable; hosted results must be recorded against the actual PR
head. This draft does not claim competent-language acceptance, all-size font
raster equivalence, Android behavior, readiness, merge or release approval.
