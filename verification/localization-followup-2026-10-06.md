# Localization follow-up, 6 October 2026

This is a bounded new result after the September reset, not completion of the
475-row register, its companion evidence register, or the eight-thread task.
No prior semantic, corpus or UI-verification claim is restored by this report.

## Source changes

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
that check. Resolution remains separate work; no PR has been merged here.

## Remaining scope and retrieval limits

The parent task recovered conversation excerpts and current GitHub material,
but no complete latest transcripts or exact conversation/message identifiers
for all eight discussions. Its newest located Library export ends on
18 September, before the relevant later work. This follow-up cannot establish
that all later user corrections have been reconciled.

The register's broader semantic and operational reviews remain open, including
all excluded short strings, Hakka official Sixian evidence/contextual PFS pairing,
Korean general-domain mixed-script evidence and its eight concepts, the complete
minority-language manuals, plural semantics, vertical/RTL/script rendering and
document-credit lifecycle. The identified PR9 documentation conflict remains.
None is closed by XML parity, test counts, word-presence checks or this report.
The unrelated 81 locales remain outside completion scope.
