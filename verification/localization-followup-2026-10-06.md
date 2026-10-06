# Localization follow-up, 6 October 2026

This is a bounded new result after the September reset, not completion of the
475-row register, its companion evidence register, or the eight-thread task.
No prior semantic, corpus or UI-verification claim is restored by this report.

## Initial source changes

- PR3: [two Malay smoothing labels](malay-smoothing-recheck-2026-10-06.md),
  replacing inappropriate Tagalog wording with Malay while retaining the
  distinction between stroke smoothing and pixel-edge antialiasing.
- PR8: [Traditional Mongolian legacy assembly capacity](mongolian-capacity-recheck-2026-10-06.md),
  restoring the omitted up-to-20-images sentence in the specific legacy key,
  with a regression that fails on the pre-fix resource.
- Both changes are carried into the existing integration branch. Canonical
  locale XML is edited directly. There are no generated/placeholder translations,
  new language choices, font/layout changes, or file removals in this follow-up.

## Fresh validation

| Source checked | Local result |
| --- | --- |
| PR3 `bd08a74b5` | 91 host tests pass; strict AAPT2 compilation of all module resources passes |
| PR8 `e2e79f905` | 91 host tests pass; strict AAPT2 compilation of all module resources passes |
| Integrated source `9b03b59b4` | 110 host tests pass; strict AAPT2 compilation of all module resources passes |

The suites include XML parsing, source-key coverage for their declared scope,
placeholder types/indices, literal percent handling, Android quoting, plural
structure, locale inventories and localized-help regressions. They are not
linguistic certification. AAPT2 is the official Google Maven
`com.android.tools.build:aapt2:8.13.0-13719691:linux` artifact. Full Gradle/lint and
device tests were not run locally: this environment has no configured Android
SDK/NDK. Current PR CI is reported separately; historical CI is not substituted.

Fresh per-file comparisons are in
[localization-parity-2026-10-06.tsv](localization-parity-2026-10-06.tsv).
All **57 explicitly scoped original-PR locale XML files** have the same Git blob
as the integrated source after these fixes. Every row records its original head,
integration source commit and both blob IDs. This proves byte parity at those
snapshots only; it does not prove semantic adequacy or incorporation of whole
branches. The inventory uses the supplied nine original-PR scopes, not counts
in a withdrawn completion report. Integration-only options are not included in
that 57-file comparison.

PR9's current merge conflict was examined without merging or changing it.
`git merge-tree --write-tree --name-only` between its current base
`41ac05dba279ca52ad86f952edeada2d772ff4b4` and head
`d60178949819a8fac8977ced0ba6497c84c7a90e` reports only
`translations/README.md`. The conflicting line links to different historical
records (`8cf4ed2e5` versus `97e511dc6`). No locale XML conflict was reported by
that check. The later [PR9 history-link repair](pr9-history-link-recheck-2026-10-06.md)
preserves both archive links and removes the conflict without a branch/PR merge.

## Remaining scope and retrieval limits

The parent task recovered conversation excerpts and current GitHub material,
but no complete latest transcripts or exact conversation/message identifiers
for all eight discussions. Its newest located Library export ends on
18 September, before the relevant later work. This follow-up cannot establish
that all later user corrections have been reconciled.

The register's broader semantic and operational reviews remain open. The new
continuation below gives bounded results for several of those areas; it does
not close their broader rows. PR9's documentation conflict is repaired; its
language review remains pending.
None is closed by XML parity, test counts, word-presence checks or this report.
The unrelated 81 locales remain outside completion scope.

## Continuation: source corrections and fresh bounded reviews

| Area | New result and inspectable evidence |
| --- | --- |
| PR3 Malay/Indonesian | [Short-message review](pr3-ms-id-short-review-2026-10-06.md) covered 604 Malay and 600 Indonesian short entries against source and callsites; ten additional values corrected spelling, preview terminology, decoder overhead, actual command names, whole-pixel and PDF-dimension instructions, and inaccurate completeness notes. Longer excluded entries remain explicit. |
| PR6 Hakka | [Contextual review](hakka-context-recheck-2026-10-06.md) corrected seven spatial 背 readings and four temporal 下擺 readings in ten Latin resources, and restored maintenance/fallback information in both scripts. The 58 Save resources contain 82 paired occurrences; matching counts are structural evidence only. Official current web entries/appendix and archival official ODS evidence are distinguished. |
| PR8 manuals and notes | [Mongolian review](mongolian-manuals-recheck-2026-10-06.md) corrected five keys covering partial transparency, alignment, adjacent Fit, remembered Save destination, and attribution clauses. [Four language notes](pr8-language-note-recheck-2026-10-06.md) regain the omitted maintenance sentence while preserving their existing English fallback. |
| PR12 Korean | [Context/evidence review](korean-context-recheck-2026-10-06.md) corrected nine values across KR/KP/mixed variants: actual recovery/assembly menu routes, conditional floating-selection information and English-fallback notes. All eight requested concepts received explicit contextual decisions; 91 exact dictionary rows, six component choices and 97 current examples were mechanically replayed. This is not renewed general-corpus acceptance. |
| PR4/5 crop plurals | Fresh [Lithuanian](crop-plural-recheck-pr4-2026-10-06.md), [Russian and Arabic](crop-plural-recheck-pr5-2026-10-06.md) source/category reviews found no correction warranted in the particular count messages. Counts 0–20, format arguments and callsites are recorded; runtime Android selection remains separate. |
| Shared cursor help | [Six explicitly implicated catalogues](shared-cursor-recheck-2026-10-06.md) were compared with the drawing menu, Brush category and cursor behavior. No new source defect was established in these exact messages. This does not certify whole catalogues or UI rendering. |
| Integration image credits | [CR-001–CR-024 source review](image-credit-recheck-2026-10-06.md) found two real transfer defects: pending-image copy/cut included unrelated canvas credits, and independent assembly replacement retained the old canvas credits. Both are repaired with clipboard, draft compatibility, undo/redo and dialog regression cases. Source review is distinguished from runtime assertions awaiting CI. |
| PR9 conflict | [History-link repair](pr9-history-link-recheck-2026-10-06.md) preserves both historical references. A fresh merge-tree check succeeds without conflict; no branch or PR was merged. |

The final integrated executable/resource source snapshot for this continuation
is `14286f266c34721f0d7f9f4a11b8420a0dccb602`. **115 host tests pass** and strict
AAPT2 compilation of both Paintroid and app resources passes. The additional
Kotlin/Robolectric tests require CI because no local Android SDK is configured.
The updated 57-file comparison is
[localization-parity-continuation-2026-10-06.tsv](localization-parity-continuation-2026-10-06.tsv).
All 57 original-PR catalogue blobs match this integration source snapshot.

Current external evidence limits are specific: the full pinned Korean literary
corpus download returned HTTP 403; exact civic-clause hashes and Gazette scans
were not replayed; the current Hakka ODS hash could not be obtained through the
proxy; fresh Irasutoya terms retrieval was blocked. Archived/derived data and
accessible current pages are labelled as such. Full native-language, vertical,
RTL and physical-device review remains open. The Mongolian report also records
three source/help behavior discrepancies without silently claiming them fixed.

CI results are reported for exact commits in PR descriptions and the current
CI record. Earlier successful runs do not verify later source edits.
